# Change request — audit SCAD build decisions against changed inputs

## Requested change

Add a post-build audit capability to `brainboxemb/tool.scad-project`.

The audit receives:

1. an existing structured SCons build-decision report;
2. an explicit list of changed input paths.

It checks whether each observed target outcome is compatible with impact that can be **proven** from the target's recorded source/dependency list.

The first implementation is deliberately conservative. It must detect clear contradictions without trying to reproduce SCons dependency analysis or infer impact that cannot be proven from the available evidence.

## Current behaviour

`tool.scad-project` already writes `scad-project.build-decisions` schema version 1 reports for SCons builds.

Each target already records:

- `output`;
- `outcome`: `BUILT`, `CACHE_RESTORED`, `CURRENT` or `ERROR`;
- `sources`: the known OpenSCAD source/dependency paths for that target;
- `target_spec_digest`;
- execution/output-state observations.

The deterministic real-SCons conformance suite already proves the build engine reacts correctly to private/shared dependency changes, target-spec changes and cache states.

What is missing is a separate check that can answer, after a build:

> Given the paths that changed, does the structured target outcome contradict anything we can prove from the recorded dependency evidence?

## Behaviour after the change

A new audit command reads the build-decision report and changed paths, evaluates every target, writes a machine-readable audit report and exits non-zero only for proven correctness failures or invalid evidence.

### Example

Target report:

```json
{
  "output": "bld/png/frame.png",
  "outcome": "CURRENT",
  "sources": [
    "dsg/openscad/render/frame.scad",
    "dsg/openscad/components/corner.scad"
  ]
}
```

Changed path:

```text
dsg/openscad/components/corner.scad
```

The changed path exactly matches a recorded source/dependency of the target. Impact is therefore proven. `CURRENT` is incompatible with that proven impact, so the audit fails.

If the same target had outcome `BUILT` or `CACHE_RESTORED`, the audit passes.

## Ownership

### `tool.scad-project`

Owns:

- parsing/validating SCAD build-decision evidence;
- matching changed paths against recorded SCAD target sources;
- audit policy and result schema;
- CLI command;
- owner tests and documentation.

### Outside `tool.scad-project`

Determining **which repository paths changed** is not part of this change.

The audit accepts changed paths as explicit input. It must not introduce its own generic `git diff` implementation or GitHub-event interpretation. Generic change discovery can later be supplied by repository/workflow tooling.

## Proposed implementation

### New module

Add:

```text
src/scad_project/build_decision_audit.py
```

The module should contain pure policy/evaluation functions so most behaviour can be tested without running SCons or Git.

Suggested public shape:

```python
def audit_report(
    decision_report: dict,
    changed_paths: list[str],
) -> dict:
    ...
```

Supporting helpers may normalize paths and evaluate one target.

### New CLI command

Add to `src/scad_project/cli.py`:

```text
scad-project build-audit \
  --report .cache/scad-project/state/last-build.json \
  --changed-path dsg/openscad/components/corner.scad
```

`--changed-path` is repeatable.

Also support a newline-delimited file for automation:

```text
scad-project build-audit \
  --report .cache/scad-project/state/last-build.json \
  --changed-paths-file .cache/scad-project/changed-paths.txt
```

Both sources may be combined; duplicates are removed after normalization.

The command writes the audit report to a default path next to normal state, for example:

```text
.cache/scad-project/state/last-build-audit.json
```

An explicit `--output` option may override that path.

### Input validation

The first version accepts only:

```text
schema = scad-project.build-decisions
schema_version = 1
```

Reject malformed reports, unknown target outcomes and target entries without a usable `output`/`sources` shape. Do not silently reinterpret incompatible future schemas.

Changed paths are normalized to forward-slash repository-style paths where possible. Matching in the first version is exact after normalization.

Do not add glob matching or heuristic basename matching.

### Impact classification

Per target, classify only:

- `PROVEN` — at least one changed path exactly matches an entry in `target.sources`;
- `NO_PROVEN_IMPACT` — no changed path matches a recorded source.

`NO_PROVEN_IMPACT` does **not** mean the target is proven unaffected. It means this audit does not have evidence to prove impact.

This distinction is required so missing evidence cannot become a false correctness failure.

### Outcome policy

| Impact | Outcome | Audit result | Reason |
| --- | --- | --- | --- |
| `PROVEN` | `BUILT` | pass | affected target was rebuilt |
| `PROVEN` | `CACHE_RESTORED` | pass | affected target was materialized for the matching SCons signature |
| `PROVEN` | `CURRENT` | fail | proven affected target was left unchanged |
| `PROVEN` | `ERROR` | fail | build evidence is already erroneous |
| `NO_PROVEN_IMPACT` | `CURRENT` | pass | no contradiction can be proven |
| `NO_PROVEN_IMPACT` | `CACHE_RESTORED` | pass | fresh/missing output may legitimately be restored without a proven source change |
| `NO_PROVEN_IMPACT` | `BUILT` | warning | possible overbuild, not a correctness contradiction |
| `NO_PROVEN_IMPACT` | `ERROR` | fail | build evidence is already erroneous |

Warnings must not make the command fail in the first version.

### Audit report

Use a separate schema:

```text
scad-project.build-decision-audit
schema_version: 1
```

Top-level fields should include at least:

- source decision-report identity/schema;
- normalized `changed_paths`;
- counts for pass/warning/fail;
- per-target audit entries;
- overall `result`: `PASS` or `FAIL`.

Per-target entries should include at least:

- `output`;
- original `outcome`;
- `impact`: `PROVEN` or `NO_PROVEN_IMPACT`;
- `matched_changed_sources`;
- `audit_result`: `PASS`, `WARNING` or `FAIL`;
- stable machine-readable `reason` code.

Suggested reason codes:

```text
PROVEN_BUILT
PROVEN_CACHE_RESTORED
PROVEN_LEFT_CURRENT
TARGET_ERROR
NO_PROVEN_IMPACT_CURRENT
NO_PROVEN_IMPACT_CACHE_RESTORED
POSSIBLE_OVERBUILD
```

Human-readable console output is secondary to this structured contract.

### Exit behaviour

- exit `0`: audit report is valid and contains no `FAIL` target;
- exit `1`: a proven contradiction, target `ERROR`, invalid report or invalid audit input exists.

Warnings alone exit `0`.

## Integration boundary for the first slice

Do **not** automatically call the audit from `scad-project build` yet.

Reason: the build command does not currently own a reliable generic source of changed repository paths. Keeping the audit as an explicit post-build command makes the SCAD policy independently testable without embedding Git/event semantics in the domain tool.

The first slice is complete when the capability itself is stable and machine-readable. A later integration step can provide changed-path input from generic repository/workflow tooling and invoke the audit automatically.

## Required tests

Add focused unit tests for the pure audit policy:

1. changed direct source + `BUILT` → pass;
2. changed transitive source + `BUILT` → pass;
3. changed source + `CACHE_RESTORED` → pass;
4. changed source + `CURRENT` → fail;
5. changed source + `ERROR` → fail;
6. unrelated changed path + `CURRENT` → pass;
7. unrelated changed path + `CACHE_RESTORED` → pass;
8. unrelated changed path + `BUILT` → warning, overall command succeeds;
9. target `ERROR` without proven impact → fail;
10. multiple changed paths with one matching source → proven impact;
11. duplicate/path-separator variants normalize deterministically;
12. invalid report schema/version/outcome → fail closed.

Add CLI tests for:

- repeatable `--changed-path`;
- `--changed-paths-file`;
- default and explicit audit output path;
- exit 0 for pass/warnings;
- exit 1 for failures.

The existing deterministic real-SCons conformance suite remains the build-engine contract. Do not duplicate that full matrix in the audit unit tests.

## Acceptance criteria

The change is accepted when:

1. `tool.scad-project` exposes the explicit `build-audit` command;
2. the command consumes schema-v1 build-decision reports without console scraping;
3. exact changed-source matches produce `PROVEN` impact;
4. `PROVEN + CURRENT` fails;
5. `PROVEN + BUILT/CACHE_RESTORED` passes;
6. possible overbuild produces a warning but not a failure;
7. invalid/unknown evidence fails closed;
8. the audit writes a documented schema-v1 structured report;
9. owner unit/CLI tests cover the scenario matrix above;
10. no generic Git-diff implementation or SCons reimplementation is introduced.

## Explicitly deferred

Not part of this first implementation:

- automatic changed-path discovery;
- comparison with a previous target-spec baseline;
- proving impact caused only by backend/tool signature changes;
- independent artifact-content integrity checks for cache restores;
- warning-to-error policy for overbuild;
- automatic Build/Verify workflow enforcement;
- consumer-library rollout.

Those can only be added after the first audit contract is proven and a concrete need is demonstrated.
