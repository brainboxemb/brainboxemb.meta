# Java CI architecture PoP

Status: **complete — initial Java CI PoP/qualification closed; reusable regression lab retained**

Tracking issue: [#69](https://github.com/brainboxemb/brainboxemb.meta/issues/69)

Implementation/evidence repository: `brainboxemb/exp.2026-004.java-ci-architecture`

## Role

This is a **design-first Proof of Principle (PoP)** and reusable qualification track for the generic Java/software CI architecture.

The working model is:

```text
Concept / target architecture
        ↓
Proof of Principle
        ↓
Qualification
        ↓
Production migration
```

The architecture is not discovered by blindly implementing every possible candidate. The target concept is designed first; the PoP proves only the assumptions that require runtime evidence.

The PoP repository remains after initial rollout as a reusable qualification/regression environment. When a later migration or owner repository exposes a Java CI problem that can be represented faithfully by the fixture, prefer to reproduce it there, qualify the correction, apply the production fix through the real owner, and retain the case as regression coverage.

## Current target concept

The intended responsibility split is:

- **GitHub Actions** — event, runner, job and artifact orchestration;
- **Moon / generic repository tooling** — repository/capability affected selection and platform policy;
- **Maven** — reactor, lifecycle, build and test authority;
- **Maven-native build cache** — optional module-level incremental/cache optimization, configurable as `none | local | shared`;
- **publication** — reuses canonical prepared build output and does not rebuild merely to publish.

Maven-native build caching is the first mechanism to qualify because module-level reuse belongs naturally inside Maven semantics if it proves correct, observable and portable. Moon output caching remains an alternative/complement only when a concrete PoP result leaves a material requirement unresolved.

## Qualified local PoP evidence

The reusable harness and local Maven Build Cache PoP are qualified on experiment main:

- exact source `bc5d1b16da3820b72430611b65969ec7fb0588d0`;
- exact-main run `35250860673` — green across discovery plus 14 control/cache jobs;
- deterministic graph `core -> feature-a/feature-b -> app`;
- seven self-verifying declarative cases;
- native Maven cache report retained and normalized;
- class/test/JAR workset and semantic JAR payload measured separately.

The local result supports Maven-native caching as a strong architectural candidate: unchanged/docs-only work is fully reused; app-local changes stay within the app module; shared-core changes invalidate the dependent graph; test-only changes rerun the affected module tests without changing production payload.

Caching remains an **optimization, not a correctness dependency**. The intended modes are:

```text
none    ordinary Maven lifecycle, no build-cache reuse
local   Maven Build Cache local reuse
shared  cross-run/shared Maven Build Cache reuse
```

`none` is the safe initial/default mode. A forced-fresh/cache-bypass path remains available regardless of configured mode.

## Qualified build-model/cache-independent evidence

The second correctness slice is qualified on:

- exact source `4106f71f09ef98e3a5ce5a1a9b965f27219cf0e7`;
- exact-main run `35317952373` — green across discovery plus all 22 control/cache testcase jobs;
- CI-08 root/shared build-model invalidation;
- CI-09 module-local build-model invalidation;
- CI-10 shared dependency-version invalidation;
- CI-11 cache-independent execution of the same Maven lifecycle;
- result schema v3 retaining native `source_raw` plus normalized execution state;
- deterministic unmeasured extension/dependency preparation before prime/measured timing.

This strengthens the conclusion that Maven-native caching can remain an optional optimisation rather than a correctness dependency. Cache-independent execution is intentionally distinct from a `clean` build with empty output directories.

## Qualified runtime/fresh-runner evidence

The third qualification slice is now on:

- exact experiment main `7bdf9017d543a81d48557968a232b39890b9b642`;
- exact-main run `35320255528` — all 28 jobs green;
- CI-12 actual Maven runtime JDK 8 → 17 invalidation;
- CI-13 separate hosted-runner producer/consumer reuse;
- CI-14 explicit transported-cache miss fallback;
- result schema v4 with prime/measured runtime evidence and fresh-runner provenance.

The PoP exposed and corrected two design gaps instead of weakening the tests:

1. Maven Build Cache 1.3.0 did not itself separate cache state for the tested Maven runtime JDK change, so the adapter now partitions cache storage by JDK release metadata, OS/architecture and exact Maven Wrapper identity.
2. Fresh-runner reuse initially restored module artifacts but not Surefire XML, so `surefire-reports` is now an attached Maven Build Cache output.

The qualified shared path keeps GitHub Actions as opaque cache transport while Maven remains the module validity/restore authority.

## Qualified cross-workflow persistence evidence

CI-15 now proves the useful production form of `shared`: Maven build-cache state survives from one GitHub Actions workflow run to a later workflow run.

Exact qualification evidence:

- experiment main `681ce7b9d56973b5540cb314c8e45e25618915a0`;
- producer run `35323272710` — all four modules `BUILD`, Maven cache populated from 0 to 12 files;
- later consumer run `35323361468` — exact transport hit on the same source, zero module outputs before Maven, all four modules `LOCAL`, four JARs restored and five Surefire reports restored;
- producer and consumer workflow-run IDs are different;
- all CI-15 correctness and qualification assertions pass;
- evidence/capability promotion merged in the experiment repository as `0d59eb6af11eff0db311650fd9b1a6aa30f8eb4f`;
- PR regression run `35324923371` — 28/28 jobs green.

This qualifies `cross_workflow_output_cache = true` for the Maven Build Cache candidate.

## Qualified representative production-value evidence

The PoP then used the exact current real-consumer workload:

```text
brainboxemb/2026-010-02.java.event-timing-framework
0f9dbc2f5aa0beaec8f63465ada83f2bc2a83709
```

Two independent exact-main benchmark pairs were retained:

- experiment `2d9ac9af9006725576009b5c453590800a1a7337` — producer `35335319664`, separate consumer `35335436917`;
- experiment `d47d10ae0cb2be7828310331a8fed8121e10d0fd` — producer `35335827417`, separate consumer `35335932166`.

Across six matched control/shared samples:

- later-run paired savings were `16, 14, 4, 3, 9, 2 s`;
- all 6/6 shared consumers were faster;
- median paired later-run saving was **6.5 s / 28.8%**;
- producer+consumer hosted-compute deltas were `10, 10, -1, 0, 9, -2 s`;
- therefore structural hosted-runner cost reduction is **not** qualified;
- the second run retained about 153 kB of Maven build-cache state, with median save/restore steps of about 1 s.

The completed owner evidence is retained on experiment main `5c3aabe2e38a7607eb3401445ee707cd244d5161`. This supports `shared` as an optional latency optimisation, not as a guaranteed compute-cost optimisation. `none` remains a valid safe/default mode.

## Qualified Git build-identity evidence

CI-16 used the immutable real-consumer workload to change Git commit identity while keeping the tracked Git tree identical.

The initial baseline correctly failed:
- run `35336851477`;
- both `event-timing-framework` and `event-timing-app` restored as `LOCAL`;
- the consumer app JAR retained the producer revision.

The qualified correction is product/module-scoped rather than repository-wide: the app module declares `maven.build.cache.input.1=../.git/HEAD`. Qualified run `35337342442` then proves:
- zero consumer module outputs before Maven;
- identical producer/consumer Git tree;
- `framework=LOCAL`;
- `app=BUILD`;
- app JAR embeds the exact consumer revision.

The retained correction/evidence is on experiment main `e30c71c2f7404a49900c301c6dceac064abd8e5d`; final PR regression run `35358585970` was 30/30 green.

## Qualified release/canonical-artifact policy

The final policy is retained on experiment main `2353b18ccfd90c25c9cc7fab65e1a2a8f2b73da9`; PR regression run `35359099065` was 30/30 green.

The qualified policy is:

```text
normal PR/main canonical
  project-selected none | local | shared
  all material inputs participate in cache validity
  hydrated output retains original producer evidence

exact release tag
  fresh/empty module output
  no Maven build-output cache read/write
  Maven dependency cache allowed
  ordinary canonical Maven lifecycle
  full release evidence/platform qualification

publication
  consume prepared canonical output
  never rebuild merely to publish
```

No additional CI-17 was needed: CI-11 already proves cache bypass within the Maven lifecycle, while immutable real-consumer release run `35211641563` proves the stronger exact-tag fresh hosted-runner boundary with no build-output cache configured.

## Completion and production handoff

The initial Java CI PoP/qualification set is **complete**.

It supports a later cross-project adoption decision with these constraints:
- caching remains optional and project-configurable as `none | local | shared`;
- `shared` has qualified later-run latency value, not guaranteed hosted-compute savings;
- runtime-specific cache namespace and restored Surefire outputs are correctness/evidence requirements;
- product modules declare material non-source inputs such as embedded Git identity;
- exact-tag release remains fresh/cache-independent;
- publication reuses prepared canonical output.

No production migration is active. Completing this PoP does not create one automatically.

## Ownership

`brainboxemb.meta` owns:

- the cross-project problem and target concept;
- active status/sequencing;
- architecture decision and production handoff;
- the decision whether a later migration should start.

`brainboxemb/exp.2026-004.java-ci-architecture` owns:

- the reusable fixture;
- declarative PoP/qualification/regression cases;
- generic harness/Action and workflow orchestration;
- PoP adapters/mechanisms;
- retained experimental/qualification evidence.

Production repositories remain the implementation owners of production behaviour.

## Reuse rule

The PoP is not disposable. After production adoption:

```text
new migration/production CI issue
        ↓
minimal reproducible testcase in PoP when faithful
        ↓
prove failure
        ↓
qualify correction
        ↓
owner fix / migration
        ↓
retain testcase as regression coverage
```

Do not force product-specific behaviour into the PoP when the fixture cannot reproduce it without losing the real failure mode.

## Production handoff

Only after concept + PoP + required qualification support a decision should a production migration be created/activated. The normal rollout owner chain remains:

```text
tool.git-project -> tool.java-project -> template.java-project -> real consumers
```
