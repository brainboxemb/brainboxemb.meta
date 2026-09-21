# SCAD coding conventions

Status: **current shared convention, expected to evolve with use**

## Purpose

This page defines the portfolio-level naming convention for current-generation
OpenSCAD source. The goal is to make it obvious whether a top-level value is a
design input, presentation state, a fixed constant, or an implementation detail.

The convention deliberately separates **Customizer visibility** from
**semantics**. A value does not become presentation state merely because it is
shown in the OpenSCAD Customizer.

## Naming classes

| Form | Meaning | Examples |
| --- | --- | --- |
| `d_...` | Standalone/design input that changes geometry, dimensions or functional configuration. It may be exposed in the Customizer. | `d_profile`, `d_bore`, `d_relief_radius`, `d_lock_release_shape` |
| `c_...` | Customizer/presentation input that changes only inspection or presentation, not the designed object. | `c_view`, `c_orientation`, `c_high_resolution` |
| `UPPERCASE` | A true fixed constant or fixed entrypoint choice, not an interactive design input. Private constants may additionally use the leading underscore. | `RENDER_ITEM`, `_HUB75_DOVETAIL_WIDTH` |
| `_...` | Private/internal/derived name. Use this for variables, functions and modules that are not part of the consumer-facing API. | `_standalone_clamp`, `_derive_width()`, `_build_transition()` |
| no prefix | Public functional API names and their normal domain parameters. | `hub75_tube_clamp_create()`, `transition_relief_radius` |

## Design versus presentation

Use `d_` when changing the value changes the actual model or its functional
configuration:

```openscad
d_profile = "medium";
d_bore = "functional";
d_relief_radius = 6.0;
d_lock_release_shape = "trapezoid";
```

Use `c_` when the value only controls how the same design is inspected or
presented:

```openscad
c_orientation = "design";
c_view = "iso";
c_high_resolution = false;
```

Both classes may appear in the OpenSCAD Customizer. The `c_` prefix means
**Customizer/presentation state**, not simply "visible in the Customizer".

A dedicated render/export entrypoint that always renders one fixed item should
normally express that choice as a constant instead:

```openscad
RENDER_ITEM = "tube-clamp";
```

Do not create an extra render-selector prefix merely for fixed entrypoint
choices.

## Public API remains domain-named

The `c_` and `d_` prefixes are for top-level standalone/design controls.
They must not leak into reusable create/build APIs or object fields.

Prefer:

```openscad
d_relief_radius = 6.0;

_clamp =
    hub75_tube_clamp_create(
        transition_relief_radius = d_relief_radius
    );
```

The public API stays:

```openscad
function hub75_tube_clamp_create(
    transition_relief_radius = 6.0
) = ...;
```

not `d_transition_relief_radius`.

## Private names

A leading underscore marks implementation detail, regardless of whether the
helper supports a public function/module or a private one.

```openscad
module public_component_build(component) {
    _build_transition(component);
}

function _derive_transition_width(component) =
    ...;

module _build_transition(component) {
    _width = _derive_transition_width(component);
    ...
}
```

Therefore:

- private/intermediate variables use `_...`;
- private/helper functions use `_...()`;
- private/helper modules use `_...()`;
- a helper used only inside the implementation of a public module is still
  private and still uses `_`;
- public consumer-facing functions/modules do not use a leading underscore.

When OpenSCAD source uses a lexically local helper inside a public module, keep
the same leading-underscore convention so its role remains obvious.

## Constants

Use uppercase for values that are genuinely fixed by the file/component or by a
dedicated entrypoint rather than interactively configured.

If a constant is private, combine both rules:

```openscad
_HUB75_DOVETAIL_WIDTH = 12;
```

Prefer public accessor functions over exposing mutable-looking global constants
as part of a reusable library API.

## Scope and evolution

This convention is intentionally small. Revisit it when real source exposes an
ambiguity; do not add prefixes pre-emptively.

Repository-specific `AGENTS.md` files should refer to this page for shared
SCAD naming rules instead of copying the convention. Local guidance may add a
genuinely repository-specific exception or constraint, but should not redefine
the shared prefixes.
