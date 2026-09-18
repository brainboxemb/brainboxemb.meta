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

## Active project-backed work

### Detachable SCAD clip interface PoP

[Detachable SCAD clip interface PoP](005-detachable-scad-clip-interface/README.md)
— **active — OG-01/OG-02 qualified; AT-01 neutral coupon next**.

This PoP is driven by the current HUB75 display-frame project but deliberately
runs outside the production coupler source. It studies a compact fixed-side /
removable-side printed attachment inspired by OpenGrid, then qualifies a
detachable aluminium-tube clip on neutral coupons before production integration.

Meta issue: [#79](https://github.com/brainboxemb/brainboxemb.meta/issues/79).

Implementation/evidence repository:
[`brainboxemb/exp.2026-005.scad-detachable-clip-interface`](https://github.com/brainboxemb/exp.2026-005.scad-detachable-clip-interface).

External-source fork:
[`brainboxemb/fork.andylevesque.quackworks`](https://github.com/brainboxemb/fork.andylevesque.quackworks),
confirmed by GitHub as a fork of `AndyLevesque/QuackWorks` and pinned by the
experiment at exact source
`e0c1cb7ec78dd9e9a8476ed739bd3402074354f3`.

OG-01 and OG-02 were completed in
[experiment PR #1](https://github.com/brainboxemb/exp.2026-005.scad-detachable-clip-interface/pull/1)
and [PR #2](https://github.com/brainboxemb/exp.2026-005.scad-detachable-clip-interface/pull/2).
The reference evidence now includes Full/Lite assembled/exploded/section PNGs,
individual receiver/snap profile PNGs, complete printable parts and 1.0 mm
profile-slice STLs. Lite is the primary reduction reference for AT-01.

This project-backed PoP does not authorize production integration before the HUB75 project reaches its own core-interface freeze gate.

## Complete

### Java CI architecture PoP

[Java CI architecture PoP](004-java-ci-architecture/README.md) — **complete — initial architecture qualification closed; reusable regression lab retained**.

The PoP qualified Maven-native module reuse, build-model/runtime invalidation, fresh-runner and cross-workflow shared reuse, representative real-consumer latency value, product-scoped Git build-identity invalidation, and the final release/canonical-artifact cache policy.

Final owner baseline:
- Git-identity correction/evidence main `e30c71c2f7404a49900c301c6dceac064abd8e5d`;
- release/cache-policy main `2353b18ccfd90c25c9cc7fab65e1a2a8f2b73da9`;
- final policy PR regression run `35359099065` — 30/30 green.

The result supports a later production adoption decision but does not automatically activate a migration. The implementation/evidence repository remains available for future migration/production regressions.

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
