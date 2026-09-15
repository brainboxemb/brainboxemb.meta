# Migration 005 — runtime image family workstream

Status: **validation/implementation prototype**

This workstream is part of Migration 005, not a separate migration.

It exists because runtime selection is part of the SCAD execution architecture: projects should only pay for the CAD runtimes and libraries they actually require, while repositories that deliberately support both OpenSCAD and PythonSCAD must keep that capability.

## Active change requests

The work is deliberately split by owner while remaining one Migration-005 workstream:

- architecture/evidence: `brainboxemb/brainboxemb.meta#59`;
- image-family implementation: `brainboxemb/docker.scad-toolchain#6`;
- external two-profile qualification: `brainboxemb/docker.scad-toolchain.test#6`.

These are draft change requests. Production consumers do not move until the qualification gate below is satisfied.

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

## Provisional image family

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

The exact package boundary remains subject to measurement. The first prototype deliberately removes only clearly PythonSCAD-specific content so size/pull differences remain attributable.

## Runtime selection model

Runtime selection should eventually derive from the effective project capabilities rather than hand-written GitHub workflow knowledge.

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

The full image must therefore remain a functional superset of the OpenSCAD capability contract.

The prototype qualification deliberately uses one hosted test runner for both profiles. It pulls/tests them sequentially so the superset proof does not require two simultaneous VMs. Image pull time, compressed OCI bytes and local unpacked size are recorded per profile.

## Validation evidence required before adoption

For both images measure:

- compressed image/layer bytes;
- local unpacked image size;
- fresh hosted-runner pull time;
- container startup time;
- functional qualification status;
- total runner-seconds used for qualification;
- shared versus unique image layers.

Then test at least:

1. an OpenSCAD-only consumer such as the HUB75 library;
2. a dual-runtime consumer such as clamps/template behavior.

## Owners

- cross-project architecture/evidence: `brainboxemb/brainboxemb.meta`;
- image implementation/release: `brainboxemb/docker.scad-toolchain`;
- external image-family qualification: `brainboxemb/docker.scad-toolchain.test`;
- later runtime selection/lifecycle integration: likely `brainboxemb/tool.scad-project`, after the image family is qualified.

## Adoption gate

Do not change production SCAD consumers merely because the prototype image is smaller.

Adoption requires:

- both image profiles independently green;
- full image still proves the existing PythonSCAD-supported routes;
- OpenSCAD image proves all normal OpenSCAD production routes;
- measured pull/compute benefit is material;
- runtime selection can be expressed clearly from project capabilities;
- release/version semantics for the two images are explicit and understandable.
