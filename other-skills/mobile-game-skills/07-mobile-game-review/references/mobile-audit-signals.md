# Mobile Audit Signals & Defect Classifications

This reference defines the technical audit signals used by `07-mobile-game-review` to inspect mobile game code across performance, GC allocations, rendering, platform runtimes, and TDD compliance.

---

## 1. GC Allocation Traps in Per-Frame Loops (BLOCKING in Tick)
Any heap allocation occurring inside per-frame tick loops (`Update`, `FixedUpdate`, `LateUpdate`, coroutine loops without intervals, render callbacks) produces GC pauses (hitching/stutter) on mobile devices:

| Defect Pattern | Antipattern Example | Compliant Replacement | Severity |
|---|---|---|---|
| **LINQ in Tick** | `enemies.Where(e => e.IsAlive).ToList();` | Manual `for` loop with reusable pre-allocated list buffer | `BLOCKING` |
| **String Formatting in Tick** | `text.text = "HP: " + currentHp;` | Custom non-alloc int-to-string buffer or event-driven UI updates | `BLOCKING` |
| **Boxing Value Types** | `object obj = playerHealth;` or passing struct to `params object[]` | Strongly typed generic methods `Print<T>(T val)` | `BLOCKING` |
| **Dynamic Allocations in Tick** | `new List<Vector3>()` or `new Collider[10]` in `Update()` | Static/reusable pre-allocated array or buffer | `BLOCKING` |
| **Allocating Physics APIs** | `Physics.RaycastAll(...)` | `Physics.RaycastNonAlloc(..., preallocatedRaycastHits)` | `BLOCKING` |
| **Uncached Component Lookups** | `GetComponent<Rigidbody>()` inside `FixedUpdate()` | Cache reference in `Awake()` or `Start()` | `BLOCKING` |
| **Closure Captures** | Lambda capturing local outer variable in tick | Cached static delegate or explicit parameter passing | `BLOCKING` |

---

## 2. Rendering, Batching & Mobile GPU Signals
Mobile GPUs rely on Tile-Based Deferred Rendering (TBDR); fill-rate overdraw and broken batching severely impact thermal throttling and battery life:

| Audit Signal | Technical Violation | Correction | Severity |
|---|---|---|---|
| **Material Instantiation** | Accessing `renderer.material` creates a cloned material, breaking batching | Use `renderer.sharedMaterial` or apply `MaterialPropertyBlock` | `BLOCKING` |
| **Monolithic Canvas Rebuild** | High-frequency animated text placed in root static Canvas, forcing full mesh rebuild | Isolate dynamic HUD elements into nested Sub-Canvases | `BLOCKING` |
| **Mass Particle Overdraw** | High particle counts with large transparent screen-filling quads | Clamp max particles, shrink screen coverage, use cutouts | `ADVISORY` |
| **Uncompressed Textures** | Raw RGBA32 textures loaded dynamically on mobile | Ensure ASTC (iOS/modern Android) or ETC2 compression format | `ADVISORY` |

---

## 3. Cross-Platform Runtime & Lifecycle Signals (iOS & Android)

| Audit Signal | Technical Violation | Correction | Severity |
|---|---|---|---|
| **Safe Area Violation** | Hardcoded top/bottom UI anchors clipping into notch / Dynamic Island | Implement dynamic RectTransform fitting to `Screen.safeArea` | `BLOCKING` |
| **Lifecycle Desync** | Ignoring `OnApplicationPause(true)`: audio continues playing, game timers drift in background | Mute audio and pause internal game loop clocks on pause | `BLOCKING` |
| **Platform #if Desync** | Game logic behaves differently under `#if UNITY_IOS` vs `#if UNITY_ANDROID` without platform rationale | Keep simulation logic 100% identical; isolate platform macros to SDK wrappers | `BLOCKING` |
| **Missing Android Back Button** | Pressing Android system back does not close modal/pause menu | Listen for `KeyCode.Escape` to navigate back or close dialogs | `ADVISORY` |

---

## 4. TDD Cheating Audit Signals (BLOCKING)
Any violation of TDD integrity mandatorily yields a `FAIL` verdict:

1. **Tautological Assertions**: `Assert.IsTrue(true)`, `Assert.AreEqual(x, x)`, or assertions comparing hardcoded identical constants.
2. **Mocking Away Core Logic**: Test mocks the entire class under test instead of mocking external dependencies.
3. **Assertion Tampering**: Modifying test expectations (e.g., lowering expected damage from 200 to 100) to force a broken implementation to pass Green.
4. **Skipped Post-Code Verification**: When TDD was skipped or inverted, omitting subsequent verification tests (`06-mobile-game-test` Scenario A/B) without an approved `no-test-framework` reason.
