# Migration 010 — standardise SCAD documentation and agent guidance

Status: **complete**

Tracking issue: [#128](https://github.com/brainboxemb/brainboxemb.meta/issues/128)

Input issues:

- [#93 — clarify AGENTS inheritance from meta across repositories](https://github.com/brainboxemb/brainboxemb.meta/issues/93);
- [#124 — plan Forge guidance discovery through repository AGENTS](https://github.com/brainboxemb/brainboxemb.meta/issues/124).

## Phase status

- **Phase 1 — implementation:** complete.
- **Phase 2 — audit/qualification:** complete.
- **Phase 3 — correction:** complete.
- **Phase 4 — closing audit:** complete.

The migration is retained as evidence; durable rules now live in the shared
working-model/SCAD-domain documents and the aligned owner repositories.

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

## Qualification evidence

The blank-agent/documentation model was qualified against real owner
repositories before the template was updated.

| Repository / role | Qualified source | Evidence |
| --- | --- | --- |
| `lib.scad.forge` — first semantic-library canary | `37ef5685f40557f68872937ed752f784d013d10f` | exact-main SCAD production `35844764572` |
| `tool.scad-project` — owner-vs-consumer guidance boundary | `bf580ab77333f544245255b0aeca82e2f8b86e91` | exact-main Test `35845493265` |
| `lib.scad.hub75` — geometry-heavy/physical-verification canary | `67cf49c417cf5fd8128b3ddb89434cb4bf8796c1` | exact-main SCAD production `35848300475` |
| HUB75 display-frame — real application/#93 reproduction | `a47dd533100661ca76f43175534662266ca8ba7b` | exact-main SCAD production `35849957392` |
| `lib.scad.clamps` | `ba6c5e5e89dcfc2d246b2610692ef3db0d10fbb0` | exact-main SCAD production `35852123977` |
| `lib.scad.mechint` | `1a2d70830db63897db89a6c132d10a48d5b9bf0b` | exact-main SCAD production `35852110157` |
| `lib.scad.util` | `3fe0586bc1a0ac45a81e15095bef1f5f26f9bbd5` | exact-main SCAD production `35852744097` |
| retained HUB75 component lab | main `a558795f05055b5cf43c2c97c578f023b880dd4a` | exact PR-head lab build `35852989072`; no push-to-main workflow by design |
| retained Experiment 006 | `1ee94f911e69d811758200a04cc69fc5f3fa6503` | exact-main SCAD production `35853720278` plus DEP-01..DEP-07 regression workflows |
| `template.scad-project` — template last | `8d7478df7e8ea2bf482aa80e356731d03d67fad2` | exact-main SCAD production `35853805546` |

Audit corrections that changed the shared convention itself are also retained:

- meta PR #135 changed bare `// Design:` breadcrumbs to docsgen-safe ordinary
  comment bullets after the HUB75 canary proved the original example invalid;
- meta PR #136 clarified that concise CAD documentation may still be visual:
  useful generated README previews are retained, while abstract repositories do
  not add decorative images merely to satisfy a format.

The current-generation rollout therefore includes the semantic libraries, the
real HUB75 application, the retained lab/experiment cases and the template.
Classic repositories remain outside the migration scope.

## Completion criteria

Migration 010 completed with all criteria met:

- the shared SCAD documentation/agent model is durable in meta;
- Forge passed the retained blank-agent audit;
- tool-owner AGENTS versus pinned consumer documentation is unambiguous;
- the geometry-heavy HUB75 library passed;
- the real HUB75 application reproduced and closed the #93 failure mode;
- selected current-generation SCAD repositories were inventoried and aligned,
  with retained lab/experiment handling kept intentionally lightweight;
- the template was updated last, after real repositories qualified the model;
- exact PR/main CI evidence is retained above;
- #93, #124 and #128 can close without unresolved guidance ambiguity.

Generated API-reference publication, self-contained physical-verification
packages and generic CHANGELOG normalisation may remain open follow-ups.
