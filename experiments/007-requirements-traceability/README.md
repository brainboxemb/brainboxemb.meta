# Experiment 007 — interactive engineering documentation and traceability

Status: **complete — qualified for production adoption; retained as review/regression lab**

Tracking issue: [#167](https://github.com/brainboxemb/brainboxemb.meta/issues/167)

Implementation/evidence repository:
[`brainboxemb/exp.2026-007.requirements-traceability`](https://github.com/brainboxemb/exp.2026-007.requirements-traceability)

Human review site:
[Experiment 007 GitHub Pages](https://brainboxemb.github.io/exp.2026-007.requirements-traceability/)

Final owner issue:
[`exp.2026-007.requirements-traceability#15`](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/issues/15) — complete

Reference project:
`brainboxemb/2026-010-01.meta.event-timing-software`

Production adoption:
[Migration 013](../../migrations/013-interactive-engineering-documentation/README.md)

First reusable mechanism owner:
`brainboxemb/tool.eng-docs`

## Question

How can BrainboxEmb engineering documentation become easier to understand,
navigate and verify as systems grow, while preserving readable project Markdown
and the useful linear engineering book?

Requirements traceability is one part of this question, not the complete target.

## Target architecture

Experiment 007 treats the engineering content as one knowledge model with
several views:

```text
                         engineering knowledge
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
       v                          v                          v
  readable book             documentation portal       engineering explorer
  ordered narrative         search/navigation          object/relationship views
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
                           traceability checks
```

The views must not become independently maintained copies of the same use case,
requirement, architecture element or verification case.

## Qualified so far

### Step 01 — target experience

The experiment retained these distinct reader needs:

- **Book** — coherent ordered reading/review/print view;
- **Portal** — search, breadcrumbs, stable deep links and fast navigation;
- **Clickable architecture** — diagram elements navigate to engineering objects;
- **Object view** — one engineering object with generated relationships/backlinks;
- **Focused graph** — bounded local relationship navigation;
- **Workspace** — related contexts remain visible side-by-side;
- **Traceability/CI** — machine-checkable IDs, relations and coverage.

### Step 02 — minimal engineering graph

A dependency-free graph baseline qualified:

- stable object IDs/types;
- typed relations;
- generated backlinks;
- duplicate/unknown-link/type validation;
- coverage rules;
- focused breadth-first traversal.

This remains the control contract for later engines.

### Step 03 — Sphinx-Needs comparison

Sphinx-Needs qualified as a strong candidate for relationship modelling,
validation/backlinks and machine-readable `needs.json` export.

The experiment also found that built-in flow traversal is not automatically the
same as the desired exact focused-graph semantics; the project-independent graph
contract remains the authority for that interaction.

Sphinx-Needs is therefore a viable engine, not the documentation architecture by
itself.

### Step 04 — Material portal/workspace

Material for MkDocs qualified as a strong reader-facing portal candidate for:

- search/navigation;
- breadcrumbs/deep links;
- generated object pages;
- static hosting;
- a thin custom two-pane engineering workspace.

The existing engineering book remains a separate first-class output rather than
being moved into MkDocs.

The qualified responsibility split is currently:

```text
project engineering source
        |
        v
engineering graph / validation
        |
        +----------------------+
        |                      |
        v                      v
tool.eng-docs Book        Material portal
                             |
                             +--> object pages
                             +--> focused graph
                             +--> thin workspace
```

### Step 05 — real Markdown authoring

A 19-object real event-timing slice compared:

- native MyST/Sphinx-Needs directives;
- normal Markdown with compact adjacent metadata;
- normal Markdown with separate sidecar metadata.

Qualified findings:

1. **real upstream sources are broader than use cases** — SAD/SVP document
   sections can legitimately source requirements;
2. **stable engineering ID does not automatically mean stable source deep
   link** — current bold SI01/IF03 requirement titles need an explicit anchor
   convention;
3. **relations should be authored once** — use-case/architecture/verification
   backlinks and matrices are generated;
4. native MyST is technically strong but too invasive as the default authored
   form for normal GitHub/Markdown review;
5. sidecar metadata is technically clean but creates avoidable synchronization
   and drift risk;
6. **compact project-owned metadata adjacent to ordinary Markdown is the
   selected authoring direction for the next PoP**.

The exact compact metadata syntax remains experimental.

## Step 06 — clickable real architecture and richer use cases

The final bounded PoP used the real SI-01 layered architecture and real use-case
narrative. It qualified:

- diagram elements carrying the same engineering object IDs as the graph;
- architecture → object → use-case navigation without a parallel lookup table;
- `TimingNode` navigation into `UC-001` and `UC-014`;
- side-by-side real use-case + architecture context at realistic scale;
- direct links back to authoritative source objects;
- an optional diagram `object_id` preserved into generated SVG as the smallest
  reusable `tool.eng-docs` mechanism.

The Step-06 fixture was refreshed to current event-timing main
`d6f629093e865a7fc33c9adbaaad7e66a5510751` and its matching generated
`prod/docs` architecture output before final review.

Human review on 28 September 2026 accepted the clickable architecture/workspace
direction. No additional UX PoP is required before production adoption.

## Ownership

`brainboxemb.meta` owns:

- the cross-project question and active sequencing;
- retained conclusions/evidence;
- the decision whether a later production adoption/migration should start.

The experiment repository owns:

- isolated fixtures;
- PoP implementations;
- executable qualification cases;
- generated experiment evidence and the human review site.

The event-timing coordination repository remains owner of its requirements,
architecture, interfaces, verification and documentation meaning.

`tool.eng-docs` remains a possible later production owner for generic
extraction, graph/validation, diagram-identity and publication mechanisms. It is
not the experiment implementation owner.

## Production decision

Experiment 007 is complete.

The qualified production direction is handed to
[Migration 013](../../migrations/013-interactive-engineering-documentation/README.md).

The experiment repository remains retained as:

- executable qualification evidence;
- a human review surface;
- a regression lab for future graph/navigation/documentation changes.

Production implementation must happen in the normal owners. The experiment
repository is not a production dependency.
