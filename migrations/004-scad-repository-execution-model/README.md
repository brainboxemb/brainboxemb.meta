# Migration 004 — SCAD repository execution model

Status: **active**

Tracking issue: [#49](https://github.com/brainboxemb/brainboxemb.meta/issues/49)

Implementation change request: [change-request.md](change-request.md)

Qualification evidence: [evidence.md](evidence.md)

## Purpose

Align current SCAD repositories on one understandable execution model and remove avoidable CI overhead.

The migration uses:

- Moon for repository-level orchestration and affected/preflight decisions;
- SCons for the already-qualified fine-grained SCAD target decisions;
- one normal SCAD production job/container when affected;
- logically independent Build and Verify domains;
- lightweight publication outside the SCAD container.

A key completion criterion is that a README-only or otherwise unaffected change does **not** start the SCAD toolchain container.

## Progress

### Step 1 — generic Moon affected preflight

**Complete.** `tool.git-project v0.2.5` introduced the released host-side affected decision used before expensive domain jobs. During Step 3 integration, aggregate/upstream affected propagation was found to be incomplete in v0.2.5; that generic correction was qualified and released as `tool.git-project v0.2.6` from `5e004f0cee53648d6b6284b014b26bed502d2da2`.

### Step 2 — reference task-graph correction

**Complete.** `template.scad-project` PR #22 removed the stale `scad.verify -> scad.build` dependency after confirming Verify does not consume normal Build output. Merge/exact-main revision: `082b0cecb47ba082899214751080adc54556e94c`. PR run `34893868011` and exact-main run `34894004036` passed with Build and Verification publication intact.

### Step 3 — shared SCAD production workflow

**Complete.** Owner: `tool.scad-project`.

The reusable production workflow is released as `tool.scad-project v0.13.0` from exact main `da57820fdadd7d203091b6818984991f1548408f`.

The final workflow provides:

- a host-side shallow/blobless Moon affected preflight;
- exact shallow BASE fetching without `fetch-depth: 0`;
- an optional source-impact `affected_task` separate from the publication-ready execution `aggregate_task`;
- one conditional SCAD container job;
- explicit production `MOON_BASE` / `MOON_HEAD` context and conservative missing-base fallback;
- separate normal and verification SCons caches;
- generic Moon materialization validation;
- lightweight Build and Verification publication outside the SCAD container.

Release run `34938168129` and released-tag Test run `34938179069` passed.

### Step 4 — released workflow in the reference template

**Complete.** Owner: `template.scad-project`.

PR #29 consumed released `tool.scad-project v0.13.0` from a fresh branch based on the Step-2 template main and replaced the copied production implementation with the thin released reusable workflow caller. It also separated source-impact gating from publication-ready execution and narrowed Verify inputs to the CAD source actually consumed by the verification entrypoints so Build-only and Verify-only producer impact are representable without artificial dependencies.

- final PR head: `ea99880acef81cf8f6d9aab9e0371caae63af9c6`;
- final PR-head run `34944252421` — passed;
- merge/exact main: `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`;
- exact-main run `34945239139` — passed with one SCAD production container and both production publication jobs.

Final-head isolated proofs:

- README-only PR #30 / run `34944598444` — host preflight succeeded; production and both publication jobs skipped before any SCAD container;
- Verify-only PR #31 / run `34944622039` — affected set contains `scad.verify` but not `scad.build` or `scad.docs`; one production job and both lightweight publication jobs passed;
- Build-side-only PR #33 / run `34944404186` — affected set contains the Build/Docs producer branch but not `scad.verify`; one production job and both lightweight publication jobs passed.

Cold baseline run `34938849331` built all reference Build, Design and Verify targets. The later warm final run restored all CAD target work through SCons cache while retaining current orchestration/materialization evidence. An exact-source rerun restored the portable Moon cache but Moon still executed the graph; this is retained as a non-blocking generic performance observation on `tool.git-project` issue #17 rather than expanding Migration 004.

### Step 5 — reference library qualification

**Active, paused for performance reassessment.** Owner: `lib.scad.clamps`.

Draft PR #7 has already proven that the common execution model is functionally suitable for the reference library without inventing a dummy Build task. Candidate `bb071329e1d6c764d09f87ecd2cc78d42ac73679` uses released `tool.scad-project v0.13.0`, one producer-impact preflight, one heavy SCAD production job, library-specific `scad.docs` and `scad.verify` producers, and lightweight Build/Verification publication.

Functional evidence is green:

- final candidate run `34947426305` — one SCAD container, library-specific OpenSCAD/PythonSCAD design and consumer verification, aggregate materialization and both host publication jobs passed;
- proof PR #8 / run `34947599096` — README-only returns `affected=false`; production and both publication jobs are skipped before container startup;
- proof PR #9 / run `34947625311` — docs-only input affects `scad.docs` but not `scad.verify`;
- proof PR #10 / run `34947539588` — Verify-only input affects `scad.verify` but not `scad.docs`.

The required before/after measurement exposed a stop-condition trade-off:

- old parallel Build/Verify CI: about **37 s** critical path with **two** SCAD-container startups and roughly 69 heavy-runner seconds;
- common lifecycle, two successful representative runs: about **64–65 s** end-to-end with **one** SCAD-container startup and roughly comparable total runner-seconds;
- README-only improves strongly to a short host preflight with **zero** SCAD containers.

Relevant-change feedback is therefore about 27 s slower even though heavy setup is consolidated. This is material enough to trigger the migration's explicit reassessment rule. PR #7 remains draft; do not start Step 6 yet.

Performance experiment [#53](https://github.com/brainboxemb/brainboxemb.meta/issues/53) now compares, using repeated measurements:

1. the released job-level Docker lifecycle;
2. the actual historical cached-host SCAD tooling mechanism reconstructed from repository history, with cold and warm cache behavior;
3. if ownership remains generic, one host-orchestrator job that performs preflight, conditionally executes exactly one Docker SCAD toolchain, and then publishes on the host without extra GitHub job transitions.

The experiment must compare critical path, runner-seconds, toolchain setup/cache/container startup, producer time, publication, evidence correctness, reproducibility and maintenance cost. Continue Step 5 only after the experiment yields a documented recommendation and any required shared-tooling change has been implemented/released in the correct owner repository.

## Reference repositories

- `template.scad-project` — reference project;
- `lib.scad.clamps` — reference library;
- `lib.scad.hub75` — second library qualification;
- `2026-009-01.cad.HUB75-display-frame` — realistic project requalification if needed.

## Owner sequence

1. `tool.git-project` — generic Moon affected/preflight capability — complete;
2. `template.scad-project` — correct the Build/Verify task graph — complete;
3. `tool.scad-project` — reusable SCAD production workflow — complete, released as v0.13.0;
4. `template.scad-project` — qualify the released shared workflow and pre-container skip — complete;
5. `lib.scad.clamps` — reference library rollout and rationale — active, paused on performance experiment #53;
6. `lib.scad.hub75` — second library rollout — blocked by Step 5 decision;
7. HUB75 frame — requalify when shared changes affect it.

Each step must be re-evaluated before implementation. Do not continue merely because it appears in this sequence.

## Explicitly outside this migration

Whether Moon should replace SCons as the SCAD target engine is a separate parked experiment tracked by meta issue #51.

Physical HUB75 verification work such as SQ-01 is also outside this migration.
