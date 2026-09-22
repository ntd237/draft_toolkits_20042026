---
name: 05-fix
description: "Permanently resolves defects across frontend/backend/database based on root causes identified by 04-bugfinder (or clearly known upfront with concrete evidence). Triggers in bug-fix scenarios (#4a, #4b, #5, #6) after root cause identification and Red tests exist (default), or before 06-test when TDD is infeasible. Read-write — modifies code; strictly prohibits modifying tests to circumvent fixing logic."
---

# 05-fix — Root-Cause Bug Fixing (Green + Refactor)

## Trigger
Invoked by `00-orchestrator` after a clear root cause is established — from `04-bugfinder` (Scenarios #4a/#4b) or from concrete evidence provided by the user upfront (Scenarios #5/#6). Must not trigger when root causes remain unknown without passing through `04-bugfinder`.

## Workflow

### Phase 1: Verify Root Cause Before Fixing
**Objective**: Confirm sufficient root cause specificity before modifying code, preventing misdirected fixes on symptoms.

1. Inspect received inputs: verify whether a specific root cause exists (exact file/line/query/config location) or merely a symptom description.
2. If only symptoms are provided without sufficient specificity to locate the fix → report back that returning to `04-bugfinder` is required; do not guess.

### Phase 2: Green — Fix to Pass
**Objective**: Fix directly at the root cause location so the targeted Red test (specifying the bug) transitions to Green.

1. Apply fixes directly to the identified root cause — do not modify unrelated code to "mask" symptoms.
2. Avoid introducing changes beyond what is required to resolve the targeted bug.
3. Re-run targeted tests to confirm Green, while executing related tests to ensure existing behavior remains intact.

### Phase 3: Refactor & Regression Check
**Objective**: Clean up code around the fix area as needed and ensure zero regressions.

1. If the root cause involves a pattern repeated across multiple locations (per impact scoping from `04-bugfinder`), apply consistent fixes across all affected sites, not just the first reported location.
2. Re-run the entire related test suite after refactoring.
3. If under a TDD exception (fix first, test later), hand off to `06-test` to author verification tests.

## Output Format
Code diff + summary: root cause fix location, implementation details, passing tests, consistent fixes applied to related locations (if any), and refactoring notes. If a specific root cause is lacking, halt and request returning to `04-bugfinder` rather than guessing.

## Don'ts
- Do not modify targeted test contents (Red tests specifying the defect) to make them pass instead of fixing the underlying logic — strictly prohibited.
- Do not fix based on speculation without a concrete root cause from `04-bugfinder` or clear upfront evidence.
- Do not merely patch surface symptoms (e.g., catching and swallowing exceptions) when the actual root cause lies deeper.
- Do not expand fix scope beyond the identified root cause, unless impact scoping explicitly identified related locations requiring consistent fixes.

## Quality Checklist
- [ ] Is the fix based on a concrete root cause location rather than symptom conjecture?
- [ ] Were zero tests modified to evade genuine logic fixes?
- [ ] Has the targeted test turned Green, and is the related test suite free of regressions?
- [ ] If the root cause followed a repeated pattern across multiple sites, were consistent fixes applied per impact scoping?
