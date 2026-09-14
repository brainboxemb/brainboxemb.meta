# Migration 001 — Consolidate public coordination into brainboxemb.meta

Status: **active — Phase 4 tech.scad integration**

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

- PR #12 established the meta identity and migration structure.
- Main merge: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`.
- Deploy run `34853241040` qualified tests, dashboard generation and Pages publication.

## Phase 2 — Canonical public repository catalog

Status: **complete**

Result:

- `repositories/catalog.yml` is the canonical public repository inventory/classification source;
- the qualified baseline contains 29 public repositories;
- stable SCAD current/classic infrastructure metadata is retained;
- `tool.eng-docs` is the current engineering-documentation tool name;
- dashboard membership is derived from the central catalog instead of a second list.

Evidence:

- PR #14 merge: `7a8ad3974bf9b3e43ce0744825d124595ae894e2`;
- exact-main Deploy run `34855023365` green;
- 28 tests green;
- runtime preparation: `29 repositories in 6 groups`;
- Pages publication green.

## Phase 3 — Isolate dashboard implementation

Status: **complete**

The dashboard implementation now lives under:

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

Repository-level workflows remain under `.github/workflows/` and run dashboard commands with `dashboard/` as their working directory.

Evidence:

- PR #15 merge: `fa1a2157f0ad39d3a64efa1fe02bcb614b281343`;
- exact-main Deploy run `34856871791` green;
- 28 tests green from relocated paths;
- runtime preparation: `29 repositories in 6 groups`;
- first relocated metrics refresh: `4179 runs across 29 repositories`;
- dashboard generation green for 29 repositories;
- Pages artifact from `dashboard/site` and final Pages deployment green.

See [evidence.md](evidence.md) for the detailed qualification record.

## Phase 4 — Integrate tech.scad

Status: **active**

Reassessment result: most of the original Phase-4 catalog work was already completed by Phase 2. The current `tech.scad` repository has no open issues and its separate tooling/library/project tables would only recreate manual duplication if copied here.

The remaining durable responsibilities are deliberately narrow:

- preserve broad SCAD landscape architecture under `domains/scad/`;
- preserve current-vs-classic project-infrastructure semantics;
- preserve the rule that CAD engine and infrastructure generation are separate classifications;
- preserve direct-dependency and migration-scope rules;
- preserve the distinction between the broad domain view and the smaller controlled integration set;
- keep repository membership/classification in the central catalog rather than new static tables.

Phase-4 completion requires:

1. equivalent durable domain architecture/navigation in `brainboxemb.meta`;
2. `tech.scad` to point readers/agents to the new current owner instead of presenting itself as the active catalog authority;
3. central catalog lifecycle/status to reflect that transition;
4. no loss of historical information, which remains available in `tech.scad` Git history.

Archival itself remains Phase 6 so it is not coupled to the knowledge migration.

## Phase 5 — Integrate meta.scad-projects

Status: **planned; revalidate before execution**

Migrate durable cross-project SCAD architecture, working conventions, active migrations and still-active cross-project issues.

Do **not** copy old plans wholesale. Separate current durable knowledge from historical evidence and obsolete implementation assumptions.

Project-specific implementation remains in its owning project repository.

Before implementation, split this phase further if necessary so active production/tooling work is not blocked by historical-document migration.

## Phase 6 — Close superseded sources

Status: **planned; revalidate before execution**

After current responsibilities and important links/evidence are covered:

- update remaining references to the new coordination source;
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
