# Experiment 012 — PartCAD–SolidCraft interoperability

**Status: proposed / inactive — no implementation repository created.**

Upstream reference: [`partcad/partcad-solidcraft`](https://github.com/partcad/partcad-solidcraft).
Related but distinct: [Experiment 011 — SolidCraft Python interface](../011-solidcraft-python-interface/README.md).

## What do we want to understand?

This is not a second implementation of Python command bindings. PartCAD integrates parts and CAD formats across workflows. Its SolidCraft plugin is a possible way to reuse SolidCraft designs in PartCAD projects.

The existing plugin provides:

- SolidCraft `.solidcraft` / JSON design reading with declared PartCAD values applied to same-name design parameters;
- Rhino `.3dm` and IGES file imports;
- STEP conversion to OpenCascade/OCP shapes on the PartCAD side;
- export from PartCAD into a SolidCraft file that contains an imported STEP-derived component;
- `pc ide open --with solidcraft` integration;
- its own container image, CLI download/cache and version-pinning logic.

**Important:** A native SolidCraft design remains parametrically editable in SolidCraft; the corresponding PartCAD shape is converted to STEP. Exporting a PartCAD object into a `.solidcraft` container does **not** reconstruct its original feature history. This distinction should be demonstrated in a test.

## Proposed qualification

1. Install/use a specific PartCAD and SolidCraft version.
2. Import a native parametric SolidCraft part through the plugin.
3. Change a declared parameter in PartCAD and verify the resulting geometry.
4. Export and reopen a PartCAD object in SolidCraft; inspect what history survives.
5. Inspect and, if needed, run the upstream plugin's Docker image and native CLI setup.
6. Decide whether the integration is useful alongside the simpler Python interface from Experiment 011.

## Start condition / ownership

Begin only when deliberately selected; first create an independent experiment repository (proposed name: `brainboxemb/exp.2026-012.partcad-solidcraft`) with its own pinned upstream dependency and evidence.

Do **not** create a generic shared CAD container or change the existing OpenSCAD toolchain on the basis of this proposal.
