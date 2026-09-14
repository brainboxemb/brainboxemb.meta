# Change request — unify the SCAD repository execution model

Status: **approved for execution after proposal merge**

Tracking issue: [#49](https://github.com/brainboxemb/brainboxemb.meta/issues/49)

Related parked experiment: [#51 — evaluate Moon as SCAD target engine](https://github.com/brainboxemb/brainboxemb.meta/issues/51)

## Requested change

Current SCAD repositories should use one understandable CI lifecycle whether the repository is a project or a reusable library.

The target model is:

```text
lightweight host preflight
        |
        | Moon affected: is SCAD production required?
        |
        +-- no --> no SCAD container
        |
        `-- yes --> one SCAD production job/container
                       |
                       +-- Build domain
                       +-- Verify domain
                       +-- generated design/docs when affected
                       +-- producer/domain/materialization evidence
                                |
                                v
                     lightweight publication jobs
```

A library may differ from a project in source layout, verification content, release content and downstream qualification. It should not use a different orchestration model merely because it evolved earlier.

## Why this change is needed

There are currently two execution models.

`template.scad-project` and `2026-009-01.cad.HUB75-display-frame` use one `SCAD production` job with a Moon repository graph.

`lib.scad.clamps` and `lib.scad.hub75` use separate reusable Build and Verify workflows. Each starts its own runner/container, checks out the repository and restores its own cache.

That difference has no demonstrated library-specific reason.

On qualified `lib.scad.clamps` main:

- Build took about 37 seconds;
- Verify took about 32 seconds;
- container initialization took about 17 and 18 seconds respectively;
- the configured Build producer itself completed within timestamp resolution;
- the Verify producer took about 2 seconds.

The two jobs run in parallel, so wall-clock time is not their sum. But the repository still pays for two heavy setups for a very small amount of SCAD work.

There is a second, more important inefficiency: current project workflows declare the SCAD image with GitHub Actions `container:` at job level. GitHub therefore pulls/starts the approximately 20-second SCAD container before repository impact is known. A README-only change currently pays that cost even though no CAD output can be affected.

## Decisions already made

### 1. Build and Verify stay logically independent

`tool.scad-project v0.10+` deliberately separated normal Build from Verify. Migration 004 must preserve that contract.

The following concepts remain independent:

```text
scad.build
scad.verify
```

Normal CI requests both through an aggregate lifecycle. That does **not** mean Verify depends on Build.

The current template dependency:

```text
scad.verify -> scad.build
```

must therefore be removed unless a concrete consumer explicitly needs Build output as a verification input.

The intended generic graph is conceptually:

```text
                 +--> scad.build  ----------------+
scad.ci -------->|                                 +--> publication/evidence
                 +--> scad.verify ----------------+
```

Generated design/document tasks keep only their real dependencies.

### 2. One GitHub job is not one domain

A GitHub job/container boundary is an execution choice, not a domain boundary.

Build and Verify may share one heavy job while retaining:

- separate commands;
- separate SCons caches;
- separate decision reports;
- separate execution evidence;
- separate output trees;
- separate publication branches;
- explicit Build-only and Verify-only invocation where needed.

### 3. Moon is the repository-level orchestration choice for Migration 004

Migration 004 will use Moon as the common repository-level task/affected layer for the current SCAD generation.

Reasons:

- it is already the qualified repository graph in the template and real HUB75 frame;
- it models task inputs and graph relations;
- affected-state can be queried from VCS changes;
- it provides whole-task cache/hydration and materialization evidence;
- using it for libraries removes a second repository-orchestration model instead of inventing a new combined workflow engine.

`lib.scad.clamps` is the reference library that must prove this remains proportionate for a small repository.

If clamps exposes a concrete library-specific reason this model is unsuitable, pause and reconsider before changing `lib.scad.hub75`.

### 4. SCons remains the SCAD target engine in this migration

Migration 004 does **not** replace SCons.

The current `tool.scad-project` dependency scanner follows static OpenSCAD `use`/`include` dependencies transitively and tracks static `import`/`surface` assets per target. SCons consumes those dependencies for fine-grained target invalidation/cache decisions.

Whether fine-grained Moon tasks can replace that layer is a separate experiment tracked by meta issue #51.

For this migration the boundary is:

```text
Moon
  repository/task affected + materialization
        |
        +--> Build producer
        |       `--> SCons target decisions
        |
        `--> Verify producer
                `--> SCons target decisions
```

## Pre-container affected gate

Avoiding unnecessary SCAD-container startup is a **completion criterion**, not a later optional optimization.

Moon v2 has the required concepts:

- task affected-state is based on declared task `inputs`;
- graph relations can propagate affected state;
- `moon query changed-files` supports explicit base/head revisions;
- affected queries expose the affected project/task set without executing SCAD producers.

`tool.git-project` owns the generic Moon/VCS preflight interface.

The CI shape must be:

```text
preflight job (host Ubuntu)
  checkout enough VCS history/configuration
  bootstrap/restore pinned Moon runtime
  determine changed files for the event
  ask Moon which production tasks are affected
  emit run_scad=true|false and diagnostic evidence

scad job
  if: preflight.run_scad == true
  start SCAD container
  restore producer caches
  execute/hydrate affected production graph
  validate/stage evidence

publication jobs
  run only when new/current publication artifacts were produced
  no SCAD container
```

The preflight must use Moon's task inputs/graph. Do not introduce a second hand-maintained list such as `*.scad => build` in GitHub YAML.

### Event baseline rules

The implementation must make base/head selection explicit and test it.

At minimum:

- pull request: compare the PR base revision with the checked-out PR head;
- push to main: compare the previous main revision with current head;
- release/manual force: may deliberately request production even when the normal affected gate is empty, when exact release materialization is required.

The exact CLI form must be qualified with the pinned Moon version before being treated as contract. Do not copy unverified command examples into consumer workflows.

### Required behavior

A root `README.md`-only PR must result in:

- preflight success;
- `run_scad=false`;
- **no SCAD container job startup**;
- no misleading fresh producer evidence.

A relevant source/configuration/tooling change must result in:

- preflight success;
- `run_scad=true`;
- exactly one normal SCAD container startup;
- Moon/SCons performing their respective decisions.

When preflight cannot determine impact safely, fail conservative: run the SCAD job rather than silently skipping it.

## What is genuinely library-specific

A library may legitimately differ in:

- source tree layout;
- reusable API examples;
- verification commands and fixtures;
- release contents;
- downstream consumer qualification.

These differences should live in repository configuration and verification content.

They do not currently justify:

- two SCAD containers;
- two checkouts;
- separate normal CI triggers for Build and Verify;
- a different repository orchestration engine.

`template.scad-project` remains the reference project. `lib.scad.clamps` becomes the practical reference library.

Do not create `template.scad-lib` during the first slice. Create one later only if the clamps/HUB75 work proves that new libraries repeatedly need the same meaningful library-specific bootstrap/configuration that is inappropriate in the project template.

## Publication ownership

Publication does not require OpenSCAD/PythonSCAD.

The common flow should therefore stage/upload Build and Verify publication material in the heavy job and publish it from lightweight host jobs.

This is already the better shape in the template/frame and should become the shared behavior.

## Shared tooling ownership

### `tool.git-project`

Owns generic repository/Moon mechanics:

- pinned Moon runtime;
- VCS base/head changed-file discovery;
- affected task query/preflight;
- portable Moon cache/materialization behavior;
- machine-readable preflight result/evidence.

It must not know SCAD target semantics.

### `tool.scad-project`

Owns SCAD production semantics and reusable CI shape:

- reusable SCAD production workflow;
- Build/Verify commands;
- SCons caches and target evidence;
- generic producer/evidence validation;
- staging of Build/Verify publication artifacts;
- calling the generic Moon preflight with the configured SCAD aggregate task.

### Consumers

Own only repository-specific configuration/tasks/verification expectations.

A consumer workflow should become a thin caller rather than containing a copied 200+ line production implementation.

## Implementation sequence

### Step 1 — generic Moon affected preflight

Owner: `tool.git-project`.

Implement and test a reusable capability that:

1. restores/bootstraps the pinned Moon runtime on the host;
2. accepts repository path, target/task scope and base/head context;
3. queries changed files and Moon affected state without executing producer commands;
4. returns at least `affected=true|false` plus diagnostics/evidence;
5. treats errors/uncertainty conservatively.

Qualification must include an actual Moon 2.5.4 integration test, not only mocked CLI output.

Release the tool before consumers depend on it.

### Step 2 — reference graph correction

Owner: `template.scad-project`.

- remove `scad.verify -> scad.build` unless demonstrated necessary;
- keep `scad.ci` as aggregate owner;
- review task inputs so Moon affected-state reflects real repository responsibilities;
- specifically ensure root reader documentation does not accidentally affect SCAD producer tasks unless its content is genuinely consumed.

Requalify Build-only, Verify-only and aggregate execution.

### Step 3 — shared SCAD production workflow

Owner: `tool.scad-project`.

Provide one reusable workflow with:

1. lightweight preflight job outside the SCAD container;
2. conditional single heavy SCAD production job;
3. separate normal/verification SCons caches;
4. Moon aggregate/affected execution inside the container;
5. generic evidence validation/staging;
6. lightweight Build and Verify publication jobs.

Do not bake template-specific expected filenames into shared tooling.

Release the tool before rolling it out.

### Step 4 — template qualification

Owner: `template.scad-project`.

Replace its copied production mechanics with the released shared workflow.

Required scenarios:

- cold relevant change;
- unchanged/rehydration path;
- README-only PR: SCAD job absent/skipped before container creation;
- Build-only source impact;
- Verify-only source impact;
- Build and Verify explicit local/logical independence;
- aggregate production;
- publication from lightweight jobs.

### Step 5 — reference library qualification

Owner: `lib.scad.clamps`.

Move normal CI from separate Build and Verify heavy workflows to the common production workflow/Moon graph.

Measure before/after:

- job count;
- SCAD-container count;
- container startup time;
- checkout/bootstrap time;
- producer/orchestration time;
- cache/hydration result;
- generated evidence/publication;
- consumer configuration size.

Document in the library README why the common orchestration is used and what remains library-specific.

If this model is materially worse or requires artificial library configuration, stop before HUB75 and reassess.

### Step 6 — second library

Owner: `lib.scad.hub75`.

Apply the already-qualified library model without changing physical verification content such as SQ-01.

Requalify its richer Verify/publication behavior.

### Step 7 — real project requalification

Owner: `2026-009-01.cad.HUB75-display-frame` only if shared tooling/template changes affect its current production flow.

The frame validates that the final shared model still works for a realistic project; it should not drive generic design prematurely.

## Qualification matrix

| Scenario | Expected result |
| --- | --- |
| Root README-only PR | Host preflight runs; SCAD container does not start. |
| Unrelated repository metadata | No SCAD container unless configured task inputs genuinely consume it. |
| SCAD source changed | Preflight marks production affected; one SCAD container starts. |
| One transitive SCAD dependency changed | Production starts; SCons decides affected targets. |
| Build-only input changed | Build branch executes/materializes correctly; Verify is not forced by a stale dependency. |
| Verify-only input changed | Verify executes/materializes without normal Build being a semantic prerequisite. |
| Tool/config pin changed | Conservative production run with clear reason. |
| Cold production | Correct Build/Verify/evidence/publication from no useful cache. |
| Warm rerun | Correct Moon/SCons reuse without stale evidence being presented as current producer execution. |
| Preflight error/uncertainty | Production runs rather than being incorrectly skipped. |
| Release/manual exact materialization | Explicit force policy works and produces exact-source artifacts/evidence. |

## Completion criteria

Migration 004 is complete only when:

- the generic Moon affected preflight is released and qualified;
- the common reusable SCAD production workflow is released;
- `template.scad-project` uses it and README-only CI proves the SCAD container is skipped;
- `lib.scad.clamps` uses the same execution model with documented library-specific rationale;
- `lib.scad.hub75` is qualified on the chosen model;
- Build and Verify remain logically independent;
- publication occurs outside the SCAD container;
- a real project is requalified if shared changes require it;
- the final decision/rationale is documented in the affected repositories and retained in meta.

Moon replacing SCons is **not** a completion criterion; that question is parked in experiment #51.

## Stop conditions

Pause and reassess instead of pushing through the plan if:

- Moon affected-state cannot safely support a pre-container decision with the pinned/runtime-qualified version;
- task inputs must become so broad that README-only or unrelated changes still trigger production routinely;
- library-specific requirements make the common graph materially artificial;
- shared workflow extraction requires consumer-specific hard-coding;
- evidence can no longer distinguish producer execution from cache/materialization;
- the single-container model causes a material regression that cannot be addressed without destroying domain independence.
