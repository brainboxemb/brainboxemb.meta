# Migration 005 — simplify the SCAD execution architecture

Status: **active — reopened for final rollout/release gates**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Status-correction issue: [#64](https://github.com/brainboxemb/brainboxemb.meta/issues/64)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this folder exists

Migration 005 changed the shared current-generation SCAD execution model from a lifecycle-heavy Moon configuration into a capability-oriented architecture that is easier to reason about and uses hosted compute more proportionately.

The architecture, shared-tool releases, canary modes, exact-source/provenance qualification and performance/resource evidence are complete. The first closeout was nevertheless premature: repository verification on 2026-09-16 found that the final qualified template state had not been released and the HUB75 frame had not been advanced from the earlier v0.14.3 consumer contract to the final v0.14.7 semantic-caller/thin-release contract before project release.

Migration 005 therefore remains active until those two release gates are satisfied. This reopening does **not** reopen the architecture decision.

Classic CAD repositories are intentionally not part of this rollout. `repositories/catalog.yml` classifies those separately as classic standalone/shared-actions projects. Moving them to the current project-tooling generation would be a separate migration.

## Remaining closeout gates

1. **Template release**
   - current qualified main: `cb1e3e50e5e56644153cdf74b54b5da1e747c8d8` on `tool.scad-project v0.14.7`;
   - current published release: `v0.0.4`, from pre-v0.14.7 source `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9`;
   - required: publish a new immutable template release (expected `v0.0.5`) using the shared v0.14.7 release flow and verify release assets plus `rel/v0.0.5/{build,verification}`.
2. **HUB75 frame final alignment and release**
   - current migrated main: `61da023ff0f6bc353687b55a8158e75ebd70b046` on `tool.scad-project v0.14.3`;
   - current Production/Release callers still use the old exact-SHA/consumer-local release orchestration;
   - current published project release: `v0.0.1`, from the old v0.9.8 generation;
   - required: advance to released `tool.scad-project v0.14.7`, use semantic reusable-workflow refs plus exact gitlink identity, collapse Release to the thin shared caller, requalify normal/zero-runtime/provenance behavior, then publish the next immutable frame release (expected `v0.0.2`).

Only after both gates are green may the final measurements/evidence be updated and Migration 005 closed again.

## Read this migration

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope, intent and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected Moon/SCons/runtime/lifecycle design. |
| [06 — Implementation plan](06-implementation-plan.md) | Owner-by-owner rollout and evidence gates. |
| [10 — Measurements](10-measurements.md) | Baseline experiments plus implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource and latency review. |

The durable current architecture is documented under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This folder remains the change/evidence record.

## Selected architecture in one view

```text
GitHub Actions host
  exact source/base, event context, credentials
        |
        v
one generic Moon affected query
  [] -> stop before planner/CAD image/runtime
        |
        v
SCAD execution plan
  validate capabilities/config
  choose focused/full runtime
  choose only applicable cache transport
        |
        v
at most one CAD runtime
  Moon executes or restores required whole capabilities
        |
        +-- tool.scad-project capability command
               |
               +-- direct execution, or
               +-- SCons fine-grained targets when configured
        |
        v
host finishing/publication
  exact source provenance
  durable timing/log evidence
  isolated Build/Verification publication
```

Maintainer-facing capabilities remain deliberately small:

```text
scad.docs    design documentation
scad.build   presentation renders, when present
scad.verify  Verification
```

Shared commands, stable common inputs, output boundaries and cache policy live in `tool.scad-project`. Consumers select the capabilities they actually have and add only project-specific source-family impact rules.

## Released shared foundations

- `docker.scad-toolchain v0.5.0`
  - full/dual: `ghcr.io/brainboxemb/scad-toolchain:v0.5.0`
  - focused: `ghcr.io/brainboxemb/scad-toolchain-openscad:v0.5.0`
  - source `a56a3aae4b9e0494e6625e75002d96b0a55986a3`
  - external qualification `34999654405`
- `tool.git-project v0.2.8`
  - exact source `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`
- `tool.scad-project v0.14.7`
  - exact source `3935e5f86fe309b8908a05554f7ada336a6d6886`
  - released-tag owner test `35084470257`

The Step-3 lifecycle started at v0.14.0 and was hardened through owner-repository patches rather than consumer workarounds. Important corrections included clean planner installation, correct Moon inherited-task placement, optional output handling, exact base-gitlink retrieval for shallow comparisons, semantic reusable-workflow refs, shared release-request handling, immutable-runtime `python3`, durable timing/log navigation and exact PR-head publication provenance.

## Current-generation rollout state

### `template.scad-project`

- final v0.14.7 qualification head `78a000603d6a64d2b495f6e054686a128c157877`;
- qualification run `35085388134` green;
- merged as `cb1e3e50e5e56644153cdf74b54b5da1e747c8d8`;
- post-merge main run `35085631904` green;
- README-only zero-runtime probe `35085786014` green;
- publication info, run context, Moon materialization and producer evidence all identify the exact assessed PR-head source revision;
- **pending:** immutable project release of this final qualified state.

### `lib.scad.clamps` — full/dual runtime + direct engine

- migration PR #16 merged as `a44d7bdfdb3407959b5d96bef654568367e0f43c`;
- canary run `35026709686` green;
- migrated main run `35065375255` green;
- README-only zero-runtime run `35065514152` green;
- immutable v0.1.4 released;
- direct engine correctly transports no normal or Verification SCons cache.

### `lib.scad.hub75` — focused OpenSCAD + SCons

- migration PR #29 merged as `ea75cee1fa83310bc2ba2ad1ce565ef81ac7f523`;
- canary run `35026885840` green;
- migrated main run `35065383879` green;
- README-only zero-runtime run `35065524524` green;
- immutable v0.1.5 released from `e0432a9533a08a1c0d9e87225c22f3f66b632531`;
- focused runtime and normal SCons transport are used; command-only Verification correctly avoids Verification-SCons transport.

### `2026-009-01.cad.HUB75-display-frame`

- Migration-005 PR #33 merged as `61da023ff0f6bc353687b55a8158e75ebd70b046` on tool v0.14.3;
- branch qualification `35069083479` green;
- post-merge main `35069411142` green;
- README-only probe PR #34 / run `35069504915` proved `affected=false`, affected task ids `[]`, and no planner/cache/runtime/Docker/publication work;
- **pending:** final v0.14.7 semantic/thin-caller alignment, requalification and immutable project release.

These four repositories remain the complete public current-generation consumer set in the canonical catalog. The missing work is final release closure for template and frame, not adding classic CAD repositories to the migration.

## Measurement state

| Scenario | Result | Interpretation |
| --- | ---: | --- |
| clamps affected canary | ~41.9 s | meets low/mid-40 s target |
| HUB75 warm/cached canary | ~32.2 s | meets low/mid-30 s target |
| clamps unrelated README-only | ~9.2 s | zero CAD/runtime; 4–6 s latency ambition not met |
| HUB75 unrelated README-only | ~7.6 s | zero CAD/runtime; 4–6 s latency ambition not met |
| template unrelated README-only | ~9.9 s | zero CAD/runtime; 4–6 s latency ambition not met |
| template full v0.14.7 qualification | 41.059 s to prepared Build snapshot | durable phase timing retained |

The selected architecture/resource goals remain met: one normal hosted job, at most one CAD runtime, one affected query, capability-appropriate image, SCons only where useful, compact normal evidence, no duplicate complete normal artifacts and zero CAD work for unrelated changes.

The unrelated-change wall-clock target is only partially met. Remaining time is dominated by GitHub Actions setup and restoring/querying the generic Moon runtime; follow-up optimisation is tracked separately in `tool.git-project#26` and does not alter the Migration-005 closeout gates.

## Completion decision

Migration 005 is **not yet complete** after the closeout review.

Already met:

- shared architecture and owner boundaries;
- shared runtime/tool releases;
- library canary qualification/releases;
- template v0.14.7 correctness/provenance/zero-runtime qualification;
- resource architecture and affected-canary latency envelopes;
- unrelated-change zero-CAD requirement.

Still required before closure:

- release the final qualified template state;
- align the frame to final v0.14.7 caller/release policy and requalify it;
- release the resulting frame state;
- record those immutable releases and exact evidence here and in `STATUS.md`.
