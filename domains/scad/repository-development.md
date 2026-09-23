# Developing and maintaining a current-generation SCAD repository

Status: **current shared maintainer guide**

## Purpose

This page is the operating guide for maintained current-generation SCAD
repositories. The technical architecture explains how the shared system works;
this guide explains what a maintainer actually changes and which changes are
managed automatically.

A repository keeps a short local `doc/40-development.md` with its own
entrypoints, dependency set, workflow set and exceptions. That local document
links here for the shared rules.

## Normal repository surface

A maintained current-generation SCAD repository normally exposes:

```text
project.yml
project.scad.yml

bootstrap.ps1
bootstrap.sh
update.ps1
update.sh

tools/
├── tool.git-project
└── tool.scad-project

.github/workflows/
├── scad.yml
├── release.yml        # when this repository publishes versioned releases
└── pr-cleanup.yml     # when PR preview output is published

doc/
└── 40-development.md
```

Libraries and projects may add domain-specific files and workflows, but shared
repository/SCAD lifecycle logic belongs in released tooling rather than being
copied into every consumer.

## Which version is changed where?

### tool.git-project

`tool.git-project` is the bootstrap engine. It is intentionally not an ordinary
`project.yml` dependency.

Its exact version is the committed gitlink:

```text
tools/tool.git-project
```

Upgrading it is a deliberate maintainer operation:

1. choose an accepted released `tool.git-project` version;
2. move `tools/tool.git-project` to the exact released commit;
3. review the changed parent gitlink;
4. run the canonical updater so managed launchers are refreshed from that exact
   tool revision;
5. commit the gitlink plus refreshed launchers together.

A root launcher never decides to advance the bootstrap-tool gitlink itself.

### tool.scad-project

The desired SCAD-tool release is declared in `project.yml`:

```yaml
dependencies:
  - name: tool.scad-project
    role: tooling
    type: git-submodule
    path: tools/tool.scad-project
    ref: vX.Y.Z
```

The maintainer changes the semantic `ref`. The generic updater then resolves
that ref and records the exact revision through the gitlink.

The SCAD post-update hook aligns brainboxemb-owned SCAD reusable-workflow calls
to the same semantic release ref. A maintainer should not have to edit
`scad.yml` and `release.yml` separately just to repeat the same
`tool.scad-project` version.

### Reusable libraries

Direct reusable-library versions are also maintainer intent in `project.yml`.
For example:

```yaml
dependencies:
  - name: lib.scad.forge
    role: external
    type: git-submodule
    path: ext/lib.scad.forge
    ref: vA.B.C
```

Change the desired ref, run the updater, review the resulting exact gitlink and
commit both configuration and gitlink.

Consumed libraries own their own nested dependency pins. An outer repository
does not independently advance a nested owner's committed dependency.

## Managed root launchers

Canonical current-generation launchers are:

```text
bootstrap.ps1
bootstrap.sh
update.ps1
update.sh
```

They are managed copies from the exact pinned `tool.git-project` revision and
carry source/version/revision metadata.

Normal behavior:

- `bootstrap.*` restores the committed bootstrap engine and establishes the
  configured dependency closure;
- `update.*` aligns configured dependencies and then runs optional
  domain-tool post-update hooks;
- `update.* status` is read-only;
- an unpatched managed launcher is refreshed from the exact pinned generic tool;
- an intentional local launcher patch must use the documented
  `Managed-Local-Patch` marker.

Legacy root `update-repo.ps1/.sh` is not part of the current canonical
consumer interface.

## Normal update sequence

For an ordinary dependency/tooling update:

```text
edit desired semantic ref(s) in project.yml
        ↓
run ./update.sh or .\update.ps1
        ↓
generic updater resolves refs and moves direct gitlinks
        ↓
tool.scad-project post-update hook aligns SCAD reusable-workflow refs
        ↓
managed root launchers are refreshed when appropriate
        ↓
review git diff / git status
        ↓
run repository verification + PR CI
        ↓
commit configuration + exact gitlinks + managed generated changes together
```

Do not hand-edit a gitlink without also keeping the human-readable configuration
intent coherent.

## GitHub Actions convention

Current-generation SCAD repositories use thin callers with stable filenames.

### `.github/workflows/scad.yml`

Normal SCAD CI caller.

For normal projects/libraries it normally calls:

```text
brainboxemb/tool.scad-project/.github/workflows/project-production.yml@<tool-scad-release>
```

A specialised lab may deliberately call a narrower released workflow such as
`project-build.yml`, but the local `doc/40-development.md` must explain that
exception.

The normal human-facing workflow name is `SCAD production`; a deliberately
specialised repository may use a clearer role-specific display name.

### `.github/workflows/release.yml`

Present when the repository owns versioned releases.

It is a thin caller of:

```text
brainboxemb/tool.scad-project/.github/workflows/project-release.yml@<tool-scad-release>
```

Normal display name: `Release`.

Repositories that do not publish versioned releases do not add this file merely
for symmetry.

### `.github/workflows/pr-cleanup.yml`

Present when the repository publishes generated PR-preview branches.

It calls the released generic cleanup workflow owned by `tool.git-project`.

Normal display name: `PR cleanup`.

The reusable-workflow version used here is a separate generic-tool version
point from the SCAD reusable-workflow ref. Until generic workflow-ref
synchronisation is automated, review this ref explicitly when adopting a new
`tool.git-project` release.

### Keep callers thin

Consumer workflow files own:

- event triggers;
- the permissions required by the reusable workflow;
- small repository-role inputs;
- the released reusable-workflow reference.

Shared runtime setup, cache policy, production orchestration, publication and
release mechanics belong to the reusable workflow owner.

If substantial shell/Python orchestration appears in an ordinary consumer
workflow, first check whether it belongs in `tool.scad-project` or
`tool.git-project`.

## Workflow dependency maintenance

There are two distinct version policies.

### BrainboxEmb reusable workflows

Use released semantic refs. For SCAD-owned workflow callers the
`tool.scad-project` ref follows the declared SCAD-tool release.

Generic workflows such as PR-preview cleanup follow a released
`tool.git-project` ref.

### Third-party actions and hosted runners

Third-party action pinning, automated update PRs, release cool-down policy and
runner-image maintenance are coordinated separately by Migration 007 / meta
issue #66.

Most third-party actions used by a normal SCAD repository should be hidden
inside the shared reusable workflows. Any remaining direct third-party action in
a consumer is still subject to that portfolio policy.

## Local `doc/40-development.md`

Every maintained current-generation SCAD repository keeps this short local
manual.

It should state, without duplicating this shared page:

1. what a developer normally opens/runs in this repository;
2. the direct shared tooling and reusable-library dependencies that matter;
3. which local files contain manually selected version refs;
4. the workflow files present and why each exists;
5. normal build/verification/release commands or entrypoints;
6. repository-specific deviations from the shared convention;
7. links to the plan, verification document and this shared guide.

Do not hard-code a long table of exact current SHAs into prose. Exact current
state is read from `project.yml`, committed gitlinks and live workflow files.
A concise semantic version summary is useful only where it helps a maintainer
know which values intentionally move together.

## Local development-document template

A normal local document can stay compact:

```md
# Development

## Start here
- Plan: [00-plan.md](00-plan.md)
- Shared SCAD repository guide: <brainboxemb.meta link>

## Local workflow
Describe the normal edit / preview / verify path for this repository.

## Dependencies and version updates
State which project.yml refs a maintainer changes and any repository-specific
dependency rule.

## GitHub Actions
- scad.yml — why this repo uses production/build
- release.yml — present/absent and why
- pr-cleanup.yml — present/absent and why

## Repository-specific exceptions
State real deviations, or say there are none.
```

The template is intentionally a minimum. Add useful repo-specific operating
knowledge, not generic architecture copied from meta.

## Before merging an update

Check at least:

- configured dependency refs express the intended released versions;
- committed direct gitlinks resolve to those releases;
- bootstrap gitlink is the deliberately accepted generic-tool revision;
- managed root launcher provenance matches the bootstrap tool after refresh;
- `scad.yml` / `release.yml` use the expected released SCAD workflow ref;
- `pr-cleanup.yml` uses the expected released generic workflow ref when
  present;
- no stale local orchestration duplicates shared tooling;
- repository-local verification passes;
- exact PR-head CI is green.

After merge, verify the expected exact-main workflow/publication behavior.
