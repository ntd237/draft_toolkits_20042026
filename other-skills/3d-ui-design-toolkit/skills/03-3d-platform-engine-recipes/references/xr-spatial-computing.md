# XR & Spatial Computing Recipes (Apple VisionOS & Meta Quest OpenXR)

Implementation standards for native spatial computing platforms: Apple VisionOS (SwiftUI / RealityKit) and Meta Quest (OpenXR / Horizon OS).

---

## 1. Apple VisionOS Architecture (SwiftUI & RealityKit)

VisionOS defines 3 fundamental spatial presentation primitives:

```
┌─────────────────────────────────────────────────────────────┐
│ VISIONOS SPATIAL CONTAINERS                                 │
├─────────────┬───────────────────────────────────────────────┤
│ 1. Window   │ Planar 2.5D floating panel with glass material│
│ 2. Volume   │ Bounded 3D cubic box containing 3D models     │
│ 3. Space    │ Unbounded immersive world (Passthrough or VR) │
└─────────────┴───────────────────────────────────────────────┘
```

### 1.1. SwiftUI Spatial Styling
- **Frosted Glass Material**: Use `.glassBackgroundEffect()` as the universal window backdrop. Do not use opaque solid backgrounds.
- **Eye-Gaze Hover Effect**: Apply `.hoverEffect()` to all interactive buttons. The system automatically handles luminous highlight expansion when the user's eye looks at the element.
- **Ornaments**: Attach peripheral toolbars outside the main window bounds using `.ornament(attachmentAnchor: .scene(.bottom))`.

### 1.2. VisionOS Touch Target Sizing
- **Gaze & Pinch Target**: Interactive elements must measure at least **44 x 44 points** with at least **16pt** spacing between adjacent targets to prevent eye-tracking ambiguity.

---

## 2. Meta Quest & OpenXR Interaction SDK

Built on OpenXR standards for 6DoF controllers and optical hand tracking:

### 2.1. Interaction SDK Primitives
- **Poke Interaction (`PokeInteractable`)**: Direct finger push for close-range virtual buttons (< 0.45m). Includes visual depth displacement and surface resistance.
- **Ray Interaction (`RayInteractable`)**: Laser pointer interaction for mid-range (1.0m - 3.0m) floating spatial canvases.
- **Distance Grab**: Grabbing and pulling spatial slates closer or pushing them back along the Z-axis.

### 2.2. Passthrough MR Integration
- **Spatial Anchors (`OVRSpatialAnchor`)**: Pin UI dashboards to real-world physical surfaces (walls, desks).
- **Environment Depth Collision**: Enable passthrough occlusion so virtual 3D UI panels disappear naturally behind real-world physical hands and obstacles.
