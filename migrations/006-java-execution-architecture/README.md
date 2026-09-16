# Migration 006 — simplify the Java execution architecture

## Why this migration exists

Current Java repositories already have a reproducible Maven/JDK baseline, but they still duplicate too much repository-level orchestration: checkout/bootstrap, Java setup, Moon invocation, evidence staging, Windows coordination and Java-output publication. That duplication spends hosted compute on unrelated changes and makes the intended ownership boundary harder to see.

Migration 006 exists to move the **generic Java execution lifecycle** into `tool.java-project`, leave consumers as thin callers, and prove the contract first in `template.java-project` and then in the real event-timing framework.

Use this migration when deciding what belongs in shared Java execution tooling, which repository is next in the rollout, or what evidence is required before the shared contract can advance.

Status: **active owner implementation — running in parallel with final Migration-005 consumer requalification; Java release/consumer rollout remains gated**

Working/research draft: [#65](https://github.com/brainboxemb/brainboxemb.meta/pull/65)

Current owner work: [`tool.java-project` #26](https://github.com/brainboxemb/tool.java-project/pull/26)

Predecessor: [Migration 005](../005-scad-execution-architecture/README.md) — reopened only for generated-output namespace normalization and consumer requalification.

## Parallel dependency on Migration 005

Migration 006 exposed a cross-domain naming inconsistency: Java already publishes Build output as `bld`, while the Migration-005 SCAD branch contract used `build`/`verification` even though current-generation SCAD workspace roots are already `dsg`/`bld`/`vrf`.

The durable portfolio convention is defined in [Generated output and publication](../../docs/working-model/generated-output.md): human-facing names stay readable, while shared technical path/branch identities use canonical compact identifiers such as `bld` and `vrf`.

Migration 005 now owns requalification of that SCAD namespace baseline. This does **not** block owner implementation in `tool.java-project`: the Java owner may continue designing, implementing and qualifying its own reusable contract in parallel. What remains gated is the **Java owner release and consumer rollout** into `template.java-project` and `2026-010-02.java.event-timing-framework` until Migration 005 closes again.

This keeps the two work tracks independent where they genuinely are independent, while still preventing Java consumers from being rolled out against an unsettled cross-domain publication contract.

## Scope

The active Java implementation chain is:

```text
tool.git-project
  generic repository / Moon / affected mechanics
        ↓
tool.java-project
  Java build, test, selective Windows qualification,
  Java evidence/artifacts and reusable workflow semantics
        ↓
template.java-project
  reference consumer
        ↓
2026-010-02.java.event-timing-framework
  real downstream consumer
```

Project-family planning/architecture documentation is intentionally **not** part of that Java chain. It follows the generic model in [Project families, coordination and engineering documentation](../../docs/working-model/project-families-and-documentation.md): meta/coordination owns cross-repository engineering meaning, `tool.eng-docs` owns reusable documentation mechanisms/assembly, and implementation domains produce only their own derived assets/evidence.

## Current evidence

The existing Java tooling already provides:

- exact Temurin, Maven and Maven-Wrapper baselines;
- one canonical Linux Maven producer;
- persistent execution/test/provenance evidence;
- reusable Windows compatibility;
- real downstream release evidence.

The current inefficiency is orchestration rather than Maven itself:

- `template.java-project` has a consumer-owned lifecycle with Windows bootstrap, Linux canonical execution, publication staging, evidence re-check, Windows compatibility and publication;
- `2026-010-02.java.event-timing-framework` repeats and expands that structure with product release semantics;
- Java/Windows work starts before a generic unrelated-change decision exists;
- several hosted-job/artifact boundaries re-check or republish evidence rather than represent a required Java correctness boundary;
- the event-timing meta repository already builds engineering documentation independently with `tool.eng-docs`, Python and generic Moon/repository tooling, without JDK/Maven.

Baseline measurements captured during investigation were roughly 72–76 seconds wall-clock for the template and roughly 94 seconds for the real downstream ordinary-main path. They remain comparison inputs and are refreshed during canary qualification.

## Selected direction

The detailed design and rollout are in:

- [05 — Target architecture](05-target-architecture.md);
- [06 — Implementation and qualification plan](06-implementation-plan.md).

The active choices are:

1. keep **Maven as Java build/test authority**;
2. add an **early exact base→head affected preflight** before JDK/Maven/Windows allocation;
3. move generic Java lifecycle orchestration into **`tool.java-project`**;
4. retain the **native pinned JDK/Maven model**;
5. make Windows qualification **selective** rather than always paying for a full Windows Maven build;
6. remove duplicate evidence/artifact boundaries that do not represent a real isolation boundary;
7. keep Java-produced output publication outside the cacheable producer graph;
8. keep project-family planning/architecture/document assembly independent from Java;
9. retain product-specific release/version semantics in the real project unless a generic contract is separately proven;
10. retain durable wall-clock and hosted-compute evidence;
11. align shared technical publication namespaces to the durable `brainboxemb.meta` convention rather than defining Java-local synonyms.

## Selective Windows contract

Consumers expose one policy input:

```text
windows-mode: auto | none | smoke | full
```

Normal callers use `auto`.

For an affected Java change:

```text
normal Java impact        -> smoke
Windows-sensitive impact -> full
release qualification    -> full
```

`smoke` means: run the **exact Linux-produced runnable JAR on Windows**, without a second Maven build.

`full` means: run an **independent Windows Maven `verify`** and, where configured, also smoke the exact Linux-produced JAR.

`none`, `smoke` and `full` are explicit overrides for exceptional/manual qualification. If Java is not affected, the lifecycle stops before Java execution and no Windows runner starts.

The automatic distinction is driven by the same affected/capability model rather than separate ad-hoc GitHub `paths:` logic.

## Cross-domain consistency rule

Java should use the same lifecycle vocabulary and technical namespace conventions as SCAD and later implementation domains where that helps maintainability:

```text
affected/preflight -> execute/materialize -> verify -> finalize/publish -> release
```

Equivalent naming does **not** require equivalent build mechanics. Maven remains Maven; SCAD may use OpenSCAD/SCons; a future embedded domain may use its own compiler/build system. Shared concepts stay aligned where practical so project families remain understandable across technologies.

## Explicitly parked work

- fine-grained Moon/Maven module incrementality is not required for this migration;
- a Java build container is not introduced without evidence that it solves a real problem;
- GitHub Actions dependency-update automation belongs to Migration 007;
- generic engineering-documentation improvements stay outside Migration 006 unless Java exposes a real ownership/correctness blocker.

## Current implementation position

Step 1 is active in `tool.java-project` draft PR #26 and may continue while Migration 005 performs its final SCAD consumer requalification.

Current owner evidence includes:

- one released generic affected authority via `tool.git-project v0.2.8`;
- exact-diff policy evidence for unrelated -> `none`, normal Java -> `smoke`, and build/toolchain-sensitive -> `full`;
- canonical Linux Maven execution still green;
- full native Windows Maven compatibility still green;
- exact Linux-produced runnable-JAR smoke on Windows still green;
- Java generated-output publication remains on the canonical technical `bld` namespace.

Owner implementation and qualification should continue to completion. After Migration 005 closes again, the remaining sequence is: finish/merge exact owner qualification if not already complete, release the qualified `tool.java-project` revision, then canary `template.java-project`, then roll into `2026-010-02.java.event-timing-framework`.

`main` in `brainboxemb.meta` is the migration status/design authority; draft PR #65 remains research history/input rather than a competing source of truth.
