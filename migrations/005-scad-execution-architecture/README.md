# Migration 005 — simplify the SCAD execution architecture

## Why this migration exists

The SCAD repositories had accumulated overlapping GitHub Actions, Moon, SCons, runtime, cache and publication responsibilities. Migration 005 established one understandable shared execution architecture and proved it through the shared tool, reference template, reusable libraries and a real HUB75 project.

The execution architecture itself is already qualified. This migration is temporarily reopened because its final persistent publication naming drifted from the technical namespace already used inside current-generation SCAD repositories.

Use this record when checking the final SCAD execution model, its rollout evidence, or the narrow namespace correction required before later domains align to it.

Status: **active — final technical namespace alignment**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55) — reopened.

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

Current-generation SCAD workspaces already follow this pattern with `dsg`, `bld` and `vrf`. Migration 005 originally standardized persistent branches as `build` and `verification`, creating two technical names for the same concepts. The reopened closeout corrects that inconsistency.

Target persistent namespaces:

```text
dev/pr-N/bld
dev/pr-N/vrf

prod/bld
prod/vrf

rel/vX.Y.Z/bld
rel/vX.Y.Z/vrf
```

Historical already-published `build`/`verification` branches and releases remain historical evidence; immutable history is not rewritten merely for naming.

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

## Previously qualified released baseline

The following baseline remains valid evidence for the execution architecture before the namespace correction:

- `docker.scad-toolchain v0.5.0`;
- `tool.git-project v0.2.8` / exact `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`;
- `tool.scad-project v0.14.8` / exact `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`;
- `template.scad-project v0.0.5`;
- `lib.scad.clamps v0.1.5`;
- `lib.scad.hub75 v0.1.6`;
- `2026-009-01.cad.HUB75-display-frame v0.0.2`.

Their affected, merged-main, unrelated zero-runtime and release evidence remains authoritative for the architecture that produced it.

## Reopened closeout sequence

Use the shortest safe path:

1. `tool.scad-project` — change shared/default persistent publication suffixes and examples/docs from `build`/`verification` to `bld`/`vrf`; qualify and patch-release.
2. `template.scad-project` — adopt the released tool and normalized project publication config; prove affected, unrelated zero-runtime, main and release paths.
3. `lib.scad.clamps` and `lib.scad.hub75` — adopt the same released baseline and normalized namespace; qualify and patch-release.
4. `2026-009-01.cad.HUB75-display-frame` — adopt the same baseline and normalized namespace; qualify and patch-release.
5. verify new `prod/{bld,vrf}` and `rel/vX.Y.Z/{bld,vrf}` outputs/provenance; then close Migration 005 again.

Do not redesign the execution architecture or rewrite historical generated branches as part of this correction.

## Evidence and design record

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Original scope and completion criteria. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected architecture. |
| [06 — Implementation plan](06-implementation-plan.md) | Owner-by-owner rollout and qualification gates. |
| [10 — Measurements](10-measurements.md) | Baseline and implementation measurements. |
| [20 — Target resource budget](20-target-resource-budget.md) | Target-versus-result resource review. |
| [30 — Final closeout evidence](30-closeout-evidence.md) | Existing exact tool/template/library/frame release and provenance evidence; extend with namespace-correction evidence before final re-close. |

The durable architecture lives under [`domains/scad/architecture.md`](../../domains/scad/architecture.md). This migration directory remains the historical change/evidence record.

## Completion decision

Migration 005 returns to **complete** only when the current-generation SCAD tool and all four qualified consumers publish new output using canonical `bld`/`vrf` technical namespaces and that behavior is immutably released. The previously qualified v0.14.8 execution model does not need to be reproven beyond the normal regression gates required by the naming change.
