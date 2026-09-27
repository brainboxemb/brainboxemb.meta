# Experiment 007 — interactive engineering documentation and traceability

Status: **active — target experience and candidate architecture first**

Tracking issue: [#167](https://github.com/brainboxemb/brainboxemb.meta/issues/167)

Implementation/evidence repository:
[`brainboxemb/exp.2026-007.requirements-traceability`](https://github.com/brainboxemb/exp.2026-007.requirements-traceability)

Current owner issue:
[`exp.2026-007.requirements-traceability#1`](https://github.com/brainboxemb/exp.2026-007.requirements-traceability/issues/1)

Reference project:
`brainboxemb/2026-010-01.meta.event-timing-software`

Possible later production mechanism owner:
`brainboxemb/tool.eng-docs`

## Question

How can BrainboxEmb engineering documentation become easier to understand,
navigate and verify as systems grow, while preserving readable project Markdown
and the useful linear engineering book?

Requirements traceability is one part of this question, not the complete target.

The event-timing project already has:

- a generated architecture book;
- system use cases;
- software-item requirements;
- architecture and detailed design;
- interface definitions;
- verification planning/cases;
- stable engineering identifiers such as `UC-001`, `SI01-REQ-020`,
  `IF03-REQ-004` and `VC-ST1-001`.

The experiment starts from the reader/author experience before selecting
technology.

## Target experience

The experiment evaluates several views over one engineering knowledge base:

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

Desired capabilities include:

- **Book** — coherent ordered reading/review/print view;
- **Portal** — search, breadcrumbs, stable deep links and contextual navigation;
- **Clickable architecture** — diagram elements navigate to engineering objects;
- **Object view** — one component/use case/requirement/interface/test with its
  generated relationships/backlinks;
- **Focused graph** — bounded local relationship navigation around one selected
  object;
- **Workspace** — related views side-by-side so context is not constantly lost;
- **Traceability/CI** — machine-checkable IDs, relations and coverage.

These should be views, not independent copies of engineering content.

## First phase

The implementation/evidence repository first defines:

1. the target documentation experience;
2. evaluation criteria;
3. a candidate architecture/tool responsibility split;
4. a bounded event-timing reference slice.

No documentation/traceability product is selected in advance.

Current candidates/references include:

- Sphinx-Needs for requirements/relationship modelling and validation;
- Material for MkDocs for portal/navigation experience;
- Structurizr for the model-versus-views architecture principle;
- Antora as a multi-repository/versioned documentation reference;
- a small custom explorer where the desired Object/Focused Graph/Workspace
  experience is more specific than an existing portal provides.

Another candidate is added only when it offers a materially different answer to
a real qualification question.

## Qualification direction

After the target architecture is reviewed, the PoP should qualify the smallest
central contract first:

```text
small readable source fixture
        |
        v
engineering graph
        |
        +--> validate IDs/links/coverage
        +--> machine-readable export
        +--> object/backlink view
        +--> focused relation query
        +--> stable source links
```

Only then should the experiment build a portal/view prototype.

The existing event-timing project is a read-only reference during this phase.

## Ownership

`brainboxemb.meta` owns:

- the cross-project question and active sequencing;
- retained conclusion/evidence;
- the decision whether production adoption/migration should start.

The experiment repository owns:

- target-experience and candidate research;
- isolated fixtures;
- PoP implementations;
- executable qualification cases;
- generated experiment evidence.

The event-timing coordination repository remains owner of its requirements,
architecture, interfaces, verification and documentation meaning.

`tool.eng-docs` is only a possible later production owner of generic mechanisms.
It is not the experiment implementation owner.

## Decision outcomes

Experiment 007 may conclude with a combined architecture rather than one tool.

A valid result can:

- adopt a bounded existing traceability engine behind a project-independent
  interchange model;
- use a dedicated portal technology while retaining `tool.eng-docs` for book
  assembly;
- add a small explorer for the interaction model not provided by the portal;
- implement a smaller generic `tool.eng-docs` graph/validation capability;
- retain more manual traceability if automation cost exceeds the benefit.

Completion does not automatically create or activate a production migration.
