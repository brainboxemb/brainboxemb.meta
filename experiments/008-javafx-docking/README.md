# Experiment 008 — JavaFX docking workbench

Status: **active**

Tracking issue: [#183](https://github.com/brainboxemb/brainboxemb.meta/issues/183)

Implementation/evidence repository:
[`brainboxemb/exp.2026-008.javafx-docking`](https://github.com/brainboxemb/exp.2026-008.javafx-docking)

Initial implementation PR:
[`exp.2026-008.javafx-docking#1`](https://github.com/brainboxemb/exp.2026-008.javafx-docking/pull/1)

Reference implementation:
`brainboxemb/2026-010-02.java.timing-point-application`

## Question

Can an IDE-style JavaFX docking framework provide a maintainable workbench for
the Event Timing Development Client and future diagnostic tools without coupling
individual views to the docking implementation?

The representative workbench includes current Development Client surfaces such
as TimingNode, Registration, Simulation, Terminal, Device Log, Client Log,
Registrations and LogBook, plus a dynamic Tag Plot placeholder representing
future realtime diagnostics.

## Target concept

Keep application views ordinary JavaFX controls and place docking-specific
responsibility in a thin workbench layer:

```text
application/tool views
        |
        v
small workbench adapter
        |
        v
docking framework
        |
        v
JavaFX Stage / windows
```

The docking framework should organize views; it should not become the model,
controller or business-logic API for those views.

## First candidate

SnapFX is the first candidate because its feature set matches the expected
workbench direction: dock/tab layouts, floating windows, cross-window docking
and persisted layouts.

The first PoP baseline is:

- Java 21;
- JavaFX 21;
- Maven, matching the Development Client build direction;
- Transit 2.0.0 for normal JavaFX look and feel;
- SnapFX as docking/workbench infrastructure.

SnapFX is not selected in advance. Another candidate should be implemented only
when this PoP fails a required principle or leaves a concrete material decision
unresolved.

## Qualification questions

The experiment must establish at least:

1. ordinary JavaFX views can dock left/right/top/bottom and as tabs;
2. split ratios can be adjusted interactively without view-specific handling;
3. panels can float, move between windows and redock reliably;
4. cross-window behaviour is suitable for multi-monitor development use;
5. tab groups, splits and floating-window geometry survive save/load across a
   fresh application session;
6. stable panel IDs and a factory can reconstruct the workbench without leaking
   docking-framework APIs throughout view classes;
7. Transit and application CSS can coexist with the docking chrome;
8. Transit 2.0.0 behaves correctly on the Java 21 / JavaFX 21 experiment
   baseline even though the current Transit source builds against JavaFX 22;
9. Terminal, Device Log and Client Log can remain dark/monospace inside a light
   workbench;
10. continuously changing/dynamic content such as a Tag Plot behaves correctly
    while docking and resizing;
11. the selected docking dependency can be consumed reproducibly from the
    Maven-based Development Client.

## Ownership

`brainboxemb.meta` owns:

- the cross-project question and active sequencing;
- experiment status and retained conclusion;
- the decision whether later production adoption/migration should start.

The experiment repository owns:

- isolated JavaFX fixtures and mock panels;
- candidate-specific docking integration;
- executable/manual qualification evidence;
- retained findings about framework behaviour.

The Event Timing implementation repository remains owner of:

- Development Client behaviour;
- production Java/JavaFX baseline decisions;
- eventual docking integration.

## Production boundary

A successful Experiment 008 supports a later production decision; it does not
itself authorize a Java 21 migration or docking-framework rollout.

Production changes should be made through the normal owner issue/PR path after
the experiment has a retained conclusion and evidence.
