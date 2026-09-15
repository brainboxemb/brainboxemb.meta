# Migration 005 — change request

Status: **approved; architecture/design validation complete; migration execution in progress**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Documentation-structure issue: [#60](https://github.com/brainboxemb/brainboxemb.meta/issues/60)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this document exists

This is the durable change request for Migration 005. It records why the migration was started, what change was requested, what is in and out of scope, which decisions are now fixed, and what remains to be migrated.

This document is being added after the architecture investigation because the durable change-request document was accidentally omitted when Migration 005 was started. That omission does **not** reopen the design phase. The architecture and technical feasibility have already been validated. The active owner-by-owner migration sequence is maintained in the implementation plan.

## Requested change

Simplify the SCAD repository execution architecture so that a normal maintainer can understand and operate it in terms of real project capabilities instead of copied lifecycle machinery.

The target model must:

- keep Moon for repository-level change-impact selection and whole-capability output reuse;
- use shared inherited Moon task policy instead of repeating generic lifecycle tasks in every consumer;
- let consumers declare only the capabilities they have plus project-specific impact patterns/overrides;
- keep SCons optional and only where a project explicitly uses it for fine-grained target reuse;
- select the SCAD runtime from effective project capabilities/configuration;
- keep one heavy hosted runner and one CAD runtime as the normal default;
- avoid starting the CAD runtime for unrelated changes;
- keep current run/ref/publication information outside source-derived cache identity;
- avoid retaining duplicate complete normal Build/Verification trees as Actions artifacts by default;
- allow isolated Build and Verification publication to overlap on the same runner when useful;
- preserve release and publication correctness while reducing duplicated compute, image transfer and configuration complexity.

## Why this migration is needed

Migration 004 proved that the common SCAD execution model works, but also exposed that the resulting consumer model was still too difficult to understand and that the latency/resource balance was not yet good enough to treat it as the final architecture.

The concrete problems were:

1. consumer `moon.yml` files exposed too much lifecycle machinery instead of only real capabilities;
2. broad tool inputs made generated Python bytecode part of Moon task identity, breaking stable whole-capability reuse across fresh runners;
3. all SCAD work used the full runtime image even when PythonSCAD was not required;
4. generic SCons cache handling was paid even by direct-engine projects;
5. complete normal output trees were uploaded as Actions artifacts even though same-run publication did not consume them;
6. Build and Verification publication was serialized despite being independently publishable;
7. the architecture needed to optimize both feedback time and total runner/resource use rather than either metric in isolation.

## Decisions now fixed

Architecture/design validation is complete. The migration now executes the following established model:

### Moon

Moon remains the repository-level layer for:

- determining which coarse SCAD capabilities are affected;
- stable whole-capability output caching/hydration.

The current generic affected query already computes the complete affected task set. Migration implementation must expose the relevant capability list from that same query rather than rerunning Moon per capability.

### Shared capability policy

`tool.scad-project` owns the standard inherited Moon tasks for real SCAD capabilities such as:

- design documentation;
- presentation renders;
- Verification.

Consumers own capability selection and project-specific impact patterns/overrides, not copied generic lifecycle mechanics.

### SCons

SCons remains optional fine-grained target reuse **inside** capabilities that explicitly configure `build_engine: scons`.

Direct-engine projects do not restore/save SCons caches.

### Runtime image family

The runtime is capability/configuration-driven:

- OpenSCAD-only work may use the focused OpenSCAD runtime;
- projects intentionally supporting PythonSCAD use the full/dual runtime.

The full image remains a tested superset of the OpenSCAD contract.

### Execution/resource model

Normal CI uses one heavy hosted runner and one CAD runtime. Eliminate unnecessary work before adding parallel VMs.

Feedback latency and total runner/resource use are both acceptance metrics.

### Artifacts and publication

Normal CI retains compact decision/orchestration evidence. Complete normal Build/Verification Actions artifacts are not retained by default when generated-output publication already carries the same trees.

Release remains a separate exact-source artifact hand-off.

Build and Verification publishers may run concurrently on the same runner because their isolated publication model has been validated.

## Maintainer-facing target

A normal consumer should be explainable in terms of its visible capabilities.

Reference examples:

```text
lib.scad.clamps
  Design documentation
  Verification
```

```text
lib.scad.hub75
  Presentation renders
  Design documentation
  Verification
```

A maintainer should not need to understand or hand-author task entries for publication staging, synthetic aggregate roots, runtime metadata, cache transport or generated indexes merely to understand what the repository builds.

## In scope

- the SCAD runtime image family and its external qualification contract;
- generic Moon affected capability-list output in `tool.git-project`;
- shared SCAD capability lifecycle in `tool.scad-project`;
- the reference template model;
- canary migration of `lib.scad.clamps` and `lib.scad.hub75`;
- downstream SCAD consumer migration after both canary modes are qualified;
- final resource/latency evidence and architecture closeout.

## Out of scope

- replacing SCons with Moon as a fine-grained CAD target engine;
- removing intentional PythonSCAD support from dual-runtime projects;
- changing physical CAD/verification semantics merely to simplify CI;
- introducing a second heavy runner only to regain feedback speed when work can instead be eliminated or reused;
- migrating the HUB75 display-frame project before the shared tooling and both canary modes are released and qualified.

## Migration execution order

The approved order is:

1. release the two-profile SCAD runtime image family and external test contract;
2. expose affected capability IDs from the existing generic Moon query;
3. release the shared SCAD capability lifecycle;
4. update the project template;
5. migrate `lib.scad.clamps` as the dual-runtime/direct canary;
6. migrate `lib.scad.hub75` as the OpenSCAD/SCons canary;
7. migrate downstream consumers, with the HUB75 display-frame project deliberately later;
8. close Migration 005 with measured implementation evidence.

The detailed current owner sequence and gates are maintained in the implementation-plan document.

## Completion criteria

Migration 005 is complete when:

- immutable released runtime/tool versions implement the validated model;
- consumers no longer duplicate generic lifecycle Moon configuration;
- unrelated changes avoid the CAD runtime;
- affected capability selection comes from one Moon analysis;
- direct and SCons project modes both behave correctly;
- OpenSCAD-only and full/dual runtime modes are both proven in real canaries;
- normal CI no longer retains duplicate full output artifacts by default;
- publication and release behavior remain correct;
- before/after feedback latency and total runner/resource use are recorded for the canaries/downstream rollout;
- durable architecture documentation reflects the final implemented system rather than the migration history.

## Stop/correction rule

This is now a migration, not an open-ended design exercise. Continue with the validated architecture unless implementation uncovers evidence that a fixed assumption is false.

If that happens, document the contradiction in `brainboxemb.meta` and correct the architecture explicitly before working around it in a consumer.