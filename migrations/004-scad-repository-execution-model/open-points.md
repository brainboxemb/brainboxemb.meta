# Migration 004 — open points handed to Migration 005

Migration 004 is **complete**. These points are not unfinished qualification work for 004; they are architecture questions discovered while closing it and deliberately handed to [Migration 005](../005-scad-execution-architecture/README.md).

## 1. Relevant-change latency did not beat the old baseline

On the simple `lib.scad.clamps` reference:

- old parallel Build + Verify: about **37 s** critical path;
- final v0.13.1 one-host model: about **41–45 s**.

The final architecture uses less duplicated runner/container work but leaves the developer waiting roughly 4–8 seconds longer for an affected change.

Migration 005 must treat both latency and total compute as separate metrics.

## 2. Docker image acquisition is the largest single measured cost

Representative final run `34971400621` spends about **20 s** pulling `ghcr.io/brainboxemb/scad-toolchain:v0.4.1`, while the Moon output graph itself reports about **5.1 s**.

The current workflow explicitly caches Moon and SCons state but does **not** explicitly cache the Docker/OCI image or Docker layer store. The representative run downloads all layers and reports `Downloaded newer image`.

Open questions:

- exact compressed/layer sizes;
- network versus unpack/startup time;
- whether an explicit image cache is cheaper than GHCR pull on disposable hosted runners;
- whether the image itself can be made materially smaller without losing the qualified runtime contract.

## 3. Moon impact checking is valuable but not free

README-only changes prove that the host impact check is useful: they finish in roughly 4–5 s and never start the SCAD runtime.

For an affected change, however, the impact path adds several seconds before the runtime can start.

Migration 005 must break that cost down and decide which evidence/runtime-restore work really belongs before the expensive boundary.

## 4. Moon and SCons need a clearer architectural boundary

The intended division is repository-level capability selection/cache in Moon and fine-grained CAD target decisions in SCons.

The current consumer graphs are detailed enough that this boundary is no longer obvious. Migration 005 must verify that the two engines are complementary rather than duplicating dependency semantics.

## 5. The consumer Moon graph exposes too much orchestration detail

`lib.scad.clamps` exposes seven Moon tasks and `lib.scad.hub75` eight. Several are finishing/orchestration tasks rather than things a project maintainer naturally thinks of as capabilities.

Open questions include:

- whether standard SCAD Moon policy should move into `tool.scad-project`;
- whether the consumer can declare only domain capabilities and exceptional inputs;
- whether the source-impact versus publication-context distinction can remain internal instead of appearing as two no-op roots.

## 6. `tool.scad-project` already has coarser producer commands

`produce-build` and `produce-verification` already compose complete results, while the current Moon graph separately exposes index/source-information steps.

Migration 005 must decide which of those is the intended stable architecture boundary rather than keeping both models indefinitely.

## 7. Evidence distinctions are useful but may be over-exposed

Producer execution, current materialization and publication context are legitimately different facts.

The open question is whether maintaining that truth really requires several consumer-visible tasks, or whether shared tooling can preserve the evidence model behind a simpler contract.

## 8. Same-job staging/artifact/publication overhead needs justification

The final lifecycle still:

- stages generated trees;
- uploads Build and Verification workflow artifacts;
- publishes Build and Verification sequentially.

Migration 005 must determine which artifacts are genuinely retained/consumed later and which operations are historical hand-offs that can be removed or overlapped safely.

## 9. HUB75 frame rollout is intentionally deferred

The HUB75 frame remains on the previous qualified model. This is deliberate: the current architecture should not be propagated further while its complexity and critical path are under review.

Its eventual migration belongs to Migration 005 after a target architecture has been selected and qualified.

## Closure interpretation

Migration 004 is therefore closed as:

> **technically qualified, released, and measurably better at avoiding unnecessary heavy work, but not accepted as the final long-term SCAD execution architecture.**

Migration 005 owns the complete architecture reflection and any resulting simplification or performance improvement.
