# Cross-project migrations

This directory contains migrations that intentionally span more than one public brainboxemb repository.

A migration should be bounded and independently reviewable. It is not a container for every improvement discovered while work is in progress.

Start with [`../STATUS.md`](../STATUS.md) for the plain-language current position.

Each migration should normally contain:

```text
<migration>/
    README.md      scope, ownership, phases and completion criteria
    handoff.md     reusable new-chat / ChatGPT handoff
    evidence.md    retained qualification evidence when useful
```

## Scope discipline

Classify discovered work as:

- **migration blocker** — required to finish the current slice safely/correctly;
- **follow-up migration** — useful cross-project work that can be scheduled separately;
- **backlog / improvement** — non-blocking cleanup or enhancement.

Only migration blockers extend the current blocking path.

## Activation states

A migration can be:

- **active** — intentionally selected as current cross-project work;
- **proposed / inactive** — prepared so scope is clear, but implementation must not start automatically;
- **complete** — retained for evidence/history, not reopened merely to add another consumer or improvement.

Presence of a migration directory does not imply activation.

## Ownership

The migration plan lives here. Implementation details and project-specific plans stay in the repository that owns the behavior being changed.

## Active migration

- [001 — Consolidate public coordination into brainboxemb.meta](001-brainboxemb-meta/README.md) — **active**, currently transferring the remaining coordination state from `meta.scad-projects`.

## Proposed / inactive

- [002 — SCAD build-decision audit](002-scad-build-decision-audit/README.md) — **proposed / inactive**. It has a defined activation gate and must be reassessed before owner implementation starts.

Deferred improvements such as physical-verification document bundles remain issues/backlog until deliberately promoted to their own migration.