# SCAD domain

`domains/scad/` is the portfolio-level knowledge and navigation layer for the public SCAD/CAD ecosystem.

The canonical repository inventory is **not** duplicated here. Repository membership and stable classification live in [`../../repositories/catalog.yml`](../../repositories/catalog.yml); live status comes from GitHub and the dashboard.

## Scope

The SCAD landscape includes:

- generic repository/bootstrap tooling used by SCAD projects;
- SCAD-specific project/build tooling;
- shared OpenSCAD/PythonSCAD runtime infrastructure;
- reference consumers/templates;
- reusable `lib.scad.*` libraries;
- current structured CAD projects;
- classic CAD projects that still use earlier infrastructure.

See [architecture.md](architecture.md) for the durable architecture and migration-scope rules.

## Broad landscape versus controlled integration

Keep these two views distinct:

```text
repositories/catalog.yml + domains/scad/
    broad portfolio view
    includes current and classic SCAD/CAD repositories

controlled SCAD integration set
    smaller set used to evolve and qualify the current shared SCAD stack
```

The controlled integration set and its current qualification/migration plans are being migrated from [`meta.scad-projects`](https://github.com/brainboxemb/meta.scad-projects) in Migration 001 Phase 5. Until that phase is complete, `meta.scad-projects` remains authoritative for those active integration plans/evidence.

## Source-of-truth boundaries

`brainboxemb.meta` owns:

- the public repository catalog and stable classification;
- portfolio-level SCAD architecture and navigation;
- cross-project migration coordination once migrated here.

Individual repositories own:

- source code and CAD geometry;
- project configuration and actual dependency versions;
- releases/tags;
- tests, verification and generated evidence;
- project-specific design documentation and implementation status.

A normal project must depend directly on the tooling/libraries it needs. `brainboxemb.meta` and the former `tech.scad` catalog are information layers, not runtime dependencies.

## Historical source

[`tech.scad`](https://github.com/brainboxemb/tech.scad) established the broad SCAD catalog, project-infrastructure generation classification and architecture rules that were consolidated here. Its static tooling/library/project indexes are retained in repository history rather than copied into a second maintained list.
