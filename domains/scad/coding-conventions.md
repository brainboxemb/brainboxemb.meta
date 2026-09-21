# SCAD coding conventions

Status: **current shared convention, expected to evolve with use**

## Purpose

This page defines the portfolio-level coding and naming convention for
current-generation OpenSCAD source.

The goal is not to prescribe every possible style choice. The goal is to make
source predictable enough that names reveal their role, meaning and units
without forcing the reader to reconstruct intent.

No convention fits every situation. When a real design is clearer by making an
exception, prefer the clearer design and document the exception.

The convention deliberately separates **Customizer visibility** from
**semantics**. A value does not become presentation state merely because it is
shown in the OpenSCAD Customizer.

## Naming style

OpenSCAD source uses **snake_case** as the normal naming style.

| Form | Use | Examples |
| --- | --- | --- |
| `snake_case` | variables, parameters, functions, modules and object fields | `hole_diameter_mm`, `tube_mount_create()`, `mounting_points` |
| `_snake_case` | private/internal variables, functions and modules | `_transition_width_mm`, `_build_transition()` |
| `UPPER_SNAKE_CASE` | true constants and fixed entrypoint choices | `RENDER_ITEM`, `DEFAULT_FLANK_ANGLE_DEG` |
| `d_snake_case` | standalone design input | `d_relief_radius_mm`, `d_profile` |
| `c_snake_case` | standalone presentation/inspection input | `c_view`, `c_show_reference` |

### Do not use camelCase or PascalCase for normal SCAD identifiers

For clarity, the common casing names mean:

- **snake_case**: `mounting_hole_diameter_mm`;
- **camelCase**: `mountingHoleDiameterMm`;
- **PascalCase**: `MountingHoleDiameterMm`;
- **UPPER_SNAKE_CASE**: `MOUNTING_HOLE_DIAMETER_MM`.

New portfolio SCAD code uses snake_case, not camelCase or PascalCase.
UPPER_SNAKE_CASE is reserved for constants.

Existing external APIs keep their own spelling. Do not rename a third-party or
already released API merely to make it match this convention.

OpenSCAD special variables such as `$fn`, `$fa` and `$fs` naturally keep
the spelling defined by OpenSCAD.

## Naming classes

| Form | Meaning | Examples |
| --- | --- | --- |
| `d_...` | Standalone/design input that changes geometry, dimensions or functional configuration. It may be exposed in the Customizer. | `d_profile`, `d_bore`, `d_relief_radius_mm`, `d_lock_release_shape` |
| `c_...` | Customizer/presentation input that changes only inspection or presentation, not the designed object. | `c_view`, `c_orientation`, `c_high_resolution` |
| `UPPER_SNAKE_CASE` | A true fixed constant or fixed entrypoint choice, not an interactive design input. Private constants may additionally use the leading underscore. | `RENDER_ITEM`, `_HUB75_DOVETAIL_WIDTH_MM` |
| `_...` | Private/internal/derived name. Use this for variables, functions and modules that are not part of the consumer-facing API. | `_standalone_clamp`, `_transition_width_mm`, `_build_transition()` |
| no prefix | Public functional API names. New scalar parameters should still carry an explicit unit suffix where applicable. | `hub75_tube_clamp_create()`, `transition_relief_radius_mm` |

## Names should reveal meaning

Prefer a name that tells the reader what a value represents, not merely its
type or how it happened to be calculated.

Prefer:

```openscad
active_mounting_points = ...;
rear_clearance_mm = ...;
panel_width_mm = ...;
```

over:

```openscad
data = ...;
result = ...;
value = ...;
filtered_points = ...;
```

Names such as `data`, `value`, `result`, `temp` and `obj` are usually
too generic. A short local temporary may be reasonable when its purpose is
immediately obvious, but it should not become part of a public API.

Qualifiers normally follow the thing they qualify:

```openscad
sample_min
sample_max
sample_avg
hole_diameter_mm
rear_clearance_mm
```

### Single-letter names

Avoid unexplained single-letter names, but do not fight established CAD
notation.

The following are normally clear in a small local scope:

- `x`, `y`, `z` for coordinate axes;
- `i`, `j` for a small index-only loop;
- mathematical names that directly match a documented formula.

When the value has domain meaning, name that meaning instead:

```openscad
for (hole_position = hole_positions) {
    ...
}
```

rather than:

```openscad
for (p = hole_positions) {
    ...
}
```

## Booleans

Boolean names should read as a positive state or a clear yes/no question.

Prefer prefixes such as:

- `is_...`
- `has_...`
- `can_...`
- `should_...`

Examples:

```openscad
is_locked = true;
has_mounting_holes = true;
can_rotate = false;
should_add_support = false;
```

For presentation controls, an imperative toggle can be clearer and is allowed:

```openscad
c_show_reference = true;
c_render_tube = false;
```

Prefer positive names. Avoid double negatives such as
`disable_no_support`.

## Collections are plural

A list or collection should normally have a plural name:

```openscad
hole_positions = [...];
mounting_points = [...];
panel_sizes = [...];
```

Use a suffix such as `_list` only when the fact that the value is specifically
a list is itself meaningful. Do not add `_array` mechanically.

## Functions and modules

Functions and modules use snake_case.

Choose names that make their behavior clear. Common portfolio patterns are:

- `*_create()` — create and return an object/specification;
- `*_build()` — emit the functional geometry;
- `*_render()` — render or present an object/view;
- `*_is_*()`, `*_has_*()` — return a boolean property;
- a property/result name — return that value.

Examples:

```openscad
function tube_mount_create(...) = object(...);

function tube_mount_width_mm(mount) =
    mount.width_mm;

function tube_mount_is_valid(mount) =
    ...;

module tube_mount_build(mount) {
    ...
}

module tube_mount_render(mount, view = "final") {
    ...
}
```

Do not force every function to start with `get_`. For a pure accessor,
`tube_mount_width_mm(mount)` says more than
`get_tube_mount_width(mount)`.

Use a verb when the name represents an operation. The verb must match the
actual behavior; a function called `calculate_...` should calculate, and a
module called `render_...` should not unexpectedly mutate the meaning of the
design.

## Object-based APIs

Object-based APIs use a deliberate distinction between the **caller-side
variable name** and the **receiver-like function/module parameter**.

At the call site, prefer a semantic domain name:

```openscad
panel = hub75_panel_create(...);
mount = tube_mount_create(...);

hub75_panel_render(panel);
tube_mount_build(mount);
```

Inside a function or module that primarily operates on one object, use `obj`
as the standard first parameter:

```openscad
function hub75_panel_width_mm(obj) =
    obj.width_mm;

module tube_mount_build(obj) {
    ...
}

module tube_mount_render(
    obj,
    view = "final",
    show_reference = false
) {
    ...
}
```

This gives object-based APIs a consistent visual pattern: the function/module
name tells us the domain, while `obj` tells us which parameter is the object
being operated on.

Use `obj` only in this narrow receiver-like role. Do not use it as a generic
name for arbitrary values elsewhere.

Do **not** use `this` or `self` as the normal convention. Those names imply a
language-level method receiver, while OpenSCAD functions/modules still receive
the object explicitly as an argument.

When a function/module works with multiple objects and their roles matter, use
role-qualified names instead of multiple ambiguous `obj` parameters:

```openscad
source_obj
target_obj

left_obj
right_obj
```

If the domain name is clearer than `obj` because several different object
types are mixed in one function, use the domain names:

```openscad
panel
mount
connector
```

### Object parameter comes first

When a function or module operates primarily on one existing object, put
`obj` first, followed by additional input/options:

```openscad
module tube_mount_render(
    obj,
    view = "final",
    show_reference = false
) {
    ...
}
```

This makes related APIs consistent and keeps the primary subject visible.

### Do not repeat the object name in its fields

The surrounding object already supplies context.

Prefer:

```openscad
panel.width_mm
panel.height_mm
panel.mounting_points
```

over:

```openscad
panel.panel_width_mm
panel.panel_height_mm
panel.panel_mounting_points
```

Existing released object fields remain compatibility contracts and are not
silently renamed.

## Design versus presentation

Use `d_` when changing the value changes the actual model or its functional
configuration:

```openscad
d_profile = "medium";
d_bore = "functional";
d_relief_radius_mm = 6.0;
d_lock_release_shape = "trapezoid";
d_lock_release_taper_angle_deg = 45;
```

Use `c_` when the value only controls how the same design is inspected or
presented:

```openscad
c_orientation = "design";
c_view = "iso";
c_high_resolution = false;
c_explode_distance_mm = 20;
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

## Units in names

OpenSCAD scalar values do not carry a unit type, so physical units should be
visible in the name when they are part of the value's interpretation.

The suffix is part of the identifier, not a statement that OpenSCAD itself
performs unit checking.

### Common unit suffixes

Use the suffix that matches the value actually stored.

| Quantity | Preferred suffixes | Examples |
| --- | --- | --- |
| length | `_um`, `_mm`, `_cm`, `_m` | `layer_height_mm`, `cable_length_m` |
| area | `_mm2`, `_cm2`, `_m2` | `contact_area_mm2` |
| volume | `_mm3`, `_cm3`, `_m3` | `part_volume_mm3` |
| angle | `_deg`, `_rad` | `flank_angle_deg` |
| time | `_us`, `_ms`, `_s` | `settle_time_ms` |
| mass | `_g`, `_kg` | `part_mass_g` |
| force | `_n` | `clamp_force_n` |
| pressure/stress | `_pa`, `_kpa`, `_mpa` | `yield_stress_mpa` |
| energy | `_j` | `impact_energy_j` |
| power | `_w` | `heater_power_w` |
| voltage | `_v` | `supply_voltage_v` |
| current | `_a`, `_ma` | `motor_current_a` |
| resistance | `_ohm`, `_kohm` | `pullup_resistance_kohm` |
| frequency | `_hz`, `_khz`, `_mhz` | `pwm_frequency_hz` |
| temperature | `_k`, `_deg_c` | `bed_temperature_deg_c` |
| speed | `_mm_s`, `_m_s` | `travel_speed_mm_s` |
| acceleration | `_mm_s2`, `_m_s2` | `acceleration_mm_s2` |
| rotational speed | `_rpm` | `spindle_speed_rpm` |

Notes:

- `_deg` is the normal angle suffix for OpenSCAD because OpenSCAD's
  trigonometric/rotation interfaces use degrees. Degrees are not an SI base
  unit, but they are the practical native unit here.
- use ASCII `um` rather than the `µm` symbol inside identifiers;
- use `ohm` rather than `Ω` inside identifiers;
- compound units use underscores: `_mm_s`, `_m_s2`;
- for constants, keep the same suffix semantics in uppercase:
  `DEFAULT_FLANK_ANGLE_DEG`, `MAX_PRESSURE_KPA`.

Do not add a unit suffix to values that do not have a physical unit. Name their
meaning instead:

```openscad
hole_count
mounting_index
scale_ratio
gear_teeth
```

For a percentage stored on a 0..100 scale, `_pct` is acceptable when it makes
that representation explicit, for example `infill_pct`.

### Unit examples

```openscad
d_relief_radius_mm = 6.0;
d_lock_release_taper_angle_deg = 45;

c_explode_distance_mm = 20;

_transition_width_mm = ...;
_flank_angle_deg = ...;

DOVETAIL_WIDTH_MM = 12;
DEFAULT_FLANK_ANGLE_DEG = 30;
```

The role prefix and unit suffix are independent. Read a name from left to right:

```text
d_relief_radius_mm
│ │             └─ unit: millimetres
│ └─────────────── meaning: relief radius
└───────────────── role: design input
```

For **new** public scalar API parameters and object fields, prefer the same
explicit unit suffix, for example `width_mm` and `angle_deg`. Existing
released/public APIs that use shorter names such as `width`, `height` or
`angle` are compatibility contracts: do not silently rename them merely to
satisfy this convention. Handle any breaking API cleanup as an explicit
migration/release decision.

## Abbreviations

Abbreviations are encouraged when they come from a **shared, documented list**
and make names shorter without making them ambiguous.

The purpose of this list is consistency: use the same abbreviation everywhere
instead of inventing a new shortened form per file or repository.

For example, prefer:

```openscad
mount_pos
hole_cnt
profile_len_mm
src_obj
des_obj
```

over mixing forms such as:

```openscad
mount_position
hole_count
profile_length_mm
source_obj
destination_object
```

Neither form is inherently unreadable, but a shared abbreviation vocabulary
makes related source easier to scan.

### General abbreviations

The following list is adapted from the supplied coding-rules reference and is
the default vocabulary for new SCAD code:

| Abbreviation | Meaning | Example |
| --- | --- | --- |
| `adm` | administration | `view_adm` |
| `avg` | average | `sample_avg` |
| `ch` | character | `separator_ch` |
| `cmd` | command | `render_cmd` |
| `cnt` | count | `hole_cnt` |
| `col` | column | `grid_col` |
| `ctrl` | control | `view_ctrl` |
| `des` | destination | `des_obj` |
| `hor` | horizontal | `hor_offset_mm` |
| `len` | length | `profile_len_mm` |
| `max` | maximum | `width_max_mm` |
| `min` | minimum | `width_min_mm` |
| `nr` | number | `panel_nr` |
| `obj` | object | `obj` |
| `pos` | position | `mount_pos` |
| `prev` | previous | `prev_pos` |
| `rec` | record | `view_rec` |
| `src` | source | `src_obj` |
| `str` | string | `name_str` |
| `ttl` | total | `width_ttl_mm` |
| `val` | value | `default_val` |
| `vert` | vertical | `vert_offset_mm` |

Use the listed spelling. For example, if `pos` is the shared abbreviation for
position, do not introduce `position`, `pst` or `psn` in comparable new
identifiers without a reason.

### Established technical abbreviations

Established technical/domain abbreviations may be used directly when the
abbreviation is more recognizable than the expanded form:

| Abbreviation | Meaning |
| --- | --- |
| `2d`, `3d` | dimensionality |
| `cad` | computer-aided design |
| `cnc` | computer numerical control |
| `id` | identifier |
| `led` | light-emitting diode |
| `pcb` | printed circuit board |
| `stl` | STL geometry/file format |
| `hub75` | HUB75 interface/domain name |

Coordinate axes `x`, `y` and `z` are also accepted without expansion.

Unit suffixes such as `mm`, `deg`, `rpm` and `mpa` are defined by the
units section and are not treated as arbitrary abbreviations.

### Domain-specific abbreviations

A repository or domain may add abbreviations when they occur often enough to
justify a shared shorthand. Add them to the relevant shared documentation
rather than inventing local variants repeatedly.

The rule is therefore not "avoid abbreviations". It is:

> abbreviate consistently from a known vocabulary.

## Use opposite pairs consistently

When two concepts form a pair, choose one vocabulary and keep it throughout the
API.

Preferred pairs include:

| Side A | Side B |
| --- | --- |
| `min` | `max` |
| `first` | `last` |
| `start` | `end` |
| `before` | `after` |
| `source` | `target` |
| `input` | `output` |
| `inner` | `outer` |
| `front` | `rear` |
| `left` | `right` |
| `top` | `bottom` |
| `open` | `closed` |
| `add` | `remove` |
| `create` | `destroy` |
| `lock` | `unlock` |
| `show` | `hide` |

Do not mix pairs such as `source`/`destination` in one API and
`source`/`target` in another without a domain reason.

## Avoid magic values

A non-obvious numeric or string literal that encodes design meaning should be
named.

Prefer:

```openscad
wall_thickness_mm = 2.0;
mounting_hole_diameter_mm = 4.2;
```

or make the value an explicit object/API parameter:

```openscad
function bracket_create(
    wall_thickness_mm = 2.0,
    mounting_hole_diameter_mm = 4.2
) =
    object(
        wall_thickness_mm = wall_thickness_mm,
        mounting_hole_diameter_mm = mounting_hole_diameter_mm
    );
```

Do not mechanically create constants for every `0`, `1` or simple geometric
factor. The purpose of the rule is to expose design meaning, not to hide simple
math behind names.

## Public API remains domain-named

The `c_` and `d_` prefixes are for top-level standalone/design controls.
They must not leak into reusable create/build APIs or object fields.

Prefer:

```openscad
d_relief_radius_mm = 6.0;

_clamp =
    hub75_tube_clamp_create(
        transition_relief_radius_mm = d_relief_radius_mm
    );
```

The public API stays:

```openscad
function hub75_tube_clamp_create(
    transition_relief_radius_mm = 6.0
) = ...;
```

not `d_transition_relief_radius_mm`.

For an already released API whose parameter is named
`transition_relief_radius`, keep that spelling until an explicit breaking
migration/release changes it.

## Private names

A leading underscore marks implementation detail, regardless of whether the
helper supports a public function/module or a private one.

```openscad
module public_component_build(component) {
    _build_transition(component);
}

function _derive_transition_width_mm(component) =
    ...;

module _build_transition(component) {
    _width_mm = _derive_transition_width_mm(component);
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

Use UPPER_SNAKE_CASE for values that are genuinely fixed by the file/component
or by a dedicated entrypoint rather than interactively configured.

If a constant is private, combine both rules:

```openscad
_HUB75_DOVETAIL_WIDTH_MM = 12;
```

Prefer public accessor functions over exposing mutable-looking global constants
as part of a reusable library API.

## Comments and documentation

Names should carry the basic meaning. Comments should explain information that
the name cannot:

- **why** a choice exists;
- the source of a measured/datasheet dimension;
- a tolerance or manufacturing reason;
- a non-obvious coordinate-system choice;
- an intentional compatibility constraint;
- why an apparently simpler implementation is wrong.

Avoid comments that merely repeat the code.

Prefer:

```openscad
// Extra clearance is required so the printed female dovetail does not
// bind after cooling.
dovetail_clearance_mm = 0.20;
```

over:

```openscad
// Set dovetail clearance to 0.20.
dovetail_clearance_mm = 0.20;
```

Because units are encoded in numeric names, a separate unit comment is normally
unnecessary. Add a comment when range, reference datum or interpretation is not
obvious from the name.

## Scope and evolution

This convention should stay practical rather than exhaustive.

When adding a rule:

1. prefer a rule that resolves a real ambiguity already seen in source;
2. include a concrete good/bad example where it helps;
3. avoid adding a taxonomy merely because one could exist;
4. preserve released API compatibility unless a migration explicitly decides
   otherwise.

Repository-specific `AGENTS.md` files should refer to this page for shared
SCAD coding rules instead of copying the convention. Local guidance may add a
genuinely repository-specific exception or constraint, but should not redefine
the shared naming model.
