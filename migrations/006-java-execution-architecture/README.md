# Migration 006 — simplify the Java execution architecture

## Why this migration exists

Current Java repositories already have a reproducible Maven/JDK baseline, but they still duplicate too much repository-level orchestration: checkout/bootstrap, Java setup, Moon invocation, evidence staging, Windows coordination and Java-output publication. That duplication spends hosted compute on unrelated changes and makes the intended ownership boundary harder to see.

Migration 006 exists to move the **generic Java execution lifecycle** into `tool.java-project`, leave consumers as thin callers, and prove the contract first in `template.java-project` and then in the real event-timing framework.

Use this migration when deciding what belongs in shared Java execution tooling, which repository is next in the rollout, or what evidence is required before the shared contract can advance.

Status: **active — owner implementation merged and exact-main qualified; owner release is next**

Working/research draft: [#65](https://github.com/brainboxemb/brainboxemb.meta/pull/65)

Owner implementation: [`tool.java-project` #26](https://github.com/brainboxemb/tool.java-project/pull/26) — merged to main.

Predecessor: [Migration 005](../005-scad-execution-architecture/README.md) — complete on the final `bld` / `vrf` namespace baseline.

## Cross-domain publication baseline

Migration 006 exposed a useful cross-domain naming inconsistency while Migration 005 was closing: Java already used technical `bld`, while SCAD publication still used `build` / `verification` even though current-generation SCAD workspace roots were already `dsg` / `bld` / `vrf`.

That inconsistency is now resolved. The durable portfolio convention is defined in [Generated output and publication](../../docs/working-model/generated-output.md): human-facing names stay readable, while shared technical path/branch identities use canonical stable identifiers such as `dsg`, `bld`, `vrf` and `docs` where those concepts apply.

Migration 006 must use that stable convention rather than invent Java-local synonyms. Java currently has a Build publication family under `bld`; it should only introduce another publication family such as `vrf` if Java actually has an independently published Verification family, not merely for symmetry.

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

The owner implementation is merged in `tool.java-project` main as:

```text
c7ed36ceaf21874b908a1dd01fa54bc60d420d9c
```

Exact-main owner evidence is green for both the affected-policy test and the full Java toolchain self-test.

The qualified owner contract includes:

- released generic affected authority through `tool.git-project v0.2.8`;
- one exact base→head affected query rather than duplicate Java/Windows policy queries;
- unrelated impact stopping before JDK/Maven/Windows allocation;
- exact-diff policy evidence for unrelated → `none`, normal Java → `smoke`, and build/toolchain-sensitive → `full`;
- canonical Linux Maven execution;
- exact Linux-produced runnable-JAR smoke on Windows;
- full native Windows Maven compatibility when required;
- exact source identity carried through preflight, Linux canonical execution, full Windows execution and provenance;
- Java generated-output publication on canonical technical `bld` naming;
- generic `tool.git-project` lifecycle refs aligned to v0.2.8;
- engineering-documentation assembly kept outside Java ownership.

Baseline measurements captured during investigation were roughly 72–76 seconds wall-clock for the template and roughly 94 seconds for the real downstream ordinary-main path. They remain comparison inputs and are refreshed during canary qualification.

## Selected direction

The detailed design and rollout are in:

- [05 — Target architecture](05-target-architecture.md);
- [06 — Implementation and qualification plan](06-implementation-plan.md).

The active choices are:

1. keep **Maven as Java build/test authority**;
2. use an **early exact base→head affected preflight** before JDK/Maven/Windows allocation;
3. keep generic Java lifecycle orchestration in **`tool.java-project`**;
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

The owner implementation phase is complete and qualified on `tool.java-project/main`. Migration 005 is closed again, so the previous release/consumer gate is removed.

The next sequence is:

1. prepare and release the already-qualified `tool.java-project` owner revision;
2. canary the released contract in `template.java-project`;
3. prove unrelated zero-Java behaviour plus `auto` smoke/full selection using a real thin production caller;
4. refine Windows policy only if canary evidence exposes a real correctness or cost problem;
5. roll the released baseline into `2026-010-02.java.event-timing-framework` and perform real downstream release qualification;
6. close Migration 006 only after the owner, template and real downstream evidence all agree.

`main` in `brainboxemb.meta` is the migration status/design authority; draft PR #65 remains research history/input rather than a competing source of truth.
