# Migration 005 — validated target architecture

Status: **validated — implementation not yet complete**

This is the selected SCAD execution architecture after Migration-005 validation. The remaining work belongs to owner-repository implementation and end-to-end qualification; later evidence may correct details, but there is no longer an open architecture-variant search.

Related:

- [Migration 005 README](README.md)
- [Measured evidence](measurements.md)
- [Moon inheritance validation](moon-inheritance-validation.md)
- [Human-understandability validation](human-understandability-validation.md)
- [Target resource budget](target-resource-budget.md)
- [Implementation plan](implementation-plan.md)

## 1. Maintainer model

A SCAD repository maintainer should normally think about only the capabilities the repository actually provides.

`lib.scad.clamps`:

```text
Design documentation
Verification
```

`lib.scad.hub75`:

```text
Presentation renders
Design documentation
Verification
```

A maintainer should not hand-maintain separate Moon tasks for Build indexes, current source/tool information, source-impact graph roots, publication graph roots, cache transport or publication staging.

## 2. Responsibility split

```text
GitHub Actions
  event, exact source/base, credentials, hosted runner
        |
        v
Moon on host
  determine affected SCAD capabilities once
  none -> stop before CAD image/runtime
        |
        v
one capability-appropriate SCAD runtime
  Moon executes or restores affected whole capabilities
        |
        +-- tool.scad-project capability command
               |
               +-- direct execution, or
               +-- SCons fine-grained targets when configured
        |
        v
host finishing/publication
  current source/tool/run information
  compact retained evidence
  Build/Verification branch publication
```

The normal design uses one heavy hosted runner and one CAD runtime.

## 3. Moon role

Moon stays for two measured reasons.

### Change-impact selection

Before Docker, Moon answers:

```text
Which coarse SCAD capabilities are affected by base -> source?
```

An unrelated change can therefore finish without acquiring the CAD image.

The released generic affected implementation already computes the complete affected-task set. Migration-005 implementation must expose the relevant capability IDs from that same query instead of reducing all information to one boolean.

### Whole-capability reuse

Moon may restore a complete source-derived capability result when task identity matches.

This was validated on a fresh runner. The earlier cache failure was caused by our broad `tools/tool.scad-project/**` input admitting generated `.pyc` files; it was not a Moon cache-model failure.

Shared policy therefore uses explicit source-controlled tool inputs.

## 4. Shared Moon policy ownership

Standard SCAD tasks live in pinned `tool.scad-project` and are inherited through Moon's native workspace task inheritance.

Validated shared capabilities:

```text
scad.docs
scad.build
scad.verify
```

Shared policy owns:

- capability command;
- common stable config/tool inputs;
- standard output boundary;
- Moon cache policy.

Consumer repositories declare only:

1. which capabilities they expose;
2. project-specific source-impact patterns;
3. exceptional output overrides only when they intentionally depart from the standard lifecycle roots.

The validated inheritance form is a single link such as:

```yaml
extends: '../../tools/tool.scad-project/moon/tasks/scad.yml'
```

No custom YAML generator is required.

## 5. Project intent and consistency

`project.scad.yml` remains the SCAD-domain project model. It already describes items such as:

- Build/output roots;
- presentation render root;
- Verification commands/output root;
- OpenSCAD/PythonSCAD configuration;
- selected build engine;
- publication branches/policy.

The reduced Moon model complements that with the visible capability set and source-impact boundaries.

Shared validation must reject contradictions between the two representations. At minimum:

- presentation/render configuration and `scad.build` agree;
- Verification configuration and `scad.verify` agree;
- PythonSCAD configuration implies the full/dual runtime;
- OpenSCAD-only configuration permits the focused runtime;
- `build_engine: scons` controls applicable SCons-cache handling;
- non-standard output roots provide compatible Moon output overrides.

## 6. Runtime image family

One `docker.scad-toolchain` repository owns one related image family from one multi-stage source.

### OpenSCAD-focused profile

Contains the normal OpenSCAD production contract, including:

- OpenSCAD;
- BOSL2;
- documentation tooling;
- Pillow/watermark support;
- SCons;
- required system/runtime tools.

### Full/dual profile

Is the OpenSCAD profile plus:

- PythonSCAD;
- pybosl2;
- Shapely;
- related PythonSCAD dependencies.

Validated compressed sizes:

- OpenSCAD-focused: 328,098,501 bytes;
- full/dual: 449,516,893 bytes.

OpenSCAD-only work therefore avoids about 121 MB / 27% of full-image compressed distribution.

Runtime selection is derived from effective project capabilities/configuration, never a repository-name allowlist.

## 7. SCons role

SCons is optional fine-grained target reuse inside capabilities that explicitly select it.

```text
Moon
  decides/reuses a whole capability

SCons, when configured
  decides/reuses individual targets inside that capability
```

Evidence distinguishes the reference cases:

- clamps: direct engine; no useful SCons cache exists;
- HUB75: SCons engine; normal SCons cache is populated and warm reuse is effective.

The workflow must not restore/save SCons caches for direct projects merely because SCons support exists elsewhere in the ecosystem.

A separate Verification SCons cache exists only if a real Verification engine populates it.

## 8. Source identity versus current-run information

Source-derived cached capability output must depend only on stable source/tool/config state.

Values such as these must not define Moon source identity:

```text
GitHub run id
PR number
current ref
publication branch/context
```

After capabilities are executed or restored, shared host finishing adds truthful current source/tool/run information required for publication.

This preserves both reusable source output and accurate current-run evidence.

## 9. GitHub Actions role

GitHub Actions is a thin lifecycle/credentials shell:

1. resolve exact source and comparison base;
2. ask Moon once which capabilities changed;
3. stop when none changed;
4. select one runtime image from effective project capability/configuration;
5. restore only applicable caches;
6. execute/materialise only affected capabilities in one Docker process;
7. validate output;
8. add current-run information;
9. publish/retain output according to explicit policy.

Repository-specific CAD logic does not belong in the reusable workflow.

## 10. Normal artifact policy

Normal successful production does not need duplicate complete Build/Verification Actions artifacts because same-job publication already uses local staging trees.

Default policy:

- retain compact impact/orchestration evidence;
- publish generated Build/Verification branches;
- do not upload complete normal output trees again merely for retention.

A future manual-download/non-publication use case may opt in explicitly.

Release is different: its separate Build/Verify/finalize jobs require exact-source cross-job artifact hand-off, so release artifacts remain mandatory.

## 11. Publication

Build and Verification publication remain separate logical outputs, but the released publisher is isolated per call and can safely run concurrently on the same host.

Validation proved two publications can overlap, publish correct independent branch trees and clean up without a second runner.

The target therefore allows same-runner publication overlap when useful. It does not add another hosted runner for finishing work.

## 12. Resource/latency objective

The architecture optimises two axes separately:

- feedback latency;
- total compute/resource demand.

It prefers, in order:

1. eliminate work;
2. reuse work at the appropriate layer;
3. reduce image distribution cost;
4. overlap independent finishing work on the same runner;
5. add heavyweight parallel infrastructure only if later measured requirements justify its extra resource cost.

The detailed acceptance budget is in [target-resource-budget.md](target-resource-budget.md).

## 13. Human-understandability result

The selected model passes the Migration-005 inspection test.

With a consumer repository plus this architecture page, a maintainer can identify:

- repository capabilities;
- change-impact boundaries;
- why Moon exists;
- when SCons exists;
- runtime profile choice;
- cache scopes;
- why current-run information is outside cached source identity;
- why publication stays outside Docker;
- where latency/resource cost is concentrated.

See [human-understandability-validation.md](human-understandability-validation.md).

## 14. Deliberately rejected long-term models

### Seven/eight lifecycle tasks copied into every consumer

Rejected. Generic finishing mechanics are not repository capabilities.

### Moon only as a boolean pre-Docker gate

Rejected as the preferred model. Stable Moon whole-capability reuse is proven and the affected query already knows more than one boolean.

### Remove Moon entirely

Rejected. Change-impact value and whole-capability reuse are both measured.

### Return to two heavy hosted jobs merely to regain latency

Rejected as the default. It duplicates runner/image/runtime setup. Migration 005 first removes work and uses same-runner/internal overlap.

## 15. Validation outcome

Architecture validation is complete:

- Moon change-impact value — passed;
- stable Moon whole-capability cache — passed;
- SCons optional/fine-grained boundary — passed;
- warm HUB75 SCons reuse — passed;
- two-profile runtime image family — passed;
- normal artifact retention decision — complete;
- same-runner concurrent publication — passed;
- native shared Moon task inheritance — passed;
- concrete clamps/HUB75 reduced consumer model — passed;
- human-understandability inspection — passed;
- latency/resource budget — established.

The next work is the owner-specific implementation sequence in [implementation-plan.md](implementation-plan.md).

`2026-009-01.cad.HUB75-display-frame` remains intentionally deferred until the shared tools and both reference canaries are released and qualified.
