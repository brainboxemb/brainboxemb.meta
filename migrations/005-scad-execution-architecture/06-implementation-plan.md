# Migration 005 — implementation plan

Status: **active migration execution — architecture/design validation is complete**

## Why this document exists

This is the operational plan for carrying the validated Migration-005 architecture through the owner repositories. Read it to determine **which repository changes next, what that step must migrate, and what gate must be satisfied before moving on**.

This is no longer a design plan. The architecture is fixed in [05 — Validated target architecture](05-target-architecture.md). New architecture work is only justified if implementation uncovers evidence that one of those fixed assumptions is false.

The plan deliberately separates owner repositories. Do not bundle unrelated owner changes into one repository just to reduce the number of pull requests.

## Current progress

- **Step 1 — runtime image family:** implementation merged and `docker.scad-toolchain v0.5.0` released from exact source `a56a3aae4b9e0494e6625e75002d96b0a55986a3`; both immutable image profiles passed external `v0.5.0` qualification in run `34999654405`. The external testsuite default now points at `v0.5.0`; any remaining verification-record housekeeping is a closeout detail rather than a dependency for later released steps.
- **Step 2 — affected capability list:** **complete**. `tool.git-project v0.2.8` is released from exact source `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb` with the complete affected-task list exposed from the existing single Moon query.
- **Step 3 — shared SCAD capability lifecycle:** **complete**. `tool.scad-project v0.14.0` is released from exact source `3178a42453a5cb7439c11a6416fc9596477ac304`; exact-main Test `35011412444`, release run `35011532281` and tagged Test `35011547837` are green.
- **Step 4 — template/reference consumer model:** **next owner step**. It must pin the released Step-2/3 dependencies rather than an unreleased tool branch.
- **Steps 5–8:** waiting on their preceding released owner dependencies and canary evidence.

## Step 1 — finalise and release the runtime image family

Owner repositories:

- `brainboxemb/docker.scad-toolchain`
- `brainboxemb/docker.scad-toolchain.test`

Starting evidence:

- toolchain PR #6, exact qualified candidate source `eeb40e7eff98e98d754baf8ddb52376a17ecef18`;
- external-test PR #6, qualified candidate source;
- controlled cold-vs-cold qualification run `34992630534`;
- normal resource-proportional qualification run `34993290359`.

Implemented result:

- one multi-stage Dockerfile/source family;
- `ghcr.io/brainboxemb/scad-toolchain:v0.5.0` remains the full/dual compatibility image;
- `ghcr.io/brainboxemb/scad-toolchain-openscad:v0.5.0` is the OpenSCAD-focused profile;
- shared layers are reused between the profiles;
- profile identity is exposed by the runtime tooling;
- one external test suite qualifies both profiles.

The external testsuite default now points at the released `v0.5.0` pair. Keep any remaining historical verification-record cleanup separate from the blocking rollout path unless it reveals contradictory evidence.

Gate to Step 2/3:

- released immutable image-family version exists — **met (`v0.5.0`)**;
- external qualification is green against that exact version — **met (`34999654405`)**;
- external testsuite default version points at the release — **met (`v0.5.0`)**.

## Step 2 — expose affected SCAD capabilities from the existing Moon query

Owner repository:

- `brainboxemb/tool.git-project`

Released result:

- `v0.2.8` / `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.

Implementation result:

The affected action/script keeps the compatibility boolean and exposes the complete Moon affected-task set from the **same Moon query** as machine-readable output.

The released contract:

- keeps conservative `affected=true/false` compatibility behaviour;
- exposes the stable affected-task list without invoking Moon once per capability;
- keeps exact base/head evidence;
- fails conservatively if Moon/config/revision resolution fails;
- is generic: SCAD capability naming/policy remains in `tool.scad-project`.

Current interface note: v0.2.8 still requires one existing task as a query anchor. The complete affected-task list itself is repository-wide and is not limited to that anchor. The Step-3 workflow currently anchors on `consumer:scad.docs`; the planned template, clamps and HUB75 reference migrations all expose that capability. Removing the anchor requirement can be a later generic improvement if repositories without docs need this lifecycle; it is not a reason to create a second changed-path model.

Gate:

- release a new immutable `tool.git-project` version/ref with the list-output contract — **met (`v0.2.8`)**.

## Step 3 — implement the shared SCAD capability lifecycle

Owner repository:

- `brainboxemb/tool.scad-project`

Released result:

- `v0.14.0` / `3178a42453a5cb7439c11a6416fc9596477ac304`;
- owner implementation/change request: `tool.scad-project#55`;
- final owner candidate before merge: `e88e865b8219302a50a9b3c454c3def9c4fec6de`, Test `35011128956`;
- exact-main Test: `35011412444`;
- release workflow: `35011532281`;
- tagged Test on `v0.14.0`: `35011547837`.

Prototype evidence:

- shared Moon task prototype `1303ae8c40817a98f9615a58762264b3ef19b6dd`;
- inheritance qualification run `34997339916`.

Implemented result:

### Shared Moon policy

Shared inherited capability tasks now cover:

- `scad.docs` — design documentation;
- `scad.build` — presentation renders;
- `scad.verify` — Verification.

Shared policy owns:

- capability commands;
- stable common project/tool source inputs;
- standard output boundaries;
- Moon cache policy.

Broad `tools/tool.scad-project/**` source identity is not used, avoiding generated Python bytecode in Moon hashes.

### Configuration consistency

`project.scad.yml` and visible capability selection are validated together.

The released planner covers:

- presentation/render configuration and `scad.build` agreement;
- Verification configuration and `scad.verify` agreement;
- PythonSCAD -> full/dual runtime;
- OpenSCAD-only -> focused runtime;
- normal SCons cache handling only for SCons-configured Build/docs work;
- no normal SCons restore/save for direct-engine projects;
- separate Verification-SCons transport only when real Verification render/export targets exist;
- explicit compatible Moon output overrides for non-standard output roots.

### Runtime selection

Runtime image selection is derived from effective project configuration rather than repository name and pins released `docker.scad-toolchain v0.5.0` profiles.

For the current references:

- clamps -> full/dual;
- HUB75 -> OpenSCAD-focused.

### One-runner execution

Normal production keeps one hosted runner and at most one CAD runtime.

The affected capability list from Step 2 drives the source-affected capability set. Moon remains the whole-capability cache/reuse layer; SCons remains optional fine-grained target reuse inside SCons-configured capabilities.

One correctness refinement was discovered during implementation: **source-affected capability selection is not always identical to publication-safe materialization**. When `scad.docs` and `scad.build` both contribute to one complete Build publication tree, a docs-only change may still need the unchanged Build contributor hydrated from Moon so publishing the complete replacement tree cannot delete unchanged presentation output. That contributor remains explicitly non-affected; hydration/reproduction exists only to make the publication family complete.

Verification is a separate publication family and is not pulled into Build for that reason.

### Current-run finishing

Current PR/ref/run/publication information remains outside Moon source-derived cache identity and is added after execution/restoration on the host.

### Normal retained artifacts

Normal CI keeps compact impact/orchestration evidence rather than uploading duplicate complete Build/Verification trees as Actions artifacts.

Release remains a separate cross-job artifact hand-off and retains complete Build/Verification artifacts.

### Publication

Build and Verification publish from isolated same-runner publisher instances and may overlap. No second hosted runner is added for publication.

### Acceptance

Owner tests and the prior architecture qualification cover:

- unrelated/non-SCAD -> zero CAD image/runtime;
- one and multiple affected capabilities;
- conservative full configured scope;
- Moon warm capability hydration;
- direct project -> no SCons transport;
- SCons project -> applicable cache transport only;
- full and focused runtime selection;
- normal publication without duplicate full Actions artifacts;
- release runtime/cache planning and cross-job artifact hand-off;
- publication-safe Build-family hydration.

Gate:

- release a new immutable `tool.scad-project` version/ref — **met (`v0.14.0`)**.

## Step 4 — update the template/reference consumer model

Owner repository:

- `brainboxemb/template.scad-project`

Purpose:

Make the repository template teach the new architecture rather than the Migration-004 lifecycle topology.

Requirements:

- reduce consumer Moon configuration to capability selection plus project-specific impact patterns;
- keep the single inherited-task link to pinned `tool.scad-project` policy;
- retain intentional OpenSCAD + PythonSCAD example capability, so the template exercises the full runtime where appropriate;
- document how a project becomes OpenSCAD-only versus dual-runtime;
- document direct versus SCons choice;
- keep generated output/publication conventions aligned with shared tooling;
- pin released `tool.git-project v0.2.8`, `tool.scad-project v0.14.0` and the released runtime-family contract rather than unreleased owner branches.

Gate:

- a newly created/updated template consumer is understandable without copying generic lifecycle tasks.

## Step 5 — migrate and qualify `lib.scad.clamps` as the dual-runtime/direct canary

Owner repository:

- `brainboxemb/lib.scad.clamps`

Why first:

- intentionally supports both OpenSCAD and PythonSCAD;
- uses the direct engine;
- therefore proves the full runtime path and proves unused SCons mechanics are gone.

Expected visible capabilities:

```text
Design documentation
Verification
```

Required evidence:

- README-only/unrelated -> zero CAD runtime;
- docs-only and Verify-only boundaries behave as declared;
- full/dual image is selected because PythonSCAD capability exists;
- no SCons cache restore/save occurs;
- stable Moon capability hashes across fresh runners;
- warm Moon reuse avoids actual capability work;
- normal full-tree Actions artifacts are absent by default;
- published Build/Verification content remains correct;
- feedback latency and total runner time/resource counts are recorded.

Gate:

- qualified main and, if appropriate, immutable clamps release.

## Step 6 — migrate and qualify `lib.scad.hub75` as the OpenSCAD/SCons canary

Owner repository:

- `brainboxemb/lib.scad.hub75`

Why second:

- exercises the focused OpenSCAD runtime;
- explicitly uses SCons;
- has three independently affected capabilities.

Expected visible capabilities:

```text
Presentation renders
Design documentation
Verification
```

Required evidence:

- README-only -> zero CAD runtime;
- Build-only/docs-only/Verify-only source changes select the correct capability set;
- OpenSCAD-focused image is selected;
- normal SCons cache restores/populates where useful;
- unused separate Verification SCons cache is absent unless Verification actually adopts SCons;
- warm SCons target reuse remains effective;
- Moon whole-capability reuse remains stable;
- image transfer/pull behaviour is remeasured against the v0.4.1 full-image baseline;
- normal artifact/publication policy is correct;
- feedback latency and total runner/resource counts meet the Migration-005 budget or deviations are explained.

Gate:

- qualified main and immutable HUB75 library release.

## Step 7 — migrate downstream SCAD consumers, HUB75 frame last

Owners:

- each consumer repository owns its own migration;
- `brainboxemb/2026-009-01.cad.HUB75-display-frame` is intentionally not first.

Prerequisites:

- Steps 1–6 complete;
- released immutable tool/image/library refs exist;
- both canary modes are proven: dual/direct and OpenSCAD/SCons.

For each consumer:

- determine capabilities from current project intent rather than copying another repository blindly;
- reduce consumer Moon topology to capability selection/impact exceptions;
- select runtime by effective capabilities;
- preserve repository-specific verification and publication semantics;
- record before/after feedback and resource evidence.

## Step 8 — close Migration 005

Owner:

- `brainboxemb/brainboxemb.meta`

Close only after implementation evidence from both canaries and at least the intended downstream migration set is available.

Final meta work:

- replace provisional/budget values with measured implementation values;
- record released immutable refs;
- document any architecture corrections learned during implementation;
- close or remove diagnostic-only branches/PRs that were not production changes;
- make the final architecture page the durable maintainer reference;
- close tracking issue #55 when no Migration-005 implementation work remains.

## Sequencing principle

Do not optimize the plan for the fewest pull requests. Optimize it so every layer is proven by its owner and later consumers pin released, already-qualified dependencies.

The intended order is therefore:

```text
runtime images + external contract
        |
        v
generic Moon affected-list contract
        |
        v
shared SCAD capability lifecycle
        |
        v
template
        |
        +--> clamps dual/direct canary
        |
        +--> HUB75 OpenSCAD/SCons canary
                    |
                    v
             downstream consumers
```
