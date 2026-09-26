# 3D UI Rendering Performance & Optimization Guide

Standards for draw-call reduction, transparent overdraw mitigation, texture atlasing, and frame budgets for 3D interfaces.

---

## 1. Frame Rate & Hardware Budgets

Interactive 3D UI must not compromise the host application's real-time rendering loop:

| Platform / Target Medium | Target Frame Rate | Frame Time Budget | Max UI Draw Calls |
| :--- | :--- | :--- | :--- |
| **Web3D (Desktop Web)** | 60 FPS | 16.6 ms | 15 - 25 draw calls |
| **Web3D (Mobile Web)** | 60 FPS | 16.6 ms | 5 - 10 draw calls |
| **PC / Console Games** | 60 - 144 FPS | 6.9 - 16.6 ms | 20 - 40 draw calls |
| **Standalone XR (Quest, Vive)**| 72 / 90 / 120 FPS | 8.3 - 13.8 ms | 10 - 20 draw calls |

*Core Rule*: An interface that drops frames in VR/XR directly induces **cyber sickness and physical nausea**.

---

## 2. Draw Call Reduction Techniques for 3D UI

1. **Sprite Sheets & Texture Atlasing**:
   - Pack all 3D UI iconography, button borders, and frame textures into a single shared texture atlas (e.g., 2048x2048 PNG).
   - Prevents GPU state changes when rendering complex multi-element 3D dashboards.
2. **Shared SDF Font Atlases**:
   - Share a single global Signed Distance Field font atlas across all 3D text meshes in the scene graph.
   - Dynamic text generation must not rebuild the font atlas during runtime gameplay.
3. **GPU Instancing for Repeated 3D Elements**:
   - When displaying multiple world-space hotspot pins, waypoints, or inventory slots, render them via GPU instanced meshes (`InstancedMesh` in Three.js / GPU Instancing in Unity).

---

## 3. Transparent Overdraw Mitigation

Mobile and standalone XR chipsets utilize Tile-Based Deferred Renderers (TBDR), where transparent overdraw is the single biggest performance killer:

- **The Problem**: Multiple stacked translucent panels (e.g., glass panel + card overlay + button background + glow effect) force the GPU to shade the exact same pixel 4–6 times per frame.
- **Overdraw Threshold**: Restrict transparent layer stacking to a maximum of **2 layers** in any line of sight.
- **Opaque / Cutout Alternatives**:
  - Use alpha testing / cutout (`discard` in pixel shader) instead of alpha blending where smooth edge transparency is unnecessary.
  - Render panel backdrops with pre-baked opaque frosted textures rather than real-time dynamic blur passes on low-end hardware.

---

## 4. Distance-Based Level of Detail (LOD) & Culling

- **Frustum Culling**: Ensure 3D UI meshes outside the camera frustum are culled before draw submission.
- **Distance LOD Thresholds**:
  - Distance > 15m: Disable secondary sub-text and interactive button colliders; render simplified icon billboard only.
  - Distance > 50m: Cull or collapse multiple nearby pins into a single clustered counter pin.
- **Occlusion Culling**: Raycast occluded spatial UI markers against static world collision geometry to fade out or hide obstructed markers.
