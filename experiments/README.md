# Experiments and Proofs of Principle

Cross-project experiments and Proofs of Principle (PoPs) are a first-class work track next to migrations. They provide controlled, reproducible evidence before production owners are changed.

A PoP is normally **design-first**: start from an explicit concept/architecture, then prove the runtime-sensitive principles that cannot be established confidently from design, documentation or existing evidence alone.

Implementation/evidence stays in an independent experiment repository. This directory records the cross-project question, target concept/status, evidence/decision and the handoff to later production work.

## Naming and document order

Experiment records use a three-digit prefix that matches the experiment number in the implementation/evidence repository where one exists:

```text
experiments/003-moon-scad-target-engine/
experiments/004-java-ci-architecture/
```

Keep the directory number stable for the lifetime of the experiment/PoP. Do not renumber older experiments when a newer one is added.

Within an experiment/PoP implementation repository, supporting documents under `docs/` use ordered numeric prefixes (`00-...`, `01-...`, `02-...`, ...). `README.md` remains the unnumbered entrypoint. This keeps the intended reading order explicit without numbering the entrypoint itself.

## Track states

- **active** — deliberately selected as current cross-project research/PoP work;
- **proposed / inactive** — defined but not started;
- **parked** — intentionally paused until a reactivation condition is met;
- **complete** — the current question/conclusion is closed with retained evidence.

A repository may remain useful after a track is complete. In particular, a PoP repository can stay as a repeatable qualification/regression lab even after its initial production migration has finished.

Completing a PoP/experiment does not automatically create or activate a migration. Production rollout is a separate decision.

## Design-first PoP model

Prefer this sequence when the architecture can be designed from established engineering knowledge:

```text
Concept / target architecture
        ↓
Proof of Principle
        ↓
Qualification
        ↓
Production migration
```

Do not turn a PoP into an open-ended tournament of candidate tools merely because alternatives exist. Implement alternatives when the target concept fails a principle or a concrete unresolved decision requires comparison.

A failed PoP is valid evidence and should cause the concept/assumption to be reconsidered; do not weaken the testcase to force success.

## Reusable PoP model

PoP repositories are preferably repeatable and retained. Later production/migration problems that can be represented faithfully should follow this loop:

```text
problem discovered
    ↓
reproduce as testcase in PoP repository
    ↓
prove failure and qualify correction
    ↓
fix production owner / migration
    ↓
retain regression testcase
```

This turns the original PoP into a durable CI architecture qualification suite rather than a disposable prototype.

## Active

### Java CI architecture PoP

[Java CI architecture PoP](004-java-ci-architecture/README.md) — **active — target concept defined; PoP qualification next**.

Tracks generic Java/software CI incremental execution, build-output reuse, module invalidation and reproducible qualification. Meta issue: [#69](https://github.com/brainboxemb/brainboxemb.meta/issues/69).

Implementation/evidence repository: `brainboxemb/exp.2026-004.java-ci-architecture`.

The reusable plain-Maven control harness is established on exact main `1f2dde6629e2acc6f6b86c482939c7752939c2f6`, run `35233519246`. The next work is the minimal Maven-native build-cache PoP, not bootstrap or repository creation.

## Parked

### Moon as SCAD target engine

[Moon as SCAD target engine](003-moon-scad-target-engine/README.md) — **parked**.

Tracks whether Moon can replace all or part of the current SCons target layer without losing fine-grained OpenSCAD dependency/selective-build behaviour. Meta issue: [#51](https://github.com/brainboxemb/brainboxemb.meta/issues/51).

## Experiment/PoP records

A useful record should state:

- implementation/evidence repository;
- problem or target concept;
- which assumptions require empirical proof;
- fixture and testcase model;
- evidence/result;
- decision the result supports;
- current state;
- where adopted production behaviour belongs;
- whether/how the repository remains reusable after adoption.

Prefer executable/declarative testcases and retained machine-readable evidence over one-off manual probing. Manual exploration can discover a question, but conclusions should be reproducible from the repository and CI where practical.
