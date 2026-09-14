# Dashboard agent guidance

Persistent guidance for automated agents changing the dashboard sub-capability of `brainboxemb.meta`.

During Migration 001 Phases 1–2 the implementation remains at the historical repository-root paths. This file preserves the dashboard-specific rules while root `AGENTS.md` now owns portfolio-level coordination guidance.

## Dashboard purpose

The dashboard is the central static GitHub Actions/status dashboard for configured brainboxemb repositories.

The normal data flow is:

```text
dashboard.yml
    -> GitHub REST/GraphQL APIs
    -> Python collectors/generator
    -> site/index.html + static assets
    -> GitHub Pages
```

Keep it intentionally small: no application server, database, Azure service, or frontend framework unless the project direction is explicitly changed.

## Sources of truth

Use the owning systems as the authoritative source instead of duplicating changing operational state:

```text
dashboard.yml                    dashboard policy and transitional repository membership
GitHub repository metadata       repository/default-branch/settings state
GitHub active branch rules       enabled rulesets affecting a branch
GitHub classic branch protection classic protected-branch state
GitHub Actions API               workflow/run state and historical metrics
GitHub pull requests/branches    PR and cleanup state
src/generate_dashboard.py        rendering and generic current-status collection logic
src/dashboard_entry.py           brainboxemb-specific collection/status policy
src/collect_action_metrics.py    historical Actions metrics collection
site/app.js                      browser-side freshness/relative-time behaviour
.github/workflows/               scheduling/deployment/settings/release automation
```

Migration 001 Phase 2 will make `repositories/` the canonical public repository catalog. Until then, do not create another repository inventory alongside `dashboard.yml` and `tech.scad/catalog.yml`.

## Workflow status semantics

For normal workflows, status represents the most recent run on the repository's configured/default branch. Do not switch Build/Verify/etc. status to the latest run on any branch because feature or PR activity must not replace the main-line health signal.

`Release` is deliberately different. Releases use temporary `release-request/**` branches, so Release status uses the latest run regardless of branch.

Reusable-only workflows (`workflow_call` without a normal trigger) are hidden by default. GitHub's synthetic Pages workflow is displayed as `Pages`.

## Branch cleanup semantics

Branch cleanup is observational only. The dashboard must never delete branches automatically.

A non-default branch is a cleanup candidate when:

- its same-repository pull request is closed and the branch still exists; or
- the branch still exists and no same-repository pull request has ever used it.

Branches with an open PR are not cleanup candidates.

Long-lived generated/release branches are excluded by configuration. Treat patterns such as `rel/*` as patterns, not version-specific literals. Unrecognised orphan branches remain useful cleanup signals.

## Repository settings

The `PR auto-delete` status comes from GitHub's `delete_branch_on_merge` repository setting.

Resolve default-branch protection in this order:

1. GitHub's effective active branch rules;
2. classic branch protection using `DASHBOARD_ADMIN_TOKEN` when available;
3. normal branch resource as compatibility fallback.

A disabled/evaluate-only ruleset is not active protection. Preserve three-state reporting:

```text
true    -> enabled/protected
false   -> disabled/not protected
unknown -> unreadable/unknown
```

Never print, expose or persist secret token values.

## Actions metrics

Historical Actions metrics use the configured rolling window and refresh more slowly than current status:

- collect at most once per UTC day;
- cache the daily snapshot;
- reuse it on later runs that day;
- do not deploy Pages merely because collection was attempted;
- deploy when metric values or other visible state actually changed.

Metrics are runtime/performance observations, not billing data.

## Scheduling and freshness

The scheduled workflow is best-effort GitHub scheduling. Do not describe it as a guaranteed polling interval. Manual rebuild remains a fallback.

The browser does not query all monitored repositories; it only checks whether a newer deployed dashboard exists and reloads when appropriate.

## Change-aware Pages deployment

Keep data collection separate from publication. The content fingerprint intentionally excludes the generation timestamp. If visible state and daily metrics are unchanged, Pages deployment should be skipped.

If the currently deployed fingerprint cannot be read, allow deployment rather than assuming the page is current.

## Releases

Use the permanent `.github/workflows/release.yml` workflow. Release requests use:

```text
release-request/vX.Y.Z/<40-character-release-sha>
```

A release must tag an exact already-verified commit, require a matching changelog heading, never overwrite an existing tag, and clean up its request branch.

## Development and tests

When changing status semantics, cleanup rules, fingerprinting, settings handling or rendering, add/update focused tests under root `tests/` while the dashboard implementation remains root-located.

Run:

```text
python -m unittest discover -s tests -v
```

Keep `src/` standard-library-first where practical; PyYAML is the intentionally small external dependency.

Do not commit generated `site/action-metrics.json` or other transient cache/output files.

## Migration constraint

Do not move dashboard implementation paths as collateral work. Migration 001 Phase 3 owns that relocation and must qualify path changes, tests and Pages publication together.
