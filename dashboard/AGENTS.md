# Dashboard agent guidance

Instructions for automated agents changing the dashboard subproject.

Read [`README.md`](README.md) for the human-readable dashboard explanation. Root [`../AGENTS.md`](../AGENTS.md) contains the repository-wide maintenance rules.

## Scope

The dashboard is a static status overview for the public repositories listed in `../repositories/catalog.yml`.

Do not create another repository inventory in dashboard configuration. `dashboard.yml` contains dashboard policy; repository membership comes from the central catalog.

## Behaviour that must be preserved

- Normal workflow health is based on the configured/default branch.
- Release workflow status may use temporary `release-request/**` branches.
- Reusable-only workflows stay hidden unless they are also directly runnable.
- Branch cleanup is **observational only**; the dashboard must never delete branches.
- Generated/release branches excluded by configuration must stay out of cleanup candidates.
- Branch protection reporting must preserve `true`, `false` and `unknown` rather than treating unreadable state as disabled.
- Secret token values must never be printed or persisted.
- Historical Actions metrics refresh at most once per UTC day and are not billing data.
- Pages deployment stays change-aware: unchanged visible state should not force a deployment.

## Development

Run dashboard commands from `dashboard/`:

```text
pip install -r requirements.txt
python src/prepare_dashboard_config.py --config dashboard.yml --output .dashboard.runtime.yml
python -m unittest discover -s tests -v
```

When changing status rules, cleanup logic, repository settings, metrics, rendering or content hashing, update focused tests under `tests/`.

Do not commit transient files such as `.dashboard.runtime.yml`, `site/action-metrics.json` or generated content hashes.

## Repository settings and workflows

Repository-level GitHub Actions stay under `../.github/workflows/` because GitHub requires that location.

The dashboard may read repository settings and status but should not silently change repositories during normal status collection. Explicit repository-settings workflows are separate actions.

## Releases

Use the root `.github/workflows/release.yml` process. A release must target an exact already-verified commit and must not overwrite an existing tag.
