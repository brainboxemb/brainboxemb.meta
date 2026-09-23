# Software

This section is the portfolio-level view of the public software repositories.

It groups software projects, Java tooling and reusable CI/qualification work without moving implementation detail out of the repositories that own it.

Start with:

- [**Projects**](projects.md) — software planning and implementation repositories;
- [**Tooling and templates**](tooling.md) — generic repository tooling, Java project tooling and the Java reference template;
- [**Technical architecture**](architecture.md) — how repository selection, Java/Maven execution, qualification and publication fit together.

## The basic picture

The current software collection has several distinct roles:

```text
project coordination / architecture
        ↓
software implementation
        ↓
shared repository + Java tooling

qualification / PoP
        ↘ reusable evidence for shared CI design
```

The event-timing software meta-project owns its project-level planning and software architecture. The Java framework repository owns implementation. Shared lifecycle behaviour belongs in `tool.git-project` and `tool.java-project`.

The reusable Java CI Proof of Principle is separate again: it qualifies cross-project CI concepts and keeps reproducible regression cases. It is not a production dependency of normal software projects.

## Java is a technology inside the software domain

The current implementation stack is Java/Maven, so much of the shared software tooling is Java-specific. The domain itself is deliberately named **software** rather than **java** so that portfolio-level software architecture and future non-Java software work do not need a second parallel top-level domain merely because the implementation language changes.

The machine-readable repository catalog still records the narrower repository classification such as `domain: java` where that is useful.

## Where should I make a change?

A useful rule is:

- change product requirements, architecture or planning in the project repository that owns them;
- change Java framework/application implementation in the corresponding software repository;
- change shared Java build/test behaviour in `tool.java-project`;
- change generic repository orchestration in `tool.git-project`;
- reproduce and qualify reusable Java CI behaviour in `exp.2026-004.java-ci-architecture`;
- update this domain view when the portfolio-level relationship or navigation changes.

For the durable Java execution model, see [Java execution model](40-01_java-execution.md).
