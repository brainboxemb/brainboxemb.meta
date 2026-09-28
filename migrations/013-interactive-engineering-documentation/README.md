# Migration 013 — adopt interactive engineering documentation and traceability

Status: **active**

Tracking issue: [#169](https://github.com/brainboxemb/brainboxemb.meta/issues/169)

Qualified source experiment:
[Experiment 007](../../experiments/007-requirements-traceability/README.md)

Human review:
[Experiment 007 GitHub Pages](https://brainboxemb.github.io/exp.2026-007.requirements-traceability/)

## Why this migration exists

Experiment 007 qualified a documentation model that keeps the existing
engineering book useful while adding machine-checkable traceability and richer
navigation over the same engineering meaning.

The experiment established that the desired production shape is not one new
monolithic documentation tool.

It is a responsibility split:

```text
project Markdown + diagram source
          |
          +-- stable engineering object identity
          +-- compact authored relations
          |
          v
generic extraction / validation / rendering
          |
          +----------------------+----------------------+
          |                      |                      |
          v                      v                      v
engineering book           documentation portal     engineering graph
linear reading             search/navigation        backlinks/context
          |                      |                      |
          +----------------------+----------------------+
                                 |
                          clickable architecture
```

The experiment repository must not become a production dependency. Generic
mechanisms now move to their normal owners and are qualified through a real
event-timing consumer.

## Qualified principles

Migration 013 preserves these Experiment-007 decisions:

1. the engineering **Book** remains a first-class output;
2. normal readable Markdown remains project source;
3. native MyST/Sphinx-Needs directives are not the default project authoring
   format;
4. stable engineering IDs and source targets are explicit;
5. relationships are authored once and inverse backlinks/matrices are generated;
6. a normalized engineering-graph boundary separates source authoring from
   reader views;
7. Sphinx-Needs remains a viable optional relationship/validation engine behind
   that boundary rather than becoming the documentation architecture;
8. Material for MkDocs is a qualified reader-facing portal candidate;
9. diagram source carries engineering identity and generated SVG preserves it;
10. project-specific meaning remains in consuming repositories.

## Scope boundary

Migration 013 is deliberately staged.

Do **not** copy the complete experiment implementation into `tool.eng-docs` in
one change.

Do **not** require every BrainboxEmb repository to adopt the portal/graph model.

The first production canary is the event-timing documentation. Wider adoption is
demand-driven only after the canary proves the released mechanisms.

## Step 1 — reusable diagram engineering identity

Owner: `brainboxemb/tool.eng-docs`

Current released baseline: `v0.3.10`.

Add the smallest reusable mechanism proven by Step 06:

- optional opaque `object_id` on diagram nodes;
- schema validation;
- semantic validation where appropriate;
- preserve the same identity in generated SVG as a stable machine-readable
  attribute such as `data-engineering-id`;
- preserve the identity in editable draw.io metadata where practical;
- domain-neutral user example;
- executable SVG/draw.io/schema tests;
- Linux + Windows normal owner qualification.

Constraints:

- no Sphinx-Needs dependency;
- no project-specific graph semantics;
- no event-timing IDs in reusable examples;
- no portal-owned label-to-object mapping.

This is the first migration gate.

## Step 2 — event-timing diagram canary

Owner: `brainboxemb/2026-010-01.meta.event-timing-software`

After Step 1 is released:

- pin the released `tool.eng-docs`;
- add `object_id` to a small set of real architecture nodes, initially the
  already-qualified `TimingNode`, `CommandHandler`, `Conductor` and
  `RemoteApi`;
- rebuild normal SVG + draw.io output;
- verify exact generated output preserves identity;
- keep the normal architecture diagram visually unchanged except for
  machine-readable metadata;
- do not add a second lookup map.

## Step 3 — stable source anchors and compact relation authoring

Owners:
- project meaning: event-timing coordination repository;
- generic syntax/extraction mechanism: reassess before implementation.

Qualify the smallest production authoring convention using the real first slice:

- `UC-001`, `UC-008`, `UC-014`;
- `SI01-REQ-003/020/021/022/030/031`;
- `IF03-REQ-001/002/004`;
- selected architecture elements;
- `VC-ST1-001`.

Requirements:

- ordinary Markdown remains readable on GitHub;
- every graph-exposed object has a stable source target;
- compact metadata stays adjacent to the owning object;
- inverse traceability is generated rather than authored;
- invalid or unknown relations fail near the owning source.

Do not migrate the complete document set in this step.

## Step 4 — reusable engineering graph boundary

After Step 3 proves the source convention, select the smallest reusable owner
capability needed for:

- object IDs/types;
- source locations;
- typed relations;
- generated backlinks;
- duplicate/unknown-link/type validation;
- bounded focused traversal;
- coverage checks where configured.

`tool.eng-docs` is the likely owner, but this is reassessed from the proven
authoring shape rather than assumed.

Sphinx-Needs may remain an optional engine/export adapter. The normalized graph
contract must not require consumers to author native Sphinx directives.

## Step 5 — event-timing production portal canary

Use released/pinned owner mechanisms to add a real derived portal while keeping
the existing book.

The canary should provide:

- existing engineering book;
- portal search/navigation;
- generated object views;
- focused relation context;
- clickable real architecture;
- richer use-case workspace;
- direct authoritative source navigation;
- exact source/tool provenance through the normal documentation lifecycle.

The portal is derived output. It does not own requirements, architecture or
verification meaning.

## Step 6 — closing audit

Migration 013 completes only when:

- reusable owner capabilities are released;
- the event-timing canary pins released owner revisions;
- production-generated SVG exposes real diagram engineering IDs;
- the selected source slice has stable anchors and checked typed relations;
- book and portal are generated from the same authoritative source;
- no hand-maintained inverse matrices or diagram label maps are required;
- exact revisions/CI/publication evidence are retained here;
- optional versus required capabilities are explicitly documented;
- Experiment 007 remains available as a regression/reference lab.

## Initial owner sequence

```text
Experiment 007 — complete
        |
        v
Migration 013
        |
        +--> Step 1: tool.eng-docs diagram object_id
        |
        +--> Step 2: event-timing diagram canary
        |
        +--> Step 3: source anchors + compact metadata
        |
        +--> Step 4: reusable graph boundary
        |
        +--> Step 5: event-timing production portal
        |
        v
closing audit
```

The migration should stop and reassess if a production owner exposes a concrete
conflict with the qualified experiment assumptions rather than weakening those
assumptions silently.
