# How brainboxemb projects are organised

This page explains the common shape of current public brainboxemb projects without assuming that you already know the individual tool repositories.

Not every repository uses the newest setup. Older projects are described as **classic** where that distinction is known.

## The basic idea

A project repository should mostly contain the project itself and the settings needed to use shared tooling. Common repository behaviour and domain-specific build logic live in reusable tool repositories instead of being copied into every project.

For a current project, that usually means three layers:

1. **shared repository tooling** — project setup, dependencies and repository-level tasks;
2. **domain tooling** — for example SCAD/SCons or Java/Maven behaviour;
3. **the project itself** — source, project settings, project-specific tests and product documentation.

## A current SCAD project

A typical current SCAD project contains:

- `project.yml` for general project/dependency settings;
- `project.scad.yml` for SCAD-specific settings;
- `tools/tool.git-project` for shared repository tooling;
- `tools/tool.scad-project` for SCAD project/build tooling;
- `dsg/` for authored design/CAD source;
- `bld/` for generated normal build output;
- `vrf/` for verification source and generated verification results.

A small reference project is [`template.scad-project`](https://github.com/brainboxemb/template.scad-project).

## A current Java project

The same basic split is used for Java:

- `tool.git-project` provides generic repository/project behaviour;
- `tool.java-project` handles Java/Maven behaviour;
- the project repository contains its modules, source and product-specific work.

A small reference project is [`template.java-project`](https://github.com/brainboxemb/template.java-project).

## Dependencies are updated deliberately

Projects keep an exact accepted revision of their dependencies. Updating a dependency is a deliberate reviewed change rather than something that happens automatically every time a project builds.

The project configuration can describe what version or branch it intends to follow, while the committed Git submodule revision records the exact version currently in use.

## Generated output stays separate from source

Generated renders, binaries, verification results and assembled documentation are normally not committed to the normal source branch.

Persistent generated output uses separate locations for different moments in the lifecycle:

- pull-request previews under `dev/pr-N/...`;
- current main output under `prod/...`;
- release output under `rel/vX.Y.Z/...`.

See [Generated output and publication](generated-output.md) for the detailed explanation.

## Current and classic projects

A classic project is not automatically broken or scheduled for migration. It simply uses an older project setup. Migration only happens when there is a useful reason and an explicit plan.

The public repository overview records the known current/classic classification.

## Where to look next

- **which repositories exist** → [Public repository overview](../../repositories/README.md)
- **how the shared tools fit together** → [How the shared tools fit together](../architecture/repository-tooling.md)
- **generated output** → [Generated output and publication](generated-output.md)
- **versions and releases** → [Versioning and releases](versioning-and-releases.md)
- **SCAD projects, libraries and tooling** → [SCAD and CAD](../../domains/scad/README.md)
- **current cross-project work** → [STATUS.md](../../STATUS.md)
