# Migration 001 evidence

## Phase 1 — Meta foundation

Status: **qualified**

- PR #12 — Establish `brainboxemb.meta` migration foundation
- Qualified PR head: `061733fca1f4d2f347df87e351c5b82dc508ab8f`
- Main merge commit: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`
- Deploy run: `34853241040`
- dashboard tests, generation, Pages artifact and Pages deployment: success

## Phase 2 — Canonical public repository catalog

Status: **qualified**

- PR #14 — Introduce canonical public repository catalog
- Qualified PR head: `dbaee6d6e87cbe7bd82e80ae793d783d3fefd38b`
- Main merge commit: `7a8ad3974bf9b3e43ce0744825d124595ae894e2`
- Deploy run: `34855023365`
- 28 unit tests: success
- catalog runtime preparation: `29 repositories in 6 groups`
- dashboard generation: 29 repositories
- Pages artifact/deployment: success

Contract proven:

- one public repository membership/classification source;
- stable SCAD current/classic metadata retained;
- dashboard/metrics/settings reuse the existing runtime contract through a thin catalog adapter;
- no dashboard status/renderer redesign required.

## Phase 3 — Dashboard subproject relocation

Status: **qualified**

- PR #15 — Move dashboard implementation under dashboard
- Qualified PR head: `caeea117650b43242422ad7d0c0787a8cc083ab8`
- Main merge commit: `fa1a2157f0ad39d3a64efa1fe02bcb614b281343`
- Deploy run: `34856871791`
- 28 relocated unit tests: success
- runtime config: `29 repositories in 6 groups`
- first metrics refresh on relocated path: `4179 runs across 29 repositories`
- generated dashboard: 29 repositories
- Pages artifact source: `dashboard/site`
- Pages artifact/deployment: success

Contract proven:

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

Repository-level workflows remain in `.github/workflows/`; central catalog resolves from the dashboard through `../repositories/catalog.yml`.

## Phase 4 — tech.scad integration

Status: **qualified**

### Reassessment

`tech.scad` had no open issues. Phase 2 had already migrated the broad machine-readable repository classification into `brainboxemb.meta/repositories/catalog.yml`.

Copying its static tooling/library/project indexes would have recreated a second hand-maintained repository inventory, so those tables were intentionally left as historical content.

### Destination evidence

`brainboxemb.meta` PR #16 — Integrate durable `tech.scad` domain knowledge:

- qualified head: `b5e9e169b4ba27228aa564600c1c32c1d3501837`;
- merge commit: `7ca593b76a26ac05861b86604fcb6f25baeac5fa`.

Durable knowledge now lives under `domains/scad/` and covers:

- broad landscape versus controlled integration view;
- classic standalone, classic shared-actions and current infrastructure generations;
- engine classification separate from infrastructure generation;
- evidence-based engine classification rather than name inference;
- direct project dependency boundaries;
- current-generation migration-scope rule;
- portfolio versus repository source-of-truth boundaries.

### Source redirect evidence

`tech.scad` PR #2 — Point `tech.scad` to `brainboxemb.meta`:

- qualified head: `50d89c4182e967fd8e1c84e1a56f98015daa8af3`;
- merge commit: `b04e539a2215efa3b38fe1aa5a4d657fe4a89ae1`.

Its README/AGENTS now state that:

- `brainboxemb.meta` owns the current catalog and SCAD portfolio knowledge;
- existing `catalog.yml`, architecture and indexes are historical evidence;
- new membership/classification must not be added there;
- the repository is not yet archived.

### Closeout state

The central catalog marks `brainboxemb/tech.scad` as:

```yaml
lifecycle: superseded
```

The repository remains visible and unarchived until the final source-closeout phase. This preserves links, Git history and old evidence without retaining duplicate current ownership.

## Deferred beyond Phase 4

The following remain separate responsibilities and do not retroactively block qualified phases:

- reassessment/migration of current `meta.scad-projects` responsibilities;
- still-active cross-project issues/plans that survive that reassessment;
- formal GitHub archival of superseded sources;
- unrelated SCAD tooling improvements;
- unrelated dashboard feature work.
