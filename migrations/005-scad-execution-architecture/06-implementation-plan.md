# Migration 005 — implementation plan

Status: **active migration execution — Step 4 complete; Steps 5 and 6 are active parallel canaries**

## Why this document exists

This is the operational owner-by-owner rollout plan for the validated Migration-005 architecture. The architecture itself is fixed in [05 — Validated target architecture](05-target-architecture.md); this page determines which repository changes next and what evidence gates the following step.

Do not bundle unrelated owner changes merely to reduce pull-request count. If integration exposes an owner defect, fix and release it in that owner repository before continuing the affected consumer step.

## Current progress

- **Step 1 — runtime image family:** complete. `docker.scad-toolchain v0.5.0` released from `a56a3aae4b9e0494e6625e75002d96b0a55986a3`; immutable profiles externally qualified in run `34999654405`.
- **Step 2 — affected capability list:** complete. `tool.git-project v0.2.8` released from `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.
- **Step 3 — shared SCAD capability lifecycle:** complete. Initial release `v0.14.0` was followed by two integration-driven patch releases; the current released foundation for consumers is **`tool.scad-project v0.14.2` / `5712324ea9e3a7c81ba1b79013f2758f52b219cf`**.
- **Step 4 — template/reference consumer model:** **complete**. `template.scad-project#37` merged as `cf3da65943968a42f3a0199cb682b1c74f452ee9`; full integration run `35020468894` was green on the released v0.14.2 foundation. The missing immutable template release is being closed as release follow-through and is not a dependency of either library canary.
- **Step 5 — clamps dual-runtime/direct canary:** **active**.
- **Step 6 — HUB75 OpenSCAD/SCons canary:** **active in parallel with Step 5**.
- **Steps 7–8:** wait until both canary gates are met.

## Parallel-canary correction

Steps 5 and 6 exercise independent modes of the same already released foundation:

- clamps proves **full/dual runtime + direct engine + no unused SCons transport**;
- HUB75 proves **OpenSCAD-focused runtime + SCons transport/reuse**.

There is no code, release or ownership dependency from `lib.scad.hub75` on a qualified `lib.scad.clamps` revision. The earlier Step-5 → Step-6 gate therefore serialized independent evidence unnecessarily. Both canaries may now be implemented and qualified concurrently after Steps 1–4. Step 7 remains gated on **both** canaries, because downstream migration should not start until both execution modes are proven.

If either canary exposes a defect in a shared owner (`tool.git-project`, `tool.scad-project` or `docker.scad-toolchain`), fix and release that shared owner first, then re-pin/requalify whichever canaries are affected.

## Step 1 — runtime image family

Owners:

- `brainboxemb/docker.scad-toolchain`
- `brainboxemb/docker.scad-toolchain.test`

Result:

- full/dual image: `ghcr.io/brainboxemb/scad-toolchain:v0.5.0`;
- focused image: `ghcr.io/brainboxemb/scad-toolchain-openscad:v0.5.0`;
- one external test suite qualifies both;
- focused profile avoids about 121 MB / 27% of compressed distribution relative to the full image.

Gate: **met**.

## Step 2 — affected capability list

Owner: `brainboxemb/tool.git-project`.

Result: `v0.2.8` exposes the complete normalized affected-task list from the same generic Moon query while retaining the compatibility boolean and conservative-failure behaviour.

The current action still needs one existing task as a query anchor. The result list itself is repository-wide. The current reference consumers all expose `scad.docs`, so this is not a blocker for Migration 005.

Gate: **met**.

## Step 3 — shared SCAD capability lifecycle

Owner: `brainboxemb/tool.scad-project`.

### Released result

Current consumer foundation:

- `v0.14.2` / `5712324ea9e3a7c81ba1b79013f2758f52b219cf`.

The original Step-3 release was `v0.14.0`. Step-4 integration then found two owner-side defects that were deliberately corrected in the owner repository rather than worked around in the template:

1. **v0.14.1** — normal production planner installation no longer assumes global `setuptools`/`wheel`; PEP 517 installs declared build requirements in a clean hosted Python environment (`tool.scad-project#56`).
2. **v0.14.2** — inherited capability selection is read from project-level `moon.yml` (`workspace.inheritedTasks.include`), matching Moon 2.5.4; `.moon/workspace.yml` remains workspace-level configuration (`tool.scad-project#57`).

### Stable lifecycle contract

Shared inherited capability tasks cover:

- `scad.docs` — design documentation;
- `scad.build` — presentation renders;
- `scad.verify` — Verification.

Shared policy owns commands, stable common inputs, normal output boundaries and Moon cache policy. Consumers own capability selection and project-specific impact patterns.

Runtime selection is configuration-driven. SCons transport is enabled only for SCons-configured work. Source-affected capabilities and publication-safe materialization remain separate concepts when complete Build replacement requires an unchanged contributor to be hydrated.

Gate: **met**.

## Step 4 — template/reference consumer model

Owner: `brainboxemb/template.scad-project`.

Status: **complete implementation; immutable release follow-through in progress**.

Owner PR:

- `template.scad-project#37`;
- merged as `cf3da65943968a42f3a0199cb682b1c74f452ee9`.

Implemented reference model:

- root `moon.yml` selects `scad.docs`, `scad.build`, `scad.verify` and contains project-specific impact inputs;
- `.moon/tasks/scad.yml` is the single inherited-policy link;
- `.moon/workspace.yml` is limited to valid workspace-level configuration;
- consumer-authored Migration-004 aggregate/lifecycle tasks are gone;
- `tool.git-project v0.2.8`, `tool.scad-project v0.14.2` and runtime-family v0.5.0 are the released foundations;
- template intentionally remains dual-runtime and SCons-enabled so it exercises the broad reference path.

Acceptance evidence:

- full integration source before final documentation-only corrections: `d439fe6dfcf968471891974177a1773678aa3d24`;
- run `35020468894` — green;
- one exact base → source Moon affected query;
- clean planner install succeeded;
- effective capabilities: docs/build/verify;
- selected runtime: full `ghcr.io/brainboxemb/scad-toolchain:v0.5.0`;
- build engine: SCons;
- normal and Verification SCons caches both applicable and restored;
- all required capabilities materialized in one Docker process;
- Build and Verification publication both succeeded;
- normal Actions retention contained compact orchestration evidence, not duplicate complete output trees.

The final README/AGENTS/CI-documentation corrections only aligned the documented Moon configuration location with the already released v0.14.2 owner fix; they did not change the qualified execution topology or pins.

The reference consumer still needs its next immutable project release after v0.0.2. That release is Step-4 follow-through, but neither Step 5 nor Step 6 consumes `template.scad-project`, so it does not block the canaries.

Gate: **implementation met; release follow-through must still be recorded**.

## Step 5 — migrate and qualify `lib.scad.clamps` as the dual-runtime/direct canary

Owner: `brainboxemb/lib.scad.clamps`.

Purpose:

- intentionally supports OpenSCAD and PythonSCAD;
- uses the direct engine;
- therefore proves the full/dual runtime path while proving unused SCons transport is absent.

Expected visible capabilities:

```text
Design documentation
Verification
```

Required evidence:

- README-only/unrelated → zero CAD runtime;
- docs-only and Verify-only boundaries behave as declared;
- full/dual image is selected from PythonSCAD configuration;
- no normal or Verification SCons cache restore/save occurs unless the repository configuration genuinely requires it;
- stable Moon capability hashes across fresh runners;
- warm Moon reuse avoids actual capability work;
- normal full-tree Actions artifacts are absent by default;
- published Build/Verification content remains correct;
- feedback latency and total runner/resource counts are recorded.

Canary completion gate:

- qualified clamps main and, if appropriate, an immutable clamps release on the Migration-005 model.

This gate does **not** block Step 6. It contributes to the joint gate for Step 7.

## Step 6 — migrate and qualify `lib.scad.hub75` as the OpenSCAD/SCons canary

Owner: `brainboxemb/lib.scad.hub75`.

Status: **active in parallel with Step 5**.

Purpose:

- prove focused OpenSCAD runtime selection;
- prove SCons cache transport remains useful and correctly scoped;
- prove three independently affected capabilities.

Expected visible capabilities:

```text
Presentation renders
Design documentation
Verification
```

Required evidence:

- README-only/unrelated → zero CAD runtime;
- Build/docs/Verify boundaries behave as declared;
- OpenSCAD-focused image is selected because PythonSCAD is not configured;
- normal and Verification SCons transport occurs only where the configured targets genuinely use it;
- warm SCons reuse is useful and correctly scoped;
- stable Moon capability hashes across fresh runners;
- warm Moon reuse avoids actual capability work where applicable;
- normal full-tree Actions artifacts are absent by default;
- published Build/Verification content remains correct;
- feedback latency and total runner/resource counts are recorded.

Canary completion gate:

- qualified HUB75 main and an immutable HUB75 library release where appropriate.

This gate does **not** depend on Step 5. Together with the Step-5 gate it unlocks Step 7.

## Step 7 — downstream SCAD consumers, HUB75 frame later

Owners: each consumer repository owns its own migration.

Prerequisites:

- Steps 1–4 complete;
- **both Step-5 and Step-6 canary gates met**;
- immutable released tool/image/library refs exist where required by downstream consumers;
- both dual/direct and OpenSCAD/SCons canary modes are proven.

`brainboxemb/2026-009-01.cad.HUB75-display-frame` remains deliberately later. Do not migrate it before both canaries qualify the released architecture.

For each consumer, derive capabilities from current repository intent, preserve repository-specific verification/publication semantics and record before/after latency/resource evidence.

## Step 8 — close Migration 005

Owner: `brainboxemb/brainboxemb.meta`.

Close only when the intended consumer rollout is complete and measured implementation evidence replaces provisional values. Record final immutable refs, architecture corrections learned during implementation and close tracking issue #55 when no Migration-005 implementation work remains.

## Sequencing principle

```text
runtime images + external contract       complete
        |
generic Moon affected-list contract      complete
        |
shared SCAD capability lifecycle          complete (current v0.14.2)
        |
template/reference consumer               complete implementation
        |
        +-------------------------------+
        |                               |
        v                               v
clamps dual/direct canary         HUB75 OpenSCAD/SCons canary
        |                               |
        +---------------+---------------+
                        |
                        v
                 downstream consumers
```
