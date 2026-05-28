# Phase 8 — Orchestrator Coordination Quality

## Objective

A bundle's orchestrator decides which skills/agents fire, in what order, with what handoffs, and how the work converges. Bad orchestration produces redundant work, missed phases, lost context between handoffs, and silent failures. This phase grades how well a bundle's orchestration layer routes, sequences, and synchronizes work.

Scope: top-level orchestrators (`commands/`, `00-orchestrator`-style skill, `using-superpowers`), sub-agent dispatch wrappers, pipeline runners that coordinate multiple agents.

## What Counts as an Orchestrator

Any of:
- A slash command file that selects and chains skills/agents (`commands/fix.md`, `commands/feature.md`).
- A meta-skill that routes (`00-orchestrator`, `using-superpowers`, `find-skills`).
- A pipeline runner that executes phases in order with state (`harness_runner.py run-pipeline`).
- A sub-agent dispatcher template that constructs prompts for downstream agents.

A bundle without any of the above is an inventory, not a harness. Skip this phase only if Phase 1 confirms the bundle has zero orchestration surface — then assign A13 = 0.

## Per-Bundle Discovery Procedure

1. Identify every orchestrator surface (commands, top-level routing skill, pipeline runner).
2. For each surface, read the prose end-to-end and answer:
   - Which skills/agents does it route to, and based on what trigger?
   - Does it pass context (artifacts, scope, prior outputs) to downstream agents?
   - Does it define synchronization points (pause gates, review gates)?
   - Does it define error / retry / escalation paths?
   - Does it write a single canonical execution log?
3. Inspect a sample handoff: trace one end-to-end pipeline (e.g., `/fix` or `/feature`) and verify whether each handoff is well-defined or ambiguous.

## Scoring — Seven Sub-Criteria (0–1 each, total 0–7)

### O1. Routing Logic (0–1)
The orchestrator picks the right downstream agent/skill based on a stated decision algorithm.

- 0 — No routing logic; orchestrator is a thin wrapper.
- 0.5 — Routes based on keyword match without a decision tree.
- 1 — Explicit decision algorithm or table mapping intent → skill/agent, including edge cases.

### O2. Pipeline Sequencing (0–1)
Standard pipelines are pre-defined for common request shapes (small fix, complex feature, unknown bug, …).

- 0 — No standard pipelines.
- 0.5 — One or two examples without a complete library.
- 1 — A complete library of named pipelines (≥ 5) covering the common shapes.

### O3. Context Handoff (0–1)
When the orchestrator dispatches a downstream agent, it constructs a focused prompt with scope, artifacts, prior outputs — not just a forwarded user message.

- 0 — Forwards the user message verbatim.
- 0.5 — Some context is added (e.g., file paths) but no template.
- 1 — A handoff template is defined: scope, prior artifacts, success criteria, downstream agent's tool list.

### O4. Pause / Review Gates (0–1)
Critical transitions (after planning, after review, before destructive action) require user approval.

- 0 — No pause gates.
- 0.5 — Generic "ask before risky actions" line.
- 1 — Specific gates named per pipeline phase, with approval template.

### O5. Error & Retry Handoff (0–1)
When a downstream agent fails, the orchestrator knows how to re-dispatch, escalate, or roll back.

- 0 — Silent on failure.
- 0.5 — Says "retry" without specifying scope or limit.
- 1 — Integrated with retry policy: per-agent limits, no-patch-stacking, diagnostic summary on escalation.

### O6. State / Log Discipline (0–1)
The orchestrator owns the execution log; sub-agents do not write to it. The pipeline state is preserved across phases.

- 0 — No log requirement; sub-agents may write anywhere.
- 0.5 — Log mentioned but writer ownership unclear.
- 1 — Orchestrator-only writer rule + canonical path + per-agent + pipeline summary sections.

### O7. Convergence / Synthesis (0–1)
After parallel or multi-phase work, the orchestrator synthesizes results into a coherent output for the user — not a raw concatenation.

- 0 — No synthesis step.
- 0.5 — Summary is described but template is missing.
- 1 — Convergence step is explicit: how to merge sub-agent outputs, how to surface conflicts, how to format the final user reply.

### Total

```
O_total = O1 + O2 + O3 + O4 + O5 + O6 + O7   (max 7)
A13     = round(O_total)                     (axis weight 7)
```

## Penalty Modifiers

- **-1** if the orchestrator routes to skills/agents that do not exist on disk (dangling reference detected in Phase 1).
- **-1** if multiple orchestrators conflict (e.g., two top-level routers with overlapping triggers and no precedence).
- **-0.5** if pause gates are described but not enforceable in the bundle's runtime.
- **-0.5** if context handoff template references variables (e.g., `{prior_artifact}`) that the orchestrator never populates.

## Output Format

```
### Orchestrator Coordination Quality — <bundle>

| Criterion | Score | Evidence (file:line + ≤ 30-word quote) |
|---|---:|---|
| O1 Routing logic       | x.x | <quote> |
| O2 Pipeline sequencing | x.x | <quote> |
| O3 Context handoff     | x.x | <quote> |
| O4 Pause/review gates  | x.x | <quote> |
| O5 Error/retry handoff | x.x | <quote> |
| O6 State/log discipline| x.x | <quote> |
| O7 Convergence         | x.x | <quote> |
| Subtotal               | x.x/7 | |
| Modifiers              | -x.x | <reason> |
| **A13 Orchestrator /7**| **x.x** | |
```

## Live Smoke Test (deep mode, optional)

If the user approves and the bundle has a runner:

1. Pick one canonical pipeline (e.g., `fix`).
2. Run `<runner> run-pipeline --workflow fix --task "smoke" --dry-run` and capture exit code + log output.
3. Verify: was a log file created? Were phases visible? Were pause gates respected in dry-run?
4. Successful dry-run = +0.5 to O5 or O6 whichever is weakest, capped at the criterion ceiling.

## Required Practices

- Always trace one end-to-end pipeline through the orchestrator's prose before scoring.
- Always check that referenced skills/agents exist on disk; broken routes are a -1.
- Always score O3 by reading an actual handoff template — vague mentions are 0.

## Prohibited Practices

- Do not give O2 credit for a single named pipeline; require ≥ 5 to reflect real coverage.
- Do not award O7 for pipelines that just chain agents without a synthesis step.
- Do not run the bundle's runner without explicit per-command user approval, even in dry-run mode.
- Do not double-credit pause gates already counted in Permission Boundaries (Phase 9 G5) — pause gates here are *orchestrator transitions*, not file-system permissions.
