---
name: 06-web-test
description: "Writes and runs tests for frontend (component/UI tests), backend (unit/integration/API tests), and database (query/transaction tests), plus E2E tests for critical user flows and load/Core Web Vitals checks when performance targets are acceptance criteria. Places test files following the project's existing test layout when established; otherwise tests/ or test/ under the workspace root (or the package, in monorepos) per the directory priority policy. Triggers at the start of the TDD cycle to author Red tests before 03-web-implement/05-web-fix (default), or afterward for verification when TDD is inverted by exception. Read-write — creates/edits test files; prohibited from modifying implementation code."
---

# 06-web-test — Test-First (Red) & Verification

## Trigger
Invoked by `00-web-orchestrator` at the start of each TDD cycle (default: authoring Red tests first) based on acceptance criteria from `01-web-brainstorm`/`02-web-plan` or root causes from `04-web-bugfinder`. Also invoked after `03-web-implement`/`05-web-fix` when units qualify for TDD exceptions (implement first, test later).

## Test Directory Location Policy
Generated test files must reside in a test directory determined by the following priority order:
1. **Project convention wins when unambiguous**: if the project already has an established test layout (existing `*.test.*`/`*.spec.*` files colocated with code, per-package test directories, or a test path configured in the test runner config), follow that layout exactly.
2. **Monorepo exception**: in a monorepo workspace (workspace globs in root `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, etc.), place tests inside the package under change — either following that package's existing convention or its direct `tests/` directory — never at the monorepo root.
3. Otherwise: `tests/` — use if `tests/` already exists directly under the workspace root.
4. Otherwise: `test/` — use if `test/` already exists directly under the workspace root.
5. If no convention, no monorepo structure, and neither `tests/` nor `test/` exists, create the `tests/` directory directly under the workspace root and place all generated test files there.

Never scatter generated test files across unrelated arbitrary directories; when a single change spans multiple monorepo packages, each package's tests go under that package.

## Workflow

### Phase 1: Red — Test Prior to Implementation
**Objective**: Author failing (Red) tests that accurately specify expected behavior or the targeted bug, prior to the existence of corresponding implementation/fix code.

1. Resolve the test directory per the **Test Directory Location Policy** (project convention → monorepo package → `tests/` → `test/` → create `tests/`).
2. For new features: translate acceptance criteria (from `01-web-brainstorm`/`02-web-plan`) into concrete test cases — select tier-appropriate test types (unit/component tests for frontend, unit/integration/API tests for backend, query/transaction tests for database).
3. For bug fixes: write tests reproducing the exact root cause identified by `04-web-bugfinder` — the test must fail against current code and pass once the bug is properly resolved.
4. Execute tests, confirming they are genuinely Red (failing) for the correct reason (missing implementation / existing bug) — not due to syntax errors or improper test setup.
5. Hand off the Red test suite along with explicit failure reasons to `03-web-implement`/`05-web-fix`.

### Phase 2: Verify — Verification Under Inverted TDD (Exceptions)
**Objective**: When implementation/fixing ran first (due to TDD exceptions), author verification tests post-hoc to ensure correct behavior and regression coverage.

1. Resolve the test directory per the **Test Directory Location Policy** (project convention → monorepo package → `tests/` → `test/` → create `tests/`).
2. Author tests reflecting the actual implemented/fixed behavior, ensuring tests are rigorous enough to detect future regressions — avoid superficial token tests.
3. Run tests and confirm immediate Green status against current code.

### Phase 3: Full Suite Verification
**Objective**: Ensure new tests do not break the existing test suite and vice versa.

1. Run the entire test suite associated with affected modules/tiers after adding new tests.
2. Report unexpected failures in pre-existing tests — these may indicate regressions requiring `04-web-bugfinder`/`05-web-fix`, rather than faults in new tests.

### Phase 4: E2E & Performance Verification (When Applicable)
**Objective**: Verify end-to-end user flows and measurable performance targets that unit/integration tests cannot cover. Run the sub-parts whose trigger applies; state explicitly "not applicable" for the rest.

1. **E2E tests**: mandatory when the change touches a critical user flow (auth/login, payments/checkout, onboarding, data-destroying actions) or a cross-tier contract visible to the user. Author E2E tests with the project's existing E2E framework (e.g., Playwright, Cypress); if none exists, introduce the project-idiomatic default and note the decision in the handoff. Cover the happy path plus the failure paths named in acceptance criteria. Guidance: `references/e2e-and-performance-testing.md`.
2. **Load/stress tests**: mandatory when an acceptance criterion states a load or response-time target (per `02-web-plan` Phase 2) — author a load test that exercises the target endpoint(s) at the specified profile and reports measured values against the target.
3. **Frontend performance checks**: mandatory for public-facing pages or when page-load targets are acceptance criteria — measure Core Web Vitals (LCP, INP, CLS) on the affected pages and report against the plan's targets.
4. Record all measured results in the handoff summary; failures against targets are reported to `00-web-orchestrator` as review-input findings, not silently omitted.

## Output Format
For Red: test cases + execution output (failing, with failure reasons) + corresponding acceptance criteria / root cause. Output the structured YAML handoff block for `03-web-implement` or `05-web-fix`:
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
For Verify: test cases + execution output (passing) + behavior coverage notes. Always include full suite verification results.

## Don'ts
- Do not create test files outside the location resolved by the Test Directory Location Policy (project convention / monorepo package / workspace-root `tests/` or `test/`).
- Do not create a new `test/` directory if `tests/` already exists, or create a new `tests/` directory if `test/` already exists.
- Do not write tests that pass immediately from the outset in Phase 1 (Red) — if a test passes before implementation exists, it fails to specify the target behavior properly.
- Do not edit implementation code to circumvent authoring proper tests — this skill's scope is strictly test files.
- Do not write fake or superficial tests (asserting always true, mocking away all actual logic) merely to achieve quick Green — this constitutes prohibited TDD cheating.
- Do not skip Phase 3 (full suite verification), even when adding only a single small test case.

## Quality Checklist
- [ ] Are generated test files placed per the location policy (project convention → monorepo package → `tests/` → `test/` → create `tests/`)?
- [ ] Where Phase 4 triggers applied (critical user flow, stated load/page-load targets, public-facing pages)? If not, was "not applicable" stated explicitly with the reason?
- [ ] In Phase 1, was the test confirmed Red for the correct reason (missing implementation / existing bug) rather than setup faults?
- [ ] Do test cases faithfully reflect acceptance criteria or root causes without superficial, tautological assertions?
- [ ] Is the structured YAML handoff block populated with failing test paths and exact run command?
- [ ] Was full suite verification executed and were all discovered regressions reported?
- [ ] Were zero implementation code files modified within the scope of this skill?
