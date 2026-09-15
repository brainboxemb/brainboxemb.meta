# Migration 004 qualification evidence

Status: **active — Steps 1–6 complete; reflection gate current**

Tracking: meta issue #49.

This file retains only the cross-project evidence needed to reconstruct the current migration state. Repository-specific implementation detail remains with the owning repository. Runtime/performance investigation detail is retained separately in [`performance-evidence.md`](performance-evidence.md).

## Qualified execution-model invariants

The currently qualified model is:

- Moon owns repository-level task orchestration and affected/preflight decisions;
- SCons remains the fine-grained SCAD target engine inside producer execution;
- Build and Verify remain logically independent producer domains;
- repositories may have an additional independent docs producer when that is a real output domain;
- unrelated/README-only changes stop before SCAD image pull and start zero SCAD containers;
- affected normal production uses one GitHub-hosted orchestrator job and at most one explicit Docker process for the immutable SCAD toolchain;
- exact source/base context is shallow; `fetch-depth: 0` is not required for the qualified explicit-base model;
- missing/invalid comparison context fails conservative into production rather than false-skipping;
- generated-output publication happens on the host after the SCAD process exits;
- publication credentials are not passed into the SCAD container;
- current Moon materialization is validated against the exact source revision before publication;
- producer execution evidence remains distinct from current orchestration/materialization/publication context.

## Step 1 — generic Moon affected preflight

Status: **complete**

Owner: `brainboxemb/tool.git-project`.

Initial capability was released as v0.2.5. Real-consumer integration exposed incomplete upstream/aggregate propagation; the generic correction was released as:

```text
tool.git-project v0.2.6
exact source: 5e004f0cee53648d6b6284b014b26bed502d2da2
```

Qualified behavior includes README-only unaffected, producer/upstream propagation, explicit BASE/HEAD ranges, conservative missing-base handling, Linux/Windows parity and retained `.moon/preflight` decision evidence.

## Step 2 — reference Build/Verify graph correction

Status: **complete**

Owner: `brainboxemb/template.scad-project`.

PR #22 removed the stale `scad.verify -> scad.build` dependency after confirming Verify does not consume normal Build output.

- merge/exact main: `082b0cecb47ba082899214751080adc54556e94c`;
- PR run `34893868011` — passed;
- exact-main run `34894004036` — passed.

## Step 3 — reusable production workflow v0.13.0

Status: **complete and released**

Owner: `brainboxemb/tool.scad-project`.

The v0.13.0 contract introduced host affected preflight, one conditional SCAD container, shallow exact BASE/HEAD context, conservative fallback, separate Build/Verify SCons caches, current Moon materialization validation and host publication after SCAD work.

The important integration correction was the distinction between:

- `affected_task` — producer/source-impact gate;
- `aggregate_task` — publication-ready execution root.

Release evidence:

- exact release source `da57820fdadd7d203091b6818984991f1548408f`;
- release run `34938168129` — passed;
- tagged Test `34938179069` — passed;
- annotated tag object resolves to the exact release source.

## Step 4 — released workflow in the reference template

Status: **complete**

Owner: `brainboxemb/template.scad-project`.

PR #29 consumed v0.13.0 and narrowed Verify inputs so producer independence stayed truthful.

- merge/exact main `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`;
- final-head run `34944252421` — passed;
- exact-main run `34945239139` — passed;
- README-only PR #30 / run `34944598444` — zero SCAD container;
- Verify-only PR #31 / run `34944622039` — Verify affected without Build/Docs;
- Build-side-only PR #33 / run `34944404186` — Build/Docs affected without Verify.

## Step 5 — performance stop and v0.13.1 shared correction

The first `lib.scad.clamps` v0.13.0 qualification was functionally correct but increased relevant feedback from the old ~37 s parallel critical path to ~64–65 s because preflight, production and publication had become serial GitHub jobs.

Migration 004 stopped rollout and ran the dedicated performance experiment tracked by issue #53.

Selected topology:

```text
one host job
  -> Moon affected preflight
  -> if affected: one explicit docker run of the exact SCAD image
  -> validate/stage after container exit
  -> host publication in the same job
```

Shared releases:

- `tool.git-project v0.2.7`, exact source `6234b7437b0dc0115642468f74d1f4a2c2214bef`, same-job generated-output publication;
- `tool.scad-project v0.13.1`, exact source `28661fc040c4994e9c1d391285b7425c7a55252b`, single-host normal production lifecycle.

Representative one-host lifecycle samples returned to about **41–45 s** while README-only controls remained about **4–5 s** with zero containers. See [`performance-evidence.md`](performance-evidence.md) for the full comparison.

## Step 5 — reference library qualification

Status: **complete and released**

Owner: `brainboxemb/lib.scad.clamps`.

The small library intentionally has no dummy normal Build producer. Its graph contains real docs and Verify producers plus publication/finalization and the two repository-level virtual roots.

Qualification:

- final PR-head relevant run `34971400621` — one host job, one explicit Docker process, current materialization and both publications green;
- README-only PR #11 / run `34971644925` — `affected=false`, no image pull/container/publication;
- docs-only PR #12 / run `34971733730` — direct docs route without Verify;
- Verify-only PR #13 / run `34971800074` — direct Verify route without docs;
- PR #7 merge/exact qualified main `c5732944c8c2ba840a3f0f2f0a0638430a796cfd`;
- exact-main run `34972350665` — passed; both `prod/*` publications record that source and `tool.scad-project v0.13.1`.

Release closeout, initially missed, was corrected before continuing:

- PR #14 release source `f0dbb82b477201646fc3e2173ccba96d70fb8920`;
- changelog-only run `34974591518` — zero-container;
- v0.1.3 release run `34974674991` — Build, Verify and finalization green;
- annotated `v0.1.3` tag, immutable release branches and GitHub Release assets exist.

## Step 6 — second library qualification

Status: **complete and released**

Owner: `brainboxemb/lib.scad.hub75`.

The live repository was reconstructed before implementation. HUB75 legitimately has three producer domains:

- `scad.docs` — generated design documentation;
- `scad.build` — standalone presentation renders;
- `scad.verify` — API verification plus physical-verification fixtures/plan output.

Physical SQ/testcase content itself was not changed by Migration 004.

Implementation and normal-production evidence:

- PR #23 final candidate `3f44c90afe8419ff56c76bdc9806c9887c46f387`;
- candidate run `34975967199` — one host job, one explicit Docker process, all producers/materialization and both publications green;
- README-only proof PR #24 / run `34976305647` — `affected=false`; all heavy/publication steps skipped;
- Build-only proof PR #25 / run `34976316887` — direct producer impact only on `scad.build`;
- docs-only proof PR #26 / run `34976333875` — direct producer impact only on `scad.docs`;
- Verify-only proof PR #27 / run `34976347095` — direct producer impact only on `scad.verify`;
- PR #23 merge/exact qualified main `5f2ed2ae3e6901e10c1b14efeed5285bdde779da`;
- exact-main run `34976840416` — passed;
- `prod/build` and `prod/verification` both record source `5f2ed2ae3e6901e10c1b14efeed5285bdde779da` and `tool.scad-project v0.13.1`.

Release closeout:

- PR #28 changed changelog only;
- PR run `34977045560` — `affected=false`; zero SCAD image pull/container/publication;
- exact release source `2eaaa540e3658bd3821eb6ec0f2d0352cbefff48`;
- release run `34977125016` — resolve, exact-source Build, exact-source Verify, finalization and release-request cleanup all green;
- annotated tag object `822ba1a8d5c0d562ad53d2135f300fd3dfef4576` points to exact source `2eaaa540e3658bd3821eb6ec0f2d0352cbefff48`;
- immutable `rel/v0.1.4/build` and `rel/v0.1.4/verification` both record that source and `tool.scad-project v0.13.1`;
- GitHub Release `v0.1.4` exists with Build ZIP, Verification ZIP and `SHA256SUMS.txt`.

## Reflection gate after Step 6

Step 6 proves the model works technically in both a small library and a richer library. It also makes the cognitive cost visible: HUB75 now exposes eight Moon tasks even though the underlying conceptual model is three producer domains, three finalization tasks and two virtual repository roots.

The design motivation exists, but is distributed across meta, `tool.scad-project/docs/production-workflow.md`, `tool.scad-project/docs/execution-evidence.md` and release history. That is not yet a sufficient human-maintainability contract for a consumer maintainer.

The current reflection and simplification candidates are documented in [`reflection.md`](reflection.md).

No HUB75-frame rollout should start until the reflection gate decides whether the graph needs documentation improvements only or a structural simplification/tool release first.
