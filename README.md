# brainboxemb.meta

`brainboxemb.meta` is the landing page and technical guide for the public brainboxemb repositories.

If you arrive here without knowing the repository structure yet, this is the place to discover **what exists, how projects are organised, which shared tools they use, where generated output goes, and what cross-project changes are currently being worked on**.

The individual repositories remain the source of truth for their own implementation. This repository connects them and explains the common model.

## Where do I start?

### I want to see the projects and tools

Start with the [public repository catalog](repositories/README.md). It groups the public repositories by role and records stable information such as domain, lifecycle and whether a project uses the current or classic infrastructure generation.

For live operational information such as workflow health, pull requests and recent activity, use the [dashboard](dashboard/README.md). The dashboard reads current state from GitHub rather than duplicating it in maintained documentation.

### I want to understand how a normal project works

Read [How brainboxemb projects are organised](docs/working-model/projects.md).

That page explains the current project model in practical terms: what belongs in a project repository, what is provided by shared tooling, how dependencies are pinned, and why generated build/verification output is kept separate from source.

The small reference projects are useful concrete examples:

- [`template.scad-project`](https://github.com/brainboxemb/template.scad-project) for current SCAD/CAD projects;
- [`template.java-project`](https://github.com/brainboxemb/template.java-project) for current Java projects.

Older projects can still use the classic infrastructure. “Classic” means not yet migrated to the current shared project stack; it does not mean the project is invalid or automatically scheduled for migration.

### I want to understand the shared tooling

The [technical guide](docs/README.md) explains the common infrastructure without requiring you to read the implementation repositories first.

Useful entry points are:

- [Repository tooling boundaries](docs/architecture/repository-tooling.md) — what `tool.git-project`, domain tools and project repositories each own;
- [Generated output and publication](docs/working-model/generated-output.md) — how review, production and release output is published without mixing generated files into source;
- [Versioning and releases](docs/working-model/versioning-and-releases.md) — how independently versioned repositories consume released tooling and exact dependency locks.

The generic repository layer is provided by `tool.git-project`. Domain-specific behaviour stays in domain tools such as `tool.scad-project`, `tool.java-project` and `tool.eng-docs`.

### I want domain-specific information

Use the [`domains/`](domains/) area. The SCAD section currently contains the most developed domain overview and explains the current SCAD ecosystem, current-versus-classic infrastructure and the relationship between projects, libraries and tooling.

Domain documentation here is intentionally broader than one project. Detailed component design or implementation documentation remains in the repository that owns it.

### I want to know what is changing now

Read [STATUS.md](STATUS.md).

That page is about **current cross-project work**, not about the whole purpose of this repository. It separates completed foundations, active work, deferred improvements and proposed migrations.

Repository-spanning changes that need coordinated work live under [migrations/](migrations/README.md). A migration can be documented before it is activated; a plan marked **proposed / inactive** must not start automatically.

### I want to understand why a technical choice was made

Experiments stay in their own repositories so evidence and temporary test code do not become production dependencies. The [`experiments/`](experiments/README.md) section records what those experiments investigated and which decisions they support.

## How the repository collection fits together

The public repositories broadly fall into a few roles:

- **projects** contain the actual CAD, software or other product work;
- **libraries** provide reusable domain components;
- **tools** provide shared repository or domain behaviour;
- **templates** are small reference consumers that demonstrate the intended current setup;
- **experiments** test architectural or tooling choices without becoming normal dependencies;
- **brainboxemb.meta** provides the overview, common technical guidance, catalog, dashboard and cross-project migration coordination.

This separation is deliberate. A project should not need `brainboxemb.meta` to build, and this repository should not absorb implementation details merely because several projects use the same tool.

## Generated output is part of the workflow

Many repositories publish generated results separately from their source branches. A pull request can have review output under `dev/pr-N/...`, the current main revision under `prod/...`, and releases under `rel/vX.Y.Z/...`.

This makes renders, binaries, verification evidence and assembled documentation inspectable without committing generated files into normal source history. The detailed model is described in [Generated output and publication](docs/working-model/generated-output.md).

## Repository catalog and dashboard

[`repositories/catalog.yml`](repositories/catalog.yml) is the canonical catalog for the public repository set. It stores stable classification and intent.

Live state is deliberately not copied into that file. The dashboard obtains changing information directly from GitHub and uses the central catalog only to know which repositories and classifications to present.

## Scope

This repository covers the **public** brainboxemb repository collection.

Individual repositories remain authoritative for their own code, releases, project-specific architecture, tests and local plans. `brainboxemb.meta` provides the map and the common technical context around them.

For maintenance/agent guidance, see [AGENTS.md](AGENTS.md).