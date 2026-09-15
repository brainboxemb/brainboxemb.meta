# Migration 004 — SCAD repository execution model

Status: **active**

Tracking issue: [#49](https://github.com/brainboxemb/brainboxemb.meta/issues/49)

Implementation change request: [change-request.md](change-request.md)

Qualification evidence: [evidence.md](evidence.md)

Step-5 performance evidence: [performance-evidence.md](performance-evidence.md)

## Purpose

Align current SCAD repositories on one understandable execution model and remove avoidable CI overhead.

The migration uses:

- Moon for repository-level orchestration and affected/preflight decisions;
- SCons for the already-qualified fine-grained SCAD target decisions;
- one normal SCAD Docker execution when affected;
- logically independent Build and Verify domains;
- one host orchestrator lifecycle around preflight, conditional Docker production and publication;
- publication outside the SCAD container process boundary and only after that process exits.

A key completion criterion is that a README-only or otherwise unaffected change does **not** start the SCAD toolchain container.

## Progress

### Step 1 — generic Moon affected preflight

**Complete.** `tool.git-project v0.2.5` introduced the released host-side affected decision used before expensive domain work. During Step 3 integration, aggregate/upstream affected propagation was found to be incomplete in v0.2.5; that generic correction was qualified and released as `tool.git-project v0.2.6` from `5e004f0cee53648d6b6284b014b26bed502d2da2`.

### Step 2 — reference task-graph correction

**Complete.** `template.scad-project` PR #22 removed the stale `scad.verify -> scad.build` dependency after confirming Verify does not consume normal Build output. Merge/exact-main revision: `082b0cecb47ba082899214751080adc54556e94c`. PR run `34893868011` and exact-main run `34894004036` passed with Build and Verification publication intact.

### Step 3 — shared SCAD production workflow

**Complete.** Owner: `tool.scad-project`.

The first reusable production workflow was released as `tool.scad-project v0.13.0` from exact main `da57820fdadd7d203091b6818984991f1548408f`.

Its qualified contract introduced:

- host-side shallow/blobless Moon affected preflight;
- exact shallow BASE fetching without `fetch-depth: 0`;
- an optional source-impact `affected_task` separate from the publication-ready execution `aggregate_task`;
- one conditional SCAD container;
- explicit production `MOON_BASE` / `MOON_HEAD` context and conservative missing-base fallback;
- separate normal and verification SCons caches;
- generic Moon materialization validation;
- Build and Verification publication outside the SCAD container.

Release run `34938168129` and released-tag Test run `34938179069` passed.

### Step 4 — released workflow in the reference template

**Complete.** Owner: `template.scad-project`.

PR #29 consumed released `tool.scad-project v0.13.0` and merged as exact main `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`.

- final PR-head run `34944252421` — passed;
- exact-main run `34945239139` — passed;
- README-only PR #30 / run `34944598444` — production skipped before any SCAD container;
- Verify-only PR #31 / run `34944622039` — `scad.verify` affected without Build/Docs;
- Build-side-only PR #33 / run `34944404186` — Build/Docs affected without `scad.verify`.

Cold run `34938849331` built all reference targets; the later final run restored all CAD target work through SCons cache while retaining current orchestration/materialization evidence.

### Step 5 — reference library qualification

**Complete.** Owner: `lib.scad.clamps`.

The first v0.13.0 library qualification proved the task semantics but exposed a material performance regression: relevant feedback rose from an old ~37 s parallel Build/Verify critical path with two containers to ~64–65 s with one container because preflight, production and publication had become serial GitHub jobs.

The migration stop condition triggered the dedicated performance experiment tracked in issue #53 and retained in `exp.2026-003.scad-ci-performance`.

#### Performance decision and shared correction

Runtime result:

- keep `ghcr.io/brainboxemb/scad-toolchain:v0.4.1` as the immutable SCAD execution environment;
- cached-host variants did not reproduce the qualified Docker EGL/output behavior reliably;
- the latency problem came from GitHub job/artifact boundaries, not from the Docker runtime itself.

Selected topology:

```text
one host job
  -> Moon affected preflight
  -> if affected: one explicit docker run of the exact SCAD image
  -> validate/stage after container exit
  -> host publication in the same job
```

Shared prerequisites were implemented by their owners:

- `tool.git-project v0.2.7` — same-job generated-output publication, exact source `6234b7437b0dc0115642468f74d1f4a2c2214bef`; release run `34960768652`; tagged Linux/Windows verification run `34960782984`;
- `tool.scad-project v0.13.1` — one-host-job production lifecycle, exact source `28661fc040c4994e9c1d391285b7425c7a55252b`; exact-main Test `34970279362`; release run `34970379930`; tagged Test `34970393104`.

Reference-template pre-release qualification of the v0.13.1 topology retained:

- relevant one-host/one-Docker run `34967002612`;
- README-only zero-container run `34967121183`;
- conservative missing-base proof with forced aggregate execution.

#### Released reference-library rollout

`lib.scad.clamps` PR #7 adopted released v0.13.1 and merged as exact main:

```text
c5732944c8c2ba840a3f0f2f0a0638430a796cfd
```

The library graph remains intentionally library-specific:

- `scad.docs` — generated OpenSCAD + PythonSCAD design documentation;
- `scad.verify` — OpenSCAD + PythonSCAD public-consumer PNG/STL verification;
- no artificial `scad.build` task because this repository has no normal configured render/export targets;
- `scad.production-impact` — source-impact gate;
- `scad.ci` — publication-ready aggregate.

Final released-interface evidence:

- final PR-head run `34971400621` — one host orchestrator job, one explicit Docker process, design + verification + current materialization + both host publications green; about **45 s** from reusable-workflow start through second publication with a ~20 s image pull;
- README-only proof PR #11 / run `34971644925` — `affected=false`, reason `target-and-upstream-unaffected`; no SCAD image pull/container/publication;
- docs-only proof PR #12 / run `34971733730` — retained preflight artifact `10397796125` contains `scad.docs` in the affected route and excludes `scad.verify`;
- Verify-only proof PR #13 / run `34971800074` — retained preflight artifact `10397512803` contains `scad.verify` and excludes `scad.docs`;
- exact-main production run `34972350665` — passed with one host job/one Docker and both production publications;
- `prod/build` and `prod/verification` both record exact source `c5732944c8c2ba840a3f0f2f0a0638430a796cfd` and `tool.scad-project v0.13.1`.

A first released v0.13.1 clamps run `34970821889` was also fully green but encountered a ~43.7 s GHCR pull outlier. The repeated final-head run demonstrates that the old ~64–65 s latency was structural to the v0.13.0 job topology and is no longer structural in v0.13.1.

Step 5 therefore satisfies both the functional and proportionality acceptance criteria.

See [performance-evidence.md](performance-evidence.md) for the full runtime/lifecycle comparison.

### Step 6 — second library qualification

**Next; re-evaluation required before implementation.** Owner candidate: `lib.scad.hub75`.

Before changing that repository:

- inspect its current `AGENTS.md`, main head, tool/dependency pins and current open PRs;
- reconstruct its actual Build/Verify/documentation/release graph rather than copying clamps or template mechanically;
- separate Migration 004 execution-model work from the ongoing physical-verification/SQ work;
- confirm whether its verification inputs can preserve truthful producer independence;
- identify any HUB75-library-specific outputs or release expectations that do not fit the reference-library graph;
- retain README-only zero-container, relevant one-container, logical-independence and publication evidence on the released v0.13.1 interface.

Do not start the HUB75 frame requalification unless Step 6 shows the shared/library change materially affects that consumer.

## Reference repositories

- `template.scad-project` — reference project;
- `lib.scad.clamps` — reference library, Step 5 complete;
- `lib.scad.hub75` — second library qualification, Step 6 next;
- `2026-009-01.cad.HUB75-display-frame` — realistic project requalification if needed.

## Owner sequence

1. `tool.git-project` — generic Moon affected/preflight capability — complete;
2. `template.scad-project` — correct the Build/Verify task graph — complete;
3. `tool.scad-project` — initial reusable SCAD production workflow — complete, released as v0.13.0;
4. `template.scad-project` — qualify the released shared workflow and pre-container skip — complete;
5. `lib.scad.clamps` — reference library rollout — **complete**;
   - `tool.git-project` same-job publisher — complete/released as v0.2.7;
   - `tool.scad-project` single-host lifecycle — complete/released as v0.13.1;
   - clamps released-interface qualification and exact-main publication — complete;
6. `lib.scad.hub75` — **next**;
7. HUB75 frame — requalify only when Step 6 shows it is needed.

Each step must be re-evaluated before implementation. Do not continue merely because it appears in this sequence.

## Explicitly outside this migration

Whether Moon should replace SCons as the SCAD target engine is a separate parked experiment tracked by meta issue #51.

Physical HUB75 verification work such as SQ-01 is also outside this migration.
