# Software technical architecture

This page is the software-domain navigation layer for durable cross-repository architecture. Detailed implementation remains with the owning repositories.

## Repository and execution layers

The current shared software execution model is:

```text
GitHub Actions
  event / runner / artifact orchestration
        ↓
tool.git-project / Moon
  repository capabilities and affected selection
        ↓
tool.java-project
  shared Java policy and evidence
        ↓
Maven
  reactor / lifecycle / build / test authority
        ↓
software consumer
  project-specific source, metadata and release semantics
```

The durable production model is documented in [Java execution model](../../docs/working-model/java-execution.md).

## Platform qualification

Windows is not treated as an unconditional second build for every event.

The shared policy uses `auto | none | smoke | full`, with affected selection deciding whether Java work is required and whether native Windows qualification adds value. A protected-main publication reuses already-qualified canonical output rather than rebuilding merely to publish it.

## Generated evidence

Java execution retains build/test evidence separately from orchestration evidence. Timing distinguishes Maven/build time from runner, checkout, setup and artifact-transfer overhead.

Generated output follows the shared technical namespaces documented in [Generated output and publication](../../docs/working-model/generated-output.md).

## CI architecture qualification

The active reusable Java CI PoP adds another layer that is deliberately **not** production runtime infrastructure:

```text
target CI concept
      ↓
declarative testcase + deterministic fixture
      ↓
qualification in exp.2026-004.java-ci-architecture
      ↓
cross-project conclusion in brainboxemb.meta
      ↓
separate production migration when adoption is justified
```

This allows cache invalidation, fresh-runner reuse, cross-workflow behaviour and later production defects to be proven reproducibly without weakening production repositories just to experiment.

See the [experiment/PoP record](../../experiments/004-java-ci-architecture/README.md) for the current cross-project qualification status.
