# Experiment 011 — SolidCraft command facade

**Status: active — source-level Python and Rust fixtures added; live integration not yet qualified.**

Implementation/evidence repository:
[`brainboxemb/exp.2026-011.solidcraft`](https://github.com/brainboxemb/exp.2026-011.solidcraft).

Initial work: [draft PR #2](https://github.com/brainboxemb/exp.2026-011.solidcraft/pull/2).
Experiment-local tracking: [issue #1](https://github.com/brainboxemb/exp.2026-011.solidcraft/issues/1).

## Question

Can we implement a small, readable, preferably typed **interface over SolidCraft's command API**, and keep that interface independent of whether commands are sent via a script, GUI control channel or headless MCP? Compare Python and Rust **as client languages**, using `vcad` only as an example of an ergonomic Rust API definition—not as a CAD engine.

## Starting direction

- SolidCraft supplies a command-based CAD engine, a GUI control channel, a headless CLI and MCP.
- The third-party [`scraftpybind`](https://github.com/waynegramlich/scraftcnc/tree/main/scraftcnc/pybind), inside `waynegramlich/scraftcnc`, maps SolidCraft commands to Python methods with a GUI and headless transport.
- Pin this upstream source; do not copy or fork it unless we identify a specific gap that requires intervention.
- Investigate a separate minimal **Rust facade** that maps the same method calls to native SolidCraft commands. Its initial ScriptTransport is not a CAD engine.
- `vcad` is a reference for ergonomic API signatures and fluent usage **only**; do not integrate its geometry kernel or create a separate vcad-engine experiment.
- SolidCraft **0.30.1** is the initial current-release target. Upstream's Python commands were generated from CLI **0.20.0**. Compatibility is **unverified**.

## Acceptance cases

| Case | Question |
|---|---|
| PY-01 | Can offline binding and example tests run from a pinned checkout? |
| PY-02 | Can Python create a visible model in the Windows GUI control session? |
| PY-03 | Can Python create and export the equivalent model headlessly through MCP? |
| PY-04 | Can it save/reopen a native SolidCraft file and revise parameters without losing history? |
| PY-05 | Are runtime versions, errors, and output reproducible and understandable? |
| API-01 | Can a small typed Rust facade produce valid SolidCraft commands? |
| API-02 | Can the same facade be used with different command transports without rewriting model logic? |

At the start of the experiment, five Python fixture tests were added but not yet executed; these test only the planned command sequence, **not** SolidCraft or its installed GUI/CLI.

A source review uncovered a Windows token-folder mismatch in the pinned upstream Python binding. The experiment's fixture handles the Windows default path without copying token files or modifying upstream.

## Boundaries

**Experiment 011 owns** Python and Rust command-facade examples, transport experiments, fixtures, and evidence. **SolidCraft owns all modeling and geometry operations.**

**Experiment 012 (separate, proposed)** will examine PartCAD's SolidCraft adapter for import/export, declared parameters and its existing Docker image. Do not fold that investigation into 011.

A new `docker.cad-toolchain` is deferred. An isolated Dockerfile may later be introduced *inside the experiment* if a repeatable headless testcase justifies it.

Production CAD/SCAD model repositories and shared tooling stay unchanged. Completing this experiment will not automatically start a migration.
