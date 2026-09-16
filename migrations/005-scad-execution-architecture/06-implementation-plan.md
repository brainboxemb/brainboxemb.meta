# Migration 005 — implementation plan

Status: **active migration execution — Steps 1–6 complete; Step 7 is next**

## Why this document exists

This is the operational owner-by-owner rollout plan for the validated Migration-005 architecture. The architecture itself is fixed in [05 — Validated target architecture](05-target-architecture.md); this page determines which repository changes next and what evidence gates the following step.

Do not bundle unrelated owner changes merely to reduce pull-request count. If integration exposes an owner defect, fix and release it in that owner repository before continuing the affected consumer step.

## Current progress

- **Step 1 — runtime image family:** complete. `docker.scad-toolchain v0.5.0` released from `a56a3aae4b9e0494e6625e75002d96b0a55986a3`; immutable profiles externally qualified in run `34999654405`.
- **Step 2 — affected capability list:** complete. `tool.git-project v0.2.8` released from `7c43f37e7b07cfb57638a1d1dad2501de09ba7eb`.
- **Step 3 — shared SCAD capability lifecycle:** complete. Current consumer foundation is **`tool.scad-project v0.14.3` / `b86b2be325f64847b8d91b7f2596bfd4e4ffb7f2`**.
- **Step 4 — template/reference consumer model:** complete. Migration implementation merged in `template.scad-project#37`; maintainable source-family impact boundaries were corrected in #39 and released as **`template.scad-project v0.0.4`** from `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9`.
- **Step 5 — clamps dual-runtime/direct canary:** complete. PR #16 merged as `a44d7bdfdb3407959b5d96bef654568367e0f43c`; migrated `main` production run `35065375255` is green; README-only zero-runtime qualification run `35065514152` is green.
- **Step 6 — HUB75 OpenSCAD/SCons canary:** complete. PR #29 merged as `ea75cee1fa83310bc2ba2ad1ce565ef81ac7f523`; migrated `main` production run `35065383879` is green; README-only zero-runtime qualification run `35065524524` is green.
- **Step 7 — downstream SCAD consumers:** **next**.
- **Step 8 — close Migration 005:** waits for the intended downstream rollout and final evidence.

## Shared foundation corrections learned during rollout

The original Step-3 release was `tool.scad-project v0.14.0`. Integration deliberately fixed shared defects in the owner repository instead of adding consumer workarounds:

1. **v0.14.1** — planner installation uses declared PEP 517 build requirements in a clean hosted Python environment (`tool.scad-project#56`).
2. **v0.14.2** — inherited capability selection comes from project-level root `moon.yml` via `workspace.inheritedTasks.include`, matching Moon 2.5.4 (`tool.scad-project#57`).
3. **v0.14.3** — shared Moon capability outputs no longer require optional SCons state files that do not exist for direct-engine consumers or command-only verification (`tool.scad-project#59`).

Current shared consumer foundation:

```text
docker.scad-toolchain   v0.5.0
tool.git-project        v0.2.8
tool.scad-project       v0.14.3 / b86b2be325f64847b8d91b7f2596bfd4e4ffb7f2
```

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

Result: `v0.2.8` exposes the complete normalized affected-task list from one generic Moon query while retaining compatibility and conservative-failure behaviour.

Gate: **met**.

## Step 3 — shared SCAD capability lifecycle

Owner: `brainboxemb/tool.scad-project`.

Shared inherited capability tasks cover:

- `scad.docs` — design documentation;
- `scad.build` — presentation renders;
- `scad.verify` — Verification.

Shared policy owns commands, stable common inputs, normal output boundaries and Moon cache policy. Consumers own capability selection and project-specific source-family impact patterns.

Runtime selection is configuration-driven. SCons transport is enabled only for SCons-configured work. Source-affected capabilities and publication-safe materialization remain separate concepts when complete Build replacement requires an unchanged contributor to be hydrated.

Gate: **met on v0.14.3**.

## Step 4 — template/reference consumer model

Owner: `brainboxemb/template.scad-project`.

Result:

- Migration implementation PR #37 merged as `cf3da65943968a42f3a0199cb682b1c74f452ee9`;
- full integration run `35020468894` qualified the three-capability full-runtime/SCons reference path;
- PR #39 replaced brittle file-by-file Moon inputs with maintainable source-family boundaries;
- immutable project release **v0.0.4** was published from `601e9f6fc7c297a5012cbf2aae0c5b95de4335c9` with Build, Verification, STL and checksum assets.

Reference model:

- root `moon.yml` selects visible capabilities and project-specific source-family impact boundaries;
- `.moon/tasks/scad.yml` inherits the shared implementation;
- `.moon/workspace.yml` remains workspace-level configuration;
- consumer-authored Migration-004 lifecycle/aggregate tasks are gone.

Gate: **met**.

## Step 5 — `lib.scad.clamps` dual-runtime/direct canary

Owner: `brainboxemb/lib.scad.clamps`.

Purpose:

- OpenSCAD + PythonSCAD intentionally select the full/dual runtime;
- direct engine proves that unused normal and Verification SCons transport stays absent.

Result:

- migration PR #16 merged as `a44d7bdfdb3407959b5d96bef654568367e0f43c`;
- final PR qualification run `35026709686` was green on v0.14.3;
- migrated `main` production run `35065375255` was green;
- full/dual runtime selected;
- direct engine selected;
- normal SCons cache transport skipped;
- Verification SCons cache transport skipped;
- Build/Verification publication completed successfully;
- normal Actions retention stayed compact;
- temporary README-only qualification PR #17 produced run `35065514152`, where planner installation, all cache transport, runtime pull, Docker materialization, finishing and publication were all skipped; PR #17 was closed without merge after evidence capture.

Gate: **met**.

## Step 6 — `lib.scad.hub75` OpenSCAD/SCons canary

Owner: `brainboxemb/lib.scad.hub75`.

Purpose:

- focused OpenSCAD runtime selection;
- normal SCons cache transport/reuse;
- independent Build, Design documentation and Verification capabilities.

Result:

- migration PR #29 merged as `ea75cee1fa83310bc2ba2ad1ce565ef81ac7f523`;
- final PR qualification run `35026885840` was green on v0.14.3;
- migrated `main` production run `35065383879` was green;
- OpenSCAD-focused runtime selected;
- normal SCons transport enabled and used;
- Verification SCons transport correctly skipped because this consumer has no verification render/export targets;
- Build and Verification publication completed successfully;
- normal Actions retention stayed compact;
- temporary README-only qualification PR #30 produced run `35065524524`, where planner installation, all cache transport, runtime pull, Docker materialization, finishing and publication were all skipped; PR #30 was closed without merge after evidence capture.

Gate: **met**.

## Parallel hardening track — orchestration observability and upgrade preflight

Owner: `brainboxemb/tool.scad-project`.

Tracking item: `tool.scad-project#60`.

This is **not a reopening of Steps 5–6**. The v0.14.3 library migrations are complete and their zero-runtime gates are proven on migrated `main`.

The follow-up track improves two things discovered while reviewing canary evidence:

1. when a future tool-upgrade PR changes the `tools/tool.scad-project` gitlink, shallow BASE/HEAD preflight should also make the exact base gitlink object available so Moon does not need a conservative fallback merely because that old tool commit is absent;
2. generated output should expose the retained full orchestration/Moon log clearly and preserve durable timing information for major workflow phases, because GitHub Actions step timing is not a permanent evidence store.

Qualification order for this hardening track:

```text
tool.scad-project owner tests/release
        |
        v
template.scad-project first integration/reference qualification
        |
        v
only then decide whether/when existing libraries should adopt the patch
```

Do not repin clamps or HUB75 to this follow-up merely because a patch exists. First prove it through the template/reference consumer. A correctness regression found there blocks rollout of that patch, but does not invalidate the already completed v0.14.3 canary migration.

## Step 7 — downstream SCAD consumers

Owners: each consumer repository owns its own migration.

Prerequisites now met:

- Steps 1–4 complete;
- both Step-5 and Step-6 canary gates met;
- dual/direct and OpenSCAD/SCons modes proven on migrated `main`;
- README-only/unrelated zero-runtime path proven after migration in both canaries.

For each downstream consumer:

- derive capabilities from current repository intent;
- keep source-family impact boundaries maintainable rather than enumerating individual component files;
- preserve repository-specific verification/publication semantics;
- use immutable released tool/image/library refs where the consumer requires them;
- record useful before/after latency and resource evidence.

`brainboxemb/2026-009-01.cad.HUB75-display-frame` remains deliberately later in the downstream sequence; do not infer that it must be the first Step-7 consumer.

The parallel hardening track above may continue independently. It becomes a downstream prerequisite only if it exposes a correctness defect that affects the current released architecture.

## Step 8 — close Migration 005

Owner: `brainboxemb/brainboxemb.meta`.

Close only when the intended downstream rollout is complete and measured implementation evidence replaces provisional values. Record final immutable refs, architecture corrections learned during implementation and close tracking issue #55 when no Migration-005 implementation work remains.

## Sequencing principle

```text
runtime images + external contract       complete
        |
generic Moon affected-list contract      complete
        |
shared SCAD capability lifecycle          complete (v0.14.3)
        |
template/reference consumer               complete (v0.0.4)
        |
        +-------------------------------+
        |                               |
        v                               v
clamps dual/direct canary         HUB75 OpenSCAD/SCons canary
        complete                         complete
        |                               |
        +---------------+---------------+
                        |
                        v
                 downstream consumers

parallel hardening:
tool.scad-project #60 -> template first -> optional later consumer adoption
```
