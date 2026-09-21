# Migration 008 — adopt transitive SCAD library dependencies

Status: **complete**

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

Production owners:

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

## Rollout sequence

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

## Completion evidence

Migration 008 is complete.

Released production owners:

- `tool.git-project v0.2.9` / exact
  `9879da589101f41b2b0e634d196ddcc51e1a6102`;
- `tool.scad-project v0.15.2` / exact
  `70fd4162731484a949dc390e942dde8b8d811f10`;
- `template.scad-project` production qualification run `35652899229` — green.

The retained Experiment 006 regression lab then ran DEP-01 through DEP-07,
normal dependency entrypoints and SCAD production against those released owners.
Exact regression head
`85a30b56307d5fac72c6389b5e34c9812a6b6881` passed all nine workflows and
merged through PR #11 as
`8ff28e04c6ca4a2e04371eada7e210166fc17183`.

The representative real production-library chain is also qualified:

- `lib.scad.mechint` PR #21 exact head
  `58331707741bc009ecc589a33861ca055a91fa48`;
- PR production run `35657957029` — green;
- merged main source
  `37a2a4fedb647cc81780f7734d57dbadb8629b10`;
- exact-main production run `35658098181` — green;
- the existing `lib.scad.util v0.1.0` dependency remains pinned to
  `5c88cd9b6b118d376825927ed67e26aff6eaee2d`;
- qualification proves that util is initialized through its
  `role: external` ownership while util's own nested tooling gitlinks remain
  uninitialized.

No new library dependency was manufactured for the migration. Future adoption
is demand-driven: libraries/consumers should use this released model when they
have a real nested runtime-library dependency, not merely to broaden rollout.
