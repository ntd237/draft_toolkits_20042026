---
name: 07-review
description: "Conducts final pipeline review covering logic, security, conventions, maintainability, cross-tier consistency (frontend-backend contracts, database schemas), and verifies that the TDD cycle was genuinely observed (no cheated tests). Triggers as the final step across all 6 pipeline scenarios after 03-implement/05-fix reaches Green and 06-test confirms. Read-only — reports issues only, does not modify code."
---

# 07-review — Final Pipeline Review & TDD Verification

## Trigger
Always the final step in every pipeline scenario (#1 through #6), invoked by `00-orchestrator` once implementation/fixing is Green and verified by tests.

## Workflow

### Phase 1: Code Quality Review
**Objective**: Review logic, security, and conventions across each affected tier.

1. Backend: audit error handling, input validation, authorization/authentication, SQL injection / N+1 queries, resource leaks (unclosed connections).
2. Frontend: audit state management, memory leaks (uncleaned subscriptions/listeners), XSS, basic accessibility when UI is involved.
3. Database: audit migration safety (backward-compatible), appropriate indexing for new queries, sensible transaction boundaries.
4. Conventions: check alignment with existing project style/patterns (naming, directory structure, error handling patterns).

### Phase 2: Cross-Layer Consistency Check
**Objective**: Verify consistency across tiers whenever cross-layer changes occur.

1. If API changes occurred: verify frontend code matches the new contract (field names, types, nullability).
2. If DB schema changes occurred: verify backend queries/models are synchronized with no lingering references to old columns/tables.

### Phase 3: TDD Compliance Verification
**Objective**: Verify that the Red-Green-Refactor cycle was genuinely observed and detect any signs of TDD cheating.

1. Cross-reference test/execution history (if available: commit history, test run logs) to confirm Red tests existed prior to implementation, or for TDD exceptions, verify that post-hoc verification tests were added.
2. Audit test quality: verify assertions are substantive (not `assert true`, no mocks masking the logic under test), and cover expected behaviors / edge cases from acceptance criteria.
3. If cheating signals are detected (tests altered to pass instead of fixing logic, superficial tests) → raise a critical flag and mandate returning to `06-test`/`03-implement`/`05-fix` to re-execute the process properly; see `references/tdd-audit-signals.md`.

## Output Format
Review report containing: Logic/security/convention findings per tier (severity: blocking / recommended / suggestion) → Cross-tier consistency issues (if any) → TDD compliance verification results (passed / suspicious signals, with details) → **Final Conclusion (PASS/FAIL)**:
- If any "blocking" issues exist (logic bugs, security vulnerabilities, TDD cheating) → conclude **FAIL**, providing for each blocking issue: the exact location (file/line/query/component) if clearly pinpointed during review, or symptom descriptions if not yet specific enough — this serves as mandatory input for `00-orchestrator` to select branches 4a/4b (unknown) or 5/6 (known).
- If no "blocking" issues exist (only optional recommendations/suggestions) → conclude **PASS**, marking the pipeline complete.
Avoid ambiguous terms such as "needs review" — always state an explicit PASS or FAIL.

## Don'ts
- Do not edit code to resolve detected issues — report only; fixing belongs to `03-implement`/`05-fix` via `00-orchestrator` re-routing.
- Do not skip Phase 3 (TDD compliance) regardless of time constraints — this is the final guardrail against TDD fraud across the entire pipeline.
- Do not inspect only the changed code while neglecting cross-tier consistency checks when APIs or schemas were touched.
- Do not issue a **PASS** when superficial/fake tests or any "blocking" issues are detected, even if all tests are currently Green.
- Do not issue ambiguous conclusions like "needs further review" — state PASS or FAIL decisively, and if FAIL, include exact locations or symptom descriptions sufficient for `00-orchestrator` to route to 4a/4b/5/6.

## Quality Checklist
- [ ] Were all affected tiers thoroughly reviewed without omitting any changed layers?
- [ ] If cross-tier changes occurred, was API contract and schema consistency verified?
- [ ] Was TDD compliance audited, including assertion quality beyond mere Green status?
- [ ] Is the final conclusion decisively PASS or FAIL without ambiguity?
- [ ] If FAIL, does every blocking issue include a specific location (if identified) or clear symptom description to enable orchestrator bug-fix routing?
