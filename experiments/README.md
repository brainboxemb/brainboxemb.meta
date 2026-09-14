# Experiments and test repositories

Cross-project experiments stay in independent repositories. This directory records their role in architecture decisions; it is not a place to absorb their implementation.

A useful experiment record should state:

- repository;
- question/hypothesis tested;
- evidence/result;
- decision the result supports;
- whether the experiment is still active;
- where the adopted production behavior now lives.

## Current experiments

- [Moon as SCAD target engine](moon-scad-target-engine.md) — **parked**. Tracks whether Moon can replace all or part of the current SCons target layer without losing fine-grained OpenSCAD dependency/selective-build behaviour. Meta issue: [#51](https://github.com/brainboxemb/brainboxemb.meta/issues/51).

Example categories include orchestration/build-system experiments such as the evidence used to justify Moon adoption.

This keeps experimental dependencies and production ownership separate while making the reasoning discoverable from the central meta repository.
