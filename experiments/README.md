# Experiments and test repositories

Cross-project experiments are a first-class work track next to migrations. They answer an architecture or tooling question with controlled, reproducible evidence before production owners are changed.

Experiment implementation stays in an independent experiment repository. This directory records the question, status, evidence/decision and the handoff to later production work.

## Experiment states

- **active** — deliberately selected as current cross-project research work;
- **proposed / inactive** — defined but not started;
- **parked** — intentionally paused until a reactivation condition is met;
- **complete** — concluded with retained evidence and a documented decision.

Completing an experiment does not automatically create or activate a migration. Production rollout is a separate decision.

## Active

### Java CI architecture

[Java CI architecture](java-ci-architecture/README.md) — **active — setup**.

Tracks generic Java/software CI incremental execution, caching, module invalidation and reproducible testcase orchestration. Meta issue: [#69](https://github.com/brainboxemb/brainboxemb.meta/issues/69).

Planned implementation repository: `brainboxemb/exp.2026-004.java-ci-architecture`.

The current prerequisite is creation of that repository. Production Java tooling must not be changed just to bootstrap the experiment.

## Parked

### Moon as SCAD target engine

[Moon as SCAD target engine](moon-scad-target-engine/README.md) — **parked**.

Tracks whether Moon can replace all or part of the current SCons target layer without losing fine-grained OpenSCAD dependency/selective-build behaviour. Meta issue: [#51](https://github.com/brainboxemb/brainboxemb.meta/issues/51).

## Experiment records

A useful experiment record should state:

- repository or required repository when setup is not complete yet;
- question/hypothesis tested;
- fixture and testcase model;
- evidence/result;
- decision the result supports;
- current state;
- where adopted production behaviour belongs.

Prefer executable/declarative testcases and retained machine-readable evidence over one-off manual probing. Manual exploration can discover a question, but experiment conclusions should be reproducible from the repository and CI where practical.
