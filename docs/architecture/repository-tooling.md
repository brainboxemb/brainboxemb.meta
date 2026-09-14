# Repository tooling boundaries

## Purpose

Public brainboxemb repositories use multiple layers because generic repository lifecycle, domain execution and project implementation have different owners.

The key rule is:

> Generic repository concerns belong in generic repository tooling; domain semantics stay with domain tooling; project-specific behavior stays with the project.

`brainboxemb.meta` coordinates those boundaries but is not a runtime dependency of normal consumers.

## Ownership model

```text
brainboxemb.meta
    cross-project architecture
    repository catalog/classification
    migration coordination/evidence
    shared working conventions

        ↓ describes / coordinates

tool.git-project
    generic Git/bootstrap/dependency lifecycle
    optional Moon repository orchestration integration
    generic generated-output publication/cleanup
    generic repository lifecycle evidence where domain-neutral

        ↓ dispatches / composes

domain tooling
    tool.scad-project
    tool.java-project
    tool.eng-docs
    ...

        ↓ owns domain semantics

consumer repository
    product/project source
    project-specific configuration
    project-specific verification/release details
    exact dependency locks
```

## `tool.git-project`

`tool.git-project` is the generic repository-infrastructure owner for current-generation repositories.

It owns concerns that are not specific to CAD, Java or documents, including where adopted:

- bootstrap of the generic tooling gitlink;
- generic `project.yml` validation;
- dependency/submodule registration, status and intentional updates;
- exact committed gitlink restoration;
- optional Moon runtime/bootstrap integration;
- high-level repository task invocation boundaries;
- generated-output lifecycle namespaces;
- publication/cleanup mechanics that are domain-neutral.

Its Git bootstrap/status/update core must stay usable without requiring domain tooling.

It must not learn domain semantics such as Maven reactor behavior, SCons target decisions or engineering-document producer logic.

## Domain tooling

Domain owners keep concrete execution semantics.

Examples:

```text
tool.scad-project
    SCAD configuration
    SCons target discovery/execution
    build/design/verification semantics
    structured target-decision evidence

tool.java-project
    Java/Maven execution
    test/build evidence
    Java-specific version/build behavior

tool.eng-docs
    generic engineering-document manifest/assembly behavior
    document-specific producer/assembly contracts
```

Moon or another repository-level orchestrator may decide whether a meaningful high-level domain stage executes or is hydrated, but it does not replace the domain engine.

## Consumer ownership

A consumer repository owns:

- authored product/project source;
- project-specific architecture and plans;
- exact dependency locks committed in the repository;
- project-specific configuration;
- project-specific verification semantics not provided by a reusable domain owner;
- product-specific release metadata/assets when needed.

Cross-project migration work must not move this implementation detail into `brainboxemb.meta`.

## Direct dependency rule

A repository initializes and manages its **direct dependencies**. Consuming a library does not imply recursively materializing every development-only dependency of that library.

Conceptually:

```text
project standalone
    restores its direct tooling/libraries

library consumed by project
    is consumed at its committed interface
    does not automatically pull its standalone development toolchain

library standalone
    restores its own direct development/tooling dependencies
```

This keeps normal consumers smaller while preserving standalone reproducibility.

## Dependency policy versus exact lock

Current-generation repositories distinguish intent from the exact accepted commit:

```text
project.yml ref
    policy used by an intentional dependency update

Git submodule gitlink
    exact commit used by normal clone/bootstrap/build
```

A normal bootstrap restores committed locks. It must not silently advance a dependency merely because its configured policy points to a newer tag/branch.

## Current and classic project infrastructure

Do not infer migration scope from repository names or from the CAD engine used.

The canonical classification is in `repositories/catalog.yml`, including where applicable:

```yaml
project_infrastructure:
  generation: current
  provider: tool.scad-project
```

or:

```yaml
project_infrastructure:
  generation: classic
  provider: brainboxemb.github.actions
```

A classic project is still a valid project. Shared-stack work does not automatically migrate it.

## Meta boundary

`brainboxemb.meta` is a coordination and observation layer.

It may define shared architecture, migration ordering and evidence requirements, but normal project execution must not require checking out `brainboxemb.meta` as a runtime dependency.
