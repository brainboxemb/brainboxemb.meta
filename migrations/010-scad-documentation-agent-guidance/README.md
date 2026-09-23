# Migration 010 — standardise SCAD documentation and agent guidance

Status: **active — audit/qualification phase**

Tracking issue: [#128](https://github.com/brainboxemb/brainboxemb.meta/issues/128)

Input issues:

- [#93 — clarify AGENTS inheritance from meta across repositories](https://github.com/brainboxemb/brainboxemb.meta/issues/93);
- [#124 — plan Forge guidance discovery through repository AGENTS](https://github.com/brainboxemb/brainboxemb.meta/issues/124).

## Phase status

- **Phase 1 — implementation:** complete. The shared SCAD documentation and
  agent-guidance model has been established.
- **Phase 2 — audit/qualification:** active. Audit the implemented model from a
  blank-agent perspective against real SCAD repositories.
- **Phase 3 — correction:** apply only concrete changes justified by audit
  findings.
- **Phase 4 — closing audit:** repeat qualification against the corrected state
  and close the migration when the completion criteria are met.

The current work is therefore an audit of the implemented model, not another
initial design/implementation pass.

## Why this migration exists

Current-generation SCAD repositories contain the information needed to work
safely, but a blank agent can still fail to discover the right information
chain.

The concrete failure behind #93 was not missing policy: the shared commit/CI
discipline already existed, but a repository agent followed pinned tool AGENTS
guidance and missed the meta guidance. That produced avoidable per-file
micro-commits and superseded CI runs.

The Forge documentation work then exposed the broader problem:

- repository-local and shared documentation roles were not explicit enough;
- specification was initially used as a contract catalogue rather than the
  explanation of why a library/capability exists;
- detailed-design numbering did not scale;
- dependency-owner AGENTS guidance was being treated as consumer guidance;
- a pinned dependency can legitimately describe exact technical behavior, but
  should not redirect a consumer's working method to dependency-owner rules;
- current CI/test state must be discovered live rather than frozen into source
  documentation.

This is therefore a SCAD/OpenSCAD documentation and agent-guidance migration,
not a Forge-only cleanup.

## Goal

A blank agent, given one current-generation SCAD repository and normal access to
the BrainboxEmb repositories, must be able to determine how to work safely and
how the repository works **without prior chat history**.

The durable model is:

```text
current shared working method
    brainboxemb.meta/AGENTS.md
        -> engineering workflow
        -> Git/commit/PR/CI workflow
        -> SCAD domain entrypoint

repository-specific intent
    local README / AGENTS / doc/00-plan
        -> specification
        -> architecture design
        -> detailed design
        -> verification
        -> source/API docs

exact dependency behavior
    local config + committed gitlink
        -> pinned dependency README / docs / source / tests

current health/status
    live issues / PRs / CI / generated evidence
```

## Authority rules

### Shared agent guidance is top-down

Repository-local `AGENTS.md` files must make
`brainboxemb.meta/AGENTS.md` discoverable as the current shared working
guidance.

Local AGENTS files add only repository-specific navigation, constraints or
exceptions.

### Dependency AGENTS are not inherited

A consumer must not automatically inherit `AGENTS.md` from
`tool.scad-project`, Forge or another pinned dependency.

Those files describe how to work **on the dependency repository itself**.

Exact version-specific dependency behavior is reconstructed from:

- the consumer's configuration;
- the committed dependency gitlink;
- the pinned dependency's README/docs/source/tests;
- exact runtime/CI provenance where applicable.

### Moving guidance versus pinned behavior

Current `brainboxemb.meta` guidance may evolve and is intentionally read as the
current portfolio working convention.

An old pinned release must remain technically understandable from its own pinned
content. A pinned dependency must not require current moving meta content to
explain what that old release does.

## SCAD documentation model

Normal source-document roles are:

```text
README / AGENTS     entrypoints
00 plan             work context, sources, focus, roadmap
10 specification    why this exists and what it should achieve
20 design           architecture-level how
20-xx detailed      detailed design of functional areas
30 verification     how intent/design are demonstrated
source/API docs     exact calls, parameters, examples, deprecation
vrf/                execution and generated evidence
```

Detailed design uses a second number:

```text
20-design.md
20-01-resolution-context.md
20-02-...
...
20-20-...
```

There is no fixed nine-document limit. The second number expresses that the
document belongs to the design family.

Component-local visual `design/design.md` remains valid where physical geometry
is best explained by worked visual construction.

## Blank-agent qualification

A canary passes only when a blank agent can answer all of the following from
discoverable current sources.

### Working method

- Where are the shared BrainboxEmb agent instructions?
- How should issues, branches, commits and PRs be handled?
- Is it clear that related edits should form coherent commits rather than
  per-file micro-commits?
- How should exact-head CI be inspected before merge?

### SCAD conventions

- Where is the current SCAD coding convention?
- Which naming, orientation and readability rules apply?
- How are repository and component design documents structured?

### Repository/library intent

- Why does this repository/library exist?
- What are its major functional areas and non-goals?
- Where is architecture-level design?
- Where is detailed design for a complex functional area?

### API use

- Can the agent find the exact public API/reference?
- Can it determine when a Forge helper should or should not be used?
- Can it identify canonical versus deprecated APIs without reconstructing the
  decision from chat history?

### Tooling and runtime

- Can the agent determine the exact pinned `tool.scad-project` revision?
- Can it understand the consumer's build engine and configured capabilities?
- Can it find how the SCAD Docker runtime is selected and identify the runtime
  actually used by current CI?
- Can it do that from consumer config plus pinned consumer-facing tool docs,
  without treating dependency-owner AGENTS as inherited instructions?

### Documentation and verification

- Can the agent determine how source/API docs are authored/generated?
- Can it determine what tests/verification exist?
- Can it distinguish source verification intent from generated `vrf/`
  evidence?
- Can it obtain the **current** test/CI state from live evidence rather than a
  stale sentence in documentation?

### Cross-project state

- Can the agent find whether a SCAD migration/experiment is currently active?
- Can it avoid starting proposed/inactive work merely because an old issue or
  migration exists?

The retained audit should record exact repository revisions and CI/evidence used
for qualification.

## Rollout sequence

### 1. Shared meta model

Qualify the durable shared rules in `brainboxemb.meta`:

- portfolio agent entrypoint;
- engineering/Git working model;
- SCAD document roles;
- `20-xx` detailed-design numbering;
- dependency-AGENTS non-inheritance rule.

### 2. Forge canary

Use `lib.scad.forge` as the first semantic-library canary.

The canary must prove the complete blank-agent path, including:

- Forge intent/specification;
- architecture and detailed design;
- source-driven API/reference;
- deprecation guidance;
- direct-engine tooling configuration;
- Docker/runtime discovery;
- verification and live CI discovery.

Do not retain canary guidance that duplicates shared meta rules.

### 3. Tooling guidance boundary

Audit `tool.scad-project` consumer-facing documentation and owner AGENTS:

- owner AGENTS may contain tool-repository-specific instructions;
- generic Git/portfolio/SCAD rules should route to meta rather than be copied;
- stale references such as `meta.scad-projects` / `tech.scad` must not remain
  normative guidance;
- consumer-facing README/docs must be sufficient to explain exact pinned tool
  behavior relevant to a consumer.

Release the tool only if a real consumer-facing contract changes require it;
documentation-only owner cleanup does not automatically justify a release.

### 4. Geometry-heavy library canary

Qualify `lib.scad.hub75` to prove coexistence of:

- repository-level numbered documents;
- public source/API documentation;
- component-local visual `design/design.md`;
- physical verification material.

### 5. Application canary

Qualify `2026-009-01.cad.HUB75-display-frame` to prove the application/project
interpretation and to reproduce the #93 failure mode as a cold-start audit.

### 6. Current-generation SCAD rollout

Inventory the remaining current-generation SCAD repositories with AGENTS/docs
and apply only the changes required by the qualified model.

Classic SCAD/CAD repositories remain out of scope unless explicitly selected.

### 7. Template last

Update `template.scad-project` only after the canaries have qualified the model.

The template records the proven convention; it does not participate in deciding
the convention.

## Existing issue disposition

### Incorporated into Migration 010

- **#93** — the original discoverability failure is a required acceptance case.
  Its earlier idea of inheriting pinned tool/domain AGENTS is refined here:
  dependency AGENTS are owner guidance and are not inherited by consumers.
- **#124** — Forge guidance discovery is qualified through the Forge canary.
  Forge owns its API/decision guidance; consumers must be able to discover the
  appropriate pinned Forge documentation when they actually consume Forge.
- **#128** — tracking issue for this migration and rollout.

### Related but not blocking

- **#125 — generated SCAD API-reference publication**: source-driven API docs
  must be discoverable, but generic `scad.docs` API-reference publication is a
  separate tooling capability and does not block this migration.
- **#18 — self-contained physical-verification document packages**: useful
  future document assembly; not required to establish the documentation roles
  or agent-routing contract.
- **#52 — CHANGELOG standardisation**: cross-domain format/template work; this
  migration only requires that agents can discover the current shared changelog
  working rule.
- **#122 — semantic SCAD object naming rollout**: separate API/naming rollout.

## Completion criteria

Migration 010 is complete when:

- the shared SCAD documentation/agent model is durable in meta;
- Forge passes the retained blank-agent audit;
- tool-owner AGENTS versus pinned consumer documentation are unambiguous;
- one geometry-heavy library passes;
- one real SCAD application passes;
- all selected current-generation SCAD repositories have been inventoried and
  aligned or explicitly exempted;
- the template reflects the qualified result;
- exact PR/main CI evidence is retained for changed owner repositories;
- #93, #124 and #128 can close without leaving unresolved guidance ambiguity.

Generated API-reference publication, self-contained physical-verification
packages and generic CHANGELOG normalisation may remain open follow-ups.
