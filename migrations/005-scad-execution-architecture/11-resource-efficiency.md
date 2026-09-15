# Migration 005 — resource efficiency and compute cost

Status: **architecture evaluation criterion**

Migration 005 must not optimize CI only for wall-clock latency. The architecture also consumes hosted compute, network transfer, storage and energy. Those costs matter even when an open-source project is not billed directly for every runner-minute.

## Two different performance questions

Every candidate architecture must answer both:

1. **How long does a maintainer wait?**
2. **How much infrastructure work is consumed to produce that answer?**

Those are not the same metric.

The Migration-004 comparison demonstrates the trade-off clearly:

- the old Build + Verify topology used two heavy hosted jobs in parallel and returned relevant feedback in about 37 seconds;
- the final one-host topology uses one heavy hosted job and returns relevant feedback in about 41–45 seconds;
- the old design therefore had the shorter critical path, but paid for it with duplicated runner/container setup and simultaneous VM use;
- README-only changes in the final model are better on both axes because they finish in about 4–5 seconds without starting the heavy CAD runtime at all.

## Required metrics

Architecture experiments should record, where practical:

| Metric | Meaning |
| --- | --- |
| wall-clock feedback latency | elapsed time from workflow start until useful result |
| total runner-seconds/minutes | sum of active hosted-runner time across all jobs |
| maximum heavy-runner concurrency | how many expensive VMs/jobs are active simultaneously |
| container count/startups | number of SCAD runtime initializations |
| repeated image transfer | duplicated network/download/unpack work |
| duplicated source/tool setup | repeated checkout/submodule/bootstrap work |
| productive execution time | time actually spent producing or verifying required CAD output |
| avoided work | irrelevant domains/runtimes correctly skipped |
| artifact/cache transfer | bytes/time spent saving and restoring intermediate state |

A design should not claim a performance improvement from only one row.

## How to interpret trade-offs

### Faster but substantially heavier

Two parallel runners may be justified when they reduce feedback latency materially for genuinely independent expensive work. They should not be preferred merely because parallelism makes the stopwatch look better if most of the duplicated time is setup/download overhead.

### Slower but substantially lighter

One runner may be preferable when the latency penalty is small and it removes a large amount of duplicated compute. It is not acceptable to serialize work indefinitely under the label of efficiency.

### Best case

Prefer architectures that remove work rather than only rearrange it:

- do not start CAD for README-only changes;
- do not execute unaffected capabilities;
- avoid repeated image/tool downloads where reuse is economical;
- avoid uploading retained artifacts nobody consumes;
- reuse trustworthy source-derived output when that reuse costs less than recomputation.

These improve both user latency and infrastructure efficiency.

## Migration-005 decision rule

The target architecture should be selected using a balanced score:

```text
correctness and evidence integrity
        +
human understandability
        +
feedback latency
        +
total compute/resource use
        +
implementation/maintenance complexity
```

No candidate wins solely because it is fastest, uses the fewest containers, or has the shortest YAML file.

Where two candidates offer similar correctness and maintainability, prefer the one that achieves the required feedback with less total hosted compute and duplicated work.

## Environmental interpretation

This migration will not attempt to estimate exact carbon emissions from GitHub-hosted runners because the required hardware, utilization and electricity-source data are not available with sufficient precision.

Instead it will use measurable engineering proxies:

- runner time;
- runner concurrency;
- duplicated execution;
- transferred bytes;
- avoidable container/runtime startups.

Reducing those proxies is a reasonable engineering goal for both indirect cost and energy use without pretending to provide an unsupported emissions number.
