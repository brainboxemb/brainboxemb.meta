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

## Current consolidation migration

The active consolidation is tracked in:

- issue #11;
- `migrations/001-brainboxemb-meta/README.md`;
- `migrations/001-brainboxemb-meta/handoff.md`.

Before each migration phase, re-check the actual repositories, open issues/PRs, CI/evidence and current generated output. Do not execute a phase only because an older plan says it is next.

Explicitly re-evaluate:

- whether the phase still solves the right problem;
- whether the owner and ownership boundary are still correct;
- whether prerequisites/order still hold;
- whether later work has already implemented part of the planned scope;
- whether the planned evidence covers the real risk;
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

Do not promote a follow-up or improvement into a blocker merely because it was discovered during the migration.

Each phase should leave affected repositories usable and should be independently reviewable.

## Migration plan convention

Repository-spanning migrations live under `migrations/` and should have:

```text
README.md      goal, scope, phases, ownership, completion criteria
handoff.md     reusable ChatGPT/new-session handoff
evidence.md    retained qualification evidence when the phase produces it
```

Individual project plans remain in the owning repository.

When a migration needs changes in another repository, implement those details there and record only cross-project status/evidence here.

## Repository catalog

`repositories/catalog.yml` is the canonical source of truth for public repository membership and stable classification.

Live operational facts that can be read from GitHub should be generated/read from GitHub rather than manually duplicated in the catalog. The catalog focuses on stable classification and intent: role, domain, lifecycle/generation and relevant ownership/provider relationships.

`tech.scad/catalog.yml` remains an input/history source until its remaining useful SCAD-domain responsibilities have been migrated; do not let it become a second current all-domain catalog.

## Domain views

Domain-specific cross-project knowledge belongs under `domains/<domain>/` only when it is still useful at the portfolio level.

Do not copy entire old repositories blindly. Separate:

- durable cross-project architecture/conventions;
- historical migration evidence worth retaining;
- project-local implementation detail that should stay with its owner;
- obsolete planning that should remain accessible through archived repository history rather than become current guidance.

## Issues and history

Open issues from an older meta repository should be migrated only when they still represent active cross-project work. Preserve links to original issue/history. Closed historical issues do not need to be duplicated merely for completeness.

Superseded repositories should be archived, not deleted, after their current responsibilities are covered and important history/evidence remains navigable.

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

Repository-level GitHub Actions workflows stay under `.github/workflows/` because GitHub requires that location. Dashboard workflows run commands with `dashboard/` as their working directory.

Dashboard operational rules remain important:

- status normally reflects the latest run on the configured/default branch;
- release status may use the latest run regardless of branch because releases use temporary request branches;
- reusable-only workflows stay hidden by default;
- branch cleanup is observational and must never delete branches automatically;
- configured long-lived generated branches such as `build`, `dev/*`, `prod/*`, `rel/*` and `gh-pages` are excluded from cleanup;
- unreadable repository settings remain `unknown`, not false;
- secrets/tokens must never be printed or written to generated output;
- Pages deployment remains change-aware and should not run only because time passed.

See `dashboard/README.md` and `dashboard/AGENTS.md` for dashboard-specific development rules.

## Testing and evidence

Use the owner repository's normal tests for implementation changes. For dashboard changes:

```text
cd dashboard
python -m unittest discover -s tests -v
```

A cross-project phase is complete only when its required evidence exists, not merely when files were moved.

Prefer exact revisions/run IDs for qualification evidence when reproducibility matters.

## Documentation discipline

Root documentation describes current portfolio-level behavior. Historical/planning language that is no longer current should either be clearly marked as historical or remain in archived source history.

Keep generated operational state out of maintained Markdown when it can be generated from repositories themselves.
