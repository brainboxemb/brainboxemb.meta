# Reusable repository documentation model

Status: **current shared convention**

## Purpose

Maintained engineering repositories should answer a predictable set of reader
questions without forcing every repository type into identical content.

A reusable tool or library should make these questions easy to answer:

1. why does this repository exist;
2. why would I use it;
3. how is it put together;
4. how is it tested and qualified;
5. how do I develop and maintain it;
6. how do I use it as a consumer;
7. who are the typical users and use cases.

The documentation reads like a small engineering book: overview, plan, manuals,
specification, design and verification.

## Numbered families

The normal source-documentation set is:

```text
README.md
AGENTS.md

docs/ or doc/
├── README.md
│
├── 10-00-plan.md
│
├── 20-00-manuals.md
├── 20-01-development.md
├── 20-02-user.md
├── 20-xx-...md             # optional additional manuals
│
├── 30-00-specification.md
│
├── 40-00-design.md
├── 40-xx-...md             # optional detailed design
│
├── 50-00-verification.md
└── 50-xx-...md             # optional verification detail
```

Generated documentation may additionally publish:

```text
bld/
└── docs/
    └── 99-00-book.md
```

Numbered source files use `<family>-<order>-<name>.md`: the first number identifies the document family, the second gives stable ordering inside that family, and the remaining kebab-case name is human-readable. Chapter 00 is the intentional exception: `README.md` is both the documentation overview and GitHub's directory landing page, so no duplicate `00-00_readme.md` is kept. Its alphabetical position in the file list is accepted; preserving GitHub's native README behavior and a single authority is more important than forcing it to sort first.

For example:

```text
20-00-manuals.md
20-01-development.md
20-02-user.md
20-10-git-workflow.md

40-00-design.md
40-01-repository-layout.md
40-02-publication-model.md
```

Do not assign a new top-level category merely because one subject grows. Add a
subdocument to the owning family.

The repository may use `doc/` or `docs/` according to its established family
convention. Do not rename an entire tree merely for spelling uniformity.

## README convention for documentation collections

Every directory that acts as a maintained documentation collection or navigation
boundary keeps a local `README.md`.

Examples:

```text
docs/
├── README.md
├── 10-00-plan.md
├── 20-00-manuals.md
└── ...

doc/
├── README.md
├── 10-00-plan.md
├── 20-00-manuals.md
└── ...

domains/scad/
├── README.md
└── ...
```

That `README.md` is the local overview/index and acts as chapter 00 for that
collection. Do not keep a parallel `00-00_readme.md`.

Its alphabetical position in GitHub's file list is accepted. Preserving native
GitHub README rendering and one clear authority is more important than forcing
the overview to sort first.

This rule applies to actual documentation collections. It does **not** require a
new README in every source-adjacent directory that happens to contain one design
document or generated artifact. For example, a component-local
`design/design.md` may remain a single focused authority when that directory is
not intended as a navigable documentation set.

## Root README and AGENTS

The root `README.md` and `AGENTS.md` remain repository entrypoints rather
than parallel technical authorities.

### Root README

The root README should quickly answer:

- what is this repository;
- why might I care;
- who normally uses it;
- one representative way to use or inspect it;
- where should I read next.

Keep it useful on GitHub.

### AGENTS

AGENTS explains how an agent should start work safely and routes to the owning
documents plus shared BrainboxEmb guidance.

Do not copy complete plans, manuals or technical contracts into AGENTS.

## 00 — Overview

`README.md` is the front page of the documentation set and acts as chapter 00.

It answers:

> What documentation exists, who is it for, and how should I read it?

Typical content:

- concise repository/documentation overview;
- intended audiences;
- document map and reading order;
- links to generated/reference material;
- links to domain-specific material where applicable.

It is the overview chapter. It should not become a second full root README.

## 10 — Plan

`10-00-plan.md` answers:

> What are we working on now, and what is the intended sequence?

Typical content:

- current scope and focus;
- information sources and authorities;
- open decisions;
- active owner work;
- phases, milestones and roadmap where useful.

The plan is operational and changes with current work.

## 20 — Manuals

`20-00-manuals.md` is the manual-family entrypoint.

It answers:

> Which practical manuals exist for this repository?

A normal reusable repository starts with:

### 20-01 — Development

`20-01-development.md` answers:

> How do I develop, test, update, release and maintain this repository?

It is written for contributors and maintainers.

Typical content:

- local development entrypoints and prerequisites;
- edit/test loop;
- generated and managed files;
- dependency/version update points;
- CI/reusable-workflow ownership;
- release procedure;
- local exceptions.

### 20-02 — User

`20-02-user.md` answers:

> How do I use this tool or library?

It is consumer-facing.

Typical content:

- installation/consumption model;
- first useful example;
- common tasks;
- configuration entrypoints;
- version-selection/compatibility guidance;
- links to exact API/CLI/config/workflow reference.

### Additional manuals

Use stable `20-xx` numbers for other practical guidance that genuinely belongs
to the manual family.

Examples:

```text
20-10-engineering-workflow.md
20-11-git-workflow.md
20-12-versioning-and-releases.md
```

A manual tells someone **what to do**. Architecture rationale belongs in design.

## 30 — Specification

`30-00-specification.md` answers:

> Why does this exist?

> Why would I use it?

> Who is it for?

Typical content:

- problem and purpose;
- target users / consumer types;
- representative use cases;
- value provided;
- when the repository is the right choice;
- important non-goals;
- desired behavior and compatibility constraints;
- major capabilities at intent level.

Do not turn specification into an API/CLI inventory.

## 40 — Design

`40-00-design.md` is the design-family entrypoint and answers:

> How is it put together?

Typical content:

- architecture and decomposition;
- ownership boundaries;
- modules/subsystems and responsibilities;
- important data/control flow;
- implementation choices and trade-offs.

Use stable `40-xx` detail documents for substantial design areas:

```text
40-00-design.md
40-01-repository-layout.md
40-02-tooling-boundary.md
40-03-publication-model.md
```

For geometry-heavy SCAD components, component-local visual design
documentation may remain beside source and be linked from the repository design.

## 50 — Verification

`50-00-verification.md` is the verification-family entrypoint and answers:

> How do we know it works?

Typical content:

- verification strategy;
- risks/contracts being exercised;
- unit/integration/consumer/physical evidence as applicable;
- release qualification;
- testcase/evidence mapping;
- acceptance criteria;
- intentional exclusions and limitations.

Use `50-xx` for substantial verification detail.

## 99 — Combined documentation book

`99-00-book.md` is optional **generated output**.

It assembles the maintained source documents in numeric reading order:

```text
README / overview
10 plan
20 manuals + 20-xx
30 specification
40 design + 40-xx
50 verification + 50-xx
```

The normal location is `bld/docs/99-00-book.md` or an equivalent generated Build
namespace. It is never hand-maintained or treated as a source authority.

A renderer may later produce HTML/PDF from the same ordered source set.

## Mapping the reader questions

| Reader question | Primary authority |
| --- | --- |
| Where do I start? | README / overview |
| What are we working on? | 10 plan |
| How do I develop/maintain it? | 20-01 development manual |
| How do I use it? | 20-02 user manual |
| Why does it exist? | 30 specification |
| Why would I use it? | 30 specification |
| Who are typical users? | 30 specification |
| How is it put together? | 40 design |
| How is it tested? | 50 verification |

## Repository-type differences

The numbered families are shared; the contents differ by repository type.

### Reusable library

Libraries commonly emphasize:

- user manual around normal API usage;
- specification around consumer semantics/use cases;
- design around API/implementation ownership;
- verification around behavior/geometry/compatibility;
- generated/code-near API reference linked from the user manual.

### Reusable tool

Tools commonly emphasize:

- development manual around owner tests, release lifecycle and workflow
  maintenance;
- user manual around CLI/configuration/managed launchers/reusable workflows;
- specification around repository/maintainer problems and consumer roles;
- design around orchestration and ownership boundaries;
- verification around fixtures, cross-platform behavior and released interfaces.

Tools may therefore have more manual subdocuments than libraries. That is an
expected specialization, not a different documentation model.

## Meta and domain documentation

A coordination/meta repository can use the same top-level families.

Portfolio-wide practical working rules belong under `20-xx` manuals; portfolio
architecture belongs under `40-xx` design documents.

Technology/domain-specific guidance may remain under a domain directory when it
would be misleading to present it as portfolio-wide policy.

This allows, for example, a SCAD or software domain to mature independently
without turning the general meta documentation into a technology-specific
collection.

## Evolution

Existing useful subject documents should be classified and retained, not
rewritten merely to satisfy filenames.

When adopting this model:

1. create the missing family entrypoints;
2. classify existing documents as manual, specification, design or
   verification material;
3. assign stable subnumbers inside the owning family;
4. move domain-specific material to the relevant domain rather than keeping it
   in a generic bucket;
5. update links and remove obsolete parallel indexes;
6. keep historical migration/experiment evidence intact;
7. generate `99-00-book.md` only after source structure is coherent.

Do not force completed experiment/PoP repositories into current documentation
maintenance unless they are deliberately reactivated.
