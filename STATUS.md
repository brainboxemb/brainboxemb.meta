# Current cross-project changes

This page only answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

There is currently **no active cross-project migration**.

## Proposed next

### Migration 004 — define the current SCAD repository execution model

**Proposed / inactive.**

Before changing the SCAD libraries again, review why current projects and libraries use different Build/Verify execution models and decide which differences are genuinely justified.

The review uses `template.scad-project` as the reference project and `lib.scad.clamps` as the practical reference library. It explicitly evaluates Moon, Build/Verify independence, duplicate container startup, container timing, evidence/publication behaviour and whether a separate `template.scad-lib` is actually useful.

No implementation starts until the [change request](migrations/004-scad-repository-execution-model/change-request.md) has been reviewed and Migration 004 is explicitly activated. Tracking issue: #49.

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

## Other follow-ups

Two useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20.
