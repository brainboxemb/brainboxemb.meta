# SCAD documentation structure

Status: **current shared documentation convention**

## Purpose

Current-generation SCAD repositories use one predictable source-documentation
home. Different kinds of engineering information have different jobs; a
single "design" document should not become a catch-all.

The normal repository-level shape is:

```text
README.md
AGENTS.md
doc/
├── 00-plan.md
├── 10-specification.md
├── 20-design.md
├── 30-verification.md
└── 40-...md

vrf/
└── ... executable verification sources and generated evidence
```

Number ordered source documents in increments of 10 so later material can be
inserted without broad renumbering.

The structure is role-based, not ceremonial. A repository does not need every
optional document merely to satisfy the tree.

## Standard entrypoints

`README.md` and `AGENTS.md` are the two standard entrypoints.

### README

The README is the human-facing start page. It should contain only enough
introduction to answer:

- what is this repository;
- why might I care;
- where should I read next.

It routes the reader to the owning source documents instead of repeating their
content.

### AGENTS

AGENTS is the agent-facing start page. It should contain:

- only genuinely agent-specific instructions;
- the minimum repository context needed to start safely;
- links to the applicable shared policy and repository source documents.

Do not duplicate the repository plan, engineering contracts, design rationale
or verification procedure in AGENTS merely to make them visible to an agent.
Point to their authority.

A fact or rule should have one clear authority. A short summary is acceptable
when it materially improves navigation, but parallel maintained copies are not.

## 00 — Plan

`doc/00-plan.md` is the normal engineering/work entrypoint after README or
AGENTS.

It explains what the repository/library/project is for, what belongs in its
scope, how work is intended to proceed and where the relevant information
lives.

Typical content includes:

- **purpose** — why the repository/library/project exists and what problem it
  serves;
- **scope** — what belongs here and what explicitly belongs elsewhere;
- repository-specific working method;
- information sources and their authority, such as drawings, STEP files,
  datasheets, upstream APIs or other local documents;
- current focus and implementation sequence;
- dependencies, decision points and known open questions;
- phases or milestones;
- an optional roadmap section;
- links to specification, design, verification and external authoritative
  sources.

The plan is operational, not a second specification. It links to normative
contracts instead of copying them and links to verification rules instead of
restating them.

Do not create a separate roadmap document by default. Keep a normal roadmap as
a section of `00-plan.md`; split it only when its scale or lifecycle genuinely
justifies an independent document.

## 10 — Specification

`doc/10-specification.md` turns the plan's purpose and scope into precise
engineering promises and constraints.

Typical content includes:

- terminology;
- requirements;
- public or semantic contracts;
- externally visible invariants;
- constraints and boundaries;
- compatibility expectations.

For a reusable library this is where semantic contracts such as context
ownership, coordinate meaning, token behavior and API invariants belong.

For a CAD application/project it records the requirements and constraints the
design must satisfy.

Stable contract identifiers are useful when verification should point back to
one exact promise, for example:

```text
RES-CTX-01
RES-CTX-02
```

## 20 — Design

`doc/20-design.md` explains **how** the specification is realised.

Typical content includes:

- architecture and decomposition;
- geometry construction;
- coordinate systems;
- internal data flow;
- implementation choices;
- trade-offs;
- reusable versus project-owned responsibilities.

A design document should refer back to specification contracts where that
improves traceability rather than repeating the contract text.

### Component-local visual design documents

Existing component-local `design/design.md` walkthroughs remain useful for
complex physical geometry. They can show named views and explain the
construction of one component step by step.

Their role is narrower than repository-level specification/design:

```text
doc/10-specification.md
    repository/library/product contracts

doc/20-design.md
    repository-level architecture/design

<component>/design/design.md
    detailed visual construction of that component
```

Do not mechanically rename existing component walkthroughs solely to satisfy
the repository-level numbering convention.

## 30 — Verification

`doc/30-verification.md` is source documentation. It explains how relevant
specification and design claims are proven.

Typical content includes:

- verification risks and questions;
- mapping from specification/design claims to tests or evidence;
- machine versus human evidence;
- acceptance criteria;
- evidence interpretation;
- intentional exclusions and limitations;
- physical verification procedure where applicable.

For contract-heavy libraries, prefer explicit traceability:

| Contract | Verification question | Test/evidence |
| --- | --- | --- |
| `RES-CTX-01` | Does the public resolution owner establish context for its child geometry? | resolution-context testcase |
| `RES-CTX-04` | Does the context stop at the child boundary? | leakage/restoration testcase |

The verification document belongs under `doc/`, not under `vrf/`.

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

API/reference documentation is separate from plan, specification, design and
verification.

For reusable OpenSCAD libraries, keep API documentation next to the owning
source and generate the reference with `openscad_docsgen` where appropriate.

Use the layers as follows:

```text
README / AGENTS     where do I start?
00 plan             why does this repo exist and how do we work here?
10 specification    what does it promise?
20 design           how is that promise realised?
30 verification     how is the promise proven?
source/API docs     how do I call the API?
```

Do not copy the same explanation into all layers.

## Libraries and applications

The same document roles apply to both, with different emphasis.

### Reusable library

```text
00 plan             purpose, scope, information sources, evolution/roadmap
10 specification    public concepts and semantic contracts
20 design           internal architecture and implementation
30 verification     contract proof strategy
API reference       code-near generated reference
```

### CAD application/project

```text
00 plan             purpose, scope, sources, working method, phases/roadmap
10 specification    requirements, constraints and external interfaces
20 design           assemblies, geometry and implementation
30 verification     product/design verification strategy
component docs      detailed visual construction where useful
```

## Evolution

This convention describes the target documentation roles. Existing
current-generation repositories are not automatically wrong because they
predate it.

Template/reference repositories should demonstrate the convention after a
separate rollout decision. Existing projects/libraries should move through a
coherent migration or when the structure materially helps the work, rather than
through ad-hoc one-file renames.
