# Migration 005 — simplify the SCAD execution architecture

Status: **active — architecture definition first**

Tracking issue: [#55](https://github.com/brainboxemb/brainboxemb.meta/issues/55)

Predecessor: [Migration 004](../004-scad-repository-execution-model/README.md)

## Why this migration exists

Migration 004 proved a working shared SCAD execution model and materially reduced unnecessary heavy CI work. It also exposed two related problems:

1. the resulting execution model is difficult to understand from a normal project or library repository;
2. on the small `lib.scad.clamps` reference repository, the final one-container architecture still takes **longer on the relevant-change critical path** than the older two-container parallel architecture.

The next change should therefore not be another mechanical rollout. First define a simpler architecture that a human maintainer can understand and that treats wall-clock feedback time as a first-class design constraint.

This migration is deliberately a **current architecture umbrella**. The final implementation is not selected yet.

## The problem in plain language

A current SCAD repository can contain several Moon tasks for building, documentation, verification, preparing generated output and deciding whether expensive CAD work is needed at all.

Those tasks have technical reasons, but the reasons are spread across several repositories and historical documents. Someone opening `moon.yml` sees many steps without a simple explanation of:

- what actually creates CAD/document output;
- what merely prepares that output for publication;
- what only decides whether expensive work is needed;
- why some steps must stay separate;
- which steps are historical complexity that can now be removed.

There is also a performance warning hidden by the phrase “one container”: the old Build and Verify containers started **in parallel**. Replacing them with one serial container reduces total compute, but does not automatically reduce the time a developer waits.

Migration 005 must make both the architecture and the critical path understandable, then simplify them together where possible.

## Performance baseline inherited from Migration 004

Architecture decisions must use measured performance, not vague claims.

The retained `lib.scad.clamps` measurements are:

| Situation | Wall-clock / lifecycle | Heavy SCAD containers | Notes |
| --- | ---: | ---: | --- |
| Pre-Migration-004 parallel Build + Verify | about **37 s** critical path | 2 | Build and Verify overlap; roughly 68–70 runner-seconds total. |
| First common v0.13.0 topology | about **64–65 s** | 1 | Clear regression caused by serial GitHub job/artifact boundaries. |
| Final v0.13.1 one-host topology | about **41–45 s** | 1 | One host job; one explicit Docker process; publication in the same host job. |
| Final README-only controls | about **4.4–4.8 s** | 0 | Stops before SCAD image pull/container startup. |

### What the final 41–45 seconds contain

Representative final run `34971400621` shows approximately:

| Phase | Approx. elapsed time |
| --- | ---: |
| Source checkout + exact base preparation | **1.9 s** |
| Moon impact check + retained evidence | **4.7 s** |
| Cache/range preparation | **1.9 s** |
| SCAD Docker image pull | **20.0 s** |
| Container bootstrap + validation + production | **9.4 s** |
| of which the Moon producer/finalization graph itself | **5.132 s** |
| Stage + upload generated artifacts | **2.6 s** |
| Sequential Build + Verification publication | **4.4 s** |
| Post-job cache/cleanup | about **1.4 s** |

This is the central performance fact for Migration 005: **the real SCAD/docs/verification workload is only about five seconds; most elapsed time is infrastructure around it.**

### Why the old two-container path could still be faster

In the old baseline, Build and Verify each spent roughly 17–18 s pulling/starting the SCAD image, but those pulls happened concurrently on separate runners.

The old critical path therefore paid roughly one image-pull delay in wall-clock time while consuming that heavy setup twice in total runner resources.

The new model pays only one image pull in compute terms, but that pull plus the new impact check and publication tail are all on one serial critical path.

So Migration 004 traded:

- **less total compute/setup duplication**

for:

- **slightly slower relevant-change feedback on the small reference repository**.

That trade-off must be reconsidered explicitly rather than treated as an automatic improvement.

## Performance rules for Migration 005

Migration 005 must keep these metrics separate:

1. **developer feedback latency** — how long until a relevant CI result is ready;
2. **total runner/compute time** — how much hosted execution is consumed across jobs;
3. **container/image setup cost** — especially the large immutable SCAD image pull;
4. **unaffected-change latency** — changes that should not execute CAD at all;
5. **actual domain work** — time spent rendering, exporting, documenting or verifying rather than orchestrating CI.

The old ~37 s relevant-change critical path is a real baseline. A new architecture should aim to meet or improve it on the simple reference repository under comparable normal image-pull conditions. If it does not, the additional latency must be justified by a material reliability/security/correctness benefit rather than by container-count reduction alone.

A design that adds substantial complexity for a one- or two-second gain is not automatically an improvement. Conversely, a design that removes substantial complexity is valuable even if performance remains statistically equivalent.

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
11. Can the affected check be made materially cheaper without losing the zero-container unaffected path?
12. Which work after production must actually be serial, and which work can safely overlap?
13. Why do we upload temporary workflow artifacts when publication happens in the same host job, and can any of that path be removed without losing retained evidence?
14. Can dependency/bootstrap work be reduced or moved without reintroducing credential or reproducibility problems?
15. Is the current ~20 s image pull an unavoidable external floor, or can runtime/image distribution be improved separately without duplicating the failed cached-host approach?

## First phase — define current and target architecture

Do not change consumers yet.

First produce:

- one plain-language diagram of the **current** execution flow;
- a critical-path diagram with measured time attached to each major phase;
- a glossary using ordinary terms before specialist terms;
- a table for every visible task: purpose, owner, inputs, outputs and why it must be separate;
- a list of accidental/historical complexity candidates;
- at least two simpler target variants;
- measured/predicted performance implications for each variant, clearly separating wall-clock and runner consumption;
- a selected target architecture with explicit reasons for keeping every remaining visible concept.

Only then derive implementation steps and repository owners.

## Human-understandability acceptance test

Give a maintainer a normal consumer repository plus one linked current-architecture page.

Without migration history or chat logs, that maintainer should be able to answer:

- what happens after a README-only change;
- what happens after a CAD source change;
- what happens after a verification-only change;
- which expensive process starts and why;
- where the majority of CI time is currently spent;
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
