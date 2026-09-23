# Reusable repository documentation model

Status: **current shared convention**

## Purpose

Maintained reusable repositories should answer the same basic questions even
when their implementation domains differ.

The documentation model is organised around reader questions rather than around
repository type.

A reusable tool or library should make these questions easy to answer:

1. why does this repository exist;
2. why would I use it;
3. how is it put together;
4. how is it tested and qualified;
5. how do I develop and maintain it;
6. how do I use it as a consumer;
7. who are the typical users and use cases.

## Numbered backbone

The normal durable source-documentation set is:

```text
README.md
AGENTS.md
docs/ or doc/
├── 00-plan.md
├── 01-development.md
├── 10-specification.md
├── 20-design.md
├── 20-xx-...md          # optional design detail
├── 30-verification.md
├── 30-xx-...md          # optional verification detail
├── 40-usage.md
└── 40-xx-...md          # optional usage/reference detail
```

The repository may use `doc/` or `docs/` according to its established
family convention. Do not rename a whole repository tree merely for spelling
uniformity.

Not every optional detail file must exist. The numbered backbone exists to make
roles and reading order predictable, not to create empty documents.

## README and AGENTS

README and AGENTS are entrypoints, not parallel authorities.

### README

The README should let a new reader quickly understand:

- what the repository provides;
- who it is for;
- why they might use it;
- one representative example or normal entrypoint;
- where to read next.

It may contain a concise architecture picture or generated visual when that
material materially improves understanding.

Do not turn the README into the only maintained specification, architecture,
verification and usage manual.

### AGENTS

AGENTS explains how an agent should start work safely in that repository.

It should route to the plan, development guide and other owning documents plus
shared BrainboxEmb working guidance. Keep repository-specific constraints there
only when they are genuinely agent-facing.

## 00 — Plan

`00-plan.md` answers:

> What are we working on now, and what is the intended sequence?

Typical content:

- current scope and focus;
- information sources and authorities;
- open decisions;
- roadmap/milestones where useful;
- active owner work;
- links to specification, design, verification and development guidance.

The plan is operational and changes with current work.

It may summarize the repository purpose, but it does not own the durable
explanation of why the tool/library exists.

## 01 — Development

`01-development.md` answers:

> How do I develop, test, update, release and maintain this repository?

Typical content:

- local development entrypoints;
- prerequisites;
- normal edit/test loop;
- generated/managed files;
- dependency and version-update points;
- CI/reusable-workflow ownership;
- release procedure;
- repository-specific exceptions from shared working conventions.

This document is written for contributors and maintainers, not for consumers.

## 10 — Specification

`10-specification.md` answers three closely related questions:

> Why does this exist?

> Why would I use it?

> Who is it for?

Typical content:

- problem and purpose;
- target users / consumer types;
- representative use cases;
- value provided to those users;
- when the repository is the right choice;
- important non-goals / when it is not the right choice;
- desired behavior and compatibility constraints;
- major capabilities at intent level.

For a library, typical users may be other libraries and product/model
repositories.

For a tool, typical users may be repository maintainers, CI workflows, domain
tools or product repositories.

Do not turn specification into an API/CLI inventory. Exact invocation belongs
under usage/reference.

## 20 — Design

`20-design.md` answers:

> How is it put together?

Typical content:

- architecture and decomposition;
- ownership boundaries;
- modules/subsystems and their responsibilities;
- important data/control flow;
- major implementation choices and trade-offs;
- how the design supports the specification.

Use `20-xx-...` detail documents only where one subsystem carries enough
reasoning to justify a separate page.

## 30 — Verification

`30-verification.md` answers:

> How do we know it works?

Typical content:

- verification strategy;
- important risks/contracts being exercised;
- unit/integration/consumer/physical evidence as applicable;
- release qualification;
- testcase/evidence mapping;
- intentional exclusions and limitations.

Tests and generated evidence remain executable artifacts; the document explains
the strategy and interpretation.

Use `30-xx-...` for substantial verification detail rather than filling the
main page with every testcase implementation.

## 40 — Usage

`40-usage.md` answers:

> How do I use this tool or library?

It is consumer-facing.

Typical content:

- installation/consumption model;
- normal first example;
- common tasks;
- configuration entrypoints;
- compatibility/version-selection guidance;
- links to exact reference material.

The usage page should help a reader accomplish useful work before exposing every
implementation detail.

### 40-xx — Reference detail

Use `40-xx-...` for exact consumer contracts where useful, for example:

For a tool:

- CLI command reference;
- project/config schema;
- managed launcher contract;
- reusable GitHub workflows/actions;
- release/publication interfaces.

For a library:

- API family guidance;
- compatibility/migration notes;
- detailed consumer examples.

Generated or code-near API reference may remain beside source. `40-usage.md`
links to it rather than copying it.

## Mapping the seven reader questions

| Reader question | Primary authority |
| --- | --- |
| Why does it exist? | 10 specification |
| Why would I use it? | 10 specification |
| How is it put together? | 20 design |
| How is it tested? | 30 verification |
| How do I develop it? | 01 development |
| How do I use it? | 40 usage |
| Who are typical users? | 10 specification |

README gives a short orientation across the first, second, sixth and seventh
questions, then routes to the owning documents.

## Repository-type differences

The backbone is shared; emphasis differs.

### Reusable library

Libraries usually have:

- a strong specification around consumer semantics;
- design around API/implementation ownership;
- verification around behavior/geometry/compatibility;
- usage that teaches the public API;
- code-near/generated API reference where appropriate.

### Reusable tool

Tools usually have:

- specification around repository/maintainer problems and consumer roles;
- design around orchestration, ownership boundaries and execution flow;
- verification around owner tests, fixtures, cross-platform/consumer
  qualification and release interfaces;
- usage around CLI/config/launchers/reusable workflows;
- more `40-xx` reference detail than a typical library.

This is a difference in content, not a reason to lose the predictable reading
order.

## Evolution

Existing useful subject documents should be classified and retained, not
rewritten merely to satisfy filenames.

When adopting this model:

1. create the missing backbone authorities;
2. decide which existing documents are design, verification or usage/reference
   detail;
3. rename/relink detail documents only when the new name makes ownership clearer;
4. remove duplicated explanations once the owning authority exists;
5. keep released/historical evidence intact.

Do not force old experiment/PoP repositories into current documentation
maintenance unless they are deliberately reactivated.
