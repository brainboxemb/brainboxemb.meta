# SCAD tooling and templates

The SCAD projects share a small set of repositories for common work such as project setup, building, verification and the CAD runtime. This page explains what each of those repositories is for without requiring you to read their implementation first.

## Current shared tooling

| Repository | Role |
| --- | --- |
| [`tool.git-project`](https://github.com/brainboxemb/tool.git-project) | Generic project/repository setup, dependency handling and shared repository tasks. |
| [`tool.scad-project`](https://github.com/brainboxemb/tool.scad-project) | SCAD-specific project configuration, builds, renders, exports and verification. |
| [`docker.scad-toolchain`](https://github.com/brainboxemb/docker.scad-toolchain) | Runtime image containing OpenSCAD, PythonSCAD and supporting tools. |
| [`docker.scad-toolchain.test`](https://github.com/brainboxemb/docker.scad-toolchain.test) | Checks that the shared runtime actually provides the expected capabilities. |
| [`template.scad-project`](https://github.com/brainboxemb/template.scad-project) | Small reference project showing the intended current setup. |

## How these pieces fit together

A normal current SCAD project contains its own design files and project configuration. Shared tooling is pulled in as dependencies instead of copied into the project.

```text
SCAD project
    ├── project source and settings
    ├── tool.git-project
    ├── tool.scad-project
    └── docker.scad-toolchain
```

`tool.git-project` covers things that are useful across different project types. `tool.scad-project` covers the SCAD-specific behaviour. The Docker repository provides the actual CAD runtime.

## Older projects

Several older CAD projects still use [`brainboxemb.github.actions`](https://github.com/brainboxemb/brainboxemb.github.actions), while some older repositories are completely standalone.

Those projects are labelled **classic** in the repository catalog. Classic does not mean broken or obsolete; it only describes the older project setup. They are migrated only when there is a useful reason to do so.

## Where next?

- [SCAD overview](README.md)
- [Reusable SCAD libraries](libraries.md)
- [SCAD projects](projects.md)
- [How projects are organised](../../docs/working-model/projects.md)
