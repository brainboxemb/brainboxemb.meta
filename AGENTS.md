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
- experiment/PoP questions/evidence → `experiments/`.

Do not make migration terminology the framing for unrelated documentation or PoPs.

## Keep ownership in the right repository

`brainboxemb.meta` owns portfolio-level overview, shared guidance, the public repository catalog, dashboard presentation and cross-project work coordination records.

Implementation stays in the repository that owns it. Project-specific plans and design documentation stay with the project; tool/library implementation details stay with that tool/library; experiment/PoP fixtures, harnesses, adapters and qualification results stay in the dedicated experiment repository.

A need observed in one consumer repository is not automatically a shared-tooling requirement. Prefer a consumer-local solution first unless the behaviour is already part of an explicit shared contract or evidence from multiple consumers shows that it belongs in shared tooling. Before promoting such a change, inspect current consumer use cases, compatibility and existing links/contracts rather than generalising from one repository.

## Cross-repository work discipline

Treat repository ownership and CI boundaries as part of the work plan:

- follow the owner repository's current issue/branch/PR convention instead of inventing a parallel naming scheme;
- group related edits into one coherent commit and branch update per affected repository when the available Git tooling permits;
- do not push per-file micro-commits merely because an API makes that convenient;
- after advancing an active CI branch, inspect that run/evidence before starting the next corrective push unless the run itself exposes a blocker that requires correction;
- when one logical task spans multiple repositories, keep one coherent change per owner rather than mixing implementation and coordination details across boundaries.

This keeps GitHub Actions evidence readable and avoids repeatedly superseding or cancelling runs with avoidable micro-pushes.

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

For intentionally retained third-party forks, use the reader-facing naming rule
from `repositories/README.md`:
`fork.<upstream-owner>.<upstream-repository>`, normalized to lowercase.
Do not add planned-but-not-created fork or experiment repositories to the
catalog.

## Cross-project work tracks

`STATUS.md` is the authority for which repository-spanning work track is currently primary. A work track may be a migration, an experiment/PoP or another explicitly documented cross-project activity.

Do not assume that the next numbered migration is active. Read the relevant index and work-track record after `STATUS.md` identifies the primary track.

## Migrations

A migration under `migrations/` can be `active`, `proposed / inactive`, or `complete`.

A proposed migration must not start automatically. Before active cross-project work, re-check the current repositories, issues/PRs and evidence rather than relying only on an older plan.

Keep the blocking path small. Newly discovered work should be separated into blockers, follow-up migrations, PoPs/experiments or backlog instead of automatically enlarging the active migration.

## Experiments and PoPs

A track under `experiments/` can be `active`, `proposed / inactive`, `parked`, or `complete`.

Experiment/PoP record directories use a stable three-digit prefix matching the experiment number where one exists, for example `experiments/004-java-ci-architecture/`. Do not renumber older records when new experiments are added. In dedicated experiment repositories, keep `README.md` as the entrypoint and number ordered supporting documents under `docs/` as `00-...`, `01-...`, `02-...`, and so on.

Use **design-first PoP** when the architecture can be specified from established engineering knowledge: define the target concept first, then identify the assumptions that genuinely require runtime evidence. Do not blindly implement every possible candidate merely because multiple tools exist.

The normal adoption sequence is:

```text
concept -> PoP -> qualification -> production migration
```

A failed PoP is valid evidence. Revisit the concept/assumption rather than weakening the testcase.

The meta repository records the problem, target concept, status, evidence conclusion and production decision; the implementation/evidence repository owns fixtures, harnesses, adapters and executable cases.

Prefer reproducible fixtures, declarative/executable testcases and retained CI evidence over one-off manual probing. Manual exploration may inform a hypothesis, but a conclusion should be reproducible where practical.

PoP repositories are preferably **reusable rather than disposable**. If a later migration or production owner exposes a problem that can be represented faithfully in the PoP fixture, reproduce it there, prove the failure, qualify the correction and retain the case as regression coverage after the production fix.

Completing a PoP/experiment does not automatically authorize or activate a production migration. If rollout across production owners is needed, create/select that work separately.

## Dashboard

The dashboard is a subproject under `dashboard/`. Read `dashboard/AGENTS.md` before changing dashboard code or workflows.

Repository-level workflows remain under `.github/workflows/` because GitHub requires that location.

## Evidence

When a migration, PoP/experiment or qualification claims completion, retain exact revisions/run IDs where useful. Do not mark work complete merely because documentation was changed.
