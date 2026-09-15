# Migration 005 — concrete target-architecture variants

Status: **comparison draft — no target selected**

This document turns the architecture reflection into concrete alternatives. The examples are intentionally **architecture sketches**, not proposed syntax to implement blindly.

Related:

- [Migration 005 README](README.md)
- [Current architecture](current-architecture.md)
- [Architecture reflection](architecture-reflection.md)
- [Measured evidence](measurements.md)

## 1. Design principle: declare project intent once

Today SCAD consumers describe related facts in multiple places.

For example, `project.scad.yml` already knows:

- the Build root;
- whether a standalone render root exists;
- verification commands and verification output root;
- publication branches/policy;
- the selected SCAD tooling through the composed `project.yml` model.

`moon.yml` then separately describes a detailed execution graph and repeats many project/tool/config inputs.

Migration 005 should prefer this rule:

> **A consumer declares project-specific intent and source-impact information; shared SCAD tooling owns the standard execution mechanics.**

That does not require hiding the effective execution graph. A good solution should make the generated/effective graph inspectable without making every repository hand-author it.

## 2. What differs legitimately between clamps and HUB75?

The two qualified libraries are useful because they are not identical.

### `lib.scad.clamps`

Natural project capabilities:

1. **Build documentation** — generated design documentation/images;
2. **Verification** — API/geometry verification output.

There is no separate configured standalone render build in the current project profile.

### `lib.scad.hub75`

Natural project capabilities:

1. **Build renders** — standalone front/rear presentation renders;
2. **Build documentation** — generated design documentation;
3. **Verification** — API STL plus richer physical-verification fixtures/plan output.

This three-way distinction is real domain behavior and should remain expressible.

The architecture should therefore simplify generic finishing/orchestration mechanics without forcing every SCAD repository into exactly two domain tasks.

## 3. Current consumer contract — reference point

### Clamps

Seven visible Moon tasks:

```text
scad.docs
scad.build-index
scad.build-provenance
scad.verify
scad.verification-provenance
scad.production-impact
scad.ci
```

### HUB75

Eight visible Moon tasks:

```text
scad.docs
scad.build
scad.build-index
scad.build-provenance
scad.verify
scad.verification-provenance
scad.production-impact
scad.ci
```

The main complaint is not the number alone. It is that several visible tasks represent standard SCAD lifecycle mechanics rather than project-specific capabilities.

---

# Variant A — keep the current internal Moon graph, generate/inherit it from SCAD project intent

## Idea

Keep the proven internal behavior largely intact, but stop asking every consumer to maintain all standard Moon tasks manually.

`tool.scad-project` would own a standard SCAD Moon graph. The consumer would supply only:

- which domain capabilities exist;
- project-specific source-impact additions/overrides that cannot be inferred;
- exceptional output paths if they differ from the project profile.

The internal graph may still contain separate finishing tasks and two roots if those remain technically useful.

## Human-facing model

Clamps:

```text
Build documentation
Verification
```

HUB75:

```text
Build renders
Build documentation
Verification
```

A maintainer does not need to edit `build-index`, source-information, impact-root or full-root mechanics for ordinary project work.

## Possible configuration shape

Illustrative only:

```yaml
# project.scad.yml
ci:
  capabilities:
    docs:
      impact:
        - openscad/**
        - pythonscad/**
        - scripts/render-openscad-design.sh

    verification:
      impact:
        - openscad/**
        - pythonscad/**
        - test/**
        - vrf/**
        - scripts/run-verification.sh
        - scripts/build-verification-index.sh
```

HUB75 adds a build capability:

```yaml
ci:
  capabilities:
    build:
      impact:
        - openscad/**/*.scad
        - openscad/**/render.yml

    docs:
      impact:
        - openscad/**/*.scad
        - openscad/**/design/**

    verification:
      impact:
        - openscad/p5-64x32-panel/hub75_p5_64x32_panel.scad
        - test/**
        - vrf/fixtures/**
        - vrf/top-left/**
        - vrf/measurement-catalog.yml
        - vrf/physical-panel-validation.md
        - vrf/test-case-template.md
        - scripts/run-verification.sh
        - scripts/build-verification-index.sh
```

Common inputs such as `project.yml`, `project.scad.yml`, the SCAD tooling tree and standard workflow files should be supplied by the shared policy rather than repeated in every capability.

## Effective internal graph

Could initially remain similar to today:

```text
source-impact root
    -> docs
    -> build (when configured)
    -> verify

full result root
    -> Build finishing
    -> Verification finishing
```

The difference is ownership: this graph belongs to `tool.scad-project`, not each consumer.

## Advantages

- lowest behavioral-change risk;
- preserves current affected logic while reducing consumer maintenance;
- central fixes to lifecycle/evidence rules apply to every SCAD repo;
- project differences remain declarative;
- possible to migrate incrementally before deeper runtime optimization.

## Disadvantages / risks

- internal complexity still exists even if consumers do not hand-author it;
- hiding the graph would be bad if no inspection mechanism exists;
- Moon configuration generation/inheritance must have a robust mechanism;
- does not by itself improve the ~20 s Docker pull or ~41–45 s relevant latency.

## Required transparency

If this variant is selected, provide a command such as conceptually:

```text
scad-project explain-ci
```

that shows, in plain language:

- capabilities;
- effective impact inputs;
- effective outputs;
- dependency relationships;
- which parts are standard shared policy versus repository overrides.

The exact command name is not selected here; the requirement is inspectability.

---

# Variant B — coarse Moon capability graph

## Idea

Change Moon itself to model only real project capabilities, rather than internal finishing steps.

The primary Moon tasks would represent complete domain results.

Clamps could become conceptually:

```text
scad.build-result
scad.verification-result
scad.ci -> both
```

HUB75 could become:

```text
scad.build-renders
scad.build-docs
scad.verification-result
scad.ci -> all
```

Or, if Build renders + docs should always travel together as one published Build tree:

```text
scad.build-result
scad.verification-result
scad.ci -> both
```

with `scad.build-result` running both Build producers internally.

## Alignment with existing `tool.scad-project`

This variant aligns more closely with commands that already exist:

```text
produce-build
produce-verification
```

Those commands already describe a complete Build or Verification result, including finishing work.

The architecture question becomes whether Moon needs to see the internal finishing steps at all.

## The hard problem: source impact versus publication context

Today the separate source-impact root exists for a real reason.

A complete result contains files whose contents depend on CI context, for example:

- PR/ref information;
- current publication context;
- exact current source information.

If those changing values are ordinary Moon inputs of the coarse cached task, the task can look affected even when no CAD source changed. That would break the zero-container README-only path.

Therefore Variant B is viable only if the architecture separates two concepts **inside shared tooling**:

```text
source impact
    !=
current publication finishing
```

without requiring consumers to model that separation as several tasks.

Possible implementation directions to investigate, not decisions:

- cache only source-derived output and write current publication information after hydration;
- keep source-information/current-run evidence outside the cached capability output;
- let `tool.scad-project` expose an internal source-impact projection of each capability;
- have Moon task inputs represent only source-derived work while host finishing updates context-specific metadata after Moon completes.

## Advantages

- much smaller effective Moon graph;
- aligns Moon with the level at which humans think about the repository;
- aligns with existing complete producer commands;
- clearer Moon/SCons boundary: Moon owns whole capabilities, SCons owns targets inside them;
- removes index/source-information tasks from the visible graph.

## Disadvantages / risks

- requires careful redesign of cache/evidence truthfulness;
- a coarse task can invalidate more output than necessary unless SCons remains effective inside it;
- may reduce opportunities for Moon to cache docs/build pieces separately;
- source-impact handling must remain correct for README-only changes.

## Architectural attractiveness

This is currently the strongest simplification candidate **if** evidence/publication context can be cleanly separated from source-derived cached output.

---

# Variant C — Moon for impact analysis only; SCons/tool.scad-project own execution

## Idea

Keep the part of Moon whose value has already been demonstrated: repository-level impact analysis before the SCAD runtime starts.

Do not rely on Moon as the in-container execution/output-cache layer.

Conceptually:

```text
host
  -> Moon: is Build/docs/Verify source affected?
  -> if none: stop
  -> if affected: pull/start SCAD runtime

container
  -> tool.scad-project / SCons produce required domain results

host
  -> finish evidence/publication
```

Moon would no longer need to execute the aggregate `scad.ci` graph inside Docker.

## Why this variant is now worth considering

Migration 004 demonstrated Moon's impact-analysis value.

The retained qualification runs inspected so far have **not** demonstrated a practical warm cross-run Moon output-hydration benefit. Cold-cache Build-only/docs-only HUB75 runs still executed unrelated domains once the full aggregate graph started.

That does not prove Moon caching is useless. It does make “Moon must be in the execution path because its output cache is valuable” an unproven premise.

## Execution choices

If only Build is affected:

```text
produce-build
```

If only Verification is affected:

```text
produce-verification
```

If both are affected, they may be executed concurrently inside one container if the output/cache directories and tooling contracts safely permit that.

For HUB75, the impact model would need to retain the distinction between standalone Build renders, docs and Verification if independent execution remains useful.

## Advantages

- preserves the proven zero-container affected gate;
- removes Moon task-cache/output-hydration mechanics from the heavy execution path;
- makes SCons clearly the only fine-grained execution/cache engine inside SCAD work;
- potentially removes Moon aggregate execution/materialization evidence and portable output-cache restore/save from the affected path;
- simpler mental model than two nested dependency/cache engines.

## Disadvantages / risks

- loses Moon whole-task output hydration if that later proves valuable;
- host must receive enough information from Moon impact analysis to know which capability/capabilities to run, not only a single boolean;
- concurrent Build/Verification execution must be qualified;
- affected analysis still requires the Moon runtime and an effective graph/source model.

## Key experiment

Before accepting or rejecting Variant C, run a controlled warm-cache experiment.

If Moon hydration saves substantial Build/Verification work in realistic SCAD changes, removing it has a real cost.

If it saves little beyond what SCons already saves, Variant C becomes much more attractive.

---

# Variant D — remove Moon from SCAD orchestration

## Idea

`tool.scad-project` would own both source-impact analysis and execution orchestration; SCons would remain the target engine.

Consumer mental model becomes smallest:

```text
GitHub -> scad-project lifecycle -> SCons/domain commands
```

## Why this is not the default recommendation

Moon was introduced specifically to avoid inventing another repository-level scheduler/hash/cache/affected engine.

Removing Moon is only a simplification if the replacement is genuinely smaller.

A custom list of changed paths in GitHub Actions or `tool.scad-project` would create two sources of truth:

```text
impact rules
build dependency rules
```

and could silently skip required work when they diverge.

## When Variant D could win

Only if measurements show that:

- Moon's only meaningful SCAD value can be replaced by a very small, trustworthy source-impact model derived directly from project configuration;
- Moon output caching is not materially useful;
- the custom impact implementation remains obviously simpler than keeping Moon.

Until then, this is a control alternative rather than the preferred direction.

---

# Variant E — keep current graph, optimize only lifecycle/runtime

## Idea

Make minimal structural changes:

- retain current consumer Moon graph;
- improve image distribution;
- reduce impact-check overhead;
- remove unnecessary workflow-artifact handoffs;
- overlap safe publication work;
- document the graph much better.

## Advantages

- lowest technical risk;
- can directly improve the measured critical path;
- useful as a baseline to separate performance gains from architecture simplification.

## Disadvantages

- consumer still sees seven/eight tasks;
- repeated configuration remains;
- human-understandability problem is explained rather than solved.

Variant E is therefore unlikely to be sufficient by itself, but its runtime improvements may be combined with another variant.

---

# 4. Side-by-side comparison

Current assessment before experiments:

| Criterion | Current | A: hidden/generated detailed graph | B: coarse Moon capabilities | C: Moon impact only | D: no Moon | E: current + optimize |
| --- | --- | --- | --- | --- | --- | --- |
| consumer-visible complexity | high | low | low | low | lowest | high |
| preserves proven Moon affected behavior | yes | yes | yes | yes | no/replaced | yes |
| preserves Moon whole-output cache | yes in design, benefit unproven | yes | yes at coarse level | no | no | yes |
| clear Moon/SCons boundary | weak | medium | **strong** | **strong** | n/a | weak |
| evidence redesign required | low | low | medium/high | medium | medium/high | low |
| likely performance change from structure alone | none | near-neutral | uncertain | possibly small improvement | uncertain | none until optimizations |
| implementation risk | current | low/medium | medium | medium | high | low |
| solves human-maintainability problem | no | yes | **yes** | yes | yes if replacement stays small | no |

## 5. Current preferred evaluation order

Do not select a target yet.

Evaluate in this order:

1. **Variant B — coarse Moon capabilities** because it gives the cleanest conceptual Moon/SCons boundary and aligns with existing complete producer commands.
2. **Variant A — generated/inherited detailed graph** as the lower-risk fallback if B cannot preserve cache/evidence correctness cleanly.
3. **Variant C — Moon impact only** if controlled measurements show Moon output hydration adds little practical value.
4. **Variant E — lifecycle optimizations** should be evaluated independently and may be combined with A/B/C.
5. **Variant D — no Moon** remains the control case; choose it only if the replacement impact logic is demonstrably simpler and equally safe.

## 6. What must be measured next

Before narrowing the target:

1. demonstrate a controlled **warm Moon output-cache** run and record exactly which tasks hydrate rather than execute;
2. demonstrate a controlled **warm SCons cache** run separately;
3. quantify image size/layer distribution and compare normal GHCR pull with any realistic explicit cache alternative;
4. split the ~4.7 s impact path into Moon-runtime restore, Moon query, evidence generation and artifact upload;
5. identify whether same-job Build/Verification workflow artifacts are consumed by anything after the run;
6. test whether publication can safely overlap;
7. sketch the effective config size/complexity for A/B/C for both clamps and HUB75.

Only after these measurements should Migration 005 choose the long-term architecture and derive implementation steps.
