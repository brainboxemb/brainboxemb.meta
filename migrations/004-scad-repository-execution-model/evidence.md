# Migration 004 qualification evidence

Status: **active**

Tracking: meta issue #49.

## Step 1 — generic Moon affected preflight

Status: **complete**

Owner: `brainboxemb/tool.git-project`.

Initial released capability: `tool.git-project v0.2.5`.

Exact v0.2.5 source commit:

```text
ce7c81c39ebc70933b4150028aa74d928a53c2ba
```

Owner work:

- issue/PR #21 — `Add generic Moon affected preflight`;
- reusable action: `moon/affected`;
- Linux wrapper: `moon-affected.sh`;
- Windows wrapper: `moon-affected.ps1`;
- retained query/decision evidence under `.moon/preflight`.

Qualified behavior with real Moon 2.5.4 and real Git commits:

- README-only change outside task inputs => `affected=false`;
- configured task-input change => `affected=true`;
- missing base revision => conservative `affected=true`;
- explicit base/head ranges are used;
- preflight queries do not execute the producer;
- Linux and native Windows behavior match;
- reusable composite action itself is exercised in CI.

PR-head qualification on `6ec28d7bd77e789a8867e8c8326d81a9c2d066ed`:

- Moon production orchestration run `34886865162` — Linux and Windows green;
- Self-test Git project tooling `34886865079` — green;
- generic release lifecycle `34886865532` — green;
- generated output publication `34886865453` — green;
- PR preview cleanup `34886865539` — green;
- execution evidence schema `34886865072` — green.

Release:

- tag `v0.2.5` points to exact main `ce7c81c39ebc70933b4150028aa74d928a53c2ba`;
- release run `34887174233` completed successfully.

During Step 3 real-consumer qualification, v0.2.5 exposed a generic aggregate-gating false-negative: constituent upstream tasks could be affected while the requested aggregate itself was not directly affected. The correction remained generic, used Moon's own affected graph propagation and introduced no SCAD path rules.

Corrected released capability:

- `tool.git-project v0.2.6`;
- exact release source `5e004f0cee53648d6b6284b014b26bed502d2da2`.

A duplicate v0.2.5 release run (`34887175316`) failed only because the successful run had already created the exact tag. Generic release idempotency is tracked separately as `tool.git-project` issue #22 and does not block Migration 004.

## Step 2 — reference task-graph correction

Status: **complete**

Owner: `brainboxemb/template.scad-project`.

Owner work:

- PR #22 — `Make SCAD Build and Verify logically independent`;
- merge/exact-main revision: `082b0cecb47ba082899214751080adc54556e94c`;
- stale `scad.verify -> scad.build` dependency removed after confirming Verify does not consume normal Build output;
- `scad.ci` remains the aggregate root;
- Build-only, Verify-only and aggregate semantics remain distinct.

Qualification:

- PR run `34893868011` — passed;
- exact-main run `34894004036` — passed;
- Build and Verification publication remained intact.

Performance observation relevant to Step 3:

- SCAD job container initialization was about 17 s on the PR run and about 30 s on exact main, before checkout;
- this strengthened pre-container gating as a required acceptance criterion rather than a later optimization.

## Step 3 — shared SCAD production workflow

Status: **complete and released**

Owner: `brainboxemb/tool.scad-project`.

### Minimal checkout prerequisite

Moon 2.5.4 was qualified with only the exact shallow HEAD and exact shallow BASE commits locally present, with intervening history unavailable:

- proof run `34895987723` — normal successful affected decision;
- `fetch-depth: 0` is not required for the explicit `base -> head` preflight.

### Generic affected correction discovered during integration

The first real template qualification exposed the v0.2.5 aggregate-propagation gap. That was fixed in `tool.git-project`, released as v0.2.6, and then consumed by the Step 3 workflow before qualification continued.

### Owner implementation

- `tool.scad-project` PR #51 — reusable SCAD production workflow with pre-container gate;
- final PR head: `f71590631fdc1d278f2bcecbee46fdcc696b7429`;
- owner PR Test run `34935383752` — passed;
- merge/exact implementation main: `94edde1527048a054de170cb8c1cb63f7e272ff3`;
- exact-main implementation Test run `34936204512` — passed.

Final workflow contract:

- host-side shallow/blobless exact-source checkout;
- exact shallow BASE fetch only;
- released `tool.git-project/moon/affected@v0.2.6` preflight before the SCAD container;
- optional source-impact `affected_task`, defaulting to `aggregate_task`;
- exactly one normal heavy SCAD container when affected;
- explicit production `MOON_BASE` / `MOON_HEAD` context;
- `MOON_FORCE=true` conservative fallback with source-as-base/head when comparison context is unavailable;
- separate Build and Verification SCons caches;
- one publication-ready Moon aggregate execution/materialization boundary;
- generic materialization validation;
- Build and Verification output staged in the heavy job;
- generated-output publication delegated to lightweight `tool.git-project` jobs outside the SCAD container.

### Reference-consumer qualification against exact PR head

Temporary qualification branch: `template.scad-project` PR #23. This PR exists only as pre-release integration evidence and must not be merged as Step 4.

Corrected qualification baseline:

- template head `a5ae867e0228df78c407478a08eabd3557958beb`;
- pinned tool head `f71590631fdc1d278f2bcecbee46fdcc696b7429`;
- baseline run `34935553530` — preflight, one SCAD container, Build/Verify aggregate materialization and both publication jobs passed.

The real README-only proof first exposed a second important integration issue: publication/index tasks with configured non-empty CI environment inputs are correctly considered affected by Moon and therefore cannot safely double as the heavy-container source-impact gate. The final contract separates:

- `affected_task` — producer/source-impact gate target;
- `aggregate_task` — publication-ready execution target.

Retained isolated consumer proofs after that correction:

- README-only PR #25, run `34935678113` — `affected=false`, reason `target-and-upstream-unaffected`; SCAD production and both publication jobs skipped;
- missing/invalid-base PR #26, run `34935787742` — `affected=true`, `status=conservative`, missing-base reason; one production job, materialization and both publication jobs passed;
- verification-only PR #27, run `34935860495` — only `vrf/README.md` changed; affected route reached the source-impact aggregate through `scad.verify`, not `scad.build`; one production job and both publication jobs passed;
- representative SCAD-source PR #28, run `34936003043` — only `dsg/openscad/main.scad` changed; source-impact route was producer-driven and one production job plus both publication jobs passed.

The earlier README-only PR #24/run `34935152313` is retained as failure evidence that motivated the `affected_task` / `aggregate_task` split.

### Release

Release preparation:

- PR #52 — `Prepare tool.scad-project v0.13.0`;
- final release-PR head `d917b83e8d36207a06c4c1bad6474dd8e936be67`;
- release-PR Test run `34937968007` — passed, 209 tests;
- release merge/exact main `da57820fdadd7d203091b6818984991f1548408f`;
- exact-main Test run `34938102439` — passed.

Immutable release:

- annotated tag `v0.13.0` points to exact commit `da57820fdadd7d203091b6818984991f1548408f`;
- tag object `a2d3a9356da396da9b6fed4e870aa1a5fa26448a`;
- release run `34938168129` — passed;
- released-tag Test run `34938179069` — passed.

Step 3 acceptance is therefore satisfied with a released shared interface rather than only PR-head behavior.

## Step 4 — released workflow in reference template

Status: **next**

Owner: `brainboxemb/template.scad-project`.

Start from current template `main`, not from temporary qualification PR #23. Consume released `tool.scad-project v0.13.0` and requalify the released interface. Required scenarios remain:

- cold relevant production;
- unchanged/rehydration path;
- README-only PR with no SCAD container startup;
- Build-only source impact where representable by the reference graph;
- Verify-only source impact;
- explicit Build/Verify logical independence;
- aggregate production/materialization;
- lightweight publication outside the SCAD container.
