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

- [011 — refresh current-generation SCAD baseline](011-current-scad-baseline/README.md) — qualify released generic/SCAD tool and Forge/util baselines, then align every catalogued current-generation SCAD repository in dependencies, managed bootstrap/update launchers and reusable GitHub Actions callers.

## Proposed / inactive

- [007 — standardise GitHub Actions dependency maintenance](007-github-actions-dependency-maintenance/README.md) — standardise action pinning/update policy and evaluate Dependabot plus `actions-up`; remains inactive while Migration 011 is the selected cross-project track; Migration 011 does not standardise third-party action update policy.

## Complete

- [010 — standardise SCAD documentation and agent guidance](010-scad-documentation-agent-guidance/README.md) — qualified the blank-agent model through real current-generation SCAD libraries/projects, corrected shared conventions from canary evidence, aligned retained lab/experiment guidance and updated the template last.

- [009 — serialize SCAD production and roll out corrected tooling](009-scad-production-serialization/README.md) — released final owner baseline `tool.scad-project v0.15.7`, qualified the retained Experiment 006 matrix, aligned every current-generation consumer, and repaired HUB75 exact-main Build/Verification publication.
- [008 — adopt transitive SCAD library dependencies](008-transitive-scad-library-dependencies/README.md) — released `tool.git-project v0.2.9` and `tool.scad-project v0.15.2`, qualified the template and full Experiment 006 regression suite, then proved the real `lib.scad.mechint -> lib.scad.util` chain on exact-main run `35658098181`.
- [006 — simplify the Java execution architecture](006-java-execution-architecture/README.md) — released `tool.java-project v0.3.2`, immutable `template.java-project v0.1.0`, real event-timing PR/main qualification and downstream `2026-010-02.java.event-timing-framework v0.2.1` all agree on selective PR/release Windows execution and Windows-free ordinary main publication; durable rules now live in [`domains/software/40-01-java-execution.md`](../domains/software/40-01_java-execution.md).
- [005 — simplify the SCAD execution architecture](005-scad-execution-architecture/README.md) — the execution/publication architecture is qualified on `bld` / `vrf`; released owner guidance is aligned in `tool.scad-project v0.14.10` and proven by the green exact-main template run `35140381160`.
- [004 — SCAD repository execution model](004-scad-repository-execution-model/README.md) — qualified the common conditional-SCAD execution model through the template and both reusable SCAD libraries.
- [003 — SCAD v0.12 rollout](003-scad-v0.12-rollout/README.md) — rolled the released tool through the template, both SCAD libraries and the real HUB75 frame.
- [002 — SCAD build-decision audit](002-scad-build-decision-audit/README.md) — added and qualified the explicit post-build decision audit.
- [001 — Consolidate public portfolio context into brainboxemb.meta](001-brainboxemb-meta/README.md) — completed repository/catalog/dashboard/documentation consolidation.

Historical already-published `build` / `verification` branches remain historical evidence and are not rewritten. Current-generation shared technical publication identities use the compact namespace documented in the working model.

## When to create a migration

Use a migration when one coordinated change genuinely needs several repositories or has an ordering/evidence problem across repository boundaries.

Project-specific work remains in the project repository. A useful improvement discovered during a migration does not automatically become part of the blocking migration; it can be scheduled separately.
