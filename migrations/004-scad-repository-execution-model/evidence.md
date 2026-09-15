# Migration 004 qualification evidence

Status: **complete**

Tracking issue: #49.

Successor: [Migration 005](../005-scad-execution-architecture/README.md).

This file retains the cross-project evidence needed to reconstruct the completed migration. Detailed performance measurements remain in [`performance-evidence.md`](performance-evidence.md); the human-maintainability finding that triggered Migration 005 remains in [`reflection.md`](reflection.md).

## Final qualified execution properties

The released Migration-004 model proved that:

- an unrelated/root-README-only change can finish without pulling or starting the SCAD runtime;
- affected normal production can use one host lifecycle and at most one explicit immutable SCAD Docker process;
- Build and Verification remain independently meaningful capabilities;
- SCons remains responsible for fine-grained CAD target decisions;
- uncertain source/base comparison runs conservatively instead of silently skipping required work;
- publication happens on the host after the SCAD process exits and GitHub write credentials are not passed into that process;
- generated output retains exact source/tooling and current execution/publication evidence.

## Step 1 — generic affected pre-check

Owner: `brainboxemb/tool.git-project`.

- initial capability: v0.2.5;
- generic aggregate/upstream propagation correction: v0.2.6;
- exact v0.2.6 source: `5e004f0cee53648d6b6284b014b26bed502d2da2`;
- explicit shallow BASE/HEAD behavior qualified with Moon 2.5.4;
- missing/invalid comparison context qualified to run conservatively.

## Step 2 — Build/Verification independence

Owner: `brainboxemb/template.scad-project`.

- PR #22 removed the stale `scad.verify -> scad.build` dependency;
- merge/exact main: `082b0cecb47ba082899214751080adc54556e94c`;
- PR run `34893868011` — passed;
- exact-main run `34894004036` — passed.

## Step 3 — first reusable production lifecycle

Owner: `brainboxemb/tool.scad-project`.

- released as v0.13.0;
- exact release source: `da57820fdadd7d203091b6818984991f1548408f`;
- release run `34938168129` — passed;
- tagged Test `34938179069` — passed.

This established the host-side impact check, conditional SCAD runtime, explicit BASE/HEAD context, separate Build/Verification caches, current materialization validation and host publication.

## Step 4 — released model in the reference template

Owner: `brainboxemb/template.scad-project`.

- PR #29 merge/exact main: `8ac67014eb2ab7252f38b41a1137b5b0c902ef6a`;
- final-head run `34944252421` — passed;
- exact-main run `34945239139` — passed;
- README-only PR #30 / run `34944598444` — zero SCAD containers;
- Verify-only PR #31 / run `34944622039` — Verification affected without Build/docs;
- Build-side-only PR #33 / run `34944404186` — Build/docs affected without Verification.

## Step 5 — performance stop and corrected lifecycle

The first v0.13.0 library qualification exposed a material regression:

- old parallel Build/Verify critical path: about **37 s** with two heavy containers;
- first common v0.13.0 lifecycle: about **64–65 s** with one container but serial GitHub job/artifact boundaries.

Rollout stopped and issue #53 / `exp.2026-003.scad-ci-performance` measured the alternatives.

Selected result:

```text
one host job
  -> cheap affected check
  -> if affected: one explicit Docker SCAD process
  -> validate/stage after process exit
  -> publish from the same host job
```

Shared releases:

- `tool.git-project v0.2.7`, exact source `6234b7437b0dc0115642468f74d1f4a2c2214bef`;
- `tool.scad-project v0.13.1`, exact source `28661fc040c4994e9c1d391285b7425c7a55252b`.

Repeated selected-topology samples were about **41–45 s** for relevant work and **4.4–4.8 s** for README-only work with zero containers.

## Step 5 — reference library

Owner: `brainboxemb/lib.scad.clamps`.

Qualification:

- final relevant PR-head run `34971400621` — one host lifecycle, one explicit Docker process, both publications green;
- README-only PR #11 / run `34971644925` — zero-container path;
- docs-only PR #12 / run `34971733730` — docs affected without Verification;
- Verify-only PR #13 / run `34971800074` — Verification affected without docs;
- PR #7 merge/exact qualified main `c5732944c8c2ba840a3f0f2f0a0638430a796cfd`;
- exact-main run `34972350665` — passed.

Release closeout:

- v0.1.3 exact release source `f0dbb82b477201646fc3e2173ccba96d70fb8920`;
- changelog-only run `34974591518` — zero-container path;
- release run `34974674991` — Build, Verification and finalization passed;
- annotated tag, immutable Build/Verification release branches and GitHub Release assets exist.

## Step 6 — HUB75 library

Owner: `brainboxemb/lib.scad.hub75`.

The live repository was reconstructed rather than copying clamps mechanically. Its real output responsibilities include standalone presentation renders, generated design documentation and richer API/physical-verification output.

Qualification:

- PR #23 final candidate `3f44c90afe8419ff56c76bdc9806c9887c46f387`;
- candidate run `34975967199` — one host lifecycle, one explicit Docker process and both publications green;
- README-only PR #24 / run `34976305647` — zero-container path;
- Build-only PR #25 / run `34976316887` — direct Build impact only;
- docs-only PR #26 / run `34976333875` — direct docs impact only;
- Verify-only PR #27 / run `34976347095` — direct Verification impact only;
- merge/exact qualified main `5f2ed2ae3e6901e10c1b14efeed5285bdde779da`;
- exact-main run `34976840416` — passed.

Release closeout:

- changelog-only PR #28 / run `34977045560` — zero-container path;
- v0.1.4 exact release source `2eaaa540e3658bd3821eb6ec0f2d0352cbefff48`;
- release run `34977125016` — exact-source Build, Verification, finalization and cleanup passed;
- annotated tag `v0.1.4`, immutable `rel/v0.1.4/build` and `rel/v0.1.4/verification`, Build/Verification release ZIPs and `SHA256SUMS.txt` exist.

Migration 004 did not alter the library's physical SQ/testcase content.

## Performance conclusion

The final result is intentionally not described as “all builds became faster”.

Measured outcome:

- ordinary relevant-change wall-clock: old ~37 s parallel baseline versus final ~41–45 s;
- temporary v0.13.0 regression: ~64–65 s, removed by v0.13.1;
- heavy normal execution: two SCAD containers reduced to one;
- repeated unrelated/README-only path: ~4.4–4.8 s and zero containers;
- old job-level container initialization had itself been observed around 17–30 s before checkout.

The material gain is therefore avoiding tens of seconds of heavy setup for changes that do not need CAD work and reducing duplicated compute/setup for changes that do.

## Why the frame rollout moved to Migration 005

The real HUB75 frame still uses `tool.scad-project v0.12.0` and `lib.scad.hub75 v0.1.3`.

Migration 004 originally made frame requalification conditional. After Step 6, the maintainability review found the new task/orchestration model too difficult to explain from a normal consumer repository. Rolling that model into the frame before deciding whether to simplify it would create churn rather than useful qualification.

The frame is therefore **not claimed as migrated by Migration 004**. Its eventual architecture/update belongs to Migration 005 after a simpler target architecture is selected.
