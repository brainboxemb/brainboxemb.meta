# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Reopened for final rollout/release gates.**

The architecture, shared-tool releases, canary qualification and performance/resource evidence remain valid. The first closeout was nevertheless premature because repository verification found skipped release/rollout steps, and the first corrected template-release attempt exposed one additional owner-level release blocker.

The current blocking order is now:

1. **`tool.scad-project` release-call compatibility** — the real `template.scad-project` v0.0.5 request on final v0.14.7 consumer main (`d524060a2af096d4728255cdc5266716a00dd226`) triggered Release run `35091703762`, but GitHub rejected the cross-repository reusable workflow before any job was created (`referenced_workflows=[]`). This matches the previously observed annotated-tag limitation recorded in `tool.scad-project#24`: the nested reusable release chain resolves through an exact commit/branch ref but not through the released annotated semantic tag. Owner fix PR `tool.scad-project#72` changes future tool release tags to lightweight refs and adds regression coverage. Finish that owner fix and publish the next patch release (expected `v0.14.8`) before changing consumers.
2. **`template.scad-project`** — after the owner patch release, move the reference consumer from v0.14.7 to that released patch, run one complete template qualification on the exact new main state, then publish immutable template release `v0.0.5` and verify its release assets plus `rel/v0.0.5/{build,verification}`. The latest published template release remains `v0.0.4` from source `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9`.
3. **`2026-009-01.cad.HUB75-display-frame`** — only after the template gate is green, advance the frame from `tool.scad-project v0.14.3` to the final released tool baseline, requalify normal/zero-runtime/provenance/release behaviour and publish the next immutable project release (expected `v0.0.2`).

The template caller itself has already been corrected and remains thin: PR #45 merged as `d524060a2af096d4728255cdc5266716a00dd226`, splitting manual-dispatch and release-request callers without moving shared release logic into the consumer. Main Production run `35091451284` is green. A cross-repository contract probe against the owner-fix branch (`35092459250`) compiled successfully, and an exact-v0.14.7-SHA probe (`35092548535`) reached the shared `resolve` job before deliberately rejecting invalid probe inputs. The remaining defect therefore belongs to the released tool-ref/tag contract, not to consumer-local orchestration.

Final released shared foundations before this blocker are:

- `docker.scad-toolchain v0.5.0` — OpenSCAD-focused and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from one generic Moon query;
- `tool.scad-project v0.14.7` / `3935e5f86fe309b8908a05554f7ada336a6d6886` — inherited capabilities, precise shallow tool-gitlink comparison, configuration/runtime/cache planning, semantic reusable-workflow refs, one-runtime normal production, durable timing/log evidence and exact host publication provenance; release-call/tag compatibility is the only newly exposed blocker on the final release path.

Already-valid qualification/evidence includes:

- template v0.14.7 qualification run `35085388134`, post-merge main run `35085631904`, README-only zero-runtime probe `35085786014`;
- template post-release-caller-fix Production run `35091451284`;
- `lib.scad.clamps` immutable v0.1.4 and zero-runtime run `35065514152`;
- `lib.scad.hub75` immutable v0.1.5 and zero-runtime run `35065524524`;
- frame Migration-005 v0.14.3 migration run `35069411142` and README-only probe `35069504915`;
- affected-canary latency of ~41.9 s for clamps and ~32.2 s for HUB75;
- unrelated README-only paths of ~7.6–9.9 s with zero CAD/runtime work.

The missing work is therefore release completion and final frame alignment, **not** a redesign of the selected SCAD execution architecture. The cross-repository release-call defect is a migration blocker because it prevents the required immutable consumer releases; it stays owned by `tool.scad-project` rather than being worked around in consumers.

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
