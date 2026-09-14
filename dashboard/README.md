# Dashboard

The GitHub Actions/status dashboard is an active sub-capability of `brainboxemb.meta`.

Its implementation is isolated under this directory. Portfolio-level coordination, repository classification and cross-project migration planning remain owned by the repository root and sibling meta directories.

The dashboard is generated as a static site and published with GitHub Pages. It has no server, database, Azure dependency or frontend framework.

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

Repository membership and stable classification live in the canonical public catalog:

```text
../repositories/catalog.yml
```

Dashboard-specific policy lives in:

```text
dashboard.yml
```

The dashboard config points to the central catalog with:

```yaml
catalog: ../repositories/catalog.yml
```

`src/prepare_dashboard_config.py` converts that catalog plus dashboard policy into the existing runtime contract:

```text
.dashboard.runtime.yml
```

The runtime file is generated and ignored by Git. This keeps the proven collector, metrics and renderer contracts unchanged while avoiding a second repository inventory.

The catalog owns stable facts such as domain/category, lifecycle, role and project-infrastructure generation/provider. Live workflow, PR, tag, branch-protection and activity state comes directly from GitHub.

## Dashboard-specific overrides

A catalog entry may contain an optional `dashboard` mapping for existing collector overrides, for example:

```yaml
- repository: brainboxemb/example
  category: project
  domain: software
  dashboard_group: Software projects
  dashboard:
    branch: develop
    include_workflows:
      - build.yml
```

Do not add a second repository inventory to `dashboard.yml`.

## Implementation layout

```text
dashboard/
├── AGENTS.md
├── README.md
├── dashboard.yml
├── requirements.txt
├── src/
│   ├── prepare_dashboard_config.py
│   ├── collect_action_metrics.py
│   ├── dashboard_entry.py
│   ├── configure_repository_settings.py
│   └── generate_dashboard.py
├── site/
│   ├── app.js
│   └── style.css
└── tests/
```

Repository-level workflows remain under `.github/workflows/` because GitHub only discovers Actions workflows there.

## Actions metrics

The dashboard derives performance metrics from GitHub workflow run history. Metrics are runtime/performance observations, not billing data.

Metrics deliberately refresh more slowly than current status: at most once per UTC day, cached for later dashboard runs that day. A catalog membership change can therefore appear in current dashboard status before its historical metrics join the next metrics refresh.

## GitHub Pages

`.github/workflows/deploy-dashboard.yml` runs dashboard commands with `dashboard/` as its working directory. It:

1. installs `requirements.txt` and runs unit tests;
2. builds `.dashboard.runtime.yml` from the canonical catalog;
3. restores or refreshes the daily metrics snapshot;
4. collects current GitHub status and generates `site/index.html`;
5. compares the dashboard-visible content hash with the deployed page;
6. publishes `dashboard/site/` through GitHub Pages only when visible state or daily metric values changed.

The scheduled run is best-effort. Manual **Rebuild dashboard** remains the fallback.

## Local development

From the repository root:

```powershell
cd dashboard
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

Open `dashboard/site/index.html` after generation when starting from the repository root, or `site/index.html` while inside `dashboard/`.

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

`Configure repository settings` changes only `delete_branch_on_merge`. It consumes the same generated runtime config and therefore the same central catalog.

Never print or persist secret token values.

## Releases

The permanent `.github/workflows/release.yml` workflow tags an exact already-verified commit. When workflow dispatch is unavailable, use the self-cleaning request form:

```text
release-request/vX.Y.Z/<40-character-release-sha>
```

Existing release tags are immutable.
