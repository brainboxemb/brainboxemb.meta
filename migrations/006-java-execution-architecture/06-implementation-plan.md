# Migration 006 — implementation and qualification plan

## Why this document exists

The target architecture defines the desired end state, but Migration 006 spans several repositories and cannot safely be changed everywhere at once. This document defines **the owner order, qualification gates and evidence needed to advance from one repository to the next**.

Use it to decide what work is allowed now, what must be released before a consumer changes, and what evidence closes each step. It is not a substitute for implementation detail in the owner repository.

Status: **active planning authority**

Target architecture: [05 — Target architecture](05-target-architecture.md).
Generic project-family/documentation boundary: [Project families, coordination and engineering documentation](../../docs/working-model/project-families-and-documentation.md).

## Working chain

```text
tool.git-project
      ↓
tool.java-project
      ↓
template.java-project
      ↓
2026-010-02.java.event-timing-framework
```

Project-family planning/architecture documentation is a parallel generic capability owned by the meta repository plus `tool.eng-docs`; it is not part of this Java implementation chain.

Current released Java baseline before this migration is `tool.java-project v0.2.0` / exact source `9c147850adb9c0c270d852166feae5f08f56c2d6`.

## Step 0 — activate and freeze the boundary

Owner: `brainboxemb.meta`

**Status: complete.**

Completed on 2026-09-16:

- Migration 005 closed after final reusable-library v0.14.8 releases;
- current Java owner/template/real-consumer baseline re-read;
- generic project-family/meta/documentation boundary separated from Java;
- cross-domain lifecycle-equivalence rule recorded;
- target architecture and owner rollout plan made authoritative on `main`;
- Migration 006 marked active before Java owner implementation.

Implementation may now proceed in `tool.java-project` only.

## Step 1 — shared Java execution contract

Owner: `tool.java-project`

**Status: active — draft PR #26.**

Goal: create one shared Java production contract without changing consumers yet.

Implement/rework reusable owner workflows so `tool.java-project` owns:

- exact source/base preflight inputs;
- generic affected classification through `tool.git-project`;
- native JDK/Maven setup;
- one canonical Linux Maven producer;
- producer/test/provenance evidence;
- durable timing/job-selection evidence;
- selective Windows qualification;
- Java-derived output finalization without a duplicate Maven build.

### Windows policy

One caller input:

```text
windows-mode: auto | none | smoke | full
```

Normal caller: `auto`.

```text
Java unrelated           -> no Java/Windows execution
normal Java impact       -> smoke
Windows-sensitive impact -> full
release                  -> full
```

`smoke` runs only the exact Linux-produced runnable JAR on Windows.

`full` runs independent Windows Maven `verify` plus exact Linux-artifact smoke where configured.

Explicit `none|smoke|full` values remain manual/exception overrides.

### Step-1 evidence

Required before release:

1. workflow/config static validation;
2. affected owner fixture proves one Linux canonical producer;
3. unrelated probe proves stop before JDK/Maven/Windows;
4. smoke path proves no independent Windows Maven job is allocated;
5. full path proves independent Windows Maven compatibility plus exact Linux artifact smoke;
6. exact source/tool provenance remains correct;
7. Java-output finalization does not rebuild Maven output;
8. durable timing/job-selection evidence identifies the selected path;
9. generic engineering-documentation assembly is not required by the Java lifecycle.

If `tool.git-project` affected mechanics are insufficient, change that owner only by the smallest necessary released extension. Do not duplicate change detection in Java.

## Step 2 — release the shared Java owner revision

Owner: `tool.java-project`

After Step 1 evidence is green:

1. merge the exact qualified owner source;
2. run exact-main owner qualification;
3. perform an unrelated-change probe on the merged owner contract where needed to prove zero-Java behaviour;
4. create the next immutable semantic tool release;
5. verify the released reusable workflow resolves to the exact qualified source;
6. record source/run/release evidence in this migration.

Consumers must not end on owner `main` or a feature branch.

## Step 3 — reference template canary

Owner: `template.java-project`

Replace consumer-owned Java orchestration with the smallest viable caller/configuration for the released shared lifecycle.

The template should own the **impact declaration**, not duplicate lifecycle implementation. At minimum it will expose:

- `java.canonical` — changes that require Java execution;
- `java.windows-full` — the narrower impact family that escalates `auto` from smoke to full Windows Maven qualification.

Do not make `java.windows-full` depend on `java.canonical` in a way that makes every normal Java source change escalate to full.

### A. normal affected Java PR

- one affected/preflight decision;
- one canonical Linux Maven producer;
- `auto` resolves to `smoke` when only normal Java impact is present;
- exact Linux artifact runs on Windows;
- no independent Windows Maven build;
- Java-output publication/finalization correct.

### B. Windows-sensitive affected PR

- `java.windows-full` affected;
- `auto` resolves to `full`;
- independent Windows Maven `verify` runs;
- exact Linux-produced artifact also runs on Windows where configured.

### C. README-only PR

- affected preflight only;
- no JDK;
- no Maven;
- no Windows runner;
- no Java-output publication.

### D. explicit override

Prove at least one deliberate `full` override path so a reviewer/manual run can request stronger evidence than automatic classification.

### E. merged main and release

- exact merged-source provenance;
- normal Java-output publication correct;
- release qualification forces full Windows;
- immutable release evidence uses exact release source.

Record before/after:

- consumer workflow size;
- hosted jobs/runners started;
- wall-clock;
- total hosted runner time;
- unrelated-path latency.

Do not continue to the real project until the template demonstrates the owner boundary cleanly.

## Step 4 — lock the Windows impact policy

Owners: `brainboxemb.meta` decision; implementation in `tool.java-project` / consumer configuration.

Use template evidence to finalize:

- which input families require `java.windows-full`;
- whether `smoke` remains the normal affected-Java default;
- whether any normal-main path needs full Windows beyond release/platform-sensitive impact;
- how explicit `full` is exposed for reviewer/manual qualification.

The decision must be based on observed runner cost and failure coverage, not on a blanket platform matrix convention.

## Step 5 — real event-timing framework rollout

Owner: `2026-010-02.java.event-timing-framework`

Move generic Java orchestration to the released shared workflow while retaining product-owned behaviour:

- Maven/version/release metadata;
- application/framework artifact naming;
- logging/dependency-boundary assertions;
- product-specific release/tag failure semantics where necessary;
- domain-specific smoke output.

Keep project-family planning/architecture documentation in `2026-010-01.meta.event-timing-software`.

Qualification scenarios:

1. normal affected multi-module PR -> Linux + Windows smoke;
2. Windows-sensitive PR -> Linux + full Windows;
3. README-only PR -> zero Java/Windows;
4. explicit full override;
5. exact merged-main publication;
6. exact release path with full Windows;
7. exact Linux-produced app artifact smoke on Windows;
8. generated Java evidence/publication provenance;
9. failure path proving incomplete releases cannot appear successful;
10. meta/engineering-docs CI remains independently executable without Java.

## Step 6 — release and closeout

Owners: downstream repository + `brainboxemb.meta`

After the real-project state is qualified:

1. publish the required immutable downstream release;
2. verify exact source, assets and provenance;
3. compare final latency/hosted-compute evidence with baseline;
4. move durable Java execution architecture outside the migration folder;
5. confirm the generic project-family/documentation model still applies unchanged;
6. mark Migration 006 complete only when template and real downstream both consume released shared tooling.

## Required evidence matrix

| Scenario | Preflight | Linux Maven | Windows smoke | Windows Maven | Publication | Exact source |
| --- | --- | --- | --- | --- | --- | --- |
| unrelated PR | yes | no | no | no | no | yes |
| normal Java PR / auto | yes | one canonical | yes | no | PR output | yes |
| Windows-sensitive PR / auto | yes | one canonical | yes | yes | PR output | yes |
| explicit full | yes | one canonical | yes | yes | context-specific | yes |
| release | release preflight | fresh exact source | yes | yes | immutable | yes |

Additional invariants:

- Maven remains build/test authority;
- no duplicate canonical Linux producer;
- smoke always consumes the exact Linux-produced artifact;
- full Windows remains independent native Maven qualification;
- Java-output publication never triggers another Maven build;
- generic engineering-documentation assembly never requires Java execution;
- durable timing/job-selection evidence survives publication;
- released workflow identity and exact committed tool identity remain aligned.

## Blocker classification

New findings are classified as:

- **Migration-006 blocker** — correctness/ownership problem preventing owner/template/real-consumer qualification;
- **follow-up migration** — useful cross-project improvement not required for this Java architecture;
- **owner backlog** — local cleanup/performance work.

Only blockers extend Migration 006. GitHub Actions dependency maintenance remains Migration 007.
