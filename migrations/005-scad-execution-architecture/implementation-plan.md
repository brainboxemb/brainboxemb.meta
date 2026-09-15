# Migration 005 — implementation plan

Status: **ready for owner-repository implementation after architecture validation merge**

This plan starts only after the validated Migration-005 architecture/evidence is merged in `brainboxemb.meta`.

The plan deliberately separates owner repositories. Do not bundle unrelated owner changes into one repository just to reduce the number of pull requests.

## Step 1 — finalise and release the runtime image family

Owner repositories:

- `brainboxemb/docker.scad-toolchain`
- `brainboxemb/docker.scad-toolchain.test`

Starting evidence:

- toolchain PR #6, exact qualified source `eeb40e7eff98e98d754baf8ddb52376a17ecef18`;
- external-test PR #6, exact qualified source `89c5b45ecb8fa48b7bd6ff660aa0c67a7713aaaa`;
- controlled cold-vs-cold qualification run `34992630534`;
- normal resource-proportional qualification run `34993290359`.

Implementation goal:

- keep one multi-stage Dockerfile/source family;
- preserve `ghcr.io/brainboxemb/scad-toolchain:<version>` as the full/dual compatibility image;
- publish `ghcr.io/brainboxemb/scad-toolchain-openscad:<version>` as the OpenSCAD-focused profile;
- keep shared layers identical where practical;
- make profile identity visible through image metadata and `scad-toolchain-info`;
- keep the external test suite as the release gate for both profiles.

Before merge/release:

- remove diagnostic-only branch triggers from the production workflow;
- update PR descriptions so they describe the actual multi-stage implementation rather than the earlier throwaway experiment;
- ensure normal tests reuse shared local layers rather than deliberately forcing a second cold pull;
- keep the independent cold-pull benchmark as historical evidence, not routine CI;
- verify release/tag metadata produces immutable version tags for both packages;
- verify the full profile remains a tested superset of the OpenSCAD contract.

Gate to Step 2/3:

- released immutable image-family version exists;
- external qualification is green against that exact version.

## Step 2 — expose affected SCAD capabilities from the existing Moon query

Owner repository:

- `brainboxemb/tool.git-project`

Current released baseline:

- v0.2.7 / `6234b7437b0dc0115642468f74d1f4a2c2214bef`.

Implementation goal:

The released affected query already computes and stores the complete Moon affected-task set in `affected-tasks.json`. Extend its public action/script contract so consumers can obtain the relevant affected capability IDs in addition to the current compatibility boolean.

Requirements:

- keep the current conservative `affected=true/false` behaviour for compatibility;
- expose a stable machine-readable list of affected requested/SCAD capability tasks from the **same Moon query**;
- do not invoke Moon once per capability;
- keep exact base/head evidence;
- preserve fail-conservative behaviour if Moon/config/revision resolution fails;
- add contract tests for zero, one and multiple affected capabilities;
- keep the generic tool independent of SCAD-specific source semantics where possible: generic query mechanics belong here, capability naming/policy belongs in `tool.scad-project`.

Gate:

- release a new immutable `tool.git-project` version/ref with the list-output contract.

## Step 3 — implement the shared SCAD capability lifecycle

Owner repository:

- `brainboxemb/tool.scad-project`

Current released baseline:

- v0.13.1 / `28661fc040c4994e9c1d391285b7425c7a55252b`.

Prototype evidence:

- shared Moon task prototype `1303ae8c40817a98f9615a58762264b3ef19b6dd`;
- inheritance qualification run `34997339916`.

Implementation goal:

Make the validated target architecture the reusable SCAD workflow contract.

### Shared Moon policy

Add shared inherited capability tasks for:

- `scad.docs` — design documentation;
- `scad.build` — presentation renders;
- `scad.verify` — Verification.

Shared policy owns:

- capability commands;
- stable common project/tool source inputs;
- standard output boundaries;
- Moon cache policy.

Do not reintroduce `tools/tool.scad-project/**` as a source input.

### Configuration consistency

Validate `project.scad.yml` and the visible capability selection together.

At minimum:

- presentation/render configuration and `scad.build` must agree;
- Verification configuration and `scad.verify` must agree;
- PythonSCAD configuration selects the full/dual runtime;
- OpenSCAD-only configuration permits the focused runtime;
- `build_engine: scons` controls applicable SCons cache handling;
- direct-engine projects do not restore/save SCons caches;
- non-standard output roots require explicit compatible output overrides.

### Runtime selection

Select the runtime image from effective project capability/configuration, not repository name.

For the current references:

- clamps -> full/dual;
- HUB75 -> OpenSCAD-focused.

Pin immutable released image versions.

### One-runner execution

Keep one heavy hosted runner and one CAD runtime.

Use the affected capability list from Step 2 so the one Docker invocation executes/materialises only the required coarse capabilities.

Moon remains the whole-capability cache/reuse layer. SCons remains optional fine-grained target reuse inside SCons-configured capabilities.

### Current-run finishing

Keep current PR/ref/run/publication information outside Moon source-derived cache identity. Add it after execution/restoration on the host.

### Normal retained artifacts

Do not upload complete normal Build/Verification trees as Actions artifacts by default. Keep compact impact/orchestration evidence. If a real non-publication/manual-download use case needs full artifacts, make that an explicit opt-in policy.

Release remains a separate cross-job artifact hand-off and must not be broken by this change.

### Publication

Publish Build and Verification from isolated same-runner publisher instances and allow them to overlap. Do not create another hosted runner for publication.

### Acceptance

Test at least:

- unrelated/README-only -> zero CAD image/runtime;
- one affected capability;
- multiple affected capabilities;
- Moon warm capability hydration;
- direct project -> no SCons transport;
- SCons project -> useful SCons restore/save only;
- full runtime selection;
- OpenSCAD-focused runtime selection;
- normal publication with no duplicate full Actions artifacts;
- release workflow remains correct.

Gate:

- release a new immutable `tool.scad-project` version/ref.

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
- keep generated output/publication conventions aligned with shared tooling.

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
