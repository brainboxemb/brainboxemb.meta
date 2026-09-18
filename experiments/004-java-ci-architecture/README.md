# Java CI architecture PoP

Status: **active — local/model qualification complete; cross-run qualification next**

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

## Remaining qualification

The next qualification work is:

1. actual toolchain/input identity invalidation;
2. fresh-runner/cross-run shared-cache transport and reuse;
3. unavailable/missing shared-cache fallback where practical;
4. repeated performance measurements on representative workloads;
5. release/canonical-artifact policy, including whether releases require separate empty-output clean qualification.

No production migration is active yet.

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
