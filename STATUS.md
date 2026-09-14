# Current cross-project changes

This page only answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 003 — roll out `tool.scad-project v0.12.0` through SCAD consumers

**Active.**

The build-decision audit from Migration 002 is implemented. The next work is to move that capability through the actual SCAD dependency chain using released and qualified versions rather than ad-hoc main commits.

Order:

1. release and tag-qualify `tool.scad-project v0.12.0`;
2. update and qualify `template.scad-project` first;
3. independently modernize, qualify and release `lib.scad.clamps` and `lib.scad.hub75`;
4. update `2026-009-01.cad.HUB75-display-frame` last as the real end-to-end consumer.

See [Migration 003](migrations/003-scad-v0.12-rollout/README.md) and issue #46.

## Recently completed

### Migration 002 — check build decisions after a SCAD build

**Complete.**

`tool.scad-project` now provides an explicit post-build audit that compares changed paths with the dependency evidence already recorded for each SCons target.

A target that is proven to depend on a changed path may be rebuilt or restored from cache, but it may not remain `CURRENT`. Possible overbuild is reported as a warning rather than a correctness failure.

The first slice deliberately leaves generic changed-path discovery and automatic workflow enforcement outside the SCAD tool.

See [Migration 002](migrations/002-scad-build-decision-audit/README.md) and its [qualification evidence](migrations/002-scad-build-decision-audit/evidence.md).

### Migration 001 — consolidate the public portfolio overview

**Complete.**

`brainboxemb.meta` now contains the public repository overview, dashboard, shared guidance and SCAD/CAD navigation that had previously been split across several repositories.

`tech.scad` and `meta.scad-projects` are now private archives.

See [Migration 001](migrations/001-brainboxemb-meta/README.md) only if you want the migration history or evidence.

## Other follow-ups

Two useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20.
