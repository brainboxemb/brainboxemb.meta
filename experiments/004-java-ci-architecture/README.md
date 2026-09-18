# Java CI architecture PoP

Status: **active — local Maven Build Cache PoP qualified; broader qualification in progress**

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

## Remaining qualification

The next qualification work is deliberately ordered:

1. root/module POM and representative dependency/plugin/configuration invalidation;
2. forced-fresh/cache-bypass correctness;
3. actual toolchain invalidation and fresh-runner/cross-run reuse;
4. missing/corrupt cache fallback where practical;
5. repeated performance measurements;
6. release/canonical artifact implications.

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
