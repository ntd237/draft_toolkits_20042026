---
name: 07-mobile-game-review
description: "Performs comprehensive architectural, performance, security, and non-functional code reviews for 2D/3D mobile games across iOS and Android. Audits per-frame GC allocations, Draw Call batching, GPU overdraw, safe area compliance, mobile lifecycle handling, game security & integrity (IAP receipt validation, save tampering, client trust boundary) for security-sensitive changes, flagged non-functional dimensions (audio/localization/accessibility), and verifies genuine TDD compliance without cheated tests. Issues strict PASS/FAIL verdicts, triggering the Post-Review Bug Loop on FAIL. Read-only — reports findings without modifying code."
---

# 07-mobile-game-review — Code & Architecture Review

## Trigger
Mandatory final step across all 6 pipeline scenarios (#1 through #6), invoked by `00-mobile-game-orchestrator` once `03-mobile-game-implement` or `05-mobile-game-fix` achieves Green and tests are verified. Read-only on production code and test files.

## Workflow

### Phase 1: Mobile Performance & Memory Audit
**Objective**: Audit code changes against mobile hardware constraints and zero-GC per-frame discipline per `references/mobile-audit-signals.md`.

1. **GC Allocations in Tick Loops**:
   - Inspect all methods running per frame (`Update`, `FixedUpdate`, `LateUpdate`, render ticks).
   - Check for hidden allocations: LINQ operations, string formatting/concatenation, boxing of value types, closures capturing variables, dynamic array/list creation.
   - Verify that physics queries use non-allocating variants (`RaycastNonAlloc`).
   - Flag any per-frame heap allocation as `[BLOCKING]`.
2. **Memory Leaks & Object Lifecycle**:
   - Confirm dynamic objects are managed via object pools rather than repeated `Instantiate`/`Destroy`.
   - Verify all static event delegates, Addressable handles, and native textures are properly unsubscribed/released in `OnDisable()` or `OnDestroy()`.

### Phase 2: Rendering, Batching & Mobile GPU Audit
**Objective**: Ensure changes maintain high batching rates and avoid GPU fill-rate exhaustion.

1. **Draw Call Batching**:
   - Verify scripts do not access `renderer.material` directly (which creates a clone and breaks batching); ensure `MaterialPropertyBlock` or `sharedMaterial` is used.
2. **UI Canvas Architecture**:
   - Ensure dynamic/animated UI elements are separated into nested Sub-Canvases so frequent updates do not dirty the main Canvas geometry.
3. **GPU Shaders & Overdraw**:
   - Audit shader arithmetic complexity on mobile tile-based GPUs; check for excessive transparent quad overlap.

### Phase 3: Cross-Platform (iOS & Android) & Lifecycle Audit
**Objective**: Verify device ergonomics and platform runtime parity.

1. **Safe Area Notch & Cutout Handling**:
   - Check that UI layouts dynamically adjust anchors to `Screen.safeArea` rather than hardcoding screen borders.
2. **Mobile App Lifecycle**:
   - Verify proper handling of `OnApplicationPause(true)` and focus loss (muting game audio, pausing timers, handling network reconnection).
3. **Platform Macro Parity**:
   - Ensure `#if UNITY_IOS` and `#if UNITY_ANDROID` blocks do not desynchronize pure game simulation logic.

### Phase 4: Game Security & Non-Functional Audit
**Objective**: Audit security-sensitive game code as an untrusted client environment, and verify flagged non-functional dimensions.

1. **Security & Integrity**: when the change touches IAP/purchases, save data, currency/economy, player identity, or leaderboards, run the full audit in `references/game-security-checklist.md` (server-side receipt validation, save integrity, client trust boundary, secrets in build, consent before identity transmission). Confirmed integrity-critical flaws are `[BLOCKING]`.
2. **Non-Functional Checks**: when the acceptance criteria or plan flagged the dimension (per `01-mobile-game-brainstorm` Phase 3 / `02-mobile-game-plan` Phase 2), verify audio (lifecycle, mixing, voice limits), localization (no hardcoded player-facing strings), and game accessibility using `references/non-functional-checklists.md`. A violation of a *stated* acceptance criterion is `[BLOCKING]`; gaps in dimensions never agreed on are `[ADVISORY]`.

### Phase 5: TDD Compliance & Test Integrity Audit
**Objective**: Detect TDD cheating and verify test substantive value.

1. **TDD Cheating Detection**:
   - Audit test files for meaningless assertions (`Assert.IsTrue(true)`, comparing identical values).
   - Confirm tests do not mock away the core class under test.
   - Cross-check git history/diffs to ensure test assertions were not altered to force Green.
2. **Post-Code Verification (TDD Skipped/Inverted)**:
   - If TDD was skipped or inverted, verify that rigorous verification tests were added by `06-mobile-game-test`.
3. **Severity Tagging**:
   - Any TDD cheating or missing post-code verification is classified as `[BLOCKING]`.

### Phase 6: Verdict Determination & Post-Review Bug Loop Handoff
**Objective**: Issue a decisive PASS or FAIL verdict.

- **PASS**: Granted if and only if **0 `[BLOCKING]` issues exist** (even if `[ADVISORY]` recommendations are present).
- **FAIL**: Mandated if **≥1 `[BLOCKING]` issue exists**. Formulate the structured Review Defect Handoff block to trigger the Post-Review Bug Loop in `00-mobile-game-orchestrator`:
```yaml
handoff:
  from_skill: "07-mobile-game-review"
  to_skill: "00-mobile-game-orchestrator"
  verdict: "FAIL"
  re_entry_pipeline: 5 # 4a | 4b | 5 | 6
  blocking_issues:
    - severity: "BLOCKING"
      subsystem: "Memory / Performance"
      location: "Scripts/Combat/CombatFeedback.cs:34"
      root_cause: "String concatenation inside Update() causes 1.8KB/frame heap allocation"
      evidence: "textMesh.text = $"Combo: {comboCount}"; inside per-frame tick"
```

## Output Format
Review report structured as:
- **Mobile Performance & GC Audit**: Findings categorized as `[BLOCKING]` or `[ADVISORY]`.
- **Rendering & UI Batching Audit**: Batching integrity and Sub-Canvas separation.
- **Cross-Platform & Safe Area Audit**: iOS/Android parity and notch fitting.
- **Security & Non-Functional Audit**: Integrity findings (per `references/game-security-checklist.md` when security-sensitive code changed) and flagged non-functional dimensions.
- **TDD Compliance Audit**: Verification of genuine Red-Green-Refactor cycles.
- **Final Verdict**: Explicit **PASS** or **FAIL** with YAML handoff block if FAIL.

## Don'ts
- Do not modify, patch, or refactor code within this skill — read-only; all fixes belong to `05-mobile-game-fix`.
- Do not issue an ambiguous verdict like "conditionally approved" — state PASS or FAIL decisively.
- Do not downgrade `[BLOCKING]` issues (GC in Update, native crash, broken batching, TDD cheating) to `[ADVISORY]`.
- Do not skip auditing per-frame tick loops for hidden allocations.
- Do not ignore iOS/Android platform parity and safe-area notch compliance.

## Quality Checklist
- [ ] Were all methods running in per-frame tick loops inspected for heap allocations?
- [ ] Was Draw Call batching verified (no `renderer.material` cloning, Sub-Canvas usage)?
- [ ] Were Safe Area and mobile pause/resume lifecycles audited?
- [ ] When security-sensitive game code changed (IAP, save, economy, identity), was the full audit from `references/game-security-checklist.md` executed rather than skipped?
- [ ] Where flagged non-functional dimensions (audio/localization/accessibility) applied, were they verified per `references/non-functional-checklists.md` — or explicitly reported as not applicable?
- [ ] Was TDD compliance verified and checked for cheating signals?
- [ ] Are findings strictly tagged with `[BLOCKING]` or `[ADVISORY]`?
- [ ] If ≥1 `[BLOCKING]` issue exists, is FAIL issued with the YAML handoff block?
- [ ] Were zero code files modified within this review skill?
