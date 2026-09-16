# Migration 007 — standardise GitHub Actions dependency maintenance

Status: **proposed / inactive**

Tracking issue: [#66](https://github.com/brainboxemb/brainboxemb.meta/issues/66)

Activation blocker: [Migration 006](../006-java-execution-architecture/README.md) must be complete first unless cross-project priorities are explicitly changed later.

## Current status

Migration 007 is parked intentionally behind the Java execution-architecture migration. It records a cross-project maintenance problem discovered while working on Migration 005, but it is **not** part of Migration 005 and should not delay the current SCAD release/rollout path.

## Problem

GitHub Actions references are currently maintained too manually and are not fully consistent across repositories. Existing workflows mix floating major refs and exact SHA pins, while reusable brainboxemb workflows may intentionally use semantic release refs as part of a separate released-tool identity contract.

The migration should standardise how action dependencies are discovered, updated, reviewed and qualified without turning workflow updates into unattended direct mutations.

## Current preferred direction

Working hypotheses for later validation:

1. Third-party GitHub Actions normally use an **exact commit SHA plus readable version comment**.
2. **Dependabot `github-actions`** is the leading candidate for normal PR-based dependency updates.
3. **`azat-io/actions-up`** is worth evaluating for initial normalisation, machine-readable audit, reusable-workflow discovery, missed-update detection and hosted-runner image updates.
4. Fresh releases should have a deliberate **age/cool-down policy** rather than being consumed immediately.
5. brainboxemb-owned reusable workflows are an explicit exception candidate: semantic released refs may remain correct where a separate exact source/gitlink contract already provides identity.
6. Updates must pass the normal repository PR/CI path; no direct unattended workflow rewriting on production branches.
7. Shared policy/configuration should have one owner rather than drift independently across every repository.

## Before activation

When Migration 006 is complete, inventory the then-current portfolio, define the exact reference/update policy, choose the Dependabot/actions-up split, select canary repositories and define portfolio-wide audit evidence before changing repositories.
