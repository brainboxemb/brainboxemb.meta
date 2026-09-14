# Migration 001 evidence

## Phase 1 — Meta foundation

Status: **qualified**

### Source change

- Pull request: `brainboxemb/brainboxemb.meta` #12 — Establish `brainboxemb.meta` migration foundation
- Qualified PR head: `061733fca1f4d2f347df87e351c5b82dc508ab8f`
- Main merge commit: `62df26489e84dedc9cbd11c7cdf7186e0b78261d`

### Main CI / Pages evidence

Deploy workflow run:

```text
34853241040
```

Run source revision:

```text
62df26489e84dedc9cbd11c7cdf7186e0b78261d
```

Observed successful steps in the build job:

- checkout;
- Python setup and dependency installation;
- dashboard unit tests;
- daily metrics-cache handling;
- dashboard generation;
- deployed-dashboard comparison;
- Pages configuration;
- Pages artifact upload.

The separate `deploy` job also completed successfully and published through GitHub Pages.

### Contract proven by Phase 1

The repository rename/foundation did not require moving the working dashboard runtime.

The following remain on their previously proven paths:

```text
dashboard.yml
requirements.txt
src/
site/
tests/
.github/workflows/deploy-dashboard.yml
```

At the same time:

- root README/AGENTS now establish the portfolio-level coordination role;
- migration planning/handoff conventions exist under `migrations/`;
- repository/domain/experiment destination boundaries exist;
- dashboard documentation and agent guidance are retained under `dashboard/`;
- dashboard self-identification uses `brainboxemb.meta`.

### Deferred, not blocked

The following were deliberately not required to qualify Phase 1:

- canonical catalog implementation;
- dashboard path relocation;
- `tech.scad` content migration;
- `meta.scad-projects` content or issue migration;
- broader dashboard redesign.

Those items remain separate migration phases so they cannot retroactively extend the Phase-1 blocking path.
