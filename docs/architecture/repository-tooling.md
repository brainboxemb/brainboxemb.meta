# How the shared tools fit together

Several brainboxemb projects use the same repository and build tooling. The tools are split up so a SCAD project, a Java project and an engineering-document project can share generic behaviour without all using the same build system.

## The short version

There are three practical layers:

1. **generic repository tooling** — things that are useful for many project types;
2. **domain tooling** — behaviour specific to SCAD, Java, documents, or another domain;
3. **the project itself** — the actual product/design source and project-specific choices.

```text
project
    ├── generic repository tooling
    └── domain-specific tooling
```

`brainboxemb.meta` only explains and connects these repositories. A normal project does not need this meta repository to build.

## Generic repository tooling

[`tool.git-project`](https://github.com/brainboxemb/tool.git-project) provides common repository behaviour such as project setup, dependency handling and shared repository tasks.

It should stay useful across different project types. It therefore does not need to understand how OpenSCAD targets, Maven modules or document assembly work internally.

## Root launcher naming

Current-generation projects expose the generic Git repository entrypoints in the
project root. Their names are a direct projection of the canonical consumer
templates owned by `tool.git-project`:

```text
tool.git-project/bootstrap/consumer-bootstrap.ps1 -> bootstrap.ps1
tool.git-project/bootstrap/consumer-bootstrap.sh  -> bootstrap.sh
tool.git-project/bootstrap/consumer-update.ps1    -> update.ps1
tool.git-project/bootstrap/consumer-update.sh     -> update.sh
```

The naming rule is deliberately mechanical: materializing a canonical consumer
launcher removes only the `consumer-` prefix. It does not apply a second rename,
so `consumer-update.*` becomes `update.*`, not `update-repo.*`.

These root files are managed copies of generic Git tooling. Their implementation
and refresh/provenance behaviour live in `tool.git-project`; this page records
the portfolio-wide naming convention used by SCAD, Java and future project
types.

## Domain-specific tools

Domain tools contain the behaviour that really is specific to that type of project.

Examples:

| Tool | What it is for |
| --- | --- |
| [`tool.scad-project`](https://github.com/brainboxemb/tool.scad-project) | SCAD project configuration, builds, renders, exports and verification. |
| [`tool.java-project`](https://github.com/brainboxemb/tool.java-project) | Java/Maven build and test behaviour. |
| [`tool.eng-docs`](https://github.com/brainboxemb/tool.eng-docs) | Engineering-document assembly. |

This split keeps shared repository tasks reusable while leaving specialist behaviour with the tool that understands it.

## What stays in the project?

The project repository owns the things that are specific to that project, including:

- product/design source;
- project configuration;
- project-specific tests or verification;
- project documentation;
- the exact dependency versions currently accepted by the project.

If a change only matters to one project, it normally belongs there rather than in a central tool.

## Libraries are separate again

A reusable library is neither generic tooling nor a project. It contains reusable design or software components that a project can consume directly.

For the SCAD examples, see [Reusable SCAD libraries](../../domains/scad/libraries.md).

## Current and classic projects

Newer repositories use the current shared project setup. Older CAD repositories can still use the previous GitHub Actions setup or be completely standalone.

We call those older setups **classic**. Classic projects remain valid and are not automatically migrated just because newer tooling exists.

The [repository overview](../../repositories/README.md) records which setup a repository uses where that classification is known.

## More detail

For the practical project layout, see [How brainboxemb projects are organised](../working-model/projects.md).

For generated output and the `dev/`, `prod/` and `rel/` locations, see [Generated output and publication](../working-model/generated-output.md).
