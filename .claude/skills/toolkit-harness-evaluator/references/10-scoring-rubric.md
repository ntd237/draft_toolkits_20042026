# Phase 10 — Final Scoring Rubric

## Objective

Combine the per-phase outputs into a single, reproducible numeric score and letter grade. The score must be defensible: every digit traceable to a phase output, no ad-hoc adjustments.

## Axis Weights (sum to 100)

| # | Axis | Source phase | Weight |
|---|---|---|---:|
| A1 | Coverage Completeness (canonical 11 categories) | Phase 2 | **13** |
| A2 | Coverage Breadth across project archetypes | Phase 2 | **8** |
| A3 | Per-Skill Content Quality (averaged) | Phase 3 | **12** |
| A4 | Plan Skill Capability | Phase 4.1 | **8** |
| A5 | Debug Skill Capability | Phase 4.2 | **7** |
| A6 | Bugfinder Capability across difficulty tiers | Phases 4.3 + 5 | **9** |
| A7 | Fix-Bug Capability | Phase 4.4 | **8** |
| A8 | UI Design Skill Capability | Phase 4.5 | **5** |
| A9 | Token Economy | Phase 6 | **6** |
| A10 | Response Latency / Throughput | Phase 6 | **4** |
| A11 | Harness-Runtime Governance Completeness | Phase 9 | **8** |
| A12 | Parallel Execution Capability | Phase 7 | **5** |
| A13 | Orchestrator Coordination Quality | Phase 8 | **7** |
| | **Total** | | **100** |

## Mapping Phase Outputs to Axis Points

### A1 Coverage Completeness (13)

```
present  = count(categories marked Present, max 11)
partial  = count(categories marked Partial)
absent   = count(categories marked Absent)

A1 = round( (present + 0.4 * partial) * 13 / 11 )
```

Cap at 13. If any category among **5 (Bug Diagnosis), 6 (Bug Fixing), 1 (Planning)** is `Absent`, A1 ≤ 4 (these three are the harness backbone).

### A2 Coverage Breadth (8)

```
supported = count(archetypes acknowledged, out of 9)
A2 = round(supported * 8 / 9)
```

Mention is sufficient; deep specialization is not required. Hard-cap at 8.

### A3 Per-Skill Content Quality (12)

```
avg = mean(normalized score of each skill, 0–100)
A3 = round(avg * 12 / 100)
```

If the bottom-three skills are each below 40, apply -2 (these drag every workflow they appear in).

### A4 Plan (8)

Direct mapping from Phase 4.1 score (0–8).

### A5 Debug (7)

Direct mapping from Phase 4.2 score (0–7).

### A6 Bugfinder (9)

```
A6 = round(tier_total * 9 / 20)   # Phase 5 produces tier_total in 0–20
```

Cap at 9.

### A7 Fix-Bug (8)

Direct mapping from Phase 4.4 score (0–8).

### A8 UI Design (5)

Direct mapping from Phase 4.5 score (0–5).

### A9 Token Economy (6)

```
A9 = round(token_score * 6 / 8)   # Phase 6 token-economy score in 0–8
```

Cap at 6.

### A10 Response Latency (4)

```
A10 = round(latency_score * 4 / 5)   # Phase 6 latency score in 0–5
```

Cap at 4.

### A11 Governance (8)

```
A11 = round(gov_score * 8 / 9)   # Phase 9 governance score in 0–9
```

Cap at 8.

### A12 Parallel Execution (5)

Direct mapping from Phase 7 score (0–5).

### A13 Orchestrator Coordination (7)

Direct mapping from Phase 8 score (0–7).

## Total

```
total = A1 + A2 + A3 + A4 + A5 + A6 + A7 + A8 + A9 + A10 + A11 + A12 + A13
```

## Grade Bands

| Letter | Range | Meaning |
|---|---|---|
| **S** | 92–100 | Exceptional. Reference-grade harness; minor polish only. |
| **A** | 82–91 | Strong. Production-ready, gaps are hygienic. |
| **B** | 70–81 | Solid. Usable; specific axes need investment. |
| **C** | 58–69 | Functional. Several axes weak; not yet a complete harness. |
| **D** | 45–57 | Partial. Operates as a prompt collection more than a harness. |
| **F** | < 45 | Insufficient. Missing core categories or governance. |

## Caps & Safeguards

These caps override the band table:

- **Critical-coverage cap**: any of the 11 canonical categories `Absent` → final letter capped at **D**.
- **Backbone cap**: any of categories 1 / 5 / 6 `Absent` → final letter capped at **F**.
- **Governance cap**: A11 < 3 → final letter capped at **C**, regardless of total.
- **Capability floor cap**: any of A4–A8 at zero → final letter capped at **C**.
- **Token cliff cap**: A9 = 0 → final letter capped at **B** (an unusable token economy outweighs other strengths).
- **Orchestrator cap**: A13 = 0 → final letter capped at **C** (an unorchestrated bundle is an inventory, not a harness).
- **Evidence-integrity cap**: if more than 25% of skills have missing referenced files, final letter capped at **C**.

When multiple caps trigger, apply the strictest.

## Display Format

```
### Final Score: <bundle-label>

| Axis | Weight | Score | Notes |
|---|---:|---:|---|
| A1 Coverage Completeness | 13 | xx.x | <one-line evidence> |
| A2 Coverage Breadth      |  8 | x.x  | ... |
| A3 Skill Content Quality | 12 | xx.x | ... |
| A4 Plan                  |  8 | x.x  | ... |
| A5 Debug                 |  7 | x.x  | ... |
| A6 Bugfinder             |  9 | x.x  | tier ceiling = <H/V/S> |
| A7 Fix-Bug               |  8 | x.x  | ... |
| A8 UI Design             |  5 | x.x  | ... |
| A9 Token Economy         |  6 | x.x  | avg load <tokens> |
| A10 Latency              |  4 | x.x  | round-trips <n> |
| A11 Governance           |  8 | x.x  | ... |
| A12 Parallel             |  5 | x.x  | ... |
| A13 Orchestrator         |  7 | x.x  | ... |
| **Total**                | **100** | **xx.x** | |
| **Letter (after caps)**  | | **<S/A/B/C/D/F>** | <triggered cap, if any> |
```

## Tie-Breakers

When two bundles' totals are within 2 points, break ties in this order:

1. Higher A11 (governance) wins.
2. Higher A13 (orchestrator) wins.
3. Higher A6 (bugfinder) wins.
4. Higher A12 (parallel) wins.
5. Higher A3 (skill content quality) wins.
6. Lower average token load (A9 stronger) wins.
7. Earlier alphabetical bundle label (deterministic).

## Worked Example (synthetic)

```
A1=11, A2=7, A3=10, A4=6, A5=5, A6=6, A7=6, A8=3, A9=4, A10=3, A11=6, A12=3, A13=4
total = 74
band  = B (70–81)
caps  = none triggered
final = B (74)
```

## Required Practices

- Always show every axis score in the table, even zeros.
- Always state which cap triggered, if any.
- Always rerun the math at the end of the report to confirm reproducibility.
- Always preserve per-bundle scores; never average across bundles for a "fleet score."

## Prohibited Practices

- Do not adjust weights "to account for project type" — weights are fixed; project-fit is communicated in the executive summary, not in the score.
- Do not soften caps for narrow bundles; if a bundle is intentionally narrow (e.g., UI-only), this rubric is the wrong rubric — say so and decline scoring rather than fudging.
- Do not award fractional points beyond one decimal place; round the total to one decimal.
