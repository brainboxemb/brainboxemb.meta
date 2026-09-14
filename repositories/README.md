# Public repository overview

This section answers a simple question: **what kinds of public brainboxemb repositories are there, and where should I look?**

For live information such as workflow status, open pull requests and recent activity, use the [dashboard](../dashboard/README.md).

## Main groups

### Projects

Projects contain the actual design or software work.

- SCAD/CAD projects → [SCAD projects](../domains/scad/projects.md)
- event-timing software planning → [`2026-010-01.meta.event-timing-software`](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software)
- Java event-timing framework → [`2026-010-02.java.event-timing-framework`](https://github.com/brainboxemb/2026-010-02.java.event-timing-framework)

### Reusable libraries

Libraries contain components intended to be reused by multiple projects.

- SCAD libraries → [Reusable SCAD libraries](../domains/scad/libraries.md)

### Shared tooling and templates

Tool repositories provide shared project or build behaviour. Templates are small reference projects that demonstrate the intended setup.

- SCAD tooling → [SCAD tooling and templates](../domains/scad/tooling.md)
- generic repository tooling → [`tool.git-project`](https://github.com/brainboxemb/tool.git-project)
- Java project tooling → [`tool.java-project`](https://github.com/brainboxemb/tool.java-project)
- engineering-document tooling → [`tool.eng-docs`](https://github.com/brainboxemb/tool.eng-docs)

### Sites and experiments

Site repositories contain published web content or site experiments. Experiment repositories investigate technical choices without becoming normal project dependencies.

See the [dashboard](../dashboard/README.md) for the complete current public set and live status.

## The machine-readable catalog

[`catalog.yml`](catalog.yml) is the maintained list used by the dashboard. It records stable information such as:

- repository name;
- broad role/category;
- domain;
- whether known project infrastructure is current or classic;
- the shared tool that provides that project setup where relevant.

It deliberately does **not** store changing GitHub information such as workflow health or open pull requests. The dashboard reads those directly from GitHub.

## Adding or changing a repository

When the public repository collection changes, update `catalog.yml` once. Do not maintain a second copy of the same membership list in dashboard configuration.

Private repositories are outside this catalog.

For dashboard implementation details, see [`../dashboard/README.md`](../dashboard/README.md).
