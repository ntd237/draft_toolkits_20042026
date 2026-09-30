---
name: 00-mobile-game-orchestrator
description: "Master orchestrator and domain gatekeeper for 2D/3D cross-platform mobile game development (iOS & Android, including app-level build/release). Classifies requests into 3 groups, assesses blast radius across game engine loops and platform runtimes, coordinates 6 canonical pipelines, enforces TDD discipline (Red-Green-Refactor) with skip and inverted mechanisms, manages approval checkpoints, drives the Post-Review Bug Loop, and owns the mandatory harness execution log mechanism (docs/harness-logs/). Mandatory entrypoint for all mobile game development tasks."
---

# 00-mobile-game-orchestrator — Mobile Engine & Systems Orchestrator

## Trigger
Triggers for any request touching 2D/3D mobile game development: gameplay mechanics, physics, character state machines, rendering/shaders, UI/HUD, audio, save state, object pooling, mobile input/touch controls, ad/IAP SDK integration, and iOS/Android build configurations. Mandatory entrypoint before any child skill (01–07) runs.

## Workflow

### Phase 1: Domain Gatekeeper
**Objective**: Confirm the request falls strictly within 2D/3D mobile game development.

1. **In-Scope Evaluation**: Accepts tasks involving mobile game architectures (Unity C#, Godot C#/GDScript, custom C++ mobile engines), mobile rendering (Metal, Vulkan, OpenGLES, URP, Draw Call batching), device ergonomics (safe area notches, aspect ratios, multi-touch), mobile OS lifecycles (`OnApplicationPause`, focus loss), ad/IAP SDK integration, and **app-level build/release work** — build configurations, code signing/keystore setup, build variants (dev/staging/release), CI pipelines for the game client, and store listing assets preparation (icons, screenshots, store metadata files).
2. **Deployment boundary**: only developer-account/store-console operations (uploading builds to App Store Connect / Google Play Console, account management, app review correspondence) are out of scope — hand those off to external tooling and clearly note which portion requires other tools.
3. **Out-of-Scope Rejection**: If the task is entirely unrelated to game client systems (pure web backend/frontend, enterprise databases, desktop-only enterprise software, pure data science/ML training) → politely decline, declare that this toolkit specializes in 2D/3D mobile game development, and halt.
4. **Hybrid Handling**: If a game request includes backend services (e.g., game server API, matchmaking), restrict this toolkit to the client-side game architecture and delegate server services to web/backend toolkits.

### Phase 2: Request Classification (3 Groups)
**Objective**: Classify the request into 1 of 3 operational groups:

1. **Group 1: New Implementation**: New game mechanics, AI behaviors, UI panels, shaders, or refactoring.
2. **Group 3: Known-Cause Bug**: Defect with confirmed root cause, exact stack trace, or review defect report.
3. **Group 2: Unknown-Cause Bug**: Symptoms reported without verified root causes (crash, freeze/ANR, GC stutter, FPS drop, memory leak, touch drop) → mandatory routing to `04-mobile-game-bugfinder`.

### Phase 3: Blast Radius & Platform Risk Assessment
**Objective**: Determine whether `01-mobile-game-brainstorm` and/or `02-mobile-game-plan` are mandatory based on `references/pipeline-routing.md`.

- **Ambiguous Scope** (unclear mechanics, controls, or feel) → mandatory `01-mobile-game-brainstorm`.
- **Complex / High Risk** (touches ≥2 subsystems, alters save schemas, updates `Update()` loops, introduces object pools, custom shaders, or native iOS/Android code) → mandatory `02-mobile-game-plan`.
- **Simple & Localized** (single script, isolated calculation, zero frame allocation) → bypass planning and proceed to TDD execution.

### Phase 4: Route to 6 Canonical Pipelines & Checkpoint Gates
**Objective**: Direct work through exactly 1 of 6 canonical pipeline flows:

| # | Pipeline Name | Skill Execution Sequence |
|---|---|---|
| **1** | Simple Implementation | `06-mobile-game-test` (Red) → `03-mobile-game-implement` (Green+Refactor)* → `07-mobile-game-review` |
| **2** | Ambiguous Implementation | `01-mobile-game-brainstorm` → User Approval → `06-mobile-game-test` (Red) → `03-mobile-game-implement` (Green+Refactor)* → `07-mobile-game-review` |
| **3** | Complex / Multi-System | `01-mobile-game-brainstorm` → User Approval → `02-mobile-game-plan` → User Approval → [TDD Waves: `06-mobile-game-test` Red → `03-mobile-game-implement` Green+Refactor]* → `07-mobile-game-review` |
| **4a** | Unknown Bug (Simple) | `04-mobile-game-bugfinder` → `06-mobile-game-test` (Red) → `05-mobile-game-fix` (Green+Refactor)* → `07-mobile-game-review` |
| **4b** | Unknown Bug (Complex) | `04-mobile-game-bugfinder` → `02-mobile-game-plan` → User Approval → [Bug Waves: `06-mobile-game-test` Red → `05-mobile-game-fix` Green]* → `07-mobile-game-review` |
| **5** | Known Bug (Simple) | `06-mobile-game-test` (Red) → `05-mobile-game-fix` (Green+Refactor)* → `07-mobile-game-review` |
| **6** | Known Bug (Complex) | `02-mobile-game-plan` → User Approval → [Bug Waves: `06-mobile-game-test` Red → `05-mobile-game-fix` Green]* → `07-mobile-game-review` |

(*) Repeat per atomic behavior. For TDD skip criteria or Inverted TDD, consult `references/tdd-exception-and-skip.md`.

#### Mandatory Approval Checkpoints:
1. **Brainstorm Gate (`01-mobile-game-brainstorm`)**: Presents a comprehensive summary with custom write-in options. Strictly pauses until the user explicitly reviews and approves the spec (`docs/specs/spec-<name>.md` in Vietnamese Markdown).
2. **Plan Gate (`02-mobile-game-plan`)**: Generates an execution plan (`docs/plans/plan-<name>.md` in Vietnamese Markdown). Strictly halts execution until the user explicitly approves the wave breakdown.

### Phase 5: Post-Review Bug Loop Governance
**Objective**: Guarantee that review failures are remediated strictly through bug-fix pipelines.

1. When `07-mobile-game-review` returns `FAIL` (due to ≥1 `[BLOCKING]` issue such as GC allocation in per-frame tick, native crash, safe-area clipping, or TDD cheating), the orchestrator **must** re-route to a bug-fix pipeline (4a, 4b, 5, or 6).
2. The root cause is extracted directly from the review defect report.
3. **Strict Skill Binding**: Code fixes must be executed exclusively by `05-mobile-game-fix` (never `03-mobile-game-implement`).
4. **Max 3 Iterations**: If review fails 3 consecutive times on the same issue, halt execution and escalate to the user.

## Output Format
Before invoking child skills, emit a structured coordination block:
- **Domain Gate**: Pass / Reject (with technical reason)
- **Classification**: New Implementation / Unknown-Cause Bug / Known-Cause Bug
- **Blast Radius**: Simple / Complex (subsystems, GC allocations, platform risks)
- **Selected Pipeline**: Scenario # (1–6)
- **Next Skill**: First skill to invoke + transition handoff

## Handoff Contract Schemas

### 1. TDD Red Handoff (`06-mobile-game-test` → `03-mobile-game-implement` / `05-mobile-game-fix`)
```yaml
handoff:
  from_skill: "06-mobile-game-test"
  to_skill: "03-mobile-game-implement" # or "05-mobile-game-fix"
  tdd_mode: "active"
  target_files: ["Scripts/Combat/DamageCalculator.cs"]
  failing_test_file: "tests/Combat/DamageCalculatorTests.cs"
  failing_test_name: "CalculateDamage_ArmorMitigation_ReducesDamageCorrectly"
  run_command: "dotnet test --filter DamageCalculatorTests"
  observed_failure: "Expected mitigation 0.35f, received 0.0f"
  next_behavior: "Implement armor formula with zero GC allocations"
```

### 2. TDD Skipped Code Handoff (`00-mobile-game-orchestrator` / `02-mobile-game-plan` → `03` / `05`)
```yaml
handoff:
  from_skill: "00-mobile-game-orchestrator" # or "02-mobile-game-plan"
  to_skill: "03-mobile-game-implement" # or "05-mobile-game-fix"
  tdd_mode: "skipped"
  skip_reason: "user-request" # "user-request" | "no-test-framework" | "config-only"
  target_files: ["Scripts/UI/SafeAreaFitter.cs"]
  task_goal: "Adjust RectTransform anchors based on Screen.safeArea"
  acceptance_criteria: "Pads UI away from device notch on iOS/Android"
```

### 3. TDD Skipped Test Handoff (`03-mobile-game-implement` / `05-mobile-game-fix` → `06-mobile-game-test`)
```yaml
handoff:
  from_skill: "03-mobile-game-implement" # or "05-mobile-game-fix"
  to_skill: "06-mobile-game-test"
  tdd_mode: "skipped"
  scenario: "B" # "A" for Bug Fix Confirmation | "B" for Post-Implementation Validation
  target_files: ["Scripts/UI/SafeAreaFitter.cs"]
  files_modified: ["Scripts/UI/SafeAreaFitter.cs"]
  implemented_behavior: "Anchors clamp to Screen.safeArea on device orientation change"
  run_command: "dotnet test --filter SafeAreaTests"
```

### 4. Defect Diagnosis Handoff (`04-mobile-game-bugfinder` → `06-mobile-game-test` / `02-mobile-game-plan`)
```yaml
handoff:
  from_skill: "04-mobile-game-bugfinder"
  to_skill: "06-mobile-game-test" # or "02-mobile-game-plan"
  offending_system: "Rendering / Memory"
  exact_location: "Scripts/VFX/ParticleAutoDestroy.cs:38"
  root_cause: "Instantiating GameObject inside Update without pooling causes GC spike and hitching"
  blast_radius: "simple" # "simple" | "complex"
  recommended_fix: "Replace dynamic Instantiate/Destroy with Generic ObjectPool<T>"
  cleanup_verified: true
```

### 5. Review Defect Handoff (`07-mobile-game-review` FAIL → `00-mobile-game-orchestrator`)
```yaml
handoff:
  from_skill: "07-mobile-game-review"
  to_skill: "00-mobile-game-orchestrator"
  verdict: "FAIL"
  re_entry_pipeline: 5 # 4a | 4b | 5 | 6
  blocking_issues:
    - severity: "BLOCKING"
      subsystem: "Memory / Engine Loop"
      location: "Scripts/Enemies/EnemySpawner.cs:52"
      root_cause: "LINQ Where() query executed inside Update() allocating 4.2KB/frame"
      evidence: "GC Profiler trace reveals heap allocation on every frame tick"
```

## Harness Execution Log (Mandatory)
Every pipeline run (Pipelines #1–#6) MUST produce a harness execution log file — in-chat YAML handoff blocks NEVER exempt or replace it.

1. **Before routing to the first skill**, Read `references/execution-log.md` and follow its schema verbatim: create `docs/harness-logs/<category>_<task_name>_<yyyymmdd>_<hhmmss>.md` (timestamp from a real shell command, never guessed), creating the directory if needed.
2. **After each child skill completes**, append its per-skill section immediately (do not batch at the end) — the orchestrator appends on behalf of the child skills.
3. **At pipeline completion** (including FAIL outcomes and Post-Review Bug Loop re-routes), append the pipeline summary section. For review-fail re-routes, keep the same log file and append the re-route sections — never create a second file for the same task.
4. Log content is written in Vietnamese; skill names, file paths, commands, and status keywords (COMPLETED, FAILED, PARTIAL, PASS, FAIL) stay in English.
5. Single-skill, read-only advisory tasks (pure explanation, ad-hoc Q&A) do not require a log.

## Don'ts
- Do not accept non-game web/backend or desktop enterprise tasks without passing the Domain Gate.
- Do not dispatch `03-mobile-game-implement` to fix bugs or remediate `07-mobile-game-review` defects — all defect fixes belong strictly to `05-mobile-game-fix`.
- Do not bypass `04-mobile-game-bugfinder` when root causes are unverified symptoms (e.g., "game crashes on Android").
- Do not advance past approval gates of `01-mobile-game-brainstorm` or `02-mobile-game-plan` without explicit user sign-off.
- Do not apply Fallback Ordering while TDD is active without recording an approved skip reason (`user-request`, `no-test-framework`, or `config-only`).
- Do not allow the Post-Review Bug Loop to exceed 3 iterations on the same defect.
- Do not run any pipeline (1–6) without creating the harness execution log in `docs/harness-logs/` before the first skill runs and appending each skill section after completion — the in-chat YAML handoff never replaces the log file.
- Do not create a second log file for the same task on Post-Review Bug Loop re-routes — append to the existing one.

## Quality Checklist
- [ ] Has the Domain Gate confirmed the request belongs to 2D/3D mobile game development?
- [ ] Is the request categorized accurately into 1 of the 3 groups?
- [ ] Does the selected pipeline match 1 of the 6 canonical scenarios?
- [ ] Are mandatory approval checkpoints enforced for brainstorm specs and implementation plans?
- [ ] Does the Post-Review Bug Loop route defects exclusively to `05-mobile-game-fix`?
- [ ] Are structured YAML handoff blocks populated across all skill transitions?
- [ ] Was the harness execution log created in `docs/harness-logs/` before the first skill ran, with one section appended per completed skill and the pipeline summary appended at the end (per `references/execution-log.md`)?
