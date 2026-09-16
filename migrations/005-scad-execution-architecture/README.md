# Migration 005 — simplify the SCAD execution architecture

## Why this migration existed

The current SCAD repositories had accumulated overlapping GitHub Actions, Moon, SCons, runtime, cache and publication responsibilities. Migration 005 established one understandable shared execution architecture and then proved it through the shared tool, reference template, reusable libraries and a real HUB75 project.

Use this record when checking the final SCAD execution model, the rollout evidence behind it, or whether a later SCAD change belongs to the durable architecture versus a new migration.

Status: **complete**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55) — completed.

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Final architecture

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

Maintainer-facing capabilities remain deliberately small: `scad.docs`, `scad.build` and `scad.verify`. Shared lifecycle mechanics belong to `tool.scad-project`; consumers keep project-specific configuration and source-family impact.

## Final released shared baseline

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.8` / exact `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`.

The v0.14.8 owner patch uses lightweight semantic tool tags for cross-repository reusable-workflow resolution while the committed tool gitlink retains exact implementation identity.

## Completed rollout gates

### Reference template

`template.scad-project v0.0.5`

- exact source `c718655cd67ff90f2d0ba2cf474c86db69cc8965`;
- exact-main Production `35097071003` — green;
- Release `35097219635` — green;
- immutable Build/Verification release output and downloadable assets/checksums verified.

### Reusable clamp library

`lib.scad.clamps v0.1.5`

- affected PR `35101169850` — green;
- merged main `35101626924` — green;
- README-only zero-runtime `35101816174` — green;
- exact release source `11f804c5087c2b5ec06af11603af4508d5c1db43`;
- Release `35103156647` — green;
- `rel/v0.1.5/{build,verification}` identify v0.14.8 and exact gitlink `85781a6b...`.

### Reusable HUB75 library

`lib.scad.hub75 v0.1.6`

- affected PR `35101188447` — green;
- merged main `35101638473` — green;
- README-only zero-runtime `35101927430` — green;
- exact release source `4dd285d5bced43657392d9fd6d245005f12e53eb`;
- Release `35103198893` — green;
- `rel/v0.1.6/{build,verification}` identify v0.14.8 and exact gitlink `85781a6b...`.

### Real HUB75 frame

`2026-009-01.cad.HUB75-display-frame v0.0.2`

- affected PR `35098196082` — green;
- merged main `35098642458` — green;
- README-only zero-runtime `35099086265` — green;
- exact release source `18f7900bed31345b8123571ade152af6914e18d6`;
- Release `35099609270` — green;
- immutable Build/Verification release output and downloadable assets/checksums verified.

## Evidence and design record

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected architecture. |
| [06 — Implementation plan](06-implementation-plan.md) | Owner-by-owner rollout and qualification gates. |
| [10 — Measurements](10-measurements.md) | Baseline and implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource review. |
| [30 — Final closeout evidence](30-closeout-evidence.md) | Exact tool/template/library/frame release and provenance evidence. |

The durable architecture lives under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This migration directory is the historical change/evidence record.

## Performance interpretation

The selected resource architecture is retained: one normal hosted job, at most one CAD runtime, one affected query, capability-appropriate runtime, SCons only where useful, compact evidence, no duplicate complete normal artifacts and zero CAD work for unrelated changes.

Previously measured affected canaries (~41.9 s clamps, ~32.2 s HUB75) met their intended latency envelopes. The unrelated README-only path remained above the aspirational 4–6 seconds but correctly performs zero CAD/runtime work. Generic unaffected-path latency remains follow-up work (`tool.git-project#26`) rather than a Migration-005 blocker.

## Completion decision

Migration 005 is complete. The final shared v0.14.8 baseline is now present and immutably released through the template, both current-generation reusable libraries and the real HUB75 frame.
