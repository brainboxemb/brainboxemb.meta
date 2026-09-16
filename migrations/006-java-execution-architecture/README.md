# Migration 006 — simplify the Java execution architecture

Status: **proposed / inactive**

Working draft: [#65](https://github.com/brainboxemb/brainboxemb.meta/pull/65)

Predecessor: [Migration 005](../005-scad-execution-architecture/README.md) — complete.

## Current status

Migration 006 is intentionally recorded on `main` before the design is finished. Migration 005 is now complete, so there is no longer a predecessor blocker, but Migration 006 is **not automatically active**. Activation requires an explicit decision after the current Java repositories have been revalidated and the working hypotheses below have been turned into a concrete target architecture, owner sequence and qualification plan.

The current investigation is useful enough to retain as cross-project status, but it is **not yet an implementation plan** and does not authorize Java owner-repository changes.

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

## What is currently known

The existing Java tooling already has a strong domain baseline: exact Temurin/Maven/Maven-Wrapper versions, a canonical Linux Maven producer, persistent execution/test evidence, reusable Windows compatibility and real downstream releases.

The main problem is repository-level orchestration. The template and downstream project still own substantial duplicated lifecycle logic: checkout/bootstrap, Java setup, Moon invocation, evidence staging, artifact hand-off, Windows coordination and generated-output publication.

Representative current runs show that this is not mainly a Maven-performance problem:

- `template.java-project` normal main execution uses six hosted jobs and roughly 72–76 seconds wall-clock;
- `2026-010-02.java.event-timing-framework` uses seven executing jobs on an ordinary main push and roughly 94 seconds wall-clock;
- there is no early generic unrelated-change gate before JDK/Maven/Windows work;
- full-history checkout and several artifact/job boundaries are still used where newer shared repository tooling may allow a simpler model.

These measurements are research inputs only. They must be refreshed against the then-current repositories before Migration 006 is activated.

## Current preferred direction

These are working hypotheses to verify when Migration 006 is activated, not final decisions:

1. Keep **Maven as the Java build/test authority**. Moon should initially be treated as affected-selection/orchestration/materialization infrastructure, not as a replacement Java build engine.
2. Add an **early generic base→head affected preflight** so unrelated changes can finish before JDK/Maven and Windows work where correctness allows.
3. Move generic Java production orchestration toward **`tool.java-project` ownership**, leaving consumers with thin triggers, permissions and project-specific configuration.
4. Prefer the existing **native pinned JDK/Maven model** over introducing a Java container unless measurements show a real benefit. Independent native Windows validation remains required in any case.
5. Reconsider **Windows cadence**. Full Windows rebuild and exact Linux-artifact smoke should not automatically run for every main push; PR qualification plus release qualification is the leading option to evaluate.
6. Remove hosted-job/artifact boundaries that exist only because consumers currently stage and re-check publication evidence themselves. Keep boundaries that represent real isolation, especially Linux→Windows artifact verification.
7. Move consumers toward the same general dependency identity principle used successfully elsewhere: readable released workflow/tool refs plus exact committed source identity where applicable.
8. Add durable workflow timing/provenance evidence so wall-clock and total hosted-compute effects can be compared before and after migration.

## Explicitly parked research

**Moon fine-grained Java/Maven incrementality is not an activation blocker.** It should be investigated separately before exposing Maven modules as Moon tasks or relying on module-level portable cache reuse. The initial migration should stay conservative and use Maven as the canonical build authority.

## Before activation

Reverify `tool.git-project`, `tool.java-project`, `template.java-project` and the real Java downstream consumer against their current `main` branches. Then turn the hypotheses above into a concrete target architecture and owner-by-owner qualification sequence, with explicit evidence for unrelated changes, normal Linux build/test, Windows compatibility, publication/provenance, releases and hosted-compute effects.

The draft material in PR #65 can be used as research input, but `main` is the authority for this migration's status.
