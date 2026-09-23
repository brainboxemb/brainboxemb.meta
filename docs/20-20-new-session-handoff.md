# New session handoff

Use this when continuing work in a fresh ChatGPT or other engineering session.

The repository is the source of truth. The handoff message only needs to say
**where to look** and **what you currently want to do**.

## Generic repository handoff

```text
Werk vanuit <owner-repository> als source of truth.

Lees eerst README.md, AGENTS.md en de genummerde documentatie in doc/ of docs/.
Controleer daarna de actuele issues, pull requests, CI/evidence en relevante
generated output voordat je verdergaat.

Mijn huidige doel / waar ik mee bezig ben:
<één korte beschrijving>
```

That is normally enough. Do not copy a complete plan, architecture description,
migration history or old chat summary into the handoff when the repository
already owns that information.

## Cross-project / meta handoff

For repository-spanning work use:

```text
Werk vanuit brainboxemb/brainboxemb.meta als cross-project coordination source.

Lees README.md, AGENTS.md, STATUS.md en de genummerde documentatie. Bepaal vanuit
de actuele repositories zelf welke migration/experiment/owner stap werkelijk aan
de beurt is. Controleer actuele issues, PRs, CI/evidence en generated output;
gebruik oude chatgeschiedenis niet als source of truth.

Mijn huidige doel / aandachtspunt:
<één korte beschrijving>
```

`STATUS.md` selects the current cross-project track. The selected migration or
experiment record then owns sequencing/evidence, while implementation detail
remains in the relevant owner repository.

## Why the handoff stays short

The handoff should not become a second operating manual.

Durable guidance already lives in:

- [20-10 — Engineering workflow](20-10_engineering-workflow.md);
- [20-11 — Git workflow](20-11_git-workflow.md);
- [20-12 — Versioning and releases](20-12_versioning-and-releases.md);
- [20-13 — Repository documentation](20-13_repository-documentation.md).

A short handoff makes a fresh session reconstruct the current state from live
repository evidence instead of inheriting stale assumptions.
