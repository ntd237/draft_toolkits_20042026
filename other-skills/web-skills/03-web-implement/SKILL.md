---
name: 03-web-implement
description: "Implements code for new features across frontend/backend/database based on established acceptance criteria or plans. Triggers when 00-web-orchestrator routes an implementation (Scenarios #1, #2, #3) after 06-web-test has created Red tests (default), or before 06-web-test when TDD is infeasible for that unit (spikes/exploratory UI, under orchestrator-approved exceptions). Read-write — creates/edits code files; strictly prohibited from modifying target tests to force them to pass."
---

# 03-web-implement — Code Implementation (Green + Refactor)

## Trigger
Invoked by `00-web-orchestrator` in implementation scenarios, typically right after `06-web-test` has produced Red tests. If a unit qualifies for a TDD exception (see `../00-web-orchestrator/references/tdd-exception-handling.md`), it may run prior to `06-web-test`.

## Workflow

### Phase 1: Green — Minimal Implementation
**Objective**: Write strictly the minimal code needed to transition targeted tests from Red to Green.

1. Thoroughly inspect the handed-off Red tests and structured YAML handoff block (target files, failing test file/name, run command, expected behavior).
2. Implement only enough to pass those tests — do not add extra features, endpoints, fields, or optimizations outside the targeted test scope.
3. If missing tests for a critical behavior are discovered during coding, do not silently expand scope — report back so `06-web-test` can add tests first.
4. Re-run the entire related test suite and verify Green.

### Phase 2: Refactor
**Objective**: Improve code quality after achieving Green without breaking passing tests.

1. Refactor for clarity, eliminate duplication, and adhere to project conventions — without altering externally observable behavior.
2. After each refactoring change, re-run the entire test suite (not just the targeted tests) to confirm zero regressions.
3. If the unit falls under a TDD exception (implement first, test later): upon finishing implementation, hand off to `06-web-test` to write verification tests — never consider this step complete without tests.

## Tier Implementation Standards
Regardless of TDD order, authored code must observe the tier-appropriate standards in `references/web-implementation-standards.md` — covering frontend (component structure, styling, responsive behavior, semantic HTML/accessibility in code), backend (input validation at the boundary, error handling, authorization checks), API design (REST conventions, versioning), database access (parameterized queries, transaction boundaries), observability (structured logging, error tracking), and app-level deployment config (env vars, build config). Standards never justify scope creep: apply only what the targeted tests and acceptance criteria demand, and report back when a standard conflicts with existing project conventions (project conventions win).

## Output Format
Complete code diff/files + summary: implemented behavior, passing tests, notable refactoring, any identified additional testing needs. If under a TDD exception, state the rationale and hand off to `06-web-test`.

## Don'ts
- Do not modify target test assertions or expectations to make them pass instead of fixing implementation logic — TDD "cheating" is strictly prohibited.
- Do not implement redundant code outside current acceptance criteria/tests, even if "convenient to do now".
- Do not skip re-running the entire test suite after refactoring.
- Do not unilaterally decide a unit qualifies for a TDD exception without prior confirmation from `00-web-orchestrator`/`01-web-brainstorm`.

## Quality Checklist
- [ ] Does the authored code strictly satisfy targeted tests without scope creep?
- [ ] Were zero tests modified to force Green?
- [ ] After refactoring, was the entire related test suite re-run and verified Green?
- [ ] If under a TDD exception (implement first), has it been handed off to `06-web-test`?
