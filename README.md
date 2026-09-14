# brainboxemb.meta

Central coordination, architecture, repository catalog, migration planning, and status overview for public brainboxemb projects and tooling.

## Start here

For the current cross-project position, read **[STATUS.md](STATUS.md)** first.

It answers in plain language:

- what is finished;
- what is active now;
- what is deferred and non-blocking;
- which migration is proposed next but not yet active.

Historical step numbers remain available in retained evidence but are not the primary status model.

## Purpose

`brainboxemb.meta` is the portfolio-level coordination repository for the public `brainboxemb` repositories.

It owns information that is intentionally broader than one implementation repository:

- the canonical public repository catalog and high-level lifecycle/classification;
- cross-project architecture and ownership boundaries;
- shared working conventions;
- current cross-project migrations, their evidence and ChatGPT handoffs;
- domain views such as the SCAD ecosystem;
- references to experiments that justify cross-project technical decisions;
- the GitHub Actions/status dashboard.

Individual repositories remain authoritative for their own implementation, project-specific plans, releases, local documentation and local issues.

This repository covers **public repositories only**. Private-project coordination belongs in an explicitly separate scope.

## Current migration

Migration 001 is consolidating responsibilities previously split across the dashboard repository, `tech.scad` and `meta.scad-projects`.

The dashboard/catalog and `tech.scad` slices are complete. The current bounded work is transferring only the still-current coordination responsibility from `meta.scad-projects`.

See:

- [STATUS.md](STATUS.md);
- [Migration 001](migrations/001-brainboxemb-meta/README.md);
- [issue #11](https://github.com/brainboxemb/brainboxemb.meta/issues/11).

Do not turn useful discoveries into migration blockers automatically. Classify them as:

```text
migration blocker
follow-up migration
backlog / improvement
```

Only the first category extends the blocking path.

## Continue cross-project work

While Migration 001 is active, use its [handoff](migrations/001-brainboxemb-meta/handoff.md) after reading `STATUS.md`.

A proposed migration may have its own handoff before activation so the intended work is clear, but its presence does not authorize implementation. Migration 002 is currently such a proposed/inactive plan.

## Repository layout

```text
brainboxemb.meta/
├── STATUS.md              human-readable current work / next work
├── docs/                  durable cross-project architecture and working model
├── repositories/          canonical public repository catalog and overview
├── domains/               domain-specific cross-project views
├── migrations/            active, proposed and completed cross-project migrations
├── experiments/           references to independent experiment/test repositories
├── dashboard/             dashboard implementation and dashboard-specific docs
├── .github/workflows/     repository-level automation
└── README.md
```

The dashboard is isolated under `dashboard/`; GitHub Actions workflows remain at root `.github/workflows/` because GitHub requires that location.

## Cross-project architecture and working model

Durable repository-spanning conventions live under [`docs/`](docs/README.md).

Current entry points include:

- [repository tooling boundaries](docs/architecture/repository-tooling.md) — `tool.git-project`, domain tooling, consumers and meta ownership;
- [generated output and publication](docs/working-model/generated-output.md) — source/generated separation, Moon/domain boundary and `dev`/`prod`/`rel` namespaces;
- [versioning and releases](docs/working-model/versioning-and-releases.md) — independent versions, exact locks and released cross-repository interfaces.

This documentation is intentionally current and compact. Detailed completed migration evidence is not copied wholesale from historical meta repositories.

## Repository catalog

[`repositories/catalog.yml`](repositories/catalog.yml) is the canonical inventory/classification source for public brainboxemb repositories.

The catalog owns stable information such as repository identity, category/domain, lifecycle where useful, role and project-infrastructure generation/provider. Live facts such as workflow health, open PRs, tags, branch protection and activity are read from GitHub instead of being copied into the catalog.

[`dashboard/dashboard.yml`](dashboard/dashboard.yml) contains dashboard policy and points to the central catalog. `dashboard/src/prepare_dashboard_config.py` converts it to the existing dashboard runtime shape so status, metrics and rendering keep one repository inventory.

See [repositories/README.md](repositories/README.md) for the catalog contract.

## Domain coordination

Domain-specific cross-project knowledge belongs under `domains/` when it remains useful at portfolio level.

For SCAD:

- the broad catalog/landscape responsibility formerly owned by `tech.scad` is now consolidated into [`repositories/catalog.yml`](repositories/catalog.yml) and [`domains/scad/`](domains/scad/);
- [`tech.scad`](https://github.com/brainboxemb/tech.scad) is retained as a superseded historical source until archival;
- Migration 001 Phase 5 is transferring the remaining current coordination responsibility from [`meta.scad-projects`](https://github.com/brainboxemb/meta.scad-projects) without copying obsolete plans wholesale.

## Cross-project migrations

See [migrations/README.md](migrations/README.md).

A migration has an explicit state. In particular, **proposed / inactive** means the plan is ready to understand and review but implementation must not start until it is deliberately activated.

Project-specific implementation plans stay in the owning project repository.

## Experiments

Experiments and test repositories stay independent. `brainboxemb.meta` records what question they tested, what decision they support and whether that result has been adopted. See [experiments/README.md](experiments/README.md).

## Dashboard

The static GitHub Actions/status dashboard is an active sub-capability under [`dashboard/`](dashboard/). It publishes through GitHub Pages while meta coordination work proceeds.

See [dashboard/README.md](dashboard/README.md) for dashboard-specific maintenance guidance.
