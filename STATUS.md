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

Step 1 is complete: `tool.git-project v0.2.5` provides the released generic Moon affected preflight.

Step 2 is complete: `template.scad-project` PR #22 removed the stale `scad.verify -> scad.build` dependency and requalified Build/Verify independence on exact main `082b0cecb47ba082899214751080adc54556e94c`.

Step 3 is next and is owned by `tool.scad-project`: extract the reusable SCAD production workflow with a lightweight host preflight, a conditional single SCAD container job and lightweight publication. Before fixing the preflight checkout contract, qualify Moon 2.5.4 `changed-files --base <sha> --head <sha>` with only the exact base and head commits locally present; do not inherit the template's current `fetch-depth: 0` by default.

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

A generic release robustness issue discovered during Migration 004 is tracked locally in `tool.git-project` issue #22 and does not block this migration.
