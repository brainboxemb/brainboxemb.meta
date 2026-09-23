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

For the SCAD examples, see [Reusable SCAD libraries](../domains/scad/libraries.md).

## Current and classic projects

Newer repositories use the current shared project setup. Older CAD repositories can still use the previous GitHub Actions setup or be completely standalone.

We call those older setups **classic**. Classic projects remain valid and are not automatically migrated just because newer tooling exists.

The [repository overview](../repositories/README.md) records which setup a repository uses where that classification is known.

## More detail

For the practical project layout, see [How brainboxemb projects are organised](40-02-projects.md).

For generated output and the `dev/`, `prod/` and `rel/` locations, see [Generated output and publication](40-04-generated-output.md).


## GitHub Actions workflow filenames

Workflow filenames under `.github/workflows/` use lowercase kebab-case and put
the **category/purpose first** so related workflows group naturally in a
directory listing.

Use these forms:

| Kind | Filename form | Example |
| --- | --- | --- |
| Repository self-entry workflow | `self-<operation>.yml` | `self-release.yml` |
| Reusable workflow API | `reusable-<capability>.yml` | `reusable-generated-output-publish.yml` |
| Contract/test workflow | `test-<capability>.yml` | `test-generated-output-publish.yml` |

The prefixes describe workflow scope:

- `self-` — owned and started by this repository (event/manual dispatch), not a
  cross-repository workflow API;
- `reusable-` — public `workflow_call` API that other workflows/repositories
  may call;
- `test-` — workflow whose primary purpose is qualifying a capability or
  contract.

Prefer:

```text
self-release.yml
self-pages.yml

test-self.yml
test-execution-evidence-schema.yml
test-generated-output-publish.yml
test-generated-output-same-job.yml
test-moon-orchestration.yml
test-pr-preview-cleanup.yml
test-release-lifecycle.yml

reusable-generated-output-publish.yml
reusable-pr-preview-cleanup.yml
reusable-release.yml
```

Do not leave current repository self-entry workflows unprefixed merely
because names such as `release.yml` or `pages.yml` are familiar. The
`self-` prefix makes their non-reusable scope explicit and groups them
together in directory listings.

Do not use the equivalent suffix form `<capability>-test.yml` for new/current
workflows. Prefixing the category keeps all tests together when files are sorted
by name.

Workflow filenames describe a durable repository capability or contract. Do not
encode issue numbers, migration numbers, temporary experiments, or the historical
bug that first caused a regression test to be added.

### Workflow purpose header

Every maintained workflow should state its intent near the top of the file,
directly after `name:`.

Use a short two-line comment:

```yaml
name: Release

# Purpose: create an immutable tool release from an already-qualified commit.
# Scope: repository self-entry workflow; not a reusable workflow API.
```

For reusable workflows, identify the public `workflow_call` contract:

```yaml
name: Reusable generated-output publication

# Purpose: publish one generated-output family for a caller repository.
# Scope: public reusable workflow API.
```

For test workflows, state the capability or contract being qualified:

```yaml
name: Test release lifecycle

# Purpose: qualify the generic release-request/tag lifecycle without publishing a real release.
# Scope: repository qualification workflow.
```

Keep these comments concise. They are orientation, not a duplicate design
document.

### Workflow display names

The workflow filename owns the machine-facing scope category. The YAML `name:`
owns the human-facing label shown in the GitHub Actions sidebar.

Do not mechanically repeat the filename or repository name in `name:`.
Keep display names short enough to scan comfortably.

Recommended pattern:

- self workflows normally use the operation only, for example `Release`,
  `Pages`, or `CI`;
- reusable workflows keep the `Reusable` group word, followed by a short
  capability label, for example `Reusable release` or `Reusable PR cleanup`;
- qualification workflows use `Self-test` or `Test <capability>`, for example
  `Test release` or `Test Moon`.

Use a domain/repository qualifier only when it disambiguates two workflows in
the same repository. The repository name itself normally adds no useful
information in the Actions sidebar.

This convention defines naming only. It does not require an unrelated classic
repository to be renamed immediately; existing current-generation repositories
can adopt it with related tooling changes or a coordinated rollout.
