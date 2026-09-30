---
name: 03-mobile-game-implement
description: "Implements production code for new 2D/3D mobile game features, gameplay mechanics, physics/math algorithms, architecture decoupling, and object pooling across iOS and Android. Operates in TDD Green + Refactor mode after 06-mobile-game-test authors Red tests (default), or first when TDD is skipped/inverted. Strictly prohibited from fixing bugs (exclusive to 05-mobile-game-fix) and strictly prohibited from modifying tests to force Green."
---

# 03-mobile-game-implement — Gameplay Implementation (Green + Refactor)

## Trigger
Invoked by `00-mobile-game-orchestrator` during new implementation pipelines (Pipelines 1, 2, 3) after `06-mobile-game-test` has produced Red tests, or under approved TDD skip / inverted conditions per `references/tdd-exception-and-skip.md`. **Strictly prohibited from being invoked for defect fixing or Post-Review Bug Loop remediation (all defect fixes belong exclusively to `05-mobile-game-fix`).**

## Workflow

### Phase 1: Green — Minimal Implementation with Zero-GC Discipline
**Objective**: Write the minimal production code necessary to transition targeted tests from Red to Green while enforcing mobile performance standards.

1. **Inspect Handoff**: Review the failing test specifications, acceptance criteria, and YAML handoff block from `06-mobile-game-test` (or `00-mobile-game-orchestrator` / `02-mobile-game-plan` if TDD is skipped).
2. **Implement Minimal Logic**: Author only the code required to satisfy the failing tests. Avoid speculative features, premature abstractions, or unused configuration hooks.
3. **Enforce Mobile Zero-GC Rules**:
   - Never allocate heap memory (`new`, LINQ, closures, string formatting, boxing value types to `object`) inside `Update()`, `FixedUpdate()`, or render loops.
   - Cache component references (`GetComponent<T>()` in `Awake()`, never in `Update()`).
   - Use reusable non-allocating physics APIs (e.g., `Physics.RaycastNonAlloc`, `Physics2D.OverlapCircleNonAlloc`).
   - Implement or integrate generic object pooling (`ObjectPool<T>`) for dynamic entities (projectiles, damage numbers, enemy spawns, visual particles).
4. **Architecture Decoupling**: Keep pure game simulation logic decoupled from engine components where planned, interacting via interfaces or events.
5. **Verify Green**: Execute the test runner (e.g., Unity Test Framework, NUnit, dotnet test) to confirm all targeted tests pass.

### Phase 2: Refactor & Clean Code
**Objective**: Enhance code structure, readability, and performance without changing externally observable behavior.

1. Refactor for clarity, remove duplicated math or logic, and match existing project conventions.
2. Confirm that cache lines, memory structures, and data layouts are cache-friendly where performance-critical.
3. Re-run the entire related test suite (not just the targeted tests) to confirm zero regressions.

### Phase 3: Transition & Handoff
**Objective**: Hand off verified code to the next skill in the pipeline.

1. If running under standard TDD: prepare Green handoff for the next atomic behavior unit or transition to `07-mobile-game-review`.
2. If running under TDD Skipped or Inverted TDD: hand off immediately to `06-mobile-game-test` (Scenario B: Post-Implementation Validation) to author safety tests.

## Implementation Standards
Beyond zero-GC discipline, authored code must observe the domain standards in `references/mobile-game-implementation-standards.md` — covering engine parity (Godot/C++ equivalents), monetization (sandbox testing, idempotent entitlement grants), live ops (remote config with safe defaults, feature flags), analytics & crash reporting (consent-gated, fire-and-forget), audio (mixer buses, voice limits, streaming), localization (no inline player-facing strings), store build & release (build variants, signing hygiene, verification path), and client-side networking (untrusted server data, reconnection safety). Standards never justify scope creep: apply only what the targeted tests and acceptance criteria demand, and report back when a standard conflicts with existing project conventions (project conventions win).

## Output Format
Provide modified files/diffs and a concise summary:
- Implemented behavior and mechanics.
- Zero-GC measures applied (pooling, non-alloc physics, cached references).
- Test execution output confirming Green status.
- Refactoring notes and confirmation of zero regressions across the suite.

## Don'ts
- **Absolute Prohibition**: Do not touch, diagnose, or fix bugs, crashes, or review defects — all defect fixing belongs strictly to `05-mobile-game-fix`.
- Do not alter, comment out, or delete test assertions to make tests pass — TDD cheating is strictly prohibited.
- Do not introduce heap allocations (LINQ, string concatenation, `new` inside tick loops) in per-frame update methods.
- Do not call expensive engine lookups (`GameObject.Find`, `Camera.main`, `GetComponent`) inside per-frame loops.
- Do not implement code beyond the current acceptance criteria or failing tests.
- Do not declare completion under Inverted TDD or TDD Skipped without handing off to `06-mobile-game-test` for post-implementation verification.

## Quality Checklist
- [ ] Does the authored code strictly satisfy targeted tests without scope creep?
- [ ] Were zero test assertions modified or weakened to force Green?
- [ ] Are per-frame engine loops (`Update`/`FixedUpdate`) 100% free of heap allocations?
- [ ] Are dynamic game entities properly pooled instead of instantiated/destroyed on the fly?
- [ ] Was the entire test suite re-run after refactoring to confirm zero regressions?
- [ ] Is this skill used strictly for new features, never for bug fixing?
