# SCAD technical architecture

Status: **current shared architecture — Migration 005 rollout is still in progress**

## Why this page exists

This page is the durable technical explanation of the shared SCAD project architecture. Read it when you want to understand how GitHub Actions, Moon, `tool.scad-project`, SCons and the SCAD runtime fit together, or what a normal current-generation consumer is expected to configure.

You should **not** need to read a migration folder or old chat history to understand the intended model. Migration records explain how decisions were reached; this page explains the architecture itself.

During Migration 005, not every repository has adopted every part of this model yet. An individual repository remains authoritative for the exact tool and image versions it currently pins.

## Architecture at a glance

```text
GitHub Actions host
  exact source/base, event context, credentials
        |
        v
Moon on host
  determine affected SCAD capabilities once
  none -> stop before CAD image/runtime
        |
        v
one capability-appropriate SCAD runtime
  Moon executes or restores affected whole capabilities
        |
        +-- tool.scad-project capability command
               |
               +-- direct execution, or
               +-- SCons targets when configured
        |
        v
host finishing/publication
  current source/tool/run information
  compact retained evidence
  generated-output publication
```

The normal resource model is one heavy hosted runner and one CAD runtime. Avoiding work is preferred over duplicating runners just to shorten the stopwatch.

## Maintainer-facing capabilities

Moon is intentionally used at a coarse level. A consumer should describe real project capabilities rather than CI lifecycle mechanics.

The shared vocabulary is:

```text
scad.build   presentation renders, when the repository has them
scad.docs    design documentation
scad.verify  Verification
```

For example:

```text
lib.scad.clamps
  scad.docs
  scad.verify

lib.scad.hub75
  scad.build
  scad.docs
  scad.verify
```

A maintainer should not need consumer-local Moon tasks for generated indexes, current run metadata, publication staging, cache transport or synthetic CI roots.

## Why Moon exists

Moon has two distinct responsibilities in the shared SCAD architecture.

### 1. Change-impact selection before the CAD runtime

Before Docker is acquired, Moon compares the exact base and source revisions and answers which coarse SCAD capabilities are affected.

Conceptually:

```text
README-only change
  -> []
  -> no CAD image/runtime

presentation-only source change
  -> [scad.build]

verification-only source change
  -> [scad.verify]
```

The generic query belongs to `tool.git-project`. SCAD capability naming and lifecycle policy belong to `tool.scad-project`.

The affected calculation is performed once. The lifecycle should expose the relevant capability IDs from that one result rather than rerunning Moon separately for every capability.

When impact cannot be determined safely, the system fails conservative: required CAD work runs instead of being silently skipped.

### 2. Whole-capability output reuse

Moon may restore an entire source-derived capability result when its task identity matches a cached result.

This is intentionally coarser than SCons. Examples of a Moon cache unit are “all design documentation for this exact source/tool/config state” or “this Verification capability result”, not an individual PNG or STL target.

Task identity must contain only stable source/tool/config inputs. Generated runtime files or current GitHub run information must not participate in that identity.

In particular, avoid broad inputs such as:

```text
tools/tool.scad-project/**
```

because generated Python `__pycache__/*.pyc` files can appear below that tree and make identical source produce different task hashes. Shared policy uses explicit source-controlled tool inputs instead.

## Shared Moon task inheritance

Standard SCAD Moon task policy is owned by the pinned `tool.scad-project` dependency, not copied into every consumer.

The shared task definitions own things that are the same across normal consumers:

- capability command;
- stable common project/tool inputs;
- standard output boundaries;
- Moon cache policy.

A consumer inherits that policy from its pinned tool revision, conceptually with one stable link such as:

```yaml
extends: '../../tools/tool.scad-project/moon/tasks/scad.yml'
```

The consumer then selects only the capabilities it actually has and adds project-specific impact inputs. A reduced consumer model looks conceptually like:

```yaml
workspace:
  inheritedTasks:
    include:
      - scad.docs
      - scad.verify

tasks:
  scad.docs:
    inputs:
      - openscad/**
      - pythonscad/**

  scad.verify:
    inputs:
      - openscad/**
      - pythonscad/**
      - test/**
      - vrf/**
```

A repository with presentation renders additionally includes `scad.build` and its project-specific render inputs.

The exact effective task can be inspected with Moon rather than inferred from several files:

```text
moon task <project>:scad.docs --json
moon task <project>:scad.build --json
moon task <project>:scad.verify --json
```

## `project.scad.yml` and Moon describe different things

The two configuration views are complementary.

`project.scad.yml` describes SCAD-domain intent, such as:

- OpenSCAD and/or PythonSCAD configuration;
- presentation render configuration;
- Verification commands/output root;
- direct versus SCons build engine;
- Build/Verification roots and publication policy.

The reduced Moon configuration describes:

- which coarse capabilities exist;
- which project-specific sources affect each capability;
- exceptional output overrides when the project intentionally departs from shared defaults.

Shared validation should reject contradictions instead of allowing the two views to drift. Examples:

- configured presentation renders should agree with `scad.build`;
- configured Verification should agree with `scad.verify`;
- PythonSCAD configuration requires the full/dual runtime;
- `build_engine: scons` controls whether SCons cache handling is applicable;
- non-standard output roots need compatible Moon output ownership.

## Moon versus SCons

Moon and SCons operate at different levels.

```text
Moon
  Which whole repository capability is affected?
  Can the complete capability output be reused?

SCons, only when configured
  Within an executing capability, which individual CAD targets
  actually need rebuilding or can be restored?
```

SCons is therefore optional.

A direct project such as the current clamps reference should not restore or save SCons object caches merely because the ecosystem supports SCons elsewhere.

A SCons-enabled project such as HUB75 can use target-level reuse inside an executing capability. If Moon restores the entire capability, SCons does not need to run for that capability at all.

## SCAD runtime profiles

`docker.scad-toolchain` owns one related image family from one multi-stage source.

### OpenSCAD-focused profile

Contains the normal OpenSCAD production contract, including:

- OpenSCAD;
- BOSL2;
- documentation tooling;
- Pillow/watermark support;
- SCons;
- required system/runtime tools.

Released package:

```text
ghcr.io/brainboxemb/scad-toolchain-openscad:<version>
```

### Full/dual profile

Contains the OpenSCAD profile plus PythonSCAD-specific support:

- PythonSCAD;
- pybosl2;
- Shapely;
- related runtime dependencies.

Compatibility package:

```text
ghcr.io/brainboxemb/scad-toolchain:<version>
```

The two-profile family was first released as `v0.5.0`. The full profile is externally tested as a functional superset of the OpenSCAD profile.

Runtime choice is based on effective project configuration/capabilities, never on a repository-name allowlist:

```text
OpenSCAD-only
  -> focused OpenSCAD runtime

OpenSCAD + PythonSCAD
  -> full/dual runtime
```

## Source-derived output versus current-run information

Reusable CAD output and current CI context are deliberately separate.

Moon source identity may depend on stable items such as:

- repository source;
- project configuration;
- pinned tool source/version;
- capability-specific project inputs.

It must not depend on invocation-specific values such as:

- GitHub run ID;
- PR number;
- current ref name;
- publication branch/context.

After a capability is executed or restored, host finishing adds truthful current source/tool/run information required for publication and auditability.

This separation allows reuse without publishing stale run metadata.

## Cache and output layers

The architecture has deliberately different reuse/output scopes:

| Layer | Scope | Purpose |
| --- | --- | --- |
| Moon | complete source-derived capability output | cross-run whole-capability reuse and change-impact |
| SCons, when configured | individual CAD targets inside a capability | fine-grained rebuild/cache decisions |
| GitHub Actions cache transport | Moon/SCons cache directories between disposable runners | move reusable cache state between runs |
| generated-output branches | normal generated Build/Verification output | durable published project output |
| release artifacts | exact-source cross-job hand-off | required by the separate release Build/Verify/finalize lifecycle |

Normal successful CI does not need to retain a second complete copy of already-published Build/Verification trees as Actions artifacts by default. Compact decision/orchestration evidence remains useful and is retained separately.

## Publication stays outside the CAD runtime

Generated-output publication needs GitHub credentials and current repository context, not OpenSCAD/PythonSCAD dependencies.

Therefore publication happens on the host after CAD work. Build and Verification remain separate logical outputs. Their publisher instances use isolated temporary Git repositories, so they may overlap on the same runner when useful without adding another hosted VM.

## Repository ownership boundaries

| Repository/layer | Responsibility |
| --- | --- |
| `tool.git-project` | Generic Moon runtime, VCS base/head handling, changed/affected query and generic repository/publication primitives. |
| `tool.scad-project` | Shared SCAD capability tasks, project/config validation, runtime selection, SCAD lifecycle, applicable cache handling and finishing orchestration. |
| `docker.scad-toolchain` | Reproducible OpenSCAD-focused and full/dual CAD runtime images. |
| `docker.scad-toolchain.test` | External functional qualification of the runtime image family. |
| consumer repository | Project source, `project.scad.yml`, capability selection and project-specific impact rules/verification content. |
| `brainboxemb.meta` | Durable cross-project explanation plus migration/decision records; never a runtime dependency. |

## Newer and older project setups

The SCAD/CAD collection contains several generations of project setup:

```text
classic standalone
    project-local OpenSCAD source
    no shared project workflow

classic shared-actions
    project source
        -> brainboxemb.github.actions

current shared tooling
    project source/configuration
        -> tool.git-project
        -> tool.scad-project
        -> docker.scad-toolchain
```

**Classic** describes an older setup. It does not mean a project is broken or should be migrated automatically.

## CAD engine and project setup are different things

The CAD engine tells you what actually evaluates a design:

- OpenSCAD;
- PythonSCAD;
- or both.

The project setup tells you how the repository is organised and built:

- classic standalone;
- classic shared-actions;
- current shared project tooling.

Do not infer the CAD engine only from a repository name. Use its actual project configuration and source.

## Projects use their dependencies directly

A project includes the tools and reusable libraries it actually needs. It does not use `brainboxemb.meta` as a runtime dependency.

Conceptually:

```text
project
    ├── shared project tooling
    └── reusable libraries it needs
```

For example, a HUB75 project can use `lib.scad.hub75` directly without going through this meta repository.

## Migration and implementation status

The architecture described above is the validated target of [Migration 005](../../migrations/005-scad-execution-architecture/README.md). The runtime image family is already released; shared tooling and consumer repositories are being migrated owner by owner.

Use the migration folder only when you need the change request, historical reasoning, validation evidence or rollout status. This page is the durable architecture reference.

## Where information should live

Use this rule of thumb:

- **project repository** — actual design, dimensions, project configuration and project-specific documentation;
- **library repository** — reusable geometry/API, library tests and releases;
- **tool repository** — shared build/project behaviour implemented by that tool;
- **brainboxemb.meta** — overview, navigation, common architecture explanations and cross-project migration records.

## Historical note

The broad SCAD overview was originally kept in `tech.scad`, while a smaller current-stack integration view was coordinated through `meta.scad-projects`. Those useful concepts have been consolidated here; both older repositories are now private archives.
