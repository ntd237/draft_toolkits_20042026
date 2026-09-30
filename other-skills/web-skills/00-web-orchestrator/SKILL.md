---
name: 00-web-orchestrator
description: "Central orchestrator for the full-stack web development pipeline (frontend, backend, database, and app-level deployment/CI). Domain gatekeeper (rejects out-of-scope requests such as pure mobile-native or pure data science; app-related deployment is in scope, pure infrastructure is not), classifies requests (new implementation / unknown-cause bug / known-cause bug), assesses complexity and risk, identifies involved layers (frontend/backend/database/multi-tier), and routes to the appropriate child skill sequence (01-web-brainstorm, 02-web-plan, 03-web-implement, 04-web-bugfinder, 05-web-fix, 06-web-test, 07-web-review) across 6 standard scenarios. Triggers for EVERY frontend/backend/database/deployment code request before any child skill runs — this is the mandatory entrypoint, not a skill directly invoked by the user. Also owns the mandatory harness execution log mechanism (docs/harness-logs/) for every pipeline run."
---

# 00-web-orchestrator — Full-Stack Pipeline Orchestrator (TDD-first)

## Trigger
Triggers for any request touching frontend/backend/database code or app-level deployment: implementing new features, fixing bugs, optimizing performance, refactoring, configuring CI/CD or hosting for the app. This is the mandatory first step in the pipeline — no child skill (01–07) may run directly bypassing orchestrator classification, unless the user explicitly invokes a child skill by name.

## Workflow

### Phase 1: Domain Gate
**Objective**: Confirm the request is within the frontend/backend/database scope (including app-level deployment) before routing.

1. If the request is entirely out of scope (pure mobile-native without web view, data science/ML training, pure graphic design) → politely decline, clearly state that this skill toolkit covers web frontend/backend/database, and do not process unilaterally. Pure infrastructure work unrelated to application code (cluster provisioning, network/VPC configuration, database server administration) is also out of scope — but note the in-scope boundary below before declining.
2. **Deployment boundary**: requests touching deployment as it relates to the application itself ARE in scope — build configuration, CI/CD pipelines for the app, environment/config management, hosting configuration (static hosts, PaaS, containers running the app). Only hand off the pure-infrastructure remainder to external tools, clearly noting which portion requires other tooling.
3. If the request is mixed (e.g., "deploy app to K8s" accompanied by backend code changes) → only handle the in-scope code changes, clearly noting that the out-of-scope portion requires other tools.
4. If the domain is clearly in scope → record the involved layers (frontend / backend / database / multi-tier) for use in Phase 2.

### Phase 2: Request Classification
**Objective**: Classify the request into 1 of 3 categories to select the correct scenario branch.

1. **New Implementation** (feature, refactor, proactive optimization) → evaluate requirement clarity and complexity (Phase 3).
2. **Unknown-Cause Bug** (symptoms described but no root cause: "app is slow", "API occasionally returns incorrect data") → mandatory routing through `04-web-bugfinder` first.
3. **Known-Cause Bug** (user pinpointed the exact offending line/query/component, clear traceback provided, or bugfinder already ran in a previous turn) → may bypass `04-web-bugfinder`.

### Phase 3: Complexity & Risk Assessment
**Objective**: Determine whether `01-web-brainstorm` and/or `02-web-plan` are mandatory.

Assess complexity/risk based on: number of layers touched (single layer vs multi-tier), number of modules/files involved, whether DB schema or API contracts are changed, and whether critical business flows (payments, auth) are affected.

- **Ambiguous** request (lacks acceptance criteria, unclear which layer is responsible) → mandatory `01-web-brainstorm` before doing anything else.
- **Complex / High Risk / Multi-tier** request → mandatory `02-web-plan` (may follow `01-web-brainstorm` if both ambiguous and complex).
- **Simple, Clear, Single-layer, Low Risk** request → bypass both brainstorm and plan, enter the TDD loop directly.

### Phase 4: Route to Scenario & Checkpoint Gates
**Objective**: Select exactly 1 of 6 scenarios and sequentially coordinate child skills, strictly pausing for user approval at checkpoint gates.

| # | Condition | Skill Sequence |
|---|---|---|
| 1 | Simple implementation | `06-web-test` (Red) → `03-web-implement` (Green+Refactor)* → `07-web-review` |
| 2 | Ambiguous implementation | `01-web-brainstorm` → user approval (`docs/specs/spec-<name>.md`) → `06-web-test` (Red) → `03-web-implement` (Green+Refactor)* → `07-web-review` |
| 3 | Complex / high risk / multi-tier implementation | `01-web-brainstorm` → user approval (`docs/specs/spec-<name>.md`) → `02-web-plan` → user approval (`docs/plans/plan-<name>.md`) → [multiple parallel TDD waves per atomic behavior]* → `07-web-review` |
| 4a | Unknown-cause bug, simple | `04-web-bugfinder` → `06-web-test` (Red) → `05-web-fix` (Green+Refactor)* → `07-web-review` |
| 4b | Unknown-cause bug, complex / multi-tier | `04-web-bugfinder` → `02-web-plan` → user approval (`docs/plans/plan-<name>.md`) → [multiple waves `06-web-test` Red → `05-web-fix` Green]* → `07-web-review` |
| 5 | Known-cause bug, simple | `06-web-test` (Red) → `05-web-fix` (Green+Refactor)* → `07-web-review` |
| 6 | Known-cause bug, complex | `02-web-plan` → user approval (`docs/plans/plan-<name>.md`) → [multiple waves `06-web-test` Red → `05-web-fix` Green]* → `07-web-review` |

(*) Repeat per atomic behavior unit; if TDD is infeasible for a specific unit (spike, exploratory UI), invert to implement/fix → test for that specific unit only; see `references/tdd-exception-handling.md`.

#### Mandatory Approval Checkpoints:
1. **Brainstorm Checkpoint (`01-web-brainstorm`)**:
   - All questions must include an open write-in option for custom user answers.
   - After questions are addressed, a comprehensive summary must be presented.
   - **Mandatory pause**: wait for user review, supplementation (if needed), and explicit approval.
   - Upon approval, the spec is saved to `docs/specs/spec-<name>.md` in Vietnamese Markdown. The orchestrator must not proceed until approved.
2. **Plan Checkpoint (`02-web-plan`)**:
   - The plan artifact is generated and saved to `docs/plans/plan-<name>.md` in Vietnamese Markdown.
   - **Mandatory pause**: strictly halt execution and wait for user review, additions/modifications, and explicit approval.
   - The orchestrator and child skills must never advance to TDD waves / implementation without explicit user approval.

### Phase 5: Review Gate — Mandatory Re-route on 07-web-review Failure
**Objective**: Handle failure results from `07-web-review` by mandating a return to the appropriate bug-fix branch (4a/4b/5/6), applicable to **all** original scenarios (even when the original scenario was already 4/5/6).

1. When `07-web-review` returns a "fail" verdict (detected logic errors, security vulnerabilities, or TDD cheating) — regardless of whether the original scenario was 1/2/3 (implementation) or 4/5/6 (bug fix) — the orchestrator **must** re-route to one of the 4 bug-fix branches. Review-fail must never be treated as "done", nor can execution arbitrarily jump back to `03-web-implement`/`05-web-fix` outside the standard pipeline.
2. Extract the root cause for branch selection **directly from the `07-web-review` report** (re-running `04-web-bugfinder` for independent investigation is not mandatory): if the report pinpoints the exact location (file/line/query/config) → treat as "known cause" → branch 5/6; if the report only describes symptoms/suspicions without sufficient specificity → treat as "unknown cause" → branch 4a/4b, using the review report itself as the bootstrap input for `04-web-bugfinder` (no need to investigate from scratch).
3. Re-evaluate complexity / blast radius (per the table in `references/tdd-exception-handling.md`) based on the review report to choose between 4a/5 (simple) and 4b/6 (complex/multi-tier) — the issue uncovered by review may be simpler or more complex than the original request; re-evaluate instead of blindly copying the previous turn's complexity.
4. After the new bug-fix branch completes (reaching `07-web-review` again), repeat Phase 5 if it still fails — no arbitrary loop limit, but if failure recurs ≥3 times on the same issue, stop and report to the user instead of looping indefinitely.

## Output Format
Before routing, output a brief summary block: Domain check (pass/reject + reason) → Classification (implementation/known bug/unknown bug) → Complexity assessment (simple/ambiguous/complex) → Selected scenario (# in table) → Skill sequence to invoke. Then proceed to invoke the first skill in the sequence. If handling a re-route after review-fail, additionally state: failed original scenario → newly selected bug-fix branch (4a/4b/5/6) → rationale (root cause from review report, simple or complex).

## Handoff Contract Schemas
To eliminate ambiguity during transitions between child skills, skills must structure transition data using standard YAML handoff blocks:

### 1. TDD Red Handoff (`06-web-test` → `03-web-implement` or `05-web-fix`)
```yaml
handoff:
  from_skill: "06-web-test"
  to_skill: "03-web-implement" # or "05-web-fix"
  target_files: ["src/services/auth.ts"]
  failing_test_file: "tests/services/auth.test.ts"
  failing_test_name: "should return 401 when token expired"
  run_command: "npm test -- tests/services/auth.test.ts"
  observed_failure: "Expected 401, received 500"
  next_behavior: "Return 401 Unauthorized instead of throwing unhandled exception"
```

### 2. Defect Diagnosis Handoff (`04-web-bugfinder` → `06-web-test` or `02-web-plan`)
```yaml
handoff:
  from_skill: "04-web-bugfinder"
  to_skill: "06-web-test" # or "02-web-plan"
  offending_layer: "backend" # frontend | backend | database | multi-tier
  exact_location: "src/db/queries/order.ts:42"
  root_cause: "N+1 query loop when fetching order items without JOIN"
  blast_radius: "simple" # simple | complex
  recommended_fix: "Use INNER JOIN with items table and eager load"
  cleanup_verified: true # confirms all temporary debug instrumentation was removed
```

### 3. Review Defect Handoff (`07-web-review` FAIL → `00-web-orchestrator`)
```yaml
handoff:
  from_skill: "07-web-review"
  verdict: "FAIL"
  blocking_issues:
    - severity: "BLOCKING"
      layer: "backend"
      location: "src/api/payment.ts:115"
      root_cause: "Missing authorization check on refund endpoint"
      evidence: "Unauthenticated POST request returns 200 OK"
```

## Harness Execution Log (Mandatory)
Every pipeline run (Scenarios #1–#6) MUST produce a harness execution log file — in-chat YAML handoff blocks NEVER exempt or replace it.

1. **Before routing to the first skill**, Read `references/execution-log.md` and follow its schema verbatim: create `docs/harness-logs/<category>_<task_name>_<yyyymmdd>_<hhmmss>.md` (timestamp from a real shell command, never guessed), creating the directory if needed.
2. **After each child skill completes**, append its per-skill section immediately (do not batch at the end) — the orchestrator appends on behalf of the child skills.
3. **At pipeline completion** (including FAIL outcomes and Phase 5 re-routes), append the pipeline summary section. For Phase 5 re-routes, keep the same log file and append the re-route sections — never create a second file for the same task.
4. Log content is written in Vietnamese; skill names, file paths, commands, and status keywords (COMPLETED, FAILED, PARTIAL, PASS, FAIL) stay in English.
5. Single-skill, read-only advisory tasks (pure explanation, ad-hoc Q&A) do not require a log.

## Don'ts
- Do not arbitrarily bypass `04-web-bugfinder` when the bug's cause is unclear, even if the user seems in a rush.
- Do not arbitrarily bypass `02-web-plan` when the request touches ≥2 layers or changes DB schema / API contracts, even if individual parts appear simple.
- Do not combine approval steps of `01-web-brainstorm` and `02-web-plan` into one if both are mandatory — each requires separate confirmation before proceeding.
- Do not proceed past `01-web-brainstorm` before the user reviews, supplements (if needed), and approves the summary, and `docs/specs/spec-<name>.md` is saved.
- Do not proceed past `02-web-plan` to TDD execution before the user reviews, supplements (if needed), and explicitly approves `docs/plans/plan-<name>.md`.
- Do not guess the scenario when input signals are insufficient for classification (e.g., unclear whether it is a bug or new feature) — ask a brief clarifying question instead of guessing.
- Do not treat an `07-web-review` failure as pipeline completion or arbitrarily jump back to `03-web-implement`/`05-web-fix` outside the standard pipeline — must go through Phase 5 to select the appropriate 4a/4b/5/6 branch.
- Do not auto-loop Phase 5 indefinitely when the same issue fails repeatedly — stop on the 3rd recurrence and report to the user.
- Do not transition between critical skill boundaries without providing the structured YAML handoff block.
- Do not run any pipeline scenario (1–6) without creating the harness execution log in `docs/harness-logs/` before the first skill runs and appending each skill section after completion — the in-chat YAML handoff never replaces the log file.
- Do not create a second log file for the same task on Phase 5 re-routes — append to the existing one.

## Quality Checklist
- [ ] Has the domain gate run with a clear pass/reject conclusion before routing?
- [ ] Has the request been properly classified into 1 of the 3 groups (implementation / known bug / unknown bug)?
- [ ] Does the selected scenario match the 6-scenario table without arbitrary improvisation?
- [ ] Are the mandatory approval checkpoints respected (brainstorm summary approved + spec created; plan approved) before advancing?
- [ ] Are child skills invoked in the correct order, passing involved layers and necessary context?
- [ ] Are structured YAML handoff blocks populated when passing tasks between critical skill boundaries?
- [ ] If `07-web-review` fails, is re-routing to the proper 4a/4b/5/6 branch enforced (for all original scenarios, including 4/5/6) without skipping Phase 5?
- [ ] Is the new bug-fix branch chosen based on root cause/complexity from the `07-web-review` report itself, freshly re-evaluated rather than copying previous complexity?
- [ ] Was the harness execution log created in `docs/harness-logs/` before the first skill ran, with one section appended per completed skill and the pipeline summary appended at the end (per `references/execution-log.md`)?
