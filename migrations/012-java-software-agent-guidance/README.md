# Migration 012 — standardise Java/software agent guidance

Status: **active**

Tracking issue: [#165](https://github.com/brainboxemb/brainboxemb.meta/issues/165)

## Why this migration exists

Migration 010 established a proven blank-agent guidance model for current-generation SCAD repositories:

```text
local repository intent/navigation
        ↓
brainboxemb.meta/AGENTS.md
        ↓
shared engineering / Git / repository-tooling rules
        ↓
domain-specific guidance
```

The Java/software family still predates that model. Its local `AGENTS.md` files contain useful repository-specific rules, but they do not consistently route agents through the current portfolio entrypoint and several still duplicate shared workflow policy locally.

The concrete trigger was a workflow change in `2026-010-01.meta.event-timing-software`. The portfolio-wide GitHub Actions naming convention already existed in `brainboxemb.meta/docs/40-03-repository-tooling.md`, but the local guidance path did not lead a blank agent there before implementation started.

The problem is therefore not a missing naming rule. The Java/software repositories have not yet adopted the shared top-down agent-guidance model.

## Goal

A blank agent starting in a current Java/software repository must be able to determine:

- where local repository intent and current work live;
- where current shared BrainboxEmb working conventions live;
- how Git/commit/PR/CI and repository-tooling conventions are discovered;
- which Java/software-specific rules apply locally;
- that `AGENTS.md` from pinned tools/dependencies are owner guidance and are not inherited by consumers;
- how exact pinned dependency behavior is reconstructed;
- where current issues, PRs, CI and generated evidence must be inspected.

Local `AGENTS.md` should contain repository-specific navigation, boundaries, constraints and exceptions rather than duplicate durable portfolio rules.

## Authority model

### Shared working guidance is top-down

`brainboxemb.meta/AGENTS.md` is the portfolio-wide agent entrypoint.

Repository-local AGENTS files should explicitly route to it for current shared working conventions.

### Dependency AGENTS are not inherited

A Java consumer must not automatically treat `AGENTS.md` from `tool.java-project`, `tool.git-project` or another pinned dependency as working policy for the consumer repository.

Exact dependency behavior comes from:

- the consumer's configuration;
- committed gitlinks / immutable workflow refs;
- the pinned dependency's README/docs/source/tests;
- exact CI/runtime provenance where relevant.

### Local AGENTS stays local

Keep only:

- where to start in this repository;
- repository role and ownership boundaries;
- local technical constraints and genuine exceptions;
- pointers to durable local documentation.

Do not duplicate changing release numbers, portfolio rollout state or generic Git/workflow conventions.

## Scope

### Java reference template — first canary

- `brainboxemb/template.java-project`
  - owner issue: [#14](https://github.com/brainboxemb/template.java-project/issues/14)
  - first consumer qualification of the shared guidance model;
  - prove the minimal/current Java repository entry path before product rollout.

### Current Java tooling owner

- `brainboxemb/tool.java-project`
  - owner issue: [#32](https://github.com/brainboxemb/tool.java-project/issues/32)
  - qualify owner-vs-consumer guidance boundary after the consumer pattern is proven.

### Real implementation consumer

- `brainboxemb/2026-010-02.java.event-timing-framework`
  - owner issue: [#39](https://github.com/brainboxemb/2026-010-02.java.event-timing-framework/issues/39)
  - roll the proven model into a real multi-module Java consumer.

### Project-family coordination canary

- `brainboxemb/2026-010-01.meta.event-timing-software`
  - this is where the workflow-naming miss was observed;
  - its large project-specific AGENTS should be reduced/routed without losing genuine local documentation boundaries.

### Experiment repositories

Experiment/PoP repositories are **not normal Java rollout consumers merely because their subject matter is Java**.

`brainboxemb/exp.2026-004.java-ci-architecture` remains a retained experiment/regression repository and is out of the normal Migration-012 rollout unless a concrete guidance defect there is deliberately selected later.

## Rollout sequence

1. **Migration authority**
   - record this migration and activate it in `STATUS.md`;
   - use Migration 010 as the proven guidance model, while using the Java template as the first Java consumer canary.

2. **Template canary first**
   - align `template.java-project/AGENTS.md`;
   - prove a blank agent can discover local intent, shared meta guidance and dependency-owner non-inheritance in the minimal reference consumer;
   - treat this as the qualification gate before rollout to real Java consumers.

3. **Real Java implementation rollout**
   - align `2026-010-02.java.event-timing-framework/AGENTS.md`;
   - use it as the first real Java implementation/end-user consumer after the template;
   - prove product architecture/implementation constraints remain discoverable without copying shared rules.

4. **Java tooling-owner cleanup**
   - align `tool.java-project/AGENTS.md` as owner guidance;
   - preserve the owner-versus-consumer boundary;
   - this owner cleanup is required for consistency but is not the consumer rollout gate.

5. **Project-family coordination canary**
   - align `2026-010-01.meta.event-timing-software/AGENTS.md`;
   - reproduce the workflow-naming discovery path and verify the shared repository-tooling authority is found.

6. **Closing audit**
   - verify exact repository revisions and live CI/evidence;
   - record any genuine Java/software exceptions;
   - close owner issues and this migration only when a blank-agent path is reproducible.

## Blank-agent qualification

A selected repository passes when a blank agent can answer, without prior chat history:

### Working method

- Where are the current shared BrainboxEmb agent instructions?
- Where are Git/commit/PR/CI rules?
- Where are GitHub Actions workflow filename/display-name conventions?
- Is it clear which rules are local and which are shared?

### Repository intent

- Why does this repository exist?
- What is its current work/plan entrypoint?
- Where are durable local architecture/design/verification documents?

### Dependency boundary

- Which exact tool versions/revisions are consumed?
- Is it explicit that dependency-owner AGENTS are not inherited?
- Can exact dependency behavior be reconstructed from pinned consumer-facing sources?

### Current state

- Can the agent identify current issues, PRs, CI and generated evidence live rather than relying on stale source text?

## Completion criteria

Migration 012 completes when:

- the selected Java/software repositories follow the same top-down guidance model proven by Migration 010;
- local AGENTS files are concise enough to remain navigation/constraint entrypoints rather than duplicate manuals;
- the workflow-naming discovery failure is reproducibly closed in the event-timing coordination repository;
- dependency-owner AGENTS non-inheritance is explicit in consumer repositories;
- experiment/PoP repositories remain out of the normal rollout unless a concrete repository-specific need justifies inclusion;
- `template.java-project` qualifies the Java consumer pattern before rollout to real Java product repositories;
- exact revisions and CI/evidence are recorded here before closure.
