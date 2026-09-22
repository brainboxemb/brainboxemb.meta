# Migration 010 — restore canonical repository update contract

Status: **active**

Tracking issue: [#115](https://github.com/brainboxemb/brainboxemb.meta/issues/115)

Primary existing owner issue:
[`tool.git-project#18` — Keep generated bootstrap/update scripts version-aware and detect drift](https://github.com/brainboxemb/tool.git-project/issues/18)

## Why this migration exists

Migration 009 successfully restored and qualified the then-current
`update-repo status` behaviour and aligned the in-scope SCAD consumers to one
released `tool.scad-project` baseline.

The later HUB75 component-lab maintenance exposed a stronger requirement that
Migration 009 did not prove:

> equal or working consumer files are not enough when the portfolio cannot
> identify their canonical owner, source revision and refresh path.

Current evidence shows several overlapping sources:

- `tool.git-project/bootstrap/consumer-bootstrap.*`;
- `tool.git-project/bootstrap/consumer-update.*`;
- `tool.scad-project/consumer/update-repo.*`;
- copied root `bootstrap.*` and `update-repo.*` files in consumers;
- SCAD documentation describing composition through
  `scad-project repo-update`;
- maintained SCAD consumers using a Python-free native wrapper instead.

That means the portfolio can have files that look aligned today while still
having no durable mechanism that tells a maintainer whether a local launcher is
the right copy tomorrow.

## Architectural baseline

The existing portfolio boundary remains:

```text
tool.git-project
    generic repository/bootstrap/dependency update/status

tool.<domain>-project
    domain-specific build/configuration/lifecycle behaviour

consumer repository
    project source + configuration + exact accepted dependency pins
```

Basic repository bootstrap/update/status must not require Python, Java,
OpenSCAD or another domain runtime. Git remains the external prerequisite for
the generic path.

Migration 010 must preserve the behaviour already qualified by Migrations 008
and 009:

- controlled direct and transitive dependency update;
- dirty-worktree protection;
- owner-local nested dependency pins;
- `update-repo status` is read-only;
- normal user entrypoints remain `bootstrap`, `update-repo` and
  `update-repo status`.

## Step 1 — launcher provenance and drift detection

**Owner: `tool.git-project`**

Do not begin by copying launchers between consumers.

Existing issue
[`tool.git-project#18`](https://github.com/brainboxemb/tool.git-project/issues/18)
already defines the required first step:

- canonical bootstrap/update launchers carry an explicit source/tool version;
- central refresh stamps the owner version that supplied the launcher;
- launchers compare that version with the repository's actually pinned
  `tool.git-project`;
- an out-of-sync copy emits a clear warning with expected and actual versions;
- manual copy/paste is no longer the normal refresh mechanism;
- intentionally older repositories remain valid when launcher and pin agree.

Acceptance of this step requires owner tests for both an in-sync consumer and an
intentionally stale consumer on Windows and POSIX.

## Step 2 — resolve composition ownership

Only after Step 1 makes launcher provenance observable, inspect the actual
current consumers and decide:

1. which root launchers are wholly generic and therefore sourced from
   `tool.git-project`;
2. whether a SCAD consumer still needs domain-specific post-update composition;
3. if SCAD composition is needed, where its canonical implementation lives and
   how the generic launcher invokes or refreshes it without duplicating generic
   dependency logic;
4. which existing copied files should be removed instead of synchronized.

Filename equality is not evidence of ownership.

The open `tool.scad-project#102` discussion is a symptom/input to this step; it
must not independently reintroduce Python as a prerequisite for the generic
root update path.

## Step 3 — release and qualify owner behaviour

Release the necessary owner changes and prove the complete normal-entrypoint
contract:

| Case | Required evidence |
| --- | --- |
| bootstrap, clean clone | pinned generic tool restored and dependencies established |
| update, no changes | idempotent and clean |
| update, dependency advance | only configured dependency/gitlink changes |
| status | read-only; no dependency movement |
| dirty dependency | update refused safely |
| stale launcher | explicit source/version drift warning |
| current launcher | no false drift warning |
| Windows | native PowerShell path, no Python requirement |
| POSIX | shell path, no Python requirement |

Reuse `exp.2026-006.scad-library-dependencies` where its retained fixtures can
faithfully represent these cases rather than creating another experiment by
default.

## Step 4 — reference SCAD consumer

After the released generic owner contract is green, align
`template.scad-project`.

Qualification must prove both layers separately:

- the generic root launcher provenance/update/status contract;
- any remaining SCAD-specific workflow-ref/composition behaviour.

A green build alone is insufficient if launcher provenance cannot be traced.

## Step 5 — portfolio rollout

Only after the template is qualified, roll the released contract through every
catalogued current-generation consumer.

For each repository retain:

- exact accepted `tool.git-project` gitlink/version;
- exact domain-tool gitlink/version where applicable;
- launcher source/version provenance;
- no drift warning on the accepted state;
- normal update/status evidence;
- normal project CI evidence where applicable.

Classic repositories remain out of scope unless explicitly selected.

## Relationship to Migration 009

Migration 009 remains valid evidence for the production-serialization fix and
for the specific `status` regression it caught.

Migration 010 narrows one over-strong conclusion from that rollout: matching
consumer files plus green entrypoint tests did **not** establish a durable
canonical-source/refresh contract.

Migration 010 therefore does not reopen the production-concurrency work. It
adds the missing provenance, ownership and synchronization invariant.

## Completion

Migration 010 is complete only when:

- the canonical launcher owner/source is explicit;
- source/version is visible in managed launchers;
- stale launchers are detected automatically;
- a central refresh route exists;
- generic bootstrap/update/status remains Python-free;
- domain-specific composition has one documented owner;
- retained regression fixtures prove Windows and POSIX normal entrypoints;
- the reference consumer is green;
- every selected current-generation consumer is aligned to the same released
  contract with exact evidence.
