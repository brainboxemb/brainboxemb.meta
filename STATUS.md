# Current cross-project changes

This page answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 005 — simplify the SCAD execution architecture

**Reopened for final rollout/release gates.**

The architecture, canary qualification and performance/resource evidence remain valid. The first closeout was nevertheless premature because repository verification found skipped release/rollout steps. The additional owner-level release blocker exposed by the corrected template release path has now been fixed and released.

The current blocking order is now:

1. **`template.scad-project`** — move the reference consumer from `tool.scad-project v0.14.7` to released `v0.14.8` / exact source `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4`, qualify the complete reference-consumer path, then publish immutable template release `v0.0.5` and verify its release assets plus `rel/v0.0.5/{build,verification}`. The latest published template release remains `v0.0.4` from source `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9` until this gate completes.
2. **`2026-009-01.cad.HUB75-display-frame`** — only after the template gate is green, advance the frame to the final released tool baseline, requalify normal/zero-runtime/provenance/release behaviour and publish the next immutable project release (expected `v0.0.2`).

The release-call blocker is resolved in the owner. `tool.scad-project` PR #72 changed future semantic tool release tags from annotated tag objects to lightweight refs so nested reusable workflows can resolve cross-repository while consumers keep readable `@vX.Y.Z` refs. PR #73 prepared patch release `v0.14.8` and was green on Test run `35096013142`; exact merged main `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4` was green on Test run `35096209854`; Release run `35096353093` created `v0.14.8` successfully; the tag resolves directly to that commit (`type: commit`); and tagged Test run `35096362420` is green. The self-cleaning release-request branch was removed successfully.

The template caller itself was already corrected and remains thin: PR #45 merged as `d524060a2af096d4728255cdc5266716a00dd226`, splitting manual-dispatch and release-request callers without moving shared release logic into the consumer. Main Production run `35091451284` is green. The previous real v0.0.5 release request `35091703762` proved the annotated-v0.14.7 failure before job creation; controlled probes `35092459250` and `35092548535` isolated that failure to the released tool-ref/tag contract rather than consumer-local orchestration.

Current released shared foundations are:

- `docker.scad-toolchain v0.5.0` — OpenSCAD-focused and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from one generic Moon query;
- `tool.scad-project v0.14.8` / `85781a6b21a0f6a06d37be154fd9eb475ecaa2a4` — inherited capabilities, precise shallow tool-gitlink comparison, configuration/runtime/cache planning, semantic reusable-workflow refs, one-runtime normal production, durable timing/log evidence, exact host publication provenance and cross-repository release-call compatibility through lightweight semantic release tags.

Already-valid qualification/evidence includes:

- template v0.14.7 qualification run `35085388134`, post-merge main run `35085631904`, README-only zero-runtime probe `35085786014`;
- template post-release-caller-fix Production run `35091451284`;
- `lib.scad.clamps` immutable v0.1.4 and zero-runtime run `35065514152`;
- `lib.scad.hub75` immutable v0.1.5 and zero-runtime run `35065524524`;
- frame Migration-005 v0.14.3 migration run `35069411142` and README-only probe `35069504915`;
- affected-canary latency of ~41.9 s for clamps and ~32.2 s for HUB75;
- unrelated README-only paths of ~7.6–9.9 s with zero CAD/runtime work.

The missing work is therefore the final template and frame release completion, **not** a redesign of the selected SCAD execution architecture.

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
