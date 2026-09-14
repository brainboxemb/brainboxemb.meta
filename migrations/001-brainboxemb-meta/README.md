# Migration 001 — Consolidate public coordination into brainboxemb.meta

Status: **active — Phase 2 catalog reassessment**

Tracking issue: [#11](https://github.com/brainboxemb/brainboxemb.meta/issues/11)

Evidence: [evidence.md](evidence.md)

## Goal

Turn the renamed `brainboxemb.meta` repository into the portfolio-level coordination and overview source for public brainboxemb repositories while preserving productive operation throughout the migration.

The migration consolidates responsibilities currently split across:

```text
brainboxemb.meta        former dashboard repository / live status UI
tech.scad               broad SCAD catalog and landscape documentation
meta.scad-projects      SCAD cross-project architecture and migration coordination
```

The result should reduce duplicated repository lists/status sources without turning `brainboxemb.meta` into the implementation owner of every project.

## Non-goals

This migration does **not**:

- migrate private repositories;
- rewrite individual project plans into the meta repository;
- modernize every legacy project;
- implement every deferred SCAD/tooling improvement;
- absorb experiment/test code into the meta repository;
- change unrelated domain tooling merely because it is discovered.

## Ownership boundary

`brainboxemb.meta` owns:

- public repository catalog/classification;
- cross-project architecture and working conventions;
- repository-spanning migration plans/handoffs/evidence;
- domain overview/navigation;
- dashboard/status presentation;
- references from experiments to adopted decisions.

Individual repositories continue to own implementation, project-specific plans, local issues, releases, tests and detailed technical design.

## Migration discipline

Before every phase, re-check the repositories and determine whether the planned work is still needed. Classify newly discovered items as:

```text
migration blocker
follow-up migration
backlog / improvement
```

Only a blocker may extend the current phase.

Do not start a later phase just because it exists in this document. Each phase has to be revalidated against current implementation first.

## Phase 1 — Establish the meta foundation

Status: **complete**

Purpose:

- accept the renamed repository as `brainboxemb.meta`;
- establish the portfolio-level README/agent guidance;
- create the migration/handoff structure;
- create clear places for repositories, domains and experiments;
- correct rename-sensitive dashboard configuration;
- preserve the working dashboard at its current paths.

Completion evidence:

- PR #12 qualified the exact Phase-1 change set;
- merge commit `62df26489e84dedc9cbd11c7cdf7186e0b78261d` is on `main`;
- Deploy run `34853241040` passed on that exact commit;
- dashboard unit tests passed in the Deploy build job;
- dashboard generation passed;
- Pages artifact upload and Pages deployment both passed;
- root documentation now describes the portfolio-level meta role;
- dashboard-specific documentation and agent guidance are preserved under `dashboard/`;
- dashboard implementation paths were deliberately not moved.

See [evidence.md](evidence.md) for retained Phase-1 evidence.

Explicitly deferred by Phase 1:

- moving `src/`, `site/`, `tests/`, `dashboard.yml` or workflows;
- creating the final canonical catalog;
- migrating `tech.scad` or `meta.scad-projects` content/issues.

## Phase 2 — Canonical public repository catalog

Status: **next candidate; reassessment in progress**

Goal:

Create one domain-neutral public repository catalog under `repositories/` from the proven stable classification in `tech.scad/catalog.yml` plus the broader repository membership currently duplicated in `dashboard.yml`.

The catalog should own stable facts such as:

- repository identity;
- category/domain;
- lifecycle/generation (for example current/classic/legacy where useful);
- high-level role;
- infrastructure/provider relationships.

Live workflow status, releases, branch protection, PR counts and similar changing facts should continue to come from GitHub.

Then adapt the dashboard to consume the canonical catalog instead of maintaining a second repository inventory.

Initial reassessment after Phase 1 shows that the existing dashboard collector already consumes a simple `groups[].repositories` structure before reading all live status from GitHub. Therefore Phase 2 should prefer a thin catalog-to-groups input transformation rather than redesigning the status engine.

Completion requires dashboard-equivalent coverage plus tests proving catalog parsing/grouping.

## Phase 3 — Isolate dashboard implementation

Status: **planned; revalidate before execution**

Move dashboard implementation into its dedicated subdirectory only after Phase 2 is stable.

Expected scope includes path changes for workflows, local commands, tests, static output and Pages artifacts. The move is complete only when the dashboard tests and Pages deployment are green on the new paths.

Do not combine this phase with unrelated dashboard redesign.

## Phase 4 — Integrate tech.scad

Status: **planned; revalidate before execution**

Migrate durable SCAD catalog/domain documentation into:

```text
repositories/catalog.yml
domains/scad/
```

Preserve the useful distinction between broad domain membership and a smaller controlled integration set.

Only after equivalent navigation/classification exists here should `tech.scad` become a candidate for archival.

## Phase 5 — Integrate meta.scad-projects

Status: **planned; revalidate before execution**

Migrate durable cross-project SCAD architecture, working conventions, active migrations and still-active cross-project issues.

Do **not** copy old plans wholesale. Separate current durable knowledge from historical evidence and obsolete implementation assumptions.

Project-specific implementation remains in its owning repository.

Active `meta.scad-projects` issues should be migrated when they still represent real cross-project work, with links to the original issue/discussion.

## Phase 6 — Close superseded sources

Status: **planned; revalidate before execution**

After all current responsibilities and important links/evidence are covered:

- update references to the new coordination source;
- archive superseded `tech.scad` / `meta.scad-projects` repositories rather than deleting them;
- retain their Git history, PRs and closed issues as historical evidence;
- record final migration evidence here.

## Completion criteria

Migration 001 is complete when:

- `brainboxemb.meta` is the clear entry point for public cross-project coordination;
- one canonical public repository catalog drives the overview/dashboard;
- dashboard functionality and Pages publication remain healthy;
- SCAD domain navigation/architecture no longer requires two active meta/catalog repositories;
- active repository-spanning plans/issues have a current owner and handoff;
- legacy/current classifications remain explicit;
- experiment repositories are referenced without becoming production dependencies;
- superseded repositories can be archived without losing current responsibility or evidence.
