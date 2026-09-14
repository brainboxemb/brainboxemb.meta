# Current cross-project changes

This page only answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

There is currently **no active cross-project migration**.

## Recently completed

### Migration 001 — consolidate the public portfolio overview

**Complete.**

`brainboxemb.meta` now contains the public repository overview, dashboard, shared guidance and SCAD/CAD navigation that had previously been split across several repositories.

`tech.scad` and `meta.scad-projects` are now private archives.

See [Migration 001](migrations/001-brainboxemb-meta/README.md) only if you want the migration history or evidence.

## Proposed, not active

### Migration 002 — check build decisions after a SCAD build

**Proposed / inactive.**

The idea is to add a check in `tool.scad-project` that compares what changed with what the build actually rebuilt or restored from cache.

Nothing from Migration 002 should be implemented until it is explicitly activated and the plan is rechecked against the current tooling.

See [Migration 002](migrations/002-scad-build-decision-audit/README.md) and issue #19.

## Other follow-ups

Two useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20.
