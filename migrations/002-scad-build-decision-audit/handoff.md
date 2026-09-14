# Migration 002 handoff — SCAD build-decision audit

Use this only after Migration 002 has been explicitly activated.

```text
Werk vanuit brainboxemb/brainboxemb.meta als cross-project coordination source.

Lees eerst:
- STATUS.md
- migrations/002-scad-build-decision-audit/README.md
- domains/scad/README.md
- domains/scad/architecture.md

Controleer daarna de actuele implementatie en tests op main van:
- brainboxemb/tool.scad-project

Reassess vóór implementatie of de voorgestelde post-build decision audit nog steeds
de kleinste juiste volgende stap is. Controleer expliciet:
- doel en owner;
- huidige build-decision report/manifest inputs;
- bewezen versus alleen mogelijke impact;
- toegestane uitkomsten per impactklasse;
- cache/integrity boundary;
- benodigde deterministic owner tests en qualification evidence.

Fysieke-verificatie document bundles (brainboxemb.meta issue #18) zijn een losse,
niet-blocking follow-up en horen niet automatisch in deze migratie.

Implementeer owner-details in tool.scad-project. Houd in brainboxemb.meta alleen
scope, cross-project contract, status en qualification evidence bij.
```

If Migration 002 is still marked `proposed / inactive`, do not execute the handoff. Return to `STATUS.md` and the currently active migration instead.
