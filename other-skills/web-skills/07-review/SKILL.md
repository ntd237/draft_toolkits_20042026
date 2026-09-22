---
name: 07-review
description: "Conducts final pipeline review covering logic, security, conventions, maintainability, cross-tier consistency (frontend-backend contracts, database schemas), and verifies that the TDD cycle was genuinely observed (no cheated tests). Triggers as the final step across all 6 pipeline scenarios after 03-implement/05-fix reaches Green and 06-test confirms. Read-only — reports issues only, does not modify code."
---

# 07-review — Final Pipeline Review & TDD Verification

## Trigger
Always the final step in every pipeline scenario (#1 through #6), invoked by `00-orchestrator` once implementation/fixing is Green and verified by tests.

## Workflow

### Phase 1: Code Quality Review & Severity Classification
**Objective**: Review logic, security, and conventions across each affected tier, classifying every finding by strict severity.

1. Backend: audit error handling, input validation, authorization/authentication, SQL injection / N+1 queries, resource leaks (unclosed connections).
2. Frontend: audit state management, memory leaks (uncleaned subscriptions/listeners), XSS, basic accessibility when UI is involved.
3. Database: audit migration safety (backward-compatible), appropriate indexing for new queries, sensible transaction boundaries.
4. Conventions: check alignment with existing project style/patterns (naming, directory structure, error handling patterns).
5. **Severity Classification Standard**:
   - **BLOCKING (Mandates FAIL)**:
     - Logic flaws, functional regressions, broken business workflows.
     - Security vulnerabilities (SQL injection, XSS, broken auth/authz, secrets leakage).
     - TDD compliance violations / cheating (tautological tests, mocks masking target logic, tests edited to force Green).
     - Cross-tier contract breakages (incompatible API payloads, unmigrated database queries).
   - **ADVISORY (Permits PASS)**:
     - Code style, naming conventions, formatting adjustments.
     - Non-critical micro-optimizations or clean-up suggestions.
     - Minor comment/documentation enhancements.

### Phase 2: Cross-Layer Consistency Check
**Objective**: Verify consistency across tiers whenever cross-layer changes occur.

1. If API changes occurred: verify frontend code matches the new contract (field names, types, nullability).
2. If DB schema changes occurred: verify backend queries/models are synchronized with no lingering references to old columns/tables.

### Phase 3: TDD Compliance Verification
**Objective**: Verify that the Red-Green-Refactor cycle was genuinely observed and detect any signs of TDD cheating.

1. Cross-reference test/execution history (if available: commit history, test run logs) to confirm Red tests existed prior to implementation, or for TDD exceptions, verify that post-hoc verification tests were added.
2. Audit test quality: verify assertions are substantive (not `assert true`, no mocks masking the logic under test), and cover expected behaviors / edge cases from acceptance criteria.
3. If cheating signals are detected (tests altered to pass instead of fixing logic, superficial tests) → classify as **BLOCKING** and mandate returning to `06-test`/`03-implement`/`05-fix` to re-execute the process properly; see `references/tdd-audit-signals.md`.

## Output Format
Review report containing: Categorized findings per tier with explicit severity tag (`[BLOCKING]` or `[ADVISORY]`) → Cross-tier consistency analysis → TDD compliance verification results → **Final Conclusion (PASS/FAIL)**:
- **FAIL**: Triggered if and only if **≥1 BLOCKING** issue exists. State each blocking issue with exact location (file/line/query/component) or symptom description. Include structured YAML handoff block for `00-orchestrator`:
```yaml
handoff:
  from_skill: "07-review"
  verdict: "FAIL"
  blocking_issues:
    - severity: "BLOCKING"
      layer: "backend"
      location: "src/api/payment.ts:115"
      root_cause: "Missing authorization check on refund endpoint"
      evidence: "Unauthenticated POST request returns 200 OK"
```
- **PASS**: Triggered when **0 BLOCKING** issues exist (even if `[ADVISORY]` recommendations are noted). Detail advisory improvements for future maintenance and conclude pipeline complete.

Avoid ambiguous terms such as "needs review" — always state an explicit PASS or FAIL.

## Don'ts
- Do not edit code to resolve detected issues — report only; fixing belongs to `03-implement`/`05-fix` via `00-orchestrator` re-routing.
- Do not conclude FAIL for minor stylistic or advisory suggestions — FAIL is reserved strictly for BLOCKING issues.
- Do not overlook BLOCKING issues or downgrade them to ADVISORY to force an unearned PASS.
- Do not skip Phase 3 (TDD compliance) regardless of time constraints — this is the final guardrail against TDD fraud across the entire pipeline.
- Do not inspect only the changed code while neglecting cross-tier consistency checks when APIs or schemas were touched.
- Do not issue ambiguous conclusions like "needs further review" — state PASS or FAIL decisively.

## Quality Checklist
- [ ] Were all affected tiers thoroughly reviewed without omitting any changed layers?
- [ ] If cross-tier changes occurred, was API contract and schema consistency verified?
- [ ] Was TDD compliance audited, including assertion quality beyond mere Green status?
- [ ] Are findings clearly categorized as `[BLOCKING]` vs `[ADVISORY]`?
- [ ] Is the FAIL verdict reserved strictly for BLOCKING issues, while ADVISORY findings permit a PASS?
- [ ] If FAIL, does the report include the structured YAML handoff block with exact locations to guide orchestrator re-routing?
