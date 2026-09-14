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

Current rule: do not turn useful discoveries into migration blockers automatically. Classify them as:

```text
migration blocker
follow-up migration
backlog / improvement
```

Only the first category extends the blocking path.

## Continue cross-project work

Use [the migration handoff](migrations/001-brainboxemb-meta/handoff.md) while the consolidation is active. It tells a new session to reconstruct state from repositories, issues/PRs, CI/evidence and generated output rather than from old chat history.

After consolidation, the root handoff becomes the generic entry point for new cross-project work.

## Repository layout

```text
brainboxemb.meta/
├── docs/                  shared architecture and working conventions
├── repositories/          canonical public repository catalog and overview
├── domains/               domain-specific views, for example SCAD
├── migrations/            cross-project migration plans, handoffs and evidence
├── experiments/           references to independent experiment/test repositories
├── dashboard/             dashboard documentation and, later, implementation
├── .github/workflows/     repository automation
└── README.md
```

### Transitional dashboard layout

The working dashboard implementation deliberately remains at its historical root paths until its dedicated relocation phase:

```text
dashboard.yml
src/
site/
tests/
requirements.txt
.github/workflows/deploy-dashboard.yml
```

This avoids coupling the meta/catalog migration to a Pages/workflow relocation. See [dashboard/README.md](dashboard/README.md).

## Repository catalog

[`repositories/catalog.yml`](repositories/catalog.yml) is the canonical inventory/classification source for public brainboxemb repositories.

The catalog owns stable information such as repository identity, category/domain, lifecycle where useful, role and project-infrastructure generation/provider. It currently includes the full public repository set used by this migration, including current tools/reference consumers, classic SCAD projects, sites and experiment repositories.

Live facts such as workflow health, open PRs, tags, branch protection and activity are still read from GitHub instead of being copied into the catalog.

Root `dashboard.yml` now contains dashboard policy and points to the canonical catalog. `src/prepare_dashboard_config.py` converts it to the existing dashboard runtime shape, so the proven status/metrics/rendering code does not need a second repository inventory.

See [repositories/README.md](repositories/README.md) for the catalog contract.

## Domain coordination

Domain-specific cross-project knowledge belongs under `domains/` when it remains useful after consolidation.

The SCAD domain is currently being migrated from:

- `brainboxemb/meta.scad-projects` — SCAD architecture, workflow and cross-project plans;
- `brainboxemb/tech.scad` — broader SCAD catalog and landscape documentation.

Those repositories remain authoritative for responsibilities not yet migrated and are not archived until active responsibilities, links and evidence are covered here.

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

The existing static GitHub Actions/status dashboard remains an active sub-capability and continues to publish through GitHub Pages while the broader meta structure is introduced.

See [dashboard/README.md](dashboard/README.md) for dashboard-specific maintenance guidance.
