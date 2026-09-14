# Phase 5 closeout — meta.scad-projects consolidation

## Purpose

Retain the information needed to understand the public current state after `meta.scad-projects` becomes archived/private.

The old repository keeps detailed historical documents, Git history, PRs and issue discussions for the owner, but public current guidance must not depend on access to it.

## Current public owner

`brainboxemb.meta` now owns:

- the public repository landing page and catalog;
- shared project/tooling working-model documentation;
- current SCAD domain overview;
- cross-project migration planning/status;
- the public dashboard.

Implementation detail remains in the owning public tool/library/project repositories.

## Source redirect

`meta.scad-projects` PR #44 replaced its root README/AGENTS with a historical-source redirect.

- redirect PR head: `6ccf161b2f3ee2b78efa3bd2d449a4d41432bdd5`;
- merge commit: `6071b21c247359e5fd40b610020494d82b5699ab`.

The redirect states that no new cross-project work should be started there and that public current documentation must not depend on future access to the repository.

## Old open-work disposition

The old repository no longer has current cross-project work that needs to remain active there.

| Old item | Disposition in brainboxemb.meta |
| --- | --- |
| `meta.scad-projects#8` — Step-3 audit reassessment | Reframed as **proposed/inactive Migration 002 — SCAD build-decision audit** (`#19`, activation gate `#26`). |
| `meta.scad-projects#13` — R2 capability-impact contract | Closed as superseded/not planned; the old sequence was overtaken by the completed Moon repository-build architecture. Reassess from current implementation if such capability pruning is needed later. |
| `meta.scad-projects#20` — architecture view refresh | Deferred documentation backlog in `brainboxemb.meta#21`. |
| `meta.scad-projects#21` — explicit release trigger/version preparation | Deferred cross-project follow-up in `brainboxemb.meta#20`. |
| `meta.scad-projects#35` — T6 persistent execution evidence | Closed completed. Repository-build/Moon production transition is recorded as a completed foundation. |
| `meta.scad-projects#42` — physical verification bundles | Reframed as deferred/non-blocking follow-up in `brainboxemb.meta#18`; it no longer blocks the next SCAD tooling migration. |

## Completed foundation summary retained publicly

The detailed historical qualification remains available to the owner in the archived source repository, but the public current state is summarized as follows:

### Repository-build / Moon production transition

Status: **complete through T6**.

Important retained qualification points:

- `tool.scad-project v0.11.0` release commit: `8e0bd8f3b31e421586554f2bc7cbd914d05836b6`;
- reference SCAD consumer exact-main qualification completed in `template.scad-project`;
- real HUB75 consumer qualification completed in `2026-009-01.cad.HUB75-display-frame`;
- real-consumer merge commit: `172c85f454b6f738a9090d49e7871f99cb429eca`;
- exact-main consumer run: `34849157429`;
- qualification covered producer evidence, domain evidence, orchestration/materialization evidence, publication context and cache/hydration behaviour.

The completed repository-build transition is not a current migration.

### SCAD build-decision foundations

Status: **complete**.

- structured per-target outcomes are available: `BUILT`, `CACHE_RESTORED`, `CURRENT`, `ERROR`;
- deterministic real-SCons decision/conformance testing is implemented;
- cache restore remains decision evidence, not an independent artifact-integrity guarantee.

The next audit layer is deliberately a separate proposed migration rather than an unfinished tail of this completed work.

### Engineering-document assembly foundation

Status: **complete**.

`tool.eng-docs v0.2.0`, release commit `a15d2d259be7a88921e6c1afd7572b5acfd0fdd3`, established the domain-neutral manifest/assembly boundary and was qualified across software documentation and SCAD reference-consumer use.

Physical-verification workbench-bundle integration is deferred separately; it is not required to call the generic assembly foundation complete.

## Visibility transition

The owner intends to archive and make `meta.scad-projects` private after this consolidation.

Because `repositories/catalog.yml` is a **public-repository-only** catalog, the `meta.scad-projects` entry must be removed once the GitHub visibility changes to private. Until then it may remain temporarily visible as a superseded public repository.

The final Migration 001 closeout should therefore verify:

1. `meta.scad-projects` is archived/private;
2. its public catalog entry has been removed;
3. dashboard generation remains green with the resulting public repository set;
4. `tech.scad` archival/visibility state is handled according to the owner's decision;
5. Migration 001 is closed without activating Migration 002 automatically.
