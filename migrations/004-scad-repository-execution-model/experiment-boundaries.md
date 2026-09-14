# Experiment boundaries for Migration 004

Migration 004 deliberately does **not** decide whether Moon should replace SCons as the fine-grained SCAD target engine.

That question is technically interesting because Moon also supports task inputs, outputs, affected state, caching and hydration. However, the current `tool.scad-project` SCons path already has qualified target-level behaviour based on the engine-independent OpenSCAD dependency scanner.

Trying to replace that engine while simultaneously changing repository orchestration, Build/Verify execution and the pre-container gate would make the migration too broad to evaluate reliably.

## Migration 004 keeps

For Migration 004, SCons remains the qualified fine-grained SCAD target engine.

The migration may change:

- the repository-level CI lifecycle;
- Moon task wiring at repository level;
- Build/Verify aggregation;
- pre-container affected/preflight decisions;
- publication placement;
- project-versus-library execution differences.

It must not change the proven target-level dependency/rebuild semantics merely to simplify the stack.

## Separate experiment

A later `tool.scad-project` experiment may compare the current Moon + SCons model with a Moon-only or Moon-dominant target model.

That experiment must prove, at minimum, that any replacement preserves the current useful properties:

- per-target selective invalidation;
- transitive `use`/`include` dependency handling;
- static `import`/`surface` dependencies;
- conservative handling of dependencies that cannot be resolved safely;
- cold, unchanged and selective-change behaviour;
- cache/hydration correctness;
- Build/Verify evidence with understandable ownership.

Until that experiment demonstrates a better model, Migration 004 must treat SCons as an implementation dependency, not as a redesign target.
