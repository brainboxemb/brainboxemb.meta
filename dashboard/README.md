# Dashboard

The GitHub Actions/status dashboard is an active sub-capability of `brainboxemb.meta`.

## Migration state

The repository was originally `brainboxemb.dashboard`. During the initial meta consolidation the dashboard runtime deliberately remains at the repository root so the rename does not become a simultaneous Pages/workflow relocation.

Current implementation paths:

```text
dashboard.yml
requirements.txt
src/
site/
tests/
.github/workflows/deploy-dashboard.yml
.github/workflows/configure-repositories.yml
```

A later dedicated migration phase will move these under `dashboard/` only after the path changes, unit tests and GitHub Pages publication can be qualified together.

## What it shows

The static dashboard provides a public overview of configured repositories, including active workflow status, latest tag, open pull requests, branch-cleanup candidates, branch auto-delete/protection state, recent activity and Actions performance metrics.

Repositories without active workflows remain visible. Reusable-only workflows are hidden by default. Normal workflow health is based on the configured/default branch; release workflows are treated specially because release requests use temporary branches.

Branch cleanup is observational only. The dashboard never deletes branches automatically.

## Configuration

Until the canonical `repositories/catalog.yml` migration is complete, dashboard membership/grouping remains configured in root [`dashboard.yml`](../dashboard.yml).

Phase 2 of the meta migration will introduce one canonical public repository catalog and adapt the dashboard to consume it. Do not create another duplicate catalog meanwhile.

## Local development

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GITHUB_TOKEN = "..."   # optional; useful for API rate limits
python src/collect_action_metrics.py --config dashboard.yml --output site/action-metrics.json
python src/generate_dashboard.py
python -m unittest discover -s tests -v
```

Open `site/index.html` after generation.

## GitHub Pages

`.github/workflows/deploy-dashboard.yml` collects current data and publishes `site/` through GitHub Pages. Deployment is change-aware: unchanged dashboard-visible state does not cause a new Pages deployment merely because a scheduled run happened.

The scheduled run is best-effort. Manual workflow dispatch remains the fallback.

## Security

Read-only/private-repository access and Administration checks use repository secrets when configured. Never place token values in configuration, logs, generated pages, fixtures or documentation.
