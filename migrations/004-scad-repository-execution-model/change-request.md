# Change request — define one understandable SCAD repository execution model

Status: **proposal for review; no implementation approved yet**

Tracking issue: [#49](https://github.com/brainboxemb/brainboxemb.meta/issues/49)

## Executive decision to review

The current evidence supports one strong default:

> A current SCAD repository should present one recognizable production lifecycle regardless of whether it contains a project or a reusable library. Build and Verify remain separate logical domains, but ordinary CI should not require two expensive SCAD-container jobs merely because the repository is a library.

The implementation mechanism is **not yet approved**. Two implementation candidates remain credible:

1. a common Moon-backed production graph for projects and libraries;
2. the same user-facing production shape with a lighter combined implementation for small libraries.

Moon is the preferred hypothesis because it is already the repository-level orchestration model used by `template.scad-project` and the real HUB75 frame, but it must still prove that its cache/materialization/evidence value is worth its configuration and runtime cost in the small `lib.scad.clamps` reference library.

A deliberately different two-workflow library model remains possible only if a concrete library requirement justifies it. No such requirement has been found yet.

## Why this change request exists

A user working across current SCAD repositories currently encounters two different CI/build execution models without a clearly documented reason.

### Reference project model

`template.scad-project` and `2026-009-01.cad.HUB75-display-frame` use one `SCAD production` GitHub Actions workflow with one heavy SCAD-toolchain job. That job starts one SCAD container and runs a repository-level Moon graph that materializes separate SCAD capabilities such as documentation, Build and Verify.

Generated Build and Verification publication are then handled by separate lightweight publication jobs outside the SCAD container.

### Current library model

`lib.scad.clamps` and `lib.scad.hub75` invoke separate reusable Build and Verify workflows from `tool.scad-project`.

Each reusable workflow:

- allocates its own runner;
- starts its own `scad-toolchain` container;
- checks out the repository again;
- configures Git safe directories again;
- restores its own cache;
- performs its domain work;
- uploads and publishes from that same container job.

Both models are correct today. The problem is that the reason for the difference is unclear, and the more expensive library execution shape appears to be historical rather than a consequence of being a library.

A library may legitimately differ from a product repository, but the difference should follow from library-specific behaviour such as API verification, reusable-source packaging or release policy. Infrastructure should not differ merely because repositories evolved at different times.

## Evidence from the current implementation

This proposal is based on the repositories as they exist now, not on the older migration plan.

### `lib.scad.clamps` exact-main baseline

Qualified source: `52048164db5e5da0b9522c758551bc3af65cae45`.

Build run: `34872343290`.

- complete Build job: about **37 s**;
- container initialization alone: about **17 s**;
- checkout: about **3 s**;
- generated design documentation in this run: about **3 s**;
- configured Build outputs: less than the one-second timestamp resolution;
- publication remains inside the container job.

Verify run: `34872343227`.

- complete Verify job: about **32 s**;
- container initialization alone: about **18 s**;
- checkout: about **3 s**;
- actual `Verify project` step: about **2 s**;
- publication remains inside the container job.

The two workflows run in parallel, so elapsed wall-clock is not the sum of both jobs. However, the repository pays for **two runner setups, two checkouts and roughly 35 seconds of container initialization** for a very small amount of actual SCAD work.

This is strong evidence that two heavy jobs should not be the default merely because this repository is a library.

### `template.scad-project` exact-main baseline

Qualified source: `57ed48879370c5c3b60076ccb5a526d154fa6aa9`.

Production run: `34871575879`.

The main SCAD job:

- lasts about **52 s**;
- starts one SCAD container, taking about **20 s**;
- performs one checkout/bootstrap;
- restores both normal and verification SCons caches;
- runs/hydrates the Moon production graph in about **13 s** for this run;
- stages Build and Verification output once;
- uploads both publication artifacts.

Two later publication jobs are lightweight host jobs and do not start the SCAD container.

This does **not** prove that Moon is faster than a direct combined workflow. It does prove that one production execution can preserve separate Build/Verify outputs while avoiding a second SCAD-container startup.

### Performance conclusion

The goal is not simply to minimize elapsed seconds.

The current library jobs are parallel and can therefore finish sooner in wall-clock time than one naïvely sequential combined job. A replacement must consider:

- elapsed CI time;
- total runner/container work;
- duplicated bootstrap/setup;
- independent failure visibility;
- cache reuse;
- evidence clarity;
- maintenance complexity.

If Moon is selected, the corrected graph should also be tested for whether independent Build and Verify branches can execute concurrently inside one production job. That must be proven from the resulting run; it should not be assumed.

## Common lifecycle to preserve

The default mental model should be the same for every current SCAD repository:

```text
repository source/configuration
        |
        v
bootstrap / validate
        |
        v
SCAD production
   |         |
   |         +---- Build domain
   |         +---- Verify domain
   |         +---- documentation/provenance where configured
   |
   v
evidence / publication
        |
        v
release when requested
```

Repository type may change the targets and checks inside those capabilities. It should not automatically change the lifecycle itself.

## What is genuinely different about a library?

The review found real project-versus-library differences, but none currently require separate heavy Build and Verify jobs.

A reusable library may differ in:

- source layout: library source may live at repository root instead of under a project `dsg/` tree;
- what Build demonstrates: reusable modules/functions/examples rather than a final project assembly;
- verification content: public API behaviour, dimensions, compatibility and representative fixtures may matter more than project integration checks;
- release contents: reusable source/API and verification evidence are primary outputs;
- downstream qualification: a library release may need one or more real consuming projects to prove compatibility.

These are **domain/content differences**. They can be expressed through `project.scad.yml`, source layout, verification commands, release configuration and consumer qualification.

No current library requirement has been identified that inherently needs:

- a second SCAD container;
- a second checkout;
- a separate GitHub Actions workflow trigger for Verify;
- a different repository-orchestration engine.

Therefore those execution differences should be treated as historical until proven otherwise.

## Build and Verify contract

Build and Verify remain **separate logical domains**.

### Build owns

- normal configured PNG/STL generation;
- generated design output where configured;
- normal SCons target state/cache;
- Build producer/domain evidence;
- Build publication content.

### Verify owns

- verification-only targets;
- project/library-specific verification commands;
- verification SCons target state/cache;
- Verification producer/domain evidence;
- Verification publication content.

The separation introduced by `tool.scad-project v0.10.0` must not be undone merely to save CI startup time.

Logical independence means all of the following should remain possible:

```text
scad.build      # build only
scad.verify     # verify only
scad.ci         # request the normal CI production set
```

The aggregate `scad.ci` can request both domains. That is different from making Verify itself depend on Build.

## Current template inconsistency

The current `template.scad-project/moon.yml` declares:

```text
scad.verify -> scad.build
```

while `tool.scad-project` intentionally made Verify independent of the normal Build domain in v0.10.0.

Unless a concrete verification target consumes normal Build output, the intended graph should instead be conceptually:

```text
                     +--> scad.build ----> build provenance ---+
scad.ci ------------>|                                      |--+--> complete
                     +--> scad.verify --> verify provenance --+
```

with documentation/build-index dependencies represented only where their outputs are actually needed.

This must be corrected or explicitly justified **before the template is used as the model copied into libraries**.

The same review must be applied to the HUB75 frame if it inherited the same dependency.

## One job does not mean one domain

A key design rule for this migration is:

> GitHub job boundaries are an execution choice, not a domain boundary.

It is valid to run Build and Verify in one container while retaining:

- independent commands;
- independent caches;
- independent SCons decision reports;
- independent execution evidence;
- independent output trees;
- independent publication branches;
- the ability to invoke either domain separately when a user explicitly wants that.

This is the main distinction that allows consistency and optimization without regressing the v0.10 Build/Verify contract.

## Publication should not keep the SCAD container alive unnecessarily

The current library reusable workflows publish generated branches from inside their Build/Verify container jobs.

The template/frame model instead:

1. performs SCAD production;
2. stages/uploads prepared publication artifacts;
3. lets lightweight host jobs publish Build and Verification output.

The latter is the better ownership/lifecycle shape because Git publication itself does not require OpenSCAD/PythonSCAD.

A common production model should therefore prefer **SCAD work in the SCAD job, repository publication outside it** unless measurements show a concrete reason otherwise.

## Container lifecycle

### Current state

Both execution models declare the SCAD toolchain with GitHub Actions `container:` at job level.

GitHub therefore starts the container **before any workflow step** can inspect the repository, restore Moon cache or decide whether producer work is required.

### Important finding

The current `tool.git-project/moon-project.sh run` command is not a preflight planner. It validates the repository and then directly performs `moon run TASK`.

That means simply moving the existing Moon action before the container is not a valid solution: on a cache miss Moon can execute a SCAD task, and that execution needs the SCAD runtime.

### Consequence

Two optimizations must be treated separately:

**Optimization 1 — remove avoidable duplicate heavy setup**

- one normal SCAD production execution;
- one container startup;
- one checkout/bootstrap;
- separate Build and Verify domains inside that execution.

This is feasible with the current tool boundaries and is the primary Migration 004 question.

**Optimization 2 — avoid starting the SCAD container at all when no SCAD execution is required**

This requires a trustworthy host-side preflight/plan capability that does not attempt to execute SCAD commands on a cache miss.

That capability does not exist today.

Migration 004 must **not** invent an ad-hoc changed-files predictor merely to achieve this optimization. Container deferral may become a later tooling improvement if Moon/tool.git-project can expose a reliable plan/cache decision.

Container deferral is therefore **not a completion criterion for the first execution-model migration**.

## What Moon must justify

Moon should be evaluated by concrete capabilities, not by architectural preference.

Potential value:

- one repository-level task graph across docs, Build and Verify;
- independent branches of work under one production entrypoint;
- portable whole-task cache/hydration above fine-grained SCons target caching;
- current materialization/orchestration evidence distinct from producer evidence;
- one recognizable execution entrypoint across projects and libraries;
- a place to express repository-level dependencies without moving them into `tool.scad-project`'s SCAD-domain semantics.

Costs:

- `.moon/` and `moon.yml` configuration in every Moon consumer;
- another cache/evidence layer users must understand;
- Moon runtime/bootstrap work;
- possible duplicated responsibility with SCons if task inputs become too fine-grained;
- consumer-owned task configuration can drift, as the current `scad.verify -> scad.build` dependency demonstrates;
- it does not currently solve the pre-container decision problem.

### Boundary with SCons

If Moon is retained/expanded, its boundary must stay coarse:

```text
Moon
  repository task/materialization decision
        |
        +--> SCAD Build producer
        |       `--> SCons decides individual Build targets
        |
        `--> SCAD Verify producer
                `--> SCons decides individual Verification targets
```

Moon must not become a second SCAD dependency graph that tries to know which individual render/export target changed.

## Reference cases

### `template.scad-project`

Role: reference **project** consumer and architectural example.

It must answer:

- Is one production job really the recommended default?
- Is the Moon graph consistent with the current Build/Verify contract?
- Can the generic 200+ line production workflow be moved into shared tooling so the template demonstrates configuration rather than copied workflow mechanics?
- Which repository-level tasks genuinely belong in Moon?
- Which differences from `lib.scad.clamps` are project-domain differences rather than historical implementation differences?

The template should not merely be a test fixture for every available tool. It should demonstrate the setup we actually recommend to a new SCAD project.

### `lib.scad.clamps`

Role: practical reference **library**.

Why use it first:

- small and cheap to execute repeatedly;
- little domain complexity unrelated to infrastructure;
- current `tool.scad-project` contracts already work;
- its current duplicate setup overhead is easy to observe;
- library-specific behaviour can be distinguished from HUB75-specific behaviour.

It must answer:

- Does the common one-production-job lifecycle fit a real small library cleanly?
- Does Moon add useful hydration/materialization/evidence value here?
- Can Build and Verify remain independently invokable while aggregate CI avoids duplicate setup?
- What library-specific configuration remains after common mechanics are shared?

### `lib.scad.hub75`

Role: second library qualification.

Its richer verification/publication behaviour should validate a model already proven with clamps. Physical verification content such as SQ-01 remains outside this migration.

### HUB75 frame

Role: realistic project requalification if shared production/tooling changes affect it.

It should not drive the first design decision because it has enough project-specific complexity to hide unnecessary generic complexity.

## User-facing target

Regardless of the internal implementation chosen, a current repository should ideally expose a similarly recognizable CI surface:

```text
SCAD production
  -> Build result/evidence
  -> Verification result/evidence
  -> build publication
  -> verification publication
```

A user should not need to learn one CI mental model for libraries and another for projects unless the difference provides a visible, documented benefit.

Explicit local/domain commands remain available:

```text
scad-project build
scad-project verify
```

A common aggregate command/task may orchestrate both in CI without changing those commands' semantics.

## Shared-workflow ownership to evaluate

The current template and frame contain substantial consumer-owned production workflow mechanics: checkout, bootstrap, cache restore, Moon invocation, evidence validation, staging and publication artifact upload.

If this becomes the common model, copying that large workflow into each library is not acceptable.

The implementation should evaluate a shared SCAD production workflow, conceptually:

```text
consumer .github/workflows/scad.yml
        |
        `--> tool.scad-project reusable production workflow
                 |
                 +--> checkout/bootstrap
                 +--> restore SCAD caches
                 +--> repository orchestration
                 +--> validate/stage evidence
                 +--> upload prepared Build/Verify publication
                 +--> lightweight publication jobs
```

`tool.scad-project` is the likely owner of the SCAD production workflow because it owns the SCAD runtime and Build/Verify producer contracts.

If Moon is used inside it, `tool.git-project` remains owner of the generic Moon runtime/cache/materialization implementation.

The shared workflow should not hard-code one consumer's target filenames as the current template/frame evidence checks do. Generic evidence validation belongs in tooling; consumer-specific expected files remain consumer configuration or verification.

## Decision options

### Option A — common Moon-backed production model

Projects and libraries use one production workflow/job and one Moon repository graph. Repository type changes target/configuration details, not orchestration shape.

**Advantages**

- strongest consistency;
- one existing repository-level graph model;
- materialization evidence retained everywhere;
- compatible with current template/frame direction;
- potential parallel Build/Verify branches inside one production graph.

**Risks/costs**

- Moon configuration added to small libraries;
- Moon whole-task caching may add little above SCons for a tiny library;
- current task graph needs correction;
- common workflow must be extracted from consumer repositories;
- container preflight remains unsolved.

**Accept if** clamps demonstrates useful materialization/hydration or simplification without disproportionate configuration/runtime cost.

### Option B — common production lifecycle, direct combined library execution

All repositories expose the same one-production-job lifecycle, but a small library's shared workflow invokes Build and Verify producers directly rather than through Moon.

**Advantages**

- removes duplicate container/setup immediately;
- minimal library configuration;
- preserves Build/Verify semantics;
- no Moon layer where whole-task orchestration provides little value.

**Risks/costs**

- two internal orchestration implementations remain;
- libraries lack Moon materialization evidence/hydration;
- tooling must define a clear criterion for when Moon is needed;
- user-facing consistency could hide maintenance complexity underneath.

**Accept if** the clamps comparison shows Moon materially complicates the small-library case without providing useful cache/evidence behavior.

### Option C — retain separate library Build and Verify jobs

**Advantages**

- current libraries already work;
- Build/Verify failures and runs are maximally independent;
- parallel jobs can minimize elapsed wall-clock.

**Costs**

- duplicate heavy container startup and checkout;
- different CI mental model;
- publication keeps both heavy jobs alive;
- no library-specific requirement has yet been found that needs this shape.

**Accept only if** an explicit technical property of libraries proves the independent-job boundary worthwhile enough to outweigh those costs.

At present this is **not the preferred direction**.

### Option D — simplify the common model away from Moon

Change template/shared project architecture toward a direct combined production workflow and reserve Moon only for consumers that demonstrably benefit from a larger repository graph.

**Advantages**

- potentially simplest common stack;
- avoids forcing Moon on tiny repositories.

**Risks/costs**

- reverses part of the recently qualified repository-build architecture;
- loses or must replace current materialization/hydration evidence;
- real HUB75 frame would need deliberate re-evaluation.

**Accept only if** measurement shows Moon is not providing enough value even in the reference project model.

## Preferred hypothesis for review

Before implementation, the preferred order of evaluation is:

1. **Keep the common lifecycle and one-production-job goal.** This is already supported by current evidence.
2. **Correct logical Build/Verify independence in the reference task graph.** Aggregate CI requests both; Verify does not inherently depend on Build.
3. **Use `lib.scad.clamps` to compare Option A and Option B.** Do not use HUB75 complexity to choose the generic answer.
4. Prefer **Option A** if Moon gives useful hydration/materialization/evidence with modest library configuration.
5. Prefer **Option B** if the same operational/user model can be achieved substantially more simply without losing evidence the library actually needs.
6. Choose Option C only with a new concrete reason; none exists now.
7. Consider Option D only if the comparison exposes a broader problem with the current template architecture.

This is a recommendation about what to test first, not permission to implement it yet.

## Qualification matrix if Migration 004 is activated

The first implementation slice should use `template.scad-project` and `lib.scad.clamps` only.

| Scenario | What must be shown |
| --- | --- |
| Cold production | Both domains execute; Build/Verify evidence and publications are correct. |
| Unchanged rerun | Reuse/hydration behavior is visible and correct; no stale evidence is presented as current execution. |
| Build-only source impact | Relevant Build targets are rebuilt/restored correctly; Verify semantics remain independent. |
| Verification-only source impact | Verification work runs without forcing normal Build solely because of orchestration wiring. |
| Documentation-only change | Only legitimately affected repository tasks rerun; no ad-hoc file predictor is introduced. |
| Build explicit invocation | Build can still be invoked and reasoned about independently. |
| Verify explicit invocation | Verify can still be invoked without normal Build as required by the v0.10+ contract. |
| Aggregate CI | Both domains complete under one normal production entrypoint without avoidable duplicate SCAD-container startup. |
| Publication | Build/Verification output is published independently and publication itself does not require the SCAD container. |
| Failure isolation | A Verify failure remains clearly a Verify failure even though aggregate CI shares setup. |

For the A/B comparison, retain at least:

- job count;
- SCAD-container count;
- container startup time;
- checkout/bootstrap time;
- orchestration time;
- actual producer time where observable;
- total elapsed time;
- cache/hydration result;
- consumer configuration size/duplication;
- evidence produced.

Do not select an option based on a single warm run.

## Implementation sequence if activated

Activation does not mean all consumers are immediately changed.

### Step 1 — reference-contract correction

Owner: `template.scad-project`, with tool owner changes only where needed.

- remove or justify the stale `scad.verify -> scad.build` dependency;
- make `scad.ci` the aggregate owner of both domains;
- ensure Build and Verify still work independently;
- update stale template README text that still describes separate thin Build/Verify workflow callers;
- establish a clean baseline run for the corrected reference graph.

### Step 2 — shared production-workflow prototype

Owner: expected `tool.scad-project`; generic Moon portions remain `tool.git-project` owned.

- avoid copying the template/frame's large `scad.yml` into consumers;
- create/prototype the smallest reusable one-production-job interface;
- keep consumer-specific target/evidence assertions out of generic workflow code;
- keep publication outside the SCAD container where practical.

No release is made until the interface has been qualified in the reference consumers.

### Step 3 — clamps A/B qualification

Owner: `lib.scad.clamps` as reference library.

- exercise Moon-backed common production shape;
- compare it with the simplest direct combined shape if the Moon value is still uncertain;
- execute the qualification matrix;
- record why the selected library model is preferred.

This is the decision point for Option A versus B.

### Step 4 — release shared tooling

Only after the reference project and clamps prove the selected model:

- release changed `tool.git-project` and/or `tool.scad-project` as required;
- pin the template and clamps to released versions;
- re-run exact-main qualification.

### Step 5 — migrate/requalify `lib.scad.hub75`

- preserve its library-specific verification behavior;
- do not mix physical verification content into this migration;
- prove the selected common execution model on the richer library.

### Step 6 — requalify real HUB75 frame when affected

If shared workflow/graph semantics changed, update and qualify the frame. Do not change its CAD geometry as part of this migration.

### Step 7 — documentation closeout

Record in the reader-facing documentation of template and libraries:

- the common SCAD lifecycle;
- why their orchestration choice exists;
- intentional project-versus-library differences;
- whether Moon is part of the common model or an optional repository-level optimization.

## `template.scad-lib` decision

Do **not** create `template.scad-lib` as part of the initial migration.

Use `lib.scad.clamps` as the practical reference library until repeated evidence shows a separate template has value.

Create a dedicated library template only when at least one of these is demonstrated:

- a second/new library requires copying a substantial stable set of library-specific files/configuration;
- library release/API verification rules materially differ from the project template and recur across libraries;
- using a real library as the reference makes bootstrap unsafe or obscures its domain purpose;
- a generated/new library cannot be created cleanly from the shared tooling plus a small library profile.

If those conditions are not met, `lib.scad.clamps` remains the example and no extra repository is created.

## Ownership boundaries

### `tool.git-project`

Owns generic repository capabilities:

- dependency/bootstrap mechanics;
- Moon runtime/bootstrap;
- portable Moon cache/materialization behavior;
- generic generated-output publication tooling.

### `tool.scad-project`

Owns SCAD-domain behavior:

- SCAD configuration;
- Build and Verify semantics;
- SCons target/dependency decisions;
- producer/domain evidence;
- SCAD toolchain execution contract;
- reusable SCAD CI interfaces.

### consumer repository

Owns:

- actual project/library source and targets;
- project/library-specific verification commands;
- repository-specific expected artifacts when those are meaningful acceptance checks;
- minimal orchestration configuration that cannot reasonably be shared.

### `brainboxemb.meta`

Owns only the cross-project decision, sequencing and retained qualification evidence.

## Acceptance criteria if activated

Migration 004 is complete only when:

1. one common reader/user-facing SCAD production lifecycle is documented;
2. any remaining project-versus-library execution difference has an explicit technical reason;
3. Build and Verify remain independently invokable logical domains;
4. normal aggregate CI avoids duplicate SCAD-container startup unless deliberately justified;
5. `template.scad-project` matches the documented reference model and its README matches reality;
6. `lib.scad.clamps` proves the selected library implementation under cold, unchanged/hydrated and selective-change scenarios;
7. publication/evidence semantics remain correct and publication does not unnecessarily require the SCAD runtime;
8. the selected use or non-use of Moon is explained by demonstrated value rather than consistency alone;
9. `lib.scad.hub75` is requalified after clamps proves the model;
10. the HUB75 frame is requalified if shared implementation changes affect it;
11. the decision about `template.scad-lib` is recorded, even if that decision is not to create it;
12. container-preflight deferral is either implemented with an authoritative mechanism or explicitly retained as a separate follow-up — it is not faked with an ad-hoc changed-file predictor.

## Non-goals

- CAD geometry changes;
- physical verification content such as HUB75 SQ-01;
- replacing SCons;
- using Moon as a second SCAD target dependency engine;
- introducing another generic changed-file implementation;
- forcing identical repository directory trees;
- creating `template.scad-lib` before repeated structure justifies it;
- requiring the first Migration 004 slice to solve host-side container preflight.

## Activation decision

This change request is intended to make an activation decision possible without rediscovering the current architecture during implementation.

It does **not** activate Migration 004.

The decision to activate should explicitly answer:

1. Do we agree that the default current SCAD lifecycle should be recognizable across project and library repositories?
2. Do we agree that Build and Verify remain logically independent while normal CI may share one heavy execution context?
3. Do we agree that the current separate two-container library workflows have no demonstrated library-specific justification?
4. Do we want to run the template/clamps reference work to choose between the Moon-backed common model and the lighter direct combined model?
5. Do we agree that container deferral before SCAD execution is a separate optimization unless a trustworthy planning mechanism is first added?

Only after those questions are accepted should issue #49 change from **proposed / inactive** to **active**.