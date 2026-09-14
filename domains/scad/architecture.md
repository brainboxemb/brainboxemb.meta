# SCAD technical architecture

This page is the more technical follow-up to the [SCAD overview](README.md). You only need it when you want to understand the different project setups, CAD engines and how shared tooling changes are scoped.

For a simple list of projects, libraries or tools, use the overview pages instead.

## Two ways to look at the SCAD repositories

There is one broad portfolio view and, when shared tooling is being changed, sometimes a smaller test set.

### The full public SCAD/CAD collection

The public collection is described by:

```text
repositories/catalog.yml
    public repository list and classification

domains/scad/
    readable SCAD/CAD guide
```

This includes current and classic projects, reusable libraries and shared tooling.

### A smaller test set for shared tooling

A tooling migration does not need every CAD project as a test consumer. It can use a smaller representative set containing the relevant tool, a reference/template consumer and one or more real consumers.

That test set is not a second repository catalog. It exists only for the migration or qualification work that needs it.

## Newer and older project setups

The SCAD/CAD collection currently contains several generations of project setup.

```text
classic standalone
    project-local OpenSCAD source
    no shared project workflow

classic shared-actions
    project source
        -> brainboxemb.github.actions

current
    structured project
        -> tool.git-project
        -> tool.scad-project
        -> docker.scad-toolchain
```

**Classic** describes an older setup. It does not mean the project or tooling can simply be removed.

The current diagram describes the intended shared setup. A repository itself remains the best place to check exactly which tool versions it currently uses.

## CAD engine and project setup are different things

The CAD engine tells you what actually evaluates the design:

- OpenSCAD;
- PythonSCAD;
- or both.

The project setup tells you how the repository is organised and built:

- classic standalone;
- classic shared-actions;
- current shared project tooling.

Do not infer the engine only from a repository name. Actual source or build configuration is better evidence.

## Projects use their dependencies directly

A project includes the tools and libraries it actually needs. It does not use `brainboxemb.meta` as a runtime dependency.

Conceptually:

```text
project
    ├── shared project tooling
    └── reusable libraries it needs
```

For example, a HUB75 project can use `lib.scad.hub75` directly without going through this meta repository.

## Choosing which projects a tooling change affects

When a change is specifically about the current shared SCAD stack, start from repositories classified as current-generation projects in the public catalog.

Classic projects are not automatically included. Migrating one of them should be an explicit project decision, not a side effect of a generic tooling change.

A migration may still test a smaller representative subset rather than every current project.

## Where information should live

Use this rule of thumb:

- **project repository** — the actual design, dimensions, project configuration and project-specific documentation;
- **library repository** — reusable geometry/API, library tests and releases;
- **tool repository** — shared build/project behaviour implemented by that tool;
- **brainboxemb.meta** — overview, navigation, common explanations and cross-project migration records.

This keeps the meta repository useful as a guide without turning it into a copy of every project's documentation.

## Historical note

The broad SCAD overview was originally kept in `tech.scad`, while a smaller current-stack integration view was coordinated through `meta.scad-projects`. Those useful concepts have been consolidated here; both older repositories are now private archives.
