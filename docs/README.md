# Technical guide

This section explains how the public brainboxemb repositories are organised and how the shared tooling fits together.

You do not need to read everything in order. Pick the question that matches what you are trying to understand.

## I want to understand how a project is structured

Start with [How brainboxemb projects are organised](working-model/projects.md).

It explains the current project model, the difference between generic tooling, domain tooling and project code, how dependencies are pinned, and why generated output is kept away from source.

## I want to understand which tool owns what

Read [Repository tooling boundaries](architecture/repository-tooling.md).

This explains the roles of `tool.git-project`, domain tools such as `tool.scad-project` and `tool.java-project`, consumer repositories, and this meta repository.

## I want to understand generated output and the special branches

Read [Generated output and publication](working-model/generated-output.md).

This covers pull-request previews, production output and release output (`dev/pr-N/*`, `prod/*`, `rel/vX.Y.Z/*`), plus the distinction between producer evidence and later materialisation/publication.

## I want to understand versions and releases

Read [Versioning and releases](working-model/versioning-and-releases.md).

This covers independent repository versions, released tool interfaces, dependency policy versus exact gitlink locks, and exact-revision release qualification.

## I want domain-specific information

SCAD-specific architecture and ecosystem information lives under [`../domains/scad/`](../domains/scad/).

More domain sections can be added when they provide useful portfolio-level guidance rather than duplicating project documentation.

## I want to see which repositories exist

Use the [public repository catalog](../repositories/README.md). The catalog records stable classification; changing operational status is read from GitHub and shown through the dashboard.

## I want current refactoring or migration work

Use [STATUS.md](../STATUS.md) and the [migrations index](../migrations/README.md).

Those are deliberately separate from the technical guide: a migration is temporary work, while the pages above describe the current intended working model.

## Documentation boundary

This section describes shared technical concepts. Project-specific design belongs in the project repository, implementation/API details belong in the owning tool or library, and detailed completed migration evidence can remain in historical source repositories rather than being copied into the current guide.