# Cross-project migrations

This directory contains migrations that intentionally span more than one public brainboxemb repository.

A migration should be bounded and independently reviewable. It is not a container for every improvement discovered while work is in progress.

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

## Ownership

The migration plan lives here. Implementation details and project-specific plans stay in the repository that owns the behavior being changed.

## Active migration

- [001 — Consolidate public coordination into brainboxemb.meta](001-brainboxemb-meta/README.md)
