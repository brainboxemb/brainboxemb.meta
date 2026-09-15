# Migration 004 qualification evidence

Status: **active — Step 5 complete; Step 6 next**

Tracking: meta issue #49.

This file retains the cross-project evidence needed to reconstruct the migration state. Implementation details remain in the repositories that own them.

## Qualified execution-model invariants

The currently qualified model is:

- Moon owns repository-level orchestration and affected/preflight decisions;
- SCons remains the fine-grained SCAD target engine;
- Build and Verify remain logically independent producer domains;
- unrelated/README-only changes stop before SCAD image pull and start zero SCAD containers;
- affected normal production uses one GitHub-hosted orchestrator job and at most one explicit Docker process for the immutable SCAD toolchain;
- exact source/base context is shallow; `fetch-depth: 0` is not required for the qualified explicit-base model;
- missing/invalid comparison context fails conservative into production rather than false-skipping;
- generated-output publication happens on the host after the SCAD process exits;
- publication credentials are not passed into the SCAD container;
- current Moon materialization is validated against the exact source revision before publication.

## Step 1 — generic Moon affected preflight

Status: **complete**

Owner: `brainboxemb/tool.git-project`.

Initial capability was released as v0.2.5. Real-consumer integration later exposed incomplete upstream/aggregate propagation, which was corrected generically through Moon's affected graph semantics and released as:

```text
tool.git-project v0.2.6
exact source: 5e004f0cee53648d6b6284b014b26bed502d2da2
```

Qualified behavior includes:

- README-only input outside the target graph => `affected=false`;
- producer/upstream input change => aggregate/source-impact target affected;
- missing base => conservative `affected=true`;
- explicit BASE/HEAD ranges;
- Linux and native Windows parity;
- retained `.moon/preflight` decision/query evidence.

A duplicate release-request/idempotency observation is tracked separately as `tool.git-project` issue #22 and does not block this migration.

## Step 2 — reference Build/Verify graph correction

Status: **complete**

Owner: `brainboxemb/template.scad-project`.

PR #22 removed the stale `scad.verify -> scad.build` dependency after confirming Verify does not consume normal Build output.

Evidence:

- merge/exact main: `082b0cecb47ba082899214751080adc54556e94c`;
- PR run `34893868011` — passed;
- exact-main run `34894004036` — passed.

Container initialization on those earlier workflows was already material enough to make pre-container gating a required migration criterion.

## Step 3 — first reusable production workflow

Status: **complete and released as v0.13.0**

Owner: `brainboxemb/tool.scad-project`.

### Shallow explicit-base prerequisite

Moon 2.5.4 was qualified with exact shallow HEAD and exact shallow BASE commits locally present while intervening history was unavailable.

- proof run `34895987723` — normal affected decision passed;
- no `fetch-depth: 0` requirement was introduced.

### Owner implementation

- owner PR #51 final head `f71590631fdc1d278f2bcecbee46fdcc696b7429`;
- owner Test run `34935383752` — passed;
- implementation merge/main `94edde1527048a054de170cb8c1cb63f7e272ff3`;
- exact-main Test `34936204512` — passed.

The v0.13.0 contract introduced host affected preflight, one conditional SCAD container, explicit Moon BASE/HEAD context, conservative fallback, separate Build/Verify SCons caches, one publication-ready aggregate/materialization boundary and host publication after the heavy SCAD work.

### Integration findings retained from the template

The first README-only proof exposed that environment-sensitive publication/index tasks cannot double as the expensive source-impact gate. The final contract therefore distinguishes:

- `affected_task` — producer/source-impact gate;
- `aggregate_task` — publication-ready execution root.

Retained pre-release proofs:

- README-only PR #25 / run `34935678113` — `affected=false`, production/publication skipped;
- missing-base PR #26 / run `34935787742` — conservative affected production passed;
- Verify-only PR #27 / run `34935860495` — source-impact route through Verify, not Build;
- representative source PR #28 / run `34936003043` — producer-driven affected route passed.

### v0.13.0 release

- release PR #52 final head `d917b83e8d36207a06c4c1bad6474dd8e936be67`;
- release PR Test `34937968007` — passed;
- exact release/main source `da57820fdadd7d203091b6818984991f1548408f`;
- exact-main Test `34938102439` — passed;
- release run `34938168129` — passed;
- tagged Test `34938179069` — passed;
- annotated tag object `a2d3a9356da396da9b6fed4e870aa1a5fa26448a` resolves to the exact release source.

## Step 4 — released v0.13.0 in the reference template

Status: **complete**

Owner: `brainboxemb/template.scad-project`.

PR #29 consumed the released interface and also narrowed the template Verify input boundary so Build-side changes could truthfully remain non-Verify impacts.

Final evidence:

- final PR head `ea99880acef81cf8f6d9aab9e0371caae63af9c6`;
- final-head run `34944252421` — passed;
- README-only PR #30 / run `34944598444` — zero SCAD container;
- Verify-only PR #31 / run `34944622039` — affected evidence contains Verify and excludes Build/Docs;
- Build-side-only PR #33 / run `34944404186` — affected evidence contains Build/Docs branch and excludes Verify;
- merge/exact main `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`;
- exact-main run `34945239139` — passed with production publication.

Cold run `34938849331` built all template CAD targets; later final-head execution restored CAD target work through SCons while current Moon materialization remained tied to the current source revision.

## Step 5 performance stop and shared correction

The first `lib.scad.clamps` v0.13.0 qualification was functionally correct but exposed a material relevant-change latency regression:

- old parallel Build/Verify lifecycle: about **37 s** critical path with **two** heavy SCAD containers;
- v0.13.0 multi-job lifecycle: about **64–65 s** with **one** SCAD container;
- README-only remained zero-container.

Migration 004 therefore stopped rollout before `lib.scad.hub75` and ran the dedicated `exp.2026-003.scad-ci-performance` experiment tracked by issue #53.

Runtime conclusion:

- keep immutable Docker SCAD tooling;
- cached-host/AppImage and exact-binary host-bundle variants did not reproduce the qualified Docker EGL/output behavior reliably;
- explicit Docker preserved the qualified runtime/output.

Lifecycle conclusion:

- the regression came primarily from serial GitHub job/artifact boundaries;
- one-host-job lifecycle samples were **41.024 s** (`34955615827`) and **45.169 s** (`34955904779`);
- README-only controls were **4.369 s** and **4.819 s**, both with zero containers;
- keep one explicit Docker process, but surround it with preflight/validation/publication in the same host job.

The executable experiment is retained on `exp.2026-003.scad-ci-performance` main after PR #1 merge `c818b41b225c818bab5d9f41d21f187dfdb41503`.

### Shared prerequisite 1 — same-job publisher

Owner: `tool.git-project`.

Released as v0.2.7:

- PR #24 merge/release source `6234b7437b0dc0115642468f74d1f4a2c2214bef`;
- release run `34960768652` — passed;
- tagged publisher verification `34960782984` — Linux contract, sequential Linux same-job publication and native Windows publication passed;
- annotated tag object `6afaa504ae68d2e774eb74e17fb0b27d44d455ef` resolves to the exact release source.

The generated-output safety contract is available as a same-job action while the artifact-based reusable workflow remains a compatibility wrapper.

### Shared prerequisite 2 — single-host SCAD lifecycle

Owner: `tool.scad-project`.

PR #53 collapsed the v0.13.0 job topology into one host orchestrator while retaining the immutable Docker runtime and public workflow inputs.

Owner/release evidence:

- PR #53 merge/main `8143f751bf0c693a7f83ef68e5e557db7d1cb798`;
- exact-main Test `34967888175` — passed;
- release PR #54 final head `5ffd73746d517b9edd7149c63f2affca879f72b7`;
- release PR Test `34969048825` — passed;
- v0.13.1 exact release/main source `28661fc040c4994e9c1d391285b7425c7a55252b`;
- exact-main Test `34970279362` — passed;
- release run `34970379930` — passed;
- annotated tag object `ce15d9ae1bfe2b4862e52fe847139fdf814410ac` resolves to exact release source;
- tagged Test `34970393104` — passed.

Reference-template candidate proofs against the new topology retained:

- relevant single-host/one-Docker run `34967002612` — passed with materialization and both same-job publications;
- README-only run `34967121183` — `affected=false`, all heavy/publication steps skipped;
- conservative missing-base proof — forced one-Docker aggregate execution and publication passed.

## Step 5 — reference library qualification

Status: **complete**

Owner: `brainboxemb/lib.scad.clamps`.

### Library-specific graph

The common lifecycle was adopted without making the small library artificial:

- `scad.docs` — generated OpenSCAD + PythonSCAD design documentation;
- `scad.verify` — existing OpenSCAD + PythonSCAD public-consumer PNG/STL verification;
- no dummy `scad.build` task because the repository has no normal configured render/export targets;
- `scad.production-impact` — source-impact gate over docs + Verify producers;
- `scad.ci` — publication-ready aggregate.

The existing public-consumer verification content was retained; only repository orchestration changed.

### Released-interface candidate

Final PR #7 head:

```text
68a0a05211ea5ed6e1303dfdc060143fe8286e23
```

Tool alignment:

```text
tool.scad-project v0.13.1
exact gitlink/workflow source: 28661fc040c4994e9c1d391285b7425c7a55252b
```

Final relevant run `34971400621` passed:

- one GitHub-hosted production job;
- affected preflight green;
- one explicit SCAD Docker process;
- OpenSCAD + PythonSCAD generated design documentation green;
- OpenSCAD PNG/STL consumer verification green;
- PythonSCAD PNG/STL consumer verification green;
- exact current `consumer:scad.ci` materialization validation green;
- both Build and Verification artifacts staged;
- both same-job host publications green.

Measured from reusable workflow start through second publication: about **45 s**, including about **20 s** GHCR image pull.

A previous released-v0.13.1 run `34970821889` was also fully green but encountered a ~43.7 s image-pull outlier. Its producer graph was about 5.2 s and both publications together about 4.8 s. The repeated final sample therefore shows that registry variance remains, while the old 64–65 s serial job topology is no longer structural.

### Isolated final-head proofs

All proof PRs were based on exact candidate `68a0a05211ea5ed6e1303dfdc060143fe8286e23` and closed without merge.

README-only / zero-container:

- PR #11;
- head `8b16c4b7cf55eb94c34dedec09a9ea48bf1508b4`;
- run `34971644925` — passed;
- preflight: `affected=false`, `status=success`, reason `target-and-upstream-unaffected`;
- SCAD tool/cache/image/Docker/staging/publication steps all skipped.

Docs-only producer impact:

- PR #12;
- head `b332c59b08b91b3eced853417c80fb04943bd31d`;
- run `34971733730` — passed;
- changed file: only `scripts/render-openscad-design.sh`;
- preflight artifact `10397796125` affected-task set contains `consumer:scad.docs` and downstream publication/aggregate tasks;
- `consumer:scad.verify` is absent from the affected-task set;
- one Docker process and both publications passed.

Verify-only producer impact:

- PR #13;
- head `db342571f0da2c618df952fb7b280d15966a2659`;
- run `34971800074` — passed;
- changed file: only `vrf/README.md`;
- preflight artifact `10397512803` affected-task set contains `consumer:scad.verify` and downstream publication/aggregate tasks;
- `consumer:scad.docs` is absent from the affected-task set;
- one Docker process and both publications passed.

The publication-ready aggregate intentionally may materialize both output branches after the affected gate; logical independence is established by the preflight affected-task evidence, not by which aggregate dependencies happen to execute/materialize afterwards.

### Merge / exact-main qualification

- PR #7 merge/exact main: `c5732944c8c2ba840a3f0f2f0a0638430a796cfd`;
- exact-main production run `34972350665` — passed;
- one host production job and one explicit Docker process;
- current materialization validation passed;
- Build and Verification same-job production publication passed;
- `prod/build/publication-info.txt` records source `c5732944c8c2ba840a3f0f2f0a0638430a796cfd`, run `34972350665`, `tool.scad-project v0.13.1` and exact SCAD-tool gitlink `28661fc040c4994e9c1d391285b7425c7a55252b`;
- `prod/verification/publication-info.txt` records the same exact source/tooling context.

Step 5 therefore satisfies both functional and proportionality acceptance and no longer blocks the second library rollout.

## Step 6 — second library qualification

Status: **next; re-evaluation required**

Owner candidate: `brainboxemb/lib.scad.hub75`.

Before implementation, reconstruct the live repository and distinguish Migration 004 execution-model work from separate physical-verification work. Re-evaluate:

- actual Build/docs/Verify producer graph;
- current tool/git dependency pins;
- existing workflow/publication/release model;
- truthful affected-input boundaries for independent producers;
- whether the reference-library graph needs adaptation for HUB75-specific outputs;
- README-only zero-container behavior;
- relevant one-host/one-Docker behavior;
- conservative missing-base behavior where appropriate;
- exact-main Build/Verification publication after rollout.

Do not mechanically copy the clamps graph, and do not fold SQ/physical-verification work into this migration.
