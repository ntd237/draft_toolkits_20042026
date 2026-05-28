# Phase 11 — Comparative Analysis

## Objective

When the user supplies two or more bundles, the report must produce a **ranked comparison** with explicit deltas, head-to-head tables, and tie-break decisions. A list of independent scorecards is not a comparison.

## When This Phase Activates

- N = 1 bundle → skip this phase. Use the single-bundle report from Phase 12.
- N ≥ 2 bundles → run this phase **after** every bundle has completed Phases 1–10 independently.

## Inputs

For each bundle:
- Final total score (from `08-scoring-rubric.md`)
- Letter grade after caps
- All 11 axis sub-scores
- Tier ceiling (Phase 5)
- Critical / important / hygiene gap lists (Phase 2)
- Bottom-three skills (Phase 3)
- Token / latency numbers (Phase 6)
- Governance pillar scores (Phase 7a)

## Comparison Outputs

### O1. Ranked Leaderboard

```
### Leaderboard

| Rank | Bundle | Total | Letter | Tier ceiling | Gov | Plan | Bugfinder | Fix-Bug | Parallel | Orchestrator | Token | Latency |
|---:|---|---:|:---:|:---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | <name> | xx.x | <L> | <T> | x.x | x | x | x | x | x | x | x |
| 2 | <name> | xx.x | <L> | <T> | x.x | x | x | x | x | x | x | x |
| ... |
```

Sort by total descending, breaking ties per `10-scoring-rubric.md` rules. Always show the cap, if any, that pinned a letter grade below its band.

### O2. Per-Axis Head-to-Head

For every axis A1–A13, show all bundles in one row each. Highlight the leader and the laggard.

```
### Per-Axis Comparison

| Axis | Weight | Bundle A | Bundle B | Bundle C | Leader | Spread |
|---|---:|---:|---:|---:|:---:|---:|
| A1 Coverage    | 13 | 11.0 | 12.0 | 8.0 | B | 4.0 |
| A2 Breadth     |  8 | ... |
| ... |
| A12 Parallel   |  5 | ... |
| A13 Orchestrator| 7 | ... |
```

`Spread` = max − min across bundles.

### O3. Strengths / Weaknesses Card per Bundle

For each bundle, output one card.

```
### <Bundle name>
- **Final**: xx.x — <Letter> (cap: <if any>)
- **Strengths** (top 3 axes by absolute score, weighted): <axis> (xx), <axis> (xx), <axis> (xx)
- **Weaknesses** (bottom 3 axes by absolute score, weighted): <axis> (xx), <axis> (xx), <axis> (xx)
- **Tier ceiling**: <E/M/H/V/S>
- **Critical gaps**: <list, or "None">
- **Standout skill**: <path> — <one line>
- **Worst skill**: <path> — <one line>
```

### O4. Pairwise Delta Matrix (when N ≤ 4)

For 2–4 bundles, show pairwise total deltas:

```
### Pairwise Deltas (rows beat columns by delta points)

|       | A   | B    | C    |
|-------|----:|-----:|-----:|
| **A** |  -  | -3.0 | +5.5 |
| **B** | +3.0|  -   | +8.5 |
| **C** | -5.5| -8.5 |  -   |
```

Negative deltas in the row = column is stronger. Use one decimal.

For N > 4, replace pairwise matrix with a top-3 / bottom-3 callout instead.

### O5. Use-Case Recommendation

Translate scores into recommendations across project archetypes:

```
| Project archetype | Recommended bundle | Why (≤ 1 line) |
|---|---|---|
| Web frontend     | <name> | strong UI design + plan |
| Web backend      | <name> | strong governance + bugfinder |
| Mobile           | <name> | UI design covers RN/Flutter explicitly |
| AI/ML            | <name> | plan handles experiment loops |
| Data pipeline    | <name> | retry policy + verification protocol best fit |
| CLI / library    | <name> | refactor + docs strongest |
| Infra / IaC      | <name> | security review + governance |
| Game / Graphics  | <name> | only one bundle acknowledges; otherwise n/a |
```

If no bundle is suited for an archetype, write "None" and explain.

### O6. Anti-Recommendations

List any bundle that should **not** be used for a given context, with reason. Example: "Bundle B's token economy makes it impractical for routine fix-bug work in budget-constrained sessions."

### O7. Migration Notes

If bundles share lineage (one is a fork or refactor of another), note what the newer revision changed and whether the change improved score. Detect by:

- Identical or near-identical CLAUDE.md.
- Skills with identical names but mutated content.
- Diffs in `references/` files.

## Required Practices

- Always rank, never just list.
- Always show every bundle on every axis.
- Always carry the cap explanation when a letter is pinned.
- Always mark the leader and laggard per axis explicitly.
- Always include the use-case recommendation table.
- Always preserve all per-bundle scorecards; the comparison adds, it does not replace.

## Prohibited Practices

- Do not collapse multiple bundles into a "fleet average".
- Do not declare a winner without showing the delta.
- Do not hide caps in footnotes; caps belong in the leaderboard row.
- Do not recommend a bundle for an archetype unless its skills/agents acknowledge that archetype.
- Do not editorialize beyond the evidence — every claim in the comparison still requires a phase-level citation.
