# SCAD domain

`domains/scad/` is the public portfolio-level knowledge and navigation layer for the SCAD/CAD repositories.

Repository membership and stable classification live in [`../../repositories/catalog.yml`](../../repositories/catalog.yml); live operational state comes from GitHub and the dashboard.

## What belongs here

The SCAD landscape includes:

- generic repository/bootstrap tooling used by SCAD projects;
- SCAD-specific project/build tooling;
- shared OpenSCAD/PythonSCAD runtime infrastructure;
- templates and reference consumers;
- reusable `lib.scad.*` libraries;
- current structured CAD projects;
- classic CAD projects that still use earlier infrastructure.

See [architecture.md](architecture.md) for the durable architecture and migration-scope rules.

## Two useful views

The portfolio deliberately keeps two different views without maintaining two separate catalog repositories:

```text
broad portfolio view
    repositories/catalog.yml + domains/scad/
    all relevant public current/classic SCAD/CAD repositories

controlled integration view
    a smaller representative set used when shared SCAD tooling is evolved or qualified
```

The controlled integration set is a testing/coordination concept, not a second repository inventory. New cross-project qualification or migration work is planned under [`../../migrations/`](../../migrations/) and implemented in the owning repositories.

## Source-of-truth boundaries

`brainboxemb.meta` owns:

- the public repository catalog and stable classification;
- portfolio-level SCAD architecture and navigation;
- cross-project migration coordination.

Individual repositories own their source/geometry, configuration and actual dependency versions, releases/tags, tests and verification, generated evidence, and project-specific design documentation.

A normal project depends directly on the tooling and libraries it needs. `brainboxemb.meta` is an information and coordination layer, not a runtime dependency.

## Historical consolidation

The current view combines responsibilities that were previously split across `tech.scad` (broad catalog/landscape) and `meta.scad-projects` (controlled integration and cross-project planning). Those repositories may be retained privately as archive history, but current public guidance must not require access to them.
