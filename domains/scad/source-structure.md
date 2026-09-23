# SCAD source structure

Status: **current shared source/documentation convention**

## Why this page exists

The shared SCAD architecture describes builds, runtimes and publication, but a
project also needs a consistent human-facing source shape. This page defines the
portfolio convention for current-generation OpenSCAD component source and
component-local visual documentation.

Repository-level plan, specification, design and verification document roles
are defined in [SCAD documentation structure](documentation-structure.md).

The goal is simple: a maintainer should be able to open a component or its
design-render adapter directly in OpenSCAD, understand the available design
states from the Customizer, and trace every explanatory image back to the real
production geometry.

This is a **source/documentation contract**, not a shared tooling
implementation requirement.

## Component layout

The established HUB75 library pattern keeps the public/production entrypoint
one level above its support/design directory:

```text
<component-family>/
├── <component>.scad
└── <component>/
    ├── <component>_render.scad
    ├── design/
    │   └── design.md
    └── render/
        └── ...                     # optional component-specific renders
```

For example, `lib.scad.hub75` uses:

```text
openscad/p5-64x32-panel/
├── hub75_p5_64x32_panel.scad
└── hub75_p5_64x32_panel/
    ├── hub75_p5_64x32_panel_render.scad
    ├── design/
    │   └── design.md
    └── render/
        └── ...
```

This split is preferred for components with substantial design/evidence
support because the production entrypoint stays prominent and uncluttered while
interactive walkthrough code and component-specific presentation files remain
grouped beside their documentation.

Repository-level presentation output remains separate:

```text
dsg/openscad/render/*.scad
dsg/openscad/export/*.scad
```

### Public/production `<component>.scad`

Owns the actual reusable/production geometry and its public modules/functions.

It may also expose documentation helpers when needed, but those helpers must be
derived from the production construction. Do not create a second approximate
geometry implementation merely to make documentation easier.

### Design discovery from production source

When a component has a design document, the production `.scad` entrypoint
should advertise it near the file header so a maintainer or automated agent
encounters the design context before changing geometry.

Use a short navigation comment, for example:

```openscad
// Design: <component>/design/design.md
// Design review: <component>/<component>_render.scad
```

Adjust the relative paths to the actual component layout. These lines are
navigation aids, not imports and not a second copy of the design rationale.

The design document is the first place to recover facts such as coordinate
systems, print orientation, geometry ownership, accepted baseline shape and
dimension provenance. Do not repeatedly reverse-engineer those decisions from
the implementation when they are already documented.

Useful rules:

- keep the production component callable as a standalone object where practical;
- expose values required across `use<>` boundaries through functions or module
  parameters because OpenSCAD does not import file-level variables through
  `use<>`;
- keep source-derived dimensions, transformed dimensions and project-owned
  dimensions distinguishable in code/comments;
- documentation helpers such as removed-material/profile views should use
  `intersection()`, `difference()` or the real production cutters rather than
  redraw the intended shape.

### Support `<component>/<component>_render.scad`

Owns the **interactive design-review adapter** for that component. It belongs
inside the component support directory, not beside the public/production
entrypoint and not inside `design/` itself.

A maintainer opening this file directly in OpenSCAD must be able to step through
the meaningful named design states with the Customizer. Follow the shared
[naming convention](coding-conventions.md): presentation-only top-level
Customizer state uses `c_`, while the public design-render module keeps normal
domain parameter names.

Example:

```openscad
/* [Design view] */
c_view = "final"; // [final,base,removed-material,profile,after-cut]

module example_design(view = "final") {
    if (view == "base")
        ...
    else if (view == "removed-material")
        ...
    else if (view == "profile")
        ...
    else
        example_build();
}

example_design(view = c_view);
```

The exact view names are component-specific, but the contract is not:

- the top-level Customizer selector is present;
- its values match the named views accepted by the design module;
- `design/design.md` uses those same names in `scad-render` blocks;
- reader-facing names are descriptive rather than internal testcase codes;
- the default view is useful when the file is opened manually;
- documentation-only colors, exploded spacing, sections and camera-oriented
  arrangements are allowed;
- alternate mating geometry that does not exist in production is not.

If another top-level switch materially helps interactive review, expose it in
the Customizer as well rather than requiring a maintainer to edit source text.

## Support `<component>/design/design.md`

Owns the step-by-step visual explanation of how the component is constructed.
Repository-level purpose, semantic contracts and verification strategy belong
in the numbered `doc/` documents defined by
[SCAD documentation structure](documentation-structure.md).

Its normal `source:` points to the sibling support adapter, for example
`source: hub75_p5_64x32_panel_render.scad`.

For a substantial component, this is not only retrospective documentation. It
is persistent engineering context for the next modification. Read it before
changing geometry so accepted baselines, coordinate transforms, print
orientation and source/derived/project-owned dimensions do not have to be
rediscovered on every iteration.

A very small leaf component does not need ceremonial documentation merely to
satisfy a folder pattern. But when a component has non-trivial construction,
multiple coordinate systems, print-orientation constraints, reusable-library
ownership boundaries, hidden fit geometry, or repeated design iterations, a
worked-out design file should exist before those decisions become dependent on
chat history or source-code archaeology.

Each important step should answer one clear question. Avoid relying on one
attractive isometric image when the geometry being explained is a profile,
subtraction or hidden retention surface.

For subtractive/profile geometry, prefer an evidence sequence such as:

```text
where does the operation happen?
    -> 3D location view

what exact profile/material is involved?
    -> straight orthographic section / removed-material view

what is the result?
    -> after-operation view

does it match the intended source/derivation?
    -> dimension/provenance table or comparison view
```

When a design is derived from an external or reusable reference, distinguish
dimensions explicitly:

| Class | Meaning |
| --- | --- |
| **Upstream** | Directly present in the pinned/reference design. |
| **Derived** | Deterministic arithmetic/geometric transform of upstream values. |
| **Project/experiment choice** | New local dimension or termination introduced by the consumer/PoP. |

Do not describe a project/experiment choice as source-derived merely because it
was attached to a source-derived profile.

## Design view quality

A generated image existing and CI being green are not sufficient evidence that
the design view is useful.

Before accepting a design walkthrough, check that:

- removed material is visibly distinguishable from cutter volume outside the
  part;
- a non-rectangular source profile is shown orthographically somewhere;
- before/after images actually reveal the change;
- hidden mating/retention geometry has a section or view that exposes it;
- framing makes the relevant geometry large enough to inspect;
- the image does not introduce ambiguity through occlusion, z-fighting or a
  misleading camera angle.

A valid CI failure caused by a design/evidence view is useful evidence. Correct
the view or geometry; do not weaken the check simply to make the build green.

## Relationship to other SCAD files

`dsg/openscad/render/*.scad` owns repository-level presentation renders. Those
files may choose cameras and assembly context for published PNGs, but they do
not replace the component-local interactive design adapter.

`dsg/openscad/export/*.scad` owns explicit export entrypoints.

`project.scad.yml`, Moon tasks and shared tooling own execution/publication
policy; they do not define the component's mechanical geometry or named design
states.

## Ownership

- **consumer/project/experiment repository** — actual component geometry,
  component-specific view names and design explanation;
- **template/reference consumer** — demonstrates the convention;
- **brainboxemb.meta** — documents the shared source-structure convention;
- **tool.scad-project** — only owns automation when behaviour genuinely needs
  shared implementation.

A missing Customizer selector or inconsistent support layout in one repository
should first be corrected in that repository. Promote automation to shared
tooling only when a real cross-consumer need is established.
