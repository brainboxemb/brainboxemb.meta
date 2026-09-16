# Migration 006 — draft implementation and qualification plan

Status: **proposed / inactive planning authority**

This plan is intentionally prepared while Migration 005 library CI completes. It does not activate Java owner-repository implementation yet.

The target architecture is defined in [05-target-architecture.md](05-target-architecture.md).
The generic project-family/documentation boundary is defined in [Project families, coordination and engineering documentation](../../docs/working-model/project-families-and-documentation.md).

## Working baseline

Current public chain:

```text
tool.git-project
      ↓
tool.java-project
      ↓
template.java-project
      ↓
2026-010-02.java.event-timing-framework
```

Project-family planning/architecture documentation remains a parallel generic capability owned by the meta repository plus `tool.eng-docs`; it is not part of this Java implementation chain.

Current consumer evidence shows the main inefficiency is orchestration duplication rather than Maven itself:

- `template.java-project` has a large consumer-owned workflow with separate Windows bootstrap, Linux canonical producer, artifact staging, Windows compatibility, evidence re-check and Java-output publication jobs;
- `2026-010-02.java.event-timing-framework` repeats that structure and adds product-specific release metadata/tag/release jobs;
- Java setup/Windows work starts before a generic unrelated-change decision exists;
- exact Linux artifacts are legitimately transferred to Windows, but other artifact/job boundaries mostly exist to re-check or republish already-produced Java evidence.

The current released Java tooling reference used by consumers is `tool.java-project v0.2.0` / exact source `9c147850adb9c0c270d852166feae5f08f56c2d6`.

The event-timing meta repository already builds its engineering documentation independently with `tool.eng-docs`, Python and generic Moon/repository tooling, without JDK/Maven. Migration 006 must preserve that separation.

## Step 0 — activate only after Migration 005 closes

Owner: `brainboxemb.meta`

Before Java code changes:

1. re-read current `main` of all four Java-chain repositories;
2. capture current successful template and downstream workflow runs;
3. record job count, wall-clock, Windows usage and artifact boundaries;
4. confirm current branch-protection/merge model where it affects Windows cadence;
5. confirm the current independent meta/engineering-documentation path remains outside Java;
6. mark Migration 006 active explicitly in `STATUS.md` and the migration index.

Exit evidence:
- dated baseline table;
- exact repository/tool revisions;
- documented Java-versus-engineering-docs ownership boundary;
- activation commit in meta.

## Step 1 — shared Java execution contract

Owner: `tool.java-project`

Goal: create one shared Java production contract without yet changing consumers or absorbing generic engineering documentation.

Implement/rework reusable owner workflows so `tool.java-project` owns:

- exact event/source inputs;
- cheap affected preflight contract;
- native JDK/Maven setup;
- one canonical Maven producer;
- producer/test/provenance evidence;
- timing/result evidence;
- Windows selection policy and exact Linux-artifact hand-off;
- Java-derived artifact/evidence finalization where appropriate;
- Javadoc or other Java-derived documentation only when Java tooling is genuinely required.

Keep Maven as build/test authority.

Do **not** yet:
- move product-specific release metadata into the tool;
- introduce module-level Moon tasks;
- introduce a Java container;
- change consumer workflows;
- move SDP/SIP/SVP/architecture assembly or generic documentation publication into Java tooling.

Required owner tests/evidence:

1. unit/static tests for workflow/config contract;
2. self-test fixture proving affected Linux execution;
3. unrelated fixture proving stop before JDK/Maven/Windows;
4. Windows fixture proving independent Maven compatibility and exact Linux artifact smoke;
5. provenance fixture proving exact source/tool identity;
6. Java-output finalization fixture proving output can be finalized without a duplicate Maven run;
7. durable phase timing/job-selection evidence;
8. ownership test/documentation proving generic engineering-documentation assembly is not required by the Java lifecycle.

If the generic affected interface in `tool.git-project` is insufficient, make only the smallest owner-correct extension there and release it before continuing.

## Step 2 — release the shared Java owner revision

Owner: `tool.java-project`

After owner tests are green:

1. merge exact qualified owner source;
2. run owner main qualification;
3. create the next immutable semantic tool release;
4. verify the released reusable workflow ref resolves to the exact qualified source;
5. record release/source/run evidence in Migration 006.

Consumer branches must not pin owner `main` or an unreleased feature branch as the final migration state.

## Step 3 — reference template canary

Owner: `template.java-project`

Replace the current consumer-heavy Java workflow with the smallest viable caller/configuration for the released shared Java lifecycle.

Preserve only template-specific assertions/configuration that genuinely belong to the reference consumer.

Qualification scenarios:

### A. affected PR
- one generic affected decision;
- one Linux canonical Maven producer;
- correct producer/test/provenance evidence;
- selected Windows qualification executes according to policy;
- exact Linux-produced artifact is smoked on Windows;
- Java-output finalization/publication is correct;
- no duplicate Linux Maven/evidence-verification job.

### B. README-only PR
- source/base + affected decision only;
- no JDK setup;
- no Maven execution;
- no Windows runner;
- no Java-output publication;
- compact evidence records `affected=false`.

### C. merged main
- exact merged source provenance;
- normal Java-output publication correct;
- Windows behaviour matches the selected cadence policy.

### D. release/reference snapshot
- exact release source;
- no unsafe reuse of an earlier producer when exact source is required;
- required Windows qualification;
- immutable Java release evidence according to template policy.

Measure against the baseline:
- workflow file size/consumer-owned lifecycle reduction;
- hosted jobs started;
- wall-clock;
- total hosted runner time;
- unaffected path latency.

Do not continue to the real project until the template demonstrates the owner boundary cleanly.

## Step 4 — decide Windows cadence from template evidence

Owners: `brainboxemb.meta` decision, implementation in `tool.java-project`

Use template evidence to select and document the shared default.

Candidate default:

```text
pull_request affected -> Windows required
release               -> Windows required
ordinary main          -> Windows optional/skip when qualified PR evidence is sufficient
manual                 -> force option available
```

Reject that candidate if current merge/protection behaviour makes it impossible to associate sufficiently strong Windows evidence with the source that reaches main.

Record the decision and rationale before the real-project rollout.

## Step 5 — real event-timing framework rollout

Owner: `2026-010-02.java.event-timing-framework`

Move generic Java orchestration to the released shared owner workflow while retaining product-owned assertions:

- Maven version/release metadata;
- application/framework artifact naming;
- logging dependency-boundary checks;
- product-specific release/tag failure semantics where still necessary;
- domain-specific smoke output.

Keep project-family planning/architecture documentation in `2026-010-01.meta.event-timing-software`; Java-produced documentation/evidence may be exposed through manifests for later generic document assembly but must not make Maven the documentation assembler.

Qualification scenarios:

1. affected PR with multi-module canonical producer;
2. README-only unrelated PR with zero Java/Windows work;
3. exact merged-main Java-output publication;
4. release candidate/tag path built from exact release source;
5. independent Windows Maven compatibility;
6. exact Linux-produced app artifact smoke on Windows;
7. generated Java evidence/publication provenance;
8. failure path proving incomplete releases do not leave a false successful release state;
9. documentation-boundary check proving meta/engineering-docs CI remains independently executable without Java.

The real-project workflow should contain product orchestration, not a second copy of generic Java lifecycle mechanics.

## Step 6 — release and closeout

Owners: downstream repository + `brainboxemb.meta`

After the final real-project state is qualified:

1. publish the next immutable project release when the repository's release policy requires it;
2. verify exact release source, assets and provenance;
3. compare final performance/resource evidence with baseline;
4. update durable Java execution architecture documentation outside the migration folder;
5. confirm the generic project-family/engineering-documentation model still applies unchanged to Java and remains reusable by future embedded/CAD domains;
6. move Migration 006 to complete only when template and real downstream are both on released shared tooling.

## Required evidence matrix

| Scenario | Preflight | Linux Maven | Windows | Java-output publication | Exact source |
| --- | --- | --- | --- | --- | --- |
| unrelated PR | yes | no | no | no | yes |
| affected PR | yes | yes, one canonical | policy-required | PR output | yes |
| normal main | yes | yes if affected | selected policy | prod output | yes |
| release | release preflight | yes, fresh exact source | yes | immutable release | yes |

Additional invariants:

- Maven remains the build/test authority;
- no duplicate canonical Linux producer in one workflow path;
- Windows consumes the exact Linux artifact for smoke while retaining independent Windows Maven compatibility;
- Java-output publication does not trigger another Maven build;
- generic engineering-documentation assembly does not require the Java lifecycle;
- Java-derived documentation such as Javadoc is a producer asset, not the project-documentation authority;
- durable timing evidence survives generated-output publication;
- released reusable workflow refs and exact committed tool identity remain aligned.

## Blocker classification during execution

New findings are classified as:

- **Migration-006 blocker** — violates correctness/ownership or prevents template/real-project qualification;
- **follow-up migration** — useful cross-project improvement not required for this Java architecture;
- **owner backlog** — local cleanup/performance issue.

Only blockers extend the active migration. In particular, GitHub Actions dependency-update automation belongs to Migration 007 and must not expand Migration 006. Generic engineering-documentation improvements also stay outside Migration 006 unless the Java work exposes an actual ownership/correctness blocker.
