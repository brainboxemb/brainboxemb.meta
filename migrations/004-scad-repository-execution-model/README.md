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

The first reusable production workflow is released as `tool.scad-project v0.13.0` from exact main `da57820fdadd7d203091b6818984991f1548408f`.

Its qualified contract provides:

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

**Active; functionally qualified, paused for shared tooling correction.** Owner: `lib.scad.clamps`.

Draft PR #7 proved the common execution semantics are suitable for the reference library without inventing a dummy Build task. Candidate `bb071329e1d6c764d09f87ecd2cc78d42ac73679` uses released `tool.scad-project v0.13.0`, library-specific `scad.docs` and `scad.verify` producers, one affected gate and one aggregate materialization boundary.

Functional evidence is green:

- candidate run `34947426305` — one SCAD container, library-specific OpenSCAD/PythonSCAD design and consumer verification, aggregate materialization and both host publication jobs passed;
- proof PR #8 / run `34947599096` — README-only returns `affected=false`; no SCAD container starts;
- proof PR #9 / run `34947625311` — docs/design-only input affects `scad.docs` but not `scad.verify`;
- proof PR #10 / run `34947539588` — Verify-only input affects `scad.verify` but not `scad.docs`.

The required before/after measurement exposed a material relevant-change latency regression:

- old parallel Build/Verify CI: about **37 s** critical path with **two** SCAD containers;
- released v0.13.0 lifecycle: about **64–65 s** with **one** SCAD container;
- README-only remains a short host preflight with **zero** SCAD containers.

Experiment #53 is now **complete**. It separated the runtime question from the GitHub workflow-topology question.

Runtime result:

- keep `ghcr.io/brainboxemb/scad-toolchain:v0.4.1` as the immutable SCAD execution environment;
- historical/cached host OpenSCAD and an exact-binary host bundle did not reproduce the Docker EGL/output behavior reliably;
- explicit Docker execution preserves the qualified runtime and byte-identical reference output.

Workflow-topology result on the exact Step-5 clamps candidate:

- one-host-job variant C, run `34955615827`: **41.024 s** measured relevant lifecycle;
- second variant-C run `34955904779`: **45.169 s** measured relevant lifecycle;
- README-only controls: **4.369 s** and **4.819 s**, both with zero container starts;
- both relevant runs used one SCAD container, successful current-source `consumer:scad.ci` materialization and two real host publications after the Docker process exited.

The selected direction is therefore:

```text
one host job
  -> Moon affected preflight
  -> if affected: docker run exact SCAD toolchain
  -> validate/stage after container exit
  -> host publication in the same job
```

The gain comes from removing serial GitHub job/artifact handoffs, **not** from replacing Docker.

Before PR #7 may continue, two shared-owner prerequisites are required:

1. `tool.git-project` must expose its existing generated-output publication safety contract as a reusable same-job action/script while retaining the current reusable publisher workflow as a thin wrapper, then release it;
2. `tool.scad-project` must consume that released primitive and release the one-host-job lifecycle with conditional Docker execution, exact-source/materialization validation and the existing conservative fallback.

After those releases, Step 5 resumes in `lib.scad.clamps` PR #7 and repeats the retained functional/performance qualification. Step 6 must not start before that is complete.

See [performance-evidence.md](performance-evidence.md) for exact runtime/lifecycle measurements and the ownership rationale.

## Reference repositories

- `template.scad-project` — reference project;
- `lib.scad.clamps` — reference library;
- `lib.scad.hub75` — second library qualification;
- `2026-009-01.cad.HUB75-display-frame` — realistic project requalification if needed.

## Owner sequence

1. `tool.git-project` — generic Moon affected/preflight capability — complete;
2. `template.scad-project` — correct the Build/Verify task graph — complete;
3. `tool.scad-project` — initial reusable SCAD production workflow — complete, released as v0.13.0;
4. `template.scad-project` — qualify the released shared workflow and pre-container skip — complete;
5. `lib.scad.clamps` — reference library rollout — active; paused on the shared single-job prerequisite;
   - `tool.git-project` same-job generated-output publisher primitive — **next**;
   - `tool.scad-project` single-host orchestrator workflow — follows after the released publisher primitive;
   - then resume the clamps PR #7 qualification;
6. `lib.scad.hub75` — blocked until Step 5 completes;
7. HUB75 frame — requalify when shared changes affect it.

Each step must be re-evaluated before implementation. Do not continue merely because it appears in this sequence.

## Explicitly outside this migration

Whether Moon should replace SCons as the SCAD target engine is a separate parked experiment tracked by meta issue #51.

Physical HUB75 verification work such as SQ-01 is also outside this migration.
