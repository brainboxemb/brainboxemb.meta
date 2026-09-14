# Migration 001 — Consolidate public coordination into brainboxemb.meta

Status: **active — Phase 5 reassessment**

Tracking issue: [#11](https://github.com/brainboxemb/brainboxemb.meta/issues/11)

Evidence: [evidence.md](evidence.md)

## Goal

Turn `brainboxemb.meta` into the portfolio-level coordination and overview source for public brainboxemb repositories while preserving productive operation throughout the migration.

The migration consolidates responsibilities originally split across:

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

Only a blocker may extend the current phase. Do not start a later phase merely because an older plan says it is next.

## Phase 1 — Establish the meta foundation

Status: **complete**

- PR #12 established the meta identity and migration structure.
- Main merge: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`.
- Deploy run `34853241040` qualified tests, dashboard generation and Pages publication.

## Phase 2 — Canonical public repository catalog

Status: **complete**

- `repositories/catalog.yml` became the canonical public repository inventory/classification source.
- Qualified baseline: 29 public repositories.
- Stable SCAD current/classic infrastructure metadata was retained.
- Dashboard membership is derived from the central catalog instead of a second list.
- PR #14 merge: `7a8ad3974bf9b3e43ce0744825d124595ae894e2`.
- Deploy run `34855023365` green; 28 tests; `29 repositories in 6 groups`; Pages green.

## Phase 3 — Isolate dashboard implementation

Status: **complete**

The dashboard implementation now lives under `dashboard/`; repository-level workflows remain under `.github/workflows/`.

Evidence:

- PR #15 merge: `fa1a2157f0ad39d3a64efa1fe02bcb614b281343`;
- Deploy run `34856871791` green;
- 28 tests green from relocated paths;
- runtime preparation: `29 repositories in 6 groups`;
- first relocated metrics refresh: `4179 runs across 29 repositories`;
- dashboard generation green for 29 repositories;
- Pages artifact from `dashboard/site` and Pages deployment green.

## Phase 4 — Integrate tech.scad

Status: **complete**

Reassessment showed that Phase 2 had already absorbed the machine-readable catalog responsibility. `tech.scad` had no open issues, so its static tooling/library/project tables were deliberately **not** copied into another maintained set.

Durable knowledge moved into `brainboxemb.meta`:

- broad SCAD landscape architecture;
- current-versus-classic project-infrastructure semantics;
- engine versus infrastructure as separate classifications;
- direct-dependency and migration-scope rules;
- distinction between the broad domain view and the smaller controlled integration set.

Evidence:

- meta PR #16 moved the durable domain knowledge; merge `7ca593b76a26ac05861b86604fcb6f25baeac5fa`;
- `tech.scad` PR #2 redirected readers/agents to the new owner while retaining historical files; merge `b04e539a2215efa3b38fe1aa5a4d657fe4a89ae1`;
- the central catalog now marks `tech.scad` as `lifecycle: superseded`;
- `tech.scad` remains unarchived until Phase 6 so history and links stay available.

## Phase 5 — Integrate meta.scad-projects

Status: **reassess before implementation**

This phase must not become another broad blocking migration. First inspect the **current** `meta.scad-projects` main branch, open issues, active plans and generated/evidence outputs, then classify material into:

```text
durable cross-project architecture / working convention
    -> migrate to brainboxemb.meta

active repository-spanning migration / issue
    -> migrate only if still current, with handoff/evidence

historical completed plan / evidence
    -> leave in source history and link when useful

project-specific implementation
    -> leave in the owning repository
```

Split Phase 5 into smaller slices if needed. Do not let historical-document cleanup block current SCAD/tooling production work.

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
