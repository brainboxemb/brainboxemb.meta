# Migration 004 qualification evidence

Status: **active**

Tracking: meta issue #49.

## Step 1 — generic Moon affected preflight

Status: **complete**

Owner: `brainboxemb/tool.git-project`.

Released capability: `tool.git-project v0.2.5`.

Exact released source commit:

```text
ce7c81c39ebc70933b4150028aa74d928a53c2ba
```

Owner work:

- issue/PR #21 — `Add generic Moon affected preflight`;
- reusable action: `moon/affected`;
- Linux wrapper: `moon-affected.sh`;
- Windows wrapper: `moon-affected.ps1`;
- retained query/decision evidence under `.moon/preflight`.

Qualified behavior with real Moon 2.5.4 and real Git commits:

- README-only change outside task inputs => `affected=false`;
- configured task-input change => `affected=true`;
- missing base revision => conservative `affected=true`;
- explicit base/head ranges are used;
- preflight queries do not execute the producer;
- Linux and native Windows behavior match;
- reusable composite action itself is exercised in CI.

PR-head qualification on `6ec28d7bd77e789a8867e8c8326d81a9c2d066ed`:

- Moon production orchestration run `34886865162` — Linux and Windows green;
- Self-test Git project tooling `34886865079` — green;
- generic release lifecycle `34886865532` — green;
- generated output publication `34886865453` — green;
- PR preview cleanup `34886865539` — green;
- execution evidence schema `34886865072` — green.

Exact-main qualification ran successfully for the merge commit before release.

Release:

- tag `v0.2.5` is an annotated tag pointing to exact main `ce7c81c39ebc70933b4150028aa74d928a53c2ba`;
- release run `34887174233` completed successfully, including tagged verification and GitHub Release creation.

A duplicate release run (`34887175316`) started for the same request and failed only because the successful run had already created the exact tag. This is not a Migration 004 blocker; generic release idempotency is tracked separately as `tool.git-project` issue #22.

## Step 2 — reference task-graph correction

Status: **complete**

Owner: `brainboxemb/template.scad-project`.

Owner work:

- PR #22 — `Make SCAD Build and Verify logically independent`;
- merge/exact-main revision: `082b0cecb47ba082899214751080adc54556e94c`;
- stale `scad.verify -> scad.build` dependency removed after confirming Verify does not consume normal Build output;
- `scad.ci` remains the aggregate root;
- Build-only, Verify-only and aggregate semantics remain distinct.

Qualification:

- PR run `34893868011` — passed;
- exact-main run `34894004036` — passed;
- Build and Verification publication remained intact.

Performance observation relevant to Step 3:

- SCAD job container initialization was about 17 s on the PR run and about 30 s on exact main, before checkout;
- this strengthens pre-container gating as a required acceptance criterion rather than a later optimization.

## Step 3 — shared SCAD production workflow

Status: **next; prerequisite qualification required**

Owner: `brainboxemb/tool.scad-project`.

Before fixing the reusable workflow's preflight checkout contract, prove with Moon 2.5.4 that `changed-files --base <sha> --head <sha>` works when the local repository contains only the exact head commit and the exact base commit needed for the comparison, without fetching intervening history or unrelated branches/tags.

Current reference-template evidence:

- checkout is already blobless (`filter: blob:none`);
- it still uses `fetch-depth: 0`, which fetches complete history and is broader than the intended preflight contract.

If the focused two-commit qualification succeeds, Step 3 should use a shallow/blobless host preflight checkout plus an explicit fetch of only the required base commit. The conditional SCAD job should then checkout only the exact source revision plus the submodules/tooling it actually needs.
