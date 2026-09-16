# Migration 005 — simplify the SCAD execution architecture

## Why this migration exists

The SCAD repositories had accumulated overlapping GitHub Actions, Moon, SCons, runtime, cache and publication responsibilities. Migration 005 established one understandable shared execution architecture and proved it through the shared tool, reference template, reusable libraries and a real HUB75 project.

The migration was reopened after completion when persistent generated-output branch names were found to conflict with the compact technical namespace already used inside current-generation SCAD repositories. That final inconsistency has now been corrected and immutably qualified.

Use this record when checking the final SCAD execution model, its rollout evidence, or why the persistent technical publication namespaces are `bld` and `vrf` rather than `build` and `verification`.

Status: **complete — execution architecture and final technical namespace alignment qualified**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55).

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

Current-generation SCAD workspaces and persistent publication now use the same technical identity:

```text
dev/pr-N/bld
dev/pr-N/vrf

prod/bld
prod/vrf

rel/vX.Y.Z/bld
rel/vX.Y.Z/vrf
```

Historical already-published `build` / `verification` branches and releases remain historical evidence; immutable history was not rewritten merely for naming.

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

## Final corrected baseline

Shared foundation:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.9` / exact `a140b22858ac1899e7f2fa71b679639a70d819c3`.

Final current-generation consumer releases:

- `template.scad-project v0.0.6` / exact source `b8a0cc9113084f56c074b7dc61b160105c615b71`;
- `lib.scad.clamps v0.1.6` / exact source `021eed7bba76ca77825bd6f6c850e1ebd2916283`;
- `lib.scad.hub75 v0.1.7` / exact source `1390cd322b31b119779c41743119c85e0e984314`;
- `2026-009-01.cad.HUB75-display-frame v0.0.3` / exact source `9ff354260276e325d571c82af67bc23e9815744d`.

All four consumers now have qualified mutable `prod/{bld,vrf}` output and immutable `rel/vX.Y.Z/{bld,vrf}` release output with exact source/tool provenance.

## Reopened closeout sequence — completed

The targeted correction followed the shortest safe route:

1. `tool.scad-project` — normalized shared/default persistent publication suffixes and released v0.14.9;
2. `template.scad-project` — adopted v0.14.9, normalized project publication config, proved affected/main/unrelated paths and released v0.0.6;
3. `lib.scad.clamps` and `lib.scad.hub75` — adopted the same baseline while preserving their direct/SCons execution differences and released v0.1.6 / v0.1.7;
4. `2026-009-01.cad.HUB75-display-frame` — adopted the same baseline without changing its HUB75 geometry dependency and released v0.0.3;
5. new `prod/{bld,vrf}` and `rel/vX.Y.Z/{bld,vrf}` output/provenance were verified in every current-generation consumer.

No execution-architecture redesign and no historical branch rewrite was needed.

## Evidence and design record

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected architecture. |
| [06 — Implementation plan](06-implementation-plan.md) | Historical owner-by-owner architecture rollout record. |
| [10 — Measurements](10-measurements.md) | Baseline and implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource review. |
| [30 — Final closeout evidence](30-closeout-evidence.md) | Exact original and namespace-correction release/provenance evidence. |

The durable architecture lives under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This migration directory remains the historical change/evidence record.

## Completion decision

Migration 005 is **complete**. The execution/performance conclusions remain unchanged, and the final current-generation baseline now uses one technical namespace consistently across workspace roots and generated-output branches: `dsg`, `bld`, `vrf` and `docs` where applicable.

Generic optimisation such as unaffected-path latency remains separate follow-up work and does not reopen this migration.
