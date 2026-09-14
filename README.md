# brainboxemb.meta

Central coordination, architecture, repository catalog, migration planning, and status overview for public brainboxemb projects and tooling.

## Purpose

`brainboxemb.meta` is the portfolio-level coordination repository for the public `brainboxemb` repositories.

It owns information that is intentionally broader than one implementation repository:

- the canonical public repository catalog and high-level lifecycle/classification;
- cross-project architecture and ownership boundaries;
- shared working conventions such as branches, generated output, pull requests and releases;
- current cross-project migrations, their evidence and ChatGPT handoffs;
- domain views such as the SCAD ecosystem;
- references to experiments that justify cross-project technical decisions;
- the GitHub Actions/status dashboard.

Individual repositories remain authoritative for their own implementation, project-specific plans, releases, local documentation and local issues.

This repository covers **public repositories only**. Private-project coordination belongs in an explicitly separate scope.

## Current migration

This repository was renamed from `brainboxemb.dashboard` and is being expanded into the broader meta role in small, independently reviewable phases.

The migration is tracked by [issue #11](https://github.com/brainboxemb/brainboxemb.meta/issues/11) and [the migration plan](migrations/001-brainboxemb-meta/README.md).

Do not turn useful discoveries into migration blockers automatically. Classify them as:

```text
migration blocker
follow-up migration
backlog / improvement
```

Only the first category extends the blocking path.

## Continue cross-project work

Use [the migration handoff](migrations/001-brainboxemb-meta/handoff.md) while the consolidation is active. Reconstruct state from repositories, issues/PRs, CI/evidence and generated output rather than old chat history.

## Repository layout

```text
brainboxemb.meta/
├── docs/                  shared architecture and working conventions
├── repositories/          canonical public repository catalog and overview
├── domains/               domain-specific views, for example SCAD
├── migrations/            cross-project migration plans, handoffs and evidence
├── experiments/           references to independent experiment/test repositories
├── dashboard/             dashboard implementation and dashboard-specific docs
├── .github/workflows/     repository-level automation
└── README.md
```

The dashboard is isolated under `dashboard/`; GitHub Actions workflows remain at root `.github/workflows/` because GitHub requires that location.

## Repository catalog

[`repositories/catalog.yml`](repositories/catalog.yml) is the canonical inventory/classification source for public brainboxemb repositories.

The catalog owns stable information such as repository identity, category/domain, lifecycle where useful, role and project-infrastructure generation/provider. Live facts such as workflow health, open PRs, tags, branch protection and activity are read from GitHub instead of being copied into the catalog.

[`dashboard/dashboard.yml`](dashboard/dashboard.yml) contains dashboard policy and points to the central catalog. `dashboard/src/prepare_dashboard_config.py` converts it to the existing dashboard runtime shape so status, metrics and rendering keep one repository inventory.

See [repositories/README.md](repositories/README.md) for the catalog contract.

## Domain coordination

Domain-specific cross-project knowledge belongs under `domains/` when it remains useful at portfolio level.

For SCAD:

- the broad catalog/landscape responsibility formerly owned by `tech.scad` is now consolidated into [`repositories/catalog.yml`](repositories/catalog.yml) and [`domains/scad/`](domains/scad/);
- [`tech.scad`](https://github.com/brainboxemb/tech.scad) is retained as a superseded historical source until the final archival phase;
- [`meta.scad-projects`](https://github.com/brainboxemb/meta.scad-projects) still owns the current controlled SCAD integration plans/evidence that have not yet been reassessed and migrated.

Migration 001 Phase 5 explicitly reassesses `meta.scad-projects` before moving anything, so historical documents or useful-but-nonblocking improvements do not automatically enter the blocking path.

## Cross-project migrations

A cross-project migration belongs under `migrations/<migration>/` and should contain at least:

- a bounded goal and scope;
- owners and ownership boundaries;
- phases with prerequisites and stop criteria;
- explicit blocker / follow-up / backlog classification;
- evidence and completion criteria;
- a reusable ChatGPT handoff.

Project-specific implementation plans stay in the owning project repository.

## Experiments

Experiments and test repositories stay independent. `brainboxemb.meta` records what question they tested, what decision they support and whether that result has been adopted. See [experiments/README.md](experiments/README.md).

## Dashboard

The static GitHub Actions/status dashboard is an active sub-capability under [`dashboard/`](dashboard/). It publishes through GitHub Pages while the broader meta consolidation proceeds.

See [dashboard/README.md](dashboard/README.md) for dashboard-specific maintenance guidance.
