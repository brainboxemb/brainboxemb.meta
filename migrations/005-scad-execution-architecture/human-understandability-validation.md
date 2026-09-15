# Migration 005 — human-understandability validation

Status: **passed for the target model, with implementation consistency checks required**

## Method

This is an architecture inspection test, not a blind user study.

The test deliberately ignores migration history and chat context. It assumes a maintainer has only:

1. a normal consumer repository;
2. its `project.scad.yml`;
3. the reduced consumer `moon.yml` proven by the inheritance prototype;
4. one linked architecture page describing the shared lifecycle.

The question is whether the maintainer can explain the repository in terms of real SCAD capabilities instead of reconstructing GitHub/Moon/cache/publication machinery.

## What the maintainer sees

### `lib.scad.clamps`

`project.scad.yml` shows:

- OpenSCAD is configured;
- PythonSCAD is configured;
- Verification has two commands and writes to `vrf/out`;
- no SCons build engine is selected;
- publication uses the standard Build/Verification branches.

The reduced Moon configuration shows only:

```text
Capabilities
  Design documentation
  Verification

Project-specific impact
  docs     <- OpenSCAD/PythonSCAD design sources
  verify   <- CAD/API/test/verification sources
```

A maintainer does not see separate tasks for index generation, publication information or synthetic CI roots.

### `lib.scad.hub75`

`project.scad.yml` shows:

- OpenSCAD is configured;
- no PythonSCAD runtime is configured;
- presentation render source is configured;
- `build_engine.engine: scons` is selected;
- Verification is configured;
- publication uses the standard Build/Verification branches.

The reduced Moon configuration shows only:

```text
Capabilities
  Presentation renders
  Design documentation
  Verification

Project-specific impact
  presentation  <- panel/render source
  docs          <- CAD/design source
  verify        <- API/fixture/testcase/verification source
```

## Acceptance questions

### Which SCAD capabilities does the repository have?

**Pass.** They are explicitly visible in the inherited-task include list. The list is two items for clamps and three for HUB75.

### What happens after a README-only change?

**Pass.** Moon compares the exact base and source revision on the host. If none of the capability inputs are affected, CI stops before pulling or starting a CAD image.

### What happens after a CAD-source change?

**Pass.** The same Moon analysis identifies the affected coarse capabilities. Only those capabilities are sent into the one CAD runtime. Whole-capability output may be restored from Moon when source identity matches; otherwise the capability command executes.

### What happens after a presentation-only, docs-only or Verification-only change?

**Pass, with one implementation requirement.** The local input lists make those boundaries visible. The released affected implementation already calculates the complete affected-task set, but the reusable workflow currently exposes only one boolean. Migration 005 implementation must expose the affected capability IDs from that existing query so the runtime receives only the required capabilities.

### Why does Moon exist?

**Pass.** It has two visible responsibilities:

1. determine which coarse SCAD capabilities changed before Docker;
2. reuse a complete capability result when an identical source-derived task result is already cached.

It is not the CAD build engine itself.

### When does SCons exist?

**Pass.** `project.scad.yml` says so explicitly. HUB75 selects SCons and may reuse individual render/documentation targets inside an executing capability. Clamps uses the direct engine and should not restore/save an SCons cache.

### What is cached where?

**Pass.** The architecture page can explain three non-overlapping scopes:

- Moon: complete source-derived capability output;
- SCons, only when selected: individual CAD targets inside a capability;
- GitHub Actions cache: transport of those reusable cache directories between disposable runners.

Normal generated output is published, not treated as another hidden cache layer.

### Why is current-run information separate from reusable source output?

**Pass.** Run/ref/PR/publication data changes every invocation and therefore cannot be part of a stable source-derived Moon identity. Shared finishing code adds truthful current-run information after a capability is executed or restored.

### Why is publication outside Docker?

**Pass.** Publication needs current GitHub credentials/context, not CAD runtime dependencies. Keeping it on the host avoids coupling source-derived CAD output to a particular CI invocation and allows Build/Verification publication to overlap without another CAD container or runner.

### Where does most CI cost go?

**Pass.** The architecture evidence makes this visible rather than implicit:

- unrelated changes: Moon/preflight only;
- affected changes: CAD image distribution is currently the dominant fixed cost on small projects;
- real CAD work is next and may be avoided through Moon/SCons reuse;
- duplicate output artifacts and unused SCons-cache actions are avoidable lifecycle overhead.

### Why is the architecture worth its complexity?

**Pass.** The complexity that remains has measured purpose:

- Moon prevents unnecessary heavy runtime starts and can reuse whole capability output;
- SCons gives fine-grained reuse only where a project actually needs it;
- the split runtime image avoids about 27% registry transfer for OpenSCAD-only work;
- one heavy runner avoids duplicated VM/image setup;
- shared task inheritance removes generic lifecycle topology from consumers;
- host publication can overlap without adding compute infrastructure.

## Configuration-drift guard

The target uses two complementary files:

- `project.scad.yml` describes SCAD project/runtime/build intent;
- `moon.yml` describes the visible capability set and project-specific source-impact boundaries.

That is understandable only if shared tooling prevents contradictions.

`tool.scad-project` validation should therefore check at least:

- a configured presentation/render capability and `scad.build` agree;
- configured Verification and `scad.verify` agree;
- PythonSCAD capability implies the full/dual runtime profile;
- no PythonSCAD capability permits the OpenSCAD-focused profile;
- `build_engine: scons` is the condition for the applicable SCons cache path;
- non-standard Build/Verification output roots provide explicit Moon output overrides when required.

This should fail configuration early rather than relying on maintainers to notice drift manually.

## Result

**The target passes the human-understandability acceptance test.**

Compared with the Migration-004 consumer graph, the maintainer-facing model is now the domain model itself: capabilities and their source-impact boundaries. Shared lifecycle mechanics remain inspectable, but they are no longer copied into every repository.

The remaining work is implementation and end-to-end qualification, not another architecture alternative search.
