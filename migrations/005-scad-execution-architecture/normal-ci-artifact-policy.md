# Migration 005 — normal CI artifact retention policy

Status: **policy decision validated from current workflows and consumers**

This decision applies to the normal SCAD production lifecycle. It does **not** change release artifact hand-off.

## Decision

Normal CI should retain **compact decision/orchestration evidence by default**, but should **not upload complete Build and Verification trees as GitHub Actions artifacts by default** when those same trees are already published to generated-output branches.

If a future caller deliberately needs a downloadable full output snapshot without normal branch publication, that should be an explicit opt-in capability/policy rather than an unconditional cost paid by every affected run.

Release remains unchanged: release Build and Verification artifacts are a real cross-job hand-off and remain required.

## Current normal lifecycle

The released `tool.scad-project` production workflow currently does all of the following for an affected run:

```text
compact impact evidence
  -> upload Actions artifact, 14 days

Build output
  -> stage complete publication tree
  -> upload complete Actions artifact, 14 days
  -> publish same staged tree to generated-output branch

Verification output
  -> stage complete publication tree
  -> upload complete Actions artifact, 14 days
  -> publish same staged tree to generated-output branch
```

The Build/Verification branch publishers read the local staging directories directly. They do not download the just-uploaded Actions artifacts.

Therefore the full normal-run artifacts are not part of the current technical hand-off.

## Current release lifecycle is different

`project-release.yml` creates separate exact-source release Build and Verification jobs:

```text
release Build job
  -> scad-project-release-build artifact

release Verify job
  -> scad-project-release-verification artifact

release Finalize job
  -> download both artifacts
  -> package / checksum / immutable branches / release assets
```

Those artifacts cross a real job boundary and are consumed by `finalize`. Removing normal production artifacts does not remove or replace this release mechanism.

## Consumer search

A repository-wide search of the current `brainboxemb` sources found normal production callers supplying names such as:

```text
lib-scad-hub75-build-publication
lib-scad-hub75-verification-publication
```

but found no downstream workflow/documented process that downloads those normal artifacts.

No current production caller was found deliberately selecting `publish: false` as its normal lifecycle.

This is not proof that a human has never manually downloaded one. It is sufficient to establish that retained full-tree Actions artifacts are not an encoded product or automation dependency today.

## Measured retained data

Representative final clamps production run `34971400621` currently retains:

| Artifact | Stored ZIP size |
| --- | ---: |
| compact preflight evidence | 4,348 bytes |
| Build publication tree | 144,367 bytes |
| Verification publication tree | 100,556 bytes |

The two full-tree artifacts total **244,923 bytes**, roughly 56 times the compact decision artifact in that small reference.

Representative HUB75 exact-main run `34976840416`, current attempt:

| Artifact | Stored ZIP size |
| --- | ---: |
| compact preflight evidence | 4,674 bytes |
| Build publication tree | 244,219 bytes |
| Verification publication tree | 450,734 bytes |

The two full trees total **694,953 bytes**, roughly 149 times the compact decision artifact.

That workflow run also contains an older rerun attempt with another Build/Verification pair (~699 KB) and another compact preflight artifact. GitHub Actions retention can therefore duplicate complete normal output across attempts even though generated-output publication is already the durable normal-output surface.

These absolute sizes are still small today. The policy decision is about ownership and unnecessary repeated transfer/storage, not pretending that hundreds of kilobytes dominate current CI cost.

## Why compact evidence stays

The small impact-decision artifact has a different purpose from generated CAD output. It records why expensive SCAD production did or did not run and is useful even for an unaffected run where no generated-output branch changes.

Keeping this small evidence for the current 14-day window is proportionate.

The generated Build/Verification branches themselves also contain the orchestration evidence staged with their published output when production runs.

## Proposed normal policy

Default normal affected run:

```text
impact decision
  -> compact retained Actions evidence

source-derived Build / Verification output
  -> local staging
  -> generated-output branch publication
  -> no duplicate full-tree Actions artifact
```

If publication is intentionally disabled and a caller needs downloadable complete output, add an explicit policy such as:

```text
retain_full_output_artifacts: true
```

The exact input name is an implementation detail. The important architecture rule is that full normal artifacts are **opt-in for a concrete consumer need**, not automatic lifecycle machinery.

## Failure/debugging consideration

A failure before branch publication should not force unconditional full-tree retention on every successful run.

Useful failure diagnosis should come from:

- step logs;
- compact orchestration/decision evidence;
- task/evidence files appropriate to the failed capability.

If later experience shows that failed generated trees themselves are routinely needed for debugging, that should be addressed with a failure-only diagnostic artifact rather than restoring unconditional successful-run duplication.

## Architecture result

The normal-CI retained-artifact question is considered **answered** for Migration 005:

- retain compact decision/evidence artifacts;
- stop treating complete normal Build/Verification Actions artifacts as mandatory;
- keep release artifacts because they are real cross-job hand-off;
- allow an explicit future full-output opt-in when a genuine non-publication/download use case exists.

Owner for implementation: `tool.scad-project`.
