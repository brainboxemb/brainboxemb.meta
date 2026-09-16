# Migration 005 — simplify the SCAD execution architecture

Status: **migration execution in progress — template and both canaries complete; downstream rollout next**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this folder exists

Migration 005 changes the shared SCAD execution model from a lifecycle-heavy Moon configuration into a capability-oriented model that is easier to understand and uses hosted compute more proportionately.

The design phase and canary qualification are complete. Shared foundations are released, the template/reference consumer is released, and both representative library execution modes are proven on migrated `main`. The migration now moves into downstream consumer rollout.

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

Source-affected capabilities and publication-safe materialization are related but not identical: an unchanged contributor may be hydrated when required to publish a complete replacement tree. That work remains non-affected and its cost is counted in measurements.

## Released shared foundations

Current immutable foundations for the completed template/canary rollout:

- `docker.scad-toolchain v0.5.0` — focused OpenSCAD and full/dual runtime profiles;
- `tool.git-project v0.2.8` — complete affected-task list from one Moon query;
- `tool.scad-project v0.14.3` / `b86b2be325f64847b8d91b7f2596bfd4e4ffb7f2` — inherited capabilities, configuration consistency, runtime/cache selection, one-runtime lifecycle and stable optional-output handling.

The original Step-3 `v0.14.0` release was followed by integration-driven patches v0.14.1, v0.14.2 and v0.14.3. Shared defects were fixed in the owner repository rather than hidden in consumer workarounds.

## Template/reference result

Step 4 is complete:

- owner: `brainboxemb/template.scad-project`;
- Migration implementation PR #37 merged as `cf3da65943968a42f3a0199cb682b1c74f452ee9`;
- full integration run `35020468894` qualified the full/dual + SCons three-capability path;
- PR #39 replaced brittle individual-file Moon inputs with source-family boundaries;
- **v0.0.4** released from `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9` with Build, Verification, STL and checksum assets.

## Canary results

### `lib.scad.clamps` — dual runtime + direct engine

Step 5 is complete:

- PR #16 merged as `a44d7bdfdb3407959b5d96bef654568367e0f43c`;
- migrated `main` run `35065375255` green;
- full/dual runtime selected;
- direct engine selected;
- normal and Verification SCons transport both skipped;
- README-only qualification run `35065514152` skipped planner setup, all caches, runtime pull, Docker materialization, finishing and publication.

### `lib.scad.hub75` — focused OpenSCAD + SCons

Step 6 is complete:

- PR #29 merged as `ea75cee1fa83310bc2ba2ad1ce565ef81ac7f523`;
- migrated `main` run `35065383879` green;
- OpenSCAD-focused runtime selected;
- normal SCons transport enabled;
- Verification SCons transport correctly absent for command-only verification;
- README-only qualification run `35065524524` skipped planner setup, all caches, runtime pull, Docker materialization, finishing and publication.

## Current execution phase

The next migration phase is **Step 7 — downstream SCAD consumers**. Each consumer remains owner-authoritative for its exact pins, capability set and publication/verification semantics.

Do not automatically enumerate individual `.scad` or verification files in `moon.yml`; use maintainable source-family capability boundaries unless a genuinely exceptional stable file boundary is required.

The real HUB75 display-frame project remains deliberately later in the downstream rollout rather than being assumed to be the first consumer.

## Parallel hardening track

`tool.scad-project#60` tracks a follow-up improvement discovered while reviewing canary evidence:

- make future tool-gitlink upgrade preflight robust when BASE references an older shallow submodule commit;
- make retained orchestration logs easier to navigate from generated output;
- preserve durable UTC timing/duration evidence for major workflow phases instead of depending on temporary GitHub Actions UI timing.

This follow-up does **not** reopen the completed v0.14.3 library canaries. Its qualification order is deliberately:

```text
tool.scad-project
        |
        v
template.scad-project first
        |
        v
only then consider repinning existing libraries/other consumers
```

Do **not** infer current repository adoption only from migration documents. During rollout, each owner repository remains authoritative for its exact current pins and evidence.

The durable post-migration explanation of the shared SCAD architecture belongs under [`domains/scad/`](../../domains/scad/). This folder remains the traceable change/evidence record.
