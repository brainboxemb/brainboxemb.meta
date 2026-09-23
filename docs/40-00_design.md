# Meta design

## Repository architecture

The repository is split by information ownership:

```text
root entrypoints
  README / AGENTS / STATUS
        |
        +-- docs/              general numbered portfolio documentation
        |
        +-- domains/           technology/domain specializations
        |
        +-- repositories/      public catalog/inventory
        |
        +-- migrations/        cross-repository rollout records
        |
        +-- experiments/       PoP/experiment records
        |
        +-- dashboard/         live status implementation
```

The general numbered documents describe portfolio-wide behavior. A domain owns
shared knowledge that would be misleading as a portfolio-wide rule.

Operational registers such as STATUS, migrations and experiments intentionally
remain outside the numbered book because they have a different lifecycle.

## Detailed design

- [40-01 — Project families](40-01-project-families.md)
- [40-02 — Projects](40-02-projects.md)
- [40-03 — Repository tooling](40-03-repository-tooling.md)
- [40-04 — Generated output](40-04-generated-output.md)

Domain-specific execution models belong in their domain, for example the
[software Java execution model](../domains/software/40-01-java-execution.md).

## Ownership principle

Implementation stays with the repository that owns the behavior. Meta explains
and coordinates ownership; it does not become a central implementation monolith.
