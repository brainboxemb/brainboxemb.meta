# 10 — Baseline measurements

## Purpose

These measurements establish the current Java execution cost before any Migration-006 design is selected. They are not target numbers yet.

The key distinction is the same one learned during SCAD work: **wall-clock latency** and **total hosted compute/resource use** are separate metrics. Parallel jobs can shorten elapsed time while increasing total runner usage, checkout/setup duplication and artifact transport.

## Reference template baseline

Repository: `brainboxemb/template.java-project`

Representative main run: **34827777608** (`tool.java-project v0.2.0` adoption)

GitHub run envelope:

- created: `2026-09-14T09:24:28Z`;
- completed/updated: `2026-09-14T09:25:44Z`;
- elapsed run envelope: about **76 s**.

The first hosted jobs started around `09:24:31Z`; the final publication job completed around `09:25:43Z`, so hosted execution spans about **72 s**.

### Hosted jobs

| Job | Approx. runtime | Purpose |
| --- | ---: | --- |
| `bootstrap-windows` | 16 s | native Windows checkout/bootstrap/tool-pin contract |
| `linux-canonical` | 27 s | checkout, bootstrap, Java setup, Moon canonical build/evidence, artifact + prepared-publication uploads |
| `verify-test-summary` | 6 s | download prepared publication and re-check retained evidence |
| Windows canonical-artifact smoke | 10 s | setup Java, download Linux artifact, run it on Windows |
| Windows compatibility build | 30 s | checkout, Java setup, Maven-wrapper validation, independent Windows `verify`, evidence upload |
| generated-output publication | ~9 s | checkout, download prepared publication, push generated branch |

Normal main execution therefore consumes **six hosted jobs**. Several operate in parallel, so summed runner time is substantially higher than the 72–76 s wall-clock envelope.

### Linux canonical step profile

Within the 27 s Linux job:

- checkout: ~1 s;
- bootstrap: ~2 s;
- exact Java setup: ~2 s;
- Moon canonical task: ~14 s;
- evidence checks/staging/uploads: a few seconds;
- cleanup/post actions: ~2 s.

The canonical producer is not the majority of total cross-platform hosted compute by itself.

## Real downstream baseline

Repository: `brainboxemb/2026-010-02.java.event-timing-framework`

Representative main run: **34828767368** (`tool.java-project v0.2.0` adoption)

GitHub run envelope:

- created: `2026-09-14T09:35:11Z`;
- completed/updated: `2026-09-14T09:36:45Z`;
- elapsed run envelope: about **94 s**.

The workflow defines **10 jobs**. On this ordinary non-release main push, seven performed work and three release-only jobs were skipped:

1. `release-metadata` — executed;
2. `bootstrap-windows` — executed;
3. `linux-canonical` — executed;
4. `verify-evidence` — executed;
5. Windows compatibility build — executed;
6. Windows canonical-artifact smoke — executed;
7. generated-output publication — executed;
8. `publish-release` — skipped;
9. `archive-failed-release` — skipped;
10. `create-release-tag` — skipped.

Measured examples from the run:

| Job | Approx. runtime | Observation |
| --- | ---: | --- |
| `release-metadata` | 4 s | product-owned version/tag validation |
| `bootstrap-windows` | 16 s | duplicates shared-tool/bootstrap validation on Windows |
| `linux-canonical` | 32 s | canonical producer path plus current evidence staging/uploads |
| `verify-evidence` | 7 s | extra runner + artifact download to re-check already-staged evidence |
| Windows compatibility build | 40 s | genuine independent native-Windows Maven correctness lane |
| Windows canonical-artifact smoke | short independent lane | verifies exact Linux-produced runnable artifact on Windows |
| generated-output publication | separate runner | publication requires another checkout + prepared-output download |

The real project therefore demonstrates both valid independent work and likely orchestration overhead. Migration 006 must distinguish the two rather than simply reducing job count.

## Unrelated-change baseline gap

The current Java workflows do not have the newer generic `affected` preflight used by current SCAD production.

The normal path invokes `tool.git-project/moon@v0.2.2` only after:

- a Linux hosted runner has been allocated;
- full-history/blobless checkout has completed;
- shared tooling has been bootstrapped;
- the exact JDK has been configured.

The Windows bootstrap lane also starts independently. As a result, there is currently no measured Java equivalent of the SCAD "README-only, zero runtime/build work" path.

A Migration-006 baseline probe should explicitly measure a documentation-only PR before implementation begins and record:

- which jobs start;
- whether Maven/JDK setup occurs;
- whether Windows work occurs;
- Moon decision/cache behavior;
- wall-clock time;
- total runner time.

## Current transport boundaries

Normal Java production currently crosses multiple artifact boundaries:

1. Linux canonical JAR uploaded for Windows smoke;
2. prepared publication uploaded from Linux;
3. prepared publication downloaded by evidence-verification job;
4. prepared publication downloaded again by publication workflow/job;
5. Windows test evidence uploaded separately.

Some transfers are semantically required — notably Linux→Windows exact-artifact smoke. Others may only exist because orchestration is split across jobs. Migration 006 should quantify payload sizes before removing or retaining those boundaries.

## Initial measurement questions

Before target budgets are set, collect at least:

- one unchanged/docs-only template run;
- one normal affected template run with warm Maven/Moon caches;
- one normal affected template run with cold caches;
- equivalent downstream framework cases;
- release/tag path for the downstream framework;
- Maven cache sizes and transfer times;
- Moon cache/materialization sizes and times;
- prepared-publication artifact sizes;
- Windows compatibility build time versus artifact-smoke time;
- total runner-minutes, not only workflow elapsed time.

## Baseline conclusion

Current performance is not obviously bad because Maven itself is slow. The evidence instead suggests a lifecycle shape with:

- no early unrelated-change stop;
- repeated runner setup/bootstrap;
- one full-history canonical checkout;
- consumer-owned evidence staging and validation;
- multiple cross-job output hand-offs;
- a separate publication runner;
- genuinely independent Windows compatibility work mixed with avoidable orchestration overhead.

That is sufficient evidence to justify preparing Migration 006, but not yet sufficient to choose its target architecture.
