# Dashboard agent guidance

Persistent guidance for automated agents changing the dashboard sub-capability of `brainboxemb.meta`.

The dashboard implementation lives under `dashboard/`. Root `AGENTS.md` owns portfolio-level coordination guidance.

## Dashboard purpose

The dashboard is the static GitHub Actions/status overview for configured public brainboxemb repositories.

The normal data flow is:

```text
../repositories/catalog.yml
        +
 dashboard.yml
        ↓
 .dashboard.runtime.yml
        ↓
 GitHub REST/GraphQL APIs
        ↓
 src/ collectors/generator
        ↓
 site/index.html + static assets
        ↓
 GitHub Pages
```

Keep it intentionally small: no application server, database or frontend framework unless the project direction explicitly changes.

## Sources of truth

```text
../repositories/catalog.yml        canonical public repository inventory/classification
dashboard.yml                       dashboard policy and catalog reference
GitHub repository metadata          repository/default-branch/settings state
GitHub active branch rules          enabled rulesets affecting a branch
GitHub classic branch protection    classic protected-branch state
GitHub Actions API                  workflow/run state and historical metrics
GitHub pull requests/branches       PR and cleanup state
src/generate_dashboard.py           rendering and generic current-status collection
src/dashboard_entry.py              brainboxemb-specific collection/status policy
src/collect_action_metrics.py       historical Actions metrics collection
site/app.js                         browser-side freshness/relative-time behaviour
../.github/workflows/               scheduling/deployment/settings/release automation
```

Do not create a second repository inventory inside the dashboard.

## Workflow status semantics

For normal workflows, status represents the most recent run on the repository's configured/default branch. Feature or PR activity must not replace the main-line health signal.

`Release` is deliberately different because releases can use temporary `release-request/**` branches; Release status uses the latest run regardless of branch.

Reusable-only workflows are hidden by default. GitHub's synthetic Pages workflow is displayed as `Pages`.

## Branch cleanup semantics

Branch cleanup is observational only. The dashboard must never delete branches automatically.

A non-default branch is a cleanup candidate when its same-repository pull request is closed and the branch still exists, or when the branch exists and no same-repository pull request has ever used it. Branches with an open PR are not cleanup candidates.

Long-lived generated/release branches are excluded by configuration. Treat patterns such as `rel/*` as patterns.

## Repository settings

The `PR auto-delete` status comes from GitHub's `delete_branch_on_merge` repository setting.

Resolve default-branch protection in this order:

1. GitHub's effective active branch rules;
2. classic branch protection using `DASHBOARD_ADMIN_TOKEN` when available;
3. normal branch resource as compatibility fallback.

Preserve three-state reporting:

```text
true    -> enabled/protected
false   -> disabled/not protected
unknown -> unreadable/unknown
```

Never print, expose or persist secret token values.

## Actions metrics

Historical Actions metrics refresh more slowly than current status:

- collect at most once per UTC day;
- cache the daily snapshot;
- reuse it on later runs that day;
- deploy only when metric values or other visible state changed.

Metrics are runtime/performance observations, not billing data.

## Scheduling and freshness

The scheduled workflow is best-effort GitHub scheduling. Manual rebuild remains a fallback.

The browser does not query every monitored repository; it checks whether a newer deployed dashboard exists and reloads when appropriate.

## Change-aware Pages deployment

Keep data collection separate from publication. The content fingerprint intentionally excludes generation time. If visible state and daily metrics are unchanged, Pages deployment should be skipped.

If the currently deployed fingerprint cannot be read, allow deployment rather than assuming the page is current.

## Development and tests

Run dashboard commands from `dashboard/`:

```text
pip install -r requirements.txt
python src/prepare_dashboard_config.py --config dashboard.yml --output .dashboard.runtime.yml
python -m unittest discover -s tests -v
```

When changing status semantics, cleanup rules, fingerprinting, settings handling or rendering, add or update focused tests under `dashboard/tests/`.

Keep `src/` standard-library-first where practical; PyYAML is the intentionally small external dependency.

Do not commit generated `site/action-metrics.json`, `.dashboard.runtime.yml`, content hashes or other transient cache/output files.

## Releases

Use the permanent root `.github/workflows/release.yml` workflow. Release requests use:

```text
release-request/vX.Y.Z/<40-character-release-sha>
```

A release must tag an exact already-verified commit, require a matching changelog heading, never overwrite an existing tag and clean up its request branch.
