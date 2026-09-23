# Agent guidance

This file is the **portfolio-wide agent entrypoint** for BrainboxEmb.

When working in another BrainboxEmb repository, read that repository's local
`README.md`, `AGENTS.md` and plan first. Then use this file to find the
shared rules that apply.

## Shared working rules

Read:

- [Shared engineering workflow](docs/20-10_engineering-workflow.md) —
  source-of-truth order, ownership, evidence and cross-repository work;
- [Git and repository workflow](docs/20-11_git-workflow.md) — issues,
  branches, commits, pull requests, CI, changelog, merge and release handoff;
- [How projects are organised](docs/40-02_projects.md) — generic
  project/tool ownership;
- [Versioning and releases](docs/20-12_versioning-and-releases.md) —
  released interfaces and dependency pins.

Keep generic rules in those documents. Repository-local AGENTS files should
link here and contain only local routing, exceptions or agent-specific
constraints.

## Domain guidance

### SCAD / CAD

Start at [SCAD and CAD](domains/scad/README.md).

For implementation work, the important shared pages are:

- [Documentation structure](domains/scad/documentation-structure.md);
- [Coding conventions](domains/scad/coding-conventions.md);
- [Source structure](domains/scad/source-structure.md);
- [Tooling and templates](domains/scad/tooling.md);
- [Technical architecture](domains/scad/architecture.md).

Read component-local detailed design before changing non-trivial geometry when
one exists.

### Software

Start at [Software](domains/software/README.md).

Use its architecture/tooling links plus the generic working-model documents
above. Language/tool-specific implementation rules belong in the owning tool or
project repository.

## Current cross-project work

For any migration, experiment, PoP or other repository-spanning task, read
[STATUS.md](STATUS.md) before selecting work.

Do not infer the active work-track number from old chat/history. Proposed or
inactive tracks do not start automatically.

## Meta repository ownership

`brainboxemb.meta` owns:

- portfolio-level overview and shared conventions;
- repository catalog/dashboard coordination;
- generic working-model documentation;
- domain-level shared guidance;
- cross-project migration/experiment coordination records.

Implementation stays in the repository that owns it.

## Meta-specific navigation

When changing this repository itself:

- general overview → `README.md`;
- public repository inventory → `repositories/`;
- durable shared working model → `docs/working-model/`;
- domain guidance → `domains/`;
- current cross-project work → `STATUS.md`;
- migrations → `migrations/`;
- experiments/PoPs → `experiments/`;
- dashboard implementation → read `dashboard/AGENTS.md` first.

Avoid duplicating durable engineering rules in this file when a linked
authority can own them.
