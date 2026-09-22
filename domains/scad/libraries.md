# Reusable SCAD libraries

Some CAD repositories are meant to be reused by several projects. Those repositories are libraries: they provide geometry, reference models or a small public API that another project can include instead of copying the same design knowledge.

## Libraries currently in use

| Library | What it provides |
| --- | --- |
| [`lib.scad.clamps`](https://github.com/brainboxemb/lib.scad.clamps) | Parametric clamp geometry and reusable clamp APIs. |
| [`lib.scad.hub75`](https://github.com/brainboxemb/lib.scad.hub75) | HUB75 LED-panel reference geometry, dimensions and mechanical helpers. |
| [`lib.scad.forge`](https://github.com/brainboxemb/lib.scad.forge) | Lightweight object-aware modeling layer for readable transforms, tagged CSG and overlap-aware cutters. |
| [`lib.scad.util`](https://github.com/brainboxemb/lib.scad.util) | Domain-independent OpenSCAD utilities outside the Forge modeling language, including reusable section-inspection helpers. |

The complete public repository list and classification live in [`../../repositories/catalog.yml`](../../repositories/catalog.yml). This page is the human-readable introduction rather than a second machine-maintained catalog.

## How a project uses a library

A project depends directly on the library it needs. For example, the current HUB75 display-frame project can use `lib.scad.hub75` for panel geometry while keeping the actual frame design in its own repository.

```text
CAD project
    ├── project-specific design
    ├── shared SCAD tooling
    └── reusable library
```

The library does not own the consuming project. Likewise, this meta repository is only the guide to the collection; projects do not need `brainboxemb.meta` in order to build.

## What belongs in the library repository?

A library repository is the place to look for:

- the reusable source and public API;
- library-specific design notes;
- tests and verification;
- releases and version history;
- generated examples or evidence that belong to that library.

Project-specific dimensions, assemblies and decisions stay in the project that uses the library.

## Where next?

- [SCAD overview](README.md)
- [SCAD tooling and templates](tooling.md)
- [SCAD projects](projects.md)
