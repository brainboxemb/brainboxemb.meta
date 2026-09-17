# Agent guidance

Instructions for automated agents working in `brainboxemb.meta`.

## Start with the reader-facing documentation

Use the repository according to the task:

- general overview → `README.md`;
- public repository list → `repositories/`;
- shared project/tooling guidance → `docs/`;
- domain overview → `domains/`;
- dashboard implementation → `dashboard/`;
- current cross-project work → `STATUS.md`;
- migration plans/evidence → `migrations/`;
- experiment questions/evidence → `experiments/`.

Do not make migration terminology the framing for unrelated documentation or experiments.

## Keep ownership in the right repository

`brainboxemb.meta` owns portfolio-level overview, shared guidance, the public repository catalog, dashboard presentation and cross-project work coordination records.

Implementation stays in the repository that owns it. Project-specific plans and design documentation stay with the project; tool/library implementation details stay with that tool/library; experiment fixtures, harnesses and candidate implementations stay in the dedicated experiment repository.

## Write for people in public documentation

README files and normal documentation should first help a reader understand:

1. what the subject is;
2. why it matters;
3. where to look or make a change.

Avoid agent-oriented headings such as “source-of-truth boundary”, “ownership boundary” or migration-step language when ordinary wording such as “where does this information live?” is clearer.

Do not duplicate the same maintenance rule across README, docs, migrations and experiments. Put agent-only rules here and explain the system once in the appropriate reader-facing page.

## Repository catalog

`repositories/catalog.yml` contains the public repository inventory and stable classification. Do not copy live GitHub status into it; the dashboard reads live status from GitHub.

Private or archived-private repositories do not belong in the public catalog.

## Cross-project work tracks

`STATUS.md` is the authority for which repository-spanning work track is currently primary. A work track may be a migration, an experiment or another explicitly documented cross-project activity.

Do not assume that the next numbered migration is active. Read the relevant index and work-track record after `STATUS.md` identifies the primary track.

## Migrations

A migration under `migrations/` can be `active`, `proposed / inactive`, or `complete`.

A proposed migration must not start automatically. Before active cross-project work, re-check the current repositories, issues/PRs and evidence rather than relying only on an older plan.

Keep the blocking path small. Newly discovered work should be separated into blockers, follow-up migrations, experiments or backlog instead of automatically enlarging the active migration.

## Experiments

An experiment under `experiments/` can be `active`, `proposed / inactive`, `parked`, or `complete`.

Experiments answer questions before production ownership is changed. The meta repository records the question, status, evidence and decision; the experiment implementation belongs in its dedicated experiment repository whenever one is defined.

Prefer reproducible fixtures, declarative/executable testcases and retained CI evidence over one-off manual probing. Manual exploration may inform a hypothesis, but an experiment conclusion should be reproducible where practical.

Completing an experiment does not automatically authorize or activate a production migration. If rollout across production owners is needed, create/select that work separately.

## Dashboard

The dashboard is a subproject under `dashboard/`. Read `dashboard/AGENTS.md` before changing dashboard code or workflows.

Repository-level workflows remain under `.github/workflows/` because GitHub requires that location.

## Evidence

When a migration, experiment or qualification claims completion, retain exact revisions/run IDs where useful. Do not mark work complete merely because documentation was changed.
