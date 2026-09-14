# Generated output and publication

## Purpose

Authored source, generated domain output, orchestration/materialization evidence and persistent publication are separate concerns.

Generated files are not committed to the normal source branch merely because they are useful for review or publication.

## Source to output model

```text
source revision
    authored code / Markdown / configuration / verification source
        ↓
repository-level task orchestration (Moon where adopted)
        ↓
stable domain action
        ↓
domain engine
    SCons / Maven / document producer / validator
        ↓
workspace generated output + domain evidence
        ↓
explicit publication side effect
```

## Repository-level versus domain-level decisions

Where Moon is adopted:

```text
Moon
    high-level repository stages
    task inputs/dependencies/outputs
    execute versus hydrate decision

Domain engine
    concrete domain semantics
    fine-grained incremental decisions
```

A Moon task should represent a meaningful independently useful repository stage. Do not split one domain lifecycle into arbitrary Moon tasks merely for visual symmetry.

Examples:

- SCons remains authoritative for individual SCAD target decisions;
- Maven remains authoritative for the phases of one canonical reactor lifecycle;
- document producers/assemblers retain their own domain contracts.

## Persistent publication namespaces

Generated publication uses lifecycle namespaces rather than one shared mutable build branch:

```text
pull request #N
    dev/pr-N/<suffix>

main
    prod/<suffix>

release vX.Y.Z
    rel/vX.Y.Z/<suffix>
```

Typical suffixes include:

```text
build
verification
docs
bld
```

The suffix is owned by the domain/repository. Common lifecycle semantics do not require unrelated artifact families to use the same suffix.

## Publication is not a producer cache task

Publication consumes output that was already executed or hydrated. It is an external side effect and should remain distinguishable from cacheable producer execution.

This separation allows a current revision to publish an equivalent hydrated result without pretending the producer ran again.

## Evidence identities

Keep three identities separate:

```text
producer evidence
    the execution that actually produced the retained bytes

materialization evidence
    the current repository revision for which orchestration executed or hydrated them

publication context
    where and why that materialization was published
```

If a portable cache hydrates output originally produced by another equivalent revision, do not rewrite producer evidence. Record the current materialization/publication context separately.

## Generated output cleanup

Preview/output cleanup follows the same lifecycle boundaries.

Typical intent:

- `dev/pr-N/*` may be removed when PR N is closed;
- `prod/*` is retained as current production output;
- `rel/vX.Y.Z/*` is immutable release-oriented output;
- cleanup must not delete long-lived output merely because its branch name resembles a feature branch.

Generic cleanup mechanics belong in `tool.git-project` where possible; domain tooling owns which output suffixes/artifacts it produces.

## SCAD-specific example

Current-generation SCAD projects commonly distinguish:

```text
bld/
    normal Build / generated design output

vrf/out/
    verification-only generated evidence
```

At persistent publication level those can remain distinct, for example:

```text
prod/build
prod/verification
```

SCons still owns individual SCAD target decisions inside the domain actions.

## Human-facing files are lifecycle-dependent

A file extension does not define its lifecycle. A PNG may be:

- a presentation render;
- design documentation;
- verification evidence;
- workbench instruction imagery;
- an engineering diagram.

Preserve producer/lifecycle identity rather than routing every Markdown/image through one generic build path.
