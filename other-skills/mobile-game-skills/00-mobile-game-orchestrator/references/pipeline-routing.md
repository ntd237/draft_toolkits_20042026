# Pipeline Routing Matrix & Blast Radius

## Overview
This document defines the routing matrix, blast radius evaluation, and decision heuristics for `00-mobile-game-orchestrator` across 2D/3D cross-platform mobile game projects (iOS & Android).

## 3 Request Groups & Pipeline Mapping

| Request Group | Description | Selected Pipeline | Primary Skills |
|---|---|---|---|
| **Group 1: New Implementation** | New gameplay mechanic, UI HUD, audio, save state, shader, or platform SDK | Pipeline 1 (Simple)<br>Pipeline 2 (Ambiguous)<br>Pipeline 3 (Complex/Risky) | `06-mobile-game-test` (Red) → `03-mobile-game-implement` (Green+Refactor) → `07-mobile-game-review` |
| **Group 2: Unknown-Cause Bug** | Crash, freeze/ANR, FPS drop, GC stutter, memory leak, frame pacing, touch input drop | Pipeline 4a (Simple RCA)<br>Pipeline 4b (Complex RCA) | `04-mobile-game-bugfinder` → (`06-mobile-game-test` Red → `05-mobile-game-fix` Green)* → `07-mobile-game-review` |
| **Group 3: Known-Cause Bug** | Defect with confirmed root cause, exact stack trace, or review defect report | Pipeline 5 (Simple defect)<br>Pipeline 6 (Complex defect) | (`06-mobile-game-test` Red → `05-mobile-game-fix` Green)* → `07-mobile-game-review` |

---

## 6 Canonical Pipeline Scenarios

### Pipeline 1: Simple Gameplay Implementation (Localized)
- **Condition**: Clear mechanic/logic, touches 1 isolated system, zero platform risk, no migration needed.
- **Sequence**: `06-mobile-game-test` (Red) → `03-mobile-game-implement` (Green + Refactor)* → `07-mobile-game-review`.

### Pipeline 2: Ambiguous Gameplay Requirements
- **Condition**: Game mechanics, control gestures, or balancing numbers lack concrete specs.
- **Sequence**: `01-mobile-game-brainstorm` → User Approval Gate (`docs/specs/spec-<name>.md`) → `06-mobile-game-test` (Red) → `03-mobile-game-implement` (Green + Refactor)* → `07-mobile-game-review`.

### Pipeline 3: Complex / Multi-System / Platform-Risky Implementation
- **Condition**: Spans ≥2 systems (e.g., Combat + Inventory + Save State), alters save schema, affects rendering pipeline (URP/Metal/Vulkan), or adds platform SDKs (IAP/Ads).
- **Sequence**: `01-mobile-game-brainstorm` → User Approval Gate (`docs/specs/spec-<name>.md`) → `02-mobile-game-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Parallel/Sequential Waves: `06-mobile-game-test` (Red) → `03-mobile-game-implement` (Green + Refactor)]* → `07-mobile-game-review`.

### Pipeline 4: Unknown-Cause Bug Investigation & Resolution
- **Condition**: Symptom reported without verified location (e.g., random ANR on Android, GC stutter during boss fight).
- **Sequence**: `04-mobile-game-bugfinder` → Evaluates Blast Radius:
  - **4a (Simple / Localized)**: `06-mobile-game-test` (Red) → `05-mobile-game-fix` (Green + Refactor)* → `07-mobile-game-review`.
  - **4b (Complex / Multi-System)**: `02-mobile-game-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Bug-Fix Waves: `06-mobile-game-test` (Red) → `05-mobile-game-fix` (Green)]* → `07-mobile-game-review`.

### Pipeline 5: Known-Cause Bug (Simple)
- **Condition**: Exact location and root cause identified (traceback, failing test, or review report), localized to 1 script/system.
- **Sequence**: `06-mobile-game-test` (Red) → `05-mobile-game-fix` (Green + Refactor)* → `07-mobile-game-review`.

### Pipeline 6: Known-Cause Bug (Complex / Architectural)
- **Condition**: Confirmed defect spanning multiple subsystems, save data corruption, or cross-platform lifecycle race condition.
- **Sequence**: `02-mobile-game-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Bug-Fix Waves: `06-mobile-game-test` (Red) → `05-mobile-game-fix` (Green)]* → `07-mobile-game-review`.

---

## Mobile Blast Radius Decision Matrix

Evaluate the following technical signals to distinguish **Simple** vs **Complex / High Risk**:

| Signal / Axis | Simple (Pipeline 1, 4a, 5) | Complex / High Risk (Pipeline 3, 4b, 6) |
|---|---|---|
| **Subsystems Touched** | 1 isolated subsystem (e.g., Damage calculation) | ≥2 interacting systems (e.g., Combat + Economy + Networking) |
| **Files & Components** | 1–2 pure C#/script files, localized logic | Multiple scripts, Prefabs, ScriptableObjects, or asset configs |
| **Engine Loop Footprint** | Logic decoupled from frame loop | Direct mutation of `Update()`, `FixedUpdate()`, render queue |
| **Memory & Allocations** | Zero dynamic heap allocation per tick | Object pooling changes, large AssetBundle/Addressable refactor |
| **Save Data / State** | Transient session state only | Binary/JSON save schema change, migration required |
| **Graphics & Rendering** | Standard materials/UI elements | Custom Shader Graph/HLSL, Draw Call batching, LOD changes |
| **Platform Target** | Pure platform-agnostic C# logic | Native iOS (Metal/GameCenter) vs Android (Vulkan/NDK/Gradle) |
| **App Lifecycle** | Ignores app pause/resume | Handles `OnApplicationPause`, focus loss, backgrounding |
| **Device Ergonomics** | Standard rectangular screen | Safe Area (notch/island cutouts), foldable aspect ratios |

> **Rule**: If ≥1 criterion falls under "Complex / High Risk", the orchestrator MUST route through `02-mobile-game-plan`.
