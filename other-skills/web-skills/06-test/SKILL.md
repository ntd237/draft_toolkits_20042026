---
name: 06-test
description: "Writes and runs tests for frontend (component/UI tests), backend (unit/integration/API tests), and database (query/transaction tests), including load testing for performance concerns. Places all generated test files in workspace-level tests/ or test/ per strict directory priority. Triggers at the start of the TDD cycle to author Red tests before 03-implement/05-fix (default), or afterward for verification when TDD is inverted by exception. Read-write — creates/edits test files; prohibited from modifying implementation code."
---

# 06-test — Test-First (Red) & Verification

## Trigger
Invoked by `00-orchestrator` at the start of each TDD cycle (default: authoring Red tests first) based on acceptance criteria from `01-brainstorm`/`02-plan` or root causes from `04-bugfinder`. Also invoked after `03-implement`/`05-fix` when units qualify for TDD exceptions (implement first, test later).

## Test Directory Location Policy
Generated test files must strictly reside in a test directory that is a direct child of the workspace root, determined by the following priority order:
1. `tests/` — Use if `tests/` already exists directly under the workspace root.
2. `test/` — Use if `tests/` does not exist, but `test/` already exists directly under the workspace root.
3. If neither `tests/` nor `test/` exists, create the `tests/` directory directly under the workspace root and place all generated test files there.

Both `tests/` and `test/` must always be direct child directories of the workspace root (e.g., `<workspace_root>/tests/` or `<workspace_root>/test/`). Never scatter generated test files across unrelated arbitrary directories.

## Workflow

### Phase 1: Red — Test Prior to Implementation
**Objective**: Author failing (Red) tests that accurately specify expected behavior or the targeted bug, prior to the existence of corresponding implementation/fix code.

1. Resolve the test directory per the **Test Directory Location Policy** (`tests/` if exists → `test/` if exists → create `tests/` directly under workspace root).
2. For new features: translate acceptance criteria (from `01-brainstorm`/`02-plan`) into concrete test cases — select tier-appropriate test types (unit/component tests for frontend, unit/integration/API tests for backend, query/transaction tests for database).
3. For bug fixes: write tests reproducing the exact root cause identified by `04-bugfinder` — the test must fail against current code and pass once the bug is properly resolved.
4. Execute tests, confirming they are genuinely Red (failing) for the correct reason (missing implementation / existing bug) — not due to syntax errors or improper test setup.
5. Hand off the Red test suite along with explicit failure reasons to `03-implement`/`05-fix`.

### Phase 2: Verify — Verification Under Inverted TDD (Exceptions)
**Objective**: When implementation/fixing ran first (due to TDD exceptions), author verification tests post-hoc to ensure correct behavior and regression coverage.

1. Resolve the test directory per the **Test Directory Location Policy** (`tests/` if exists → `test/` if exists → create `tests/` directly under workspace root).
2. Author tests reflecting the actual implemented/fixed behavior, ensuring tests are rigorous enough to detect future regressions — avoid superficial token tests.
3. Run tests and confirm immediate Green status against current code.

### Phase 3: Full Suite Verification
**Objective**: Ensure new tests do not break the existing test suite and vice versa.

1. Run the entire test suite associated with affected modules/tiers after adding new tests.
2. Report unexpected failures in pre-existing tests — these may indicate regressions requiring `04-bugfinder`/`05-fix`, rather than faults in new tests.

## Output Format
For Red: test cases + execution output (failing, with failure reasons) + corresponding acceptance criteria / root cause. Output the structured YAML handoff block for `03-implement` or `05-fix`:
```yaml
handoff:
  from_skill: "06-test"
  to_skill: "03-implement" # or "05-fix"
  target_files: ["src/services/auth.ts"]
  failing_test_file: "tests/services/auth.test.ts"
  failing_test_name: "should return 401 when token expired"
  run_command: "npm test -- tests/services/auth.test.ts"
  observed_failure: "Expected 401, received 500"
  next_behavior: "Return 401 Unauthorized instead of throwing unhandled exception"
```
For Verify: test cases + execution output (passing) + behavior coverage notes. Always include full suite verification results.

## Don'ts
- Do not create test files outside the designated direct workspace test directory (`tests/` or `test/`).
- Do not create a new `test/` directory if `tests/` already exists, or create a new `tests/` directory if `test/` already exists.
- Do not write tests that pass immediately from the outset in Phase 1 (Red) — if a test passes before implementation exists, it fails to specify the target behavior properly.
- Do not edit implementation code to circumvent authoring proper tests — this skill's scope is strictly test files.
- Do not write fake or superficial tests (asserting always true, mocking away all actual logic) merely to achieve quick Green — this constitutes prohibited TDD cheating.
- Do not skip Phase 3 (full suite verification), even when adding only a single small test case.

## Quality Checklist
- [ ] Are generated test files placed in the correct directory per the location policy (`tests/` if exists → `test/` if exists → create `tests/` directly under workspace root)?
- [ ] Is the designated test folder (`tests/` or `test/`) a direct child directory of the workspace root?
- [ ] In Phase 1, was the test confirmed Red for the correct reason (missing implementation / existing bug) rather than setup faults?
- [ ] Do test cases faithfully reflect acceptance criteria or root causes without superficial, tautological assertions?
- [ ] Is the structured YAML handoff block populated with failing test paths and exact run command?
- [ ] Was full suite verification executed and were all discovered regressions reported?
- [ ] Were zero implementation code files modified within the scope of this skill?
