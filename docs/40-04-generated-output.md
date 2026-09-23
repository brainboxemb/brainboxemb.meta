# Generated output and publication

## Why this document exists

This page defines the durable cross-project rules for generated output, publication namespaces and evidence identity. Read it when choosing where generated files belong, how persistent output branches should be named, or how a new implementation domain should align with existing SCAD/Java conventions.

The goal is one recognizable lifecycle across domains without forcing different build systems to use identical mechanics.

## Source to output model

Authored source, generated domain output, orchestration/materialization evidence and persistent publication are separate concerns.

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

Generated files are not committed to the normal source branch merely because they are useful for review or publication.

## Human names versus technical identifiers

Human-facing lifecycle concepts use readable names. Stable technical paths and branch suffixes use the portfolio-wide compact identifiers where such an identifier has been defined.

Canonical mapping:

| Human-facing concept | Technical identifier |
| --- | --- |
| Design | `dsg` |
| Build | `bld` |
| Verification | `vrf` |
| Documentation | `docs` |

This is not a rule that every identifier must have three letters. `docs` remains `docs` because it is already the clear and established technical name. Do not introduce a new abbreviation merely to make a path shorter.

Use the human name in prose, headings, job descriptions and UI labels. Use the technical identifier for stable machine/path identity such as workspace roots, generated-output branch suffixes and equivalent repository-level namespaces.

Do not keep two technical names for the same lifecycle concept in current-generation tooling. For example, Build should not be `bld` locally but `build` on generated branches.

## Persistent publication namespaces

Generated publication uses lifecycle namespaces rather than one shared mutable output branch:

```text
pull request #N
    dev/pr-N/<suffix>

main
    prod/<suffix>

release vX.Y.Z
    rel/vX.Y.Z/<suffix>
```

For the canonical Build and Verification families this means:

```text
dev/pr-N/bld
dev/pr-N/vrf

prod/bld
prod/vrf

rel/vX.Y.Z/bld
rel/vX.Y.Z/vrf
```

A domain may define an additional output family when it represents a genuinely different lifecycle. It should reuse an existing portfolio identifier when the concept is already shared rather than inventing a domain-local synonym.

Historical branches created under an older naming convention remain historical evidence. Normalization applies to current tooling and future publication; immutable release history is not rewritten merely to rename it.

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

Generic cleanup mechanics belong in `tool.git-project` where possible; domain tooling owns which output families it produces.

## SCAD example

Current-generation SCAD projects already use compact workspace identities:

```text
dsg/
    design source/generated design documentation

bld/
    normal Build output

vrf/
    Verification output/evidence
```

Persistent publication uses the same technical identities:

```text
prod/bld
prod/vrf
```

Human-facing documentation still calls these **Build** and **Verification**.

## Cross-domain alignment

Java, SCAD, embedded and future implementation domains should align shared lifecycle concepts and technical namespaces where practical:

```text
affected/preflight -> execute/materialize -> verify -> finalize/publish -> release
```

Equivalent naming does not require equivalent build mechanics. Maven remains Java build/test authority; SCons/OpenSCAD retain SCAD semantics; other domains keep their own engines.

The consistency requirement is that the same portfolio concept should not acquire a different technical name merely because it is implemented by a different domain tool.

## Human-facing files are lifecycle-dependent

A file extension does not define its lifecycle. A PNG may be:

- a presentation render;
- design documentation;
- verification evidence;
- workbench instruction imagery;
- an engineering diagram.

Preserve producer/lifecycle identity rather than routing every Markdown/image through one generic build path.
