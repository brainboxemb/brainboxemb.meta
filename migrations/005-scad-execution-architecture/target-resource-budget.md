# Migration 005 — target lifecycle resource and latency budget

Status: **architecture budget established; implementation must remeasure end-to-end**

This document does not pretend that one network timing predicts future GitHub Actions runs. It separates measured fixed/structural savings from timing estimates that remain sensitive to hosted-runner and registry variance.

## Reference points

### Old parallel topology

Migration 004 measured roughly **37 s** relevant-change critical-path feedback with separate Build and Verification heavy jobs.

That topology paid for:

- two hosted heavy jobs at the same time;
- two source/runtime setup paths;
- up to two independent cold CAD image pulls;
- two CAD runtime starts.

The exact total runner-seconds varied by run, but a ~37 s critical path with two overlapping heavy jobs is on the order of **70+ heavy runner-seconds**, not 37 runner-seconds.

### Current v0.13.1 one-runner clamps sample

Controlled rerun `brainboxemb/lib.scad.clamps` run `34972350665`, attempt-2 job `104427368493`:

- hosted job: about **49 s** from start to completion;
- current full CAD image pull: about **19 s**;
- aggregate CAD/Moon step: about **9 s** at Actions step granularity;
- two SCons restore actions ran although clamps uses the direct engine;
- complete normal Build/Verification Actions-artifact uploads took about **3 s** together in this sample;
- one hosted runner and one CAD runtime.

This is a useful high-overhead sample, not the only v0.13.1 timing; Migration 004 also observed relevant runs around 41–45 s.

### Current v0.13.1 warm HUB75 sample

`brainboxemb/lib.scad.hub75` run `34976840416`, attempt-2 job `104442409672`:

- hosted job: about **37 s**;
- current full CAD image pull: about **16 s**;
- aggregate CAD/Moon step: about **8 s** at Actions step granularity;
- internal warm SCons/Moon graph: about **5.071 s**;
- complete normal Build/Verification Actions-artifact uploads took about **2 s** together;
- normal SCons cache restore/save was useful;
- separate Verification SCons cache remained unused;
- one hosted runner and one CAD runtime.

The corresponding cold graph had been about 8.805 s, so warm target-level SCons reuse saves real CAD work even though image acquisition remains larger.

## Target structural budget

For a normal affected run, Migration 005 targets:

```text
hosted heavy runners     1
CAD image pulls          1
CAD runtime starts       1
Moon impact analyses     1
full normal artifacts    0 by default
SCons cache paths        only those actually used
Build/Verify publication 2 isolated publishers, allowed to overlap on the same runner
```

For an unrelated change:

```text
hosted workflow runner   1 short host-only path
CAD image pulls          0
CAD runtime starts       0
CAD work                 0
```

## Image-transfer budget

Externally qualified candidate images:

| Runtime profile | Compressed OCI bytes |
| --- | ---: |
| OpenSCAD-focused | 328,098,501 |
| full/dual | 449,516,893 |

Therefore an OpenSCAD-only affected repository avoids:

```text
121,418,392 compressed bytes per cold image acquisition
```

or about **27.0%** relative to the current full image.

### Reference repository consequences

**Clamps** intentionally supports PythonSCAD, so it still needs the full/dual image. Its image-transfer win versus current one-runner v0.13.1 is therefore not image slimming; its main resource wins come from keeping one runner, removing unused SCons handling, stable Moon reuse and removing duplicate normal artifacts.

**HUB75** is OpenSCAD-only and can use the focused image, so it receives the ~121 MB cold-transfer reduction directly.

Compared with the old two-heavy-job topology, a cold affected OpenSCAD-only run can avoid both duplication and the PythonSCAD-only layers. Two independent full pulls would represent about 899 MB of compressed image descriptors/data before registry/client reuse effects; one focused pull is about 328 MB. The exact network transfer depends on registry caching, but the architecture removes the duplicated demand by construction.

## Cache-transfer budget

### Moon

Keep Moon whole-capability cache because stable-task validation proved that it can replace real render work. A cached clamps docs capability reduced Moon execution to a cached 2 ms result and about 1.322 s through the wrapper instead of roughly 5.3 s through the cold wrapper path.

### SCons

- clamps/direct: **no SCons cache restore/save**;
- HUB75/SCons: normal target cache remains useful;
- Verification SCons cache: only create/transport it if a Verification engine actually populates it.

The warm HUB75 normal SCons archive was only about 222 KB, so this is a small transfer for a demonstrated target-reuse benefit.

## Artifact-transfer budget

Normal successful production currently duplicates its already-published output into 14-day Actions artifacts.

Representative retained compressed artifact sizes:

- clamps Build + Verification: roughly **245 KB** together;
- HUB75 Build + Verification: roughly **695 KB** together.

The byte totals are not huge, but they recur on every affected run and the upload actions also consume runner time. Since same-job publication does not download them and release uses separate exact-source artifacts, the target default is zero complete normal Build/Verification artifact uploads.

Compact impact/evidence artifacts remain because they answer a different audit/debugging need.

## Publication budget

The controlled publication probe `34994181268` showed on one runner:

- Build publisher: 2.089 s;
- Verification publisher: 2.144 s;
- measured overlap: 2.089 s;
- concurrent window: 2.144 s;
- sequential duration sum: 4.233 s.

This proves concurrency/isolation. It does **not** promise a fixed 2.089 s production saving because real output trees and GitHub network conditions differ.

Architecture budget: publication may overlap on the existing runner, but must never add another hosted runner solely for this finishing work.

## Capability-selection budget

The target does not ask one opaque aggregate root to execute every visible lifecycle step.

The host impact query already computes Moon's complete affected-task set once. The implementation should expose the affected coarse capability IDs and pass only those capabilities to the single CAD runtime.

Examples:

```text
README-only
  []

HUB75 render-only
  [scad.build]

HUB75 docs-only
  [scad.docs]

Verification-only
  [scad.verify]

shared API source change
  [one or more genuinely affected capabilities]
```

This is a work-elimination mechanism, not a parallelism trick.

## Expected latency envelopes

These are engineering budgets for implementation acceptance, not promises.

### Unrelated changes

Keep the proven host-only path approximately in the existing **4–6 s** class and start no CAD runtime.

### Clamps affected, cold capability output

Clamps must still pull the full image. Therefore Migration 005 should not claim a dramatic image-based speedup for this repository.

Relative to the current one-runner model, expected improvements are mainly:

- skip unused SCons cache actions;
- do not upload duplicate full normal artifacts;
- execute only affected coarse capabilities;
- overlap independent publication when it is material.

A cold all-capability clamps run should remain in roughly the **low-to-mid 40-second class** under similar registry conditions, with one heavy runner. A run with reusable Moon capability output can be lower because actual CAD work is removed.

If implementation remains near 49 s on a comparable runner after removing those known costs, investigate before accepting it.

### HUB75 affected with warm SCons reuse

The current warm reference is about 37 s with a 16 s full-image pull.

The target additionally has:

- ~27% less compressed image transfer;
- no duplicate full normal artifacts;
- no unused Verification SCons cache handling;
- selective coarse capability execution;
- same-runner publication overlap when useful.

A reasonable implementation acceptance envelope is approximately the **low-to-mid 30-second class** for a warm affected run under comparable registry conditions. The controlled image experiment itself improved one cold-pull sample by 2.253 s, but byte reduction is the stronger expectation than that single time difference.

A cold SCons graph can add several seconds of real CAD work, so cold relevant feedback around the **mid/high 30-second class** is plausible without violating the architecture goal.

## Compute/resource comparison

| Property | Old parallel | v0.13.1 one-host | Migration-005 target |
| --- | ---: | ---: | ---: |
| simultaneous heavy runners | 2 | 1 | **1** |
| CAD runtime starts | 2 | 1 | **1** |
| cold image demand | duplicated full image | one full image | **one capability-appropriate image** |
| unrelated change CAD runtime | avoidable/varied historically | 0 | **0** |
| Moon whole-output reuse | not reliably proven | transport present, identity issue fixed experimentally | **stable source-only identity required** |
| SCons handling | per job/path | generic normal + Verification slots | **only configured/populated paths** |
| normal full-tree artifact uploads | duplicated across jobs/workflows | 2 | **0 by default** |
| Build/Verify publication | separate/sequential paths | sequential same-host | **same-host overlap allowed** |

## Acceptance rule

Migration 005 implementation should be rejected if it improves stopwatch latency only by reintroducing duplicated heavy runners or duplicated image/runtime setup.

Likewise, it should be challenged if “resource efficiency” is achieved merely by serialising avoidable work and making feedback materially worse.

The intended order is:

1. eliminate work;
2. reuse work at the correct layer;
3. reduce runtime distribution cost;
4. overlap independent finishing work on the same runner;
5. add heavyweight parallel infrastructure only if measured feedback requirements still justify its extra compute cost.

## Conclusion

The provisional target has a credible resource and latency budget. It can plausibly recover much of the old parallel topology's feedback advantage for OpenSCAD/SCons projects while retaining the one-heavy-runner resource model.

Clamps is intentionally a harder speed case because it needs the full dual-runtime image; its acceptance case is primarily lower duplicated/unused work and stable capability reuse, not image slimming.

Final end-to-end timings must be measured during the owner-repository implementation/canary steps before broad consumer migration.
