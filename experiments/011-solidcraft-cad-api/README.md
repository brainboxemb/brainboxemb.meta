# Experiment 011 — SolidCraft CAD API

**Status: active — offline API/adapter checks qualified; real SolidCraft runtime unqualified.**

Implementation/evidence:
[`brainboxemb/exp.2026-011.solidcraft`](https://github.com/brainboxemb/exp.2026-011.solidcraft);
[draft PR #2](https://github.com/brainboxemb/exp.2026-011.solidcraft/pull/2);
[tracking issue #1](https://github.com/brainboxemb/exp.2026-011.solidcraft/issues/1).

## The question

Can we provide a **real CAD modeling interface** in which a user describes
`Part`, `Hole`, `Edges`, fillets, workplanes and features, while SolidCraft
owns the actual geometry and design history?

This is **not** just a one-function-per-SolidCraft-command wrapper.
`vcad` and **CadQuery** are *references for good public CAD API design*;
neither CAD engine is integrated into this experiment.

## Architecture

```text
semantic CAD domain API (engine-independent)
             -> SolidCraft adapter (high-level feature to many commands)
             -> transport (native script now / GUI / MCP later)
             -> SolidCraft (only geometry engine)
```

The upstream [`waynegramlich/scraftcnc`](https://github.com/waynegramlich/scraftcnc/tree/main/scraftcnc/pybind)
contains existing Python command bindings (`scraftpybind`) that are useful
as a *lower-level transport / command mapping reference*. They do not,
on their own, provide the desired CAD domain API.

Rust has been selected for the first typed **CAD-domain** PoP, without
excluding Python as an alternative implementation language later.

The [µcad project](https://codeberg.org/microcad/microcad/) was also provided as
an **API design reference**, specifically for declarative named parts/sketches,
unit-aware quantities and separating design intent from evaluation. Its
older GitHub repository was reviewed; the current Codeberg source was not
accessible to the automated reader. We are not adopting the µcad engine or DSL.
See [µcad design notes](https://github.com/brainboxemb/exp.2026-011.solidcraft/blob/feature/issue-1-python-interface/docs/07-microcad-inspiration.md).

## First implemented semantic subset

- `Part::box3d(length, width, height)` and typed `Part::box_with_units(Length::mm(...), Length::inches(...), ...)`.
- `.edges(Edges::OuterVertical).fillet(radius)`.
- `.through_holes(&holes)` and `.faces(Faces::Top).workplane().circles(&holes)?.cut_through()?`, including input validation.
- SolidCraft-specific adapter expanding each high-level operation into
  native sketch, extrusion, cut and fillet commands.
- Command script transport and offline tests.

See [API design informed by CadQuery and vcad](https://github.com/brainboxemb/exp.2026-011.solidcraft/blob/feature/issue-1-python-interface/docs/05-cad-api-design.md).

**Top-face selection is now implemented for a base box only**: the SolidCraft adapter uses the documented native face-attachment mechanism on `sketch.create` rather than a free-floating global plane. The reference point and local-face 2D orientation require live verification. The edge selector is still limited to four original outside box edges; general topology is not implemented. See [face/workplane design](https://github.com/brainboxemb/exp.2026-011.solidcraft/blob/feature/issue-1-python-interface/docs/08-face-workplanes.md).

## Evidence

GitHub Actions [offline qualification run](https://github.com/brainboxemb/exp.2026-011.solidcraft/actions/runs/42658989559)
succeeded on `cf40297f9446767218f5e58020c4e312c7a63527`:

- 7 Rust tests passed in the earlier qualified run; later CI also covers typed units.
- 8 Python fixture tests passed;
- semantic CAD model generated syntactically valid SolidCraft JSON.

Additionally, the [typed-length CI](https://github.com/brainboxemb/exp.2026-011.solidcraft/actions/runs/42659957864) and the [face-workplane CI](https://github.com/brainboxemb/exp.2026-011.solidcraft/actions/runs/42667955909) passed. The latest proof of principle now includes native face-attachment command mapping tests.

This demonstrates **source / offline adapter correctness only**.
It does **not** prove the generated script builds the right CAD solid.

## Remaining qualification

1. Run the [Windows qualification script](https://github.com/brainboxemb/exp.2026-011.solidcraft/blob/feature/issue-1-python-interface/scripts/qualify-solidcraft.ps1) with `-SkipBuild -Snapshot` against installed SolidCraft 0.30.1 (**no Rust installation required**); retain CLI results, native `.sc`, STEP evidence and preview. The committed JSON fixture is checked against Rust-generated output in [offline CI](https://github.com/brainboxemb/exp.2026-011.solidcraft/actions/runs/42668871056).
2. Inspect real STEP geometry: dimensions, holes, outside edge fillets.
3. Save/reopen native feature history and alter parameters.
4. Implement/qualify GUI control and headless MCP transport backends.
5. Investigate reliable topological references, workplanes and selectors.

## Boundaries

No new geometry kernel. No use of CadQuery or vcad for processing.
No OpenSCAD migration and no production integration.

**Experiment 012** remains a separate proposed/inactive investigation
into PartCAD–SolidCraft interoperability. A generic shared Docker
toolchain is deferred.
