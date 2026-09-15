# Migration 005 — validated target architecture

Status: **validated — migration implementation in progress**

## Why this document exists

This is the primary technical design for Migration 005. Read this when you need to understand **how the target SCAD execution architecture works**: Moon responsibilities, inherited capabilities, the SCons boundary, runtime selection, cache identity, GitHub Actions and publication.

You do not need the earlier design history to use this document. The reasoning that led here is kept separately in [03 — Architecture reflection](03-architecture-reflection.md) and [04 — Alternatives and decision](04-architecture-decision.md). The active owner-by-owner rollout is in [06 — Implementation plan](06-implementation-plan.md).

Related evidence:

- [10 — Measured evidence](10-measurements.md)
- [18 — Moon inheritance validation](18-moon-inheritance-validation.md)
- [19 — Human-understandability validation](19-human-understandability-validation.md)
- [20 — Target resource budget](20-target-resource-budget.md)

## 1. Maintainer model

A SCAD repository maintainer should normally think about only the capabilities the repository actually provides.

`lib.scad.clamps`:

```text
Design documentation
Verification
```

`lib.scad.hub75`:

```text
Presentation renders
Design documentation
Verification
```

A maintainer should not hand-maintain separate Moon tasks for Build indexes, current source/tool information, source-impact graph roots, publication graph roots, cache transport or publication staging.

## 2. Responsibility split

```text
GitHub Actions
  event, exact source/base, credentials, hosted runner
        |
        v
Moon on host
  determine affected SCAD capabilities once
  none -> stop before CAD image/runtime
        |
        v
one capability-appropriate SCAD runtime
  Moon executes or restores required whole capabilities
        |
        +-- tool.scad-project capability command
               |
               +-- direct execution, or
               +-- SCons fine-grained targets when configured
        |
        v
host finishing/publication
  current source/tool/run information
  compact retained evidence
  Build/Verification branch publication
```

The normal design uses one heavy hosted runner and one CAD runtime.

## 3. Moon role

Moon stays for two measured reasons.

### Change-impact selection

Before Docker, Moon answers:

```text
Which coarse SCAD capabilities are affected by base -> source?
```

An unrelated change can therefore finish without acquiring the CAD image.

`tool.git-project v0.2.8` exposes the complete affected-task set from the existing single Moon query. `tool.scad-project v0.14.0` interprets the relevant SCAD capability IDs from that result instead of reducing the decision to one aggregate boolean.

The v0.2.8 interface still takes one existing task as a query anchor. The complete affected-task list itself is repository-wide and is not limited to that task. The first Migration-005 reference consumers all expose `scad.docs`, so the v0.14.0 workflow uses `consumer:scad.docs` as the current anchor. Removing that interface requirement is a possible later generic improvement if repositories without docs need this lifecycle; it must not reintroduce a second changed-path calculation.

### Whole-capability reuse

Moon may restore a complete source-derived capability result when task identity matches.

This was validated on a fresh runner. The earlier cache failure was caused by our broad `tools/tool.scad-project/**` input admitting generated `.pyc` files; it was not a Moon cache-model failure.

Shared policy therefore uses explicit source-controlled tool inputs and production sets `PYTHONDONTWRITEBYTECODE=1` as an additional runtime safeguard.

### Affected capabilities versus publication-safe materialization

Step-3 implementation exposed one important correctness refinement: **source impact and local materialization are related but not always identical**.

`scad.docs` and `scad.build` can both contribute to one complete generated Build publication tree. If only docs changed on a fresh runner, publishing a tree containing only the newly generated documentation would replace the branch and delete unchanged presentation output.

Therefore the lifecycle distinguishes:

```text
affected capabilities
  what source changes say actually changed

materialization capabilities
  what must exist locally to publish a complete changed output family
```

For example:

```text
affected:        scad.docs
materialization: scad.docs + scad.build
publication:     Build
```

The unchanged contributor normally hydrates from Moon's whole-capability cache. If that cache entry is absent, Moon may safely reproduce it. It remains explicitly non-affected; the extra work exists only to make the replacement publication tree complete.

Verification is a separate publication family and is not pulled into Build merely for completeness.

## 4. Shared Moon policy ownership

Standard SCAD tasks live in pinned `tool.scad-project` and are inherited through Moon's native workspace task inheritance.

Validated shared capabilities:

```text
scad.docs
scad.build
scad.verify
```

Shared policy owns:

- capability command;
- common stable config/tool inputs;
- standard output boundary;
- Moon cache policy.

Consumer repositories declare only:

1. which capabilities they expose;
2. project-specific source-impact patterns;
3. exceptional output overrides only when they intentionally depart from the standard lifecycle roots.

The validated inheritance form is a single link such as:

```yaml
extends: '../../tools/tool.scad-project/moon/tasks/scad.yml'
```

No custom YAML generator is required.

## 5. Project intent and consistency

`project.scad.yml` remains the SCAD-domain project model. It already describes items such as:

- Build/output roots;
- presentation render root;
- Verification commands/output root;
- OpenSCAD/PythonSCAD configuration;
- selected build engine;
- publication branches/policy.

The reduced Moon model complements that with the visible capability set and source-impact boundaries.

Shared validation rejects contradictions between the two representations. At minimum:

- presentation/render configuration and `scad.build` agree;
- Verification configuration and `scad.verify` agree;
- PythonSCAD configuration implies the full/dual runtime;
- OpenSCAD-only configuration permits the focused runtime;
- `build_engine: scons` controls applicable normal SCons-cache handling;
- direct projects do not transport SCons caches;
- separate Verification-SCons transport exists only when SCons is selected and actual verification render/export targets populate that cache;
- non-standard output roots provide compatible Moon output overrides.

## 6. Runtime image family

One `docker.scad-toolchain` repository owns one related image family from one multi-stage source.

### OpenSCAD-focused profile

Contains the normal OpenSCAD production contract, including:

- OpenSCAD;
- BOSL2;
- documentation tooling;
- Pillow/watermark support;
- SCons;
- required system/runtime tools.

### Full/dual profile

Is the OpenSCAD profile plus:

- PythonSCAD;
- pybosl2;
- Shapely;
- related PythonSCAD dependencies.

Validated compressed sizes:

- OpenSCAD-focused: 328,098,501 bytes;
- full/dual: 449,516,893 bytes.

OpenSCAD-only work therefore avoids about 121 MB / 27% of full-image compressed distribution.

Runtime selection is derived from effective project capabilities/configuration, never a repository-name allowlist.

The two-profile family is released as `docker.scad-toolchain v0.5.0`.

## 7. SCons role

SCons is optional fine-grained target reuse inside capabilities that explicitly select it.

```text
Moon
  decides/reuses a whole capability

SCons, when configured
  decides/reuses individual targets inside that capability
```

Evidence distinguishes the reference cases:

- clamps: direct engine; no useful SCons cache exists;
- HUB75: SCons engine; normal SCons cache is populated and warm reuse is effective.

The workflow does not restore/save SCons caches for direct projects merely because SCons support exists elsewhere in the ecosystem.

A separate Verification SCons cache exists only when the SCons engine plus real Verification render/export targets populate it. Command-only Verification does not justify that transport.

## 8. Source identity versus current-run information

Source-derived cached capability output depends only on stable source/tool/config state.

Values such as these do not define Moon source identity:

```text
GitHub run id
PR number
current ref
publication branch/context
```

After capabilities are executed or restored, shared host finishing adds truthful current source/tool/run information required for publication.

This preserves both reusable source output and accurate current-run evidence.

## 9. GitHub Actions role

GitHub Actions is a thin lifecycle/credentials shell:

1. resolve exact source and comparison base;
2. ask Moon once which capabilities changed;
3. stop when no configured SCAD capability changed;
4. select one runtime image from effective project capability/configuration;
5. restore only applicable caches;
6. execute/hydrate affected capabilities plus any unchanged contributors required for a complete changed publication family, in one Docker process;
7. validate output;
8. add current-run information;
9. publish/retain output according to explicit policy.

Repository-specific CAD logic does not belong in the reusable workflow.

## 10. Normal artifact policy

Normal successful production does not need duplicate complete Build/Verification Actions artifacts because same-job publication already uses local staging trees.

Default policy:

- retain compact impact/orchestration evidence;
- publish generated Build/Verification branches;
- do not upload complete normal output trees again merely for retention.

A future manual-download/non-publication use case may opt in explicitly.

Release is different: its separate Build/Verify/finalize jobs require exact-source cross-job artifact hand-off, so release artifacts remain mandatory.

## 11. Publication

Build and Verification publication remain separate logical outputs, but the released publisher is isolated per call and can safely run concurrently on the same host.

Validation proved two publications can overlap, publish correct independent branch trees and clean up without a second runner.

The target therefore allows same-runner publication overlap when useful. It does not add another hosted runner for finishing work.

Only output families whose source-affected capabilities changed are published; publication-safe materialization of an unchanged contributor does not by itself trigger another output family.

## 12. Resource/latency objective

The architecture optimises two axes separately:

- feedback latency;
- total compute/resource demand.

It prefers, in order:

1. eliminate work;
2. reuse work at the appropriate layer;
3. reduce image distribution cost;
4. overlap independent finishing work on the same runner;
5. add heavyweight parallel infrastructure only if later measured requirements justify its extra resource cost.

The detailed acceptance budget is in [20 — Target resource budget](20-target-resource-budget.md).

Publication-safe hydration can occasionally materialize one unchanged contributor that source impact alone would not select. This is a correctness requirement of complete branch replacement, not an invitation to execute the entire graph. Its actual cache-hit/rebuild cost must be included in Step-4/5/6 measurements rather than hidden from the resource comparison.

## 13. Human-understandability result

The selected model passes the Migration-005 inspection test.

With a consumer repository plus this architecture page, a maintainer can identify:

- repository capabilities;
- change-impact boundaries;
- why Moon exists;
- why an unchanged Build-family contributor may occasionally be hydrated for complete publication;
- when SCons exists;
- runtime profile choice;
- cache scopes;
- why current-run information is outside cached source identity;
- why publication stays outside Docker;
- where latency/resource cost is concentrated.

See [19 — Human-understandability validation](19-human-understandability-validation.md).

## 14. Deliberately rejected long-term models

### Seven/eight lifecycle tasks copied into every consumer

Rejected. Generic finishing mechanics are not repository capabilities.

### Moon only as a boolean pre-Docker gate

Rejected as the preferred model. Stable Moon whole-capability reuse is proven and the affected query already knows more than one boolean.

### Remove Moon entirely

Rejected. Change-impact value and whole-capability reuse are both measured.

### Return to two heavy hosted jobs merely to regain latency

Rejected as the default. It duplicates runner/image/runtime setup. Migration 005 first removes work and uses same-runner/internal overlap.

## 15. Validation and implementation outcome

Architecture validation is complete:

- Moon change-impact value — passed;
- stable Moon whole-capability cache — passed;
- SCons optional/fine-grained boundary — passed;
- warm HUB75 SCons reuse — passed;
- two-profile runtime image family — passed and released as `v0.5.0`;
- normal artifact retention decision — complete;
- same-runner concurrent publication — passed;
- native shared Moon task inheritance — passed;
- concrete clamps/HUB75 reduced consumer model — passed;
- human-understandability inspection — passed;
- latency/resource budget — established.

The first shared implementation layers are also released:

- `tool.git-project v0.2.8` — exact source `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.0` — exact source `3178a42453a5cb7439c11a6416fc9596477ac304`, tagged Test `35011547837` green.

The remaining work is the consumer/canary migration sequence in [06 — Implementation plan](06-implementation-plan.md), starting with `template.scad-project`.

`2026-009-01.cad.HUB75-display-frame` remains intentionally deferred until the shared tools and both reference canaries are released and qualified.
