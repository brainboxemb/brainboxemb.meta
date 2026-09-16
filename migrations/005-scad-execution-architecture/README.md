# Migration 005 — simplify the SCAD execution architecture

Status: **active — final library baseline alignment**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55) — reopened.

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Outcome retained so far

Migration 005 simplified the shared current-generation SCAD execution model into a capability-oriented architecture with proportionate hosted compute and explicit evidence.

The selected model remains:

```text
GitHub Actions host
  exact source/base + one generic affected query
        |
        +--> unrelated -> stop before planner/CAD runtime
        |
        v
SCAD execution plan
  validate capabilities/configuration
  choose runtime/cache/materialization scope
        |
        v
at most one normal CAD runtime
  Moon whole-capability execution/reuse
  SCons fine-grained targets only where configured
        |
        v
host finishing/publication
  exact provenance
  durable timing/log evidence
  isolated Build/Verification publication
```

Maintainer-facing capabilities remain deliberately small: `scad.docs`, `scad.build` and `scad.verify`. Shared lifecycle mechanics belong to `tool.scad-project`; consumers keep project-specific configuration and source-family impact only.

## Final released shared baseline

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.8` / exact `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`.

The final v0.14.8 patch changed semantic tool release tags to lightweight refs so cross-repository nested reusable workflows resolve through readable `@vX.Y.Z` refs without losing the exact committed tool-gitlink identity contract.

## Completed consumer gates

### `template.scad-project`

- immutable release: `v0.0.5`;
- exact source: `c718655cd67ff90f2d0ba2cf474c86db69cc8965`;
- exact-main Production: `35097071003` — green;
- Release: `35097219635` — fully green;
- Build, Verification, STL and checksum release assets present;
- immutable `rel/v0.0.5/{build,verification}` provenance matches exact source and tool v0.14.8 identity.

### `2026-009-01.cad.HUB75-display-frame`

- final shared baseline: `tool.scad-project v0.14.8` / exact gitlink `85781a6b...`;
- affected PR Production `35098196082` — green;
- merged baseline Production `35098642458` — green;
- README-only probe `35099086265` — green with planner, caches, runtime, materialization, finishing and publication skipped after the one affected query;
- immutable release: `v0.0.2` from exact source `18f7900bed31345b8123571ade152af6914e18d6`;
- Release `35099609270` — fully green including request cleanup;
- Build, Verification, STL and checksum release assets present.

These gates remain valid and do not need to be repeated.

## Remaining final consistency gates

The closeout was corrected again after checking the actual library repositories on 2026-09-16. Both reusable current-generation libraries still declare `tool.scad-project v0.14.3` in `project.yml`, even though the shared baseline used by the template and real frame is now v0.14.8.

### `lib.scad.clamps`

Current state:
- immutable library release `v0.1.4` remains valid for the earlier Migration-005 qualification;
- current `main` still declares `tool.scad-project v0.14.3`.

Required final gate:
- repin semantic caller/config refs and exact tool gitlink to v0.14.8 / `85781a6b...`;
- qualify the library's normal direct-engine path and README-only zero-runtime path;
- publish the next immutable library release from the qualified final baseline and verify exact release provenance/assets.

### `lib.scad.hub75`

Current state:
- immutable library release `v0.1.5` remains valid for the earlier Migration-005 qualification;
- current `main` still declares `tool.scad-project v0.14.3`.

Required final gate:
- repin semantic caller/config refs and exact tool gitlink to v0.14.8 / `85781a6b...`;
- qualify the focused OpenSCAD runtime, configured SCons path and README-only zero-runtime path;
- publish the next immutable library release from the qualified final baseline and verify exact release provenance/assets.

Only after both library gates are complete may Migration 005 be closed.

## Evidence and design record

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected architecture. |
| [06 — Implementation plan](06-implementation-plan.md) | Owner-by-owner rollout and qualification gates. |
| [10 — Measurements](10-measurements.md) | Baseline and implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource review. |
| [30 — Closeout evidence](30-closeout-evidence.md) | Template/frame corrected release evidence; retained as completed intermediate closeout evidence. |

The durable architecture lives under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This migration directory remains the historical change/evidence record.

## Performance interpretation

The selected resource architecture is retained: one normal hosted job, at most one CAD runtime, one affected query, capability-appropriate runtime, SCons only where useful, compact normal evidence, no duplicate complete normal artifacts and zero CAD work for unrelated changes.

Previously measured affected canaries (~41.9 s clamps, ~32.2 s HUB75) met their intended latency envelopes. The unrelated README-only path remained around 7.6–9.9 s rather than the aspirational 4–6 s, but correctly performed zero CAD/runtime work. Generic unaffected-path latency remains follow-up work (`tool.git-project#26`) rather than a Migration-005 blocker.

## Parallel Migration 006 work

Migration 006 may be elaborated in parallel while these two library Actions paths run. That parallel work is planning/documentation only: current Java repositories may be re-read and the target architecture/decision/qualification plan may be sharpened, but Java owner implementation remains inactive until Migration 005 closes or priorities are explicitly changed.

## Completion decision

Migration 005 is **not yet complete**. The template and frame closeout gates are complete, but the reusable library consumers must still be aligned to the same final released v0.14.8 baseline and released from that qualified state.