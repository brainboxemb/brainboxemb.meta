# Migration 011 — refresh current-generation SCAD baseline

Status: **active**

Tracking issue: [#138](https://github.com/brainboxemb/brainboxemb.meta/issues/138)

Input issue:

- [#116 — audit current tooling state before future cross-project migrations](https://github.com/brainboxemb/brainboxemb.meta/issues/116).

## Why this migration exists

Migration 010 aligned documentation and agent guidance, but the current-generation
SCAD repositories still do not share one current released implementation baseline.

The live repositories show several forms of drift at once:

- most consumers still declare `tool.scad-project v0.15.7`, while newer tool
  releases already exist;
- the HUB75 frame is on a different tool release again (`v0.15.8`);
- `lib.scad.mechint` still declares Forge `v0.2.1` while newer Forge releases
  exist;
- every catalogued current-generation SCAD repository still has root
  `update-repo.ps1` / `update-repo.sh`;
- current `tool.git-project` documentation defines the canonical managed root
  launcher family as `update.ps1` / `update.sh`;
- current `tool.scad-project` consumer documentation still describes the old
  root `update-repo.*` spelling, so the owners themselves disagree;
- open owner issues include a mixture of real blockers, completed-but-left-open
  work and superseded requests.

The goal is therefore not merely "update version numbers". It is to establish one
coherent released owner baseline and then make every modern SCAD consumer agree
with that baseline in dependencies, root launchers and GitHub Actions callers.

## Scope

The rollout scope is derived from the live repository catalog, not a hard-coded
historical migration list.

Included repositories are those with:

```text
project_infrastructure.generation: current
project_infrastructure.provider: tool.scad-project
```

Normal rollout scope:

1. `brainboxemb/template.scad-project`;
2. `brainboxemb/lib.scad.clamps`;
3. `brainboxemb/lib.scad.hub75`;
4. `brainboxemb/lib.scad.forge`;
5. `brainboxemb/lib.scad.util`;
6. `brainboxemb/lib.scad.mechint`;
7. `brainboxemb/2026-009-01.cad.HUB75-display-frame`;
8. `brainboxemb/2026-009-02.cad.hub75-component-lab`.

`brainboxemb/exp.2026-006.scad-library-dependencies` is **not part of the
Migration-011 rollout**. It is a completed PoP/experiment repository retained as
historical qualification/regression evidence. Migration 011 does not reactivate
that PoP and does not update it merely to keep pace with production releases.

Classic/legacy SCAD repositories are explicitly out of scope. Moving a classic
repository to current-generation tooling would be a separate migration.

## Observed starting point

| Repository | Declared tool.scad-project | Other relevant declared refs |
| --- | --- | --- |
| template.scad-project | v0.15.7 | lib.scad.clamps v0.1.1 |
| lib.scad.clamps | v0.15.7 | — |
| lib.scad.hub75 | v0.15.7 | — |
| lib.scad.forge | v0.15.7 | — |
| lib.scad.util | v0.15.7 | — |
| lib.scad.mechint | v0.15.7 | Forge v0.2.1; util v0.4.0 |
| HUB75 display frame | v0.15.8 | Forge v0.3.0; util v0.4.0 plus product libraries |
| HUB75 component lab | v0.15.7 | clamps v0.1.8; mechint v0.1.6 |

All eight normal rollout repositories currently contain root
`bootstrap.ps1/.sh` and legacy `update-repo.ps1/.sh`.

Their GitHub Actions are thin callers, but the exact caller set depends on
repository role. Migration 011 standardises the **filenames and ownership
contract**:

- `.github/workflows/scad.yml` — normal SCAD production/build caller;
- `.github/workflows/release.yml` — only when the repository publishes
  versioned releases;
- `.github/workflows/pr-cleanup.yml` — only when PR preview output exists.

The shared reusable workflows own the substantial CI implementation.


Current observed owner releases before qualification:

- `tool.git-project v0.2.12`;
- `tool.scad-project v0.15.10`;
- `lib.scad.forge v0.3.0`;
- `lib.scad.util v0.4.0`.

These are observations, not automatically the Migration-011 accepted baseline.

## Owner baseline

Consumer rollout starts only after the four shared owners have an accepted
release baseline.

### 1. tool.git-project

First determine whether the existing released `v0.2.12` is already sufficient.

The accepted generic-tool release must prove:

- canonical managed `bootstrap.ps1/.sh` and `update.ps1/.sh` launchers;
- launcher source/version/revision metadata;
- committed bootstrap-gitlink enforcement before mutating operations;
- dirty/stale bootstrap refusal;
- read-only `update.* status`;
- correct generic dependency closure/update behavior;
- exact release/tag self-test evidence.

Do not manufacture a new release if `v0.2.12` already satisfies this contract
on immutable evidence.

### 2. tool.scad-project

The SCAD tool release must consume the accepted generic-tool release and resolve
the owner-side naming/documentation mismatch before rollout.

Blocking owner work includes:

- [tool.scad-project #107](https://github.com/brainboxemb/tool.scad-project/issues/107)
  — align SCAD consumers with canonical managed `update.*` launchers;
- reconcile owner tests, fixtures and consumer docs with the generic launcher
  contract;
- verify the SCAD post-update hook owns only reusable-workflow ref alignment;
- qualify the normal production, release and PR-preview cleanup caller contracts.

The next accepted SCAD release must have exact-main and exact-tag/release
qualification appropriate to the tool's release model.

### 3. lib.scad.forge

Forge should enter the rollout from a coherent pre-1.0 API state rather than
publishing another transitional duplicate surface.

At minimum reconcile:

- [Forge #30](https://github.com/brainboxemb/lib.scad.forge/issues/30) —
  retire the `fg_overlap_mm()` compatibility alias according to the current
  pre-1.0 cleanup policy;
- any already-started resolution-context deprecation/removal work in the current
  Forge plan must be internally consistent at the selected release boundary.

Forge #12 and #13 remain evaluation/future-API questions unless evidence makes
them required; they do not block this baseline merely because they are open.

### 4. lib.scad.util

Complete the already-qualified inspection-only cleanup:

- [util #16](https://github.com/brainboxemb/lib.scad.util/issues/16);
- [util PR #17](https://github.com/brainboxemb/lib.scad.util/pull/17).

The accepted release must contain only the intended util-owned inspection API
and managed inspection consumer controls; the old transform/Forge surfaces must
not remain as a parallel modeling language.

Because this removes released pre-1.0 public API, the release notes/changelog
must state the removal clearly.

## Open-issue audit

Before accepting any owner release, classify related open issues as one of:

```text
blocking current work
superseded / completed-but-left-open
valid non-blocking follow-up
unrelated
```

Known cases requiring explicit disposition:

### tool.git-project

- #4 generic generated-output publication: current README already documents
  released publication interfaces; audit whether the issue is completed and
  should close.
- #16 release preparation before exact-commit tagging: related to meta #20 and
  not automatically a blocker for this SCAD baseline.
- #17 and #26: performance follow-ups, non-blocking unless correctness evidence
  changes.
- #22: duplicate release-request idempotency; release robustness follow-up, not
  automatically a rollout blocker.
- #31 and #32: owner-test/feedback optimisation, non-blocking for consumer
  semantics.

### tool.scad-project

- #107: blocking launcher-contract alignment.
- #80: requests runtime v0.5.1, while later released changelog entries already
  establish runtime v0.6.1; reconcile as superseded rather than implementing
  obsolete work.
- #10: substantial release-publication functionality is already implemented and
  used; reconcile completed portions and any genuinely remaining owner/product
  work instead of leaving one ambiguous historical issue.
- #42: retain only if its audit capability is still independently desired; it is
  not automatically part of this baseline.

### lib.scad.forge

- #30: blocking for the selected cleanup release.
- #12 / #13: non-blocking API evaluations unless deliberately promoted.

### lib.scad.util

- #16 / PR #17: blocking until merged, exact-main qualified and released.

### brainboxemb.meta

- #116 is incorporated by this migration and can close when the owner-state
  audit and baseline reconstruction are retained here.
- #20 remains a deferred generic cross-domain release-flow follow-up.
- Migration 007 / #66 remains separate from this migration.

## Consumer dependency rule

For every in-scope repository, each direct dependency ref and committed gitlink
must be one of:

1. the accepted current release for that dependency; or
2. an explicitly documented historical/alternative pin required by the
   repository's purpose.

For normal maintained consumers there should be no unexplained stale direct pin.

Completed experiment/PoP repositories are outside this rule because their
historical pins are retained evidence, not production dependency policy.

## Managed root launchers

The intended current-generation root interface after rollout is:

```text
bootstrap.ps1
bootstrap.sh
update.ps1
update.sh
```

These are managed copies from the accepted `tool.git-project` release.

Acceptance rules:

- managed headers identify canonical source, source version and exact revision;
- undeclared local divergence is removed by refresh;
- a real local patch is retained only through the documented
  `Managed-Local-Patch` mechanism;
- mutating launchers enforce the committed bootstrap gitlink before delegating;
- `update.* status` remains read-only;
- the SCAD-specific post-update hook only synchronizes SCAD reusable-workflow
  refs;
- root `update-repo.*` is removed unless the accepted owner contract
  deliberately retains it as an explicit compatibility forwarder.

Do not copy substantial dependency/update logic into individual repositories.

## Development/maintenance documentation

Migration 011 also closes a durable documentation gap.

The shared operating rules live in
[`domains/scad/repository-development.md`](../../domains/scad/repository-development.md).

Every maintained in-scope repository gets a concise local:

```text
doc/40-development.md
```

It records the repository-specific developer experience: normal entrypoints,
direct dependencies/version-selection points, workflow set, build/verification/
release path and intentional deviations.

Generic rules are linked rather than copied.

The template currently has `doc/40-ci-orchestration.md`. When the template is
updated last, move that detail page to `doc/40-01-ci-orchestration.md` and make
`doc/40-development.md` the development-family entrypoint.

## GitHub Actions audit

Every in-scope repository must be checked against the accepted
`tool.scad-project` release rather than mechanically receiving the same three
workflow files.

Audit at least:

- the normal SCAD production caller;
- the coordinated release caller where that repository intentionally publishes
  versioned releases;
- PR-preview cleanup where the repository produces preview branches;
- permissions required by the reusable workflow;
- reusable-workflow refs matching the declared accepted
  `tool.scad-project` release;
- absence of duplicated/stale consumer-side orchestration now owned by the tool.

Repository-role differences are valid. For example, a retained lab or
experiment does not need a product release workflow merely for uniformity.

Third-party GitHub Actions version-maintenance policy is **out of scope** here
and remains Migration 007. Migration 011 only proves that the SCAD workflow
shape and released reusable-workflow refs are correct.

## Rollout order

### Phase 1 — owner issue audit

Reconcile the related open issues and establish the exact work required for the
four owners. Close or rewrite stale issues rather than carrying contradictory
requirements into release qualification.

### Phase 2 — generic and SCAD tool baseline

1. accept or replace the `tool.git-project` release;
2. fix #107 and any directly exposed SCAD owner inconsistencies;
3. release/accept the new `tool.scad-project` baseline against that generic
   tool release.

### Phase 3 — Forge and util baseline

1. complete Forge's selected pre-release cleanup and release it;
2. merge/qualify the util inspection-only cleanup and release it.

### Phase 4 — maintained consumer rollout

Roll the accepted owner releases directly through maintained libraries and
projects. This migration assumes the underlying architecture is already
qualified by previous work and owner test suites.

Do not reopen or repurpose Experiment 006 as a qualification step.

If rollout exposes a genuinely new generic behavior that cannot be diagnosed or
qualified cleanly in an owner repository or maintained real consumer, create a
new dedicated qualification/experiment repository with an explicit question.
Do not silently turn a completed PoP repository back into active migration
infrastructure.

### Phase 5 — remaining current-generation consumers

Roll the baseline through the production libraries/projects/lab. For each repo:

- update declared refs and exact gitlinks;
- refresh managed root launchers;
- audit workflows;
- run exact PR-head qualification;
- merge only that qualified revision;
- verify expected exact-main production/publication afterward.

Downstream library ordering must respect released interfaces. For example,
mechint can adopt the new Forge/util releases only after those releases exist.

### Phase 6 — template last

Update `template.scad-project` only after the real repositories have proved the
baseline.

The template records the qualified convention; it does not decide it.

### Phase 7 — closing audit

Re-query the live catalog and prove that every current-generation SCAD
repository is either:

- aligned to the accepted baseline; or
- carrying a documented intentional exception.

Confirm classic repositories remained untouched.

## Completion criteria

Migration 011 is complete only when:

- a qualified generic-tool release is recorded;
- a qualified SCAD-tool release is recorded and the owner docs agree on the
  canonical launcher names;
- qualified Forge and util releases are recorded;
- relevant stale/completed open issues have been reconciled;
- completed PoP/experiment repositories are not updated as part of the rollout;
- all eight normal current-generation SCAD rollout repositories have audited
  direct dependency refs/gitlinks;
- canonical managed root bootstrap/update launchers are installed;
- every maintained rollout repository has `doc/40-development.md` with its local operating summary and exceptions;
- GitHub Actions callers use the standard filenames and match the released SCAD contract for each repository role;
- every intentional old dependency pin is documented as such;
- exact PR/main CI evidence is retained for rollout repositories;
- the template is updated last;
- meta #116 can close with its requested tooling-state audit captured here.

Migration 007, generic release-flow work in meta #20, API-doc publication #125
and unrelated Forge feature evaluations may remain open.
