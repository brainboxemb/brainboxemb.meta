# Project families, coordination and engineering documentation

## Why this document exists

brainboxemb projects can start as one repository and later grow into several implementation repositories, reusable tools and project-wide engineering documentation. Without a common model, each technology could invent its own meaning for `meta`, documentation ownership, generated output and lifecycle names.

This document defines the **preferred growth model across Java, embedded, CAD/SCAD and future domains**. Use it when deciding whether a project should remain one repository, when a coordination/meta repository is justified, where engineering documentation belongs, or how different build systems should stay recognisably aligned without being forced into identical mechanics.

The goal is consistency where it helps and separation where ownership/lifecycle genuinely differs.

## Core model

A non-trivial project family is split by **ownership**, not by programming language:

```text
project family
|
+-- coordination / meta repository
|     project direction, planning, requirements,
|     system/software architecture, verification strategy,
|     cross-repository decisions and closure evidence
|
+-- engineering-documentation capability
|     reusable diagrams, planning renderers, document assembly,
|     publication packaging and documentation provenance
|
+-- implementation-domain repositories
      Java / embedded / CAD / web / other concrete producers
      with their own build, test and runtime tooling
```

Implementation repositories can form dependency chains, but executable code does not automatically become the owner of project-wide planning or architecture.

## 1. Coordination / meta repository

A project-family coordination repository is justified when information genuinely spans implementation repositories or exists above a particular implementation technology.

Typical content:

- project purpose and scope;
- repository map and ownership boundaries;
- handoff/status and active implementation plan;
- requirements and use cases;
- system architecture and software-item architecture;
- cross-repository interface ownership;
- development/implementation planning;
- verification strategy and cross-component evidence;
- important architectural decisions and assumptions;
- release-backed closure where several repositories participate.

For event timing this role is currently:

```text
2026-010-01.meta.event-timing-software
```

`meta` therefore means **project-family coordination authority**, not “documentation that happens to accompany Java”.

## 2. Engineering documentation is a generic capability

Reusable documentation mechanics belong in `tool.eng-docs` and generic repository tooling, not in a language-specific build tool.

`tool.eng-docs` owns mechanisms such as:

- declarative engineering diagrams;
- diagram validation/rendering;
- generic planning/roadmap rendering;
- producer manifests;
- document assembly;
- documentation provenance and assembly metadata.

The project remains owner of the engineering meaning: labels, requirements, architecture decisions, planning content and project-specific configuration.

Generated documentation normally follows the shared generated-output lifecycle:

```text
pull request -> dev/pr-N/docs
main         -> prod/docs
release      -> rel/vX.Y.Z/docs
```

Publication is a repository side effect and remains outside language build semantics and cacheable producer graphs where publishing would falsify producer identity.

## 3. Implementation repositories own domain-specific producers

Each implementation domain owns only build/test/documentation producers that genuinely require that domain.

### Java

`tool.java-project` may own:

- JDK/Maven setup;
- Maven build/test execution;
- Java test/provenance evidence;
- JAR/application artifacts;
- Javadoc or another Java-derived artifact;
- Windows Java qualification.

It does **not** own:

- SDP/SIP/SVP project documents;
- system/software architecture books;
- generic diagram rendering;
- generic document assembly;
- project-family documentation publication semantics.

### Embedded

A future embedded domain may own:

- compiler/toolchain setup;
- firmware build/test;
- hardware-target evidence;
- binary/map/size reports;
- Doxygen or other source-derived output that genuinely requires C/C++/embedded tooling.

It should use the same top-level coordination/documentation model rather than invent an embedded-specific meta structure.

### CAD / SCAD

SCAD tooling owns geometry/render/export/verification producers. Engineering documentation may consume the produced images/evidence through manifests without becoming responsible for running OpenSCAD.

## 4. Source documentation versus generated documentation

Keep these stages distinct:

```text
authoritative engineering source
    Markdown, diagram YAML, planning data, requirements

implementation-derived documentation assets
    Javadoc, Doxygen, generated API reports, build/verification evidence

assembled documentation
    self-contained review/publication tree produced by tool.eng-docs

publication
    dev/prod/rel branch update or equivalent repository side effect
```

They may depend on each other, but they do not need the same runtime or owner.

A documentation-only change should not start Maven, Java, an embedded compiler or CAD runtime unless that documentation genuinely requires regeneration of an implementation-derived asset.

## 5. Producer/assembler contract

Preferred cross-repository flow:

```text
implementation producer
  -> artifact/evidence + producer manifest

meta/docs producer
  -> authored documentation + diagram/planning output

        both feed
           |
           v
     tool.eng-docs assemble
           |
           v
     assembled project documentation
           |
           v
     generic generated-output publication
```

The assembler consumes already-produced assets/provenance. It does not silently rerun Maven, OpenSCAD or an embedded build.

## 6. Repository topology: single repo by default, project family when justified

This is a **hybrid mono-/multi-repository model**.

Default preference:

- keep a simple project in one repository while source, planning, documentation, build and release still have one clear ownership/lifecycle boundary;
- split only when there is a real ownership, reuse, access-control, release-cadence, technology or cross-repository coordination boundary;
- introduce a meta repository when decisions/planning/requirements/qualification genuinely span multiple implementation repositories;
- do not create a meta repository merely because the model allows one.

A small CAD project can therefore remain one CAD repository with its own project documentation. It does **not** need a sibling meta repository by default.

A larger system may evolve naturally from:

```text
single implementation repository
```

to:

```text
meta / coordination
+ Java implementation
+ embedded implementation
+ CAD implementation
+ other component repositories
```

without changing the ownership principles.

Practical split signals:

- multiple implementation repositories need one shared plan/architecture;
- one repository is being forced to own decisions about another;
- reusable tools/libraries have an independent release lifecycle;
- public/private or access-control boundaries require separation;
- documentation must combine evidence from several producers;
- one runtime is being started only to build unrelated project-level documentation;
- repository size or CI coupling becomes materially harmful.

Absent such evidence, prefer the simpler single-repository shape.

A separate documentation source repository is also **not** the default. Keep project-family source documentation in meta when meta exists, otherwise in the owning project; keep code-near docs beside the implementation; split a dedicated docs repository only for a concrete ownership/access/lifecycle/size reason.

## 7. Cross-domain lifecycle equivalence

Different build systems should remain **recognisably equivalent where practical**, without pretending their mechanics are identical.

Preferred shared vocabulary:

```text
affected / preflight
    -> execute or materialize
    -> verify
    -> finalize / publish
    -> release qualification
```

Preferred shared concepts include:

- exact source/base identity;
- early unrelated-change stop;
- producer versus current materialization provenance;
- durable execution evidence;
- generated-output lifecycle `dev / prod / rel`;
- immutable released owner tooling before consumer rollout;
- thin consumers calling released reusable owner contracts.

Domain differences remain explicit:

- Java: Maven/JDK and selective native Windows qualification;
- SCAD: OpenSCAD/PythonSCAD runtime profiles and optional SCons target engine;
- embedded: compiler/linker/HIL/target-specific evidence as appropriate.

The rule is **same concept/name when the meaning is the same; different mechanism/name when the meaning really differs**. This keeps build systems in sync structurally without creating false uniformity.

## 8. Naming and numbering

Project numbering identifies related repositories; the repository role identifies ownership.

A family may evolve toward:

```text
<project>.meta.<system>        coordination / planning / architecture
<project>.java.<component>     Java implementation
<project>.embedded.<component> embedded implementation
<project>.cad.<component>      CAD implementation
```

Exact numbering remains project policy; `meta` stays technology-neutral.

## 9. Consequence for migrations

Execution-architecture migrations stop at their domain boundary.

A Java execution migration may optimize affected selection, JDK/Maven execution, Windows qualification and Java-derived artifacts/evidence, but should not absorb generic engineering-documentation assembly merely because a Java consumer also publishes documentation.

Cross-domain documentation/tooling improvements belong in generic engineering-documentation/repository tooling and can then be reused by Java, embedded, CAD and future domains.
