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

**Complete.** `tool.git-project v0.2.5` provides the released host-side affected decision used before expensive domain jobs. Exact released source: `ce7c81c39ebc70933b4150028aa74d928a53c2ba`.

### Step 2 — reference task-graph correction

**Complete.** `template.scad-project` PR #22 removed the stale `scad.verify -> scad.build` dependency after confirming Verify does not consume normal Build output. Merge/exact-main revision: `082b0cecb47ba082899214751080adc54556e94c`. PR run `34893868011` and exact-main run `34894004036` passed with Build and Verification publication intact.

### Step 3 — shared SCAD production workflow

**Next.** Owner: `tool.scad-project`.

Extract the reusable production workflow with a host-side Moon preflight, a conditional single SCAD container job and lightweight publication jobs. Before fixing the checkout contract, qualify Moon 2.5.4 `changed-files --base <sha> --head <sha>` with only the exact base and head commits locally present. The current template is blobless but uses `fetch-depth: 0`; that broad history fetch must not be copied into the new preflight unless the focused qualification proves it is necessary.

## Reference repositories

- `template.scad-project` — reference project;
- `lib.scad.clamps` — reference library;
- `lib.scad.hub75` — second library qualification;
- `2026-009-01.cad.HUB75-display-frame` — realistic project requalification if needed.

## Owner sequence

1. `tool.git-project` — generic Moon affected/preflight capability — complete;
2. `template.scad-project` — correct the Build/Verify task graph — complete;
3. `tool.scad-project` — reusable SCAD production workflow — next;
4. `template.scad-project` — qualify the released shared workflow and pre-container skip;
5. `lib.scad.clamps` — reference library rollout and rationale;
6. `lib.scad.hub75` — second library rollout;
7. HUB75 frame — requalify when shared changes affect it.

Each step must be re-evaluated before implementation. Do not continue merely because it appears in this sequence.

## Explicitly outside this migration

Whether Moon should replace SCons as the SCAD target engine is a separate parked experiment tracked by meta issue #51.

Physical HUB75 verification work such as SQ-01 is also outside this migration.
