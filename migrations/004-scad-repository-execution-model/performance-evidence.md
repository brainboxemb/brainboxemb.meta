# Migration 004 Step-5 performance evidence

Status: **decision complete; shared tooling correction required**

Tracking:

- Migration 004: issue #49;
- execution-model experiment: issue #53 — closed as completed;
- reference-library draft: `brainboxemb/lib.scad.clamps` PR #7;
- executable benchmark: `brainboxemb/exp.2026-003.scad-ci-performance` PR #1.

## Trigger

`lib.scad.clamps` proved the released `tool.scad-project v0.13.0` lifecycle functionally correct, but relevant-change feedback regressed materially:

- old parallel Build/Verify lifecycle: about 37 s critical path, two SCAD containers;
- released common lifecycle: about 64–65 s critical path, one SCAD container;
- total runner use remained roughly 68–70 runner-seconds;
- README-only correctly became a short host preflight with zero SCAD containers.

The stop condition required a measured execution-model reassessment before Step 6.

## Runtime-boundary experiment

The executable benchmark first separated the SCAD runtime question from the GitHub workflow-topology question.

Reference image:

```text
ghcr.io/brainboxemb/scad-toolchain:v0.4.1
```

Exact OpenSCAD identity retained by that immutable image:

```text
openscad-nightly=20260909T191259.git33e8fdd8.debian-0
sha256 2ae45a19d347c39338f8ffa4b5468f097b96419f23fb814e08cbaed8b965f4e2
```

The exact OBS package version is no longer available from the live package repository, strengthening the immutable-image reproducibility case.

### Runtime comparison

| Variant | Result |
| --- | --- |
| A — GitHub job container | stable reference; fixture workload roughly 0.6–0.8 s |
| B — historical cached-host AppImage | not the same OpenSCAD build; fresh runners still provision host libraries; slower and variable |
| C — host + explicit `docker run` | same runtime and byte-identical fixture output as A; Docker-pull latency itself is not faster |
| D — exact-binary cached host bundle | warm setup about 1.2–1.5 s, but required a second ~178 MB userspace distribution; EGL remained non-equivalent and outputs differed |

Representative final runtime run `34954182921`:

- A workload `760.2 ms`;
- C Docker setup/workload `16.33 s / 734.4 ms`;
- D cold setup/workload `31.03 s / 6006.2 ms`;
- D still reported `EGL_BAD_DISPLAY` after including Mesa DRI drivers as recursive dependency roots.

A/C remained byte-identical:

- STL `958c62133b6d0c13351adb738d2f59a646d7a1f4b5dc662366d6d877de915c8a`;
- PNG `39e2904488000be0d782cc5e4c119d157ec101beaabe1798d09126b6cf9f0dcb`.

Runtime decision: **retain Docker; reject cached-host SCAD tooling as the production execution environment.**

## Full lifecycle A versus C

The runtime-only benchmark could not answer the actual Step-5 regression, because v0.13.0 serializes several GitHub jobs:

```text
A — released v0.13.0
host preflight job
  -> job-container production
  -> separate host publication jobs
```

Variant C keeps Docker but removes those GitHub boundaries:

```text
C — selected topology
one host job
  -> Moon preflight
  -> if affected: docker run exact SCAD image
  -> validate/stage after container exit
  -> host publication in the same job
```

Fixed consumer candidate:

- `lib.scad.clamps` source `bb071329e1d6c764d09f87ecd2cc78d42ac73679`;
- base `52048164db5e5da0b9522c758551bc3af65cae45`;
- affected target `consumer:scad.production-impact`;
- aggregate `consumer:scad.ci`;
- `tool.git-project v0.2.6` / `5e004f0cee53648d6b6284b014b26bed502d2da2`;
- `tool.scad-project v0.13.0` source `da57820fdadd7d203091b6818984991f1548408f`.

### Repeated relevant-change measurements

| Metric | A — released topology | C — run `34955615827` | C — run `34955904779` |
| --- | ---: | ---: | ---: |
| End-to-end / measured lifecycle | ~64–65 s | **41.024 s** | **45.169 s** |
| Checkout + base | separate job overhead included | 3.059 s | 3.026 s |
| Moon preflight | ~10–13 s host job | 2.725 s | 2.569 s |
| Docker setup | ~16–23 s job-container init | 24.738 s | 26.026 s |
| Container production | ~6–8 s producer work within production job | 6.342 s | 8.188 s |
| Both publications | two ~9 s jobs | **3.862 s combined** | **4.529 s combined** |
| SCAD container starts | 1 | 1 | 1 |
| GitHub lifecycle jobs | preflight + production + publishers | **1** | **1** |
| Runner consumption | ~68–70 runner-s | roughly one ~44 s job | roughly one ~48 s job |

Both C runs:

- used the exact immutable v0.4.1 image;
- produced successful current-source `consumer:scad.ci` materialization;
- retained Moon 2.5.4 and `tool.git-project 0.2.6` orchestration evidence;
- completed the same six-task library graph;
- performed two real generated-output force-pushes in the experiment repository after the Docker process exited.

The variance is dominated by normal registry/layer-pull behavior. Both samples remain about 20 s faster than the released topology.

### Repeated README-only measurements

| Run | Affected | SCAD containers | Measured lifecycle |
| --- | --- | ---: | ---: |
| `34955615827` | false | 0 | **4.369 s** |
| `34955904779` | false | 0 | **4.819 s** |

Therefore the selected topology preserves the most important unaffected-path invariant.

## Scenario evidence retained around the exact Step-5 candidate

- docs/design-only: `lib.scad.clamps` proof PR #9, run `34947625311`; `scad.docs` affected, `scad.verify` not in the source-impact route;
- Verify-only: proof PR #10, run `34947539588`; `scad.verify` affected, `scad.docs` not in the source-impact route;
- README-only: C lifecycle runs above, zero containers;
- normal relevant aggregate: C lifecycle runs above, one container and successful current-source materialization;
- representative SCAD-source and conservative missing-base behavior were already proven for the generic v0.2.6 / Migration-004 production semantics during earlier qualification and must remain explicit release tests in the shared single-job implementation.

The topology does not create a second affected engine; it reuses the released `tool.git-project` Moon decision path.

## Ownership finding

The experiment prototype contained local same-job publication code only to measure the topology. That code is **not** an acceptable production implementation.

`tool.git-project v0.2.6` owns generated-output safety today in `reusable-generated-output-publish.yml`:

- allowed PR/main/release publication contexts;
- branch-suffix validation;
- exact source-revision validation;
- stale-source checks before staging and immediately before force-push;
- generated branch naming;
- publication credentials and commit identity.

That contract is not yet exposed as a same-job action/script. Therefore the next valid Migration-004 work is a generic owner prerequisite, not a clamps-specific optimization.

## Decision

Adopt **variant C at the workflow-topology level**, while retaining the immutable Docker runtime.

Required sequence:

1. `tool.git-project` — factor generated-output publication into a callable same-job primitive and keep the existing reusable workflow as a thin wrapper; release it.
2. `tool.scad-project` — consume the released primitive and collapse preflight + conditional Docker production + host publication into one orchestrator job; retain exact-source/materialization checks and conservative fallback; release it.
3. `lib.scad.clamps` — update PR #7 to the released topology and repeat functional/performance qualification.
4. `lib.scad.hub75` remains blocked until Step 5 is complete.

Qualitative rationale:

- **reproducibility:** unchanged immutable Docker runtime;
- **isolation/security:** publication token remains host-only and publication occurs after the SCAD process exits;
- **debugging:** one chronological relevant-change job while retaining an explicit Docker process boundary;
- **maintenance:** one generic publisher owner, no consumer-specific copy;
- **portability:** inputs remain generic task/output/publication concepts applicable to projects and libraries.

Experiment #53 is complete. This file is the retained cross-project evidence for the Step-5 performance decision.
