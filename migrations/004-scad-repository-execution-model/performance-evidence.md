# Migration 004 Step-5 performance evidence

Status: **decision implemented and reference-library qualification complete**

Tracking:

- Migration 004: issue #49;
- execution-model experiment: issue #53 — closed as completed;
- reference-library rollout: `brainboxemb/lib.scad.clamps` PR #7 — merged;
- executable benchmark: `brainboxemb/exp.2026-003.scad-ci-performance` PR #1 — merged to `main`.

## Trigger

The first `lib.scad.clamps` qualification on released `tool.scad-project v0.13.0` was functionally correct but relevant-change feedback regressed materially:

- old parallel Build/Verify lifecycle: about **37 s** critical path, two SCAD containers;
- v0.13.0 common lifecycle: about **64–65 s** critical path, one SCAD container;
- total runner use remained roughly 68–70 runner-seconds;
- README-only correctly became a short host preflight with zero SCAD containers.

The migration stop condition therefore required a measured execution-model reassessment before Step 6.

## Runtime-boundary experiment

The executable benchmark separated the SCAD runtime question from the GitHub workflow-topology question.

Reference image:

```text
ghcr.io/brainboxemb/scad-toolchain:v0.4.1
```

Exact OpenSCAD identity retained by that image:

```text
openscad-nightly=20260909T191259.git33e8fdd8.debian-0
sha256 2ae45a19d347c39338f8ffa4b5468f097b96419f23fb814e08cbaed8b965f4e2
```

The exact OBS package version was no longer available from the live package repository during the experiment, strengthening the immutable-image reproducibility case.

### Runtime comparison

| Variant | Result |
| --- | --- |
| A — GitHub job container | stable reference; fixture workload roughly 0.6–0.8 s |
| B — historical cached-host AppImage | not the same OpenSCAD build; fresh runners still provision host libraries; slower/variable |
| C — host + explicit `docker run` | same runtime and byte-identical fixture output as A; Docker-pull latency itself is not faster |
| D — exact-binary cached host bundle | warm setup about 1.2–1.5 s, but required a second large userspace distribution; EGL remained non-equivalent and outputs differed |

Representative final runtime run `34954182921`:

- A workload `760.2 ms`;
- C Docker setup/workload `16.33 s / 734.4 ms`;
- D cold setup/workload `31.03 s / 6006.2 ms`;
- D still reported `EGL_BAD_DISPLAY` after Mesa DRI drivers were included as recursive dependency roots.

A/C remained byte-identical:

- STL `958c62133b6d0c13351adb738d2f59a646d7a1f4b5dc662366d6d877de915c8a`;
- PNG `39e2904488000be0d782cc5e4c119d157ec101beaabe1798d09126b6cf9f0dcb`.

Runtime decision: **retain Docker; reject cached-host SCAD tooling as the production execution environment.**

## Full lifecycle A versus selected C topology

The runtime-only benchmark could not explain the v0.13.0 regression because that release serialized several GitHub jobs:

```text
v0.13.0
host preflight job
  -> job-container production
  -> separate host publication jobs
```

The selected topology keeps Docker but removes those GitHub boundaries:

```text
one host job
  -> Moon preflight
  -> if affected: docker run exact SCAD image
  -> validate/stage after container exit
  -> host publication in the same job
```

Fixed experiment consumer candidate:

- `lib.scad.clamps` source `bb071329e1d6c764d09f87ecd2cc78d42ac73679`;
- base `52048164db5e5da0b9522c758551bc3af65cae45`;
- affected target `consumer:scad.production-impact`;
- aggregate `consumer:scad.ci`.

### Repeated relevant-change measurements

| Metric | v0.13.0 released topology | C — `34955615827` | C — `34955904779` |
| --- | ---: | ---: | ---: |
| End-to-end / measured lifecycle | ~64–65 s | **41.024 s** | **45.169 s** |
| Checkout + base | separate job overhead included | 3.059 s | 3.026 s |
| Moon preflight | ~10–13 s host job | 2.725 s | 2.569 s |
| Docker setup | ~16–23 s job-container init | 24.738 s | 26.026 s |
| Container production | ~6–8 s | 6.342 s | 8.188 s |
| Both publications | two ~9 s jobs | **3.862 s combined** | **4.529 s combined** |
| SCAD container starts | 1 | 1 | 1 |
| GitHub lifecycle jobs | preflight + production + publishers | **1** | **1** |

### Repeated README-only controls

| Run | Affected | SCAD containers | Measured lifecycle |
| --- | --- | ---: | ---: |
| `34955615827` | false | 0 | **4.369 s** |
| `34955904779` | false | 0 | **4.819 s** |

The experiment therefore selected **one host orchestrator + one conditional Docker process**. The gain comes from removing serial GitHub job/artifact handoffs, not from replacing Docker.

The experiment is retained permanently on `exp.2026-003.scad-ci-performance` main after PR #1 merge:

```text
c818b41b225c818bab5d9f41d21f187dfdb41503
```

## Production implementation of the selected topology

### `tool.git-project v0.2.7`

The generic generated-output safety contract was exposed as a callable same-job action while preserving the older artifact-based reusable workflow as a compatibility wrapper.

Evidence:

- PR #24 merge/release source `6234b7437b0dc0115642468f74d1f4a2c2214bef`;
- release run `34960768652` — passed;
- tagged same-job verification `34960782984` — Linux contract/sequential publication and native Windows publication passed;
- annotated tag object `6afaa504ae68d2e774eb74e17fb0b27d44d455ef` resolves to exact release source.

### `tool.scad-project v0.13.1`

The SCAD owner then composed affected preflight, exact source/base worktree, conditional Docker execution, current materialization validation/staging and both publications inside one GitHub host job.

Evidence:

- PR #53 merge/main `8143f751bf0c693a7f83ef68e5e557db7d1cb798`;
- exact-main Test `34967888175` — passed;
- release/main source `28661fc040c4994e9c1d391285b7425c7a55252b`;
- exact-main Test `34970279362` — passed;
- release run `34970379930` — passed;
- tagged Test `34970393104` — passed;
- annotated tag object `ce15d9ae1bfe2b4862e52fe847139fdf814410ac` resolves to exact release source.

Reference-template qualification retained:

- relevant run `34967002612` — one host job, one explicit Docker process, current materialization and both publications passed;
- README-only `34967121183` — `affected=false`, heavy path skipped;
- missing-base proof — conservative forced aggregate execution passed.

## Released reference-library validation

`lib.scad.clamps` PR #7 then moved from the v0.13.0 candidate to released v0.13.1.

Final candidate:

```text
68a0a05211ea5ed6e1303dfdc060143fe8286e23
```

Final candidate run `34971400621`:

- one host production job;
- one explicit SCAD Docker process;
- image pull about **20.0 s**;
- OpenSCAD + PythonSCAD docs/verification green;
- current aggregate materialization green;
- both host publications green;
- about **45 s** from reusable-workflow start through second publication.

An earlier released-v0.13.1 run `34970821889` was also fully green but had a ~43.7 s GHCR pull outlier. Its producer graph was about 5.2 s and both publications together about 4.8 s. This isolates registry variance from the workflow topology.

Final zero-container and producer-independence proofs:

- README-only PR #11 / `34971644925` — `affected=false`, all image/Docker/publication steps skipped;
- docs-only PR #12 / `34971733730` — preflight artifact `10397796125` contains `scad.docs`, excludes `scad.verify`;
- Verify-only PR #13 / `34971800074` — preflight artifact `10397512803` contains `scad.verify`, excludes `scad.docs`.

Merge/exact-main:

```text
lib.scad.clamps main = c5732944c8c2ba840a3f0f2f0a0638430a796cfd
exact-main run = 34972350665
```

Exact-main run passed one-host/one-Docker production and both same-job publications. `prod/build` and `prod/verification` both record the exact merge source and `tool.scad-project v0.13.1`.

## Final Step-5 conclusion

The performance stop condition is resolved:

- **runtime reproducibility:** Docker retained;
- **unaffected cost:** zero SCAD containers;
- **affected heavy setup:** one SCAD container instead of two;
- **relevant feedback:** repeated one-host measurements around 41–45 s under normal image-pull conditions instead of the structural 64–65 s v0.13.0 topology;
- **logical independence:** docs-only and Verify-only affected routes remain distinct;
- **publication/security:** write token remains host-side after the container exits;
- **maintenance:** generic publication stays owned by `tool.git-project`, SCAD orchestration by `tool.scad-project`, consumer graph by the library.

Step 5 is complete. Step 6 may proceed to `lib.scad.hub75` after re-evaluating that repository's own producer graph and keeping physical-verification work outside Migration 004.
