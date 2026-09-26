# 3D Spatial Tokens, Materials & Audio System

Standardized token architecture for 3D spatial scale, material shaders, elevation depth, and 3D spatial audio feedback.

---

## 1. Metric Scale & Spatial Depth Tokens

All 3D coordinate values conform to the universal standard: **1 unit = 1 meter (1m)**.

### 1.1. Spatial Depth Elevation Layers
Used to separate interactive controls, panels, and floating text along the local Z-axis (normal to panel face):
- `--spatial-depth-base: 0.000m` (Backing chassis or structural frame)
- `--spatial-depth-content: 0.005m` (5mm: Base text and icons resting on glass)
- `--spatial-depth-interactive: 0.015m` (15mm: Elevated button surface above panel)
- `--spatial-depth-focus: 0.030m` (30mm: Hovered/focused element popped forward)
- `--spatial-depth-overlay: 0.060m` (60mm: Contextual menus, floating tooltips)

### 1.2. Spatial Dimensions & Target Sizing
- `--spatial-target-touch-min: 0.044m` (44mm physical touch button for direct finger tap)
- `--spatial-target-raycast-min: 0.060m` (60mm for distant laser / gaze targeting at 1.5m)
- `--spatial-panel-corner-radius: 0.012m` (12mm rounded corners on 3D meshes)

---

## 2. 3D Material & Shader Specifications

```
┌─────────────────────────────────────────────────────────────┐
│ 3D MATERIAL PROFILES                                        │
├───────────────────┬─────────────────────────────────────────┤
│ 1. Unlit Emissive │ Guaranteed legibility in all lighting   │
│ 2. Glassmorphic   │ Frosted translucent glass with fresnel  │
│ 3. Holographic    │ Scanlines, additive glow, edge rim      │
└───────────────────┴─────────────────────────────────────────┘
```

### 2.1. Unlit Emissive (High-Legibility UI Controls)
- **Shader Model**: `Unlit` / Self-Illuminated.
- **Rule**: All critical text, icons, and status indicators must use unlit emissive shaders so they remain 100% legible regardless of whether the surrounding 3D world is in pitch darkness or blinding sunlight.
- **Tokens**:
  - `--mat-emissive-brand: #3B82F6` (Emission intensity: 1.5 - 2.0)
  - `--mat-emissive-alert: #EF4444` (Emission intensity: 2.5)

### 2.2. Frosted Glassmorphism (Spatial Panels in XR / VisionOS)
- **Shader Model**: Translucent PBR with physical depth refraction:
  - Base Color: `#FFFFFF` with 15% opacity (`rgba(255, 255, 255, 0.15)`)
  - Roughness: `0.25 - 0.35` (blurred frosted appearance)
  - Transmission: `0.85`
  - Index of Refraction (IOR): `1.50`
  - Specular Fresnel: Highlight rim on glancing angles (`fresnel-power: 3.0`)

### 2.3. Holographic & Cyberpunk Style (Sci-Fi / Games)
- **Shader Model**: Additive transparent blending (`srcAlpha, one`)
  - Scanline frequency: 200 lines/meter with subtle vertical crawl (0.1m/s)
  - Fresnel rim glow: Falloff 2.5, intensifying at silhouette edges

---

## 3. Positional 3D Spatial Audio Tokens (HRTF)

Audio provides critical spatial confirmation when physical tactile touch is absent in 3D:

| Interaction Event | Sound Characteristics | Spatial HRTF Setting |
| :--- | :--- | :--- |
| **Hover / Raycast Lock** | High-frequency subtle click (800 Hz, 30ms, soft sine) | Attenuation rolloff: Logarithmic; clamped to 3 meters. |
| **Select / Push Actuation**| Crisp, tactile mechanical snap (1200 Hz, 60ms) | Direct point source located at contact mesh coordinates. |
| **Modal Open / Expansion** | Harmonious whoosh swell (300-600 Hz sweep, 180ms) | Stereo spatial spread: 45 degrees. |
| **Error / Invalid Action** | Low-frequency damp thud (180 Hz, 120ms, square wave) | Point source with subtle localized screen vibration. |
