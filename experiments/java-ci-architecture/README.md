# Java CI architecture PoP

Status: **active — target concept defined; PoP qualification next**

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
- **Maven-native build cache** — first PoP mechanism for module-level incremental/cache semantics;
- **publication** — reuses canonical prepared build output and does not rebuild merely to publish.

Maven-native build caching is the first mechanism to qualify because module-level reuse belongs naturally inside Maven semantics if it proves correct, observable and portable. Moon output caching remains an alternative/complement only when a concrete PoP result leaves a material requirement unresolved.

## Existing control evidence

The reusable harness/control baseline is already on experiment main:

- exact source `1f2dde6629e2acc6f6b86c482939c7752939c2f6`;
- exact-main workflow run `35233519246` — green;
- deterministic graph `core -> feature-a/feature-b -> app`;
- cases CI-01 through CI-05;
- declarative TOML cases, generic harness and GitHub Actions matrix;
- normalized machine-readable result/evidence including exact source/run/toolchain provenance.

The plain-Maven control shows:

- warm/no-op: no module JAR rewrite, but all Surefire reports rewritten;
- docs-only: no module JAR rewrite, but all Surefire reports rewritten;
- app-only: only app JAR rewritten, but all Surefire reports rewritten;
- core change: all module JARs and Surefire reports rewritten.

This is control evidence, not the architecture decision.

## Minimal PoP

The next step is to qualify the smallest set of principles needed to trust the target concept:

1. unchanged warm module reuse;
2. application-only selectivity;
3. shared/core dependent invalidation;
4. representative build-model/toolchain invalidation;
5. fresh-runner cross-run reuse;
6. forced-fresh execution for correctness-sensitive qualification.

Correctness and observability are gates. Performance is evaluated after those pass.

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
