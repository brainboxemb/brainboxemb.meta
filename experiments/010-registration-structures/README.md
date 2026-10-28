# Experiment 010 — Java registration state and projection structures

Status: **active — architecture/prototype/qualification in progress**

Tracking issue: [#190](https://github.com/brainboxemb/brainboxemb.meta/issues/190)

Implementation/evidence repository:
[`brainboxemb/exp.2026-010.java-registration-structures`](https://github.com/brainboxemb/exp.2026-010.java-registration-structures)

Production reference:
`brainboxemb/2026-010-02.java.timing-point-application`

## Question

Which Java data/state architecture best supports the Event Timing registration path with
predictable allocation behaviour, efficient incremental mutations, competition ranking,
change propagation and display-facing projections?

This experiment deliberately treats those concerns as one data-management problem rather
than optimizing the ranking algorithm in isolation.

## Target workload

The normal design population is approximately **500 active registrations**. The preferred
architecture should prepare sensibly for that population without making 500 a hard limit.

The experiment must therefore distinguish:

- startup/preallocation cost for normal capacities such as 128, 512 and 1024;
- first population build to roughly 500 registrations;
- capacity/pool growth across boundaries such as 512 -> 513;
- steady-state mutation and query behaviour once normal capacity is available;
- larger populations such as 1,000 and 5,000 registrations;
- allocation bytes/op and explicit growth/allocation events.

Fresh-JVM startup is measured separately from warmed-JVM constructor/allocation cost so that
class loading/JIT and actual data-structure initialization are not conflated.

## Data path in scope

The representative experiment covers:

```text
registration / timing mutation
        |
        v
retained active registration state
        |
        +----> incremental ranking/index state
        |
        +----> change / dirty tracking
        |
        v
bounded display/query projection
        |
        v
display/client update
```

Representative mutations include:

- ADD registration/passage;
- REV/invalidation;
- stage-start SET/DEL changing elapsed time;
- repeated/equal elapsed times;
- state rebuild followed by live incremental updates;
- changes that affect one row versus changes that affect ordering/rank of many rows.

## Candidate model

The experiment starts with several intentionally different reference candidates rather
than assuming one implementation is production-ready:

1. rebuild/sort baseline matching the straightforward current approach;
2. sorted primitive storage with binary search and shifting;
3. JDK ordered-map/multiset-style object structures as a maintainability/reference point;
4. pooled order-statistic tree with occurrence/subtree counts and controlled growth;
5. broader registration/projection layouts added when needed to answer the data/change/display
   questions, not merely to improve a microbenchmark.

Candidate APIs and workloads should remain common so evidence is comparable.

## Correctness before performance

Every candidate must first match a simple oracle for deterministic and randomized mutation
sequences. Ranking uses competition semantics:

```text
rank = 1 + number of valid/rankable passages with a strictly smaller elapsed time
```

Equal elapsed times share a rank.

Change propagation/display tests must also prove that a consumer sees the correct final
projection without depending on incidental internal ordering or stale derived state.

## Qualification environments

The experiment uses two deliberately different environments:

1. **desktop / CI** — fast iteration, correctness, randomized tests, comparative profiling and
   repeatable benchmark development;
2. **Raspberry Pi Zero target hardware** — retained end-stage evidence for startup latency,
   preallocation/pool initialization, growth events, steady-state mutation/query performance,
   memory pressure and GC/allocation behaviour on constrained hardware.

Desktop results are useful for relative comparison and finding defects, but do not by themselves
select the production structure. Before a production adoption decision, the shortlisted candidates
must be rerun on the actual Pi Zero model/JVM intended for deployment.

The benchmark harness must therefore remain Java-version compatible with the production target,
non-GUI, command-line runnable, and able to emit machine-readable results without depending on
desktop-only profilers.

Target-image/environment ownership is deliberately outside this experiment. Event Timing tracks
that infrastructure separately in
[`2026-010-01.meta.event-timing-software#935`](https://github.com/brainboxemb/2026-010-01.meta.event-timing-software/issues/935),
with proposed repository `brainboxemb/2026-010-03.raspberry-pi-test-image`. Experiment 010
consumes that reproducible target environment; it does not build or own the Raspberry Pi image.

## Performance evidence

Performance qualification includes at least:

- constructor and initial-capacity allocation time;
- eager object-pool initialization versus capacity-only reservation;
- first 500 inserts;
- 512 -> 513 or equivalent growth event;
- steady-state ADD/REMOVE/REV/stage-start/rank queries;
- mixed update/query workload;
- worst-case ordered-array shifts;
- display-facing iteration/query/update workload;
- allocated bytes/op where the JVM exposes allocation counters;
- retained capacity/pool size and growth-event counts;
- the same shortlisted workload repeated on Raspberry Pi Zero, including fresh-process startup.

A fast steady state does not compensate for unacceptable startup cost, and low startup cost
does not compensate for recurring heap churn.

## Ownership

`brainboxemb.meta` owns:

- the cross-project question and experiment status;
- qualification expectations;
- the retained conclusion;
- the decision whether a production migration/refactor should start.

The experiment repository owns:

- candidate data structures;
- deterministic fixtures/oracles;
- correctness and randomized tests;
- benchmark/startup/allocation harnesses;
- retained machine-readable and readable evidence.

The Event Timing implementation repository remains owner of:

- production Registration/ActiveRegistrations behaviour;
- production display/client semantics;
- any later adoption after the experiment concludes.

## Production boundary

Experiment results do **not** automatically authorize production replacement.

No further registration-storage/ranking/change-propagation optimization should be selected
only from production-code iteration. A production change should reference the retained
Experiment 010 evidence and explain which qualified architecture is being adopted.
