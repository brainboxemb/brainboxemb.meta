# Migration 005 — simplify the SCAD execution architecture

Status: **active — architecture definition first**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this migration exists

Migration 004 proved a working shared SCAD execution model and materially reduced unnecessary heavy CI work. It also exposed a new problem: the resulting execution model is difficult to understand from a normal project or library repository.

The next change should therefore not be another mechanical rollout. First define a simpler architecture that a human maintainer can understand without reconstructing old migration history or chat/agent reasoning.

This migration is deliberately a **current architecture umbrella**. The final implementation is not selected yet.

## The problem in plain language

A current SCAD repository can contain several Moon tasks for building, documentation, verification, preparing generated output and deciding whether expensive CAD work is needed at all.

Those tasks have technical reasons, but the reasons are spread across several repositories and historical documents. Someone opening `moon.yml` sees many steps without a simple explanation of:

- what actually creates CAD/document output;
- what merely prepares that output for publication;
- what only decides whether expensive work is needed;
- why some steps must stay separate;
- which steps are historical complexity that can now be removed.

Migration 005 must make that understandable first and simpler where possible.

## Performance baseline inherited from Migration 004

Architecture decisions must use measured performance, not vague claims.

The retained `lib.scad.clamps` measurements are:

| Situation | Wall-clock / lifecycle | Heavy SCAD containers | Notes |
| --- | ---: | ---: | --- |
| Pre-Migration-004 parallel Build + Verify | about **37 s** critical path | 2 | Build about 37 s, Verify about 32 s; roughly 68–70 runner-seconds total. |
| First common v0.13.0 topology | about **64–65 s** | 1 | Regression caused by serial GitHub job/artifact boundaries. |
| Final v0.13.1 one-host topology | about **41–45 s** | 1 | One host job; one explicit Docker process; publication in the same host job. |
| Final README-only controls | about **4.4–4.8 s** | 0 | Stops before SCAD image pull/container startup. |

Important interpretation:

- relevant-change wall-clock was **not faster than the old ~37 s parallel baseline**; it ended around 41–45 s;
- the v0.13.0 64–65 s regression was removed;
- heavy setup/runner usage was reduced from two SCAD jobs/containers to one;
- unrelated changes became dramatically cheaper because they now stop in roughly 4–5 s with no SCAD container;
- old job-level container initialization alone was observed around 17–30 s before checkout, so avoiding that path for unrelated changes is a material improvement.

Migration 005 must continue to distinguish:

1. **wall-clock feedback time**;
2. **total runner/compute time**;
3. **container/image setup cost**;
4. **unaffected-change cost**.

A design that adds substantial complexity for a one- or two-second gain is not automatically an improvement. Complexity must buy a material reliability, understandability or performance benefit.

## Architecture invariants to preserve unless explicitly reconsidered

These are the useful outcomes already proven by Migration 004:

- an unrelated change such as a root README edit should not start the SCAD container;
- uncertain impact should run safely rather than incorrectly skip required work;
- normal Build and Verification remain independently meaningful capabilities;
- SCAD target-level rebuild decisions remain dependency-aware;
- generated output must state which exact source/tooling produced it;
- GitHub write credentials stay outside the SCAD runtime;
- a release is reproducible from one exact source revision.

Everything else is open to simplification if those outcomes can be retained more clearly.

## Architecture questions

Before implementation, answer these in ordinary language:

1. What are the minimum concepts a maintainer actually needs to see?
2. Which current Moon tasks create real output, and which only exist to support orchestration/publication?
3. Can finalization/index/provenance steps be grouped without making cache/evidence misleading?
4. Do we need two visible Moon root tasks for impact checking and full execution, or can the same behavior be expressed more clearly?
5. Is Moon still the right visible repository-level abstraction for all these responsibilities?
6. Where should SCons stop and repository orchestration start?
7. Which evidence is useful to a human, and which is implementation detail that should stay hidden in tooling?
8. Can a project describe its intent with substantially less repeated input/output configuration?
9. What should a new project/library have to configure itself versus inherit from shared tooling?
10. How do we explain the resulting model with terms that do not require CI-specialist vocabulary?

## First phase — define current and target architecture

Do not change consumers yet.

First produce:

- one plain-language diagram of the **current** execution flow;
- a glossary using ordinary terms before specialist terms;
- a table for every visible task: purpose, owner, inputs, outputs and why it must be separate;
- a list of accidental/historical complexity candidates;
- at least two simpler target variants;
- measured performance implications for each variant;
- a selected target architecture with explicit reasons for keeping every remaining visible concept.

Only then derive implementation steps and repository owners.

## Human-understandability acceptance test

Give a maintainer a normal consumer repository plus one linked current-architecture page.

Without migration history or chat logs, that maintainer should be able to answer:

- what happens after a README-only change;
- what happens after a CAD source change;
- what happens after a verification-only change;
- which expensive process starts and why;
- where generated Build and Verification output comes from;
- why each visible task is separate.

If that cannot be answered, the architecture is not finished.

## Initial repositories in scope

Architecture/reference work may involve:

- `brainboxemb.meta` — cross-project decision and migration evidence;
- `tool.git-project` — generic repository/Moon mechanics;
- `tool.scad-project` — SCAD lifecycle and reusable workflow behavior;
- `template.scad-project` — reference consumer;
- `lib.scad.clamps` and `lib.scad.hub75` — qualified library examples;
- `2026-009-01.cad.HUB75-display-frame` — real consumer, but do not migrate it until the target architecture is selected.

The frame currently remains on `tool.scad-project v0.12.0` and `lib.scad.hub75 v0.1.3`. Its eventual migration belongs here rather than extending Migration 004 with an architecture we are already reconsidering.
