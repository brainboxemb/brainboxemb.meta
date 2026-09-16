# Migration 006 — simplify the Java execution architecture

Status: **proposed / inactive**

Working draft: [#65](https://github.com/brainboxemb/brainboxemb.meta/pull/65)

Predecessor: [Migration 005](../005-scad-execution-architecture/README.md) — active final library alignment.

## Current status

Migration 006 is intentionally being elaborated on `main` while Migration 005 finishes its final SCAD library rollout. This parallel work is planning/documentation only: it does **not** authorize Java owner-repository implementation yet.

The current Java chain is:

```text
tool.git-project
  generic repository / Moon / affected mechanics
        ↓
tool.java-project
  Java build, test, toolchain and reusable workflow semantics
        ↓
template.java-project
  reference consumer
        ↓
2026-010-02.java.event-timing-framework
  real downstream consumer
```

Project-family planning/architecture documentation is intentionally **not** part of that Java chain. It follows the generic model in [Project families, coordination and engineering documentation](../../docs/working-model/project-families-and-documentation.md): the meta repository owns project-wide engineering meaning, `tool.eng-docs` owns reusable documentation mechanisms/assembly, and implementation domains produce only their own derived assets/evidence.

## Current evidence

The existing Java tooling already has a strong domain baseline: exact Temurin/Maven/Maven-Wrapper versions, a canonical Linux Maven producer, persistent execution/test evidence, reusable Windows compatibility and real downstream releases.

The main problem is repository-level orchestration. The template and downstream project still own substantial duplicated lifecycle logic: checkout/bootstrap, Java setup, Moon invocation, evidence staging, artifact hand-off, Windows coordination and Java-output publication.

Current repository inspection confirms:

- `template.java-project` keeps its normal Java lifecycle in one consumer-owned workflow of roughly 8.4 kB, including Windows bootstrap, Linux canonical execution, publication staging, evidence re-check, Windows compatibility and publication;
- `2026-010-02.java.event-timing-framework` repeats and expands that pattern in a roughly 19.4 kB workflow with additional product release semantics;
- consumers currently use released `tool.java-project v0.2.0` / exact source `9c147850adb9c0c270d852166feae5f08f56c2d6`;
- there is no early generic unrelated-change gate before JDK/Maven/Windows work;
- several hosted-job/artifact boundaries exist to re-check or republish evidence rather than because a Java correctness boundary requires them;
- `2026-010-01.meta.event-timing-software` already builds engineering documentation independently with `tool.eng-docs`, Python and generic Moon/repository tooling, without JDK/Maven.

Earlier representative runs suggested roughly 72–76 seconds wall-clock for the template and roughly 94 seconds for the real downstream on ordinary main execution. Those measurements remain research inputs and must be refreshed at activation.

## Preferred direction

The working direction is now documented more concretely in:

- [05 — Draft target architecture](05-target-architecture.md);
- [06 — Draft implementation and qualification plan](06-implementation-plan.md).

The key choices are:

1. keep **Maven as Java build/test authority**;
2. add an **early generic exact base→head affected preflight** before JDK/Maven/Windows allocation;
3. move generic Java lifecycle orchestration into **`tool.java-project`** and leave consumers thin;
4. retain the **native pinned JDK/Maven model** unless measurements justify a container;
5. keep **independent Windows compatibility**, but make cadence an explicit policy to qualify rather than automatically running it on every main push;
6. remove duplicate evidence-verification/artifact boundaries that do not represent a real isolation boundary;
7. keep **Java-produced** output publication as a repository side effect outside Moon's cacheable task graph;
8. keep project-family planning/architecture/document assembly **independent from Java**, using the generic meta + `tool.eng-docs` model;
9. retain product-specific release/version metadata in the real project unless a genuinely generic contract is separately proven;
10. record durable phase timing and hosted-job evidence before and after the migration.

## Explicitly parked research

**Moon fine-grained Java/Maven incrementality is not an activation blocker.** The first migration remains conservative: Maven owns build/test semantics; Moon/tool.git-project supply affected selection and orchestration/materialization support.

GitHub Actions dependency-update automation also stays out of this migration and belongs to Migration 007.

Generic engineering-documentation improvements stay outside Migration 006 unless the Java rollout exposes a real ownership/correctness blocker. The intended reusable top-level structure is technology-neutral so a later embedded domain can join the same meta/docs model without inheriting Java concepts.

## Activation gate

When Migration 005 closes:

1. refresh exact repository revisions and current successful baseline runs;
2. confirm branch/merge policy where it affects the Windows cadence decision;
3. review the target architecture and implementation plan against that current state;
4. confirm the independent engineering-documentation path remains outside Java;
5. explicitly mark Migration 006 active in `STATUS.md` and `migrations/README.md` before any Java owner implementation.

Draft PR #65 remains research input; `main` is the status/design authority.
