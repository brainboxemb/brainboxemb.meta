# Migration 005 — Moon shared-capability inheritance validation

Status: **passed**

## Question

Can normal SCAD repositories inherit the shared Moon capability mechanics from their pinned `tools/tool.scad-project` revision while keeping only their actual capabilities and project-specific change-impact patterns in the consumer repository?

The desired consumer model is:

```text
consumer
  which capabilities exist?
  which project sources affect each capability?

shared tool.scad-project
  command
  stable tool inputs
  normal output boundary
  cache policy
```

This is deliberately different from the Migration-004 model, where consumers repeated seven/eight lifecycle tasks including indexes, publication information and synthetic graph roots.

## Controlled validation

Final diagnostic run:

- repository: `brainboxemb/brainboxemb.meta`
- run: `34997339916`
- exact clamps source: `f0dbb82b477201646fc3e2173ccba96d70fb8920`
- exact HUB75 source: `2eaaa540e3658bd3821eb6ec0f2d0352cbefff48`
- shared-task prototype: `brainboxemb/tool.scad-project@1303ae8c40817a98f9615a58762264b3ef19b6dd`
- Moon runtime owner: `brainboxemb/tool.git-project@6234b7437b0dc0115642468f74d1f4a2c2214bef`
- Moon: `2.5.4`
- hosted runners: one Ubuntu 24.04 runner
- Docker/CAD runtime starts: zero

The fixture replaced only the consumer Moon configuration. It did not render CAD output.

## Shared task policy that was tested

The prototype in `tool.scad-project` defines three coarse capabilities:

```text
scad.docs    -> design-build
scad.build   -> presentation renders
scad.verify  -> verification
```

Shared policy owns:

- the `scad-project.sh` command;
- `project.yml`, `project.scad.yml` and `.gitmodules` as common inputs;
- explicit source-controlled `tool.scad-project` inputs (`scad-project.sh`, `pyproject.toml`, `src/**/*.py`);
- standard output boundaries under `bld/...` and `vrf/out/...`;
- Moon whole-capability caching.

The broad Migration-004 input `tools/tool.scad-project/**` is intentionally absent. This prevents generated Python runtime state below `__pycache__` from becoming source identity again.

## Resulting clamps consumer model

The tested effective consumer intent is equivalent to:

```yaml
workspace:
  inheritedTasks:
    include:
      - scad.docs
      - scad.verify

tasks:
  scad.docs:
    inputs:
      - openscad/**
      - pythonscad/**
      - scripts/render-openscad-design.sh

  scad.verify:
    inputs:
      - openscad/**
      - pythonscad/**
      - test/**
      - vrf/README.md
      - scripts/run-verification.sh
      - scripts/build-verification-index.sh
      - bootstrap.sh
      - bootstrap.ps1
      - update-repo.sh
      - update-repo.ps1
      - .github/workflows/**
      - tools/tool.git-project/**
```

The inherited-task file itself is one stable link to the pinned tool policy:

```yaml
extends: '../../tools/tool.scad-project/moon/tasks/scad.yml'
```

Validation proved:

- `scad.docs` exists with the inherited documentation command and shared outputs;
- `scad.verify` exists with the inherited verification command and shared `vrf/out/**` output ownership;
- `scad.build` does **not** exist for clamps;
- local impact patterns were merged into the effective inherited tasks;
- generated test bytecode under `tools/tool.scad-project/src/.../__pycache__/*.pyc` did not become an effective task input.

## Resulting HUB75 consumer model

The tested effective consumer intent is equivalent to:

```yaml
workspace:
  inheritedTasks:
    include:
      - scad.docs
      - scad.build
      - scad.verify

tasks:
  scad.docs:
    inputs:
      - openscad/**/*.scad
      - openscad/**/design/**

  scad.build:
    inputs:
      - openscad/**/*.scad
      - openscad/**/render.yml

  scad.verify:
    inputs:
      - openscad/p5-64x32-panel/hub75_p5_64x32_panel.scad
      - test/**
      - vrf/README.md
      - vrf/fixtures/**
      - vrf/top-left/**
      - vrf/measurement-catalog.yml
      - vrf/physical-panel-validation.md
      - vrf/test-case-template.md
      - scripts/run-verification.sh
      - scripts/build-verification-index.sh
      - bootstrap.sh
      - bootstrap.ps1
      - update-repo.sh
      - update-repo.ps1
      - .github/workflows/**
      - tools/tool.git-project/**
```

Validation proved all three inherited capabilities existed with their shared commands, stable tool inputs and standard output boundaries.

## Standard paths versus overrides

The final prototype moves standard output ownership into shared policy because current consumers already use the standard lifecycle roots:

- Build root: `bld`
- Verification root: `vrf/out`

A repository that deliberately chooses a non-standard output root may need a local output override. That is an exception to shared defaults, not a reason to repeat standard output declarations in every repository.

`tool.scad-project` validation should reject inconsistent capability/output configuration rather than silently allowing Moon and `project.scad.yml` to drift apart.

## Capability and runtime consistency

The consumer capability list is intentionally visible. It should be checked against `project.scad.yml` by shared tooling.

For the reference repositories:

- clamps has `pythonscad:` configuration, so its effective runtime profile is the full/dual image;
- HUB75 has no `pythonscad:` section, so its effective runtime profile is OpenSCAD-focused;
- HUB75 selects `build_engine.engine: scons`, so normal SCons cache handling applies there;
- clamps uses the direct default engine, so generic SCons restore/save must not run there;
- HUB75 has a configured presentation `render_root`, matching `scad.build`;
- both have configured Verification commands, matching `scad.verify`.

The implementation should make these consistency checks explicit so a maintainer cannot accidentally declare contradictory models in two files.

## Impact-query consequence

The released `tool.git-project/moon-affected` implementation already asks Moon once for the complete affected task set and stores it as `affected-tasks.json`. Its public interface currently reduces that result to one boolean for one requested graph root.

The target lifecycle needs the actual human-level affected capabilities, for example:

```text
scad.docs
scad.verify
```

or:

```text
scad.build
```

Therefore the implementation should expose the relevant affected capability IDs from the **same existing Moon query**. It should not run separate change analyses per capability merely to recover information Moon already calculated.

This allows one Docker invocation to receive only the capabilities that need execution/materialisation.

## Conclusion

**Passed.** Native Moon task inheritance from the exact pinned `tool.scad-project` path is sufficient for the target architecture.

No custom Moon-YAML generator is needed. Consumer repositories can be reduced from lifecycle topology to a small capability list plus project-specific impact rules, while the effective task remains inspectable through `moon task ... --json`.
