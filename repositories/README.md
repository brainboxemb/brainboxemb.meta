# Public repository catalog

`repositories/catalog.yml` is the canonical catalog of public `brainboxemb` repositories.

It owns stable classification and intent. Live operational state remains sourced from GitHub.

## What belongs in the catalog

Use the catalog for information such as:

```text
repository identity
category
domain
lifecycle where meaningful
high-level role
dashboard grouping
project-infrastructure generation/provider
engine metadata where already established
```

Do **not** copy changing GitHub state into the catalog:

```text
workflow status
open pull requests
latest tag
branch protection
branch cleanup candidates
recent activity
```

The dashboard reads those values directly from GitHub.

## Dashboard integration

`dashboard/dashboard.yml` contains dashboard policy and points to the central catalog with a path relative to the dashboard subproject:

```yaml
catalog: ../repositories/catalog.yml
```

`dashboard/src/prepare_dashboard_config.py` translates catalog membership/grouping into the existing dashboard `groups[].repositories` runtime shape. This deliberately keeps the proven status collector, metrics code and renderer unchanged.

The generated runtime file is `dashboard/.dashboard.runtime.yml` and is not committed.

## Coverage

The catalog is public-repository-only. Phase 2 was built from the current GitHub public repository inventory and the established SCAD classification in `tech.scad/catalog.yml`.

Older SCAD projects remain explicit as:

```yaml
project_infrastructure:
  generation: classic
```

where that classification was already established. Current consumers use `generation: current` with the relevant tooling provider.

`tool.sw-docs` is not a separate current repository: that earlier name was broadened to `tool.eng-docs`, which is the catalog entry to use.

## Adding or changing a repository

Update `repositories/catalog.yml`. Do not add the repository a second time to dashboard configuration.

For dashboard-specific overrides, use the optional per-entry `dashboard` mapping. Supported overrides are intentionally limited to the existing dashboard contract, such as branch/workflow filtering and cleanup exclusions.

After a catalog change, normal dashboard CI builds `dashboard/.dashboard.runtime.yml`, runs the existing collectors and publishes Pages only when dashboard-visible state changed.
