---
name: 06-test
description: "Writes and runs tests for frontend (component/UI tests), backend (unit/integration/API tests), and database (query/transaction tests), including load testing for performance concerns. Triggers at the start of the TDD cycle to author Red tests before 03-implement/05-fix (default), or afterward for verification when TDD is inverted by exception. Read-write — creates/edits test files; prohibited from modifying implementation code."
---

# 06-test — Test-First (Red) & Verification

## Trigger
Invoked by `00-orchestrator` at the start of each TDD cycle (default: authoring Red tests first) based on acceptance criteria from `01-brainstorm`/`02-plan` or root causes from `04-bugfinder`. Also invoked after `03-implement`/`05-fix` when units qualify for TDD exceptions (implement first, test later).

## Workflow

### Phase 1: Red — Test Prior to Implementation
**Objective**: Author failing (Red) tests that accurately specify expected behavior or the targeted bug, prior to the existence of corresponding implementation/fix code.

1. For new features: translate acceptance criteria (from `01-brainstorm`/`02-plan`) into concrete test cases — select tier-appropriate test types (unit/component tests for frontend, unit/integration/API tests for backend, query/transaction tests for database).
2. For bug fixes: write tests reproducing the exact root cause identified by `04-bugfinder` — the test must fail against current code and pass once the bug is properly resolved.
3. Execute tests, confirming they are genuinely Red (failing) for the correct reason (missing implementation / existing bug) — not due to syntax errors or improper test setup.
4. Hand off the Red test suite along with explicit failure reasons to `03-implement`/`05-fix`.

### Phase 2: Verify — Verification Under Inverted TDD (Exceptions)
**Objective**: When implementation/fixing ran first (due to TDD exceptions), author verification tests post-hoc to ensure correct behavior and regression coverage.

1. Author tests reflecting the actual implemented/fixed behavior, ensuring tests are rigorous enough to detect future regressions — avoid superficial token tests.
2. Run tests and confirm immediate Green status against current code.

### Phase 3: Full Suite Verification
**Objective**: Ensure new tests do not break the existing test suite and vice versa.

1. Run the entire test suite associated with affected modules/tiers after adding new tests.
2. Report unexpected failures in pre-existing tests — these may indicate regressions requiring `04-bugfinder`/`05-fix`, rather than faults in new tests.

## Output Format
For Red: test cases + execution output (failing, with failure reasons) + corresponding acceptance criteria / root cause. For Verify: test cases + execution output (passing) + behavior coverage notes. Always include full suite verification results.

## Don'ts
- Do not write tests that pass immediately from the outset in Phase 1 (Red) — if a test passes before implementation exists, it fails to specify the target behavior properly.
- Do not edit implementation code to circumvent authoring proper tests — this skill's scope is strictly test files.
- Do not write fake or superficial tests (asserting always true, mocking away all actual logic) merely to achieve quick Green — this constitutes prohibited TDD cheating.
- Do not skip Phase 3 (full suite verification), even when adding only a single small test case.

## Quality Checklist
- [ ] In Phase 1, was the test confirmed Red for the correct reason (missing implementation / existing bug) rather than setup faults?
- [ ] Do test cases faithfully reflect acceptance criteria or root causes without superficial, tautological assertions?
- [ ] Was full suite verification executed and were all discovered regressions reported?
- [ ] Were zero implementation code files modified within the scope of this skill?
