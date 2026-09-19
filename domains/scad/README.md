# SCAD and CAD

This section is the easiest place to understand the public SCAD/CAD repositories as a group.

You do not need to know the tooling architecture first. Start with the part you are interested in:

- [**Projects**](projects.md) — the actual CAD designs;
- [**Source structure**](source-structure.md) — how OpenSCAD components, interactive design views and design documentation fit together;
- [**Libraries**](libraries.md) — reusable geometry and reference models used by projects;
- [**Tooling and templates**](tooling.md) — which shared repositories own project setup, builds, verification and the CAD runtime;
- [**Technical architecture**](architecture.md) — how GitHub Actions, Moon capabilities/inheritance, SCons, runtime profiles, caches and publication fit together.

Historical experimental evidence that shaped the current execution boundary is retained in [`exp.2026-003.scad-ci-performance`](https://github.com/brainboxemb/exp.2026-003.scad-ci-performance). That experiment compared the Docker and host execution shapes used during Migration 004; it is evidence, not a production dependency.

## The basic picture

The SCAD/CAD repositories have three main roles:

```text
projects
    actual designs

libraries
    reusable design knowledge

tooling
    shared build/project infrastructure
```

A project can use one or more libraries and the shared tooling, but it still owns its own design and documentation.

For example, the current HUB75 display-frame project uses shared SCAD tooling and can reuse panel geometry from `lib.scad.hub75`, while the frame design itself stays in the project repository.

## Current and classic projects

The collection contains both newer projects using the current shared project setup and older projects using the earlier setup.

We call the older setup **classic**. That label is descriptive, not a judgement: a classic project can still be perfectly usable and does not need to be migrated unless there is a reason to do so.

See [Projects](projects.md) for the readable list and the [repository catalog](../../repositories/README.md) for the complete public inventory.

## Where should I make a change?

A useful rule is:

- change a **specific design** in its project repository;
- change **reusable geometry** in the library repository that owns it;
- change **shared build/project behaviour** in the relevant tooling repository;
- update this section when the overview or navigation between repositories changes.

`brainboxemb.meta` explains the collection; normal projects do not need this repository in order to build.

## Historical note

The broad SCAD overview used to live in `tech.scad`, while cross-project SCAD coordination lived in `meta.scad-projects`. Their useful public overview has been consolidated here; both older repositories are now private archives.
