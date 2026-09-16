# Project families, coordination and engineering documentation

This page defines the preferred cross-domain structure for a brainboxemb project that spans multiple repositories or implementation technologies.

The model is deliberately **not Java-specific**. A Java application, embedded firmware, CAD project, desktop client or later implementation domain should be able to participate in the same project family without changing the top-level coordination/documentation architecture.

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

The implementation repositories can themselves form a dependency chain, but they do not become the owner of the project-level planning/document model merely because they contain executable code.

## 1. Coordination / meta repository

The project-family coordination repository is the authority for information that spans implementation repositories or exists before a particular implementation is chosen.

Typical content includes:

- project purpose and scope;
- repository map and ownership boundaries;
- handoff/status and active implementation plan;
- requirements and use cases;
- system architecture and software-item architecture;
- interface ownership across repositories;
- software-development and implementation planning;
- verification strategy and cross-component qualification evidence;
- important architectural decisions and assumptions;
- release-backed step closure where several repositories participate.

For the event-timing software project this role is currently fulfilled by:

```text
2026-010-01.meta.event-timing-software
```

The word `meta` therefore means **project-family coordination authority**, not "documentation that happens to accompany Java".

## 2. Engineering documentation is a generic capability

Reusable documentation mechanics belong in `tool.eng-docs` and generic repository tooling, not in a language-specific build tool.

`tool.eng-docs` owns mechanisms such as:

- declarative engineering diagrams;
- diagram validation/rendering;
- planning/roadmap rendering where generic;
- producer manifests;
- document assembly;
- documentation provenance and assembly metadata.

The project repository remains owner of the actual engineering meaning: labels, requirements, architecture decisions, planning content and project-specific scripts/configuration.

Generated documentation follows the normal generated-output lifecycle rather than being committed back into the source branch:

```text
pull request -> dev/pr-N/docs
main         -> prod/docs
release      -> rel/vX.Y.Z/docs
```

Documentation publication is a repository side effect. It remains outside language build semantics and outside cacheable producer graphs where publication would falsify producer identity.

## 3. Implementation repositories own domain-specific producers

Each implementation repository owns only the build/test/documentation producers that genuinely require that implementation domain.

Examples:

### Java

`tool.java-project` may own:

- JDK/Maven setup;
- Maven build/test execution;
- Java test/provenance evidence;
- JAR/application artifacts;
- Javadoc or another artifact that genuinely requires Java source/tooling;
- Windows Java compatibility.

It should **not** own:

- the project SDP/SIP/SVP;
- system/software architecture books;
- generic diagram rendering;
- generic document assembly;
- project-family documentation publication semantics.

### Embedded

A future embedded tool/domain may own:

- compiler/toolchain setup;
- firmware build/test;
- hardware-target evidence;
- binary/map/size reports;
- Doxygen or other source-derived output when it genuinely requires the embedded/C/C++ producer.

It should consume the same coordination and engineering-documentation model as Java rather than inventing an embedded-specific meta structure.

### CAD / SCAD

SCAD tooling owns geometry/render/export/verification producers. Engineering documentation can consume the produced images/evidence through manifests without becoming responsible for running OpenSCAD.

## 4. Source documentation versus generated documentation

The architecture distinguishes four things that are often incorrectly bundled together:

```text
authoritative engineering source
    Markdown, YAML diagram source, planning data, requirements

implementation-derived documentation assets
    Javadoc, Doxygen, generated API reports, build/verification evidence

assembled documentation
    self-contained review/publication tree produced by tool.eng-docs

publication
    dev/prod/rel branch update or equivalent repository side effect
```

These stages may depend on each other, but they do not need the same runtime or owner.

A documentation-only change should therefore not start Maven, a Java runtime, an embedded compiler or a CAD runtime unless the changed documentation explicitly requires regeneration of an implementation-derived asset.

## 5. Producer/assembler contract

The preferred cross-repository contract is producer based:

```text
implementation producer
  -> artifact/evidence + producer manifest

meta/docs producer
  -> project-authored documentation + diagram/planning output

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

The assembler consumes already-produced assets and provenance. It does not silently rerun Maven, OpenSCAD or an embedded build.

This allows one documentation set to include material from several implementation domains without coupling the documentation workflow to all of their toolchains.

## 6. Repository topology: single repo by default, project family when justified

This is a **hybrid mono-/multi-repository model**, not a rule that every project must become a repository family.

Default preference:

- keep a simple project in one repository while source, planning, documentation, build and release still have one clear ownership/lifecycle boundary;
- split repositories only when there is a real boundary in ownership, reuse, access control, release cadence, implementation technology or cross-repository coordination;
- introduce a coordination/meta repository when decisions, planning, requirements or qualification genuinely span multiple implementation repositories;
- do not create a meta repository merely because the architecture allows one.

A small CAD project can therefore remain a single CAD repository with its own project documentation. It does **not** need a sibling meta repository by default.

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

without changing the top-level ownership principles.

Practical split signals include:

- more than one implementation repository needs one shared plan/architecture;
- one repository is being forced to own decisions about another repository;
- reusable tooling or libraries develop an independent release lifecycle;
- public/private or access-control boundaries require separation;
- generated documentation must combine evidence from several producers;
- one technology/runtime is being started only to build unrelated project-level documentation;
- repository size or CI coupling becomes materially harmful.

Absent such evidence, prefer the simpler single-repository shape.

This model also does **not** require a separate documentation source repository for every project.

Default documentation preference:

- keep project-family planning/requirements/architecture source in the coordination/meta repository when such a repository exists;
- otherwise keep that source in the owning project repository;
- keep code-near implementation documentation in the implementation repository that owns it;
- assemble/publish combined engineering documentation as generated output when needed;
- create a separate documentation source repository only when ownership, access control, lifecycle or repository size gives a concrete reason.

A dedicated `*.docs.*` repository should therefore be an evidence-backed split, not the default architecture.

## 7. Naming and numbering

Project numbering identifies related repositories, while the repository role identifies ownership.

A family may therefore evolve toward a shape such as:

```text
<project>.meta.<system>        coordination / planning / architecture
<project>.java.<component>     Java implementation
<project>.embedded.<component> embedded implementation
<project>.cad.<component>      CAD implementation
```

Exact naming/number allocation remains project policy; the architectural rule is that `meta` stays technology-neutral.

## 8. Consequence for migrations

Execution-architecture migrations should stop at their domain boundary.

For example, a Java execution migration may optimize:

- affected selection;
- JDK/Maven execution;
- Windows qualification;
- Java-derived artifacts/evidence;

but should not absorb generic engineering-documentation assembly merely because the current Java consumer also happens to publish documentation.

Cross-domain documentation/tooling improvements belong in the generic engineering-documentation/tooling track and can then be reused by Java, embedded, CAD and future domains.
