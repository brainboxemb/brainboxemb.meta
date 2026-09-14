# Dashboard

The GitHub Actions/status dashboard is an active sub-capability of `brainboxemb.meta`.

> **Migration note:** the repository was renamed from `brainboxemb.dashboard`. During Migration 001 the working dashboard implementation intentionally remains at the repository root (`dashboard.yml`, `src/`, `site/`, `tests/`). Its filesystem move is a later isolated phase so Pages/workflow relocation is not mixed into catalog/coordination changes.

The dashboard is generated as a static site and published with GitHub Pages. It has no server, database, Azure dependency, or JavaScript framework.

## What it shows

- repositories grouped by purpose;
- active GitHub Actions workflows discovered automatically;
- reusable-only workflows hidden automatically;
- status of the most recent run on each repository's default branch;
- latest Git tag and open pull-request count;
- default-branch protection and PR-branch auto-delete state;
- branch-cleanup candidates;
- daily GitHub Actions performance metrics over a configurable rolling window;
- last activity, search, problems-only filtering, and responsive light/dark styling.

Repositories without active workflows remain visible in a separate section unless configuration says otherwise. Branch cleanup is observational only; the dashboard never deletes branches.

## Repository catalog and dashboard policy

Repository membership/classification lives in the canonical public catalog:

```text
repositories/catalog.yml
```

Root `dashboard.yml` now owns only dashboard policy, labels and the catalog reference:

```yaml
catalog: repositories/catalog.yml
```

`src/prepare_dashboard_config.py` converts the canonical catalog into the existing dashboard runtime structure. The generated file is:

```text
.dashboard.runtime.yml
```

and is intentionally ignored by Git.

This keeps the existing collector, metrics and renderer contracts unchanged while removing the duplicate repository list from `dashboard.yml`.

The catalog contains stable portfolio information such as domain/category, lifecycle, role and project-infrastructure generation/provider. Live workflow/PR/tag/protection/activity state still comes directly from GitHub.

## Dashboard-specific overrides

A catalog entry may contain an optional `dashboard` mapping for the small set of existing collector overrides, for example:

```yaml
- repository: brainboxemb/example
  category: project
  domain: software
  dashboard_group: Software projects
  dashboard:
    branch: develop
    include_workflows:
      - build.yml
    workflow_labels:
      build: Build
```

Supported overrides intentionally mirror the existing dashboard contract: branch, workflow include/exclude/labels, reusable-workflow visibility and branch-cleanup exclusions.

Do not add a second repository inventory to `dashboard.yml`.

## Actions metrics

The dashboard derives performance metrics from GitHub workflow run history. Metrics are runtime/performance observations, not billing data.

Metrics deliberately refresh more slowly than current status: at most once per UTC day, cached for later dashboard runs that day. A catalog membership change can therefore appear in current dashboard status before its historical metrics join the next metrics refresh. That existing cadence is not used as a reason to duplicate or delay catalog membership.

## GitHub Pages

`.github/workflows/deploy-dashboard.yml`:

1. checks out the repository;
2. installs dependencies and runs unit tests;
3. builds `.dashboard.runtime.yml` from the canonical catalog;
4. restores or refreshes the daily metrics snapshot;
5. collects current GitHub status and generates `site/index.html`;
6. compares the dashboard-visible content hash with the deployed page;
7. publishes Pages only when visible state or daily metric values changed.

The scheduled run is best-effort. Manual **Rebuild dashboard** remains the fallback.

## Local development

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GITHUB_TOKEN = "..."   # optional; useful for API rate limits

python src/prepare_dashboard_config.py `
  --config dashboard.yml `
  --output .dashboard.runtime.yml

python src/collect_action_metrics.py `
  --config .dashboard.runtime.yml `
  --output site/action-metrics.json

python src/dashboard_entry.py `
  --config .dashboard.runtime.yml `
  --output site/index.html

python -m unittest discover -s tests -v
```

Open `site/index.html` after generation.

## Current implementation structure

```text
.
├── .github/workflows/deploy-dashboard.yml
├── .github/workflows/configure-repositories.yml
├── dashboard.yml
├── repositories/catalog.yml
├── requirements.txt
├── src/
│   ├── prepare_dashboard_config.py
│   ├── collect_action_metrics.py
│   ├── dashboard_entry.py
│   ├── configure_repository_settings.py
│   └── generate_dashboard.py
├── site/
└── tests/
```

Migration 001 Phase 3 owns any future relocation of these runtime files under `dashboard/`; that move must qualify path changes, tests and Pages publication together.

## Branch cleanup

A non-default branch is a cleanup candidate when its same-repository pull request is closed and the branch still exists, or when the branch still exists and no same-repository pull request has ever used it. Branches with an open PR are not candidates.

Configured long-lived generated branches such as `build`, `verification`, `dev/*`, `prod/*`, `rel/*` and `gh-pages` are excluded. Treat `rel/*` as a pattern.

## Repository settings

The dashboard preserves three-state reporting for repository settings:

```text
true    -> enabled/protected
false   -> disabled/not protected
unknown -> unreadable/unknown
```

Default-branch protection is resolved from effective active branch rules, classic protection when Administration-read access is available, and the normal branch resource as compatibility fallback.

`Configure repository settings` can change only `delete_branch_on_merge`. It now builds the same runtime config from `repositories/catalog.yml`, so catalog membership is also the repository set used by the settings workflow.

Never print or persist secret token values.

## Releases

The permanent `.github/workflows/release.yml` workflow tags an exact already-verified commit. When workflow dispatch is unavailable, use the self-cleaning request form:

```text
release-request/vX.Y.Z/<40-character-release-sha>
```

Existing release tags are immutable.
