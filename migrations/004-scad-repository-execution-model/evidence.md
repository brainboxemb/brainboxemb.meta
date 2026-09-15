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

Temporary qualification branch: `template.scad-project` PR #23. This PR was retained only as pre-release integration evidence and later closed without merge after the released rollout started.

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

Status: **complete**

Owner: `brainboxemb/template.scad-project`.

### Rollout implementation

- PR #29 — `Qualify released SCAD production workflow`;
- final PR head `ea99880acef81cf8f6d9aab9e0371caae63af9c6`;
- released dependency policy: `tool.scad-project v0.13.0`;
- exact tool gitlink / Production workflow / Release workflow pin: `da57820fdadd7d203091b6818984991f1548408f`;
- copied SCAD production mechanics replaced by the thin released `project-production.yml` caller;
- `scad.production-impact` added as the source-impact gate while `scad.ci` remains the publication-ready aggregate execution root;
- `scad.verify` inputs narrowed from coarse `dsg/**` to the CAD source actually consumed by the two template verification entrypoints plus their clamp dependency and the existing verification/configuration/tooling inputs.

That Verify-input correction was necessary to make the Step-4 Build-only and Verify-only scenario matrix truthful rather than merely asserting logical independence while every design change also marked Verify affected.

### Final PR-head qualification

Run `34944252421` on exact final head — passed:

- host preflight succeeded;
- exactly one SCAD production container ran;
- exact shallow production source/base range succeeded;
- exact dependencies bootstrapped successfully;
- aggregate `consumer:scad.ci` execution and generic materialization validation succeeded;
- Build and Verification publication trees were staged/uploaded by the heavy job;
- both lightweight publication jobs succeeded outside the SCAD container.

### Final isolated scenario proofs

README-only/no-container:

- proof PR #30;
- final run `34944598444` — passed;
- only the README proof file changed;
- preflight succeeded;
- SCAD production, Build publication and Verification publication were all skipped;
- therefore no SCAD container started.

Verify-only producer impact:

- proof PR #31;
- final run `34944622039` — passed;
- only `vrf/README.md` changed;
- retained affected-task evidence contains `scad.verify` but not `scad.build` and not `scad.docs`;
- exactly one production job ran;
- aggregate materialization and both lightweight publication jobs passed.

Build-side-only producer impact:

- proof PR #33;
- run `34944404186` — passed;
- only `dsg/openscad/render/tube-holder-assembly.scad` changed;
- retained affected-task evidence contains the Build/Docs producer branch but not `scad.verify`;
- exactly one production job ran;
- aggregate materialization and both lightweight publication jobs passed.

The older generic source-impact proof PR #32 was superseded by final-head Build-only proof #33 and closed without merge. All temporary Step-4 proof PRs were closed without merge after their evidence was retained.

### Cold and warm execution

First released-interface baseline run `34938849331` was cold at the SCons target layer:

- Build: 2 targets built, 0 cache-restored;
- Design: 16 targets built, 0 cache-restored;
- Verify: 2 targets built, 0 cache-restored.

Final PR-head run `34944252421` demonstrated warm target reuse:

- Build: 0 built, 2 cache-restored;
- Design: 0 built, 16 cache-restored;
- Verify: 0 built, 2 cache-restored;
- current Moon materialization evidence remained tied to exact source `ea99880acef81cf8f6d9aab9e0371caae63af9c6`.

A second attempt of the exact same production job restored the portable Moon Actions cache and both SCons caches from attempt 1. Moon still executed the seven-task graph rather than whole-task hydrating it, while SCons again restored all CAD targets. This is a performance observation, not a correctness failure: no stale producer evidence was presented as current materialization. The same-source observation was added to existing generic `tool.git-project` issue #17 instead of enlarging Migration 004.

### Merge / exact-main qualification

- PR #29 merge/exact main `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`;
- exact-main SCAD production run `34945239139` — passed;
- host preflight correctly requested production for the rollout merge;
- exactly one heavy SCAD production job passed;
- aggregate materialization validation passed;
- lightweight `prod/build` and `prod/verification` publication jobs both passed.

Step 4 acceptance is therefore satisfied on the released workflow and exact template main.

## Step 5 — reference library qualification

Status: **next; re-evaluation required before implementation**

Owner: `brainboxemb/lib.scad.clamps`.

Before editing the library, inspect its current owner guidance, normal/release workflows, current `tool.scad-project` and `tool.git-project` pins, Build/Verify semantics, publication behavior, Moon/task configuration if any, and current CI evidence. Re-check whether the common project-qualified production model remains proportionate for this small reusable library.

If the model still fits, Step 5 should retain before/after evidence for:

- normal heavy GitHub job count;
- SCAD container count;
- container initialization and checkout/bootstrap overhead;
- producer/orchestration time;
- cold and warm cache/materialization behavior;
- Build/Verify evidence and publication;
- consumer workflow/configuration size;
- the library-specific responsibilities that remain distinct from projects.

If clamps exposes a material mismatch or requires artificial configuration solely to satisfy the shared model, pause before Step 6 and reconsider the migration design instead of mechanically applying it to `lib.scad.hub75`.
