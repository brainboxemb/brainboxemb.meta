# Transitive SCAD library dependencies PoP

Status: **complete**

Tracking issue: [#96](https://github.com/brainboxemb/brainboxemb.meta/issues/96)

Implementation/evidence repository:
`brainboxemb/exp.2026-006.scad-library-dependencies` — retained as a reusable
qualification/regression lab.

Production handoff:
[Migration 008](../../migrations/008-transitive-scad-library-dependencies/README.md)
— **proposed / inactive**.

## Question

Can reusable Brainboxemb SCAD libraries own and pin other SCAD libraries while
keeping the normal developer experience simple?

Required experience:

```text
clone / checkout
        ↓
bootstrap
        ↓
open the relevant .scad directly in desktop OpenSCAD
        ↓
works without global OPENSCADPATH or manual library installation
```

## Qualified dependency model

The experiment qualified a controlled closure based on owner-local
`project.yml` dependencies:

```text
role: external + type: git-submodule
    -> follow transitively

tooling/development submodules
    -> do not recurse merely because a parent library owns them
```

Each owner keeps authority over its own path and ref. The same repository may
therefore appear at independent paths with different pins.

Representative qualified layout:

```text
experiment
├── lib.scad.util v0.2.0
└── lib.scad.mechint v0.1.6
    └── lib.scad.util v0.1.0
```

## Qualification result

DEP-01 through DEP-07 are complete:

1. released direct-only baseline retained;
2. controlled transitive external closure on Linux and Windows;
3. direct Windows desktop OpenSCAD use without global path setup;
4. nested SCAD source discovery and precise SCons invalidation;
5. independent project/library pins with no search-path fallback;
6. normal bootstrap/update/status, dirty-worktree protection and safe recovery;
7. machine-readable target-level provenance of the exact dependency revisions
   actually present in the normal SCons source graph.

The provenance case distinguishes the project-owned `lib.scad.util v0.2.0`
from mechint-owned nested `lib.scad.util v0.1.0` in one real build target.

## Final evidence

- exact qualifying source:
  `16f36faf2ff9e2c19f5df6d23121c46ca9c33af4`;
- DEP-07 build-dependency provenance run:
  `35645913457` — green;
- normal SCAD production:
  `35645914291` — green through Moon materialization, finishing and Build
  publication;
- all DEP-01 through DEP-07 regressions and normal dependency entrypoints green
  on the same qualifying source;
- qualified experiment result merged to main as
  `035a9233f4ef99ad468c3ed0ab288f4772654922`.

The direct desktop gate was also exercised manually on Windows by opening the
nested `lib.scad.mechint/main.scad` normally and rendering with F6.

## Decision

The architecture is viable and supports production adoption.

The PoP does **not** itself change production owners. The experiment-owned
bootstrap/status/provenance prototypes remain evidence until a production
migration deliberately adopts them.

Migration 008 records that possible rollout and remains inactive until selected.
