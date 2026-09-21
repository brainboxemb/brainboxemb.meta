# Migration 008 — adopt transitive SCAD library dependencies

Status: **active**

Tracking issue: [#100](https://github.com/brainboxemb/brainboxemb.meta/issues/100)

Source PoP:
[Experiment 006](../../experiments/006-transitive-scad-library-dependencies/README.md)
— complete.

## Goal

Adopt the dependency contract qualified by Experiment 006 in the production
owners without changing the developer experience into a collection of special
dependency commands.

Normal use should remain:

```text
bootstrap
update-repo
update-repo status
normal SCAD build / production
```

## Qualified baseline

Experiment 006 proved:

- only owner-declared `role: external` git-submodule dependencies are followed
  transitively;
- nested tooling is not recursively initialized;
- owner-local refs remain independent, including two pins of the same repository;
- direct desktop OpenSCAD works without global `OPENSCADPATH`;
- SCons discovers nested sources and invalidates only real consumers;
- dirty nested worktrees block revision-changing updates;
- uninitialized nested dependencies are reported and restored safely;
- build evidence can record the exact owner/path/ref/revision actually used by a
  target, based on the normal SCons source graph.

Final PoP source:
`16f36faf2ff9e2c19f5df6d23121c46ca9c33af4`.

## Production ownership

Expected owners if the migration is activated:

- **tool.git-project**
  - controlled transitive external closure;
  - normal bootstrap/update/status integration;
  - cycle and dirty-worktree protection;
  - owner-local ref/path handling;
  - explicit rather than guessed dependency removal.
- **tool.scad-project**
  - integrate exact dependency provenance with normal SCAD producer/build
    evidence;
  - derive provenance from the actual build dependency graph rather than all
    initialized submodules.
- **template.scad-project**
  - reference-consumer qualification of the released behaviour.
- **selected libraries/consumers**
  - adopt released tooling only where they actually declare/use nested runtime
    libraries;
  - preserve product/library ownership of dependency intent.

## Likely rollout sequence

1. reproduce the PoP contract in owner tests before changing released behaviour;
2. implement/release the generic dependency closure in `tool.git-project`;
3. implement/release SCAD dependency provenance in `tool.scad-project`;
4. qualify the releases through `template.scad-project`;
5. move the Experiment 006 fixture from prototype adapters to the released
   owner behaviour and retain all DEP regressions;
6. update a representative real library/consumer chain such as
   `lib.scad.mechint -> lib.scad.util`;
7. only then broaden adoption where there is a real dependency need.

Do not manufacture new library dependencies merely to demonstrate the migration.

## Current status

Migration 008 is active.

The first blocking step is `tool.git-project`: reproduce the already-qualified
Experiment 006 closure/status/update contract in owner tests before changing
released generic behaviour. The PoP remains the regression oracle; production
implementation should preserve that contract rather than redesign it.

Later owner steps remain blocked until the preceding owner has qualified and
released its part of the contract.
