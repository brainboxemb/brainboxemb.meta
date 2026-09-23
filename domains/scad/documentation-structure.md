# SCAD documentation structure

Status: **current shared SCAD specialization**

## Shared model

Current-generation maintained SCAD repositories specialize the shared
[reusable repository documentation model](../../docs/working-model/repository-documentation.md).

The normal SCAD library documentation set is:

```text
README.md
AGENTS.md

doc/
├── 00-readme.md
├── 10-plan.md
├── 20-manuals.md
├── 20-01-development.md
├── 20-02-user.md
├── 20-xx-...md
├── 30-specification.md
├── 40-design.md
├── 40-xx-...md
├── 50-verification.md
└── 50-xx-...md
```

The first number identifies the family; the second number is a stable detail
inside that family.

Not every optional detail page is required.

## Root README

The root README remains the GitHub-facing start page.

For visual CAD repositories it may and often should contain one or a few
representative generated renders when they explain the library or design faster
than prose.

Prefer stable generated Build/Verification output over committed duplicate
screenshots where practical.

Do not remove an existing useful preview merely to make a README shorter.

## 00 — Overview

`doc/00-readme.md` is the documentation front page.

For a reusable SCAD library it should briefly state:

- what the library provides;
- typical consumers/use cases;
- how the numbered documents are organised;
- where generated or source-adjacent API reference lives;
- where useful Build/Verification output can be found.

## 10 — Plan

`doc/10-plan.md` owns current repository work, information sources, focus,
sequence and roadmap.

Durable engineering intent belongs in specification rather than being repeated
as plan history.

## 20 — Manuals

`doc/20-manuals.md` is the manual-family index.

### 20-01 — Development

`doc/20-01-development.md` explains how to work on the repository itself.

For current-generation maintained SCAD repositories it should cover:

- normal edit/build/verify workflow;
- dependency and tool version-selection points;
- managed bootstrap/update launchers;
- GitHub Actions caller files and their roles;
- release procedure where applicable;
- repository-specific exceptions.

Shared SCAD repository maintenance mechanics live in
[repository-development.md](repository-development.md); the local manual gives
the repo-specific summary.

### 20-02 — User

`doc/20-02-user.md` teaches a consumer how to use the library/tool/project.

For a reusable SCAD library it normally contains:

- normal `use` / `include` model;
- one small useful example;
- main public API families;
- compatibility/version guidance;
- links to generated or code-near API reference.

For a one-off CAD project without a meaningful operator/consumer interface, the
user manual may be short or omitted when it would add no useful information.

### Additional SCAD manuals

Use `20-xx` only for durable practical guidance that really needs its own page.

Examples might include:

- migration/compatibility instructions for consumers;
- a specialized release/manual verification procedure.

Do not put architecture rationale in a manual merely because it is operationally
important.

## 30 — Specification

`doc/30-specification.md` explains:

- why the library/project exists;
- why a consumer would use it;
- typical users and use cases;
- goals and desired behavior;
- important non-goals and constraints.

Do not make specification an API catalog.

## 40 — Design

`doc/40-design.md` owns repository/system architecture.

Use `40-xx` for detailed non-visual design topics such as resolution context,
transform behavior or cutter semantics.

### Component-local visual design

Geometry-heavy components may keep detailed visual construction documentation
beside source, for example:

```text
<component>/design/design.md
```

with generated/interactive design-render adapters.

That is a SCAD-specific detailed-design form. The repository-level
`40-design.md` links to those component-local authorities instead of moving
them merely for numbering symmetry.

## 50 — Verification

`doc/50-verification.md` explains how intended behavior/design is validated.

Typical SCAD evidence includes:

- executable OpenSCAD/PythonSCAD verification;
- generated STL/PNG/SVG evidence;
- geometry assertions;
- consumer compilation/render checks;
- physical testcases where geometry requires human/physical confirmation.

`vrf/` owns executable verification material and generated evidence. A
published verification snapshot may include the applicable verification document
for self-contained review, but source authority remains in `doc/`.

Use `50-xx` for substantial verification procedures/details.

## API/reference documentation

Exact public API reference remains code-near.

For reusable OpenSCAD libraries, keep source/API documentation beside the owning
source and generate reference with `openscad_docsgen` where appropriate.

The user manual links to that reference. Specification and design should not
duplicate signatures/parameter catalogs.

## Generated combined book

A future `bld/docs/99-book.md` may assemble the numbered source documentation
in reading order.

It is generated output, not a source authority.

## Libraries versus projects

The same numbered families apply with different emphasis.

### Reusable library

```text
00 overview
10 plan
20 manuals
  20-01 development
  20-02 user/API guidance
30 specification
40 design + optional details
50 verification
source/API reference beside code
```

### CAD application/project

```text
00 overview
10 plan
20 manuals
  20-01 development
  20-02 operator/user guide only when meaningful
30 specification
40 design + component-local visual details
50 verification
```

## Evolution

Existing current-generation SCAD repositories are migrated to this model as
part of the current baseline/documentation refresh.

Preserve useful content. Renumber and classify it rather than rewriting history
for filename symmetry.
