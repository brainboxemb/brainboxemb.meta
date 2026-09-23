# brainboxemb.meta

This repository is the **map of the public brainboxemb repositories**.

Use it when you want to understand what projects and tools exist, how they relate to each other, and where to look for more detail.

You do not need this repository to build a project. Each project, library and tool still lives in its own repository.

## What are you looking for?

### Projects and repositories

Start with the [repository overview](repositories/README.md) or the live [dashboard](dashboard/README.md).

The repository overview explains the stable roles of projects, tools, libraries, templates and experiments. The dashboard shows changing GitHub information such as workflow health and pull requests.

### SCAD / CAD

Go to [SCAD and CAD](domains/scad/README.md).

There you can browse separately through:

- [projects](domains/scad/projects.md);
- [reusable libraries](domains/scad/libraries.md);
- [tooling and templates](domains/scad/tooling.md).

### Software

Go to [Software](domains/software/README.md).

There you can browse separately through:

- [projects](domains/software/projects.md);
- [tooling and templates](domains/software/tooling.md);
- [technical architecture](domains/software/architecture.md).

### How projects are organised

Read [How brainboxemb projects are organised](docs/40-02_projects.md).

That page explains the common project structure in practical terms and points to the reference projects for SCAD and Java.

### Shared tooling

Use the [technical guide](docs/README.md) when you want to understand how shared tooling, generated output, versions and releases work.

The implementation details stay in the tool repositories themselves.

### Current cross-project work

Read [STATUS.md](STATUS.md).

This is intentionally separate from the general documentation. It tells you whether a repository-spanning migration is active, what is deferred, and which plans are only proposals.

To continue cross-project work in a fresh ChatGPT/work session, use the copy/paste instruction in [New chat / work-session handoff](docs/20-20_new-session-handoff.md).

### Experiments

The [experiments section](experiments/README.md) explains which separate experiment repositories were used to investigate technical choices.

## How the collection is organised

Most repositories have one clear role:

- **projects** contain the actual product or design work;
- **libraries** contain reusable components or geometry;
- **tools** provide shared build or repository behaviour;
- **templates** show the intended setup for a new project;
- **experiments** test an idea without becoming a normal project dependency;
- **brainboxemb.meta** provides the overview, shared guidance, dashboard and cross-project migration records.

If you want to change a specific project, start in that project's own repository. If you want to change shared behaviour, start in the tool or library that owns it.

## Public scope

This repository describes the **public** brainboxemb repository collection.

The machine-readable list is [`repositories/catalog.yml`](repositories/catalog.yml). It feeds the dashboard and is kept separate from changing GitHub status.

For automated-agent maintenance instructions, see [AGENTS.md](AGENTS.md).
