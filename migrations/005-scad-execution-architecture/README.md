# Migration 005 — simplify the SCAD execution architecture

Status: **complete**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55) — completed.

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Outcome

Migration 005 simplified the shared current-generation SCAD execution model into a capability-oriented architecture with proportionate hosted compute and explicit evidence.

The selected model is:

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

## Final released foundations

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.8` / exact `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`.

The Step-3 tool line was hardened through owner fixes rather than consumer workarounds. The final v0.14.8 patch changed semantic tool release tags to lightweight refs so cross-repository nested reusable workflows resolve through readable `@vX.Y.Z` refs without losing the exact committed tool-gitlink identity contract.

## Final consumer state

### `template.scad-project`

- immutable release: `v0.0.5`;
- exact source: `c718655cd67ff90f2d0ba2cf474c86db69cc8965`;
- exact-main Production: `35097071003` — green;
- Release: `35097219635` — fully green;
- Build, Verification, STL and checksum release assets present;
- immutable `rel/v0.0.5/{build,verification}` provenance matches the exact source and tool v0.14.8 gitlink.

### `lib.scad.clamps`

- immutable release: `v0.1.4`;
- final Migration-005 main and zero-runtime qualification remain valid;
- direct engine correctly avoids SCons cache transport.

### `lib.scad.hub75`

- immutable release: `v0.1.5` / exact `e0432a9533a08a1c0d9e87225c22f3f66b632531`;
- focused OpenSCAD runtime and configured SCons behaviour qualified;
- README-only zero-runtime path remains valid.

### `2026-009-01.cad.HUB75-display-frame`

- final shared baseline: `tool.scad-project v0.14.8` / exact gitlink `85781a6b...`;
- affected PR Production `35098196082` — green;
- merged baseline Production `35098642458` — green;
- README-only probe `35099086265` — green with planner, caches, runtime, materialization, finishing and publication all skipped after the one affected query;
- immutable release: `v0.0.2` from exact source `18f7900bed31345b8123571ade152af6914e18d6`;
- Release `35099609270` — fully green including request cleanup;
- Build, Verification, STL and checksum release assets present;
- immutable `rel/v0.0.2/{build,verification}` provenance matches exact release source and final tool identity.

## Evidence and design record

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected architecture. |
| [06 — Implementation plan](06-implementation-plan.md) | Owner-by-owner rollout and qualification gates. |
| [10 — Measurements](10-measurements.md) | Baseline and implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource review. |
| [30 — Final closeout evidence](30-closeout-evidence.md) | Corrected release/rollout closeout evidence. |

The durable architecture lives under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This migration directory remains the historical change/evidence record.

## Final performance interpretation

The selected resource architecture is retained: one normal hosted job, at most one CAD runtime, one affected query, capability-appropriate runtime, SCons only where useful, compact normal evidence, no duplicate complete normal artifacts and zero CAD work for unrelated changes.

Previously measured affected canaries (~41.9 s clamps, ~32.2 s HUB75) met their intended latency envelopes. The unrelated README-only path remained around 7.6–9.9 s rather than the aspirational 4–6 s, but correctly performed zero CAD/runtime work. Generic unaffected-path latency remains follow-up work (`tool.git-project#26`) rather than a Migration-005 blocker.

## Completion decision

The migration was reopened once because the first closeout skipped the final template and frame release gates. Those gates are now explicitly verified and recorded in [30 — Final closeout evidence](30-closeout-evidence.md).

Migration 005 is therefore **complete**. Migration 006 and Migration 007 remain separate proposed/inactive work and are not activated by this completion automatically.
