# Migration 005 — runtime image family workstream

Status: **validated and released as `docker.scad-toolchain v0.5.0`; consumer rollout is part of later migration steps**

## Why this document exists

This document records the runtime-profile part of Migration 005: why one shared Docker source now produces an OpenSCAD-focused image and a full OpenSCAD + PythonSCAD image, how that family is qualified, and which later migration step selects a profile for a consumer.

Detailed controlled evidence is in [14 — Runtime image validation](14-runtime-image-validation.md).

## Owner implementation result

The work is split by owner while remaining one Migration-005 workstream:

- cross-project architecture/evidence: `brainboxemb/brainboxemb.meta`;
- image-family implementation/release: `brainboxemb/docker.scad-toolchain` PR #6;
- external two-profile qualification: `brainboxemb/docker.scad-toolchain.test` PR #6.

Both owner implementation PRs have been merged. `docker.scad-toolchain v0.5.0` was released from exact source:

```text
a56a3aae4b9e0494e6625e75002d96b0a55986a3
```

The immutable `v0.5.0` image pair passed external qualification in workflow run `34999654405`.

This does **not** mean every production consumer has already moved to the new profile-selection model. Runtime selection is integrated later through `tool.scad-project` and the canary migrations.

## Why this belongs in Migration 005

Migration 005 evaluates:

- feedback latency;
- total hosted-runner/compute use;
- runtime/container startup and image distribution;
- Moon capability selection;
- SCons versus direct execution;
- human-understandability of the lifecycle.

The container image was the largest individual latency cost on affected small-project runs. Splitting runtime capabilities is therefore an execution-architecture decision rather than an independent migration.

## Product reality

The ecosystem is not uniformly OpenSCAD-only.

Examples:

- `lib.scad.hub75` currently uses the OpenSCAD path for its reusable library and verification;
- `lib.scad.clamps` intentionally contains both `openscad/` and `pythonscad/` implementations and declares both runtime flag sets;
- `template.scad-project` also carries OpenSCAD and PythonSCAD project support;
- the external toolchain qualification keeps PythonSCAD as an alternative/experimental runtime and records known interoperability XFAILs rather than pretending it is equivalent to OpenSCAD.

Therefore the target does **not** remove PythonSCAD globally.

## Released image family

One owner repository, `brainboxemb/docker.scad-toolchain`, builds two related runtime images from the same source/version:

```text
OpenSCAD runtime
    OpenSCAD
    BOSL2
    docsgen / mdimggen
    Pillow + watermark tooling
    SCons
    Git / Xvfb / required runtime libraries

Full / dual runtime
    FROM the OpenSCAD runtime capability set
    + PythonSCAD
    + pybosl2
    + Shapely
    + PythonSCAD-specific runtime dependencies
```

The existing package remains the full/dual compatibility image:

```text
ghcr.io/brainboxemb/scad-toolchain:v0.5.0
```

The focused package is:

```text
ghcr.io/brainboxemb/scad-toolchain-openscad:v0.5.0
```

The earlier architecture candidate came from exact Docker source:

```text
eeb40e7eff98e98d754baf8ddb52376a17ecef18
```

and was qualified as immutable candidate tags before the production release:

```text
ghcr.io/brainboxemb/scad-toolchain-openscad:sha-eeb40e7
ghcr.io/brainboxemb/scad-toolchain:sha-eeb40e7
```

## Qualification result

Controlled external run `34992630534`, job `104460840663`, qualified both candidate profiles sequentially on one `ubuntu-24.04` hosted VM.

| Profile | Compressed OCI bytes | Unpacked bytes | Controlled cold pull |
| --- | ---: | ---: | ---: |
| OpenSCAD | 328,098,501 | 961,779,232 | 13.211 s |
| Full | 449,516,893 | 1,313,898,129 | 15.464 s |

For an OpenSCAD-only capability this removes:

- 121,418,392 compressed bytes, about **27.0%** of full-image registry transfer;
- 352,118,897 unpacked bytes, about **26.8%** of local image size.

The one controlled timing sample was 2.253 s faster for the smaller image. That timing is supporting evidence only because network variance is significant; the exact byte reduction is the stronger resource-cost signal.

Functionally:

- the OpenSCAD image passed OpenSCAD PNG/STL, BOSL2, SCons, documentation generation, watermark/Pillow and Git/tooling tests;
- the full image passed that same shared contract;
- the full image additionally passed PythonSCAD PNG/STL, define/path probes and pybosl2 tests;
- the documented PythonSCAD interoperability XFAILs still matched their intended failure boundaries.

The full profile is therefore a tested functional superset rather than merely a larger package.

The released `v0.5.0` pair was subsequently qualified again by the external test repository, so the production release is not relying only on the candidate-SHA experiment.

## Runtime selection model

Runtime selection derives from the effective project capabilities rather than hand-written GitHub workflow knowledge.

Conceptually:

```text
OpenSCAD-only project/capabilities
    -> OpenSCAD runtime

OpenSCAD + PythonSCAD project/capabilities
    -> full/dual runtime
```

A repository such as `lib.scad.clamps` must not silently lose PythonSCAD validation merely because the primary reusable-library direction is OpenSCAD.

This is a capability rule, not a repository-name allowlist. The integration owner is `tool.scad-project`, which should derive the required runtime from the effective project model so a repository can change capability without editing GitHub orchestration by hand.

## Qualification model

Keep one external qualification repository: `brainboxemb/docker.scad-toolchain.test`.

Do not split it into separate repositories. Qualify the family as one contract:

| Capability | OpenSCAD image | Full image |
| --- | ---: | ---: |
| OpenSCAD PNG/STL | required | required |
| native BOSL2 | required | required |
| docsgen/mdimggen | required | required |
| watermark/Pillow | required | required |
| SCons OpenSCAD consumer | required | required |
| Git/tooling basics | required | required |
| PythonSCAD PNG/STL | not required | required |
| PythonSCAD define/path behavior | not required | required |
| pybosl2 | not required | required |
| PythonSCAD interoperability/XFAIL probes | not required | required |

The full image must remain a functional superset of the OpenSCAD capability contract.

Routine qualification uses one hosted test runner for both profiles and permits shared Docker layers to remain local. The one-time independent cold-pull benchmark deliberately cleared Docker state between profiles; its broad `docker system prune -af` cost about 16 s and removed 1.88 GB of mostly unrelated hosted-runner images, so that behaviour is **not** normal CI policy.

## Remaining adoption work

The image-family implementation itself is released. Consumer adoption still requires the later Migration-005 layers to:

- make `tool.scad-project` select the runtime from effective project capabilities;
- prove an OpenSCAD-only consumer through the focused image;
- prove a dual-runtime consumer such as clamps/template through the full image;
- avoid adding repository-specific image selection to GitHub workflow files;
- record the resulting end-to-end runner/resource measurements.

Those tasks are tracked in [06 — Implementation plan](06-implementation-plan.md).
