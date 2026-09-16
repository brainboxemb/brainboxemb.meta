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

**None.**

Migration 005 is complete. Migration 006 is the next intended candidate, but remains proposed/inactive until it is explicitly activated after current-state revalidation.

## Proposed / inactive

The intended sequencing is **006 → 007** unless cross-project priorities are explicitly changed later.

- [006 — simplify the Java execution architecture](006-java-execution-architecture/README.md) — next intended candidate. Current status and preferred direction are recorded on `main`; Maven remains build/test authority, but the target architecture and owner-by-owner qualification plan must be revalidated before activation.
- [007 — standardise GitHub Actions dependency maintenance](007-github-actions-dependency-maintenance/README.md) — standardise action pinning/update policy and evaluate Dependabot plus `actions-up` for PR-based maintenance and audit. Planning-only and intentionally sequenced after Migration 006.

## Complete

- [005 — simplify the SCAD execution architecture](005-scad-execution-architecture/README.md) — completed the capability-oriented SCAD execution architecture, released `tool.scad-project v0.14.8`, qualified/released `template.scad-project v0.0.5`, and qualified/released the HUB75 frame as `v0.0.2` with exact immutable release provenance.
- [004 — SCAD repository execution model](004-scad-repository-execution-model/README.md) — qualified the common conditional-SCAD execution model through the template and both reusable SCAD libraries; retained measured performance evidence and handed architecture simplification/final frame rollout to Migration 005.
- [003 — SCAD v0.12 rollout](003-scad-v0.12-rollout/README.md) — rolled the released tool through the template, both SCAD libraries and the real HUB75 frame.
- [002 — SCAD build-decision audit](002-scad-build-decision-audit/README.md) — added and qualified the explicit post-build decision audit.
- [001 — Consolidate public portfolio context into brainboxemb.meta](001-brainboxemb-meta/README.md) — completed repository/catalog/dashboard/documentation consolidation.

## When to create a migration

Use a migration when one coordinated change genuinely needs several repositories or has an ordering/evidence problem across repository boundaries.

Project-specific work remains in the project repository. A useful improvement discovered during a migration does not automatically become part of the blocking migration; it can be scheduled separately.
