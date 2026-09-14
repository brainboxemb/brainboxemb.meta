# Migration 001 — Consolidate public coordination into brainboxemb.meta

Status: **active — Phase 5A readable current status**

Tracking issue: [#11](https://github.com/brainboxemb/brainboxemb.meta/issues/11)

Phase-5 umbrella: [#25](https://github.com/brainboxemb/brainboxemb.meta/issues/25)

Evidence: [evidence.md](evidence.md)

Current plain-language status: [`../../STATUS.md`](../../STATUS.md)

## Goal

Turn `brainboxemb.meta` into the portfolio-level coordination and overview source for public brainboxemb repositories while preserving productive operation throughout the migration.

The migration consolidates responsibilities originally split across:

```text
brainboxemb.meta        former dashboard repository / live status UI
tech.scad               broad SCAD catalog and landscape documentation
meta.scad-projects      SCAD cross-project architecture and migration coordination
```

The result should reduce duplicated sources without turning `brainboxemb.meta` into the implementation owner of every project.

## Non-goals

This migration does **not**:

- migrate private repositories;
- rewrite individual project plans into the meta repository;
- modernize every legacy project;
- implement deferred SCAD/tooling improvements;
- absorb experiment/test code;
- resume old roadmap steps simply because they are present in historical documentation.

## Ownership boundary

`brainboxemb.meta` owns public catalog/classification, cross-project architecture/conventions, repository-spanning migration coordination/evidence, domain overview and dashboard/status presentation.

Individual repositories continue to own implementation, project-specific plans/issues, releases, tests and detailed technical design.

## Migration discipline

Classify discoveries as:

```text
migration blocker
follow-up migration
backlog / improvement
```

Only a blocker may extend the current migration slice.

A later migration can be prepared as **proposed / inactive** without becoming current work. Activation is an explicit decision.

## Phase 1 — Meta foundation

Status: **complete**

- PR #12 established the meta identity and migration structure.
- Main merge: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`.
- Deploy run `34853241040` qualified tests, dashboard generation and Pages publication.

## Phase 2 — Canonical public repository catalog

Status: **complete**

- `repositories/catalog.yml` became the canonical public repository inventory/classification source.
- Qualified baseline: 29 public repositories.
- Dashboard membership is derived from that catalog.
- PR #14 merge: `7a8ad3974bf9b3e43ce0744825d124595ae894e2`.
- Deploy run `34855023365` green; 28 tests; `29 repositories in 6 groups`; Pages green.

## Phase 3 — Isolate dashboard implementation

Status: **complete**

Dashboard implementation lives under `dashboard/`; repository-level workflows remain under `.github/workflows/`.

Evidence:

- PR #15 merge: `fa1a2157f0ad39d3a64efa1fe02bcb614b281343`;
- Deploy run `34856871791` green;
- 28 relocated tests green;
- runtime preparation `29 repositories in 6 groups`;
- first relocated metrics refresh `4179 runs across 29 repositories`;
- dashboard generation and Pages deployment green.

## Phase 4 — Integrate tech.scad

Status: **complete**

Phase 2 had already absorbed the machine-readable catalog responsibility, so static repository tables were not copied again.

Durable SCAD landscape knowledge moved into `brainboxemb.meta`, and `tech.scad` now redirects current readers/agents while retaining history.

Evidence:

- meta PR #16 merge `7ca593b76a26ac05861b86604fcb6f25baeac5fa`;
- `tech.scad` PR #2 merge `b04e539a2215efa3b38fe1aa5a4d657fe4a89ae1`;
- central catalog marks `tech.scad` as `superseded`;
- closeout PR #17 merge `70526bf2c3cf903e0f72bada788eb83924509159`;
- exact-main Deploy run `34858288823` green including Pages deployment.

## Phase 5 — Transfer meta.scad-projects coordination

Status: **active, split into bounded slices**

The repository-build transition in the old meta repository is already complete. Phase 5 therefore does **not** copy its old roadmaps wholesale or present completed work as still active.

The remaining transfer is:

### 5A — readable current status

Status: **active** — issue #27.

- create `STATUS.md` as the primary human-readable current-work entry point;
- clearly separate completed foundations, deferred work and next proposed work;
- retire “Step 2.5 core complete” as current-status wording;
- prepare proposed/inactive Migration 002 with an explicit activation gate.

### 5B — durable SCAD coordination conventions

Status: **planned** — issue #30.

Move only cross-project rules that are still current, such as ownership boundaries, current/classic migration scope, dependency/bootstrap responsibilities and stable version/release interface conventions.

Historical plan detail and implementation detail remain in source/owner history.

### 5C — active issue transfer and source redirect

Status: **planned** — issue #31.

- finish transferring still-relevant coordination issues with origin links;
- close source issues whose work is complete or superseded;
- update `meta.scad-projects` README/agent guidance to point current coordination here;
- retain detailed historical documents/evidence until archival.

### 5D — consolidation closeout / archival readiness

Status: **planned** — issue #32.

Verify no current coordination responsibility still depends on the old meta repositories, then complete Migration 001 and prepare superseded repositories for archival.

## Proposed next work after Migration 001

[`../002-scad-build-decision-audit/README.md`](../002-scad-build-decision-audit/README.md) is intentionally **proposed / inactive**.

It describes the former actionable “Step 3” work in plain language as a separate SCAD build-decision audit migration. It must be reassessed and explicitly activated; it does not start automatically when Migration 001 completes.

Physical-verification document bundle integration is a separate deferred follow-up (issue #18) and does not block that migration.

## Completion criteria

Migration 001 is complete when:

- `brainboxemb.meta` is the clear entry point for public cross-project coordination;
- one canonical public repository catalog drives the overview/dashboard;
- dashboard functionality and Pages publication remain healthy;
- durable SCAD domain architecture/conventions have a current owner here;
- active repository-spanning work has been classified and either transferred, deferred or closed;
- `meta.scad-projects` no longer owns current coordination work;
- superseded source repositories can be archived without losing current responsibility or important evidence.
