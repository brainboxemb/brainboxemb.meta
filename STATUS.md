# Current cross-project changes

This page only answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

There is currently **no active cross-project migration**.

The next practical decision is whether to publish the newly qualified `tool.scad-project` build-audit capability as a normal tool release before updating SCAD library consumers.

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
