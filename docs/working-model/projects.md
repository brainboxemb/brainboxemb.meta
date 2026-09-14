# How brainboxemb projects are organised

This page explains the common shape of current public brainboxemb projects without assuming knowledge of the individual tool repositories.

Not every repository has already migrated to this model. The repository catalog marks older projects as `classic` where that distinction is known.

## The basic idea

A project repository should contain the project itself and only the configuration needed to use shared tooling. Generic repository behaviour and domain-specific build logic live in reusable tool repositories instead of being copied into every project.

For a current-generation project, that usually means three layers:

1. **generic repository tooling** — cloning/bootstrap, dependency pins, repository-level orchestration and generated-output publication;
2. **domain tooling** — for example SCAD/SCons or Java/Maven behaviour;
3. **the project itself** — source, project configuration, project-specific tests/verification and product documentation.

This lets projects share infrastructure without making a central meta repository part of their runtime.

## A current SCAD project

A typical current SCAD consumer contains:

- `project.yml` for generic repository/dependency policy;
- `project.scad.yml` for SCAD-specific configuration;
- `tools/tool.git-project` as the generic bootstrap/tooling pin;
- `tools/tool.scad-project` as the SCAD domain tooling dependency;
- `dsg/` for authored design/CAD source;
- `bld/` for generated normal build output;
- `vrf/` for verification source and generated verification evidence.

Normal CAD renders/exports, design documentation and verification evidence can have different lifecycles even though they ultimately use the same SCAD tooling stack.

The small reference implementation is [`template.scad-project`](https://github.com/brainboxemb/template.scad-project).

## A current Java project

A current Java consumer follows the same ownership idea but keeps Maven semantics in the Java tool layer:

- `tool.git-project` provides generic repository/bootstrap/orchestration behaviour;
- `tool.java-project` owns the canonical Java/Maven execution and evidence contract;
- the project repository owns its Maven modules, source and product-specific behaviour.

The small reference implementation is [`template.java-project`](https://github.com/brainboxemb/template.java-project).

## Dependencies: policy and exact lock

Current projects distinguish the dependency they *intend* to follow from the exact commit they currently use.

- `project.yml` records the dependency policy/reference;
- the Git submodule gitlink records the exact accepted commit.

Normal bootstrap restores that exact lock. Updating a dependency is a deliberate reviewed action rather than a side effect of building a project.

## Generated output is kept away from source

Generated renders, binaries, verification evidence and assembled documentation are normally not committed to the normal source branch.

Persistent generated output uses lifecycle namespaces:

- pull-request previews under `dev/pr-N/...`;
- current main output under `prod/...`;
- release output under `rel/vX.Y.Z/...`.

This makes generated evidence easy to inspect without mixing it with authored source.

See [Generated output and publication](generated-output.md) for the detailed model.

## Current versus classic projects

The public repository set contains both current-generation and older/classic projects.

A classic project is not automatically broken or scheduled for migration. Migration happens only when there is a useful reason and an explicit plan.

The canonical classification is maintained in [`../../repositories/catalog.yml`](../../repositories/catalog.yml).

## Where to look next

If you want to understand:

- **which repositories exist and what role they have** → [`../../repositories/`](../../repositories/README.md);
- **generic tooling ownership** → [Repository tooling boundaries](../architecture/repository-tooling.md);
- **generated output branches and evidence** → [Generated output and publication](generated-output.md);
- **versioning/releases** → [Versioning and releases](versioning-and-releases.md);
- **SCAD-specific architecture** → [`../../domains/scad/`](../../domains/scad/README.md);
- **current migrations/refactoring work** → [`../../migrations/`](../../migrations/README.md).
