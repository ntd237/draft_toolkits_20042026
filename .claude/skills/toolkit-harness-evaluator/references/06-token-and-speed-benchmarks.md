# Phase 6 — Token Economy & Response Latency

## Objective

A bundle that produces excellent output but loads 30k tokens per turn and waits 90 seconds for completion is operationally worse than a leaner bundle. This phase turns *cost-to-run* into a graded score.

Scope: **Claude Code only**. No multi-platform comparisons. No third-party providers.

## What Counts as "Loaded"

For a given user invocation of a skill, the *loaded* tokens are:

1. Always-on context: `CLAUDE.md`, `MEMORY.md`, all `@-imported` rules and harness protocol files.
2. The skill's `SKILL.md`.
3. Any reference files the skill instructs the assistant to read at the start of a phase.
4. Any agent / command file the skill routes to.

Tokens added later during execution (file reads, tool outputs) are not part of the *load* score; they belong to the run-time variance.

## Token Estimation Method

Use a consistent token-estimation rule for every bundle:

- Default: **1 token ≈ 4 characters** for English/Vietnamese mixed prose. This matches the Claude tokenizer's typical density closely enough for comparison.
- Code blocks: 1 token ≈ 3.5 characters (denser).
- For each file, compute `tokens ≈ ceil(byte_length / 4)`.

Always label the number as **estimated**. Live measurement is `deep` mode only.

### Per-Skill Load Budget

```
load_tokens(skill) =
    tokens(CLAUDE.md)
  + tokens(MEMORY.md)
  + sum(tokens(rule) for rule in @-imported_rules)
  + sum(tokens(protocol) for protocol in @-imported_harness)
  + tokens(SKILL.md)
  + sum(tokens(ref) for ref in references referenced in phase 1 of SKILL.md)
```

A skill that lazy-loads references later in the workflow is rewarded; a skill that imports everything up-front is penalized.

## Token Economy Score (0–8)

Award based on bundle-level averages and worst-case loads:

| Bundle behaviour | Points |
|---|---:|
| Average per-skill load ≤ 6k tokens; max ≤ 9k; lazy-loading evident | 8 |
| Average ≤ 9k; max ≤ 14k | 6 |
| Average ≤ 14k; max ≤ 20k | 4 |
| Average ≤ 20k; max ≤ 30k | 2 |
| Average > 20k or max > 30k | 0 |

Apply additional modifiers:

- **+1** if the bundle clearly separates always-on context from per-skill content (e.g., uses `references/` lazy loading).
- **-1** if rule files exceed 200 lines without splits.
- **-1** if `CLAUDE.md` re-imports content already present in skills.
- **-1** if any skill embeds another skill verbatim.

Cap final score at 8. Show the math.

## Latency / Response Speed Score (0–5)

Latency is graded as a function of:

1. **Round-trip count expected per task** — each phase that requires user approval, each tool call cluster, each handoff between agents.
2. **File reads expected** — total bytes the workflow forces the assistant to read before producing output.
3. **Decision granularity** — "ask for approval per command" doubles latency; lazy-loading saves it.

Static scoring rubric:

| Behaviour | Points |
|---|---:|
| ≤ 2 round-trips on a typical task; ≤ 30 KB read budget; lazy refs | 5 |
| 3–4 round-trips; ≤ 60 KB read; some eager loading | 3 |
| 5–6 round-trips; > 60 KB read; mostly eager | 1 |
| > 6 round-trips OR > 100 KB read budget per task | 0 |

If the bundle's commands force per-command approval gates that the user did not opt into, deduct 1 (cap at 0).

## Live Measurements (deep mode only)

If the user approves live runs:

1. Pick three canonical tasks: small refactor, medium feature add, hard bug fix.
2. For each, run the bundle's recommended skill/command in a fresh Claude Code session.
3. Capture from the session:
   - Wall-clock duration from command start to `verdict: VERIFIED` (or final assistant message).
   - Total input + output tokens, if exposed by the CLI.
   - Number of tool calls made.
4. Persist measurements under `docs/toolkit-evaluation/measurements/<bundle-label>.csv`.

Use measured numbers in place of estimates **only** when both bundles in a comparison were measured under the same setup.

## Reporting Format

```
### Token Economy
| Skill | Always-on (tokens) | SKILL.md | Phase-1 refs | Total load | Bucket |
|---|---:|---:|---:|---:|---|
| <skill> | xxxx | xxxx | xxxx | xxxxx | green/yellow/red |
| ... |

Average load: xxxx tokens
Max load: xxxxx tokens (skill: <name>)
Modifiers applied: <list>
Final token economy: x/8
```

```
### Latency
- Typical task round-trips: <n>
- Typical read budget per task: <KB>
- Approval-gate cost: <description>
- Static estimate: x/5
- Live measurements (if any): see csv
```

## Comparing Bundles on These Axes

When the report ranks N bundles, present a head-to-head table:

```
| Bundle | Avg load (tokens) | Max load | Round-trips | Token score | Latency score |
|---|---:|---:|---:|---:|---:|
| A | ... |
| B | ... |
```

Tie-break on these axes uses **average load** before **max load**.

## Required Practices

- Always show the per-skill table — never a single aggregate number.
- Always label numbers as `estimated` or `measured`.
- Always identify the heaviest skill in the bundle and explain what makes it heavy.
- Always use the same token-estimation rule across bundles in a comparison.

## Prohibited Practices

- Do not measure tokens by counting words; use character-based estimates as defined.
- Do not award token-economy points for a bundle that hides bulk in `references/` if those references are eagerly loaded by the SKILL.md's first phase.
- Do not run live latency tests without per-test user approval, and never against billed APIs without budget approval.
- Do not extrapolate measured numbers from one bundle onto another; measure each.
