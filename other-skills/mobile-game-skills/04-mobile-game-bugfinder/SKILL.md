---
name: 04-mobile-game-bugfinder
description: "Investigates and pinpoints the true root cause of crashes, freezes/ANRs, FPS hitching, memory leaks, frame pacing stutter, and touch input drops in 2D/3D mobile games across iOS and Android. Operates a 3-tier diagnostic ladder (non-invasive observation → transient [DEBUG-PROBE] instrumentation → human device reproduction) with a mandatory Cleanup Gate. Product-read-only — strictly prohibited from implementing permanent code fixes."
---

# 04-mobile-game-bugfinder — Root Cause Investigation

## Trigger
Mandatorily invoked by `00-mobile-game-orchestrator` when a bug or performance degradation occurs with unknown or unverified causes (Pipeline 4a/4b). Read-only on production logic; temporary transient instrumentation is strictly governed by the Cleanup Gate.

## Mobile Defect Domains
Covers the core failure vectors of mobile game clients:
- **Crashes**: Native iOS crashes (`EXC_BAD_ACCESS`, Metal shader compilation failures, OOM Jetsam terminations), Android native crashes (`SIGSEGV`, JNI local ref overflows, Vulkan validation crashes), and managed exceptions (`NullReferenceException`, array index bounds).
- **Freezes & ANRs**: Main thread stalled by synchronous resource loading, heavy pathfinding algorithms, or deadlock during app suspension.
- **Performance & Stutter**: GC collection spikes (heap allocation churn), Draw Call spikes, excessive overdraw on tile-based mobile GPUs, and Canvas rebuild thrashing.
- **Memory Leaks**: Undisposed AssetBundles/Addressables, leaked native textures, lingering static event delegates retaining destroyed GameObjects.
- **Input & Frame Pacing**: Irregular frame pacing (V-Sync misalignments, thermal throttling drops), and lost multi-touch events under frame lag.

## Workflow

### Phase 1: Symptom Capture & Subsystem Localization
**Objective**: Gather diagnostic artifacts and isolate the offending subsystem.

1. **Artifact Ingestion**: Collect stack traces, crash dumps (iOS `.ips` / Android tombstone & logcat), profiler captures (Unity Profiler, Xcode Instruments, Android GPU Inspector), and reproduction steps.
2. **Subsystem Isolation**: Pinpoint whether the fault originates in Gameplay Logic, Physics/Collision, Animation, UI/Canvas, Audio, Asset Streaming, or Platform Native Plugins.
3. **Reproduction Validation**: If reproduction conditions are missing or ambiguous, formulate specific diagnostic queries rather than speculating.

### Phase 2: Diagnostic Ladder & Root Cause Pinpointing
**Objective**: Traverse the 3-tier diagnostic ladder to isolate the exact line, asset, or allocation causing the defect.

1. **Tier 0 (Non-Invasive Observation)**: Inspect stack traces, profiler frames, memory allocation dumps, and platform logs without touching source code.
2. **Tier 1 (Transient Debug Probes)**: If non-invasive methods cannot isolate intermittent issues (e.g., race conditions during scene transitions, lifecycle pause/resume timing):
   - Insert temporary read-only probe statements tagged strictly with `// [DEBUG-PROBE]`.
   - Probes must only log values, timestamps, or allocation markers — **never alter state, modify game variables, or change execution flow**.
3. **Tier 2 (Human Device Reproduction)**: If the issue depends on physical hardware factors (multi-touch gesture timing, gyroscope, thermal throttling over sustained play), compile clear reproduction instructions and pause for human testing.
4. **Identify True Cause**: Distinguish symptoms from root causes (e.g., "Framerate dropped to 15 FPS" is a symptom; "Spawning 20 bullets per second using `Instantiate` creates 3.5MB GC allocation triggering GC.Collect every 2 seconds" is the root cause).

### Phase 3: Blast Radius Assessment
**Objective**: Determine whether the fix requires simple or complex routing.

- **Simple (Pipeline 4a)**: Localized defect in 1 script, isolated math error, or missing reference with no cross-system side effects.
- **Complex (Pipeline 4b)**: Defect involving save data corruption, asset bundle lifecycle, multi-threading/async operations, or native platform lifecycle callbacks.

### Phase 4: Mandatory Cleanup Gate & Handoff
**Objective**: Ensure 100% of temporary probe instrumentation is removed prior to handoff.

1. Search the entire codebase for `[DEBUG-PROBE]` to locate all injected probes.
2. Delete every probe statement and revert modified files to their exact pre-investigation state.
3. Run `git diff` / inspection to confirm zero residual debug probes remain (`cleanup_verified: true`).

## Output Format
Emit an investigation report:
- **Observed Symptoms & Environment**: Device model, OS (iOS/Android), reproduction frequency.
- **Offending Subsystem**: Memory / Rendering / Physics / Lifecycle / Logic.
- **Exact Root Cause**: Script path, line number, offending method/allocation, and technical explanation.
- **Blast Radius**: Simple (→ Pipeline 4a) or Complex (→ Pipeline 4b).
- **Recommended Remediation**: Architectural fix advice (do not write fix code).
- **YAML Handoff Block**:
```yaml
handoff:
  from_skill: "04-mobile-game-bugfinder"
  to_skill: "06-mobile-game-test" # or "02-mobile-game-plan" if complex
  offending_system: "Memory / Engine Loop"
  exact_location: "Scripts/Weapons/BulletEmitter.cs:45"
  root_cause: "Repeated instantiation of GameObject in Fire() triggers heavy GC pause on mobile devices"
  blast_radius: "simple" # "simple" | "complex"
  recommended_fix: "Use generic object pooling with pre-warmed capacity"
  cleanup_verified: true
```

## Don'ts
- Do not implement permanent fixes or refactor code — investigation only; all fixing belongs to `05-mobile-game-fix`.
- Do not leave any `[DEBUG-PROBE]` statements in the codebase — 100% removal is mandatory.
- Do not inject probe code that mutates state, executes logic, or alters timing.
- Do not stop at surface symptoms (e.g., reporting "NullRef occurred" without identifying why the reference was null).
- Do not skip Blast Radius evaluation — this determines routing between Pipeline 4a and 4b.

## Quality Checklist
- [ ] Were non-invasive logs and profiler traces analyzed prior to inserting transient probes?
- [ ] Were all temporary probes tagged with `// [DEBUG-PROBE]` and 100% removed (Cleanup Gate passed)?
- [ ] Is the root cause isolated to an exact file, line number, or asset?
- [ ] Is the distinction between symptom and root cause clearly articulated?
- [ ] Was the blast radius accurately classified to guide orchestrator branching (4a vs 4b)?
- [ ] Is `cleanup_verified: true` present in the YAML handoff block?
