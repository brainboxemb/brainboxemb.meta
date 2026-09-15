# Current cross-project changes

This page only answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 004 — SCAD repository execution model

**Active.**

The migration aligns current SCAD projects and libraries on one understandable production lifecycle:

- Moon as repository-level orchestration and affected/preflight layer;
- SCons retained as the qualified fine-grained SCAD target engine;
- Build and Verify remain logically independent;
- at most one normal heavy SCAD job/container when production is affected;
- a lightweight host preflight must prevent the SCAD container from starting for README-only or otherwise unaffected changes;
- publication happens outside the SCAD container;
- `template.scad-project` is the reference project and `lib.scad.clamps` the reference library.

Step 1 is complete: `tool.git-project` provides the released generic Moon affected preflight. The original capability shipped in v0.2.5; aggregate/upstream affected propagation discovered during Step 3 qualification was corrected generically and released as v0.2.6.

Step 2 is complete: `template.scad-project` PR #22 removed the stale `scad.verify -> scad.build` dependency and requalified Build/Verify independence on exact main `082b0cecb47ba082899214751080adc54556e94c`.

Step 3 is complete: `tool.scad-project v0.13.0` provides the reusable production workflow with shallow host preflight, optional producer-only `affected_task`, one conditional SCAD container, separate Build/Verify caches and lightweight publication. Release source is exact main `da57820fdadd7d203091b6818984991f1548408f`; release run `34938168129` and released-tag Test run `34938179069` passed.

Step 4 is complete: `template.scad-project` PR #29 consumed released `tool.scad-project v0.13.0` and merged as exact main `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`. Final PR-head run `34944252421` and exact-main run `34945239139` passed. Final-head proofs demonstrated README-only no-container (`#30`, run `34944598444`), Verify-only producer impact without Build/Docs (`#31`, run `34944622039`), and Build-side impact without the Verify producer (`#33`, run `34944404186`). Cold production built all reference targets in run `34938849331`; the later warm path restored all CAD targets through SCons cache. Whole-task Moon hydration did not occur on an exact-source rerun even though the portable Moon cache restored; that remains a non-blocking generic performance observation on `tool.git-project` issue #17.

Step 5 is next and is owned by `lib.scad.clamps`: re-evaluate the reference-library assumptions against its current repository, then move normal CI from separate heavy Build/Verify execution to the released common production lifecycle only if the library-specific requirements still fit the shared model proportionately.

Tracking issue: #49. See [Migration 004](migrations/004-scad-repository-execution-model/README.md) and its [qualification evidence](migrations/004-scad-repository-execution-model/evidence.md).

## Recently completed

### Migration 003 — roll out `tool.scad-project v0.12.0` through SCAD consumers

**Complete.**

The released SCAD tool was qualified through the template, both reusable SCAD libraries, and finally the real HUB75 frame project.

Current qualified versions include:

- `tool.scad-project v0.12.0`;
- `lib.scad.clamps v0.1.2`;
- `lib.scad.hub75 v0.1.3`;
- `2026-009-01.cad.HUB75-display-frame` on tool v0.12.0 + HUB75 library v0.1.3.

The separate physical-verification work in `lib.scad.hub75` is project-local work, not a continuation of this migration.

See [Migration 003](migrations/003-scad-v0.12-rollout/README.md) and its [qualification evidence](migrations/003-scad-v0.12-rollout/evidence.md).

### Migration 002 — check build decisions after a SCAD build

**Complete.**

`tool.scad-project` provides an explicit post-build audit that compares changed paths with dependency evidence already recorded for each SCons target.

See [Migration 002](migrations/002-scad-build-decision-audit/README.md) and its [qualification evidence](migrations/002-scad-build-decision-audit/evidence.md).

### Migration 001 — consolidate the public portfolio overview

**Complete.**

`brainboxemb.meta` contains the public repository overview, dashboard, shared guidance and SCAD/CAD navigation that had previously been split across several repositories.

`tech.scad` and `meta.scad-projects` are private archives.

See [Migration 001](migrations/001-brainboxemb-meta/README.md) for its history and evidence.

## Parked experiment

- **Moon as SCAD target engine** — issue #51. This is explicitly outside Migration 004; SCons remains the target engine during the execution-model migration.

## Other follow-ups

Useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20.

Generic performance/robustness follow-ups discovered while executing Migration 004 remain owner-local and non-blocking:

- `tool.git-project` issue #17 — improve safe Moon cache/materialization reuse, now including same-source SCAD evidence where the portable Moon cache restored but whole-task hydration did not occur;
- `tool.git-project` issue #22 — generic release request idempotency.
