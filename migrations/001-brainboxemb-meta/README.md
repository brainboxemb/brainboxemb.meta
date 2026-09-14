# Migration 001 — Consolidate public portfolio context into brainboxemb.meta

Status: **final qualification pending**

Tracking issue: [#11](https://github.com/brainboxemb/brainboxemb.meta/issues/11)

Phase-5 umbrella: [#25](https://github.com/brainboxemb/brainboxemb.meta/issues/25)

Final closeout: [#32](https://github.com/brainboxemb/brainboxemb.meta/issues/32)

Evidence: [evidence.md](evidence.md)

Phase-5 closeout summary: [phase5-meta-scad-closeout.md](phase5-meta-scad-closeout.md)

Current plain-language status: [`../../STATUS.md`](../../STATUS.md)

## Goal

Turn `brainboxemb.meta` into the landing page, technical guide, public repository overview and cross-project coordination source for the public brainboxemb repository collection, while keeping implementation ownership in the individual repositories.

The migration consolidated responsibilities that had been split across:

- the former `brainboxemb.dashboard` repository;
- `tech.scad` for the broad SCAD catalog/landscape;
- `meta.scad-projects` for current-stack SCAD architecture and migration coordination.

## Ownership boundary

`brainboxemb.meta` owns:

- the public repository catalog and stable classification;
- the portfolio landing page and common technical working model;
- domain-level overviews such as `domains/scad/`;
- repository-spanning migration plans, handoffs and retained coordination evidence;
- the dashboard/status presentation.

Individual repositories own their implementation, project-specific architecture/plans, tests, releases and detailed technical documentation.

## Migration discipline

Discoveries are classified as:

```text
migration blocker
follow-up migration
backlog / improvement
```

Only a blocker extends an active migration. A later migration may be documented as **proposed / inactive** without being activated.

## Phase 1 — Meta foundation

Status: **complete**

- PR #12 established the new meta identity and migration structure.
- Main merge: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`.
- Deploy run `34853241040` qualified tests, dashboard generation and Pages publication.

## Phase 2 — Canonical public repository catalog

Status: **complete**

- `repositories/catalog.yml` became the canonical public repository inventory/classification source.
- Initial qualified baseline: 29 public repositories.
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
- dashboard generation and Pages deployment green.

## Phase 4 — Integrate tech.scad

Status: **complete**

The canonical machine-readable catalog responsibility had already moved in Phase 2, so static duplicate repository tables were not copied.

Durable SCAD landscape knowledge moved into `domains/scad/`.

Evidence:

- meta PR #16 merge `7ca593b76a26ac05861b86604fcb6f25baeac5fa`;
- `tech.scad` redirect PR #2 merge `b04e539a2215efa3b38fe1aa5a4d657fe4a89ae1`;
- closeout PR #17 merge `70526bf2c3cf903e0f72bada788eb83924509159`;
- exact-main Deploy run `34858288823` green including Pages deployment;
- final archive/private-ready `tech.scad` PR #3 merge `26a2ef228231bdad9b8ebfb884a54506a7a01c6d`;
- GitHub verified on 2026-09-14 that `brainboxemb/tech.scad` is `private: true` and `archived: true`.

## Phase 5 — Transfer meta.scad-projects coordination

Status: **coordination transfer complete**

The completed repository-build roadmap was not copied as active work. Only durable current conventions, current/deferred work and enough retained evidence to preserve public understanding were transferred.

### 5A — readable current status

Status: **complete** — issue #27 / PR #35.

- established a readable current-change status;
- separated completed, deferred and proposed work;
- retired “Step 2.5 core complete” as current headline wording;
- prepared Migration 002 as proposed/inactive rather than automatically next.

### 5B — durable technical conventions

Status: **complete** — issue #30 / PR #36, followed by reader-oriented landing-page correction PR #37.

Public guidance now covers project organisation, repository/tool/domain boundaries, generated-output publication, evidence identities and version/release interfaces.

### 5C — active issue transfer and source redirect

Status: **complete** — issue #31.

- old open coordination issues were completed, superseded or recreated here;
- `meta.scad-projects` PR #44 redirected current work to the new owner;
- redirect merge: `6071b21c247359e5fd40b610020494d82b5699ab`;
- essential public status/evidence is retained in [phase5-meta-scad-closeout.md](phase5-meta-scad-closeout.md).

### 5D — archival/private closeout

Status: **visibility complete; dashboard qualification pending** — issue #32.

Verified GitHub state on 2026-09-14:

```text
brainboxemb/meta.scad-projects   private + archived
brainboxemb/tech.scad            private + archived
```

Public SCAD documentation was made independent of both repositories in `brainboxemb.meta` PR #39, merge `4a14762f83156f260cf3ce5cbc90cc00c9248c94`.

The current closeout change removes both private repositories from `repositories/catalog.yml`. The resulting public catalog contains **27 repositories**. Migration 001 closes only after the exact-main dashboard/Pages run qualifies that catalog and the evidence is recorded.

## Proposed next work after Migration 001

[`../002-scad-build-decision-audit/README.md`](../002-scad-build-decision-audit/README.md) remains **proposed / inactive**.

It describes a bounded SCAD post-build decision audit. It must be reassessed and explicitly activated after this migration closes; it does not start automatically.

Physical-verification document bundle integration remains a separate deferred follow-up (issue #18).

## Completion criteria

Migration 001 is complete when:

- `brainboxemb.meta` is the clear public landing page and technical guide;
- the canonical catalog contains only public repositories and drives the dashboard;
- dashboard tests, generation and Pages deployment are green against the 27-repository post-archive catalog;
- durable shared architecture/conventions have a current public owner here;
- active repository-spanning work has been classified and transferred, deferred or closed;
- `tech.scad` and `meta.scad-projects` are private/archived and no longer required for public current understanding;
- Migration 002 remains inactive unless separately activated.
