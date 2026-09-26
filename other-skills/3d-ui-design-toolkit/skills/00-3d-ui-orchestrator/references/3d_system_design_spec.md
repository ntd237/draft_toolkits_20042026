# [3D Product Name] — 3D System Design Specification (3d_system_design.md)

Specification artifact for technical artists, game developers, spatial software engineers, and AI agents implementing interactive 3D interfaces.

---

## 1. 3D Product & Spatial Context

- **Product Category**: [3D Web Configurator / 3D Game / XR Spatial App / Digital Twin / Virtual World / Automotive HMI]
- **Target Medium**: [Web3D (Three.js/R3F/Babylon) / Unity / Unreal Engine / Godot / Apple VisionOS / Meta Quest]
- **Display & Viewing Modality**: [2D Monoscopic Screen (Desktop/Mobile) / Stereoscopic VR / Passthrough AR / 3D Volumetric]
- **Primary Input Mechanics**: [Mouse Raycast / Touch Drag & Pinch / 6DoF VR Controllers / Hand Tracking Gaze & Pinch / Gamepad D-pad]
- **Spatial Comfort Bounds**: Viewing distance 0.5m - 2.0m; primary FoV cone ±15° vertical, ±30° horizontal.

---

## 2. Spatial UX Architecture & Classification

### 2.1. 4-Tier UI Classification Matrix
| Element Name | Classification | Spatial Anchor & Coordinates | Fiction Integration | Interaction Modality |
| :--- | :--- | :--- | :--- | :--- |
| **Cockpit Instruments / Device** | **Diegetic** | Rigidly attached to vehicle/in-game mesh | Full world fiction | Direct physics press / pointer raycast |
| **Floating Waypoint / Nameplate**| **Spatial** | World-space coordinates with billboarding | Real-world position, non-fictional overlay | Distance-scaled click / proximity trigger |
| **HUD Resource Bar (HP/Shield)** | **Non-Diegetic** | Orthographic screen-space overlay (Camera) | Zero fictional presence | Traditional mouse / touch / controller |
| **Damage Vignette / Goggle Frost**| **Meta** | Screen plane attached to camera viewport | Perceived by character fictionally | Passive visual feedback |

### 2.2. Spatial Depth Planes
- **Near Field (< 0.5m)**: Direct manipulation zone (tactile virtual buttons, hand-held menus).
- **Mid Field / Comfort Plane (0.75m - 2.0m)**: Primary interactive canvases, floating UI panels, text dialogs.
- **Far Field (> 2.0m)**: World landmarks, skybox markers, environmental alerts.

---

## 3. 3D Design Tokens & Materials

### 3.1. Spatial Scale & Unit Standards
- **World Metric**: 1 unit = 1 meter (standard across Unity, Unreal, Three.js, VisionOS).
- **Spatial Depth Tokens**:
  - `--depth-base: 0.0m` (Reference plane)
  - `--depth-float: +0.02m` (Elevated layer / button surface)
  - `--depth-overlay: +0.05m` (Active modal / tooltips)

### 3.2. 3D Materials & Lighting Shaders
- **Shader Model**: `Unlit` or `Additive/Transparent Emission` for critical text and UI controls to ensure legibility in pitch-black or intensely lit 3D scenes.
- **Surface Material**: Glassmorphism / Frosted Glass in XR (`translucent PBR`, roughness: 0.25, metallic: 0.05, subtle fresnel edge highlight).
- **Spatial Audio Tokens**: 3D HRTF positional feedback on hover, select, and error events.

### 3.3. Spatial Typography & Billboarding
- **Font Rendering**: Signed Distance Field (SDF) / MSDF text meshes (crisp resolution at any viewing angle).
- **Billboarding Mode**: Spherical (faces camera fully) or Cylindrical (Yaw-axis only, keeping upright vertical orientation).

---

## 4. 3D Component Specifications & State Matrix

| Component | Default | Hover / Proximity (<0.5m) | Raycast Target / Gaze | Active / Press / Pinch | Disabled | Loading / Processing |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **3D World Button** | Flat plane, emissive outline | Glow intensifies + pushes forward 5mm | Focus halo + tick sound | Depresses into panel 10mm (Physics) | 30% Opacity, no depth push | Orbiting particle ring |
| **Floating Panel** | Translucent frosted slab | Elevation shadow deepens | Subtle tilt towards camera (Parallax) | Pinned to hand/raycast | Desaturated surface | Shimmer wave pulse across glass |
| **3D Hotspot Pin** | Pulsing dot + icon | Expands, displays brief label | Unfolds detailed floating card | Launches modal focus view | Static gray dot | Rotating wireframe ring |

---

## 5. Platform Engine Integration Recipes

- **Web3D (Three.js / R3F)**: `Canvas` with `OrbitControls`, HTML overlays via `@react-three/drei/Html` or 3D text using `@react-three/drei/Text` (Troika SDF).
- **Game Engine (Unity / Unreal)**: Unity World Space Canvas (Dynamic Pixels Per Unit calibrated to 100) / Unreal UMG 3D Widget Component with Unlit Material.
- **XR Spatial (Apple VisionOS / Quest)**: VisionOS SwiftUI `WindowGroup` with `.windowStyle(.volumetric)` or Meta Quest OpenXR Passthrough hand interactions.

---

## 6. Spatial QA & Performance Sign-off

- [ ] **Frame Rate Budget**: Maintained 60 FPS (Web3D/Mobile), 90/120 FPS (VR/XR Headsets).
- [ ] **Draw Call Optimization**: All 3D UI icons packed in a single Texture Atlas; dynamic text batched.
- [ ] **Transparent Overdraw**: Maximum 2 overlapping transparent layers on spatial panels.
- [ ] **Motion Sickness / Comfort Audit**: No forced camera acceleration; stereoscopic depth within comfort vergence zone (1.0m - 2.5m).
