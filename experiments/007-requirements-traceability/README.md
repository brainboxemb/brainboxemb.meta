# Experiment 007 — requirements traceability PoP

Status: **active**

Tracking issue: [#167](https://github.com/brainboxemb/brainboxemb.meta/issues/167)

Planned implementation/evidence repository:
`brainboxemb/exp.2026-007.requirements-traceability`

Reference project:
`brainboxemb/2026-010-01.meta.event-timing-software`

Possible later production mechanism owner:
`brainboxemb/tool.eng-docs`

## Question

Can BrainboxEmb engineering documentation gain useful, machine-checkable
requirements traceability without replacing readable project Markdown or moving
project meaning into a documentation framework?

The event-timing project already has a deliberate chain:

```text
use case
  -> requirement
  -> interface / architecture / detailed design
  -> implementation
  -> verification case / evidence
```

It also already uses stable identifiers such as `UC-001`,
`SI01-REQ-020`, `IF03-REQ-004` and `VC-ST1-001`.

The PoP must determine whether that existing model can become machine-checkable
with acceptable authoring cost.

## Target concept

Keep project meaning in the owning project repository.

Use a bounded traceability mechanism to:

- represent stable engineering objects and typed links;
- reject duplicate IDs and broken references;
- check useful coverage rules;
- generate traceability tables and graph views;
- export a machine-readable graph for CI and later tooling;
- keep the existing document assembler independent from the traceability engine.

The first candidate is current Sphinx-Needs with MyST/Markdown support.

The PoP compares two integration shapes:

1. **native MyST/Sphinx-Needs authoring** — need objects and links are authored
   directly in Markdown directives;
2. **non-invasive source model** — existing readable Markdown remains the
   primary authored form while a thin metadata/extraction layer produces or
   imports a machine-readable traceability graph.

Do not turn this into a broad tool tournament. Add another candidate only when a
qualified result exposes a concrete unresolved requirement.

## Qualification cases

### TRC-01 — stable identity and graph

Represent a bounded event-timing slice using the project's existing ID schemes
without renumbering or introducing a parallel identity model.

### TRC-02 — invalid-reference detection

Automated verification must reject at least:

- duplicate IDs;
- references to unknown IDs;
- malformed or unsupported relationships.

### TRC-03 — coverage rules

Demonstrate machine-checkable rules for the promoted slice, including:

- an SI-01 requirement has at least one upstream source;
- a requirement has an applicable interface/design allocation;
- a requirement in the selected verification baseline has verification
  coverage;
- orphaned verification cases can be identified.

### TRC-04 — generated views and export

Generate at least:

- a traceability/coverage table;
- a graph/flow view;
- a machine-readable graph/export suitable for CI or later tooling.

### TRC-05 — real event-timing slice

Model a bounded current slice from the real event-timing documentation,
including representative:

- `UC-*`;
- `SI01-REQ-*`;
- `IF03-REQ-*`;
- SAD/SDD allocation;
- `VC-ST1-001`.

The reference project must not be modified merely to satisfy the experiment.

### TRC-06 — authoring/readability cost

Compare the practical source impact of native MyST directives with a
sidecar/extracted metadata approach. The result should explicitly describe:

- source readability on GitHub;
- duplication risk;
- maintenance burden;
- review ergonomics;
- required project syntax changes.

### TRC-07 — tool.eng-docs handoff

Prove a clean boundary by which a later `tool.eng-docs` capability could
consume/publish traceability results without taking ownership of project
requirements and without making Sphinx the general document assembler.

## Ownership

`brainboxemb.meta` owns:

- the cross-project question and active sequencing;
- the qualification scope;
- retained evidence/conclusion;
- the decision whether later production adoption should start.

The planned experiment repository owns:

- the isolated fixture;
- PoP implementation and candidate configuration;
- executable qualification cases;
- generated traceability evidence.

The event-timing coordination repository is a reference source during the PoP.
Its production documents remain unchanged unless a later adoption track is
explicitly selected.

`tool.eng-docs` is only a possible later production owner for a generic
traceability mechanism. It is not the experiment implementation owner.

## Decision outcomes

Experiment 007 should close with one explicit outcome:

- adopt Sphinx-Needs behind a bounded integration;
- adopt the traceability/interchange model but implement a smaller
  `tool.eng-docs` capability;
- retain manual traceability because automation cost exceeds its value;
- define one concrete unresolved requirement that justifies a narrowly scoped
  additional candidate.

Completion does not automatically create or activate a production migration.
