# Migration 005 — SCons warm-cache validation

Status: **validated**

This validation answers one narrow architecture question:

> Does SCons provide measurable target-level reuse on a real SCAD repository that explicitly selects the SCons build engine?

The answer is **yes** for `lib.scad.hub75`.

## Test boundary

No source or library implementation was changed for this measurement.

The existing qualified exact-main production run was rerun against the same source revision:

- repository: `brainboxemb/lib.scad.hub75`;
- workflow run: `34976840416`;
- exact source: `5f2ed2ae3e6901e10c1b14efeed5285bdde779da`;
- original job: `104406598990`;
- warm-cache rerun job: `104442409672`;
- SCAD tool: `tool.scad-project v0.13.1`, exact source `28661fc040c4994e9c1d391285b7425c7a55252b`;
- runtime image: `ghcr.io/brainboxemb/scad-toolchain:v0.4.1`.

`lib.scad.hub75` explicitly selects:

```yaml
build_engine:
  engine: scons
```

The first attempt had already saved the normal SCons object cache. The second attempt therefore provides a fresh-hosted-VM warm-cache measurement without introducing a diagnostic branch.

## Cache transfer

Attempt 2 restored the normal SCons cache from attempt 1:

```text
Cache hit for restore-key:
scad-production-build-scons-v1-Linux-1361750675-v0.4.1-28661fc040c4994e9c1d391285b7425c7a55252b-34976840416-1

Received 222110 of 222110
Cache restored successfully
```

So the portable SCons cache transfer was only about **222 KB** in this example.

The separate Verification SCons cache had no entry:

```text
Cache not found for input keys:
scad-production-verification-scons-v1-...
```

That matches the current HUB75 Verification path: it is not using the separate SCons target cache.

## Presentation-render result

The presentation-build capability had two SCons targets.

Attempt 2 restored both from cache:

```text
Retrieved `bld/png/hub75-p5-64x32-panel-front-angled.png' from cache
Retrieved `bld/png/hub75-p5-64x32-panel-rear-angled.png' from cache
SCons summary: targets=2 built=0 cache-restored=2 current=0 error=0
```

Measured Moon task duration:

- original exact-main attempt: about **2.0 s**;
- warm SCons attempt: **0.430 s**.

No presentation render had to be recomputed.

## Design-documentation result

The design-documentation capability had 26 SCons targets.

Attempt 2 restored all 26 generated images from cache:

```text
SCons design summary: targets=26 built=0 cache-restored=26 current=0 error=0
```

Measured Moon task duration:

- original exact-main attempt: about **8.07 s**;
- warm SCons attempt: **0.602 s**.

No design image had to be rerendered.

## Verification remains real work

Verification still executed normally and took about **4.403 s** in the warm attempt. The separate Verification SCons cache was not populated or restored.

This is useful evidence: a generic lifecycle should not restore/save a Verification SCons cache merely because some other capability in the repository uses SCons.

## Complete graph effect

The original exact-main Moon graph was about **8.805 s**, with presentation Build, design documentation and Verification overlapping where possible.

The warm-SCons rerun completed the Moon graph in about **5.071 s**:

- presentation Build: **0.430 s**, all 2 targets cache-restored;
- design documentation: **0.602 s**, all 26 targets cache-restored;
- Verification: **4.403 s**, real work;
- full graph: **5.071 s**.

The remaining critical path is therefore Verification rather than Build/docs rendering.

## Docker still dominates the outer lifecycle

Even though SCons avoided all 28 Build/docs render targets, the fresh hosted runner still downloaded all 11 SCAD image layers.

For this rerun the image step ran from approximately `15:15:57.323` until the image became available at `15:16:13.309`: roughly **16 seconds**.

This is several times larger than the entire warm Moon graph and much larger than the SCons cache restore itself.

So SCons cache reuse is real and useful, but reducing Docker image-distribution cost remains a higher-leverage end-to-end latency question.

## Architecture conclusion

This validation supports the provisional Migration-005 boundary:

```text
Moon
  whole capability identity, change-impact selection and complete-output reuse

SCons, when the capability selects it
  individual target dependency checks and target-level cache reuse
```

These are different levels rather than duplicate caches for the same decision.

A capability restored completely by Moon does not need to invoke SCons. When the capability itself must execute, SCons can still avoid rebuilding its unchanged targets.

The workflow must therefore derive SCons cache handling from the effective project/capability configuration:

- no SCons engine -> no SCons cache restore/save;
- SCons Build/docs capability -> restore/save the applicable SCons cache;
- Verification SCons cache -> only when Verification actually uses that engine/cache.

## Validation result

**Passed.**

Warm SCons reuse is demonstrated on the richer HUB75 library and materially reduces target execution with a small cache transfer. This validation no longer blocks the provisional target architecture.

The next highest-leverage validation is SCAD Docker image distribution because it remains the dominant fresh-runner cost after both Moon and SCons reuse are working.