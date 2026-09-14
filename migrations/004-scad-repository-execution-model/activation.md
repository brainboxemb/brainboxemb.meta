# Migration 004 activation

Migration 004 was activated after proposal PR #50 was merged.

The first active slice is Step 1 in `brainboxemb/tool.git-project`: add a generic Moon affected/preflight capability that can decide from an explicit VCS base/head range whether a configured repository task is affected, without executing producer commands.

The first consumer-facing acceptance criterion remains: a README-only change in a current SCAD repository must not start the SCAD toolchain container.

Moon replacing SCons remains outside this migration and is tracked separately as parked experiment #51.
