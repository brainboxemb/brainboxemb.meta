# Migration 005 — simplify the SCAD execution architecture

Status: **migration execution in progress — template/reference migration complete; clamps canary next**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this folder exists

Migration 005 changes the shared SCAD execution model from a lifecycle-heavy Moon configuration into a capability-oriented model that is easier to understand and uses hosted compute more proportionately.

The design phase is finished. Shared runtime/query/SCAD-tool foundations are released and the template/reference consumer has completed the new model. The migration is now in **canary qualification**, starting with `lib.scad.clamps`.

## Start here

For normal migration work, read these in this order:

| Document | Role | Read it when... |
| --- | --- | --- |
| [01 — Change request](01-change-request.md) | Scope and fixed intent | You need the migration goal and boundaries. |
| [05 — Validated target architecture](05-target-architecture.md) | Selected technical design | You need the Moon/SCons/runtime/lifecycle model. |
| [06 — Implementation plan](06-implementation-plan.md) | Active execution order | You need the next owner step and its evidence gate. |

Earlier design-history documents (`02`–`04`) explain how the selected architecture was reached. Supporting evidence (`10`–`20`) records measurements and validation for specific decisions.

## Selected architecture in one view

```text
GitHub Actions
  exact source/base, credentials, hosted lifecycle
        |
        v
Moon on host
  determine affected SCAD capabilities once
  none -> stop before CAD image/runtime
        |
        v
one capability-appropriate SCAD runtime
  Moon executes or restores required whole capabilities
        |
        +-- tool.scad-project capability command
               |
               +-- direct execution, or
               +-- SCons fine-grained targets when configured
        |
        v
host finishing/publication
  current source/tool/run information
  compact retained evidence
  isolated Build/Verification publication
```

The maintainer-facing capability vocabulary is deliberately small:

```text
scad.build   presentation renders, when the repository has them
scad.docs    design documentation
scad.verify  Verification
```

Generic task commands, cache policy and standard output boundaries belong in shared `tool.scad-project` policy, not copied lifecycle topology in every consumer.

Source-affected capabilities and publication-safe materialization are related but not identical: an unchanged contributor may be hydrated when required to publish a complete replacement tree. That work remains non-affected and its cost is counted in canary measurements.

## Released shared foundations

Current immutable foundations for consumer rollout:

- `docker.scad-toolchain v0.5.0` — focused OpenSCAD and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from one Moon query;
- `tool.scad-project v0.14.2` — inherited capabilities, configuration consistency, runtime/cache selection and one-runtime lifecycle.

`v0.14.2` supersedes the original Step-3 `v0.14.0` release after Step-4 integration found and fixed two owner-side defects: clean hosted-Python planner installation and the correct Moon location for inherited capability selection.

## Template/reference result

Migration Step 4 is complete:

- owner: `brainboxemb/template.scad-project`;
- PR #37 merged as `cf3da65943968a42f3a0199cb682b1c74f452ee9`;
- full integration run `35020468894` green on `tool.scad-project v0.14.2`;
- full/dual runtime selected from PythonSCAD configuration;
- normal + Verification SCons cache paths exercised;
- docs/build/verify capabilities materialized in one Docker runtime;
- Build and Verification publication succeeded;
- normal Actions retention stayed compact rather than duplicating complete output trees.

## Current execution phase

The next owner step is **Step 5 — `brainboxemb/lib.scad.clamps`**, qualifying the dual-runtime/direct-engine canary.

After clamps, `lib.scad.hub75` qualifies the focused OpenSCAD/SCons mode. Downstream consumers follow only after both canaries are proven; the real HUB75 display-frame project remains deliberately later.

Do **not** infer current repository adoption only from migration documents. During rollout, each owner repository remains authoritative for its exact current pins and evidence.

The durable post-migration explanation of the shared SCAD architecture belongs under [`domains/scad/`](../../domains/scad/). This folder remains the traceable change/evidence record.
