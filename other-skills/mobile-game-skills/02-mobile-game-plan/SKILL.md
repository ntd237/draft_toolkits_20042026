---
name: 02-mobile-game-plan
description: "Produces execution-ready implementation and risk mitigation plans for complex, multi-system, or cross-platform mobile game features and architectural defects (iOS & Android). Decouples pure simulation logic from engine lifecycles, plans platform and save-migration risks, partitions work into parallel TDD waves, and halts at a mandatory Plan Approval Gate before execution. Saves plan to docs/plans/plan-<name>.md in Vietnamese Markdown. Read-only on production code."
---

# 02-mobile-game-plan — Mobile Architecture & Wave Planning

## Trigger
Invoked by `00-mobile-game-orchestrator` for complex features (Pipeline 3), complex unknown-cause bug investigations (Pipeline 4b), or complex known defects (Pipeline 6). Receives input from `01-mobile-game-brainstorm` (specification in `docs/specs/spec-<name>.md`) or `04-mobile-game-bugfinder` (defect diagnosis). Read-only on production code; writes plans exclusively to `docs/plans/`.

## Workflow

### Phase 1: Architectural Decoupling & Unit Decomposition
**Objective**: Break down requirements into atomic, independently testable units by decoupling pure logic from the game engine lifecycle.

1. **Architecture Decoupling**: Isolate pure simulation logic (combat algorithms, status effects, inventory, economy math) from engine-specific classes (`MonoBehaviour`, `Node`, scene graphs). Pure logic runs in plain C# or engine-agnostic classes, enabling rapid execution in isolated test runners without bootstrapping the full engine.
2. **Decomposition**: Partition work into atomic units covering:
   - *Core Simulation Tier*: Pure logic classes, domain interfaces, state machines.
   - *Engine Adapter Tier*: Component wrappers, input adapters, object pools, audio triggers.
   - *Presentation & UI Tier*: HUD views, animations, safe-area layout fitters.
3. **Dependency Mapping**: Establish prerequisite links between units to determine which can run in parallel versus those requiring sequential ordering.

### Phase 2: Cross-Platform Risk & Migration Planning
**Objective**: Identify and mitigate mobile hardware and platform runtime risks.

1. **Platform Divergence (iOS vs Android)**:
   - iOS: Metal graphics API, Apple Silicon alignment, App Tracking Transparency (ATT), Apple Sign-In.
   - Android: Vulkan/OpenGL ES fallbacks, Gradle build configs, target API levels, Android back-button handling, memory trim events (`TrimMemory`).
2. **Device Ergonomics & Aspect Ratios**:
   - Safe Area constraints (notches, dynamic islands, camera cutouts) on portrait and landscape orientations.
   - Extreme aspect ratios (e.g., 19.5:9, 21:9 ultra-wide, foldable unfolding events).
3. **Save Data Schema & State Migration**:
   - If player save data or game state changes: define backward-compatible serialization schemas (versioned JSON/Protobuf/Binary) and migration functions with rollback protection.
4. **App Lifecycle Transitions**:
   - Handling `OnApplicationPause`, app backgrounding, focus loss, and interruption recovery (phone calls, system alerts).

### Phase 3: Wave Sequencing & Plan Artifact Generation
**Objective**: Group units into executable waves and generate the comprehensive plan artifact.

1. **Wave Ordering**: Group independent units into concurrent waves (Wave 1: Pure Core Logic → Wave 2: Engine Integration & Pooling → Wave 3: UI & Platform Adapters).
2. **TDD Mode Assignment**: Tag each unit as standard TDD (`tdd_mode: "active"`), skipped (`tdd_mode: "skipped"` with reason), or Inverted TDD (`inverted_tdd: true` for feel/juice).
3. **Artifact Generation**: Save the complete plan document to `docs/plans/plan-<name>.md` (e.g., `docs/plans/plan-inventory-system.md`).
4. **Language Protocol**: The entire content of `docs/plans/plan-<name>.md` must be written in **Vietnamese Markdown**.

### Phase 4: Mandatory Plan Review & Approval Gate
**Objective**: Present the plan to the user and halt until explicit confirmation is granted.

1. Present a concise plan summary and a clickable link to `docs/plans/plan-<name>.md` in chat.
2. **Mandatory User Approval Gate**: Strictly pause execution. **Do not advance to TDD waves, test authoring (`06-mobile-game-test`), or code implementation without explicit user review and approval.**
3. If the user requests adjustments or scope changes, update `docs/plans/plan-<name>.md` and re-confirm.

## Output Format
Save the plan file to `docs/plans/plan-<name>.md` in **Vietnamese Markdown** containing:
- Tổng quan kiến trúc & phạm vi (các hệ thống game liên quan, tách biệt logic khỏi engine loop).
- Kế hoạch rủi ro đa nền tảng (iOS Metal vs Android Vulkan, Safe Area tai thỏ, vòng đời Pause/Resume).
- Kế hoạch migration dữ liệu lưu trữ (Save Data schema & versioning).
- Phân chia các Wave thực thi chi tiết (danh sách unit, tệp mục tiêu, acceptance criteria, chế độ TDD).
- Thứ tự thực thi đề xuất cho `00-mobile-game-orchestrator`.

In chat: Provide a summary and file link, then **halt execution and prompt the user for approval.**

## Don'ts
- Do not create, modify, or execute production code, shaders, or scene assets.
- Do not proceed to wave execution or invoke `06-mobile-game-test` / `03-mobile-game-implement` before receiving explicit user approval.
- Do not bundle dependent units into the same parallel wave.
- Do not omit the cross-platform iOS/Android risk analysis or safe-area considerations.
- Do not write the plan file in any language other than Vietnamese Markdown.
- Do not design monolithic classes that tightly couple game logic to `MonoBehaviour` / engine ticks.

## Quality Checklist
- [ ] Is the plan saved at `docs/plans/plan-<name>.md` in Vietnamese Markdown?
- [ ] Are pure game logic units decoupled from engine-specific lifecycle loops?
- [ ] Are cross-platform iOS (Metal) and Android (Vulkan/lifecycle) risks documented?
- [ ] Are safe-area notch and aspect ratio considerations included?
- [ ] Are units structured into dependency-ordered waves with concrete acceptance criteria?
- [ ] Did execution strictly halt at the Approval Gate awaiting explicit user sign-off?
