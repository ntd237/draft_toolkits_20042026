---
name: 03-3d-platform-engine-recipes
description: "Implement 3D UI architectures across Web3D (Three.js, R3F, Babylon), Game Engines (Unity, Unreal, Godot), and XR Spatial platforms (VisionOS, Quest)."
---

# 3D Platform & Engine Recipes

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs engine-specific 3D UI implementation recipes for Web3D (Three.js, React Three Fiber, Babylon.js, Spline), Game Engines (Unity World Space, Unreal UMG 3D Widgets, Godot), or XR Spatial Platforms (Apple VisionOS, Meta Quest OpenXR).

Skip when the task focuses exclusively on 2D DOM layouts without 3D canvas or game engine scene integration.

## Workflow

### Phase 1: Web3D Spatial Implementation (Three.js / R3F / Babylon)
**Objective**: Architect web-based 3D interfaces integrating interactive 3D scene elements with modern DOM UI.

1. Implement in-scene 3D elements using `@react-three/drei` per `references/web3d-spatial-recipes.md`:
   - Use `<Text>` (Troika MSDF) for crisp 3D labels with Vietnamese line-height (1.5).
   - Use `<Html transform occlude>` for complex interactive DOM forms embedded into 3D meshes.
2. Build hybrid viewport overlays: Pair a transparent background 3D canvas with high-performance 2D HTML controls, synchronized via lightweight state stores.
3. Configure Babylon.js `GUI3DManager` or Spline runtime event bindings where applicable.

### Phase 2: Game Engine 3D UI Integration (Unity / Unreal / Godot)
**Objective**: Configure in-world and spatial widget components within real-time game engines.

1. **Unity**: Configure World Space Canvases per `references/game-engine-recipes.md`:
   - Normalize scale to metric standard (`Scale = 0.001` for 1mm per pixel).
   - Set Dynamic Pixels Per Unit to 10-20 to prevent zoom blur.
   - Attach `GraphicRaycaster` or `TrackedDeviceGraphicRaycaster` for XR controller rays.
2. **Unreal Engine**: Configure Actor `WidgetComponent` set to `World` space with an `Unlit` material domain, paired with character `WidgetInteractionComponent`.
3. **Godot**: Render 2D `SubViewport` controls onto a `QuadMesh` with an unshaded `ViewportTexture` material.

### Phase 3: XR & Spatial Computing (VisionOS & Meta Quest)
**Objective**: Deploy native spatial containers, eye-gaze targeting, and hand tracking gestures.

1. **Apple VisionOS**:
   - Implement the 3-container model: Windows, Volumes, and Immersive Spaces per `references/xr-spatial-computing.md`.
   - Apply native `.glassBackgroundEffect()` and `.hoverEffect()` for gaze-and-pinch targeting.
   - Enforce minimum 44pt target sizes with at least 16pt target separation.
2. **Meta Quest / OpenXR**:
   - Configure `PokeInteractable` for physical finger-touch buttons (<0.45m).
   - Bind `RayInteractable` for distant spatial canvas laser navigation.
   - Anchor UI panels to real-world surfaces using spatial anchors with passthrough occlusion.

## Output Format
Engine Integration Blueprint specifying:
1. Scene hierarchy and canvas render mode configurations
2. Component code snippets / Blueprint wiring instructions
3. Input raycaster and collider bindings

## Don'ts
- Do not mix unscaled screen-space pixels into world-space canvases without metric normalization.
- Do not use opaque solid backdrops for VisionOS windows instead of native glass background materials.
- Do not deploy 3D UI without input raycaster colliders or hit-test bounding volumes.

## Quality Checklist
- [ ] Engine-appropriate render mode explicitly declared (World Space / 3D Widget / Spatial Volume)
- [ ] Metric coordinate scale (1 unit = 1 meter) maintained across scene hierarchy
- [ ] 3D text uses SDF/MSDF mesh generation with unlit shader profiles
- [ ] Input handling specified for the target platform (mouse raycast, controller laser, or gaze-pinch)
- [ ] XR targets meet minimum size thresholds (>= 44pt / 44mm)
