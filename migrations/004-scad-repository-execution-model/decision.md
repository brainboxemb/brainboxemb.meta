# Migration 004 execution decision

The migration is active.

Selected direction:

- one recognizable SCAD production lifecycle across current projects and libraries;
- Moon for repository-level orchestration and affected/preflight decisions;
- SCons retained as the qualified fine-grained SCAD target engine;
- Build and Verify remain logically independent;
- host-side affected preflight before SCAD toolchain startup;
- README-only/unaffected work starts no SCAD container;
- affected normal CI uses exactly one immutable SCAD Docker execution environment;
- preflight, conditional `docker run`, validation/staging and publication should live in one host orchestrator job to avoid serial GitHub job/artifact handoffs;
- publication remains outside the SCAD container **process boundary** and occurs only after that container exits;
- publication credentials stay host-side and are not passed into the SCAD container.

`template.scad-project` is the reference project and `lib.scad.clamps` the reference library.

## Step-5 performance reassessment

Migration-004 experiment #53 compared the released multi-job topology, historical/cached host tooling and a single-host orchestration model.

Runtime conclusion:

- retain the immutable Docker SCAD toolchain; cached host OpenSCAD did not reproduce the Docker EGL/output behavior reliably;
- explicit Docker execution preserves the qualified toolchain and byte-identical reference output.

Workflow-topology conclusion:

- current released `tool.scad-project v0.13.0` relevant clamps runs take about 64–65 s end-to-end;
- single-host variant C measured 41.024 s and 45.169 s on the exact Step-5 candidate while still using one SCAD container;
- README-only controls measured 4.369 s and 4.819 s with zero container starts;
- the improvement comes from removing serial GitHub job and artifact-transfer boundaries, not from replacing Docker.

Therefore Step 5 is paused for a shared-owner correction before `lib.scad.clamps` can finish:

1. `tool.git-project` must expose its generated-output publication safety contract as a same-job reusable primitive while keeping the current reusable publication workflow as a thin wrapper;
2. `tool.scad-project` must consume that released primitive and release the one-host-job lifecycle with conditional Docker execution;
3. `lib.scad.clamps` then requalifies Step 5 on the released topology;
4. Step 6 remains blocked until Step 5 completes.

The separate Moon-versus-SCons target-engine question is parked in meta issue #51.
