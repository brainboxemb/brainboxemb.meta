# Experiment 008 — JavaFX docking workbench

Status: **complete — JavaFX workbench qualified; BentoFX preferred as Event Timing Step-6 D02 input**

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
Registrations, LogBook and a shared Raw Data detail view.

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

## Candidates evaluated

The PoP baseline is Java 21, JavaFX 21, Maven and Transit 2.0.0.

Two docking candidates were evaluated against the same framework-independent
panel catalogue:

- **SnapFX 0.8.0** — strong floating-window and built-in layout-persistence
  capability, but not available through the normal Maven Central path and it
  required more application-owned integration/presentation correction;
- **BentoFX 0.16.0** — explicit root/branch/leaf workbench structure, cleaner
  application adapter code, normal Maven Central dependency and the better
  out-of-the-box workbench feel for the representative Event Timing client.

The experiment therefore retains **BentoFX as the preferred docking candidate**
for the later Event Timing technology decision. SnapFX remains useful comparison
evidence rather than the preferred production direction.

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
10. shared application-owned selection/detail content remains independent from
    the docking framework while docking and resizing;
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


## Result

Experiment 008 is complete.

The main question is answered positively: an IDE-style dockable JavaFX workbench
can keep application views as ordinary JavaFX controls while concentrating
framework-specific behaviour in a small workbench adapter.

The retained findings are:

- Java 21 / JavaFX 21 is a workable desktop baseline for this PoP;
- Transit 2.0.0 can provide the application look-and-feel when the application
  owns the JavaFX runtime version and prevents older transitive JavaFX modules
  from entering the runtime classpath;
- shared application views such as Registrations, LogBook and Raw Data can stay
  independent from both docking candidates;
- SnapFX provides useful floating and persistence behaviour, but its release-JAR
  bootstrap and additional adapter/chrome/style handling are production costs;
- BentoFX gives the clearer workbench structure and normal Maven dependency path
  and is the preferred candidate for Event Timing Step 6 D02;
- layout persistence, final floating/multi-monitor product behaviour, JPMS/runtime
  packaging and installer/update choices remain product-technology concerns for
  the owning project rather than reasons to keep this PoP open.

Final representative experiment baseline:
`brainboxemb/exp.2026-008.javafx-docking@aea57c394743e742778c3493652ebc5f564f6a7d`.

## Production handoff

The PoP does not select the Event Timing Desktop GUI Application (SI-02)
technology by itself.

Its evidence is handed to **Event Timing Step 6 D02 — GUI technology, runtime,
client-library and packaging decision**. That decision must compare the qualified
JavaFX/BentoFX direction with credible alternatives against the SI-02 Draft
requirements and must separately choose the IF-03 HTTP/WebSocket client and
distribution model.

The experiment repository remains retained as implementation/evidence and may be
used again when a future workbench regression can be represented there. It is not
a production dependency.
