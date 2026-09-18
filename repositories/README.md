# Public repository overview

This section answers a simple question: **what kinds of public brainboxemb repositories are there, and where should I look?**

For live information such as workflow status, open pull requests and recent activity, use the [dashboard](../dashboard/README.md).

## Main groups

### Projects

Projects contain the actual design or software work.

- SCAD/CAD projects → [SCAD projects](../domains/scad/projects.md)
- software projects → [Software projects](../domains/software/projects.md)

### Reusable libraries

Libraries contain components intended to be reused by multiple projects.

- SCAD libraries → [Reusable SCAD libraries](../domains/scad/libraries.md)

### Shared tooling and templates

Tool repositories provide shared project or build behaviour. Templates are small reference projects that demonstrate the intended setup.

- SCAD tooling → [SCAD tooling and templates](../domains/scad/tooling.md)
- generic repository tooling → [`tool.git-project`](https://github.com/brainboxemb/tool.git-project)
- software/Java tooling → [Software tooling and templates](../domains/software/tooling.md)
- engineering-document tooling → [`tool.eng-docs`](https://github.com/brainboxemb/tool.eng-docs)

### Sites and experiments

Site repositories contain published web content or site experiments. Experiment repositories investigate technical choices without becoming normal project dependencies.

The maintained cross-project experiment/PoP records are under [experiments/](../experiments/README.md). The public experiment repositories themselves are listed canonically in `catalog.yml`, including the SCAD CI performance experiment and reusable Java CI architecture PoP.

See the [dashboard](../dashboard/README.md) for the complete current public set and live status.

## External source forks

Some experiments need a retained fork of a third-party repository so upstream
history, licensing and exact source provenance remain visible.

Use:

```text
fork.<upstream-owner>.<upstream-repository>
```

with owner and repository normalized to lowercase for the brainboxemb repository
name. For example:

```text
AndyLevesque/QuackWorks
    -> brainboxemb/fork.andylevesque.quackworks
```

Including the upstream owner avoids collisions when unrelated projects use the
same repository name.

A fork has a narrow role:

- preserve the GitHub fork relationship and upstream history;
- retain upstream licence and attribution;
- provide a stable brainboxemb-side exact revision for an experiment;
- stay close to upstream instead of becoming the experiment or product owner.

Experiment fixtures, adapters and qualification evidence belong in the
corresponding `exp....` repository. Product-specific implementation belongs in
its production repository. If an experimental upstream patch is required, keep
it explicit and separable from the experiment's own geometry.

Only add a fork to `catalog.yml` after the public fork actually exists.

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
