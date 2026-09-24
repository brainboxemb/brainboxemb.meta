# Git and repository workflow

This page records shared Git/repository working conventions for BrainboxEmb
repositories. Repository-local rules may add constraints, but should link here
rather than copy this page.

## Issue before implementation when the work is durable

Use an issue when the change benefits from a durable problem statement,
especially for:

- API or behavior changes;
- non-trivial bug fixes;
- architecture/documentation convention changes;
- work spanning multiple commits or repositories;
- follow-up/removal work such as deprecations.

Tiny editorial fixes do not require ceremonial issue creation.

## Branches

Follow the owning repository's established branch naming when one exists.

Prefer a branch that clearly connects to the issue or purpose, for example:

```text
feature/issue-24-deprecate-res-apply
fix/issue-...
docs/issue-...
```

Do not invent a new naming convention in a consumer when the owner already has
one.

### GitHub Actions workflow naming

When adding or renaming files under `.github/workflows/`, use the portfolio-wide
workflow naming convention owned by
[How the shared tools fit together](40-03-repository-tooling.md#github-actions-workflow-filenames).

That page is the single authority for the `self-`, `reusable-` and `test-`
filename categories, workflow display names and the required Purpose/Scope
header. Do not duplicate that naming table in consumer repositories.

## Commits

A commit should represent one coherent reviewable change.

Prefer:

- one meaningful commit for a small focused PR;
- a small number of commits when separate review steps are genuinely useful;
- commit messages that describe the change, not the editing mechanism.

Avoid:

- one commit per file merely because an API/tool writes files separately;
- repeated corrective micro-commits when the corrections can be batched before
  pushing;
- mixing unrelated repository-owner changes in one commit.

When tooling allows it, prepare the complete tree and push one coherent commit.

## Pull requests

Use a PR as the normal review/qualification boundary for protected production
branches.

A PR description should explain:

- the problem or goal;
- the intended change;
- important design/compatibility choices;
- verification/evidence;
- related issue(s).

Use draft state while a substantial change is still intentionally incomplete.
Make it ready when the branch itself is ready for review/merge.

## CI discipline

After pushing a coherent branch update:

1. inspect the exact run for that head SHA;
2. diagnose failures from logs/evidence;
3. batch related corrections where practical;
4. avoid superseding broad workflow runs with avoidable micro-pushes.

A green run should correspond to the exact revision being considered for merge.

For visual/generated evidence, CI success alone is not sufficient when human
inspection is part of the verification question. Inspect the generated result.

## Changelog

Repositories that maintain a `CHANGELOG.md` should record meaningful
user-visible or repository-contract changes under `Unreleased`.

Examples:

- public API additions/deprecations/removals;
- behavior changes;
- meaningful documentation structure changes;
- generated-resource/publication changes.

Do not add changelog noise for whitespace or typo-only fixes.

Released entries are historical records; later corrections belong under
`Unreleased`, not by rewriting the released section.

## Merge

Before merge, check:

- expected PR head SHA is still the qualified revision;
- required CI/evidence is green;
- documentation/changelog are consistent with the final branch;
- no known WIP is accidentally presented as complete.

Use the repository's normal merge strategy. For repositories using squash
merges, merge against the expected head SHA rather than an unverified moving
branch state.

After merge, verify that the expected main-branch CI/publication run starts and
finishes successfully when the repository lifecycle requires it.

## Releases and reusable interfaces

A reusable library/tool API consumed by other repositories is a production
interface.

Normal adoption order:

```text
owner implementation
    ↓
qualified owner PR
    ↓
merged exact main
    ↓
exact-main verification
    ↓
immutable release/tag
    ↓
deliberate consumer update
```

Do not normally update production consumers to an unreleased moving owner
`main`.

See [Versioning and releases](versioning-and-releases.md) for the complete
release/pinning model.

## Multi-repository changes

Keep each repository's Git history self-contained:

- issue/branch/PR in the owner repository;
- implementation evidence in that owner;
- consumer update in a separate consumer PR;
- portfolio coordination in meta when needed.

This makes rollback, review and evidence understandable without relying on chat
history.
