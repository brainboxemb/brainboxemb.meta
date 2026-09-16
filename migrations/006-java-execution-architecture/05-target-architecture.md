# Migration 006 — draft target architecture

Status: **proposed / inactive design authority**

This document records the current preferred Java execution architecture. It is deliberately concrete enough to guide later implementation, but it does **not** activate Migration 006 while Migration 005 remains open.

## Design goals

The target should reduce consumer-owned orchestration, hosted-job count and unrelated-change cost without changing the Java build authority or weakening independent Windows compatibility.

The important distinction is:

- **Maven owns Java build and test semantics**;
- **Moon/tool.git-project owns affected selection and portable orchestration/materialization mechanics**;
- **tool.java-project owns reusable Java lifecycle execution and evidence**;
- **consumer repositories own product-specific inputs, metadata and release semantics that are genuinely domain-specific**.

## Target flow

```text
GitHub Actions caller in consumer
  exact event/source context + permissions
        |
        v
shared Java preflight (host)
  exact source/base
  one generic affected query
  Java-impact decision
        |
        +--> unrelated
        |      stop before JDK/Maven/Windows/publication
        |
        v
shared Linux canonical producer
  pinned native Temurin JDK
  pinned Maven Wrapper/Maven policy
  one canonical Maven lifecycle
  producer + test + provenance evidence
  exact portable materialization evidence
        |
        +----------------------+
        |                      |
        v                      v
optional Windows          publication finalizer
compatibility             repository side effect
  independent Maven         exact-source generated output
  exact Linux artifact      no duplicate evidence build
  smoke/compat evidence
        |
        v
shared result / durable timing evidence
```

Release execution remains a separate path because it has stronger exact-source and immutability requirements.

## Selected principles

### 1. Maven remains the Java build/test authority

Migration 006 does not expose Maven modules as fine-grained Moon build tasks and does not replace Maven dependency/build semantics with Moon.

The canonical producer remains one Maven lifecycle owned by `tool.java-project`. Moon may decide whether that capability must execute or may hydrate compatible materialization, but Maven remains authoritative when execution is required.

Fine-grained module-level Moon/Maven incrementality is explicitly outside the first migration.

### 2. Unrelated changes stop before Java setup

The current consumer workflows start Windows and Linux jobs before they know whether Java work is required. The target adds a cheap shared preflight before JDK, Maven or Windows runner allocation.

The preflight must:

- resolve the exact source revision and comparison base;
- fetch only history needed for the base→head decision where practical;
- use one generic affected query from `tool.git-project`;
- produce a small machine-readable decision/evidence record;
- stop cleanly when no Java capability is affected.

A README-only change is the primary zero-Java canary.

### 3. Consumer workflows become thin callers

Today `template.java-project` and the event-timing framework duplicate checkout/bootstrap, JDK setup, Moon invocation, evidence staging, artifact hand-off, Windows coordination and publication checks.

The target moves generic lifecycle ownership into released reusable workflows in `tool.java-project`.

A normal consumer caller should ideally contain only:

- triggers;
- permissions;
- one released `tool.java-project` reusable-workflow ref;
- small product-specific inputs/policy selections.

Exact committed tooling identity remains separate from the readable released workflow ref, following the same general identity principle already used in the SCAD generation.

### 4. Keep native Java execution

The current pinned Temurin/Maven model is retained unless measurements show a material reason to introduce a Java container.

Reasons to keep native execution as the default:

- Java setup is already explicit and reproducible;
- Maven dependency cache support is mature;
- Windows qualification must remain native anyway;
- a Java container would add another image lifecycle without currently solving the main orchestration problem.

### 5. Collapse duplicate evidence verification

The current consumers upload a prepared publication artifact and then start another Linux job largely to download and re-check evidence already produced by the canonical producer.

The target keeps validation close to the producer and transports only what a real runner/permission boundary requires.

Expected normal boundaries are:

- Linux canonical producer → Windows, because Windows must smoke the exact Linux artifact while also performing independent compatibility work;
- producer → publication finalizer only when a separate write-permission/side-effect boundary remains useful.

A separate hosted job solely to repeat deterministic file/grep assertions should disappear.

### 6. Windows remains independent but cadence becomes policy

Windows compatibility is a real architecture requirement, not a cosmetic matrix entry. It should continue to verify both:

- an independent native Windows Maven build/test path;
- the exact Linux-produced runnable artifact where applicable.

However, running both the Windows bootstrap contract check and full Windows compatibility on every ordinary main push is not assumed to be necessary.

The target makes Windows cadence an explicit shared policy. The leading candidate to qualify is:

- affected pull request: Windows required;
- release qualification: Windows required;
- ordinary post-merge main: Linux/publication required, Windows may be skipped when repository protection and exact-source evidence make the PR qualification sufficient;
- manual/exception path: Windows can be forced.

This cadence remains an **open qualification decision** until branch/release behaviour is verified in the reference template.

### 7. Publication remains a side effect, not a cacheable build task

Generated branch publication is repository state mutation and must remain outside Moon's portable cache graph.

`tool.java-project` should own the generic publication implementation and provenance contract. Consumers provide only names/paths/policy that are genuinely project-specific.

### 8. Release semantics are not broadened unnecessarily

The first Migration-006 implementation should not absorb every product release rule into shared Java tooling.

The event-timing framework currently has product-owned Maven version/tag metadata and failed-tag handling. Those rules remain product-owned unless a separate generic release migration proves a stable common contract.

For releases, the architecture must still guarantee:

- exact tagged/source commit execution;
- no acceptance of an equivalent earlier cached producer when exact release provenance is required;
- required Windows qualification;
- immutable release artifacts/tags according to the owning repository's policy.

### 9. Durable timing and compute evidence are first-class

The migration should measure both wall-clock latency and hosted compute, not just whether CI is green.

At minimum record:

- preflight duration;
- Linux canonical producer duration;
- Windows duration when selected;
- publication/finalization duration;
- total wall-clock to required evidence;
- number of hosted jobs/runners started;
- unrelated-change path and whether Java/Windows work was avoided.

## Ownership boundary

### `tool.git-project`

Owns only generic repository mechanics used by Java:

- exact base/head affected selection;
- Moon invocation/materialization infrastructure;
- generic repository validation/bootstrap primitives.

It must not gain Java/Maven semantics.

### `tool.java-project`

Primary implementation owner for Migration 006:

- Java execution policy/config validation;
- canonical Maven producer lifecycle;
- JDK/Maven setup contract;
- producer/test/provenance evidence;
- reusable Windows compatibility;
- shared Java preflight/production orchestration;
- generic generated-output publication;
- durable Java workflow timing/result evidence.

### `template.java-project`

Reference consumer and first canary:

- proves the thin-caller contract;
- proves unrelated-change zero-Java behaviour;
- qualifies affected Linux, Windows policy and publication;
- demonstrates that consumer-local lifecycle duplication can be removed.

### `2026-010-02.java.event-timing-framework`

Real downstream consumer:

- proves the architecture with multi-module/product-specific Java code;
- retains logging/dependency-boundary checks that are product architecture assertions;
- retains product-specific version/tag/release metadata where it is not generic;
- should no longer duplicate the generic Java lifecycle owned by `tool.java-project`.

## Explicit non-goals

Migration 006 does not initially:

- replace Maven with Moon;
- introduce a Java build container by default;
- split every Maven module into a Moon task;
- solve GitHub Actions dependency maintenance (Migration 007);
- redesign application/framework logging or domain architecture;
- make generic release semantics out of product-specific versioning without separate evidence;
- remove independent Windows qualification.

## Open decisions to qualify

Before implementation is considered complete, evidence must settle:

1. whether the default Windows cadence can safely be PR + release rather than every main push;
2. whether publication should be a final step in the Linux reusable workflow or a small separate write-permission job;
3. whether the preflight can reuse the current generic Moon affected interface unchanged or needs a small `tool.git-project` extension;
4. which Java project configuration fields are shared policy versus consumer-owned inputs;
5. what latency/hosted-compute target is realistic after eliminating the current duplicate jobs.

These are qualification questions, not reasons to keep the existing consumer-heavy workflow structure.