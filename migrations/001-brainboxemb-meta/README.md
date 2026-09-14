# Migration 001 — Consolidate public coordination into brainboxemb.meta

Status: **active — Phase 3 dashboard relocation**

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
- preserve the working dashboard without coupling the rename to a filesystem move.

Completion evidence:

- PR #12 qualified the exact Phase-1 change set;
- merge commit `62df26489e84dedc9cbd11c7cdf7186e0b78261d` is on `main`;
- Deploy run `34853241040` passed on that exact commit;
- dashboard tests, generation, Pages artifact upload and Pages deployment passed.

## Phase 2 — Canonical public repository catalog

Status: **complete**

Goal:

Create one domain-neutral public repository catalog under `repositories/` from the proven stable classification in `tech.scad/catalog.yml` plus the broader dashboard repository membership, while keeping live operational state in GitHub.

Result:

- `repositories/catalog.yml` is the canonical public repository inventory/classification source;
- it contains 29 unique public repositories in the qualified baseline;
- stable SCAD current/classic infrastructure metadata is retained;
- `tool.eng-docs` is the current engineering-documentation tool name; obsolete `tool.sw-docs` is not a separate entry;
- `dashboard.yml` no longer carries a second repository inventory;
- `src/prepare_dashboard_config.py` converts catalog membership/grouping to the existing dashboard runtime contract;
- dashboard collector, metrics and renderer semantics were not redesigned.

Completion evidence:

- PR #14 merged as `7a8ad3974bf9b3e43ce0744825d124595ae894e2`;
- exact-main Deploy run `34855023365` passed;
- all 28 tests passed;
- runtime preparation reported `29 repositories in 6 groups`;
- dashboard generation successfully collected and rendered all 29 repositories;
- Pages artifact upload and Pages deployment passed.

## Phase 3 — Isolate dashboard implementation

Status: **active**

Goal:

Move the dashboard implementation into `dashboard/` now that catalog ownership is stable, without changing dashboard behaviour.

Scope:

```text
dashboard/dashboard.yml
dashboard/requirements.txt
dashboard/src/
dashboard/site/
dashboard/tests/
dashboard/README.md
dashboard/AGENTS.md
```

Repository-level workflows stay under `.github/workflows/` because GitHub requires that location. They run dashboard commands with `dashboard/` as their working directory.

Completion requires:

- no dashboard runtime/config/test/static files left at their former root paths;
- central catalog reference still resolves correctly from the moved config;
- unit tests green;
- runtime config generation green;
- dashboard generation green;
- Pages publication green on exact `main`.

Do not combine this phase with dashboard redesign.

## Phase 4 — Integrate tech.scad

Status: **planned; revalidate before execution**

Migrate durable SCAD catalog/domain documentation into:

```text
repositories/catalog.yml
domains/scad/
```

Preserve the useful distinction between broad domain membership and a smaller controlled integration set.

Do not copy historical material merely because it exists. Prefer current durable knowledge and links to historical evidence.

Only after equivalent navigation/classification exists here should `tech.scad` become a candidate for archival.

## Phase 5 — Integrate meta.scad-projects

Status: **planned; revalidate before execution**

Migrate durable cross-project SCAD architecture, working conventions, active migrations and still-active cross-project issues.

Do **not** copy old plans wholesale. Separate current durable knowledge from historical evidence and obsolete implementation assumptions.

Project-specific implementation remains in its owning project repository.

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
