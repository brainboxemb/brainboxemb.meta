# Cross-project migrations

This directory contains changes that intentionally span more than one public brainboxemb repository.

A migration is temporary work with a clear goal and completion point. It should not become the place where the normal technical documentation lives.

Start with [`../STATUS.md`](../STATUS.md) to see whether any migration is currently active.

## Migration states

- **active** — deliberately selected as current cross-project work;
- **proposed / inactive** — documented so the idea and scope are clear, but not started;
- **complete** — finished and retained for history/evidence.

Having a migration directory does not mean that work is active.

## Active

There is currently **no active migration**.

## Proposed / inactive

- [002 — SCAD build-decision audit](002-scad-build-decision-audit/README.md) — proposed only; reassess before activation.

## Complete

- [001 — Consolidate public portfolio context into brainboxemb.meta](001-brainboxemb-meta/README.md) — completed repository/catalog/dashboard/documentation consolidation.

## When to create a migration

Use a migration when one coordinated change genuinely needs several repositories or has an ordering/evidence problem across repository boundaries.

Project-specific work remains in the project repository. A useful improvement discovered during a migration does not automatically become part of the blocking migration; it can be scheduled separately.
