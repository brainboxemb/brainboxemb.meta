# Migration 005 — target lifecycle resource and latency budget

Status: **complete — final implementation measured against the budget**

This document separates structural/resource targets from network-sensitive wall-clock targets. The final closeout keeps that distinction explicit: the architecture/resource goals are met, the affected canary latency envelopes are met, and the unrelated-change 4–6 second wall-clock ambition is only partially met.

## Reference points

### Old parallel topology

Migration 004 measured roughly **37 s** relevant-change critical-path feedback with separate Build and Verification heavy jobs.

That path used two simultaneous heavy hosted jobs, duplicated setup/image/runtime work and therefore consumed substantially more total heavy runner time than its 37 s critical path suggested.

### Migration-004 one-runner references

Representative v0.13.1 observations:

- clamps high-overhead sample `34972350665` attempt 2: ~49 s hosted job, ~19 s full-image pull, generic unused SCons handling, duplicate complete normal artifacts;
- warm HUB75 `34976840416` attempt 2: ~37 s hosted job, ~16 s full-image pull, useful normal SCons cache, unused Verification-SCons path, duplicate complete normal artifacts;
- README-only controls: ~4.4–4.8 s with zero CAD runtime.

These were the inputs to the Migration-005 budget, not guaranteed future timings.

## Target structural budget

For a normal affected run:

```text
hosted heavy runners     1
CAD image pulls          1
CAD runtime starts       1
Moon impact analyses     1
full normal artifacts    0 by default
SCons cache paths        only those actually useful
Build/Verify publication isolated publishers, allowed to overlap on the same runner
```

For an unrelated change:

```text
hosted workflow runner   1 short host-only path
CAD image pulls          0
CAD runtime starts       0
CAD work                 0
```

### Final structural result

**Met.**

The released v0.14.7 production path uses one hosted job, one generic affected query, at most one CAD Docker process, capability-appropriate runtime selection and only applicable SCons transport. Normal successful production retains compact orchestration evidence rather than another complete copy of Build/Verification output. Build and Verification publication can overlap on the same runner.

Three independent README-only probes prove zero CAD work for an unrelated change.

## Image-transfer budget

Externally qualified v0.5.0 runtime profiles:

| Runtime profile | Compressed OCI bytes |
| --- | ---: |
| OpenSCAD-focused | 328,098,501 |
| full/dual | 449,516,893 |

An OpenSCAD-only affected repository therefore avoids **121,418,392 compressed bytes**, about **27.0%**, relative to the full image.

Final behaviour:

- clamps intentionally uses the full/dual image because it supports PythonSCAD;
- HUB75 selects the focused OpenSCAD image;
- normal production requests only one capability-appropriate image.

Result: **met**.

## Cache-transfer budget

Final policy/result:

- Moon whole-capability cache: retained and proven useful;
- clamps/direct: no normal or Verification SCons cache transport;
- HUB75/SCons: normal SCons transport retained and useful;
- command-only HUB75 Verification: no Verification-SCons transport;
- direct projects do not pay generic SCons transport merely because another project uses SCons.

Result: **met**.

## Artifact-transfer budget

Target: no duplicate complete normal Build/Verification Actions artifacts by default; retain compact decision/orchestration evidence. Coordinated release remains different because its separate Build/Verify/finalize jobs genuinely require complete cross-job artifacts.

Final result: **met**.

## Publication budget

Controlled probe `34994181268` proved isolated Build/Verification publishers can overlap safely on one hosted runner. The migrated consumers use same-runner publication rather than adding a second hosted VM solely for finishing.

Result: **met**.

## Capability-selection budget

Target: compute one complete Moon affected-task result, map it to coarse SCAD capabilities and avoid the SCAD planner/runtime entirely when no configured SCAD capability is affected.

Final v0.14.7 zero-runtime template probe `35085786014`:

```text
Moon decision           success
affected task ids       []
workflow affected       false
host Python/planner     skipped
Moon/SCons transport    skipped
runtime pull            skipped
Docker materialization  skipped
host finishing          skipped
publication             skipped
```

Result: **met**.

## Expected versus measured latency

The original envelopes were engineering budgets, not guarantees. Final measurements are:

| Scenario | Target | Measured | Result |
| --- | ---: | ---: | --- |
| unrelated change | ~4–6 s, zero CAD | HUB75 ~7.6 s | zero-CAD met; latency partial |
| unrelated change | ~4–6 s, zero CAD | clamps ~9.2 s | zero-CAD met; latency partial |
| unrelated change | ~4–6 s, zero CAD | template ~9.9 s | zero-CAD met; latency partial |
| clamps affected canary | low/mid 40 s | ~41.9 s | met |
| HUB75 warm affected canary | low/mid 30 s | ~32.2 s | met |

The first migrated main runs were ~48.1 s for clamps and ~47.1 s for HUB75. They are intentionally not treated as steady-state selective-impact benchmarks because both were migration/tool-gitlink changes before later exact-base-gitlink hardening and included cold/conservative conditions.

### Why the unrelated path is still 7.6–9.9 s

The heavy SCAD stages are genuinely absent. The remaining time is mostly fixed generic host-preflight overhead:

- GitHub Actions job/action preparation and downloads;
- exact shallow source/base checkout;
- initialization of the pinned SCAD task-policy gitlink;
- restore of the generic Moon runtime;
- one Moon affected query;
- compact evidence upload and job cleanup.

In template run `35085786014`, restoring the ~20 MB Moon 2.5.4 runtime alone took about **2.0 s** and the affected query about **1.2 s**. No SCAD planner, image or CAD process started.

This makes the remaining optimisation boundary clear: reduce generic preflight fixed cost without weakening exact source/base correctness or reintroducing false skips. It is not evidence that the SCAD runtime architecture should be reopened.

## Compute/resource comparison

| Property | Old parallel | v0.13.1 one-host | Migration-005 final |
| --- | ---: | ---: | ---: |
| simultaneous heavy runners | 2 | 1 | **1** |
| CAD runtime starts | 2 | 1 | **<=1** |
| cold image demand | duplicated full image | one full image | **one capability-appropriate image** |
| unrelated change CAD runtime | avoidable/varied historically | 0 | **0** |
| Moon whole-output reuse | not reliably proven | transport present | **stable source-only identity, proven reuse** |
| SCons handling | per job/path | generic normal + Verification slots | **only configured/populated paths** |
| normal full-tree artifact uploads | duplicated | 2 | **0 by default** |
| Build/Verify publication | separate heavy paths | sequential same-host | **same-host overlap allowed** |
| durable workflow timing/provenance | limited | limited | **generated snapshot timing + exact source provenance** |

## Acceptance rule and final decision

Migration 005 was not allowed to improve stopwatch latency by reintroducing duplicated heavy runners, duplicated image acquisition or duplicate CAD runtime setup.

The final implementation follows the intended priority order:

1. eliminate unrelated CAD work;
2. reuse whole capabilities with Moon;
3. reuse fine-grained targets with SCons only where configured;
4. reduce runtime distribution cost with focused/full profiles;
5. remove duplicate normal artifacts;
6. overlap independent finishing work on the same runner.

Final acceptance:

- correctness/publication model: **accepted**;
- resource model: **accepted**;
- clamps affected envelope: **accepted**;
- HUB75 warm affected envelope: **accepted**;
- unrelated zero-CAD behaviour: **accepted**;
- unrelated 4–6 s latency envelope: **not fully achieved; non-blocking generic preflight follow-up**.

The partial latency miss is retained as evidence rather than being used to keep a completed SCAD architecture migration artificially open.
