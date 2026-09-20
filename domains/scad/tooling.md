# SCAD tooling and templates

The SCAD projects share a small set of repositories for project setup, change-impact decisions, building, verification and the CAD runtime. This page explains **which repository owns which part** without requiring you to read its implementation first.

For the technical execution model — including Moon capabilities, inheritance, Moon versus SCons, runtime-profile selection and publication — see [SCAD technical architecture](architecture.md).

## Current shared tooling

| Repository | Role |
| --- | --- |
| [`tool.git-project`](https://github.com/brainboxemb/tool.git-project) | Generic repository/Moon mechanics: exact revision comparison, affected-task query and shared Git/publication primitives. |
| [`tool.scad-project`](https://github.com/brainboxemb/tool.scad-project) | SCAD-specific project model and lifecycle: shared capability tasks, builds/renders/docs/verification, runtime selection and applicable cache policy. |
| [`docker.scad-toolchain`](https://github.com/brainboxemb/docker.scad-toolchain) | Related SCAD runtime image family: OpenSCAD-focused, drawing/publication and full OpenSCAD + PythonSCAD profiles. |
| [`docker.scad-toolchain.test`](https://github.com/brainboxemb/docker.scad-toolchain.test) | External qualification of the published SCAD runtime profiles and their shared/specific capability contracts. |
| [`template.scad-project`](https://github.com/brainboxemb/template.scad-project) | Reference project showing the intended consumer-facing setup. |

## How these pieces fit together

A normal current-generation SCAD project contains its own design files and project configuration. Shared tooling is pinned as dependencies instead of copied into the project.

```text
SCAD project
    ├── project source and project.scad.yml
    ├── small Moon capability/impact configuration
    ├── tool.git-project
    ├── tool.scad-project
    └── one appropriate scad-toolchain runtime profile
```

The intended ownership split is:

- `tool.git-project` knows **generic Git/Moon repository mechanics**, not SCAD domain rules;
- `tool.scad-project` knows **SCAD capabilities and lifecycle policy**;
- the consumer says **which capabilities it has and which project-specific sources affect them**;
- `docker.scad-toolchain` supplies the reproducible CAD runtime.

Normal consumers should therefore not copy a large Moon lifecycle graph. Shared capability tasks such as `scad.build`, `scad.docs` and `scad.verify` are inherited from pinned `tool.scad-project` policy; the project adds only its capability selection and project-specific impact rules.

## Runtime profiles

The normal shared SCAD runtime is one image family, not one mandatory
all-inclusive image for every task.

```text
OpenSCAD-focused
  OpenSCAD + BOSL2 + docs tooling + SCons + common runtime tools

drawing/publication
  OpenSCAD-focused contract
  + drawsvg + Inkscape

full/dual
  OpenSCAD-focused contract
  + PythonSCAD + pybosl2 + PythonSCAD-specific dependencies
```

The focused/full split was introduced in `docker.scad-toolchain v0.5.0`; the
drawing profile followed in v0.6.0 and the current v0.6.1 line pins drawsvg for
scripted SVG authoring.

Runtime selection follows effective project configuration/capabilities rather
than a repository-name allowlist. OpenSCAD-only work may use the focused
profile, publication work can opt into the drawing profile, and a project that
intentionally supports PythonSCAD uses the full/dual profile.

## Moon and SCons are different layers

A short rule of thumb:

```text
Moon
  whole repository capability: affected or reusable?

SCons, only when configured
  individual targets inside an executing capability
```

A direct-engine project does not need SCons cache handling merely because another project uses SCons.

The complete rationale and configuration model are documented in [SCAD technical architecture](architecture.md).

## Current rollout status

The architecture is being rolled out through [Migration 005](../../migrations/005-scad-execution-architecture/README.md). The runtime image family is already released; shared tooling and consumers move owner by owner.

During rollout, each repository remains authoritative for the exact versions and lifecycle it currently pins. This page describes the intended current shared architecture, not a claim that every SCAD repository has already migrated.

## Older projects

Several older CAD projects still use [`brainboxemb.github.actions`](https://github.com/brainboxemb/brainboxemb.github.actions), while some older repositories are completely standalone.

Those projects are labelled **classic** in the repository catalog. Classic does not mean broken or obsolete; it only describes the older project setup. They are migrated only when there is a useful reason.

## Where next?

- [SCAD overview](README.md)
- [Technical architecture](architecture.md)
- [Reusable SCAD libraries](libraries.md)
- [SCAD projects](projects.md)
- [How projects are organised](../../docs/working-model/projects.md)
