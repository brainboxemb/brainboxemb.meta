# Transitive SCAD library dependencies PoP

Status: **proposed / inactive**

Tracking issue: [#96](https://github.com/brainboxemb/brainboxemb.meta/issues/96)

Implementation/evidence repository: **not created; create only when this PoP is deliberately activated**

Potential production owners:

- `brainboxemb/tool.git-project` — dependency/bootstrap behavior;
- `brainboxemb/tool.scad-project` — SCAD dependency discovery/build behavior where required;
- reusable SCAD libraries such as `brainboxemb/lib.scad.mechint`;
- `brainboxemb/lib.scad.util` as the candidate lightweight foundation library.

## Question

Can reusable Brainboxemb SCAD libraries depend on another SCAD library at
runtime — initially `lib.scad.util` — while keeping the normal developer
experience simple?

The required experience is:

```text
clone / checkout
        ↓
bootstrap
        ↓
open a component .scad directly in desktop OpenSCAD
        ↓
works without additional machine configuration
```

## Why this is a PoP first

The intended architecture is plausible, but several SCAD-specific assumptions
still need reproducible evidence before changing the shared dependency model:

- nested external dependencies must bootstrap predictably;
- a library embedded in a consumer must still resolve its own dependency;
- direct desktop OpenSCAD use must not depend on CI-only environment setup;
- different owners may pin different revisions of the same foundation library;
- dependency scanning, status/update behavior and provenance must remain
  deterministic.

If qualified, a later migration can adopt the model in tooling and selected
libraries. This PoP does not authorize that rollout.

## Target concept

```text
lib.scad.util
    lightweight foundation library

        ↓

lib.scad.mechint
lib.scad.clamps
other reusable SCAD libraries

        ↓

project consumers
```

A library owns and pins its direct runtime dependencies. A candidate standalone
layout is:

```text
lib.scad.mechint/
├── openscad/
└── ext/
    └── lib.scad.util/
```

A real consumer may independently pin the same foundation library:

```text
HUB75 project
├── ext/lib.scad.util
└── ext/lib.scad.mechint
    └── ext/lib.scad.util
```

The exact directory/import contract is part of the PoP and is not yet frozen.

## Desktop OpenSCAD constraint

A successful architecture must not require a developer to:

- install `lib.scad.util` globally;
- edit OpenSCAD's global library directories;
- set a permanent `OPENSCADPATH`;
- launch OpenSCAD through a special wrapper merely to resolve normal library
  dependencies.

After the normal repository bootstrap, directly opening the relevant
`.scad` file on Windows must work.

## Candidate dependency rule

The PoP should evaluate a controlled runtime/external dependency closure rather
than unrestricted recursive submodules:

```text
external/runtime dependency
    -> follow transitively

tooling/development dependency
    -> do not recursively initialize merely because a parent library has it
```

The existing `role: external` declaration in `project.yml` is a candidate
signal; the PoP must determine whether that is sufficient.

## Qualification cases

Retain reproducible evidence for at least:

1. standalone library bootstrap;
2. bootstrap through a real consumer;
3. direct Windows desktop OpenSCAD use after bootstrap;
4. CI/build dependency discovery for nested dependencies;
5. independent compatible version pins in consumer and nested library;
6. understandable status/update behavior;
7. publication/provenance identifying the actual nested revision.

## First representative dependency

The motivating case is `lib.scad.mechint` using the lightweight transform
helpers introduced in `lib.scad.util v0.2.0`, such as `xf_move()` and
`xf_yrot()`.

Their value is source readability rather than new geometry. The PoP therefore
tests whether readable, consistent transform language can be a library-level
contract without making repositories harder to use locally.

The current HUB75 trapezoid/lock-relief geometry work does **not** wait for this
PoP and may continue independently using plain OpenSCAD.

## Activation boundary

This record is intentionally only proposed. Do not create an implementation
repository, change shared bootstrap semantics or roll a new dependency model
through production libraries until the PoP is explicitly selected as active.
