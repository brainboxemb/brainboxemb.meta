# Changelog

## Unreleased

- Rename the repository to `brainboxemb.meta` and establish it as the portfolio-level coordination source for public brainboxemb repositories.
- Add the phased `brainboxemb.meta` consolidation migration plan and reusable handoff.
- Add `repositories/catalog.yml` as the canonical inventory/classification source for public repositories and derive the dashboard runtime repository groups from it.
- Preserve stable SCAD current/classic project-infrastructure classification while expanding catalog coverage to the current public repository set.
- Move dashboard configuration, Python sources, static site files, tests and dependencies under `dashboard/` while keeping repository-level workflows under `.github/workflows/`.
- Update dashboard self-identification from `brainboxemb.dashboard` to `brainboxemb.meta`.
- Add `tool.eng-docs` to **Tooling**.
- Add `tool.git-project` to **Tooling**.
- Add `2026-010-02.java.event-timing-framework` to **Software projects**.
- Define shared changelog coverage for meaningful user-visible repository/resource changes, including non-functional documentation and presentation changes, while excluding trivial editorial noise.
- Activate Experiment 006 to qualify transitive SCAD library dependencies and `lib.scad.util` as a lightweight foundation dependency without sacrificing direct desktop OpenSCAD use.

## v0.2.0 - 2026-09-12

- Detect default-branch protection from active GitHub branch rules plus classic branch protection, using `DASHBOARD_ADMIN_TOKEN` for the Administration-read check when available.
- Stack the **Branch protected** and **PR auto-delete** table headers onto two lines so the settings columns remain compact.
- Add a permanent self-cleaning `Release` workflow using `release-request/vX.Y.Z/<sha>` branches for interfaces that cannot dispatch workflows directly.
- Split `lib.scad.clamps` and `lib.scad.hub75` into a dedicated **CAD libraries** group and rename **Tooling & libraries** to **Tooling**.
- Use compact `✓` / `✕` / `–` indicators for both default-branch protection and PR branch auto-delete status.
- Add `tool.java-project` to the **Tooling** dashboard group.
- Show whether each repository's default branch is protected, with protected, unprotected, or unknown status.
- Add a **Software projects** group and register `2026-010-01.meta.event-timing-software` as its first repository.
- Treat `rel/*` branches as persistent release output branches in **Branch cleanup**, while keeping temporary `chore/...`, `temp-release-...` and `release-request/...` branches visible for review.
- Show the most recent **Release** workflow run across all branches so short-lived `release-request/...` branches do not leave an older default-branch failure on the dashboard.
- Add 30-day Actions performance metrics from workflow run history, refreshed at most once per UTC day through a date-keyed cache; unchanged metrics do not force a Pages deployment.
- Include non-default branches that have never had a pull request in **Branch cleanup**, while ignoring configured long-lived publication/output branches.
- Keep `Last activity` relative through 99 days, show `>99d ago` beyond that, and show the exact date on hover without a time.
- Read PR branch auto-delete settings through GitHub GraphQL and show unknown instead of incorrectly reporting disabled when the setting cannot be read.
- Keep Actions cells as normal table cells so row separators align across all columns, and label the synthetic GitHub Pages workflow simply as `Pages`.
- Skip GitHub Pages deployment when the dashboard fingerprint is unchanged; scheduled data checks now run once per hour at minute 11.
- Clarify that the browser freshness check only checks for a newer deployed page, not live repository data.
- Auto-check every minute for a newly deployed dashboard and cache-bust static assets.
- Update relative activity timestamps live in the browser on the static dashboard.
- Show and manage the automatic deletion of merged pull-request branches per repository.
- Show branch cleanup candidates when closed pull request branches still exist.
- Hide reusable-only workflows that are invoked exclusively through `workflow_call`.
- Show open pull request counts per repository with links to the PR list.
- Show the dashboard refresh timestamp at the top in browser-local time.
- Add a shortcut to manually run the dashboard workflow.
- Group repositories without active Actions in a separate section at the bottom.
- Show configured repositories even when they have no active workflows.
- Show the latest Git tag for each monitored repository.

## v0.1.0 - 2026-09-09

- Initial static GitHub Actions dashboard.
- Repository grouping through `dashboard.yml`.
- Automatic workflow discovery.
- Default-branch run status.
- GitHub Pages deployment.
- Search and problems-only filter.
- Responsive light/dark styling.
- Unit tests for status mapping and rendering.
