# Public repository catalog

This directory is the target home for the canonical catalog of public `brainboxemb` repositories.

## Current state

The final catalog is **not yet authoritative**. It is intentionally deferred to Migration 001 Phase 2 so the repository rename/foundation does not become a simultaneous data-model and dashboard migration.

Current inputs that must be reconciled in Phase 2:

- `brainboxemb/tech.scad` → `catalog.yml` for the broad SCAD landscape and current/classic infrastructure classification;
- root `dashboard.yml` for the wider set of repositories monitored by the status dashboard.

## Intended catalog ownership

The catalog should contain stable classification/intent, for example:

```text
repository identity
category
domain
lifecycle / infrastructure generation
high-level role
provider / ownership relationships where useful
```

Changing operational state should come from GitHub instead of being copied into YAML:

```text
workflow status
open PR count
latest tag
branch protection
branch cleanup candidates
recent activity
```

The dashboard will consume the canonical catalog after Phase 2 is qualified.
