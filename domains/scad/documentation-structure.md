# SCAD documentation structure

Status: **current shared documentation convention**

## Purpose

Current-generation SCAD repositories specialize the shared
[reusable repository documentation model](../../docs/working-model/repository-documentation.md).
The same reader questions and numbered backbone apply, with SCAD-specific
visual/API conventions layered on top. The model must not create documents for
their own sake.

Each document role answers a different question:

```text
README / AGENTS     where do I start?
00 plan             how do we work here and what is happening now?
10 specification    why does this exist and what should it achieve?
20 design           how is the repository/system organised to achieve that?
20-xx detail        how is one functional part built in detail?
30 verification     how do we know the intended result is achieved?
40 usage            how do I consume/use this repository?
01 development      how do I work in and maintain this repository?
source/API docs     exact public API reference
```

The normal repository-level shape is:

```text
README.md
AGENTS.md
doc/
├── 00-plan.md
├── 01-development.md
├── 10-specification.md
├── 20-design.md
├── 20-01-...md            # optional detailed design
├── 20-02-...md            # optional detailed design
├── ...
├── 30-verification.md
└── 40-usage.md

vrf/
└── ... executable verification sources and generated evidence
```

The second number keeps detailed design inside the design family and scales
without reserving only a handful of filenames. This is intentionally similar to
the hierarchical numbering already used in larger BrainboxEmb engineering
documentation sets.

The numbered files are source documentation. `vrf/` is execution/evidence,
not a second source-documentation tree.

## Standard entrypoints

`README.md` and `AGENTS.md` are the two standard entrypoints.

### README

The README is the human-facing start page. Keep enough introduction to answer:

- what is this repository;
- why might I care;
- where should I read next.

Route the reader to the owning documents instead of duplicating them.

For visual CAD repositories, a short README does **not** mean a text-only
README. Include one or a few representative generated renders when they let a
reader understand the model or product substantially faster than prose alone.
Prefer stable generated Build/Verification output over committed duplicate
images on `main`.

Do not remove an existing useful preview merely to make the README more
"minimal".

### AGENTS

AGENTS is the agent-facing start page. Keep:

- genuinely agent-specific instructions;
- the minimum repository context needed to start safely;
- links to shared policy and repository authorities.

Do not duplicate the plan, specification, design or verification procedure in
AGENTS merely to make it visible to an agent.

Repository-local AGENTS files should route to the current
`brainboxemb.meta/AGENTS.md` shared entrypoint. Dependency AGENTS files are not
inherited by consumers; exact pinned dependency behavior is read from the pinned
dependency's consumer-facing README/docs/source.

A fact or rule should have one clear authority. A short orienting summary is
fine; parallel maintained copies are not.

## 00 — Plan

`doc/00-plan.md` is the normal engineering/work entrypoint after README or
AGENTS.

It is operational. Typical content includes:

- a short statement of the repository/library/project goal and scope;
- repository-specific working method;
- information sources and which questions they are authoritative for;
- applicable shared BrainboxEmb **entrypoints** from `brainboxemb.meta`;
- current focus and implementation sequence;
- dependencies, decision points and open questions;
- phases or milestones;
- an optional roadmap;
- links to the specification, design, detailed design and verification.

The plan may summarize the goal so a maintainer knows what they are working on,
but the durable explanation of **why** the library/project and its functional
parts exist belongs in the specification.

For a current-generation SCAD repository the plan should normally make these
routes discoverable without duplicating every shared page:

```text
shared working guidance
    -> brainboxemb.meta/AGENTS.md

shared SCAD-domain guidance
    -> brainboxemb.meta/domains/scad/README.md

exact tool/library behavior
    -> local config + exact gitlink + pinned dependency README/docs/source
```

Do not create a separate roadmap document by default. A normal roadmap is a
section of the plan unless its size/lifecycle genuinely justifies separation.

## 10 — Specification

`doc/10-specification.md` primarily answers **why**.

It should help a reader understand the engineering intent before looking at
architecture or source.

Typical content includes:

- the problem the repository/library/project is intended to solve;
- goals and desired outcomes;
- important non-goals;
- why each major functional area, sub-library or capability exists;
- what those capabilities are intended to mean to a user/consumer;
- important requirements and constraints at the intent level.

For example, a modeling library specification can explain **why semantic
resolution is needed** and what problem it prevents. It should not immediately
turn that idea into an implementation inventory of `$fn/$fa/$fs`, helper
modules or private data flow; those belong in design/detail/API documentation.

### Numbering and requirement identifiers

Document numbering exists for navigation and reading order.

Do **not** automatically name specification headings with identifiers such as
`FORGE-GEN-01`, `RES-CTX-02`, and so on. That creates noise when the reader
only needs a clear explanation.

Use a stable requirement identifier only when one individual requirement
genuinely benefits from independent traceability, for example because physical
or automated verification must refer to it exactly.

Readable headings remain the default.

## 20 — Design

`doc/20-design.md` answers **how at architecture level**.

Typical content includes:

- major decomposition and responsibilities;
- sub-libraries/modules and how they interact;
- public versus internal ownership;
- coordinate/data/control flow at system level;
- major implementation choices and trade-offs;
- how the architecture supports the intent from the specification.

The design document should stay understandable without descending into every
private helper or geometry operation.

Keep architecture concrete while doing so. Tie abstractions back to real
components, files, views, public objects or representative generated images
where that makes the design easier to read. A design document should not become
a vocabulary of layers and boundaries that requires the reader to already know
the repository.

## 20-xx — Detailed design

Detailed-design documents are optional. Add one when a functional area has
enough internal reasoning that keeping it inside `20-design.md` would make the
architecture document noisy.

Examples:

```text
doc/20-01-resolution-context.md
doc/20-02-transform-model.md
doc/20-03-cutter-overlap.md
...
doc/20-20-...
```

Detailed design answers questions such as:

- how one module/function family is internally composed;
- local control/data flow;
- scope/lifetime behavior;
- geometry construction sequence;
- algorithms and transformations;
- private-helper responsibilities;
- implementation edge cases and rationale.

Do not create detailed-design files pre-emptively. Create only the documents
that carry useful engineering knowledge.

### Component-local detailed design

For geometry-heavy components, the established component-local
`design/design.md` plus its interactive design-render adapter may be the
better detailed-design form because the explanation is inherently visual.

The relationship can therefore be:

```text
doc/10-specification.md
    why the library/project or capability exists

doc/20-design.md
    repository/system architecture

doc/20-01-...md
    detailed design of a functional software/modeling area

<component>/design/design.md
    detailed visual construction of a physical component
```

Do not mechanically move useful visual component documentation into `doc/`.

## 30 — Verification

`doc/30-verification.md` is source documentation. It explains how we determine
whether the specification/design intent is actually satisfied.

Typical content includes:

- verification risks and questions;
- the specification/design section being exercised;
- machine versus human evidence;
- testcase/evidence mapping;
- acceptance criteria;
- evidence interpretation;
- intentional exclusions and limitations;
- physical verification procedures where applicable.

Prefer links to clear specification/design headings. Use requirement IDs only
where the requirement itself genuinely needs a stable identifier.

## vrf — execution and evidence

`vrf/` owns executable verification material and generated evidence.

A published verification snapshot may include a copy of the applicable
verification document so the evidence branch is self-contained, but the source
authority remains `doc/30-verification.md`.

## 01 — Development and maintenance

`doc/01-development.md` is the repository-local operating manual for a
maintainer/developer.

It answers practical questions that do not belong in the engineering plan,
product/library specification or architecture design:

- what should I open or run for normal development in this repository;
- which dependency/tool versions are selected locally and where they are changed;
- which root launchers are managed rather than hand-maintained;
- which GitHub Actions callers exist and why;
- what build/verification/release path is normal here;
- what repository-specific deviations from the shared SCAD convention exist.

The local document should stay concise and link to the shared
[SCAD repository development guide](repository-development.md) for generic
bootstrap/update/workflow/version-management rules.

Unlike the plan, this page is not primarily about current work or roadmap. It is
the durable "how to work in this repo" page.

Current-generation maintained SCAD repositories should normally have this
document even when the repository otherwise needs only minimal documentation.

Additional operating detail can remain in a clearly named optional subject document when it genuinely deserves its own page. The main `01-development.md` remains the repository-local operating entrypoint.

## 40 — Usage

`doc/40-usage.md` is the consumer-facing guide.

For a reusable SCAD library it should explain the normal include/use model,
show a small useful example, describe the main API families and route to the
code-near/generated API reference.

For a CAD application/project, a separate usage page is optional unless the
repository has a meaningful reusable/operator-facing interface. Do not invent a
consumer manual for a one-off design merely for symmetry.

The shared repository documentation model owns the generic role; this SCAD
convention adds only the domain-specific expectations above.

## API/reference documentation

API/reference documentation is code-near and answers **how do I call it?**

For reusable OpenSCAD libraries, keep API documentation beside the owning
source and generate the reference with `openscad_docsgen` where appropriate.

API/reference documentation is also the natural place for:

- exact function/module signatures;
- parameters and return values;
- focused call examples;
- compatibility/deprecation notices.

Do not make the specification an API catalog.

## Libraries and applications

The same roles apply to both, with different emphasis.

### Reusable library

```text
00 plan             work context, sources, focus, roadmap
10 specification    why the library/capabilities exist; goals/non-goals
20 design           library architecture and responsibilities
20-xx detail        internal design of complex functional areas when useful
30 verification     how intended behavior is demonstrated
40 usage            how a consumer uses the library
01 development      how to develop, update and release this repository
API reference       exact consumer-facing calls
```

### CAD application/project

```text
00 plan             work context, sources, focus, phases/roadmap
10 specification    why the product/design exists; goals/requirements/constraints
20 design           assembly/model architecture and major design choices
20-xx detail        optional non-visual detailed design topics
component docs      detailed visual construction where useful
30 verification     product/design verification strategy
01 development      local development/update/release operating guide
```

## Evolution

Existing repositories are not wrong merely because they predate this structure.

Migration 010 qualifies and rolls this model through current-generation SCAD
repositories before the template is treated as the settled reference.
