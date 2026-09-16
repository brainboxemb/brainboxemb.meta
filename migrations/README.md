# Cross-project migrations

This directory contains changes that intentionally span more than one public brainboxemb repository.

A migration is temporary work with a clear goal and completion point. It should not become the place where normal long-lived technical documentation lives.

Start with [`../STATUS.md`](../STATUS.md) to see which cross-project work is currently active.

## Migration states

- **active** — deliberately selected as current cross-project work;
- **proposed / inactive** — documented so the idea and scope are clear, but not started;
- **complete** — finished and retained for history/evidence.

Having a migration directory does not mean that work is active.

## Active

- [006 — simplify the Java execution architecture](006-java-execution-architecture/README.md) — active. Owner implementation starts in `tool.java-project`, followed by release, `template.java-project` qualification and then the real `2026-010-02.java.event-timing-framework` rollout.

## Proposed / inactive

- [007 — standardise GitHub Actions dependency maintenance](007-github-actions-dependency-maintenance/README.md) — standardise action pinning/update policy and evaluate Dependabot plus `actions-up`; intentionally after Migration 006.

## Complete

- [005 — simplify the SCAD execution architecture](005-scad-execution-architecture/README.md) — final v0.14.8 execution architecture qualified and released through the template, both reusable SCAD libraries and the real HUB75 frame.
- [004 — SCAD repository execution model](004-scad-repository-execution-model/README.md) — qualified the common conditional-SCAD execution model through the template and both reusable SCAD libraries.
- [003 — SCAD v0.12 rollout](003-scad-v0.12-rollout/README.md) — rolled the released tool through the template, both SCAD libraries and the real HUB75 frame.
- [002 — SCAD build-decision audit](002-scad-build-decision-audit/README.md) — added and qualified the explicit post-build decision audit.
- [001 — Consolidate public portfolio context into brainboxemb.meta](001-brainboxemb-meta/README.md) — completed repository/catalog/dashboard/documentation consolidation.

## When to create a migration

Use a migration when one coordinated change genuinely needs several repositories or has an ordering/evidence problem across repository boundaries.

Project-specific work remains in the project repository. A useful improvement discovered during a migration does not automatically become part of the blocking migration; it can be scheduled separately.
