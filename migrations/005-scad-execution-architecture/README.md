# Migration 005 — simplify the SCAD execution architecture

Status: **complete**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Closeout issue: [#63](https://github.com/brainboxemb/brainboxemb.meta/issues/63)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this folder exists

Migration 005 changed the shared current-generation SCAD execution model from a lifecycle-heavy Moon configuration into a capability-oriented architecture that is easier to reason about and uses hosted compute more proportionately.

The migration is complete because the shared foundations are released, the reference consumer and both representative canary modes are qualified, every public current-generation `tool.scad-project` consumer is migrated, and final latency/resource evidence has been recorded.

Classic CAD repositories are intentionally not part of this rollout. `repositories/catalog.yml` classifies those separately as classic standalone/shared-actions projects. Moving them to the current project-tooling generation would be a separate migration.

## Read this migration

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope, intent and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected Moon/SCons/runtime/lifecycle design. |
| [06 — Implementation plan](06-implementation-plan.md) | Completed owner-by-owner rollout and evidence gates. |
| [10 — Measurements](10-measurements.md) | Baseline experiments plus final implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource and latency review. |

The durable post-migration architecture is documented under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This folder remains the historical change/evidence record.

## Final architecture in one view

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

## Final released foundations

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

## Completed current-generation rollout

### `template.scad-project`

- final v0.14.7 qualification head `78a000603d6a64d2b495f6e054686a128c157877`;
- qualification run `35085388134` green;
- merged as `cb1e3e50e5e56644153cdf74b54b5da1e747c8d8`;
- post-merge main run `35085631904` green;
- README-only zero-runtime probe `35085786014` green;
- publication info, run context, Moon materialization and producer evidence all identify the exact assessed PR-head source revision.

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

- migration PR #33 merged as `61da023ff0f6bc353687b55a8158e75ebd70b046`;
- branch qualification `35069083479` green;
- post-merge main `35069411142` green;
- README-only probe PR #34 / run `35069504915` proved `affected=false`, affected task ids `[]`, and no planner/cache/runtime/Docker/publication work.

These four repositories are the complete public current-generation consumer set in the canonical catalog at migration closeout.

## Final measurement result

| Scenario | Result | Interpretation |
| --- | ---: | --- |
| clamps affected canary | ~41.9 s | meets low/mid-40 s target |
| HUB75 warm/cached canary | ~32.2 s | meets low/mid-30 s target |
| clamps unrelated README-only | ~9.2 s | zero CAD/runtime; 4–6 s latency ambition not met |
| HUB75 unrelated README-only | ~7.6 s | zero CAD/runtime; 4–6 s latency ambition not met |
| template unrelated README-only | ~9.9 s | zero CAD/runtime; 4–6 s latency ambition not met |
| template full v0.14.7 qualification | 41.059 s to prepared Build snapshot | durable phase timing retained |

The architecture/resource goals are met: one normal hosted job, at most one CAD runtime, one affected query, capability-appropriate image, SCons only where useful, compact normal evidence, no duplicate complete normal artifacts and zero CAD work for unrelated changes.

The unrelated-change wall-clock target is only partially met. Remaining time is dominated by GitHub Actions setup and restoring/querying the generic Moon runtime. That is a generic preflight optimisation opportunity, not unfinished SCAD architecture work.

## Completion decision

Migration 005 closes with the following interpretation:

- correctness and publication semantics: **met**;
- current-generation consumer rollout: **met**;
- resource architecture: **met**;
- warm affected latency envelopes: **met** on the two canaries;
- unrelated-change zero-CAD requirement: **met**;
- unrelated-change 4–6 s wall-clock ambition: **partially met / follow-up optimisation**.

No remaining item requires keeping Migration 005 active.
