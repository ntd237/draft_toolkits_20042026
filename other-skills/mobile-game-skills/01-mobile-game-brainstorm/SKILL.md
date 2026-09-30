---
name: 01-mobile-game-brainstorm
description: "Clarifies ambiguous gameplay mechanics, touch control ergonomics, and analyzes mobile performance trade-offs (Draw Calls, zero-allocation GC per frame, CPU/GPU thermal limits) for 2D/3D mobile games before implementation. Enforces open write-in options on all questions, halts at a mandatory Review Gate for user approval, and saves the specification to docs/specs/spec-<name>.md in Vietnamese Markdown. Read-only on production code."
---

# 01-mobile-game-brainstorm — Gameplay Clarification & Mobile Trade-Offs

## Trigger
Invoked by `00-mobile-game-orchestrator` when gameplay mechanics, control schemes, or architectural designs are ambiguous (Pipeline 2), or prior to planning complex, multi-system features (Pipeline 3). Read-only on production code; creates only specification files in `docs/specs/`.

## Workflow

### Phase 1: Gameplay Discovery & Touch Input Ergonomics
**Objective**: Clarify undefined game mechanics, player controls, and mobile interaction rules.

1. **Gap Analysis**: Cross-examine the request against core game loops: player objectives, character stats/progression, game state transitions, and win/loss rules.
2. **Touch Control Ergonomics**: Clarify mobile-specific interaction vectors:
   - Control scheme: virtual joystick (fixed vs floating), directional swipes, touch-to-move, tap-to-aim.
   - Touch parameters: gesture swipe velocity thresholds, pinch-to-zoom limits, dead-zone radii, multi-touch simultaneous input handling.
   - Screen edge interference: handling system gestures (iOS home bar swipe up, Android navigation bar) near interactive UI elements.
3. **Mandatory Write-in Option**: For every question or set of options presented, **always include an open custom write-in option** enabling the user to specify their own preference (e.g., `[Custom] Tùy chỉnh theo yêu cầu riêng`).

### Phase 2: Mobile Performance & Architectural Trade-offs
**Objective**: Propose 2–3 viable design options balancing visual fidelity and mobile hardware constraints.

1. **Draw Calls & Batching**: Analyze rendering trade-offs:
   - Dynamic vs Static batching, GPU Instancing, SRP Batcher compatibility.
   - Sprite atlasing, Canvas separation (splitting dynamic HUD from static background UI to prevent full canvas mesh rebuilds).
2. **Memory & Zero-GC Policy**:
   - Evaluate pooling strategies (Generic `ObjectPool<T>` vs pre-warmed scene pools) vs dynamic instantiation.
   - Identify potential GC allocation traps (boxing, LINQ, lambda closures in tick loops).
3. **Hardware & Thermal Limits**:
   - Target framerate profile (30 FPS power-save, 60 FPS standard, 90/120 FPS high-refresh).
   - Thermal throttling mitigation on sustained mobile gameplay sessions.
4. **Recommendation**: Present options with explicit trade-offs and recommend 1 preferred approach, allowing user customization.

### Phase 3: Acceptance Criteria & TDD Boundary Formulation
**Objective**: Formulate concrete, testable behaviors for subsequent skills.

1. Draft acceptance criteria in structured Given/When/Then format or explicit rule checklists.
2. Clearly categorize criteria into:
   - **Deterministic Logic**: Combat math, state transitions, cooldowns, score systems (strictly standard TDD test-first).
   - **Inverted TDD Candidates**: Visual juice, camera shake curves, particle bursts, feel tuning (flagged for Inverted TDD per `references/tdd-exception-and-skip.md`).
3. **Non-Functional Criteria Sweep**: Before finalizing, screen the feature against the dimensions relevant to its scope and add explicit criteria for each that applies (mark N/A for those that do not, so the omission is a decision rather than an oversight):
   - **Security & integrity**: IAP/entitlement flows, save data protection, economy/leaderboard trust boundaries (audit standard: `../07-mobile-game-review/references/game-security-checklist.md`).
   - **Monetization & live ops**: sandbox/test product IDs, receipt validation flow, remote config/feature-flag exposure for the new content.
   - **Analytics & observability**: events to track for the feature, crash-reporting coverage for new subsystems.
   - **Localization**: player-facing strings routed through the localization system.
   - **Game accessibility**: color-independent feedback, text legibility, input alternatives.
   - **Audio**: new sources routed through mixer buses, lifecycle mute behavior.

### Phase 4: Mandatory Review Gate & Spec Generation
**Objective**: Present findings, pause for user review, and generate the final specification.

1. **Mandatory Summary & Pause**: Present a complete summary of clarified mechanics, control choices, performance constraints, and acceptance criteria in chat. **Strictly pause and await explicit user review, additions, and approval.**
2. If the user provides feedback or adjustments, update the proposal and re-confirm.
3. **Artifact Generation**: Only after explicit approval, save the finalized specification to `docs/specs/spec-<name>.md` (where `<name>` is a descriptive kebab-case identifier, e.g., `spec-combat-combo.md`).
4. **The entire content of `docs/specs/spec-<name>.md` must be written in Vietnamese using standard Markdown.**

## Output Format
1. **Interactive Questions**: Focused questions with explicit open write-in options.
2. **Review Gate Block**:
   - Tóm tắt cơ chế gameplay & sơ đồ điều khiển cảm ứng đã làm rõ.
   - Phân tích đánh đổi hiệu năng (Draw Calls, GC per frame, giới hạn nhiệt/pin).
   - Danh sách Acceptance Criteria chi tiết.
   - Đánh dấu các unit áp dụng ngoại lệ TDD / Inverted TDD (nếu có).
   - **Yêu cầu dừng bắt buộc**: Chờ người dùng xác nhận và bổ sung trước khi lưu file spec.
3. **Artifact Generation**: Clickable link to `docs/specs/spec-<name>.md` in Vietnamese Markdown once approved.

## Don'ts
- Do not present questions without providing an open write-in option for user custom input.
- Do not create `docs/specs/spec-<name>.md` or advance to subsequent skills before receiving explicit user approval.
- Do not write the spec artifact in any language other than Vietnamese Markdown.
- Do not modify, create, or delete production code, assets, or shaders.
- Do not ignore mobile constraints (Draw Calls, GC heap allocations, touch dead zones) during design analysis.

## Quality Checklist
- [ ] Did every question include an open custom write-in option?
- [ ] Were mobile touch ergonomics (swipes, virtual stick, dead zones) explicitly clarified?
- [ ] Were mobile performance factors (Draw Calls, GC allocations, thermal limits) evaluated?
- [ ] Was the non-functional criteria sweep performed (security / monetization & live ops / analytics / localization / accessibility / audio), with non-applicable dimensions explicitly marked N/A?
- [ ] Did execution halt at the Review Gate for explicit user review and approval?
- [ ] Is `docs/specs/spec-<name>.md` authored in Vietnamese Markdown after approval?
- [ ] Were zero production code files modified?
