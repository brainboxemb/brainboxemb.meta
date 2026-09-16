# Migration 005 — simplify the SCAD execution architecture

## Why this migration exists

The SCAD repositories had accumulated overlapping GitHub Actions, Moon, SCons, runtime, cache and publication responsibilities. Migration 005 established one understandable shared execution architecture and proved it through the shared tool, reference template, reusable libraries and a real HUB75 project.

The migration was reopened after completion when persistent generated-output branch names were found to conflict with the compact technical namespace already used inside current-generation SCAD repositories. The v0.14.9 runtime/default/test correction and all consumer releases now prove `bld` / `vrf`, but final durable review found one remaining released-owner inconsistency: `tool.scad-project v0.14.9` `AGENTS.md` still tells agents to use legacy `build` / `verification` branches.

Use this record when checking the final SCAD execution model, its rollout evidence, or the last correction required before the migration can close for good.

Status: **active — final released owner-guidance correction**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55) — remains open until released/pinned guidance matches the qualified runtime contract.

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Durable namespace rule

The portfolio-wide rule is defined in [Generated output and publication](../../docs/working-model/generated-output.md).

Human-facing lifecycle names remain readable:

```text
Design
Build
Verification
Documentation
```

Stable technical path/branch identifiers use the canonical compact identifiers where defined:

```text
Design        -> dsg
Build         -> bld
Verification  -> vrf
Documentation -> docs
```

Current-generation SCAD workspaces and persistent publication use:

```text
dev/pr-N/bld
dev/pr-N/vrf

prod/bld
prod/vrf

rel/vX.Y.Z/bld
rel/vX.Y.Z/vrf
```

Historical already-published `build` / `verification` branches and releases remain historical evidence; immutable history is not rewritten merely for naming.

## Qualified execution/publication baseline

The runtime/publication correction itself is fully proven on:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.9` / exact `a140b22858ac1899e7f2fa71b679639a70d819c3`;
- `template.scad-project v0.0.6` / exact source `b8a0cc9113084f56c074b7dc61b160105c615b71`;
- `lib.scad.clamps v0.1.6` / exact source `021eed7bba76ca77825bd6f6c850e1ebd2916283`;
- `lib.scad.hub75 v0.1.7` / exact source `1390cd322b31b119779c41743119c85e0e984314`;
- `2026-009-01.cad.HUB75-display-frame v0.0.3` / exact source `9ff354260276e325d571c82af67bc23e9815744d`.

All four consumers have qualified mutable `prod/{bld,vrf}` and immutable `rel/vX.Y.Z/{bld,vrf}` output with exact source/tool provenance.

## Final blocker discovered during durable review

Consumers explicitly tell agents to read the pinned `tools/tool.scad-project/AGENTS.md`. In released v0.14.9 that file still says:

```text
dev/pr-N/build
dev/pr-N/verification
prod/build
prod/verification
```

That guidance conflicts with the released workflow defaults, tests and consumer evidence. A main-only documentation edit would not fix consumers because they pin the tool commit. Therefore this is a small but real release blocker.

## Remaining closeout sequence

Use the shortest safe path:

1. `tool.scad-project` — change only released owner guidance/examples from legacy `build` / `verification` branch names to `bld` / `vrf`; add/retain a regression check if useful;
2. patch-release the owner without changing execution semantics;
3. update current-generation consumers to the corrected owner pin so their embedded/pinned guidance is no longer stale;
4. perform the minimum qualification needed to prove the pin update did not change runtime/publication behaviour, and create immutable consumer releases where the repository's release baseline requires it;
5. verify new release provenance and close Migration 005.

Migration 006 owner implementation may remain merged and qualified in parallel, but its owner release/consumer rollout stays gated until this final released-guidance baseline is stable.

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

## Evidence and design record

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected architecture. |
| [06 — Implementation plan](06-implementation-plan.md) | Historical owner-by-owner architecture rollout record. |
| [10 — Measurements](10-measurements.md) | Baseline and implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource review. |
| [30 — Final closeout evidence](30-closeout-evidence.md) | Exact historical and namespace-correction release/provenance evidence; final owner-guidance patch is appended before closure. |

The durable architecture lives under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This migration directory remains the historical change/evidence record.

## Completion decision

Migration 005 returns to **complete** only when runtime/publication behavior **and the released owner guidance consumed by pinned repositories** use the same technical namespace. No execution-architecture redesign is required.
