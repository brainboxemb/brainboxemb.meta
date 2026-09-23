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

The document set is ordered like a small engineering book: orientation first,
then current work, then practical manuals, then intent, design and verification.

## Numbered backbone

The normal source-documentation set is:

```text
README.md                    # repository/GitHub entrypoint
AGENTS.md                    # agent entrypoint

docs/ or doc/
├── 00-readme.md
├── 10-plan.md
├── 20-development-manual.md
├── 21-user-manual.md
├── 30-specification.md
├── 40-design.md
├── 40-xx-...md             # optional design detail
├── 50-verification.md
└── 50-xx-...md             # optional verification detail
```

Generated documentation may additionally publish:

```text
bld/
└── docs/
    └── 99-book.md
```

The repository may use `doc/` or `docs/` according to its established family
convention. Do not rename a complete repository tree merely for spelling
uniformity.

The numbered source files are authorities. `99-book.md` is generated output,
not another maintained authority.

## Root README and AGENTS

The root `README.md` and `AGENTS.md` remain repository entrypoints.

### Root README

The root README should quickly answer:

- what is this repository;
- why might I care;
- who normally uses it;
- what is one representative way to use or inspect it;
- where should I read next.

Keep it useful on GitHub. Do not turn it into the only maintained plan,
specification, design, verification and user manual.

### AGENTS

AGENTS explains how an agent should start work safely in that repository and
routes to the owning documents plus shared BrainboxEmb guidance.

Do not copy complete plans, manuals or technical contracts into AGENTS.

## 00 — Documentation README

`00-readme.md` is the front page of the documentation set.

It answers:

> What documentation exists, who is it for, and in what order should I read it?

Typical content:

- a concise repository/documentation overview;
- intended audiences;
- document map and reading order;
- links to the plan, manuals, specification, design and verification;
- links to important generated/reference material.

It may repeat a very short orientation from the root README, but should not
become a second full repository README.

## 10 — Plan

`10-plan.md` answers:

> What are we working on now, and what is the intended sequence?

Typical content:

- current scope and focus;
- information sources and authorities;
- open decisions;
- active owner work;
- phases, milestones and roadmap where useful;
- links to the durable manuals/specification/design/verification documents.

The plan is operational and changes with current work.

## 20/21 — Manuals

The manual family explains how people actually work with the repository.

### 20 — Development manual

`20-development-manual.md` answers:

> How do I develop, test, update, release and maintain this repository?

Typical content:

- local development entrypoints and prerequisites;
- normal edit/test loop;
- generated and managed files;
- dependency/version update points;
- CI/reusable-workflow ownership;
- release procedure;
- repository-specific exceptions from shared working conventions.

It is written for contributors and maintainers.

### 21 — User manual

`21-user-manual.md` answers:

> How do I use this tool or library?

It is consumer-facing.

Typical content:

- installation/consumption model;
- first useful example;
- normal/common tasks;
- configuration entrypoints;
- version-selection and compatibility guidance;
- links to exact API/CLI/config/workflow reference.

For a tool, this may lead to CLI, schema, launcher and reusable-workflow
reference.

For a library, this may lead to generated/code-near API reference and focused
examples.

A repository that genuinely has no external/operator-facing usage surface may
keep this page very small, but reusable tools and libraries should normally have
one.

## 30 — Specification

`30-specification.md` answers:

> Why does this exist?

> Why would I use it?

> Who is it for?

Typical content:

- problem and purpose;
- target users / consumer types;
- representative use cases;
- value provided to those users;
- when the repository is the right choice;
- important non-goals and when it is not the right choice;
- desired behavior and compatibility constraints;
- major capabilities at intent level.

Do not turn specification into an API/CLI inventory.

## 40 — Design

`40-design.md` answers:

> How is it put together?

Typical content:

- architecture and decomposition;
- ownership boundaries;
- modules/subsystems and their responsibilities;
- important data/control flow;
- major implementation choices and trade-offs;
- how the design supports the specification.

Use `40-xx-...` detail documents only when a subsystem carries enough
engineering reasoning to justify its own page.

For geometry-heavy SCAD components, component-local visual design documentation
may remain beside the owning geometry rather than being mechanically moved into
this family.

## 50 — Verification

`50-verification.md` answers:

> How do we know it works?

Typical content:

- verification strategy;
- important risks/contracts being exercised;
- unit/integration/consumer/physical evidence as applicable;
- release qualification;
- testcase/evidence mapping;
- acceptance criteria;
- intentional exclusions and limitations.

Tests and generated evidence remain executable artifacts; the document explains
their strategy and interpretation.

Use `50-xx-...` for substantial verification detail.

## 99 — Combined documentation book

`99-book.md` is an optional **generated** reading artifact.

It concatenates or renders the maintained source documents in their intended
order, for example:

```text
00-readme
10-plan
20-development-manual
21-user-manual
30-specification
40-design
40-xx details
50-verification
50-xx details
```

The combined book should normally be produced into `bld/docs/` or another
generated Build namespace. It should not be hand-edited or treated as a source
authority.

A future renderer may also produce HTML/PDF from the same ordered source set.
The source Markdown files remain authoritative.

## Mapping the reader questions

| Reader question | Primary authority |
| --- | --- |
| Where do I start? | 00 documentation README |
| What are we working on? | 10 plan |
| How do I develop/maintain it? | 20 development manual |
| How do I use it? | 21 user manual |
| Why does it exist? | 30 specification |
| Why would I use it? | 30 specification |
| Who are typical users? | 30 specification |
| How is it put together? | 40 design |
| How is it tested? | 50 verification |

## Repository-type differences

The numbered backbone is shared; emphasis differs.

### Reusable library

Libraries commonly emphasize:

- specification around consumer semantics and use cases;
- user manual around normal API usage;
- design around API/implementation ownership;
- verification around behavior/geometry/compatibility;
- generated or code-near API reference linked from the user manual.

### Reusable tool

Tools commonly emphasize:

- development manual around owner tests, release lifecycle and workflow
  maintenance;
- user manual around CLI/configuration/managed launchers/reusable workflows;
- specification around repository/maintainer problems and supported consumer
  roles;
- design around orchestration and ownership boundaries;
- verification around owner fixtures, cross-platform behavior and released
  interfaces.

The content differs; the reading order stays predictable.

## Evolution

Existing useful subject documents should be classified and retained, not
rewritten merely to satisfy filenames.

When adopting this model:

1. add the missing numbered backbone;
2. classify existing documents as manual, design detail, verification detail or
   consumer/reference detail;
3. rename/relink existing detail documents only when the new name improves
   discoverability;
4. remove duplicated explanations once the owning authority exists;
5. keep historical/released evidence intact;
6. generate `99-book.md` only after the source set is coherent.

Do not force completed experiment/PoP repositories into current documentation
maintenance unless they are deliberately reactivated.
