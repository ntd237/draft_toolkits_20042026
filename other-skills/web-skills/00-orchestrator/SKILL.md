---
name: 00-orchestrator
description: "Central orchestrator for the full-stack web development pipeline (frontend, backend, database). Domain gatekeeper (rejects out-of-scope requests such as pure mobile-native or pure data science), classifies requests (new implementation / unknown-cause bug / known-cause bug), assesses complexity and risk, identifies involved layers (frontend/backend/database/multi-tier), and routes to the appropriate child skill sequence (01-brainstorm, 02-plan, 03-implement, 04-bugfinder, 05-fix, 06-test, 07-review) across 6 standard scenarios. Triggers for EVERY frontend/backend/database code request before any child skill runs — this is the mandatory entrypoint, not a skill directly invoked by the user."
---

# 00-orchestrator — Full-Stack Pipeline Orchestrator (TDD-first)

## Trigger
Triggers for any request touching frontend/backend/database code: implementing new features, fixing bugs, optimizing performance, refactoring. This is the mandatory first step in the pipeline — no child skill (01–07) may run directly bypassing orchestrator classification, unless the user explicitly invokes a child skill by name.

## Workflow

### Phase 1: Domain Gate
**Objective**: Confirm the request is within the frontend/backend/database scope before routing.

1. If the request is entirely out of scope (pure mobile-native without web view, data science/ML training, infrastructure DevOps unrelated to application code, pure graphic design) → politely decline, clearly state that this skill toolkit covers web frontend/backend/database, and do not process unilaterally.
2. If the request is mixed (e.g., "deploy app to K8s" accompanied by backend code changes) → only handle the in-scope code changes, clearly noting that the out-of-scope portion requires other tools.
3. If the domain is clearly in scope → record the involved layers (frontend / backend / database / multi-tier) for use in Phase 2.

### Phase 2: Request Classification
**Objective**: Classify the request into 1 of 3 categories to select the correct scenario branch.

1. **New Implementation** (feature, refactor, proactive optimization) → evaluate requirement clarity and complexity (Phase 3).
2. **Unknown-Cause Bug** (symptoms described but no root cause: "app is slow", "API occasionally returns incorrect data") → mandatory routing through `04-bugfinder` first.
3. **Known-Cause Bug** (user pinpointed the exact offending line/query/component, clear traceback provided, or bugfinder already ran in a previous turn) → may bypass `04-bugfinder`.

### Phase 3: Complexity & Risk Assessment
**Objective**: Determine whether `01-brainstorm` and/or `02-plan` are mandatory.

Assess complexity/risk based on: number of layers touched (single layer vs multi-tier), number of modules/files involved, whether DB schema or API contracts are changed, and whether critical business flows (payments, auth) are affected.

- **Ambiguous** request (lacks acceptance criteria, unclear which layer is responsible) → mandatory `01-brainstorm` before doing anything else.
- **Complex / High Risk / Multi-tier** request → mandatory `02-plan` (may follow `01-brainstorm` if both ambiguous and complex).
- **Simple, Clear, Single-layer, Low Risk** request → bypass both brainstorm and plan, enter the TDD loop directly.

### Phase 4: Route to Scenario
**Objective**: Select exactly 1 of 6 scenarios and sequentially coordinate child skills, waiting for approval at checkpoint gates.

| # | Condition | Skill Sequence |
|---|---|---|
| 1 | Simple implementation | `06-test` (Red) → `03-implement` (Green+Refactor)* → `07-review` |
| 2 | Ambiguous implementation | `01-brainstorm` → approval → `06-test` (Red) → `03-implement` (Green+Refactor)* → `07-review` |
| 3 | Complex / high risk / multi-tier implementation | `01-brainstorm` → approval → `02-plan` → approval → [multiple parallel TDD waves per atomic behavior]* → `07-review` |
| 4a | Unknown-cause bug, simple | `04-bugfinder` → `06-test` (Red) → `05-fix` (Green+Refactor)* → `07-review` |
| 4b | Unknown-cause bug, complex / multi-tier | `04-bugfinder` → `02-plan` → approval → [multiple waves `06-test` Red → `05-fix` Green]* → `07-review` |
| 5 | Known-cause bug, simple | `06-test` (Red) → `05-fix` (Green+Refactor)* → `07-review` |
| 6 | Known-cause bug, complex | `02-plan` → approval → [multiple waves `06-test` Red → `05-fix` Green]* → `07-review` |

(*) Repeat per atomic behavior unit; if TDD is infeasible for a specific unit (spike, exploratory UI), invert to implement/fix → test for that specific unit only; see `references/tdd-exception-handling.md`.

After selecting the scenario, the orchestrator invokes each child skill in strict order, passing: original request description, involved layers, brainstorm/plan results (if any), and current Red/Green state.

### Phase 5: Review Gate — Mandatory Re-route on 07-review Failure
**Objective**: Handle failure results from `07-review` by mandating a return to the appropriate bug-fix branch (4a/4b/5/6), applicable to **all** original scenarios (even when the original scenario was already 4/5/6).

1. When `07-review` returns a "fail" verdict (detected logic errors, security vulnerabilities, or TDD cheating) — regardless of whether the original scenario was 1/2/3 (implementation) or 4/5/6 (bug fix) — the orchestrator **must** re-route to one of the 4 bug-fix branches. Review-fail must never be treated as "done", nor can execution arbitrarily jump back to `03-implement`/`05-fix` outside the standard pipeline.
2. Extract the root cause for branch selection **directly from the `07-review` report** (re-running `04-bugfinder` for independent investigation is not mandatory): if the report pinpoints the exact location (file/line/query/config) → treat as "known cause" → branch 5/6; if the report only describes symptoms/suspicions without sufficient specificity → treat as "unknown cause" → branch 4a/4b, using the review report itself as the bootstrap input for `04-bugfinder` (no need to investigate from scratch).
3. Re-evaluate complexity / blast radius (per the table in `references/tdd-exception-handling.md`) based on the review report to choose between 4a/5 (simple) and 4b/6 (complex/multi-tier) — the issue uncovered by review may be simpler or more complex than the original request; re-evaluate instead of blindly copying the previous turn's complexity.
4. After the new bug-fix branch completes (reaching `07-review` again), repeat Phase 5 if it still fails — no arbitrary loop limit, but if failure recurs ≥3 times on the same issue, stop and report to the user instead of looping indefinitely.

## Output Format
Before routing, output a brief summary block: Domain check (pass/reject + reason) → Classification (implementation/known bug/unknown bug) → Complexity assessment (simple/ambiguous/complex) → Selected scenario (# in table) → Skill sequence to invoke. Then proceed to invoke the first skill in the sequence. If handling a re-route after review-fail, additionally state: failed original scenario → newly selected bug-fix branch (4a/4b/5/6) → rationale (root cause from review report, simple or complex).

## Don'ts
- Do not arbitrarily bypass `04-bugfinder` when the bug's cause is unclear, even if the user seems in a rush.
- Do not arbitrarily bypass `02-plan` when the request touches ≥2 layers or changes DB schema / API contracts, even if individual parts appear simple.
- Do not combine approval steps of `01-brainstorm` and `02-plan` into one if both are mandatory — each requires separate confirmation before proceeding.
- Do not guess the scenario when input signals are insufficient for classification (e.g., unclear whether it is a bug or new feature) — ask a brief clarifying question instead of guessing.
- Do not treat an `07-review` failure as pipeline completion or arbitrarily jump back to `03-implement`/`05-fix` outside the standard pipeline — must go through Phase 5 to select the appropriate 4a/4b/5/6 branch.
- Do not auto-loop Phase 5 indefinitely when the same issue fails repeatedly — stop on the 3rd recurrence and report to the user.

## Quality Checklist
- [ ] Has the domain gate run with a clear pass/reject conclusion before routing?
- [ ] Has the request been properly classified into 1 of the 3 groups (implementation / known bug / unknown bug)?
- [ ] Does the selected scenario match the 6-scenario table without arbitrary improvisation?
- [ ] If a scenario with mandatory brainstorm/plan is selected, is there an approval wait step before proceeding?
- [ ] Are child skills invoked in the correct order, passing involved layers and necessary context?
- [ ] If `07-review` fails, is re-routing to the proper 4a/4b/5/6 branch enforced (for all original scenarios, including 4/5/6) without skipping Phase 5?
- [ ] Is the new bug-fix branch chosen based on root cause/complexity from the `07-review` report itself, freshly re-evaluated rather than copying previous complexity?
