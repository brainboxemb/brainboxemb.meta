# Migration 006 — target architecture

## Why this document exists

The migration README says what problem Migration 006 solves; this document says **what the Java execution architecture should look like when the migration is done**. It prevents implementation details from silently redefining ownership while `tool.java-project`, the template and the real consumer are changed in sequence.

Use this document to review an implementation choice against the intended end state. Ordered rollout steps and required evidence belong in [06 — Implementation and qualification plan](06-implementation-plan.md).

Status: **active design authority**

The generic project-family/documentation boundary is defined in [Project families, coordination and engineering documentation](../../docs/working-model/project-families-and-documentation.md). Migration 006 stays inside that boundary.

## Design goals

Reduce consumer-owned orchestration, hosted-job count and unrelated-change cost without changing Java build authority or losing meaningful Windows qualification.

Ownership is intentionally layered:

- **Maven** owns Java build/test semantics;
- **Moon / `tool.git-project`** owns generic affected selection and portable orchestration/materialization mechanics;
- **`tool.java-project`** owns reusable Java lifecycle execution and Java-derived evidence/artifacts;
- **`tool.eng-docs`** owns generic engineering-documentation mechanisms and assembly;
- **consumers** own product-specific inputs, impact declarations and release semantics that are genuinely product-specific.

## Target flow

```text
consumer GitHub Actions caller
  event/source context + small policy inputs
        |
        v
shared Java preflight
  exact source/base
  generic affected query
  Java impact + Windows impact classification
        |
        +--> Java unrelated
        |      stop before JDK/Maven/Windows/publication
        |
        v
shared Linux canonical producer
  pinned native Temurin JDK
  repository Maven Wrapper
  one canonical Maven lifecycle
  artifact + test + provenance evidence
        |
        +---------------------------+
        |                           |
        v                           v
selective Windows              Java-output finalizer
qualification                  repository side effect
  none / smoke / full            exact-source output
                                  no duplicate Maven build
        |
        v
shared result + durable timing/job-selection evidence
```

Project-family engineering-documentation production remains a separate generic flow. It may consume Java-produced assets/manifests such as Javadoc or verification evidence, but Java does not assemble the SDP/SIP/SVP/architecture document set.

## 1. Maven remains the Java build/test authority

Migration 006 does not replace Maven dependency/build semantics with Moon and does not initially split Maven modules into fine-grained Moon build tasks.

When Java execution is required, one canonical Maven lifecycle is authoritative. Moon decides **whether** a capability is affected and may support materialization; it does not become the Java build engine.

## 2. Unrelated changes stop before Java setup

The shared preflight must:

- resolve exact source and comparison base;
- fetch only history needed for base→head classification where practical;
- use the generic affected interface from `tool.git-project`;
- produce compact machine-readable decision evidence;
- stop before JDK, Maven, Windows and Java-output publication when Java is unrelated.

A README-only change remains the primary zero-Java canary.

## 3. Consumers become thin callers

A normal Java consumer caller should contain only:

- triggers;
- permissions;
- one released `tool.java-project` reusable-workflow ref;
- product paths/artifact names and small policy inputs.

Checkout/bootstrap, JDK setup, canonical Maven execution, evidence staging and Windows coordination should not be copied into each consumer.

Readable released workflow identity and exact committed tooling identity remain separate concepts, following the same principle used by the final SCAD architecture.

## 4. Native Java execution stays the default

Keep pinned native Temurin/Maven execution unless measurements show a real need for a Java container.

Reasons:

- Java setup is already explicit and reproducible;
- Maven dependency caching is mature;
- meaningful Windows qualification must remain native;
- a Java container would add an image lifecycle without solving the current orchestration duplication.

## 5. Windows qualification is selective

Windows support is a real compatibility requirement, but a full second Maven build is not required for every affected PR.

The shared policy input is:

```text
windows-mode: auto | none | smoke | full
```

Normal consumers use `auto`.

### `smoke`

Run the exact canonical Linux-produced runnable JAR on a Windows runner. No source checkout and no second Maven build are required.

This is the normal qualification for an affected Java change when the change does not affect the Windows-sensitive build/toolchain capability.

### `full`

Run both:

1. independent native Windows Maven `verify` using the repository wrapper; and
2. exact Linux-produced artifact smoke where a runnable artifact exists.

This is required for Windows-sensitive toolchain/build/platform impact and release qualification.

### `none`

Explicit escape hatch for cases where Windows qualification is deliberately not useful. Unrelated Java changes do not need this override; they stop before execution automatically.

### `auto`

The preflight maps affected capabilities to a real qualification level:

```text
normal Java impact        -> smoke
Windows-sensitive impact -> full
release qualification    -> full
```

The exact input families that mark `java.windows-full` are consumer-owned configuration. Build/toolchain/Maven-wrapper/workflow/platform-sensitive changes are expected candidates. Ordinary Java source should not automatically pay for full Windows Maven verification unless the project declares it platform-sensitive.

A reviewer/manual workflow can explicitly force `full` when the automatic classification is not conservative enough for a particular change.

## 6. Real evidence boundaries stay; duplicate re-check jobs go

Keep cross-job transfer where it represents a real boundary, especially Linux canonical artifact → Windows smoke.

Do not create a separate hosted Linux job merely to repeat deterministic assertions over evidence already validated by the producer.

Java-output finalization may remain a small permission/side-effect boundary if needed, but must not trigger another Maven build.

## 7. Java-output publication is a side effect

Publication of generated Java artifacts/evidence mutates repository state and stays outside Moon's cacheable producer graph.

`tool.java-project` may own generic preparation/finalization for Java output it actually produces. Generic branch mapping/push mechanics remain in generic repository tooling where already established.

This does **not** make Java the owner of project-family documentation publication.

## 8. Release semantics remain exact but product rules stay product-owned

Release qualification must guarantee:

- exact tagged/source commit execution;
- fresh exact-source Java producer evidence where release policy requires it;
- full Windows qualification;
- immutable artifacts/tags/output according to the owning repository policy.

Product-specific Maven version/tag metadata and failed-tag semantics remain in the real project unless a separate reusable contract is proven.

## 9. Durable timing and hosted-compute evidence are first-class

Record at least:

- preflight duration;
- Linux canonical duration;
- selected Windows mode and Windows duration when used;
- Java-output finalization duration;
- total wall-clock to required evidence;
- hosted jobs/runners actually started;
- unrelated path and proof that Java/Windows work was avoided.

## 10. Engineering documentation stays independent from Java

The event-timing meta repository already proves the intended separation by building its documentation with `tool.eng-docs`, Python and generic repository/Moon tooling without JDK/Maven.

Normal contract:

```text
Java producer
  -> JAR / tests / provenance / Java-derived docs + manifest

meta/docs producer
  -> Markdown / diagrams / planning output

             both may feed
                  |
                  v
           tool.eng-docs assemble
```

A documentation-only project change must not start Java merely because Java implementations exist elsewhere in the project family.

## Ownership boundary

### `tool.git-project`

Owns generic repository mechanics:

- exact base/head affected selection;
- Moon bootstrap/query/materialization primitives;
- generic repository validation/bootstrap;
- generic generated-output publication primitives.

It must not gain Java/Maven semantics.

### `tool.eng-docs`

Owns reusable documentation mechanisms, schemas, producer manifests, document assembly and documentation provenance. It consumes producer output; it does not run Maven/OpenSCAD/embedded producers.

### `tool.java-project`

Primary implementation owner:

- Java policy/config validation;
- shared Java preflight mapping;
- canonical Maven producer lifecycle;
- JDK/Maven setup contract;
- producer/test/provenance evidence;
- selective Windows `none|smoke|full` qualification;
- Java-derived artifacts/documentation where Java tooling is required;
- Java-output finalization where appropriate;
- durable Java timing/result evidence.

### `template.java-project`

Reference consumer:

- proves the thin caller;
- proves unrelated zero-Java behaviour;
- proves `auto` smoke/full selection and explicit override behaviour;
- qualifies Java-output publication and release consumption.

### `2026-010-02.java.event-timing-framework`

Real consumer:

- proves the contract with multi-module/product-specific Java code;
- retains product architecture assertions such as dependency/logging boundaries;
- retains product-specific release metadata where it is genuinely product-owned;
- stops duplicating generic Java lifecycle mechanics.

## Cross-domain equivalence

Where practical, Java, SCAD and future embedded tooling use the same lifecycle vocabulary:

```text
affected/preflight -> execute/materialize -> verify -> finalize/publish -> release
```

The equivalence is conceptual, not mechanical. Shared naming/evidence should make different build systems easier to operate together without hiding real domain differences.

## Explicit non-goals

Migration 006 does not initially:

- replace Maven with Moon;
- introduce a Java build container;
- split every Maven module into a Moon task;
- solve GitHub Actions dependency maintenance;
- redesign event-timing application architecture;
- remove meaningful Windows qualification;
- move project-family engineering-documentation assembly into Java;
- create Java-specific meta/documentation architecture.

## Remaining qualification decisions

Evidence still needs to settle:

1. the exact `java.windows-full` input families for template and real consumer;
2. whether Java-output finalization remains a small separate write-permission job or can be folded into the producer without weakening the boundary;
3. whether the existing generic Moon affected interface is sufficient without `tool.git-project` changes;
4. which Java configuration fields are shared policy versus consumer inputs;
5. realistic latency and hosted-compute targets after duplicate jobs are removed.
