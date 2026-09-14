# Repository agent guidance

Persistent guidance for automated agents working in `brainboxemb.meta`.

## Repository purpose

`brainboxemb.meta` is the portfolio-level coordination source for **public** brainboxemb repositories.

It owns cross-project information and migrations, not the implementation of the projects it describes.

```text
brainboxemb.meta
    public repository catalog / lifecycle overview
    cross-project architecture and working conventions
    repository-spanning migration plans and evidence
    migration handoffs
    domain-level overviews
    dashboard/status overview
    experiment references and decisions

individual repository
    implementation
    project-specific architecture and plan
    local tests and releases
    project-specific issues and evidence
```

Do not move implementation detail into this repository merely because a migration touches multiple repositories.

## Determine current work

**Read `STATUS.md` first.**

It is the primary human-readable current-work entry point and distinguishes:

- completed foundations;
- the active migration/slice;
- deferred non-blocking follow-ups;
- proposed migrations that are intentionally inactive.

Do not infer current work from the highest step number in an older roadmap.

A migration marked **proposed / inactive** must not be implemented merely because its README/handoff exists. It requires an explicit activation decision and its current assumptions must be reassessed first.

## Current consolidation migration

Migration 001 is tracked in:

- issue #11;
- `migrations/001-brainboxemb-meta/README.md`;
- `migrations/001-brainboxemb-meta/handoff.md`.

Its current bounded Phase-5 transfer is tracked by issue #25 and the slices named in `STATUS.md`.

Before each phase, re-check actual repositories, open issues/PRs, CI/evidence and generated output. Do not execute a phase only because an older plan says it is next.

Explicitly re-evaluate:

- whether the phase still solves the right problem;
- whether owner/ownership boundaries are still correct;
- whether prerequisites/order still hold;
- whether later work already implemented part of the scope;
- whether planned evidence covers the real risk;
- whether the step can be made smaller or more reversible.

## Keep the blocking path small

Classify every newly discovered item before adding it to an active migration:

```text
migration blocker
    required for the current migration to be safe/correct

follow-up migration
    valuable cross-project change, but not required to finish the current slice

backlog / improvement
    useful cleanup or enhancement that should not block productive work
```

Do not promote a follow-up or improvement into a blocker merely because it was discovered during migration.

Each phase should leave affected repositories usable and should be independently reviewable.

## Migration plan convention

Repository-spanning migrations live under `migrations/` and should have:

```text
README.md      goal, status, scope, ownership, phases and completion criteria
handoff.md     reusable ChatGPT/new-session handoff
evidence.md    retained qualification evidence when useful
```

Migration status must be explicit: `active`, `proposed / inactive`, or `complete` where applicable.

Individual project plans remain in the owning repository. When a migration needs changes in another repository, implement those details there and record only cross-project status/evidence here.

## Repository catalog

`repositories/catalog.yml` is the canonical source of truth for public repository membership and stable classification.

Live operational facts that can be read from GitHub should be generated/read from GitHub rather than manually duplicated. The catalog focuses on stable classification and intent: role, domain, lifecycle/generation and relevant ownership/provider relationships.

`tech.scad` is now a superseded historical source, not a second current catalog owner.

## Domain views

Domain-specific cross-project knowledge belongs under `domains/<domain>/` only when it is still useful at portfolio level.

Do not copy entire old repositories blindly. Separate:

- durable cross-project architecture/conventions;
- historical migration evidence worth retaining;
- project-local implementation detail that stays with its owner;
- obsolete planning that remains accessible through archived repository history rather than becoming current guidance.

## Issues and history

Open issues from an older meta repository should be recreated here only when they still represent real work worth tracking. Preserve origin links and classify them as active migration, proposed migration, deferred follow-up, backlog, completed or superseded.

Do not leave a completed historical issue appearing as current work merely because it was accidentally left open in the old repository.

Superseded repositories should be archived, not deleted, after current responsibilities are covered and important history/evidence remains navigable.

## Dashboard

The dashboard is an active sub-capability isolated under `dashboard/`:

```text
dashboard/
    dashboard.yml
    requirements.txt
    src/
    site/
    tests/
    README.md
    AGENTS.md
```

Repository-level GitHub Actions workflows stay under `.github/workflows/`. Dashboard workflows run commands with `dashboard/` as their working directory.

See `dashboard/README.md` and `dashboard/AGENTS.md` for dashboard-specific rules.

## Testing and evidence

Use the owner repository's normal tests for implementation changes. For dashboard changes:

```text
cd dashboard
python -m unittest discover -s tests -v
```

A cross-project phase is complete only when its required evidence exists, not merely when files were moved. Prefer exact revisions/run IDs where reproducibility matters.

## Documentation discipline

Root documentation describes current portfolio-level behavior. Historical/planning language that is no longer current should be clearly marked historical or remain in archived source history.

Keep generated operational state out of maintained Markdown when it can be generated from repositories themselves.
