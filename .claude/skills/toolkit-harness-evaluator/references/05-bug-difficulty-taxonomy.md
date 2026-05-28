# Phase 5 — Bug Difficulty Tier Taxonomy

## Objective

Differentiate bundles by the *hardest* class of bugs their bugfinder + fix-bug skills can credibly handle. A bundle that finds easy bugs is table-stakes; the separator is what happens at Hard / Very Hard / Super Hard.

This file defines the tiers, the example bug types per tier, the techniques required, and the grading procedure.

## Tier Definitions

### Tier E — Easy
**Hallmark**: single-file, single-symbol, immediately visible from one careful read.

Examples:
- Typos in identifiers
- Wrong comparison operator (`==` vs. `===`, `>` vs. `>=`)
- Off-by-one in array slicing
- Missing `await` on a single async call with obvious symptom
- Inverted boolean condition

Required technique: read the file, run the test, fix.

### Tier M — Medium
**Hallmark**: cross-file or cross-function; symptom is several frames removed from cause.

Examples:
- Stale parameter passed through three functions
- Type drift across module boundaries
- Cache invalidation missing one branch
- Wrong order of operations in middleware chain
- DTO field renamed in API but consumer not updated

Required technique: trace data flow, search references, build a small mental call graph, write a focused failing test.

### Tier H — Hard
**Hallmark**: state machines, lifecycles, ordering, concurrency, transactions, error-path interactions.

Examples:
- Race condition between connection-pool checkout and reset
- Re-entrant lock deadlock in non-obvious code path
- Idempotency-key reuse on retry under partial failure
- Event-loop starvation due to a CPU-bound branch
- Optimistic-locking version mismatch under load
- Missing rollback on outer transaction when inner rolls back
- Async iterator that leaks on early break

Required technique: model the state space, enumerate transitions, identify race window, build a deterministic reproducer (seed, schedule, fault injection), inspect logs/traces with timestamps.

### Tier V — Very Hard
**Hallmark**: integration / infrastructure / encoding / time / network / OS — bug lives at the seam between systems.

Examples:
- Timezone bug: cron drifts on DST or under UTC offset edge cases
- Encoding bug: UTF-8 vs. CP1258 vs. Latin-1 misinterpretation in a binary boundary
- TLS bug: SNI mismatch, certificate chain issue, OCSP soft-fail under proxy
- DNS bug: TTL races, IPv6 fallback, split-horizon misconfiguration
- Filesystem bug: case-sensitivity drift between local and prod, EXDEV on rename across mounts
- Process bug: SIGPIPE handling, file descriptor leak under fork+exec, ulimit ceilings
- Container bug: cgroup v1 vs v2 metric drift; OOMKill silent on liveness probe
- DB bug: phantom reads under READ COMMITTED, serializable conflict storms

Required technique: capture full environment fingerprint (OS, kernel, libc, container runtime, locale, TZ, charset), reproduce in an isolated sandbox, use system tracing (`strace`, `dtrace`, `eBPF`, `tcpdump`, `Wireshark`, `perf`), bisect against environment variables.

### Tier S — Super Hard
**Hallmark**: heisenbugs, performance cliffs, memory corruption, ABI mismatch, cross-language FFI, distributed-system anomalies, data corruption.

Examples:
- Use-after-free that only triggers under specific allocator + ASLR layout
- Data race that disappears under TSAN due to instrumentation reordering
- JIT deoptimization cliff caused by polymorphic call site with a single rare type
- TCP incast / microburst causing tail latency spikes only under specific NIC offload settings
- GC pause amplification by a finalizer chain
- Distributed deadlock: A→B→C→A across services with no single root
- Silent data corruption: 1-in-10⁶ checksum collision; reproduction requires production traffic shape
- Cross-FFI memory-ownership bug between Rust and Python causing intermittent SIGSEGV under specific Python version
- Cache-coherency / NUMA effect explaining "fast on dev, slow on prod" with identical CPU model

Required technique: combine sanitizers (ASAN/TSAN/MSAN/UBSAN), record-and-replay debugging (rr, time-travel), differential profiling, statistical analysis of distributions (not means), targeted fault injection, hypothesis grounded in hardware/runtime semantics.

## Per-Tier Capability Score (0–4 each)

For each tier, evaluate the bundle's bugfinder + fix-bug skills together. Award 0–4 based on:

- 0 — Skill does not address this tier; methodology is generic.
- 1 — Tier mentioned; methodology lists keywords but no concrete steps.
- 2 — Methodology partially present; missing key tools or stop rules.
- 3 — Solid coverage; named tools, named patterns, reproducer guidance.
- 4 — Authoritative coverage; multi-method approach, falsifiable hypotheses, escape conditions, examples.

A bundle without a `bugfinder-hard` (or equivalent named tier-split) almost never scores >2 on Tier H, and almost never scores >1 on Tiers V and S.

## Tier Coverage Matrix

```
| Tier | Score (0–4) | Evidence (file:line + ≤ 30-word quote) |
|---|---:|---|
| E (Easy)       | x/4 | <quote> |
| M (Medium)     | x/4 | <quote> |
| H (Hard)       | x/4 | <quote> |
| V (Very Hard)  | x/4 | <quote> |
| S (Super Hard) | x/4 | <quote> |
| Total          | xx/20 | (used as input to bug-tier sub-axis) |
```

The tier-coverage total (0–20) is normalized to fit Phase 4's bugfinder capability axis (0–10) using:

```
bugfinder_capability = round(tier_total / 2)   # 20 -> 10
```

## Tier Ceiling

Define the bundle's *tier ceiling* as the highest tier where score ≥ 3.

- Ceiling E: bundle handles only trivial bugs.
- Ceiling M: bundle handles cross-file logic bugs.
- Ceiling H: bundle handles concurrency / lifecycle bugs.
- Ceiling V: bundle handles infra/integration bugs.
- Ceiling S: bundle handles heisenbugs and ABI/perf cliffs.

The tier ceiling is reported in the executive summary and used as a tie-breaker in comparative analysis when overall scores are within 2 points.

## Required Tooling Vocabulary

A bundle that claims tier H+ coverage should reference, in its bugfinder/fix-hard prose, a meaningful subset of:

- Reproducers: deterministic seeds, fault injection, scheduler control
- Concurrency: TSAN, lock-order analysis, happens-before reasoning, fuzzers
- System: `strace`, `dtrace`, `eBPF`, `perf`, `Wireshark`, `tcpdump`
- Memory: ASAN, MSAN, valgrind, address sanitizer policies
- Distributed: distributed tracing (OpenTelemetry), structured logs with correlation IDs, time-travel debug
- Reproducibility: rr, gdb scripting, container snapshots
- Statistics: percentile latency, distribution shape, anomaly detection

Absence of all of these in tier H+ claims is automatic ≤ 1 score for that tier.

## Phase 5 Output

- Tier coverage matrix (E / M / H / V / S) with scores and evidence.
- Tier ceiling.
- Computed bugfinder capability score (0–10) feeding Phase 4 / Phase 7.

## Required Practices

- Always evaluate against the **strictest** tier the bundle claims; do not soften because the lower tiers are well-covered.
- Always demand named techniques for tier H+; conceptual prose is not enough.
- Always quote the strongest line in the bundle for each tier — the auditor's job is to find evidence, not to invent it.

## Prohibited Practices

- Do not collapse tiers — a 3 on Easy and a 3 on Super Hard are not interchangeable.
- Do not award H+ scores based on a single sentence acknowledging "concurrency bugs are hard."
- Do not penalize a bundle for naming tools it does not implement, *if* the methodology is otherwise sound — tools are the floor, methodology is the ceiling.
- Do not give a bundle a tier-S score without an evidence quote that includes both a methodology and a hypothesis-falsification mechanism.
