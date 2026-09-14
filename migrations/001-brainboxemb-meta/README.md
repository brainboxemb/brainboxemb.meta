# Migration 001 — Consolidate public coordination into brainboxemb.meta

Status: **active — final archival/private closeout**

Tracking issue: [#11](https://github.com/brainboxemb/brainboxemb.meta/issues/11)

Phase-5 umbrella: [#25](https://github.com/brainboxemb/brainboxemb.meta/issues/25)

Evidence: [evidence.md](evidence.md)

Phase-5 closeout summary: [phase5-meta-scad-closeout.md](phase5-meta-scad-closeout.md)

Current plain-language status: [`../../STATUS.md`](../../STATUS.md)

## Goal

Turn `brainboxemb.meta` into the portfolio-level landing page, technical guide, repository overview and coordination source for public brainboxemb repositories while preserving productive operation throughout the migration.

The migration consolidates responsibilities originally split across:

```text
brainboxemb.meta        former dashboard repository / live status UI
tech.scad               broad SCAD catalog and landscape documentation
meta.scad-projects      SCAD cross-project architecture and migration coordination
```

The result reduces duplicated sources without turning `brainboxemb.meta` into the implementation owner of every project.

## Non-goals

This migration does **not** migrate private projects, rewrite individual project plans into meta, modernize every legacy project, implement deferred SCAD/tooling improvements, absorb experiment code, or resume old roadmap steps merely because they remain in historical documentation.

## Ownership boundary

`brainboxemb.meta` owns the public landing page, repository catalog/classification, shared technical guidance, domain-level overviews, repository-spanning migration coordination/evidence and dashboard/status presentation.

Individual repositories continue to own implementation, project-specific plans/issues, releases, tests and detailed technical design.

## Migration discipline

Classify discoveries as `migration blocker`, `follow-up migration`, or `backlog / improvement`. Only a blocker may extend the current migration slice.

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

Status: **coordination transfer complete; final visibility/catalog closeout remains**

The repository-build transition in the old meta repository was already complete. Phase 5 therefore did not copy old roadmaps wholesale or present completed work as still active.

### 5A — readable current status

Status: **complete** — issue #27 / PR #35.

Result:

- `STATUS.md` became the current-change status entry point;
- completed, deferred and proposed work were separated explicitly;
- “Step 2.5 core complete” was retired as current headline wording;
- Migration 002 was created as a proposed/inactive plan with an explicit activation gate.

### 5B — durable technical conventions

Status: **complete** — issue #30 / PR #36, followed by reader-oriented landing-page correction PR #37.

Current public guidance now covers:

- how projects are organised;
- repository/tool/domain ownership boundaries;
- `tool.git-project` generic responsibilities;
- current/classic project-infrastructure classification;
- generated-output publication namespaces;
- producer/materialization/publication evidence separation;
- version/release interface rules.

The root README now treats migration coordination as one part of the repository rather than its entire purpose.

### 5C — active issue transfer and source redirect

Status: **complete** — issue #31.

- all old open coordination issues were completed, superseded or recreated as current/deferred work in `brainboxemb.meta`;
- `meta.scad-projects` PR #44 redirected README/AGENTS to the new owner;
- old repository redirect merge: `6071b21c247359e5fd40b610020494d82b5699ab`;
- essential public current-state/evidence summary is retained in [phase5-meta-scad-closeout.md](phase5-meta-scad-closeout.md), so public readers do not need access to the old repository after it becomes private.

### 5D — archival/private closeout

Status: **active — waiting for owner visibility action** — issue #32.

The owner intends to archive and make `meta.scad-projects` private.

After that external GitHub setting change:

1. remove `meta.scad-projects` from `repositories/catalog.yml` because the catalog is public-only;
2. regenerate/qualify the dashboard against the remaining public repository set;
3. verify no public current documentation depends on the private source;
4. close Migration 001;
5. leave Migration 002 proposed/inactive until explicitly activated.

## Proposed next work after Migration 001

[`../002-scad-build-decision-audit/README.md`](../002-scad-build-decision-audit/README.md) is intentionally **proposed / inactive**.

It describes the former actionable “Step 3” work in plain language as a separate SCAD build-decision audit migration. It must be reassessed and explicitly activated; it does not start automatically when Migration 001 completes.

Physical-verification document bundle integration is a separate deferred follow-up (issue #18) and does not block that migration.

## Completion criteria

Migration 001 is complete when:

- `brainboxemb.meta` is the clear public landing page and technical guide;
- one canonical public repository catalog drives the overview/dashboard;
- dashboard functionality and Pages publication remain healthy;
- durable shared architecture/conventions have a current owner here;
- active repository-spanning work has been classified and either transferred, deferred or closed;
- `meta.scad-projects` no longer owns current coordination work and is removed from the public catalog after becoming private;
- superseded-source visibility changes do not break public documentation or dashboard operation.
