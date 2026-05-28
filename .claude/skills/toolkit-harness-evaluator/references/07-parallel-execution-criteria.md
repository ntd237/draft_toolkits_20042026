# Phase 7 — Parallel Execution Capability

## Objective

Modern Claude Code workflows lean heavily on parallel tool calls and parallel sub-agent dispatch. A bundle that executes everything sequentially burns wall-clock time and tokens for no benefit. This phase grades how well a bundle exploits Claude Code's parallel-execution surface.

Scope: parallel **tool calls** (multiple Bash/Read/Grep in one message), parallel **sub-agent dispatch** (Agent tool with multiple invocations in one message), parallel **pipeline phases** (when independent steps run side-by-side).

## Why This Matters

- **Wall-clock**: 4 agents in parallel finish in ~1 agent's time, not 4×.
- **Token economy**: each parallel branch can keep its own focused context instead of dumping everything into the main thread.
- **Failure isolation**: a parallel sub-agent that fails does not block siblings.
- **Reviewer independence**: parallel reviewers without shared context produce more honest critiques.

A bundle that does not address parallelism explicitly is leaving capability on the table.

## What to Look For

For each bundle, search for evidence of these patterns:

1. **Explicit parallel-tool guidance**: prose telling the assistant to batch independent tool calls in a single message (e.g., "make all independent tool calls in parallel", "send a single message with N tool uses").
2. **Sub-agent fan-out**: skills that spawn ≥ 2 sub-agents in one dispatch (e.g., parallel reviewers, parallel scouts, parallel code-quality + spec-compliance reviewers).
3. **Pipeline parallelism**: workflow phases that explicitly mark steps as runnable concurrently, with merge/synchronization rules.
4. **Map-reduce / divide-and-conquer**: search/scout skills that split a codebase into N chunks, dispatch N agents, merge results.
5. **Independence rules**: explicit statement that "parallel only when no dependencies" and how to detect dependencies.
6. **Conflict / race handling**: rules for what happens when two parallel branches touch the same file or both want to write.

## Per-Bundle Discovery Procedure

1. Grep each bundle for terms: `parallel`, `concurrent`, `fan-out`, `dispatch`, `single message`, `simultaneously`, `independent`, `batch`, `map-reduce`, `divide`.
2. For each hit, read the surrounding paragraph and decide whether it is a **rule** (the skill forces parallelism), a **mention** (the skill names the concept without enforcing), or a **prohibition** (the skill bans parallelism for safety).
3. Inspect the heaviest skills (plan, debug, scout, review, subagent-driven-development): do they spawn parallel sub-agents in their workflow? Do they batch tool calls?
4. Inspect commands/agents: do command files instruct the orchestrator to dispatch sub-agents in parallel?
5. For harness-driven bundles, inspect `harness-runtime/config/pipelines.json` (or equivalent): does the pipeline schema support concurrent phases?

## Scoring — Six Sub-Criteria (0–1 each, total 0–6)

### P1. Parallel Tool-Call Guidance (0–1)
- 0 — No mention of batching independent tool calls.
- 0.5 — Mention but no clear rule.
- 1 — Explicit rule: "always batch independent tool calls in a single message" with a how-to.

### P2. Sub-Agent Fan-Out (0–1)
- 0 — Sub-agents are spawned one at a time.
- 0.5 — Some skills suggest spawning multiple but without enforcement.
- 1 — At least one skill explicitly spawns ≥ 2 sub-agents in one dispatch (e.g., scout + reviewers + executors), with prompt templates.

### P3. Pipeline Concurrency (0–1)
- 0 — No pipeline definition, or pipeline is strictly sequential.
- 0.5 — Pipeline supports independent phases but no mechanism to mark them parallel.
- 1 — Pipeline schema supports `parallel: true` (or equivalent) and the runner respects it.

### P4. Map-Reduce / Divide-and-Conquer (0–1)
- 0 — No skill divides work across N agents.
- 0.5 — One skill mentions splitting but doesn't define the merge step.
- 1 — At least one skill (typically scout/research) defines split → dispatch N → merge with explicit reduction rule.

### P5. Independence & Dependency Detection (0–1)
- 0 — Bundle does not warn about ordering dependencies.
- 0.5 — Generic warning ("only if independent").
- 1 — Concrete heuristic for when work is independent (no shared file, no upstream output dependency, no shared lock).

### P6. Conflict / Race Handling (0–1)
- 0 — Silent on what happens when parallel branches collide.
- 0.5 — Mentions the risk without a resolution.
- 1 — Defines locking, last-writer rule, or reject-and-retry policy when collisions occur.

### Total

```
P_total = P1 + P2 + P3 + P4 + P5 + P6   (max 6)
A12     = round(P_total * 5 / 6)        (axis weight 5)
```

## Penalty Modifiers

- **-1** if the bundle's plan/debug/fix workflow forces serial execution where parallelism is obviously safe (e.g., reading 5 unrelated files one at a time in 5 messages).
- **-0.5** if parallel guidance contradicts the bundle's own permission boundaries (e.g., parallel writers without write-lock policy).

## Output Format

```
### Parallel Execution Capability — <bundle>

| Criterion | Score | Evidence (file:line + ≤ 30-word quote) |
|---|---:|---|
| P1 Tool-call batching | x.x | <quote> |
| P2 Sub-agent fan-out  | x.x | <quote> |
| P3 Pipeline concurrency | x.x | <quote> |
| P4 Map-reduce         | x.x | <quote> |
| P5 Independence rules | x.x | <quote> |
| P6 Conflict handling  | x.x | <quote> |
| Subtotal              | x.x/6 | |
| Modifiers             | -x.x | <reason> |
| **A12 Parallel /5**   | **x.x** | |
```

## Required Practices

- Always cite a workflow excerpt for each awarded point — no quote, no points.
- Always check both prose **and** any pipeline / runner config; both count.
- Always penalize bundles that prevent parallelism by accident (e.g., per-command approval gates that force serial dispatch).

## Prohibited Practices

- Do not award P-points based on bundle marketing language ("supports parallel agents") if no skill or config enforces it.
- Do not equate "spawning a sub-agent" with parallelism — single sub-agent dispatch is just delegation, not parallelism.
- Do not give pipeline-concurrency credit for sequential pipelines that merely declare phase boundaries.
