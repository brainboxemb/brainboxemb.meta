# Shared engineering workflow

This page is the durable portfolio-wide working model for engineering changes in
BrainboxEmb repositories.

Repository-local documentation remains authoritative for the thing being
changed. This page explains how to find and combine that local information with
shared portfolio guidance.

## Start from the owning repository

For work in any repository, begin with:

1. `README.md` — human-facing repository orientation;
2. `AGENTS.md` — agent-facing local navigation and exceptions;
3. the repository plan when present, normally `doc/00-plan.md`;
4. the source/design/specification/verification documents relevant to the
   change.

Do not reconstruct durable project knowledge from chat history when the owning
repository already documents it.

## Then load shared BrainboxEmb guidance

The portfolio-wide agent entrypoint is
[`brainboxemb.meta/AGENTS.md`](../../AGENTS.md).

From there, load only the shared material relevant to the task:

- [Git and repository workflow](git-workflow.md) for issues, branches, commits,
  PRs, CI, changelog and merge discipline;
- [project organisation](projects.md) for generic project/tool ownership;
- [versioning and releases](versioning-and-releases.md) for released interfaces
  and consumer pins;
- the applicable domain entrypoint under `domains/`;
- [STATUS.md](../../STATUS.md) when the work spans repositories or relates to an
  active/proposed migration, experiment or PoP.

A local repository plan should identify the shared **entrypoints** relevant to
that repository. It should not duplicate the complete list of downstream shared
documents when the shared entrypoint already routes to them.

## AGENTS do not inherit through dependencies

An `AGENTS.md` file describes how an agent should work **in the repository that
owns that file**.

A consumer does not automatically inherit the `AGENTS.md` instructions of a
pinned tool or library dependency. In particular, dependency-owner commit/PR
rules must not override the consumer repository's working conventions.

When a consumer needs to understand the exact behavior of a pinned dependency,
use the documentation and source from that **pinned dependency revision**:

```text
consumer working method
    -> current brainboxemb.meta/AGENTS.md
    -> consumer-local AGENTS / plan

exact dependency behavior
    -> consumer config + exact gitlink
    -> pinned dependency README / docs / source / tests
```

A pinned dependency may link to current portfolio guidance for contribution
conventions, but current moving guidance must not be required to reconstruct the
technical behavior of an old pinned release.

## Use the current repository as source of truth

For implementation work, current live repository state takes precedence over
old plans, old chat summaries or assumptions.

Inspect, as applicable:

- current source and configuration;
- current README/AGENTS/numbered docs;
- open issues and pull requests;
- exact dependency pins;
- current CI runs and retained evidence;
- generated output when it is part of the review.

Historical migrations and experiments are evidence and rationale. They do not
override the current owner repository unless a current document explicitly
still adopts that contract.

## Keep ownership explicit

Make the change in the repository that owns the behavior.

Typical ownership split:

- project/product-specific design or behavior → project repository;
- reusable API/geometry → owning library;
- generic repository mechanics → `tool.git-project`;
- domain build/runtime behavior → domain tool such as `tool.scad-project` or
  `tool.java-project`;
- portfolio-wide convention/coordination → `brainboxemb.meta`;
- experiment fixtures/evidence → experiment repository.

A problem first observed in one consumer is not automatically a shared-tooling
problem. Prefer a local correction unless the behavior is already a shared
contract or evidence shows multiple consumers need the same mechanism.

## Work from intent to evidence

For non-trivial work, keep this order visible:

```text
why / intended result
        ↓
design / implementation choice
        ↓
code or geometry
        ↓
verification / evidence
        ↓
review and merge
```

Do not weaken a valid testcase merely to make CI green. If a test exposes a bad
design, fix the design or update the intended contract explicitly.

## Cross-repository work

When one logical task spans repositories:

1. identify the owner of each change;
2. keep one coherent change/branch/PR per owner;
3. qualify the owner change before advancing consumers where practical;
4. release reusable interfaces before normal production consumers adopt them;
5. use `brainboxemb.meta` for portfolio-wide coordination and durable shared
   convention changes.

Do not mix implementation into meta merely because the work was discovered
while coordinating there.

## Cross-project work tracks

If the task is a migration, experiment, PoP or other repository-spanning track,
read [STATUS.md](../../STATUS.md) first.

Do not guess the active migration/experiment number from history. Derive the
current track from live coordination state.

A proposed/inactive track does not start automatically.

## Evidence and completion

Completion should be supported by the strongest practical evidence for the
change, such as:

- exact source revision;
- passing owner CI;
- relevant generated output;
- physical verification;
- exact consumer qualification;
- post-merge main verification;
- immutable release/tag evidence when a reusable interface is released.

Documentation changes alone do not prove an implementation or migration is
complete.

## Avoid duplicated authorities

README and AGENTS are entrypoints. Plans, specifications, designs, coding
standards and verification documents are durable authorities.

When shared guidance exists in meta, repository-local documentation should link
to it and record only genuine local additions or exceptions.
