# SCAD landscape architecture

## Overview layers

The portfolio needs two different views of the SCAD ecosystem, but they do not need separate catalog repositories.

### Broad portfolio view

The broad view is owned by:

```text
repositories/catalog.yml
    canonical public repository membership and stable classification

domains/scad/
    durable SCAD-specific architecture and navigation
```

It includes both current and classic project infrastructure, reusable libraries, shared tooling and actual user CAD projects.

### Controlled integration view

A smaller controlled set is used to evolve and qualify the current shared SCAD stack. It may contain generic bootstrap tooling, runtime verification, SCAD project tooling, a reference consumer and representative library/real-consumer integration.

That controlled set must not become a second complete CAD-project inventory. Active cross-project plans and qualification evidence belong in `brainboxemb.meta/migrations/`; implementation evidence remains in the repositories that own the implementation.

## Project-infrastructure generations

Keep current and classic infrastructure explicit.

```text
classic standalone
    project-local OpenSCAD source
    no shared project workflow

classic shared-actions
    project CAD source
        -> brainboxemb.github.actions
        -> shared OpenSCAD setup/render/export workflow

current
    structured SCAD project
        -> tool.git-project        generic bootstrap/dependency layer
        -> tool.scad-project       SCAD project/build/verification layer
        -> docker.scad-toolchain   OpenSCAD/PythonSCAD runtime
```

`brainboxemb.github.actions` remains relevant while classic consumers still use it. Classic describes the project generation; it does not mean the tooling or project can be removed.

The current-generation diagram describes the intended ownership boundary. Actual adoption is repository-specific: inspect the repository before claiming that it has migrated to a particular bootstrap/tooling contract.

## Engine and infrastructure are separate

Do not conflate the CAD engine with project infrastructure.

```text
engine
    OpenSCAD
    PythonSCAD
    both

project infrastructure
    classic standalone
    classic shared-actions
    current tool.scad-project generation
```

A repository name such as `.cad.` is not evidence of an engine.

For OpenSCAD, actual `.scad` project source or an OpenSCAD build invocation is direct evidence. For PythonSCAD, a generic `.py` file is insufficient; use PythonSCAD-specific source/API usage, explicit project configuration or build/render invocation.

## Dependency rule

A project depends directly on the tooling and libraries it needs.

Conceptually, a current consumer looks like:

```text
project
    ├── tools/tool.git-project
    ├── tools/tool.scad-project
    └── dsg/.../ext/lib.scad.*
```

It must not depend on `brainboxemb.meta` or a catalog repository to obtain those dependencies.

Classic projects may continue to use `brainboxemb.github.actions` directly until an explicit project-specific migration is chosen.

## Migration-scope rule

For generic current-stack migrations, start from the canonical catalog and repositories classified with:

```yaml
project_infrastructure:
  generation: current
```

Do not infer that every CAD repository participates merely from its name or language.

Repositories classified as `classic` remain outside a generic current-stack migration unless a separate project-specific migration explicitly includes them.

A controlled integration/qualification set may be smaller than the broad current-generation candidate set. That is intentional.

## Source-of-truth boundaries

`brainboxemb.meta` owns:

- public repository membership and stable portfolio classification;
- broad SCAD architecture and navigation;
- repository-spanning migration plans and retained cross-project evidence.

Individual repositories own:

- source code and geometry;
- project configuration;
- actual dependency pins/adoption state;
- releases/tags;
- tests and verification;
- detailed technical/design documentation;
- generated artifacts/evidence.

Shared tool repositories own their implementation contracts. The meta layer describes boundaries and coordinates migration; it does not absorb tool implementation.

## Historical origin

The current architecture consolidates ideas that were previously maintained in separate public `tech.scad` and `meta.scad-projects` repositories. Their useful rules and current status have been transferred here; those old repositories can therefore become private archives without being required for current public understanding.
