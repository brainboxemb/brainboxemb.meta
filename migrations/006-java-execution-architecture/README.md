# Migration 006 — simplify the Java execution architecture

Status: **proposed / inactive**

Tracking issue: [#65](https://github.com/brainboxemb/brainboxemb.meta/issues/65)

Activation blocker: [Migration 005](../005-scad-execution-architecture/README.md) is still active and must close first.

## Why this migration is being prepared

The current Java tooling already has several strong foundations: a released `tool.java-project`, exact Temurin/Maven/Maven-Wrapper configuration, a canonical Linux Maven producer, persistent producer/test evidence, an independent Windows compatibility path, Moon-based capability reuse and real downstream releases.

The repository-level execution model is nevertheless much more consumer-heavy than the current SCAD architecture. `template.java-project` and `2026-010-02.java.event-timing-framework` still own large workflows containing checkout/bootstrap, JDK provisioning, Moon invocation, evidence staging/verification, artifact transport, Windows coordination and publication mechanics.

This migration investigates whether those lifecycle mechanics can be simplified and moved to their proper owners without weakening Java-specific correctness requirements.

## Scope

Primary repositories:

- `brainboxemb/tool.java-project` — owner of Java build/test/toolchain semantics and reusable Java workflows;
- `brainboxemb/template.java-project` — reference consumer/canary;
- `brainboxemb/2026-010-02.java.event-timing-framework` — real current-generation downstream consumer;
- `brainboxemb/tool.git-project` — only for genuinely domain-neutral affected/Moon/publication mechanics.

The event-timing software meta repository is **not** the owner of this infrastructure migration. Product architecture remains there; generic Java project execution belongs in the shared tooling chain.

## Important non-assumption

Migration 006 must **not** copy the SCAD solution mechanically.

In particular, Java may not need a dedicated container image. The current exact native baseline (`Temurin 8.0.504+1`, Maven `3.9.16`, Maven Wrapper `3.3.4`) and required Windows compatibility may make pinned hosted-runner provisioning the correct runtime contract. This is an explicit design question, not a predetermined migration step.

## Initial hypothesis

The most promising direction to evaluate is:

```text
GitHub Actions host
  exact source/base + generic change-impact preflight
        |
        +--> unrelated -> stop before JDK/Maven/Windows work
        |
        v
shared Java execution plan / capability policy
        |
        +--> canonical Linux build/test/materialization
        |
        +--> independent Windows compatibility only when required
        |
        v
host finishing/publication/release
  exact current source context
  durable orchestration timings/evidence
```

This is only a hypothesis. The target architecture is not selected until current-state and measurement evidence support it.

## Read this proposal

| Document | Role |
| --- | --- |
| [01 — Change request](01-change-request.md) | Problem, goals, non-goals and activation/completion criteria. |
| [02 — Current state](02-current-state.md) | Current owner boundaries, workflows, duplication and open architecture questions. |
| [10 — Baseline measurements](10-baseline-measurements.md) | Current template/downstream wall-clock and hosted-job baseline. |

A target architecture and implementation plan will be added only after the proposal is sufficiently validated.

## Activation criteria

Migration 006 may become active only when:

1. Migration 005 is actually complete;
2. current Java ownership and execution flows have been reverified against repository main branches;
3. baseline measurements cover at least the template and real downstream consumer;
4. the runtime decision (native pinned JDK versus dedicated immutable runtime) has evidence behind it;
5. capability boundaries and unrelated-change behavior are defined;
6. an owner-by-owner implementation/qualification order is documented.

Until then, this folder is planning material only and no Java owner repository should be changed because of Migration 006.
