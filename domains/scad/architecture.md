# SCAD technical architecture

Status: **current shared architecture — Migration 005 complete**

## Why this page exists

This page is the durable explanation of the current shared SCAD project architecture. Read it to understand how GitHub Actions, Moon, `tool.scad-project`, SCons and the SCAD runtime fit together.

You should not need migration history to use the architecture. The Migration-005 folder remains available for design history, measurements and rollout evidence.

## Architecture at a glance

```text
GitHub Actions host
  exact source/base, event context, credentials
        |
        v
one Moon affected query
  no affected SCAD capability
        -> stop before planner/image/runtime
        |
        v
SCAD execution plan
  validate project/capabilities
  choose runtime profile
  choose only applicable cache transport
        |
        v
at most one CAD runtime
  Moon executes or restores required whole capabilities
        |
        +-- tool.scad-project capability command
               |
               +-- direct execution, or
               +-- SCons targets when configured
        |
        v
host finishing/publication
  exact current source/tool context
  durable orchestration evidence
  Build/Verification publication
```

Normal current-generation production uses one hosted job and at most one SCAD runtime. Avoiding work and reusing work are preferred over adding heavy parallel runners merely to improve stopwatch time.


## Current released baseline

At Migration-005 closeout the shared baseline is:

```text
docker.scad-toolchain   v0.5.0
tool.git-project        v0.2.8
tool.scad-project       v0.14.7
```

Exact `tool.scad-project v0.14.7` source:

```text
3935e5f86fe309b8908a05554f7ada336a6d6886
```

A consumer expresses the released SCAD tool version semantically in `project.yml` and in reusable-workflow callers, for example:

```yaml
dependencies:
  - name: tool.scad-project
    path: tools/tool.scad-project
    ref: v0.14.7
```

```yaml
uses: brainboxemb/tool.scad-project/.github/workflows/project-production.yml@v0.14.7
```

The committed submodule gitlink remains the exact resolved source identity. This gives maintainers readable release intent without losing reproducibility.

## Maintainer-facing capabilities

Moon is intentionally coarse at repository level. Current shared capabilities are:

```text
scad.docs    design documentation
scad.build   presentation renders, when present
scad.verify  Verification
```

Consumers should describe real project capabilities, not duplicate lifecycle mechanics such as indexes, publication staging, cache transport or synthetic CI roots.

Shared task definitions come from the pinned `tool.scad-project` gitlink, conceptually:

```yaml
# .moon/tasks/scad.yml
extends: '../../tools/tool.scad-project/moon/tasks/scad.yml'
```

Root `moon.yml` selects the capabilities the project actually exposes and adds only project-specific source-family impact rules.

The exact effective inherited task can be inspected with Moon rather than inferred from several files:

```text
moon task <project>:scad.docs --json
moon task <project>:scad.build --json
moon task <project>:scad.verify --json
```

## `project.scad.yml` and Moon describe different things

The two views are complementary.

`project.scad.yml` describes SCAD-domain intent, including:

- OpenSCAD and/or PythonSCAD configuration;
- presentation render/export configuration;
- Verification commands and output roots;
- direct versus SCons build engine;
- publication-related SCAD paths and policy.

Moon describes repository execution boundaries:

- which coarse SCAD capabilities exist;
- which project source families affect those capabilities;
- normal inherited output/cache behaviour;
- exceptional project-specific output overrides when needed.

Shared validation should reject contradictions rather than allow the two descriptions to drift. Examples include:

- configured presentation renders should agree with `scad.build`;
- configured Verification should agree with `scad.verify`;
- PythonSCAD configuration requires the full/dual runtime;
- `build_engine: scons` controls whether normal SCons transport is applicable;
- direct projects do not transport SCons caches;
- Verification-SCons transport exists only when real verification render/export targets use it;
- non-standard output roots require compatible Moon output ownership.

## Moon has two jobs

### Change-impact selection before CAD

`tool.git-project` owns the generic exact base-to-source Moon query. `tool.scad-project` owns the SCAD capability interpretation.

Examples:

```text
README-only change
  -> []
  -> no planner, image or CAD runtime

presentation source change
  -> [scad.build]

verification-only source change
  -> [scad.verify]
```

If comparison context cannot be established safely, the system fails conservative: required work runs rather than being silently skipped.

Tool-gitlink upgrade PRs are also handled precisely. The production workflow makes the exact base `tools/tool.scad-project` gitlink commit available before the Moon query, so a shallow checkout does not fall back merely because an older tool commit is initially absent.

### Whole-capability reuse

Moon can restore complete source-derived capability output when stable source/tool/config identity matches a cached result.

Task identity deliberately excludes invocation-specific or generated state such as:

- GitHub run ID;
- PR number;
- publication destination;
- generated Python bytecode.

This is why broad inputs such as `tools/tool.scad-project/**` are avoided: generated runtime files must not destabilise source identity.

## Affected versus materialized capabilities

What changed and what must exist locally for safe publication are different questions.

For example, if docs and presentation output both belong to one complete Build tree:

```text
affected
  scad.docs

materialize before complete Build replacement
  scad.docs
  scad.build
```

The unchanged `scad.build` contributor may be hydrated through Moon so replacing the generated Build branch does not delete unchanged files. It remains non-affected work and its cost is still counted.

Verification is its own publication family and is not materialized merely to complete Build.

## Moon versus SCons

Moon and SCons work at different levels:

```text
Moon
  repository capability impact
  whole-capability reuse

SCons, only when selected by project configuration
  individual CAD target dependency/rebuild/cache decisions
```

SCons is optional.

Examples from the qualified consumers:

- `lib.scad.clamps` uses the direct engine and transports no normal or Verification SCons cache;
- `lib.scad.hub75` uses SCons for normal CAD work and retains useful normal SCons transport;
- command-only Verification does not get a Verification-SCons cache merely because normal Build uses SCons.

If Moon restores the complete capability, SCons does not need to execute for that capability at all.

## Runtime profiles

The normal SCAD execution/publication runtime is the related
`docker.scad-toolchain` image family.

### OpenSCAD-focused

```text
ghcr.io/brainboxemb/scad-toolchain-openscad:<version>
```

Contains the normal OpenSCAD production contract: OpenSCAD, BOSL2,
documentation tooling, watermark support, SCons and required runtime/system
tools.

### Drawing/publication

```text
ghcr.io/brainboxemb/scad-toolchain-drawing:<version>
```

Extends the OpenSCAD-focused contract with drawsvg and Inkscape for scripted
technical-drawing composition and deterministic SVG/PNG/PDF publication.

### Full/dual

```text
ghcr.io/brainboxemb/scad-toolchain:<version>
```

Adds PythonSCAD/pybosl2/Shapely support.

Runtime selection comes from effective project configuration, never a
repository-name allowlist:

```text
OpenSCAD-only                 -> focused runtime
drawing/publication           -> drawing runtime
OpenSCAD + PythonSCAD         -> full/dual runtime
```

The Migration-005 controlled qualification measured the focused image at about
27% fewer compressed bytes than the then-current full image. Later drawing
capabilities remain opt-in for the same reason: normal consumers should not
carry unrelated heavy tooling.

## CAD engine and project setup are different things

The CAD engine says what evaluates the design:

- OpenSCAD;
- PythonSCAD;
- or both.

The project setup says how the repository is organised and built:

- classic standalone;
- classic shared-actions;
- current shared project tooling.

Do not infer the CAD engine from the repository name or from whether it is a classic/current project. Use the actual project configuration and source.

## Projects use dependencies directly

A project uses the tools and reusable libraries it actually needs. `brainboxemb.meta` is documentation/coordination, never a runtime dependency.

Conceptually:

```text
project
    ├── shared project tooling
    └── reusable libraries it needs
```

For example, a HUB75 project can depend directly on `lib.scad.hub75`; it does not route that dependency through the meta repository.

## Host finishing and exact provenance

Reusable source-derived output stays separate from current invocation context. After capability execution or hydration, host finishing adds current publication/index/provenance information.

The resolved exact source SHA is exported from preflight into host finishing. For pull requests this prevents `publication-info.txt` from accidentally using GitHub's synthetic merge SHA.

Qualified v0.14.7 reference output shows the same exact source revision in:

- `publication-info.txt`;
- `orchestration/run-context.json`;
- Moon `materialization.json`;
- producer execution evidence.

## Durable orchestration evidence

Normal affected output retains navigable current-run evidence rather than relying only on temporary GitHub Actions UI logs.

Generated Build/Verification snapshots include:

- coarse workflow timing in `orchestration/timings.json`;
- readable timing table in generated README navigation;
- Moon materialization records;
- links/copies of retained raw Moon/producer logs;
- current run/source context.

The final template v0.14.7 qualification measured **41.059 s to prepared Build snapshot**, including 16.767 s runtime pull and 13.072 s capability materialization.

## Cache and output layers

| Layer | Scope | Purpose |
| --- | --- | --- |
| Moon | complete source-derived capability output | whole-capability impact/reuse |
| SCons, when configured | individual CAD targets inside a capability | fine-grained dependency/rebuild/cache decisions |
| GitHub Actions cache | Moon/SCons state between disposable runners | transport reusable cache state |
| generated-output branches | normal Build/Verification output | durable browsable project output |
| release artifacts | complete exact-source cross-job hand-off | coordinated release Build/Verify/finalize lifecycle |

Normal successful production does not upload another complete copy of Build/Verification output merely for retention. Compact orchestration evidence remains because it serves a different audit/debugging purpose.

Release remains intentionally different: separate release jobs genuinely require complete Build/Verification artifacts as cross-job hand-off.

## Publication stays outside CAD

Publication needs GitHub credentials and repository context, not CAD dependencies. It therefore runs on the host after the CAD runtime exits.

Build and Verification are separate logical outputs. Their isolated publishers can overlap on the same runner without requiring another hosted VM.

Only publication families with source-affected capabilities are republished. Hydrating an unchanged contributor to make a changed family complete does not mark unrelated families as changed.

## Resource model and measured result

Final normal resource model:

```text
hosted production jobs       1
Moon affected queries        1
CAD runtime processes        0 or 1
runtime profile              configuration driven
SCons transport              only where useful
complete normal artifacts    0 duplicate copies by default
```

Unrelated README-only probes on HUB75, clamps and the template all started **zero CAD runtime** and skipped planner/cache/runtime/materialization/finishing/publication. Hosted-job elapsed time was approximately 7.6–9.9 s rather than the aspirational 4–6 s because fixed Actions setup and generic Moon-runtime restore/query remain.

Affected canary measurements were approximately:

- clamps full/direct: 41.9 s;
- HUB75 focused/SCons warm/cached: 32.2 s.

Those meet the Migration-005 affected latency envelopes while retaining one-heavy-runner resource use.

The remaining unrelated-change preflight latency is tracked as generic `tool.git-project` issue #26. It is an optimisation opportunity, not an open SCAD architecture requirement.

## Repository ownership boundaries

| Repository/layer | Responsibility |
| --- | --- |
| `tool.git-project` | Generic Moon runtime, VCS base/head handling, affected query and generic repository/publication primitives. |
| `tool.scad-project` | Shared SCAD capabilities, configuration validation, runtime/cache selection, normal/release SCAD lifecycle and finishing orchestration. |
| `docker.scad-toolchain` | Reproducible focused/drawing/full SCAD runtime image family. |
| `docker.scad-toolchain.test` | External functional qualification of the SCAD runtime image family. |
| consumer repository | Project source/configuration, capability selection, project-specific source impact and verification content. |
| `brainboxemb.meta` | Durable portfolio/architecture explanation and migration evidence; never a runtime dependency. |

## Current-generation versus classic project setup

The public SCAD/CAD collection still contains different project-infrastructure generations:

```text
classic standalone
    project-local source
    no current shared project workflow

classic shared-actions
    project source
        -> brainboxemb.github.actions

current shared tooling
    project source/configuration
        -> tool.git-project
        -> tool.scad-project
        -> docker.scad-toolchain
```

**Classic does not mean broken or automatically pending migration.**

Migration 005 completed the repositories currently classified in `repositories/catalog.yml` with `project_infrastructure.provider: tool.scad-project`:

- `template.scad-project`;
- `lib.scad.clamps`;
- `lib.scad.hub75`;
- `2026-009-01.cad.HUB75-display-frame`.

Moving classic projects to the current tooling generation would be a separate cross-project change with its own scope and evidence.

## Where information should live

- **project repository** — actual design, dimensions, project configuration and project-specific documentation;
- **library repository** — reusable geometry/API, library tests and releases;
- **tool repository** — shared behaviour implemented by that tool;
- **brainboxemb.meta** — overview, navigation, common architecture explanation and cross-project migration records.

For historical reasoning and measured rollout evidence, see [Migration 005](../../migrations/005-scad-execution-architecture/README.md).
