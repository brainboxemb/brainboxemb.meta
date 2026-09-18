# Technical guide

This section explains how the public brainboxemb repositories work together.

You do not need to read it from top to bottom. Pick the question that matches what you are trying to understand.

## How is a project organised?

Start with [How brainboxemb projects are organised](working-model/projects.md).

It explains what normally lives in a project repository, what shared tooling provides, and how current projects differ from older classic projects.

## Which shared tool does what?

Read [How the shared tools fit together](architecture/repository-tooling.md).

This gives a practical overview of `tool.git-project`, domain tools such as `tool.scad-project` and `tool.java-project`, and the project repositories that use them.

## How does Java execution work?

Read [Java execution model](working-model/java-execution.md).

This records the durable Maven/Moon ownership boundary, selective `auto|none|smoke|full` Windows policy, generated Java evidence and the rule that ordinary protected-main publication does not repeat Windows qualification already performed on the pull request.

## Where does generated output go?

Read [Generated output and publication](working-model/generated-output.md).

This explains why renders, binaries, verification results and assembled documentation are kept separate from normal source, and where review, production and release output can be found.

## How do versions and releases work?

Read [Versioning and releases](working-model/versioning-and-releases.md).

This explains how repositories release independently and how projects keep an exact accepted version of their dependencies.

## I am looking for SCAD/CAD information

Go to [SCAD and CAD](../domains/scad/README.md).

That section has separate readable pages for projects, reusable libraries and shared tooling.

## I am looking for software information

Go to [Software](../domains/software/README.md).

That section groups software projects, Java tooling/templates and reusable Java CI qualification work, with a technical architecture view linking to the durable Java execution model.

## I want to see the repositories

Use the [repository overview](../repositories/README.md) for the maintained public list and the [dashboard](../dashboard/README.md) for live GitHub status.

## I want to know what is changing across repositories

Use [STATUS.md](../STATUS.md).

Migration plans and their evidence are kept under [migrations/](../migrations/README.md), separate from the normal technical guide because migrations are temporary work rather than the permanent explanation of how the repositories work.

## Where should detailed information live?

This guide explains ideas that apply across repositories. Detailed design or implementation information stays closer to the thing it describes:

- project design → project repository;
- reusable component/API → library repository;
- tool behaviour → tool repository;
- cross-project overview → this repository.
