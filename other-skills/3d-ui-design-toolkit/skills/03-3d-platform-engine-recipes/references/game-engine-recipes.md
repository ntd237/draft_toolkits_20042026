# Game Engine 3D UI Recipes (Unity, Unreal Engine & Godot)

Implementation patterns for in-world, diegetic, and spatial user interfaces across major real-time game engines.

---

## 1. Unity Game Engine (World Space Canvas & UI Toolkit)

```
[GameObject] ──(Canvas: World Space)──→ [RectTransform: Metric Scale 0.001]
    │
 ├── [CanvasScaler: Dynamic Pixels Per Unit = 100]
 ├── [GraphicRaycaster + TrackedDeviceGraphicRaycaster (XR)]
 └── [TextMeshPro 3D: SDF Font Material (Unlit)]
```

### 1.1. World Space Canvas Calibration
- **Canvas Render Mode**: Set to `World Space`.
- **Metric Normalization**:
  - By default, Unity Canvas units are pixels. To map 1 unit = 1 meter, set Canvas `Scale = (0.001, 0.001, 0.001)`.
  - A 500px wide panel now measures exactly 0.5 meters in 3D world space.
- **Dynamic Pixels Per Unit (PPU)**: Set `Dynamic Pixels Per Unit = 10 - 20` to prevent blurry text rendering when zoomed.

### 1.2. Raycast Input Handling
- **Non-XR Mouse**: Attach a `PhysicsRaycaster` to the main camera. Add `BoxCollider` to interactive UI meshes.
- **XR Controller**: Attach `TrackedDeviceGraphicRaycaster` to the Canvas. Drive interaction via the XR Interaction Toolkit `XR Ray Interactor`.

---

## 2. Unreal Engine (UMG 3D Widget Components)

Unreal projects 2D UMG Slate widgets onto 3D polygon meshes via Widget Components:

### 2.1. Widget Component Configuration
- **Component**: Add `WidgetComponent` to any Actor Blueprint.
- **Space**: Set to `World`.
- **Geometry Mode**: Set to `Plane` or `Cylinder` (for curved sci-fi HUDs).
- **Material Blend Mode**: Use `Masked` or `Translucent`.
- **Material Domain**: Set material domain to `User Interface` with an **Unlit** shading model to guarantee constant brightness.

### 2.2. Player Interaction (`WidgetInteractionComponent`)
- Add `WidgetInteractionComponent` to the Player Character / Controller attached to the camera or motion controller hand mesh.
- Set `Interaction Distance = 500` (5 meters).
- Forward input events:
  - `PressPointerKey(EKeys::LeftMouseButton)` on trigger pull / click.
  - Call `PressAndReleaseKey(EKeys::Enter)` for gamepad confirmation.

---

## 3. Godot Engine (SubViewport to 3D Quad)

In Godot 4.x, 2D Control nodes are projected into 3D via Viewport Textures:

1. **Hierarchy**:
   ```
   Node3D
     ├── SubViewport (size: 1024x768, render_target_update_mode: Always)
     │     └── Control (UI elements, buttons, text)
     └── MeshInstance3D (QuadMesh: size 1.0m x 0.75m)
   ```
2. **Material**: Create a `StandardMaterial3D`:
   - Set `Albedo > Texture` to a `ViewportTexture` pointing to the `SubViewport`.
   - Enable `Shading > Shading Mode = Unshaded` for consistent UI illumination.
3. **Raycast Input**: Intercept mouse events on the `CollisionObject3D` covering the QuadMesh and project UV coordinates to `SubViewport.push_input()`.
