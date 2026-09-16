# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Reopened for final rollout/release gates.**

The architecture, shared-tool releases, canary qualification and performance/resource evidence remain valid. The first closeout was nevertheless premature because repository verification found two skipped release/rollout steps:

1. **`template.scad-project`** is fully qualified on `tool.scad-project v0.14.7` and merged as `cb1e3e50e5e56644153cdf74b54b5da1e747c8d8`, but the latest published template release is still `v0.0.4` from the earlier source `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9`. A v0.0.5 release of the qualified v0.14.7 state is now required.
2. **`2026-009-01.cad.HUB75-display-frame`** is migrated only to `tool.scad-project v0.14.3` on main commit `61da023ff0f6bc353687b55a8158e75ebd70b046`. Its Production/Release callers still use the old exact-SHA/consumer-local release orchestration and the latest project release is still `v0.0.1` from the v0.9.8 generation. The frame must first move to final `tool.scad-project v0.14.7`, then be requalified and released as a new immutable project version.

Final released shared foundations remain:

- `docker.scad-toolchain v0.5.0` — OpenSCAD-focused and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from one generic Moon query;
- `tool.scad-project v0.14.7` / `3935e5f86fe309b8908a05554f7ada336a6d6886` — inherited capabilities, precise shallow tool-gitlink comparison, configuration/runtime/cache planning, semantic reusable-workflow refs, one-runtime normal production, durable timing/log evidence and exact host publication provenance.

Already-valid qualification/evidence includes:

- template v0.14.7 qualification run `35085388134`, post-merge main run `35085631904`, README-only zero-runtime probe `35085786014`;
- `lib.scad.clamps` immutable v0.1.4 and zero-runtime run `35065514152`;
- `lib.scad.hub75` immutable v0.1.5 and zero-runtime run `35065524524`;
- frame Migration-005 v0.14.3 migration run `35069411142` and README-only probe `35069504915`;
- affected-canary latency of ~41.9 s for clamps and ~32.2 s for HUB75;
- unrelated README-only paths of ~7.6–9.9 s with zero CAD/runtime work.

The missing work is therefore release completion and final frame alignment, **not** a redesign of the selected SCAD execution architecture.

Tracking issue: #55. Status-correction issue: #64. Canonical record: [Migration 005](migrations/005-scad-execution-architecture/README.md). Durable architecture: [SCAD technical architecture](domains/scad/architecture.md).

A possible Java execution-architecture migration may be prepared in parallel as **proposed/inactive**, but it does not become active until Migration 005 is actually complete.

## Recently completed

### Migration 004 — SCAD repository execution model

**Complete.**

Migration 004 qualified the conditional-SCAD execution model through the template and both reusable SCAD libraries. Its measured wall-clock/resource trade-offs became the starting point for Migration 005 rather than being hidden inside a success label.

See [Migration 004](migrations/004-scad-repository-execution-model/README.md), [qualification evidence](migrations/004-scad-repository-execution-model/evidence.md) and [performance evidence](migrations/004-scad-repository-execution-model/performance-evidence.md).

### Migration 003 — roll out `tool.scad-project v0.12.0` through SCAD consumers

**Complete.**

The released SCAD tool was qualified through the template, both SCAD libraries and finally the real HUB75 frame project.

### Migration 002 — check build decisions after a SCAD build

**Complete.**

`tool.scad-project` provides an explicit post-build audit that compares changed paths with dependency evidence already recorded for each SCons target.

### Migration 001 — consolidate the public portfolio overview

**Complete.**

`brainboxemb.meta` contains the public repository overview, dashboard, shared guidance and SCAD/CAD navigation that had previously been split across several repositories.

## Parked experiment

- **Moon as SCAD target engine** — issue #51. Migration 005 deliberately retained SCons as the fine-grained target engine where selected; this parked experiment remains separate.

## Other follow-ups

Useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20;
- **Standardise CHANGELOG format and add a shared template** — issue #52.

Generic performance/robustness follow-ups remain owner-local unless explicitly promoted:

- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse;
- `tool.git-project` issue #22 — generic release request idempotency;
- `tool.git-project` issue #26 — reduce fixed latency of unaffected Moon preflight after Migration 005.
