# Repository agent guidance

Persistent guidance for automated agents working in `brainboxemb.meta`.

## Repository purpose

`brainboxemb.meta` is the **landing page, technical guide and portfolio overview** for the public brainboxemb repositories.

Its responsibilities include:

- explaining what repositories exist and what roles they have;
- describing how current projects are organised;
- documenting shared technical conventions and tooling boundaries;
- providing domain-level overviews;
- presenting live repository status through the dashboard;
- coordinating repository-spanning migrations and retaining their evidence;
- recording the role of experiments that support technical decisions.

Cross-repository migration coordination is therefore **one capability of this repository, not its whole purpose**.

Individual repositories remain authoritative for their own implementation, project-specific architecture/plans, releases, tests and local issues.

## Choose the right entry point

Use the repository according to the question being answered:

- general overview / first-time reader → `README.md`;
- how projects and tooling work → `docs/README.md` and `docs/working-model/`;
- which public repositories exist → `repositories/`;
- domain-specific ecosystem information → `domains/`;
- live GitHub/project status → `dashboard/`;
- current cross-project changes → `STATUS.md`;
- repository-spanning refactoring/migration → `migrations/`;
- technical experiments and their conclusions → `experiments/`.

Do **not** make `STATUS.md` or the active migration the framing for unrelated documentation work. They describe temporary/current work, while README/docs describe the repository collection and intended working model.

## Current work and migrations

When the task actually concerns current cross-project work, read `STATUS.md` first.

It distinguishes:

- completed foundations;
- active migration/slice;
- deferred non-blocking follow-ups;
- proposed migrations that are intentionally inactive.

Do not infer current work from the highest step number in an older roadmap.

A migration marked **proposed / inactive** must not be implemented merely because its README/handoff exists. It requires an explicit activation decision and current assumptions must be reassessed first.

Migration 001 is currently tracked in:

- issue #11;
- `migrations/001-brainboxemb-meta/README.md`;
- `migrations/001-brainboxemb-meta/handoff.md`.

Before every active migration phase, re-check actual repositories, issues/PRs, CI/evidence and generated output. Re-evaluate the goal, owner, prerequisites, current assumptions, evidence coverage and whether the slice can be smaller or more reversible.

## Keep the blocking path small

Classify newly discovered migration-related work as:

- **migration blocker** — required for the current migration to be safe/correct;
- **follow-up migration** — valuable cross-project change, but independently schedulable;
- **backlog / improvement** — useful cleanup or enhancement that should not block productive work.

Do not promote a follow-up or improvement into a blocker merely because it was discovered during migration.

## Migration plan convention

Repository-spanning migrations live under `migrations/` and should normally contain:

- `README.md` — purpose, status, scope, ownership, phases and completion criteria;
- `handoff.md` — reusable ChatGPT/new-session handoff;
- `evidence.md` — retained qualification evidence when useful.

Migration status must be explicit: `active`, `proposed / inactive`, or `complete` where applicable.

Implementation belongs in the repository that owns the behavior. `brainboxemb.meta` keeps the cross-project scope, status and evidence.

## Technical documentation

Technical pages should be written for a reader trying to understand the system, not as compressed internal implementation notes.

Prefer this order:

1. what problem/concept is being explained;
2. the mental model and practical meaning;
3. where it applies and where to look next;
4. lower-level configuration, commands or evidence only when useful.

Avoid making pages a wall of code blocks or migration terminology. Small examples are useful, but prose should explain why the reader cares about them.

Shared technical concepts live under `docs/`. Project-specific design stays in the owning project, and API/implementation detail stays in the owning tool/library.

## Repository catalog

`repositories/catalog.yml` is the canonical source of truth for public repository membership and stable classification.

Live operational facts that GitHub can provide should not be manually duplicated there. The catalog focuses on identity, role, domain, lifecycle/generation and relevant ownership/provider relationships.

`tech.scad` is a superseded historical source, not a second current catalog owner.

## Domain views

Domain-specific portfolio knowledge belongs under `domains/<domain>/` when it helps explain the ecosystem beyond one project.

Do not copy whole old repositories blindly. Separate durable cross-project knowledge from historical evidence, obsolete planning and project-local implementation detail.

## Issues and history

When consolidating an older meta repository, recreate only issues that still represent useful work. Preserve origin links and classify them clearly as active migration, proposed migration, deferred follow-up, backlog, completed or superseded.

Superseded repositories should be archived rather than deleted after their current responsibilities are covered and their history remains navigable.

## Dashboard

The dashboard is an active sub-capability under `dashboard/`. Repository-level GitHub Actions workflows remain under `.github/workflows/` because GitHub requires that location.

See `dashboard/README.md` and `dashboard/AGENTS.md` for dashboard-specific maintenance rules.

For dashboard tests:

```text
cd dashboard
python -m unittest discover -s tests -v
```

## Evidence and documentation discipline

A migration phase is complete only when its required evidence exists, not merely when files were moved. Prefer exact revisions/run IDs where reproducibility matters.

Root documentation should describe the current portfolio and working model. Historical planning language that is no longer current should either be marked historical or remain in archived source history.

Keep generated operational state out of maintained Markdown when it can be generated from repositories themselves.
