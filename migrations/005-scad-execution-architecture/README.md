# Migration 005 — simplify the SCAD execution architecture

Status: **migration execution in progress — shared foundations released; consumer rollout is next**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this folder exists

Migration 005 changes the shared SCAD execution model from a lifecycle-heavy Moon configuration into a capability-oriented model that is easier to understand and uses hosted compute more proportionately.

The design phase is finished. The selected architecture and its important technical assumptions have been validated, and the shared runtime/generic-query/SCAD-tool foundations are released. Work in this migration is now **consumer and canary migration/qualification**. Historical design and validation documents remain here so decisions can be traced without relying on chat history.

## Start here

For normal migration work, read these in this order:

| Document | Role | Read it when... |
| --- | --- | --- |
| [01 — Change request](01-change-request.md) | Scope and fixed intent | You need to know why Migration 005 exists, what is in/out of scope and what is no longer an open design question. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected technical design | You need to understand the Moon/SCons/runtime/lifecycle model that is being migrated to. |
| [06 — Implementation plan](06-implementation-plan.md) | Active execution order | You are implementing or reviewing the next owner-repository migration step. |

The intervening design-history documents are useful when you need to reconstruct how the selected design was reached:

| Document | Role |
| --- | --- |
| [02 — Migration-004 baseline architecture](02-current-architecture.md) | What existed before Migration 005 and which problems were visible. |
| [03 — Architecture reflection](03-architecture-reflection.md) | What was learned from reconstructing and measuring the old model. |
| [04 — Alternatives and decision](04-architecture-decision.md) | Which alternatives were considered and why the selected direction won. |

## Supporting evidence

These documents are not the primary reading route. They exist to support a particular decision or acceptance criterion and are intentionally numbered separately.

| Document | Why it exists |
| --- | --- |
| [10 — Measurements](10-measurements.md) | Consolidated measured baseline used for the architecture decision. |
| [11 — Resource efficiency](11-resource-efficiency.md) | Defines why wall-clock speed and total compute/resource use are evaluated separately. |
| [12 — SCons cache validation](12-scons-cache-validation.md) | Proves SCons target-level reuse is useful for an actual SCons-enabled SCAD repository and unnecessary for direct projects. |
| [13 — Runtime image family](13-runtime-image-family.md) | Records the OpenSCAD-focused/full runtime-profile design and its ownership. |
| [14 — Runtime image validation](14-runtime-image-validation.md) | Controlled functional/size validation of the two runtime profiles. |
| [15 — Publication analysis](15-publication-analysis.md) | Explains the normal publication path and why normal Actions artifacts are not a same-job hand-off. |
| [16 — Publication concurrency validation](16-publication-concurrency-validation.md) | Proves Build and Verification branches can be published concurrently on one runner. |
| [17 — Normal CI artifact policy](17-normal-ci-artifact-policy.md) | Records the decision to retain compact evidence but not duplicate complete normal output trees by default. |
| [18 — Moon inheritance validation](18-moon-inheritance-validation.md) | Proves consumers can inherit shared capability tasks from pinned `tool.scad-project` policy. |
| [19 — Human-understandability validation](19-human-understandability-validation.md) | Checks that a maintainer can understand the resulting consumer model without migration history. |
| [20 — Target resource budget](20-target-resource-budget.md) | Sets the latency/runner/image/cache acceptance envelope for canary migration. |

## Selected architecture in one view

```text
GitHub Actions
  exact source/base, credentials, hosted lifecycle
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
  isolated Build/Verification publication
```

The normal maintainer-facing capability vocabulary is deliberately small:

```text
scad.build   presentation renders, when the repository has them
scad.docs    design documentation
scad.verify  Verification
```

Generic task commands, cache policy and standard output boundaries belong in shared `tool.scad-project` policy, not copied lifecycle topology in every consumer.

One implementation refinement is important when reading “required” above: the source-affected capability set and the set that must be materialized for a complete replacement publication can differ. For example, a docs-only change may hydrate an unchanged presentation capability through Moon when both contribute to the same complete Build branch. That extra contributor stays non-affected; it exists only to keep publication correct.

## Released shared foundations

Migration 005 currently has these immutable shared layers available for the consumer rollout:

- `docker.scad-toolchain v0.5.0` — focused OpenSCAD and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from the existing single Moon query;
- `tool.scad-project v0.14.0` — inherited SCAD capabilities, configuration consistency, runtime/cache selection and normal one-runtime lifecycle.

The next owner step is `template.scad-project`; after that the clamps and HUB75 canaries qualify the two important runtime/build-engine modes before broader downstream adoption.

## Current execution phase

The architecture search is closed. If an implementation uncovers evidence that a fixed assumption is false, document that contradiction explicitly before changing the design. Otherwise continue the migration sequence in [06 — Implementation plan](06-implementation-plan.md).

Do **not** infer current repository adoption only from these migration documents. During rollout, individual repositories remain authoritative for the exact tool/image versions they currently pin.

The durable post-migration explanation of the shared SCAD architecture belongs under [`domains/scad/`](../../domains/scad/), not in this migration folder. This folder remains the traceable change record and evidence set.
