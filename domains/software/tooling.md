# Software tooling and templates

The software repositories use a layered tooling model so generic repository behaviour and Java-specific behaviour stay separate.

## Generic repository tooling

[`tool.git-project`](https://github.com/brainboxemb/tool.git-project)

Owns generic repository setup and orchestration behaviour, including shared dependency/bootstrap mechanics, Moon-based capability selection and generated-output support.

It should not need to understand the Maven lifecycle internally.

## Java project tooling

[`tool.java-project`](https://github.com/brainboxemb/tool.java-project)

Owns reusable Java/Maven project behaviour: canonical build/test execution, Java evidence, Windows qualification policy and Java generated-output finalization.

Maven remains the Java build/test semantic authority.

## Java reference template

[`template.java-project`](https://github.com/brainboxemb/template.java-project)

A minimal external consumer of the released generic and Java tooling. It provides an immutable reference for the intended project setup without becoming the owner of shared lifecycle behaviour.

## Reusable CI qualification

[`exp.2026-004.java-ci-architecture`](https://github.com/brainboxemb/exp.2026-004.java-ci-architecture)

A reusable Proof of Principle and qualification repository for Java CI architecture, incremental builds, caching and affected execution.

It owns fixtures, declarative testcases, harnesses, candidate adapters and qualification results. Cross-project conclusions and production decisions are coordinated from `brainboxemb.meta`.

## Related cross-domain tooling

[`tool.eng-docs`](https://github.com/brainboxemb/tool.eng-docs) is domain-neutral engineering-document tooling. Software projects can consume it, but it is not part of the Java build stack.

For the general repository-tooling split, see [How the shared tools fit together](../../docs/40-03_repository-tooling.md).
