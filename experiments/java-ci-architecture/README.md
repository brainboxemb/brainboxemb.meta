# Java CI architecture experiment

Status: **active — setup**

Tracking issue: [#69](https://github.com/brainboxemb/brainboxemb.meta/issues/69)

Planned experiment repository: `brainboxemb/exp.2026-004.java-ci-architecture`

Current prerequisite: **create the experiment repository**. Until that exists, implementation must not be pushed into `tool.java-project`, `template.java-project` or a product repository merely to make progress.

## Question

What generic Java/software CI architecture gives correct, reproducible and understandable incremental execution while avoiding unnecessary builds and runner usage?

The experiment must distinguish at least:

- repository-level affected selection;
- module/task-level invalidation;
- dependency caching;
- build-output caching/hydration;
- local versus cross-run/remote cache behaviour;
- test correctness after cache reuse;
- exact release qualification;
- Linux/Windows execution boundaries;
- retained machine-readable and human-readable evidence.

## Current baseline

The Migration-006 production model already provides useful orchestration:

- Moon determines whether Java and full-Windows capabilities are affected;
- unrelated changes can stop before Java execution;
- Maven remains Java build/test authority;
- ordinary Java PRs use exact-artifact Windows smoke;
- sensitive PRs and releases use native full Windows qualification;
- ordinary protected-main publication does not repeat Windows qualification.

What is not yet proven generically is incremental Java build execution itself. Current Java Moon tasks are impact declarations rather than cached build tasks, and canonical execution still performs Maven `verify` when Java execution is required.

## Experiment ownership

`brainboxemb.meta` owns:

- the research question;
- experiment status and sequencing;
- the cross-project decision record;
- the handoff to any later production rollout.

The dedicated experiment repository owns:

- Java fixture projects;
- candidate CI implementations;
- declarative test cases;
- the generic test harness/Action;
- GitHub workflow orchestration;
- retained experiment results.

Production owners are only changed after the experiment supports a decision.

## Test model

Prefer explicit declarative test cases over manual probing or case-specific shell logic.

Each test case should describe:

- starting fixture/revision/cache state;
- the controlled change applied;
- expected affected projects/tasks/modules;
- expected executed versus reused/cached work;
- expected tests and artifacts;
- expected platform/Windows policy where relevant;
- correctness assertions and evidence that must be retained.

A generic harness executes one case. GitHub Actions orchestrates a matrix of test cases and candidate architectures and publishes structured results.

Real GitHub event semantics that cannot be faithfully simulated inside one job may use a small separate end-to-end suite, but those cases should still be declared and automatically asserted rather than manually inspected.

## Candidate architectures

Compare at least:

1. current Maven baseline;
2. Maven-native build-cache/incremental capabilities;
3. Moon task/output cache capabilities;
4. hybrid Moon affected/orchestration plus Maven incremental/cache.

Do not preselect Moon or Maven as the incremental-build authority before evidence exists.

## Fixture requirements

Use a deterministic multi-module dependency graph that can distinguish leaf, shared and application changes, for example:

```text
        core
       /    \
feature-a  feature-b
       \    /
         app
```

The fixture should be deliberately small enough that orchestration/cache overhead is visible, while still exercising realistic Maven reactor and test behaviour.

## Initial testcase families

Cover at least:

- cold clean build;
- identical warm rebuild;
- unrelated documentation change;
- leaf-module source change;
- shared/core source change and dependent invalidation;
- application-only change;
- test-only change;
- module POM change;
- root POM change;
- dependency/plugin/compiler/toolchain change;
- warm cache on a fresh CI runner;
- cache miss and cache corruption fallback;
- artifact/test correctness after cache hydration;
- exact release qualification where correctness must not depend on an unsafe stale cache.

## Decision output

The experiment should finish with a documented answer to:

1. which layer decides whether Java work is affected;
2. which layer owns module-level incremental build/test decisions;
3. what may be cached and what must be rebuilt;
4. how cache keys and invalidation are derived;
5. which evidence proves execution versus hydration;
6. what release qualification deliberately bypasses or constrains;
7. which changes, if any, belong in `tool.java-project`, templates and consumers.

Only after that decision should a cross-project migration be created for production rollout.
