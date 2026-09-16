# Migration 005 — implementation plan

Status: **complete — Steps 1–8 closed**

## Why this document exists

This is the completed owner-by-owner rollout record for the validated Migration-005 architecture. The architecture itself is defined in [05 — Validated target architecture](05-target-architecture.md); this page records execution order, owner corrections and the evidence gates that were actually used.

The migration followed one rule throughout: when integration exposed a shared defect, fix and release it in the owner repository before continuing the affected consumer. Consumer workarounds were not accepted as substitutes for owner fixes.

## Final progress

- **Step 1 — runtime image family:** complete.
- **Step 2 — generic affected capability list:** complete.
- **Step 3 — shared SCAD capability lifecycle:** complete; final migration baseline `tool.scad-project v0.14.7`.
- **Step 4 — template/reference consumer:** complete and requalified on v0.14.7.
- **Step 5 — clamps full/dual + direct canary:** complete.
- **Step 6 — HUB75 focused OpenSCAD + SCons canary:** complete.
- **Step 7 — downstream current-generation consumers:** complete; the real HUB75 display-frame consumer is migrated and the canonical repository catalog contains no other public `tool.scad-project` consumers.
- **Step 8 — close Migration 005:** complete after final measurement/resource review and durable documentation update.

## Final shared foundation

```text
docker.scad-toolchain   v0.5.0
tool.git-project        v0.2.8 / 7c43f37e7b07cfb57638a1d1dad2501de09ba7eb
tool.scad-project       v0.14.7 / 3935e5f86fe309b8908a05554f7ada336a6d6886
```

Released-tag owner test for `tool.scad-project v0.14.7`: `35084470257`.

## Step 1 — runtime image family

Owners:

- `brainboxemb/docker.scad-toolchain`
- `brainboxemb/docker.scad-toolchain.test`

Result:

- full/dual image `ghcr.io/brainboxemb/scad-toolchain:v0.5.0`;
- focused image `ghcr.io/brainboxemb/scad-toolchain-openscad:v0.5.0`;
- release source `a56a3aae4b9e0494e6625e75002d96b0a55986a3`;
- external qualification run `34999654405`;
- focused profile removes about 121 MB / 27% of compressed distribution relative to the full image.

Gate: **met**.

## Step 2 — affected capability list

Owner: `brainboxemb/tool.git-project`.

Result: `v0.2.8` exposes the complete normalized affected-task list from one generic Moon query while retaining conservative failure behaviour.

Gate: **met**.

## Step 3 — shared SCAD capability lifecycle

Owner: `brainboxemb/tool.scad-project`.

Shared capabilities:

```text
scad.docs
scad.build
scad.verify
```

Shared policy owns commands, stable common inputs, normal output boundaries, Moon cache policy, runtime/cache planning and host finishing. Consumers own capability selection and project-specific source-family impact rules.

The original v0.14.0 lifecycle was corrected through owner releases as integration exposed real defects:

1. **v0.14.1** — clean PEP517 planner installation;
2. **v0.14.2** — correct Moon `workspace.inheritedTasks.include` placement in root `moon.yml`;
3. **v0.14.3** — optional Moon outputs no longer require SCons state files for direct/command-only consumers;
4. **v0.14.4** — exact base tool-gitlink retrieval for shallow comparisons, semantic reusable-workflow refs, shared release-request parsing/cleanup and durable orchestration navigation;
5. **v0.14.5** — shared capability launchers use the immutable runtime's guaranteed `python3` executable;
6. **v0.14.6** — durable coarse workflow phase timings in generated output;
7. **v0.14.7** — exact resolved source SHA reaches host publication finishing so PR provenance cannot fall back to a synthetic merge SHA.

Final gate: **met on v0.14.7**.

## Step 4 — template/reference consumer

Owner: `brainboxemb/template.scad-project`.

Earlier Migration-005 reference work landed through PRs #37 and #39 and project release v0.0.4. The later owner hardening line was then qualified template-first before broader adoption.

Final v0.14.7 qualification:

- exact PR head `78a000603d6a64d2b495f6e054686a128c157877`;
- run `35085388134` green;
- semantic Production/Release callers `@v0.14.7`;
- exact tool gitlink `3935e5f86fe309b8908a05554f7ada336a6d6886`;
- Build/Verification publication info, run context, Moon materialization and producer execution all identify the same exact PR-head source;
- merge `cb1e3e50e5e56644153cdf74b54b5da1e747c8d8`;
- post-merge main run `35085631904` green;
- README-only zero-runtime probe `35085786014` green.

Gate: **met**.

## Step 5 — `lib.scad.clamps` full/dual + direct canary

Owner: `brainboxemb/lib.scad.clamps`.

Result:

- migration PR #16 merged as `a44d7bdfdb3407959b5d96bef654568367e0f43c`;
- canary run `35026709686` green;
- migrated main run `35065375255` green;
- full/dual runtime selected;
- direct engine selected;
- normal and Verification SCons transport skipped;
- README-only zero-runtime run `35065514152` skipped planner, caches, runtime pull, Docker, finishing and publication;
- immutable v0.1.4 released.

Final measured affected canary: about **41.9 s**, within the intended low/mid-40 s class.

Gate: **met**.

## Step 6 — `lib.scad.hub75` focused OpenSCAD + SCons canary

Owner: `brainboxemb/lib.scad.hub75`.

Result:

- migration PR #29 merged as `ea75cee1fa83310bc2ba2ad1ce565ef81ac7f523`;
- canary run `35026885840` green;
- migrated main run `35065383879` green;
- focused OpenSCAD runtime selected;
- normal SCons transport enabled and useful;
- Verification SCons transport skipped for command-only Verification;
- README-only zero-runtime run `35065524524` skipped planner, caches, runtime pull, Docker, finishing and publication;
- immutable v0.1.5 released from `e0432a9533a08a1c0d9e87225c22f3f66b632531`.

Final warm/cached canary: about **32.2 s**, within the intended low/mid-30 s class.

Gate: **met**.

## Step 7 — downstream current-generation SCAD consumers

Owner: each consumer repository.

At closeout the canonical `repositories/catalog.yml` lists four public repositories with `project_infrastructure.provider: tool.scad-project`:

- `template.scad-project`;
- `lib.scad.clamps`;
- `lib.scad.hub75`;
- `2026-009-01.cad.HUB75-display-frame`.

The first three are Steps 4–6. The remaining downstream consumer was therefore the real HUB75 display-frame project.

Frame result:

- migration PR #33 merged as `61da023ff0f6bc353687b55a8158e75ebd70b046`;
- final branch run `35069083479` green;
- post-merge main run `35069411142` green;
- README-only probe PR #34 / run `35069504915` proved Moon `status=success`, affected task ids `[]`, `affected=false`, with planner/cache/runtime/Docker/finishing/staging/publication skipped.

Repositories still classified as **classic** are not unfinished Step-7 consumers. Moving classic standalone/shared-actions projects to the current project-tooling generation requires a separate migration with its own scope and evidence.

Gate: **met**.

## Step 8 — close Migration 005

Owner: `brainboxemb/brainboxemb.meta`.

Final evidence review:

- all current-generation consumers migrated and qualified;
- final immutable shared refs recorded;
- durable architecture documentation updated;
- final affected and unrelated-change measurements recorded in [10 — Measurements](10-measurements.md);
- target/resource outcomes recorded in [20 — Target resource budget](20-target-resource-budget.md).

The 4–6 s unrelated-change latency envelope was not fully reached: measured zero-CAD hosted-job times are approximately 7.6–9.9 s. The remaining cost is generic Actions/Moon preflight overhead and is tracked as non-blocking follow-up rather than keeping the SCAD architecture migration open.

Gate: **met; Migration 005 complete**.

## Final sequencing record

```text
runtime images                          complete
        |
generic Moon affected-list             complete
        |
shared SCAD lifecycle                   complete (v0.14.7)
        |
template/reference                     complete
        |
        +-----------------------------+
        |                             |
        v                             v
clamps full/direct              HUB75 focused/SCons
complete                       complete
        |                             |
        +---------------+-------------+
                        |
                        v
             display-frame downstream
                     complete
                        |
                        v
            final measurements/docs
                     complete
```
