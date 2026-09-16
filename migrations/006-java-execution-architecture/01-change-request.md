# 01 — Change request

## Status

**Proposed / inactive.** This document defines the problem to investigate. It does not authorize implementation while Migration 005 is active.

## Problem statement

The current Java project generation has strong Java-domain tooling but weak repository-level lifecycle ownership.

`tool.java-project` owns canonical Maven execution, toolchain validation, evidence and reusable Windows compatibility, yet consumers still reconstruct a large part of the production lifecycle themselves. The reference template and real event-timing framework both contain substantial GitHub Actions orchestration for checkout/bootstrap, JDK setup, Moon, evidence staging, cross-job artifact hand-off and generated-output publication.

This creates four concerns:

1. **Ownership duplication** — generic/shared lifecycle mechanics live in consumer repositories.
2. **Unrelated-change cost** — there is no current generic affected preflight that can finish before JDK/Maven and Windows work.
3. **Resource multiplication** — normal verification is spread across several hosted jobs, including jobs whose only purpose is to move or re-check already-produced evidence.
4. **Policy drift** — consumers still combine older `tool.git-project/moon@v0.2.2` calls and exact reusable-workflow SHAs while the shared repository tooling has evolved further.

## Goals

Migration 006 should determine and, if activated, implement a Java-specific current-generation execution model that:

- keeps Java build/test semantics in `tool.java-project`;
- keeps domain-neutral affected/Moon/publication mechanics in `tool.git-project`;
- makes `template.java-project` a thin reference consumer rather than a second workflow owner;
- proves the model on `2026-010-02.java.event-timing-framework`;
- stops unrelated changes before expensive Java/Windows work when correctness allows;
- uses exact source/base identity and reproducible Java/Maven versions;
- retains Linux canonical producer evidence and meaningful independent Windows compatibility evidence;
- runs Windows checks at an intentional cadence instead of assuming every produced JAR needs to be tested on Windows on every push;
- avoids duplicate artifact/job boundaries when they do not represent a real isolation or hand-off requirement;
- gives generated output durable current-run timing/materialization/provenance navigation;
- defines an explicit release contract for the Java reference consumer and downstream projects;
- measures both wall-clock feedback and total hosted compute/resource use.

## Non-goals

The proposal does **not** assume:

- that Java needs a Docker runtime merely because SCAD has one;
- that Linux and Windows verification should be collapsed into one runner;
- that every JAR must be re-tested on Windows for every `main` push;
- that the real event-timing product should move its product-specific release/version semantics into generic tooling;
- that Moon must become the Java build engine — Maven remains the Java build/test authority;
- that Moon incremental-build behavior is already understood or selected as part of the target architecture;
- that every SCAD capability name or cache strategy maps directly to Java;
- that current successful release semantics may be removed just to reduce workflow size.

## Architecture questions that must be answered

1. What are the real source-derived Java capabilities?
2. Is Windows compatibility a source-derived capability, an independent verification lane, or both?
3. Which current jobs exist only because the consumer orchestrates staging/verification/publication itself?
4. Can one `tool.git-project` affected query safely classify Java-relevant changes before JDK setup?
5. How much Git history does Moon actually need, and can the shallow exact-base pattern from current repository tooling replace `fetch-depth: 0`?
6. Which current Java outputs are reusable source-derived data and which are current-run/publication context?
7. Should normal production keep Linux build/evidence/publication on one hosted runner while retaining Windows separately?
8. Which workflow references should be semantic release refs and which identities must remain exact gitlinks/commits?
9. Is pinned `actions/setup-java` plus Maven Wrapper sufficient as the immutable runtime contract?
10. What release/publication responsibilities should become shared and what must remain product-owned?
11. Which Windows checks belong on every affected push, which are better PR-only qualification gates, and which should also run for release candidates/tags? In particular, testing every produced JAR on Windows on every `main` push should require explicit evidence that the cost is justified.
12. How does Moon incremental execution actually behave for Java/Maven projects: what input/output boundaries, dependency graph and cache/materialization semantics are needed, and does it add value beyond Maven's own incremental/local-repository behavior?

## Parked research note — Moon incremental builds

Moon incremental-build behavior is relevant because a future Java execution model may want to avoid rebuilding unaffected modules or capabilities. It is **not** a blocking Migration-006 prerequisite yet and should not be treated as a selected solution.

Before using Moon for finer-grained Java incrementality, a separate experiment should establish at least:

- whether Moon should cache/reuse whole Maven capabilities or individual modules;
- how Maven reactor dependencies map to Moon project/task dependencies;
- which inputs and outputs are stable enough for safe reuse;
- how `target/`, the Maven local repository and generated resources affect cache identity;
- whether warm Maven builds already make finer Moon granularity unnecessary;
- how changed-path/base→head impact differs from build-output cache reuse;
- whether incremental reuse remains correct across Linux and Windows lanes.

Until that evidence exists, Migration 006 should preserve Maven as the build authority and treat Moon primarily as orchestration/impact/materialization infrastructure.

## Activation criteria

Before implementation begins, the proposal must contain:

- verified current-state inventory for owner, template and downstream repositories;
- baseline measurements for normal affected and unrelated-change behavior;
- selected runtime/toolchain model with rationale;
- selected capability and orchestration boundaries;
- an explicit Windows validation cadence with rationale;
- target resource/latency budget;
- target architecture;
- owner-by-owner implementation sequence;
- explicit template-first and downstream qualification gates.

Migration 005 must also be complete.

## Completion criteria if activated

The eventual migration should not be considered complete merely because new workflows are green. Completion requires:

- shared owner implementation released immutably;
- template migrated, simplified, qualified and versioned/released as the reference consumer;
- unrelated-change path proven to skip unnecessary Java/Windows work;
- real event-timing framework migrated without losing product-specific release semantics;
- Linux canonical evidence and the selected Windows qualification lanes verified at their intended event cadence;
- release path verified with immutable assets/checksums where applicable;
- current-run timing/provenance retained durably;
- final target-versus-result resource measurements recorded;
- durable post-migration Java architecture documented outside the migration folder.
