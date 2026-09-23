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

- `.github/workflows/self-ci.yml` — normal SCAD CI/build caller;
- `.github/workflows/self-release.yml` — only when the repository publishes
  versioned releases;
- `.github/workflows/self-pr-cleanup.yml` — only when PR preview output exists.

The shared reusable workflows own the substantial CI implementation. Owner-side
`workflow_call` interfaces use `reusable-<capability>.yml`; repository-local
event/manual entry workflows use `self-<operation>.yml`; qualification
workflows use `test-<capability>.yml`.


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

**Accepted baseline: `v0.2.14`.**

`v0.2.13` was initially accepted, but the first Forge Migration-011 rollout
(PR #33, failed run `35888314845`) exposed a generic managed-launcher
regression: an uninitialized `tools/tool.git-project` gitlink path could resolve
Git's top-level to the dirty parent consumer worktree and be refused as though
the bootstrap engine itself were dirty.

Owner issue #42 / PR #43 fixed that distinction in both shell and PowerShell
bootstrap/update launchers and added a regression fixture with unrelated dirty
parent state before bootstrap.

Exact immutable `v0.2.14` evidence:

- release commit: `d1ed47c7d85524cfcb2a8f7e1ea81ba106ae9c60`;
- annotated tag object: `ddd3025c7b1f544a48a94acf766efd68c034d8bd`,
  pointing to that exact commit;
- complete exact-main release gate on that commit:
  - `test Self` — run `35893428515`;
  - `test PR cleanup` — run `35893428966`;
  - `test Output publish` — run `35893428906`;
  - `test Output same-job` — run `35893428650`;
  - `test Release` — run `35893428870`;
  - `test Moon` — run `35893428525`;
  - `test Evidence schema` — run `35893428526`;
- release lifecycle run `35893647253` passed and published the GitHub Release;
- tagged `test Output same-job` verification run `35893672305` passed on
  `v0.2.14`.

The numbered documentation families and self/reusable/test workflow naming
qualified in `v0.2.13` remain unchanged. `v0.2.14` supersedes it as the
Migration-011 generic-tool baseline solely because the rollout found a real
managed-launcher correctness defect.

Owner issue audit at acceptance:

- #42 uninitialized bootstrap gitlink vs parent worktree — **completed/closed**;
- #4 generic generated-output publication — **completed/closed**;
- #16 release preparation hook — valid non-blocking generic follow-up;
- #17 and #26 Moon performance/cache work — valid non-blocking follow-ups;
- #22 duplicate release-request idempotency — valid non-blocking release
  robustness follow-up;
- #31 synthetic Git fixtures and #32 PR feedback optimization — valid
  non-blocking owner-test/feedback work.

### 2. tool.scad-project

**Accepted baseline: `v0.15.11`.**

Exact immutable evidence:

- release commit / lightweight tag target:
  `8d167ad17dbfa798d68f46d871aaeed2e2e09857`;
- release-preparation PR #114 exact-head `test Self` run
  `35886336178` — success;
- exact-main `test Self` run `35886486580` — success;
- repository release run `35886631700` — success; it validated the request,
  created lightweight `v0.15.11`, dispatched tagged owner qualification and
  removed the release-request branch;
- Git ref `refs/tags/v0.15.11` resolves directly to
  `8d167ad17dbfa798d68f46d871aaeed2e2e09857`;
- tagged `test Self` workflow-dispatch run `35886652260` — success.

The accepted release was built against `tool.git-project v0.2.13` and includes the
Migration-011 owner cleanup. The later `v0.2.14` generic patch changes only the
managed consumer bootstrap/update launchers; it does not change the reusable
Moon/publication interfaces consumed internally by `tool.scad-project v0.15.11`.
Current consumers therefore pin their bootstrap gitlink/managed launchers to
`v0.2.14` without requiring a SCAD-tool rerelease.

The accepted SCAD owner cleanup includes:

- #107 — canonical managed `update.ps1/.sh` launcher ownership: completed;
- #110 — numbered repository documentation families: completed;
- #112 — public `reusable-build` / `reusable-verify` / `reusable-ci` /
  `reusable-release` APIs, `self-*` owner entries and `test-self.yml`
  qualification: completed;
- the redundant SCAD PR-cleanup wrapper is removed; consumers use the generic
  `tool.git-project/reusable-pr-preview-cleanup.yml` API;
- owner post-update synchronization covers only the current reusable SCAD API
  names;
- `self-pages.yml` successfully followed renamed `test Self` on exact main
  in run `35886151702`.

Owner issue audit at acceptance:

- #10 release-publication lifecycle — completed/closed;
- #80 runtime v0.5.1 request — superseded/closed as not planned by the later
  v0.6.1 runtime baseline;
- #42 post-build decision audit — valid non-blocking follow-up.

### 3. lib.scad.forge

**Accepted baseline: `v0.3.1`.**

Migration 011 for Forge was intentionally scoped to integrating the accepted
shared tooling baseline. A separate attempt to fold Forge API cleanup into the
same owner release exposed an ambiguity in release-boundary/version selection;
that policy follow-up is tracked in
[brainboxemb.meta #155](https://github.com/brainboxemb/brainboxemb.meta/issues/155).

The accepted Forge patch release therefore keeps API cleanup issue #30 separate
and publishes the qualified repository/tooling integration only.

Exact immutable evidence:

- release source commit:
  `100693541e056e312605c88a2f145ee1cbb829a4`;
- exact-main CI run `35896539896` — success;
- both `prod/bld` and `prod/vrf` identify that exact source and record:
  - `tool.git-project` gitlink
    `d1ed47c7d85524cfcb2a8f7e1ea81ba106ae9c60` (`v0.2.14`);
  - `tool.scad-project` gitlink
    `8d167ad17dbfa798d68f46d871aaeed2e2e09857` (`v0.15.11`);
- release lifecycle run `35896692612` — success;
- annotated tag object `7452eda080c056a4a24be0c2a500cdafb2f6eccc`
  points to exact release commit
  `100693541e056e312605c88a2f145ee1cbb829a4`;
- immutable release publications `rel/v0.3.1/bld` and `rel/v0.3.1/vrf`
  both identify tag `v0.3.1`, the same exact source commit and the accepted
  tool gitlinks.

Owner issue disposition at acceptance:

- #32 repository/tooling baseline integration — **completed/closed**;
- #30 `fg_overlap_mm()` retirement — valid separate/non-blocking Forge API
  follow-up; explicitly not part of `v0.3.1`;
- #12 / #13 — non-blocking API evaluations unless deliberately promoted.

Post-release owner documentation records `v0.3.1` as the accepted
Migration-011 Forge baseline; later Forge API cleanup does not retroactively
change this migration baseline.

### 4. lib.scad.util

**Accepted baseline: `v0.4.1`.**

The util owner state now combines three already-qualified pieces:

- #16 / PR #17 — inspection-only ownership cleanup;
- #18 / PR #19 — Migration-011 tooling integration;
- #20 / PR #21 — current numbered documentation structure.

The `v0.4.1` release is intentionally a patch release. The removed util-owned
`xf_*` / `fg_*` code was stale against an ownership decision that had already
been made; this release does not establish a new incompatible product direction.

Exact immutable evidence:

- release source commit:
  `af04b44c2fb1d779a87797da4290deca92c7594d`;
- exact-main documentation qualification commit
  `123207fb32bcad81b209265d8f52bf8abf307127`, run `35899078347` — success;
- release-metadata exact-main run `35899314331` — success;
- release lifecycle run `35899380256` — success;
- annotated tag object
  `fc84b97d9ef40a2442b3b6a410067f78ab78c469` points to exact release
  commit `af04b44c2fb1d779a87797da4290deca92c7594d`;
- immutable release publications `rel/v0.4.1/bld` and
  `rel/v0.4.1/vrf` both identify tag `v0.4.1`, that exact source commit,
  `tool.git-project` at
  `d1ed47c7d85524cfcb2a8f7e1ea81ba106ae9c60` (`v0.2.14`) and
  `tool.scad-project` at
  `8d167ad17dbfa798d68f46d871aaeed2e2e09857` (`v0.15.11`).

The accepted source surface contains section inspection plus managed consumer
controls only. The current documentation collection follows the shared
`README / 10 / 20 / 30 / 40 / 50` family structure.

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

- #32: completed repository/tooling integration baseline.
- #30: valid separate/non-blocking API cleanup follow-up; excluded from the
  accepted `v0.3.1` tooling-integration release.
- #12 / #13: non-blocking API evaluations unless deliberately promoted.

### lib.scad.util

- #16 / PR #17: completed inspection-only ownership cleanup.
- #18 / PR #19: completed Migration-011 tooling integration.
- #20 / PR #21: completed current numbered documentation structure.

### brainboxemb.meta

- #116 is incorporated by this migration and can close when the owner-state
  audit and baseline reconstruction are retained here.
- #155 tracks the release-boundary/version-selection ambiguity exposed while
  integrating Forge; it is a policy follow-up and does not block the accepted
  owner baselines.
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

## Repository documentation

Migration 011 also closes the durable documentation-structure gap.

Maintained current-generation repositories follow the shared numbered
documentation-family convention from
[`docs/20-13-repository-documentation.md`](../../docs/20-13-repository-documentation.md),
with the SCAD specialization in
[`domains/scad/documentation-structure.md`](../../domains/scad/documentation-structure.md).

A maintained SCAD library/tool/project documentation collection normally has:

```text
doc/ or docs/
README.md
10-00-plan.md
20-00-manuals.md
20-01-development.md
20-02-user.md          # when a meaningful consumer/operator surface exists
30-00-specification.md
40-00-design.md
50-00-verification.md
```

Optional `20-xx`, `40-xx` and `50-xx` documents keep useful detail in the
appropriate family.

The local development manual records the repository-specific developer
experience: normal entrypoints, direct dependencies/version-selection points,
workflow set, build/verification/release path and intentional deviations.
Generic rules are linked rather than copied.

Existing useful documents are classified and renumbered rather than discarded.
For example, the template's current CI-orchestration page belongs under the
manual family and should be linked from `20-00-manuals.md` /
`20-01-development.md` after renumbering.

Every maintained documentation collection keeps one local `README.md` as its
overview/index; no parallel `00-00_readme.md` is added.

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

1. **Complete:** accept `tool.git-project v0.2.14` at exact
   `d1ed47c7d85524cfcb2a8f7e1ea81ba106ae9c60`;
2. **Complete:** accept `tool.scad-project v0.15.11` at exact
   `8d167ad17dbfa798d68f46d871aaeed2e2e09857`.

### Phase 3 — Forge and util baseline

1. **Complete:** accept `lib.scad.forge v0.3.1` at exact
   `100693541e056e312605c88a2f145ee1cbb829a4`;
2. **Complete:** accept `lib.scad.util v0.4.1` at exact
   `af04b44c2fb1d779a87797da4290deca92c7594d`.

### Phase 4 — maintained consumer rollout

**Current.**

1. **Complete:** accept `lib.scad.mechint v0.2.4` at exact
   `28a8ac1aa1097f7284fd806c91b4cab655566509`.
   - integration PR #35 exact-head CI run `35900314113` — success;
   - exact-main integration run `35900507034` — success;
   - release-metadata exact-main run `35900865180` — success;
   - release lifecycle run `35900990289` — success;
   - annotated tag object `1d8b150f0a658e1bb5b4b014551aad19ceada88f`
     points to exact release commit
     `28a8ac1aa1097f7284fd806c91b4cab655566509`;
   - immutable `rel/v0.2.4/bld` and `rel/v0.2.4/vrf` both retain
     `tool.git-project v0.2.14`, `tool.scad-project v0.15.11`,
     `lib.scad.forge v0.3.1` and `lib.scad.util v0.4.1`.
2. **Current:** roll the accepted tooling/documentation baseline through the
   standalone libraries `lib.scad.clamps` and `lib.scad.hub75` before the
   HUB75 application/lab repositories consume their resulting releases.

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
- every maintained rollout repository uses the shared numbered documentation families, including a local documentation `README.md` and `20-01-development.md` operating summary where applicable;
- GitHub Actions workflows follow the `self-*` / `reusable-*` / `test-*` naming convention and callers match the released SCAD contract for each repository role;
- every intentional old dependency pin is documented as such;
- exact PR/main CI evidence is retained for rollout repositories;
- the template is updated last;
- meta #116 can close with its requested tooling-state audit captured here.

Migration 007, generic release-flow work in meta #20, API-doc publication #125
and unrelated Forge feature evaluations may remain open.
