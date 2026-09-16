# 02 — Current state

## Repository owner map

The canonical catalog currently identifies this Java chain:

```text
tool.git-project
    generic bootstrap / dependency gitlinks / Moon / generated output

        ↓

tool.java-project
    Java build, verification, toolchain and reusable workflow semantics

        ↓

template.java-project
    reference consumer

        ↓

2026-010-02.java.event-timing-framework
    real current-generation downstream consumer
```

The event-timing software meta repository owns product planning/architecture, not generic Java build infrastructure.

## `tool.java-project`

Current release: **v0.2.0**.

The tool already centralises important domain behavior:

- exact Java baseline: Temurin `8.0.504+1`;
- Maven `3.9.16`;
- Maven Wrapper `3.3.4`;
- canonical runner: Ubuntu 24.04;
- compatibility runner: Windows 2025;
- canonical Maven producer and test evidence;
- `brainboxemb.execution-evidence` producer envelope and canonical execution log;
- reusable Windows compatibility workflow;
- reusable Java publish workflow;
- release/self-test workflows.

Its older all-in-one `reusable-java-verify.yml` already proves an important owner boundary: the canonical Linux Maven action and Windows compatibility can be shared. However, current consumers do not simply call one current-generation shared production workflow; they reconstruct significant orchestration around lower-level building blocks.

## `template.java-project`

Current Java tool dependency is semantic `tool.java-project v0.2.0` with an exact committed gitlink.

The current `java-verify.yml` is about 8.4 kB and owns six logical hosted jobs/lanes in a normal main run:

1. `bootstrap-windows`;
2. `linux-canonical`;
3. `verify-test-summary`;
4. Windows canonical-artifact smoke;
5. Windows compatibility build;
6. generated-output publication.

The consumer itself currently owns or hard-codes:

- Windows bootstrap checks and exact tool SHAs;
- full-history blobless Linux checkout (`fetch-depth: 0`);
- exact `actions/setup-java` configuration;
- direct `tool.git-project/moon@v0.2.2` invocation;
- canonical output/evidence assertions;
- staging Moon logs/materialization into a publication tree;
- artifact upload for the Linux JAR;
- artifact upload/download solely for prepared publication hand-off;
- exact-SHA reusable Windows and publish callers;
- an extra job to download and re-verify already-produced publication evidence.

The template currently has **no GitHub project releases**. This is a notable difference from the SCAD reference consumer and should be evaluated as part of the reference-consumer contract rather than assumed to be either correct or wrong.

## `2026-010-02.java.event-timing-framework`

The real downstream repository demonstrates that the same pattern expands substantially with product needs.

Its `java-verify.yml` is about 19.4 kB and the current main workflow contains ten jobs, of which seven normally execute on a non-release main push and three release-only jobs are skipped.

Product-specific responsibilities that correctly belong in the downstream repository include:

- Maven/project version interpretation;
- CHANGELOG/tag semantics;
- failed release tag archival policy;
- application/framework artifact names;
- product-specific dependency-boundary assertions;
- product release assets and release notes.

But the same workflow also repeats generic/shared lifecycle mechanics:

- Windows bootstrap and exact shared-tool SHA assertions;
- full-history Linux checkout;
- JDK setup;
- direct `tool.git-project/moon@v0.2.2` invocation;
- evidence staging and a later evidence-download verification job;
- exact-SHA Windows reusable call;
- prepared-publication artifact hand-off;
- separate generated-output publication runner.

The framework already has successful real releases (`v0.0.1`, `v0.1.0`), including application/framework JARs, checksum files and release evidence. Migration 006 must preserve these product release semantics while reducing generic lifecycle duplication.

## Generic repository tooling gap

Current consumers use the older direct Moon action (`tool.git-project/moon@v0.2.2`) rather than the newer generic affected-query model released later in `tool.git-project`.

Consequences:

- normal workflows do not have an early, domain-neutral base→head impact decision that can terminate unrelated changes before Java setup;
- Linux canonical jobs fetch complete history even though newer generic repository tooling has demonstrated exact shallow base/head strategies;
- consumer workflows own current materialization staging rather than receiving a higher-level production contract.

Whether all newer SCAD-era generic mechanisms apply to Java must still be verified; they should not simply be copied because their version number is newer.

## Runtime/toolchain model

There is no current `docker.java-toolchain` repository in the canonical catalog.

That is not automatically a defect. Java's exact setup currently comes from:

- a pinned `actions/setup-java` action revision;
- exact Temurin version;
- Maven Wrapper validation against exact Maven/wrapper versions;
- native Ubuntu and Windows runners.

A dedicated container could improve Linux runtime immutability but cannot replace the independent native Windows lane. It could also add image-pull overhead for a toolchain that `setup-java` currently installs quickly. Migration 006 must measure this before choosing a runtime model.

## Evidence model

Java already has strong producer evidence compared with many generic CI setups:

- canonical execution JSON/log;
- Java toolchain build provenance;
- Surefire test evidence and readable test summary;
- current Moon materialization JSON/log;
- generated-output README evidence navigation;
- exact Linux-produced artifact smoke on Windows.

Missing or weaker current-run observability compared with the final SCAD model includes:

- no durable coarse workflow phase timings;
- no single shared run-context record across preflight/materialization/publication;
- no early affected decision evidence for unrelated changes because there is no preflight gate;
- current publication staging/verification spread across consumer jobs rather than one owner-controlled lifecycle.

## Preliminary ownership assessment

Likely owner-local responsibilities:

### `tool.git-project`

- generic exact source/base resolution helpers;
- generic affected-task query;
- Moon runtime/cache/materialization mechanics;
- generic generated-output publication/cleanup.

### `tool.java-project`

- Java capability definitions and source-impact interpretation;
- JDK/Maven/Maven-Wrapper policy;
- canonical Maven producer/test evidence;
- Java-specific materialization validation;
- Windows compatibility semantics;
- Java production orchestration around those capabilities;
- Java release building blocks where genuinely generic across Java consumers.

### Consumer/template

- project configuration;
- project-specific source-impact additions/overrides;
- artifact names/smoke expectations when project-specific;
- minimal triggers/permissions/options;
- project-specific release semantics only where they cannot be generic.

This boundary is provisional and must be validated before activation.
