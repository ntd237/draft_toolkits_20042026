# Phase 4 — Specialized Capability Tests

## Objective

Move beyond content review and grade whether the bundle's specialized skills will actually **deliver** on plan, debug, bugfinder, fix-bug, and UI design tasks. Each skill is tested against an adversarial rubric. In `quick`/`standard` mode, run static analysis against the skill prompt + bundle examples; in `deep` mode, execute the live skill against canned prompts (with explicit user approval).

## Common Test Protocol

For every test below:

1. Identify the bundle's matching skill or agent (or note absent).
2. Run static analysis: simulate executing the skill on the test prompt by reading its workflow and asking — *would this prompt force the skill to produce the required output?*
3. In `deep` mode, execute the skill on the test prompt and capture the actual output.
4. Grade against the per-skill rubric below.

If the bundle does not have a matching skill, score **0** for that capability axis.

## 4.1 Plan Skill — Capability Rubric (0–8)

Test prompt (level 1, easy):
> "Add OAuth2 login with Google to an existing Express + Postgres app. Plan the work."

Test prompt (level 2, hard):
> "Migrate a 200k-LOC monolith Django app to a service-oriented architecture with three services. Plan it including data migration, rollout, and rollback."

Rubric (sum to 8):

- **Decomposition** (0–2) — Are phases distinct, ordered, with clear handoffs?
- **Verifiable success criteria** (0–2) — Each phase has a check the user can run.
- **Risk and rollback** (0–2) — Risks called out per phase; rollback path stated for irreversible steps.
- **Re-planning protocol** (0–1) — The skill explains how to update the plan when assumptions change.
- **Output discipline** (0–1) — The plan is saved/structured (Markdown file or canonical section), not free-form chat.

## 4.2 Debug Skill — Capability Rubric (0–7)

Test prompt:
> "The /api/users endpoint returns 500 only when the request body contains a unicode emoji in the `name` field. Investigate."

Rubric (sum to 7):

- **Reproduction-first stance** (0–2) — The skill demands a minimal reproducer before guessing.
- **Hypothesis–test loop** (0–2) — The skill enumerates hypotheses, ranks them, and tests one at a time.
- **Tooling literacy** (0–1) — Mentions language-specific debuggers, log levels, observability tools.
- **State capture** (0–1) — Captures input, env, version, stack trace verbatim before reasoning.
- **Stop conditions** (0–1) — Defines what "found the cause" means; avoids fix-creep into unrelated code.

## 4.3 Bugfinder Skill — Capability Rubric (0–10, gated by Phase 5 tier coverage)

Bugfinder is graded across the five bug difficulty tiers (Easy / Medium / Hard / Very Hard / Super Hard, defined in `references/05-bug-difficulty-taxonomy.md`).

Capability score = sum of tier-coverage scores below, capped at 10.

| Tier | Max points | Awarded if the skill |
|---|---:|---|
| Easy | 1 | Reads file, locates obvious typo / wrong operator / off-by-one. |
| Medium | 2 | Cross-file: traces a wrong return type or stale parameter through two modules. |
| Hard | 3 | Concurrency / state machine / lifecycle bug; identifies race window or invalid transition with evidence. |
| Very Hard | 2 | Diagnoses an infra/integration bug (timezone, encoding, certificate, DNS, kernel limit) with reproducer plan. |
| Super Hard | 2 | Diagnoses heisenbugs/perf cliffs/memory corruption with multi-tool methodology and a falsifiable hypothesis. |

A bundle with only `bugfinder` (no `bugfinder-hard` equivalent) maxes out around 5–6 unless the single skill explicitly walks the assistant through tier-3+ techniques (debuggers, sanitizers, perf tools, distributed tracing).

For each awarded tier, cite a workflow paragraph from the skill (or a reference file under it) that demonstrates the technique. No quote → no points.

## 4.4 Fix-Bug Skill — Capability Rubric (0–8)

Rubric (sum to 8):

- **Targeted change** (0–2) — Skill instructs assistant to touch only files implicated by root cause.
- **Verification-first fix** (0–2) — Demands a failing test (or reproducer) before the fix; demands re-run after.
- **Regression protection** (0–2) — Runs broader test suite; explains policy when no tests exist.
- **Tier escalation** (0–1) — Differentiates simple fixes from those requiring planner involvement.
- **Same-error escape** (0–1) — Has a stop rule when the same error reappears (per retry policy).

For bundles with both `fix` and `fix-hard`, score the **higher** capability of the two but require both files to exist.

## 4.5 UI Design Skill — Capability Rubric (0–5)

Test prompt:
> "Design a responsive dashboard (PC / tablet / mobile) for a Vietnamese cosmetics comparison app, including light/dark themes, accessible components, and a token-based design system."

Rubric (sum to 5):

- **Token-first system** (0–1) — Defines color/spacing/typography tokens; aligns to themes.
- **Multi-platform layouts** (0–1) — Web + at least one of desktop / mobile, with responsive breakpoints.
- **Accessibility** (0–1) — WCAG 2.1 AA references; contrast, focus, keyboard, ARIA.
- **Typography for Vietnamese** (0–1) — Diacritics-friendly font stacks and line-height guidance.
- **Implementation handoff** (0–1) — Stack-specific output (CSS variables / Tailwind / Flutter / SwiftUI) with concrete component examples.

## Static-Analysis Mode Procedure

When live execution is not possible:

1. Read the skill's `SKILL.md` and every reference file end-to-end.
2. Walk the test prompt through the skill's stated workflow on paper.
3. For each rubric criterion, decide:
   - "The skill **would** force this output" — full credit.
   - "The skill **might** produce this output if the assistant is careful" — half credit (round down).
   - "Nothing in the skill compels this output" — zero.
4. Cite the skill paragraph that justified each award.

## Live-Execution Mode Procedure (deep only)

1. Get explicit user approval before sending any test prompt.
2. Send each test prompt against the bundle (e.g., via a Claude Code session that has the bundle installed).
3. Capture the full transcript.
4. Score against the rubric using the transcript as evidence.
5. Persist transcripts under `docs/toolkit-evaluation/transcripts/<bundle-label>/<skill>.md`.

## Output of Phase 4

Per bundle:

- Plan capability score (0–8) with evidence.
- Debug capability score (0–7) with evidence.
- Bugfinder capability score (0–10) including the per-tier breakdown.
- Fix-bug capability score (0–8) with evidence.
- UI design capability score (0–5) with evidence.
- Optional transcripts directory (deep mode only).

## Required Practices

- Always cite a workflow excerpt for every awarded point.
- Always state whether the score is from static analysis or live execution.
- Always run both the easy and the hard plan/debug/fix prompts; never skip the harder one to avoid embarrassing the bundle.

## Prohibited Practices

- Do not award capability points based on the skill's own marketing description.
- Do not give credit for "the skill *could* in principle do X" — require workflow that *forces* X.
- Do not award full bug-tier credit when the skill's methodology is generic; tier-3+ requires named tools and techniques.
- Do not run live tests without per-prompt user approval.
- Do not paste full transcripts inline in the report; link to the persisted transcript file.
