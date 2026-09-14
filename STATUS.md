# Current cross-project changes

This page only answers: **what repository-spanning work is active or waiting to be picked up?**

For the normal repository overview, start with [`README.md`](README.md).

## Active now

### Migration 002 — check build decisions after a SCAD build

**Active.**

`tool.scad-project` already records what happened to each SCons target. Migration 002 adds a separate post-build audit that checks whether those outcomes contradict changes that can be proven to affect a target.

The first implementation slice is deliberately small: the audit receives an existing build-decision report plus explicit changed paths. It does not add another dependency engine or generic Git-diff implementation.

See [Migration 002](migrations/002-scad-build-decision-audit/README.md), the [implementation change request](migrations/002-scad-build-decision-audit/change-request.md), and issue #19.

## Recently completed

### Migration 001 — consolidate the public portfolio overview

**Complete.**

`brainboxemb.meta` now contains the public repository overview, dashboard, shared guidance and SCAD/CAD navigation that had previously been split across several repositories.

`tech.scad` and `meta.scad-projects` are now private archives.

See [Migration 001](migrations/001-brainboxemb-meta/README.md) only if you want the migration history or evidence.

## Other follow-ups

Two useful cross-project improvements remain parked until there is a reason to pick them up:

- **Self-contained physical-verification document packages** — issue #18;
- **One release flow for requested versions across project types** — issue #20.
