# Migration 005 — runtime image family validation

Status: **validated for architecture selection**

This validation answers one execution-architecture question:

> Can the SCAD runtime be split into a smaller OpenSCAD-focused profile and a full OpenSCAD + PythonSCAD profile without losing the required functional contract, and is the distribution saving large enough to justify capability-driven runtime selection?

The answer is **yes**.

This is architecture evidence only. No production consumer has been migrated by this validation.

## Owner change requests

- architecture/evidence: `brainboxemb/brainboxemb.meta#59`;
- image-family implementation: `brainboxemb/docker.scad-toolchain#6`;
- external qualification: `brainboxemb/docker.scad-toolchain.test#6`.

All three change requests remain draft while Migration 005 continues.

## Exact candidate

The two images came from one `docker.scad-toolchain` source revision:

```text
eeb40e7eff98e98d754baf8ddb52376a17ecef18
```

The candidate images were published with Docker Metadata's immutable shortened SHA tag:

```text
ghcr.io/brainboxemb/scad-toolchain-openscad:sha-eeb40e7
ghcr.io/brainboxemb/scad-toolchain:sha-eeb40e7
```

The existing `scad-toolchain` package remains the full/dual profile for backward compatibility. The prototype does not move `edge` and does not switch existing consumers.

## External qualification boundary

External qualification ran in `brainboxemb/docker.scad-toolchain.test`:

- workflow run: `34992630534`;
- test job: `104460840663`;
- test branch revision: `51b11a975f2417599651b0b8a8eed1ab1f4ed4ac`;
- runner: `ubuntu-24.04`;
- maximum heavy-runner concurrency: **1**.

The same hosted VM tested the profiles sequentially. For this one controlled measurement the local Docker state was cleared between profiles so both pull timings represent cold acquisition rather than letting the full image benefit from the OpenSCAD image's shared layers.

## Distribution measurements

| Profile | Compressed linux/amd64 OCI layers | Docker unpacked size | Cold pull |
| --- | ---: | ---: | ---: |
| OpenSCAD | 328,098,501 bytes | 961,779,232 bytes | 13.211 s |
| Full | 449,516,893 bytes | 1,313,898,129 bytes | 15.464 s |

Difference when an OpenSCAD-only capability can use the smaller profile:

- **121,418,392 fewer compressed bytes**, about 121.4 MB decimal / 115.8 MiB;
- about **27.0% less registry transfer** than the full image;
- **352,118,897 fewer unpacked bytes**, about 352.1 MB decimal / 335.8 MiB;
- about **26.8% less local Docker image size**;
- in this controlled run, cold pull was **2.253 s faster**, about 14.6%.

The byte difference is the stronger architecture signal. Pull time depends on runner location, registry/network conditions and concurrent transfer behaviour, so the single timing sample should not be treated as a guaranteed 2.253-second production saving.

The OpenSCAD image uses nine runtime layers in this candidate. The full image contains those shared layers plus three full-profile layers. The multi-stage build therefore preserves the intended family relationship instead of maintaining two unrelated Dockerfiles.

## Functional qualification

The OpenSCAD-focused image independently passed:

- OpenSCAD PNG and STL generation;
- OpenSCAD -> BOSL2 PNG and STL generation;
- SCons driving OpenSCAD;
- `openscad-docsgen` lint/parse and Markdown generation;
- `openscad-mdimggen` availability;
- Pillow/watermark processing;
- Git/tooling smoke checks.

Its runtime information deliberately reports PythonSCAD, pybosl2 and Shapely as not installed.

The full image passed the same OpenSCAD-facing contract and additionally passed:

- PythonSCAD PNG and STL generation;
- PythonSCAD command-line define behaviour;
- PythonSCAD embedded `sys.path` probe;
- PythonSCAD -> pybosl2 PNG and STL generation.

The two previously documented interoperability boundaries remained explicit XFAILs rather than being silently skipped:

- PythonSCAD -> BOSL2 `.scad` runtime compatibility mismatch;
- PythonSCAD -> OpenSCAD `object()` bridge probe.

This proves that the full image remains a tested functional superset of the OpenSCAD profile.

## Resource-efficiency note about the controlled test

The qualification intentionally forced an independent cold pull for each profile. The current diagnostic workflow uses `docker system prune -af` between them.

That broad prune took about **16 seconds** and reported **1.88 GB reclaimed**, because it removed several unrelated images preloaded on the hosted runner in addition to the candidate image layers.

That cost is useful evidence about the test method, not a recommended lifecycle step. It must **not** become normal production CI behaviour.

For routine external qualification, the architecture should prefer:

- functional testing of both profiles in one VM, allowing their shared layers to be reused locally;
- exact OCI compressed-byte inspection without downloading a second independent copy merely to measure size;
- cold-pull comparison only as an explicit diagnostic/benchmark when distribution performance needs remeasurement.

This preserves the one-runner superset test while avoiding repeated deletion and redownload of shared data.

## Architecture interpretation

The image-family option passes its Migration-005 validation gate:

1. the smaller image has a material transfer/storage reduction;
2. it independently satisfies the normal OpenSCAD production contract;
3. the full image preserves the PythonSCAD capability set and known XFAIL discipline;
4. both can be built from one owner repository and shared multi-stage source;
5. qualification does not require two simultaneous hosted VMs.

The resulting runtime selection rule must be capability-driven, not repository-name-driven:

```text
OpenSCAD-only effective capability set
    -> OpenSCAD runtime

OpenSCAD + PythonSCAD effective capability set
    -> full runtime
```

A repository such as `lib.scad.clamps` or `template.scad-project` must therefore continue to receive the full runtime while it deliberately exposes PythonSCAD capabilities. An OpenSCAD-only consumer such as the current HUB75 library can eventually select the lighter runtime.

The owner for that selection logic is expected to be `tool.scad-project`: GitHub workflow files should not contain a hand-maintained repository allowlist.

## Result

**Architecture validation: passed.**

The remaining work is implementation integration and the other Migration-005 validation items. This result does not by itself authorize migration of production consumers or merge/release of the draft image-family change requests.
