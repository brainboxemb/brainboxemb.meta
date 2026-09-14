# Migration 001 evidence

## Phase 1 — Meta foundation

Status: **qualified**

### Source change

- PR #12 — Establish `brainboxemb.meta` migration foundation
- Qualified PR head: `061733fca1f4d2f347df87e351c5b82dc508ab8f`
- Main merge commit: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`

### Main CI / Pages evidence

- Deploy run: `34853241040`
- Source revision: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`
- dashboard tests: success
- dashboard generation: success
- Pages artifact: success
- Pages deployment: success

Phase 1 established the portfolio-level meta identity and migration structure without coupling the rename to catalog or dashboard-path changes.

## Phase 2 — Canonical public repository catalog

Status: **qualified**

### Source change

- PR #14 — Introduce canonical public repository catalog
- Qualified PR head: `dbaee6d6e87cbe7bd82e80ae793d783d3fefd38b`
- Main merge commit: `7a8ad3974bf9b3e43ce0744825d124595ae894e2`

### Main CI / Pages evidence

- Deploy run: `34855023365`
- Source revision: `7a8ad3974bf9b3e43ce0744825d124595ae894e2`
- 28 unit tests: success
- catalog runtime preparation: `29 repositories in 6 groups`
- dashboard generation: 29 repositories rendered successfully
- Pages artifact: success
- Pages deployment: success

### Contract proven

- `repositories/catalog.yml` is the single public repository membership/classification source;
- stable SCAD current/classic infrastructure metadata was retained;
- `dashboard.yml` no longer owns a duplicate repository list;
- dashboard/metrics/settings reuse the existing runtime `groups[].repositories` contract through a thin catalog adapter;
- status collectors and renderer semantics did not need redesign.

## Phase 3 — Dashboard subproject relocation

Status: **qualified**

### Source change

- PR #15 — Move dashboard implementation under dashboard
- Qualified PR head: `caeea117650b43242422ad7d0c0787a8cc083ab8`
- Main merge commit: `fa1a2157f0ad39d3a64efa1fe02bcb614b281343`

The implementation files were Git renames; dashboard collector, metrics, renderer and test logic were unchanged.

### Main CI / Pages evidence

- Deploy run: `34856871791`
- Source revision: `fa1a2157f0ad39d3a64efa1fe02bcb614b281343`
- dependency install from `dashboard/requirements.txt`: success
- 28 unit tests from `dashboard/tests/`: success
- runtime config generation from `dashboard/dashboard.yml`: success
- runtime config reported `29 repositories in 6 groups`
- first metrics refresh on the relocated cache path: success
- metrics snapshot: `4179 runs across 29 repositories`
- dashboard generation from the relocated subproject: success
- generated dashboard: 29 repositories
- Pages artifact source: `dashboard/site`
- Pages artifact upload: success
- Pages deployment: success

### Contract proven

The dashboard is now isolated under:

```text
dashboard/
    dashboard.yml
    requirements.txt
    src/
    site/
    tests/
    README.md
    AGENTS.md
```

Repository-level workflows remain under `.github/workflows/` and run dashboard commands with `dashboard/` as their working directory.

The central catalog remains outside the dashboard subproject and resolves through `../repositories/catalog.yml`.

## Deferred from Phases 1–3

The following remain separate migration responsibilities rather than retroactive blockers:

- durable `tech.scad` domain-knowledge migration;
- durable `meta.scad-projects` architecture/working-plan migration;
- still-active cross-project issue migration;
- archival of superseded source repositories;
- unrelated dashboard redesign or feature work.
