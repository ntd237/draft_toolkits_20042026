---
name: 05-mobile-game-fix
description: "Permanently resolves defects, crashes, memory leaks, performance hitches, and review findings in 2D/3D mobile games based on root cause analysis from 04-mobile-game-bugfinder or 07-mobile-game-review defect reports. Sole authorized Green + Refactor skill for all bug-fix pipelines (4a, 4b, 5, 6) and Post-Review Bug Loops. Strictly prohibits modifying tests to evade logic fixes and prohibits patching surface symptoms."
---

# 05-mobile-game-fix — Defect Remediation (Green + Refactor)

## Trigger
Invoked by `00-mobile-game-orchestrator` in defect resolution pipelines (Pipelines 4a, 4b, 5, 6) and during every iteration of the Post-Review Bug Loop. **Sole authorized skill for writing defect-fixing code — `03-mobile-game-implement` is strictly forbidden from executing bug fixes.**

## Workflow

### Phase 1: Root Cause Verification
**Objective**: Validate root cause clarity before modifying any production scripts or game assets.

1. **Verify Handoff Details**: Inspect the incoming YAML handoff from `04-mobile-game-bugfinder`, `00-mobile-game-orchestrator`, or `07-mobile-game-review`. Ensure the report contains:
   - Exact file path, line number, or asset identifier.
   - Root cause description (not merely surface symptoms).
   - Confirmation of probe cleanup (`cleanup_verified: true` if coming from `04-mobile-game-bugfinder`).
2. **Reject Insufficient Inputs**: If the input contains only vague symptoms (e.g., "game sometimes freezes on pause") without specific diagnostic evidence, decline to proceed and request routing to `04-mobile-game-bugfinder`. Do not guess.

### Phase 2: Green — Surgical Root Cause Remediation
**Objective**: Fix the root cause directly to transition targeted failing tests from Red to Green while adhering to mobile performance constraints.

1. **Surgical Fix**: Apply changes directly to the offending logic, memory structure, or component lifecycle.
2. **Zero-GC & Performance Compliance**:
   - Ensure the fix introduces zero heap allocations in per-frame tick loops (`Update`/`FixedUpdate`).
   - If fixing a memory leak, ensure all native textures, event subscriptions (`-=`), and Addressables/AssetBundles are explicitly released in `OnDestroy()` or `OnDisable()`.
   - If fixing an ANR or freeze, move synchronous file I/O or heavy computations to background tasks/coroutines with frame throttling.
3. **No Surface Masking**: Do not swallow exceptions with empty `catch` blocks or inject artificial null checks that leave game entities in undefined states. Fix the underlying initialization or state transition.
4. **Execute Tests**: Run the targeted regression test suite to verify Green status.

### Phase 3: Multi-Site Consistency & Regression Verification
**Objective**: Propagate fixes across all related locations and verify zero regressions.

1. **Impact Scope Propagation**: If the root cause pattern exists across multiple entities or weapons (e.g., unpooled instantiation replicated across several classes per `04-mobile-game-bugfinder`'s blast radius), apply identical, consistent fixes to all affected classes.
2. **Full Suite Regression Check**: Execute the entire related test suite to guarantee that fixing the defect did not break adjacent gameplay mechanics, save data integrity, or UI state.
3. **Handoff**: Transition to `07-mobile-game-review` (or to `06-mobile-game-test` under Scenario A if TDD was skipped).

## Output Format
Provide code diffs and a structured remediation summary:
- **Root Cause Addressed**: Script path and line number corrected.
- **Remediation Details**: Explanation of the fix and prevention of memory leaks/GC churn.
- **Multi-Site Updates**: List of additional files updated for consistency.
- **Verification Evidence**: Test runner output showing targeted and regression tests passing Green.

## Don'ts
- **Absolute Prohibition**: Do not alter, weaken, or delete test assertions to make tests pass — all fixes must be achieved by correcting production code.
- Do not apply surface patches (e.g., catching exceptions and doing nothing) that mask deeper game logic flaws.
- Do not guess or attempt fixes without a verified root cause from `04-mobile-game-bugfinder` or explicit diagnostic evidence.
- Do not introduce new heap allocations, LINQ queries, or boxing inside per-frame update methods.
- Do not leave event subscriptions dangling when objects are destroyed.

## Quality Checklist
- [ ] Is the fix targeted directly at the verified root cause rather than surface symptoms?
- [ ] Were zero test assertions modified to circumvent fixing production code?
- [ ] Does the fix introduce zero per-frame heap allocations or memory leaks?
- [ ] Were consistent fixes applied to all related locations identified in the blast radius?
- [ ] Did the targeted test transition to Green, and did the regression suite pass completely?
- [ ] Was `05-mobile-game-fix` used exclusively for this defect work (never `03-mobile-game-implement`)?
