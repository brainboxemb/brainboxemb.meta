# Meta development manual

This page explains how to develop and maintain `brainboxemb.meta` itself.

## Start here

Before editing:

1. read [../AGENTS.md](../AGENTS.md);
2. read [10-00-plan.md](10-00-plan.md);
3. check [../STATUS.md](../STATUS.md) for repository-spanning work;
4. load only the relevant manual/design/domain authority.

## Ownership rule

Meta owns portfolio-level coordination and shared conventions. It does not absorb
implementation merely because a problem was discovered during coordination.

Typical ownership:

- generic repository behavior → `tool.git-project`;
- domain tooling → the relevant tool repository;
- reusable behavior/API → the owning library;
- product behavior → the project repository;
- portfolio convention/coordination → this repository.

## Normal change flow

Follow [20-11 — Git workflow](20-11-git-workflow.md).

For shared-convention changes:

1. state the durable rule in meta;
2. dogfood it here where applicable;
3. specialize it in domains only where the domain genuinely differs;
4. roll implementation changes through owner repositories;
5. retain qualification evidence in the appropriate owner/migration record.

## Catalog and dashboard

`repositories/catalog.yml` is the machine-readable public inventory.

When catalog metadata changes, keep the readable repository overview and
dashboard behavior coherent.

Read [../dashboard/AGENTS.md](../dashboard/AGENTS.md) before changing dashboard
implementation.

## Documentation

Use the numbered model in
[20-13 — Repository documentation](20-13-repository-documentation.md).

Domain-specific material remains under `domains/`. Migrations and experiments
remain operational/historical registers rather than being folded into the
general documentation book.
