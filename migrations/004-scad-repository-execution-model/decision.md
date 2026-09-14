# Migration 004 execution decision

The migration is active.

Selected direction:

- one recognizable SCAD production lifecycle across current projects and libraries;
- Moon for repository-level orchestration and affected/preflight decisions;
- SCons retained as the qualified fine-grained SCAD target engine;
- Build and Verify remain logically independent;
- one heavy SCAD container job only when repository/task impact requires it;
- host-side preflight before container startup;
- publication outside the SCAD container.

`template.scad-project` is the reference project and `lib.scad.clamps` the reference library.

The separate Moon-versus-SCons target-engine question is parked in meta issue #51.
