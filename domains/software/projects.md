# Software projects

The current public software project family is the event-timing software project.

## Project coordination and architecture

[`2026-010-01.meta.event-timing-software`](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software)

This repository owns project-level software planning, system/software architecture and coordination between implementation repositories.

It is a project repository, not a replacement for `brainboxemb.meta`: `brainboxemb.meta` coordinates portfolio-wide work, while this repository coordinates the event-timing software project itself.

## Java framework implementation

[`2026-010-02.java.event-timing-framework`](https://github.com/brainboxemb/2026-010-02.java.event-timing-framework)

This repository owns the reusable Java framework implementation for the project. It uses the current shared Java project infrastructure supplied by `tool.java-project`.

Project-specific implementation, tests, packaging and releases stay here rather than in the shared tooling repository.

## Shared qualification is separate

[`exp.2026-004.java-ci-architecture`](https://github.com/brainboxemb/exp.2026-004.java-ci-architecture) is not a product project. It is the reusable qualification/regression environment for Java CI architecture.

Use it when a CI concept or defect can be represented as a reproducible cross-project testcase before changing production tooling or a production consumer.
