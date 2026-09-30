---
name: 06-mobile-game-test
description: "Authors and executes tests for 2D/3D mobile games: decoupled unit tests, EditMode validation, and PlayMode engine integration tests, plus manual verification protocols for hardware-dependent behaviors. Resolves test placement by engine convention first (Unity UTF Assets/Tests, Godot GUT directory), then workspace tests/ priority. Runs in test-first Red mode before 03-mobile-game-implement/05-mobile-game-fix (default), or in post-code verification mode when TDD is skipped or inverted. Read-write for test files only; strictly prohibited from modifying production code."
---

# 06-mobile-game-test — Test Authoring & Verification

## Trigger
Invoked by `00-mobile-game-orchestrator` at the start of each TDD cycle to author failing Red tests (default), or after implementation/fixing when TDD is skipped or inverted (Scenario A: Bug Fix Confirmation, Scenario B: Post-Implementation Validation). Read-write strictly within test directories.

## Test Directory Location Policy
All generated test files must reside in a test directory resolved in this exact priority order:
1. **Engine & project convention wins when unambiguous**: if the project already has an established test layout, follow it exactly — e.g., Unity Test Framework requires test assemblies under `Assets/<...>/Tests/` (with asmdef) or `Packages/`; Godot GUT runs the directory configured in project settings/`.gutcfg`. Never place tests where the engine's runner cannot discover them.
2. `tests/` — Use if `tests/` already exists directly under the workspace root.
3. `test/` — Use if `tests/` does not exist, but `test/` already exists directly under the workspace root.
4. If no engine convention and neither exists, create `tests/` directly under the workspace root and place all generated test files there.

> **Rule**: Never scatter test files across arbitrary folders; when resolved to `tests/`/`test/`, they must be direct children of the workspace root.

## Mobile Game Test Typology
- **Pure Logic Unit Tests** (Fastest, High Coverage): Tests decoupled domain logic (combat formulas, inventory math, loot drop tables, stat modifiers, state machine transitions) in plain C#/GDScript without bootstrapping the game engine.
- **EditMode / Data Validation Tests**: Tests save data serialization/migration schemas, asset reference integrity, and ScriptableObject data validity.
- **PlayMode / Frame Simulation Tests**: Tests physics sub-stepping, coroutines, component lifecycle transitions, and object pool recycle cycles.
- **Device/On-Device Verification**: For hardware-dependent behaviors (thermal throttling, multi-touch, safe area on physical notch displays), author the Manual Verification Protocol checklist (steps, expected observations) — automated device farms (e.g., Unity Device Simulator, Appium) are used only when the project already has that infrastructure.

## Workflow

### Phase 1: Test Directory Resolution & Context Ingestion
**Objective**: Resolve the target test path and ingest behavior specifications.

1. Resolve the test directory per the **Test Directory Location Policy** (engine/project convention → `tests/` → `test/` → create `tests/`).
2. Ingest acceptance criteria from `01-mobile-game-brainstorm` / `02-mobile-game-plan`, or defect root causes from `04-mobile-game-bugfinder` / `07-mobile-game-review`.

### Phase 2: Red Phase — Test-First Authoring (Standard TDD Default)
**Objective**: Author failing tests that precisely specify the next required behavior or defect condition before production code exists.

1. **Author Targeted Test**:
   - For new features: translate acceptance criteria into clear assertions with concrete inputs and boundary cases.
   - For defects: write a reproduction test capturing the exact failure condition identified by `04-mobile-game-bugfinder`.
2. **Execute & Verify Red**: Run the test runner (e.g., `dotnet test`, Unity UTF batch mode, GUT CLI) to confirm the test fails for the expected semantic reason (missing method, unmet assertion) rather than compilation errors.
3. **Emit Red Handoff**: Structure the YAML handoff block containing test path, test name, run command, and expected failure.

### Phase 3: Verify Phase — Post-Code Verification (TDD Skipped or Inverted)
**Objective**: Author safety tests after code has been authored under approved skip or inverted TDD conditions.

1. **Scenario A (Bug Fix Confirmation)**: Author regression tests ensuring the bug cannot recur, verifying immediate Green status against current code.
2. **Scenario B (Post-Implementation Validation)**: Author behavior verification tests covering the implemented mechanic or inverted spike, confirming Green status.
3. Verify that assertions are substantive, testing true business behavior rather than tautologies.

### Phase 4: Full Suite Regression Verification
**Objective**: Guarantee that new tests and changes do not break existing test suites.

1. Run the entire project test suite across related subsystems.
2. Report any pre-existing test failures immediately as potential regressions.

## Output Format
- **For Red Phase**: Test file path + test method name + execution output showing expected failure + YAML handoff block:
```yaml
handoff:
  from_skill: "06-mobile-game-test"
  to_skill: "03-mobile-game-implement" # or "05-mobile-game-fix"
  tdd_mode: "active"
  target_files: ["Scripts/Combat/DamageCalculator.cs"]
  failing_test_file: "tests/Combat/DamageCalculatorTests.cs"
  failing_test_name: "CalculateDamage_CriticalHit_AppliesMultiplier"
  run_command: "dotnet test --filter CalculateDamage_CriticalHit_AppliesMultiplier"
  observed_failure: "Expected 200, received 100"
  next_behavior: "Apply critical multiplier when isCrit is true"
```
- **For Verify Phase**: Test file path + execution output (Green) + behavior coverage notes.

## Don'ts
- Do not create test files outside the directory resolved by the Test Directory Location Policy (engine/project convention / workspace-root `tests/` or `test/`) — in particular, never place tests where the engine's runner cannot discover them.
- Do not modify production code, shaders, or scene files — test scope only.
- Do not author tests that pass immediately in Phase 2 (Red) — tests must fail genuinely first.
- Do not write fake or tautological tests (e.g., `Assert.IsTrue(true)`, mocking away the logic under test).
- Do not skip Phase 4 (full suite verification).

## Quality Checklist
- [ ] Are test files located strictly within the directory resolved by the location policy?
- [ ] In Phase 2, was the test confirmed Red for the expected semantic failure?
- [ ] Do tests validate pure logic without unnecessary engine dependencies where possible?
- [ ] Are test assertions substantive, validating edge cases and boundary conditions?
- [ ] Was the full test suite executed to confirm zero regressions?
- [ ] Were zero production code files modified?
