# SCAD documentation structure

Status: **current shared documentation convention**

## Purpose

Current-generation SCAD repositories use one predictable documentation model,
but that model must not create documents for their own sake.

Each document role answers a different question:

```text
README / AGENTS     where do I start?
00 plan             how do we work here and what is happening now?
10 specification    why does this exist and what should it achieve?
20 design           how is the repository/system organised to achieve that?
21..29 detail       how is one functional part built in detail?
30 verification     how do we know the intended result is achieved?
source/API docs     how do I call the public API?
```

The normal repository-level shape is:

```text
README.md
AGENTS.md
doc/
├── 00-plan.md
├── 10-specification.md
├── 20-design.md
├── 21-...md               # optional detailed design
├── 22-...md               # optional detailed design
├── ...
├── 30-verification.md
└── 40-...md               # other optional subject documents

vrf/
└── ... executable verification sources and generated evidence
```

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

### AGENTS

AGENTS is the agent-facing start page. Keep:

- genuinely agent-specific instructions;
- the minimum repository context needed to start safely;
- links to shared policy and repository authorities.

Do not duplicate the plan, specification, design or verification procedure in
AGENTS merely to make it visible to an agent.

A fact or rule should have one clear authority. A short orienting summary is
fine; parallel maintained copies are not.

## 00 — Plan

`doc/00-plan.md` is the normal engineering/work entrypoint after README or
AGENTS.

It is operational. Typical content includes:

- a short statement of the repository/library/project goal and scope;
- repository-specific working method;
- information sources and which questions they are authoritative for;
- applicable shared BrainboxEmb guidance from `brainboxemb.meta`, including the portfolio agent entrypoint, generic Git workflow and domain conventions;
- current focus and implementation sequence;
- dependencies, decision points and open questions;
- phases or milestones;
- an optional roadmap;
- links to the specification, design, detailed design and verification.

The plan may summarize the goal so a maintainer knows what they are working on,
but the durable explanation of **why** the library/project and its functional
parts exist belongs in the specification.

For current-generation repositories, the information-sources section should make
shared dependencies explicit rather than assuming an agent already knows the
portfolio. A SCAD repository will normally point to `brainboxemb.meta/AGENTS.md`
and the relevant SCAD coding/document/source guidance, plus its pinned tooling
AGENTS where tool-specific behavior matters.

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

Readable headings remain the default:

```text
Why semantic resolution exists
Why coordinate frames are separate from simple rotations
What Forge deliberately does not replace
```

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

## 21..29 — Detailed design

Detailed-design documents are optional. Add one when a functional area has
enough internal reasoning that keeping it inside `20-design.md` would make the
architecture document noisy.

Examples:

```text
doc/21-resolution-context.md
doc/22-transform-model.md
doc/23-cutter-overlap.md
```

Detailed design answers questions such as:

- how one module/function family is internally composed;
- local control/data flow;
- scope/lifetime behavior;
- geometry construction sequence;
- algorithms and transformations;
- private-helper responsibilities;
- implementation edge cases and rationale.

Do not create all `21..29` files pre-emptively. Create only the detailed
designs that carry useful engineering knowledge.

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

doc/21-...md
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

`vrf/` owns executable verification material and generated evidence, for
example:

```text
vrf/
├── openscad/
│   └── verification_evidence.scad
└── out/
    ├── README.md
    ├── png/
    ├── evidence/
    └── ...
```

Temporary machine artifacts may exist during execution but should not be
published merely because a testcase generated them.

A published verification snapshot may include a copy of the applicable
verification document so the evidence branch is self-contained, but the source
authority remains `doc/30-verification.md`.

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
21..29 detail       internal design of complex functional areas when useful
30 verification     how intended behavior is demonstrated
API reference       exact consumer-facing calls
```

### CAD application/project

```text
00 plan             work context, sources, focus, phases/roadmap
10 specification    why the product/design exists; goals/requirements/constraints
20 design           assembly/model architecture and major design choices
21..29 detail       optional non-visual detailed design topics
component docs      detailed visual construction where useful
30 verification     product/design verification strategy
```

## Evolution

Existing repositories are not wrong merely because they predate this structure.

Templates/reference repositories should demonstrate the convention after a
coherent rollout decision. Existing projects/libraries should adopt it when the
documents carry useful knowledge rather than through ceremonial file creation.
