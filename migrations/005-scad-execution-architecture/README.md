# Migration 005 — simplify the SCAD execution architecture

## Why this migration exists

The SCAD repositories had accumulated overlapping GitHub Actions, Moon, SCons, runtime, cache and publication responsibilities. Migration 005 established one understandable shared execution architecture and proved it through the shared tool, reference template, reusable libraries and a real HUB75 project.

The migration was reopened twice for narrow closeout corrections without redesigning that architecture: first to align persistent generated-output namespaces with the compact technical `dsg` / `bld` / `vrf` convention, and finally to correct released owner guidance that still showed legacy `build` / `verification` branch examples.

Use this record when checking the final SCAD execution model, its rollout evidence, or why later Java work may rely on the same technical namespace convention.

Status: **complete**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55) — closed after the released guidance correction was externally qualified.

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Durable namespace rule

The portfolio-wide rule is defined in [Generated output and publication](../../docs/40-04-generated-output.md).

Human-facing lifecycle names remain readable:

```text
Design
Build
Verification
Documentation
```

Stable technical path/branch identifiers use compact canonical identifiers where defined:

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

The runtime/publication namespace correction is fully proven on:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.9` / exact `a140b22858ac1899e7f2fa71b679639a70d819c3`;
- `template.scad-project v0.0.6` / exact release source `b8a0cc9113084f56c074b7dc61b160105c615b71`;
- `lib.scad.clamps v0.1.6` / exact source `021eed7bba76ca77825bd6f6c850e1ebd2916283`;
- `lib.scad.hub75 v0.1.7` / exact source `1390cd322b31b119779c41743119c85e0e984314`;
- `2026-009-01.cad.HUB75-display-frame v0.0.3` / exact source `9ff354260276e325d571c82af67bc23e9815744d`.

Those consumers prove mutable `prod/{bld,vrf}` and immutable `rel/vX.Y.Z/{bld,vrf}` output with exact source/tool provenance. Detailed runtime/release evidence remains in [30 — Final closeout evidence](30-closeout-evidence.md).

## Final released-guidance correction

Durable review after the v0.14.9 rollout found that released `tool.scad-project` agent guidance still named legacy branch suffixes even though workflows, tests and consumers already used `bld` / `vrf`.

That mismatch was corrected without changing execution semantics:

- `tool.scad-project v0.14.10` -> exact source `3ad040b2d9c26b8c482853157baeb99a8d9b36db`;
- `template.scad-project` pinned the corrected release on exact main source `637906c49b90308ebba7e4477fa2e5036d9543da`;
- exact-main Production run `35140381160` -> green;
- that run resolves `tool.scad-project/.github/workflows/project-production.yml@v0.14.10` to exact `3ad040b2d9c26b8c482853157baeb99a8d9b36db`.

The final correction was guidance-only. It therefore did not require a new template semantic release merely to re-prove unchanged runtime behaviour. The existing immutable consumer releases remain the execution/publication evidence; the exact-main template run proves that current pinned guidance now matches that contract.

The separate [31 — Final released-guidance closeout](31-final-guidance-closeout.md) records this final patch evidence without rewriting the v0.14.9 runtime evidence in document 30.

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
| [30 — Final closeout evidence](30-closeout-evidence.md) | Exact v0.14.9 runtime/release/provenance evidence. |
| [31 — Final released-guidance closeout](31-final-guidance-closeout.md) | v0.14.10 guidance-only owner patch plus exact-main template qualification. |

The durable architecture lives under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This migration directory remains the historical change/evidence record.

## Completion decision

Migration 005 is complete because the runtime/publication contract **and** the released owner guidance consumed by current repositories now use the same technical namespace. No later template patch tag is required for this guidance-only final gate, and no execution-architecture redesign remains open.
