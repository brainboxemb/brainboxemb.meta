# Change request — define one understandable SCAD repository execution model

Status: **proposal for review; no implementation approved yet**

## Problem

A user working across current SCAD repositories currently encounters two different CI/build execution models without a clearly documented reason.

### Reference project model

`template.scad-project` and the current HUB75 frame use one `SCAD production` GitHub Actions job. That job starts one SCAD-toolchain container and runs a repository-level Moon graph that materializes separate SCAD capabilities such as documentation, Build and Verify.

### Current library model

`lib.scad.clamps` and `lib.scad.hub75` invoke separate reusable Build and Verify workflows from `tool.scad-project`. Build and Verify therefore run as separate jobs and each starts its own SCAD-toolchain container.

Both models work. The problem is that the reason for the difference is unclear, and the more expensive library execution shape may be historical rather than intentional.

A library is allowed to differ from a product repository, but the difference should follow from library-specific behaviour such as API verification or release packaging. Infrastructure should not differ merely because the repositories evolved at different times.

## Desired result

After this change is decided and, if approved, implemented:

- a user can recognize the same high-level SCAD lifecycle across project and library repositories;
- Build and Verify have clear, stable semantics independent of the repository type;
- any project-versus-library difference is documented next to the repository that owns it;
- expensive CI/runtime startup is not duplicated without a concrete benefit;
- Moon is present only where its orchestration/materialization behaviour earns its complexity;
- `template.scad-project` accurately demonstrates the architecture we recommend to new SCAD repositories;
- `lib.scad.clamps` demonstrates the intended library form unless repeated library-only boilerplate justifies a dedicated `template.scad-lib`.

## Common lifecycle to preserve

The default mental model should be the same for every current SCAD repository:

```text
repository source/configuration
        |
        v
bootstrap / validate
        |
        +---- docs
        +---- Build
        +---- Verify
        |
        v
evidence / publication / release
```

Repository type may change the targets and checks inside those capabilities. It should not automatically change the lifecycle itself.

## Build and Verify contract

Build and Verify should remain **separate logical domains**.

Build owns normal design outputs such as configured PNG/STL generation and its own SCons state/evidence.

Verify owns verification-only targets and project/library-specific checks with its own SCons state/evidence.

The separation introduced by `tool.scad-project` must not be undone merely to save CI startup time.

However, logical separation does **not** require separate GitHub Actions jobs or separate containers. One production execution may request both domains while preserving independent caches, targets and evidence.

The intended relationship should therefore be evaluated as:

```text
scad.ci
  |-- scad.docs / build publication preparation as needed
  |-- scad.build
  `-- scad.verify
```

rather than making Verify semantically depend on Build unless a real verification target requires a Build artifact.

## Current template inconsistency to review

The current `template.scad-project` Moon graph declares `scad.verify` with a dependency on `scad.build`.

That should be explicitly justified or removed because `tool.scad-project` has intentionally treated Verify as a separate domain since v0.10.0.

The aggregate CI graph may run both. That is different from defining Verify itself as dependent on Build.

This is a review finding, not yet an approved implementation change.

## Container lifecycle question

Current one-job project workflows declare the SCAD toolchain container at the GitHub job level. This means the container is started before checkout/bootstrap/Moon can decide whether producer work can be reused or hydrated.

The review must determine whether there is a safe and worthwhile cheaper preflight before starting the SCAD container.

The target optimisation is conceptually:

```text
cheap repository preflight
        |
        v
is SCAD execution/materialization required?
       / \
      no  yes
      |    |
 reuse/    start one SCAD container
 hydrate          |
                  +-- run required Build work
                  `-- run required Verify work
```

This diagram is a goal to evaluate, not a requirement to invent another change detector.

Any preflight must reuse authoritative repository/orchestration information. It must not try to predict SCons target decisions with a separate ad-hoc changed-files implementation.

## What Moon must justify

Moon should be evaluated by concrete capabilities, not by architectural preference.

For a SCAD repository it may provide value by:

- representing one repository-level task graph across docs, Build, Verify and publication preparation;
- avoiding duplicated repository-level work when several capabilities are requested in one CI run;
- portable whole-task cache/hydration above the fine-grained SCons object/target cache;
- recording current materialization/orchestration evidence separately from producer evidence;
- giving projects and libraries one recognizable execution entrypoint.

Costs include:

- `.moon/` and `moon.yml` configuration in every consumer;
- another cache/evidence layer that users must understand;
- Moon runtime/bootstrap overhead;
- risk of overlapping responsibility with SCons if boundaries are unclear;
- extra maintenance when a small library would otherwise need only one or two producer commands.

The migration should choose Moon only when the benefits are measurable or materially simplify the common model.

## Reference cases

### `template.scad-project`

Role: reference **project** consumer.

Questions to prove:

- Is its current one-job/Moon graph the architecture we actually recommend?
- Is the Build/Verify relationship correct?
- Is the large consumer-owned workflow appropriate, or should more of it be shared tooling?
- Can the container start be delayed without making the model brittle?

### `lib.scad.clamps`

Role: practical reference **library**.

Why use it first:

- small and inexpensive to build;
- little domain complexity unrelated to infrastructure;
- already uses current `tool.scad-project` release contracts;
- differences from the template can be inspected as library requirements rather than HUB75-specific requirements.

Questions to prove:

- Which Build/Verify checks are genuinely library-specific?
- Does a single production execution materially reduce duplicated work/container startup?
- Does Moon simplify or complicate this small repository?
- Which configuration can be shared with the project model and which should remain library-owned?

### `lib.scad.hub75`

Role: second library qualification only after clamps establishes the model.

Its richer verification/publication behaviour should validate the model, not determine it prematurely.

### HUB75 frame

Role: realistic project requalification when shared tooling/reference behaviour changes.

It should not be modified merely to make Migration 004 look complete.

## Decision options to compare

### Option A — common Moon-backed production model

Projects and libraries use one production job and one Moon repository graph. Repository type changes target/configuration details, not orchestration shape.

Accept only if Moon's materialization/cache/evidence benefits justify its consumer configuration and runtime cost even for `lib.scad.clamps`.

### Option B — common production shape, lighter library implementation

Projects and libraries expose the same user-facing lifecycle and preferably one expensive SCAD execution, but small libraries use a shared combined `tool.scad-project` workflow without Moon.

Accept only if this avoids meaningful complexity while keeping the user-facing model and evidence semantics consistent.

### Option C — deliberately different library model

Keep separate Build/Verify jobs/workflows for libraries.

Accept only if a concrete library property requires or materially benefits from independent job boundaries enough to justify duplicate runner/container setup and a different mental model.

Historical convenience is not sufficient justification.

### Option D — fix only the reference project model

If analysis shows that the library model is already the simpler and more appropriate common shape, change the template/shared architecture instead of migrating libraries toward Moon.

This option must remain viable during review.

## `template.scad-lib` decision

Do **not** create `template.scad-lib` as part of the proposal.

Use `lib.scad.clamps` as the practical library reference until at least one of these becomes true:

- starting a second/new library requires copying a substantial repeated set of library-specific files/configuration;
- the library lifecycle has stable rules that are materially different from `template.scad-project`;
- maintaining those rules in a real library obscures its domain purpose or makes new-library bootstrap error-prone.

Only then should a separate library template be considered.

## Measurements/evidence required before choosing

For the reference project and clamps, capture enough evidence to compare the options rather than arguing from file layout alone:

- number of GitHub jobs and SCAD-container starts for a normal PR run;
- runner/container/bootstrap overhead versus actual producer work;
- cold-run behaviour;
- unchanged/no-op or hydration behaviour;
- selective source change affecting only Build targets;
- verification-only source change;
- documentation-only change where practical;
- generated output/evidence/publication correctness;
- complexity added to each consumer repository;
- whether Build can be run independently;
- whether Verify can be run independently;
- whether aggregate CI can run both without duplicate expensive setup.

Exact duration is useful evidence but is not the only criterion. Consistency, correctness, observability and maintenance cost matter as well.

## Ownership boundaries

### `tool.git-project`

Owns generic repository bootstrap/orchestration capabilities, including Moon runtime/cache/materialization behaviour when Moon is selected.

### `tool.scad-project`

Owns SCAD-domain semantics:

- configuration;
- Build;
- Verify;
- SCons target/dependency decisions;
- producer/domain evidence;
- reusable SCAD producer/workflow interfaces.

It should not absorb generic repository orchestration solely because a SCAD consumer needs it.

### consumer repository

Owns:

- which project/library targets exist;
- project/library-specific verification commands;
- source/configuration inputs;
- only the minimal orchestration configuration that cannot reasonably be shared.

## Proposed acceptance criteria if activated

An implementation is complete only when:

1. the chosen project-versus-library execution model is documented with its reason, not merely its mechanics;
2. `template.scad-project` matches that documented model;
3. `lib.scad.clamps` proves the intended library model under cold, unchanged/hydrated and relevant selective-change scenarios;
4. Build and Verify remain independently invokable logical domains;
5. aggregate CI can request both without avoidable duplicate heavy setup according to the chosen architecture;
6. evidence/publication semantics remain intact;
7. `lib.scad.hub75` is migrated/requalified only after clamps proves the model;
8. the HUB75 frame is requalified only if shared changes affect it;
9. every intentional difference between project and library execution is documented in reader-facing repository documentation;
10. the decision on `template.scad-lib` is recorded, even if the decision is not to create it.

## Non-goals

- CAD geometry changes;
- physical verification content such as HUB75 SQ-01;
- replacing SCons;
- using Moon as a second SCAD dependency engine;
- introducing a new generic changed-file implementation just to avoid a container start;
- forcing identical repository trees when the underlying lifecycle genuinely differs;
- creating another template before repeated structure demonstrates its value.

## Activation decision

This change request is complete enough to review, but it deliberately does not select Option A, B, C or D yet.

The next action is an architecture/implementation review. Only after that review should Migration 004 become **active** and acquire a fixed implementation sequence.