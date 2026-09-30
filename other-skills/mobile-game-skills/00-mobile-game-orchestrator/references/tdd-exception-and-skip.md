# Mobile TDD Exceptions, Skip Criteria & Inverted Testing

## 1. Standard TDD Policy (Default)
In mobile game development, gameplay logic (combat algorithms, status effects, inventory math, quest progressions, economy balancing, and state machines) MUST follow the standard **Red → Green → Refactor** cycle:
1. `06-mobile-game-test` authors a failing unit/integration test (Red).
2. `03-mobile-game-implement` or `05-mobile-game-fix` writes the minimal production code to pass (Green) and optimizes (Refactor).
3. `07-mobile-game-review` audits implementation and test fidelity.

---

## 2. Permissible TDD Skip Criteria
Skipping the test-first Red phase is permitted IF AND ONLY IF one of the following 3 criteria is formally met and recorded in the handoff:

| Skip Reason Code | Condition Description | Required Handoff Field |
|---|---|---|
| `user-request` | The user explicitly directs the agent to bypass TDD for this task. | `skip_reason: "user-request"` |
| `no-test-framework` | The game project lacks a test runner (e.g., Unity Test Framework, Godot GUT) and the user explicitly declines installing one. | `skip_reason: "no-test-framework"` |
| `config-only` | The changes are strictly confined to non-executable assets, build metadata (Gradle `build.gradle`, Xcode `Info.plist`), static UI Canvas layouts, or audio asset assignments without logic scripts. | `skip_reason: "config-only"` |

### Fallback Ordering when TDD is Skipped
When TDD is skipped under an approved criterion, the execution order alters to Fallback Ordering. **Skipping testing entirely is prohibited** unless `no-test-framework` applies:

1. **New Implementation / Refactoring**:
   `03-mobile-game-implement` → `06-mobile-game-test` (Scenario B: Post-Implementation Validation) → `07-mobile-game-review`.
2. **Defect Fixing**:
   `05-mobile-game-fix` → `06-mobile-game-test` (Scenario A: Bug Fix Confirmation) → `07-mobile-game-review`.

> **Critical Rule**: If `no-test-framework` applies, `06-mobile-game-test` is omitted, but `03-mobile-game-implement` / `05-mobile-game-fix` must provide a comprehensive **Manual Verification Protocol** (step-by-step device or PlayMode checklist).

---

## 3. Inverted TDD Protocol (Spikes & Game Feel)
Certain game systems cannot be cleanly specified upfront via automated assertions. Inverted TDD (Implement First → Author Tests Immediately After) is allowed for specific atomic units:

### Permitted Inverted TDD Scenarios:
1. **Technical Spikes & Engine Experiments**:
   - Prototyping custom HLSL/Shader Graph shaders on mobile GPUs (tile-based rendering limits).
   - Validating newly imported platform SDK plugins (Apple Game Center, Google Play Games Services).
2. **Game Feel, Juice & Visual Polish**:
   - Tweaking camera shake curves, particle burst timings, gamepad haptics, or spring-damping animations where correctness is purely perceptual.
3. **Hardware & Input Ergonomics**:
   - Tuning multi-touch gesture dead zones, virtual joystick responsiveness, or safe-area cutout padding on physical notch displays.

### Inverted TDD Guardrails:
- The unit must be flagged as `inverted_tdd: true` in the plan or brainstorm spec.
- Production code is authored by `03-mobile-game-implement` (features) or `05-mobile-game-fix` (fixes).
- Immediately upon completing the spike/feel tuning, `06-mobile-game-test` **must** execute to author characterization tests or freeze parameters (e.g., validating curve ranges, clamping bounds, zero GC allocations) to prevent regression.
- Bypassing subsequent verification after an inverted implementation is strictly prohibited.
