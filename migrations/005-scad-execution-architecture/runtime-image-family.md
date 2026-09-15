# Migration 005 — runtime image family workstream

Status: **architecture validation passed; production adoption not started**

This workstream is part of Migration 005, not a separate migration.

It exists because runtime selection is part of the SCAD execution architecture: projects should only pay for the CAD runtimes and libraries they actually require, while repositories that deliberately support both OpenSCAD and PythonSCAD must keep that capability.

Detailed evidence: [runtime-image-validation.md](runtime-image-validation.md).

## Active change requests

The work is deliberately split by owner while remaining one Migration-005 workstream:

- architecture/evidence: `brainboxemb/brainboxemb.meta#59`;
- image-family implementation: `brainboxemb/docker.scad-toolchain#6`;
- external two-profile qualification: `brainboxemb/docker.scad-toolchain.test#6`.

These remain draft change requests. Production consumers do not move merely because the architecture experiment passed.

## Why this belongs in Migration 005

Migration 005 already evaluates:

- feedback latency;
- total hosted-runner/compute use;
- runtime/container startup and image distribution;
- Moon capability selection;
- SCons versus direct execution;
- human-understandability of the lifecycle.

The container image is currently the largest individual latency cost on affected small-project runs. Splitting runtime capabilities is therefore an execution-architecture decision rather than an independent migration.

## Current product reality

The ecosystem is not uniformly OpenSCAD-only.

Examples:

- `lib.scad.hub75` currently uses the OpenSCAD path for its reusable library and verification;
- `lib.scad.clamps` intentionally contains both `openscad/` and `pythonscad/` implementations and declares both runtime flag sets;
- `template.scad-project` also carries OpenSCAD and PythonSCAD project support;
- the external toolchain qualification keeps PythonSCAD as an alternative/experimental runtime and records known interoperability XFAILs rather than pretending it is equivalent to OpenSCAD.

Therefore the target must **not** remove PythonSCAD globally.

## Validated image family

Keep one owner repository: `brainboxemb/docker.scad-toolchain`.

Build two related runtime images from the same source/version:

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

The prototype keeps the existing `ghcr.io/brainboxemb/scad-toolchain` package as the full/dual runtime for compatibility and introduces `ghcr.io/brainboxemb/scad-toolchain-openscad` for the OpenSCAD-focused profile. This avoids forcing existing dual-runtime consumers to migrate merely to perform the architecture experiment.

The externally qualified candidate came from exact Docker source:

```text
eeb40e7eff98e98d754baf8ddb52376a17ecef18
```

and was tested as:

```text
ghcr.io/brainboxemb/scad-toolchain-openscad:sha-eeb40e7
ghcr.io/brainboxemb/scad-toolchain:sha-eeb40e7
```

## Qualification result

External run `34992630534`, job `104460840663`, qualified both profiles sequentially on one `ubuntu-24.04` hosted VM.

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

## Runtime selection model

Runtime selection should derive from the effective project capabilities rather than hand-written GitHub workflow knowledge.

Conceptually:

```text
OpenSCAD-only project/capabilities
    -> OpenSCAD runtime

OpenSCAD + PythonSCAD project/capabilities
    -> full/dual runtime
```

A repository such as `lib.scad.clamps` must not silently lose PythonSCAD validation merely because the primary reusable-library direction is OpenSCAD.

This is a capability rule, not a repository-name allowlist. The eventual integration in `tool.scad-project` should derive the required runtime from the effective project model so a repository can change capability without editing GitHub orchestration by hand.

## Qualification model

Keep one external qualification repository: `brainboxemb/docker.scad-toolchain.test`.

Do not split it into separate repositories. Instead qualify the family as a matrix:

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

Routine qualification should still use one hosted test runner for both profiles. Unlike the one-time benchmark, it should allow shared Docker layers to stay local instead of deleting and redownloading them merely to simulate two independent cold pulls.

Cold-pull benchmarking can remain an explicit diagnostic. The validation run's broad `docker system prune -af` cost about 16 s and removed 1.88 GB of mostly unrelated hosted-runner images, so it is not an appropriate normal-CI step.

## Owners

- cross-project architecture/evidence: `brainboxemb/brainboxemb.meta`;
- image implementation/release: `brainboxemb/docker.scad-toolchain`;
- external image-family qualification: `brainboxemb/docker.scad-toolchain.test`;
- runtime selection/lifecycle integration: `brainboxemb/tool.scad-project` after the image family is adopted.

## Adoption gate

Architecture validation of the image family has passed, but production adoption still requires the integration path to be explicit.

Before consumers move:

- retain one understandable release/version relationship for both profiles;
- make `tool.scad-project` select the runtime from effective project capabilities;
- prove at least one OpenSCAD-only consumer through the smaller image;
- prove a dual-runtime consumer such as clamps/template through the full image;
- avoid adding repository-specific image selection to GitHub workflow files;
- keep routine external qualification resource-proportionate.

No production consumer is changed by this document or by the current draft PRs.
