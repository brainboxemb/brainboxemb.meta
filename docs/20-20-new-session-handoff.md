# New session handoff

Use this when continuing work in a fresh ChatGPT or other engineering session.

The repository is the source of truth. The handoff message should therefore stay
short: say where to look, let the repository explain itself, and add the current
goal separately in the new conversation.

## Generic repository handoff

Copy/paste this complete message and change only the repository line at the end:

```text
Werk vanuit de repository onderaan dit bericht als source of truth.

Lees eerst README.md en AGENTS.md. Lees daarna de genummerde documentatie in
doc/ of docs/, te beginnen bij de lokale README.md en het plan.

Controleer vervolgens de actuele repository zelf: openstaande issues en pull
requests, relevante CI/evidence, dependency-pins en generated output wanneer die
voor het werk van belang zijn.

Gebruik oude chatgeschiedenis niet als source of truth wanneer de repository
actuelere informatie bevat. Bepaal uit de actuele repository wat de eerstvolgende
geldige stap is en welke documentatie/evidence daarvoor authority is.

Als tijdens het werk een gedeelde of cross-repository wijziging nodig blijkt,
controleer dan eerst brainboxemb/brainboxemb.meta en de relevante owner
repository voordat je de verantwoordelijkheid lokaal oplost.

Repository:
https://github.com/brainboxemb/REPOSITORY
```

In the new conversation, add the actual request or current goal as the normal
message around or after this handoff. The reusable handoff itself does not need a
second placeholder for that.

## Cross-project / meta handoff

For repository-spanning work the repository is fixed, so this is also directly
copy/pasteable:

```text
Werk vanuit brainboxemb/brainboxemb.meta als cross-project coordination source.

Lees README.md, AGENTS.md, STATUS.md en de genummerde documentatie. Bepaal vanuit
de actuele repositories zelf welke migration, experiment of owner-stap werkelijk
aan de beurt is.

Controleer actuele issues, pull requests, CI/evidence en generated output voordat
je verdergaat. Gebruik oude chatgeschiedenis niet als source of truth wanneer de
repositories actuelere informatie bevatten.

Gebruik de geselecteerde owner repository voor implementatie en
brainboxemb.meta voor cross-project sequencing, gedeelde conventies en
retained evidence.
```

## Why the handoff stays short

The handoff is navigation, not a second operating manual.

Durable guidance lives in:

- [20-10 — Engineering workflow](20-10-engineering-workflow.md);
- [20-11 — Git workflow](20-11-git-workflow.md);
- [20-12 — Versioning and releases](20-12-versioning-and-releases.md);
- [20-13 — Repository documentation](20-13-repository-documentation.md).

A short handoff makes a fresh session reconstruct current state from repository
evidence rather than inheriting stale assumptions.
