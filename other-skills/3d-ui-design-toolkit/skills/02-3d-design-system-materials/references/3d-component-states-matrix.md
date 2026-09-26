# 3D Component Specifications & Spatial State Matrix

Specifications for 3D interactive primitives, physical depth transitions, and feedback across spatial input modalities.

---

## 1. 6-States Spatial Interaction Matrix

Unlike flat 2D screens, 3D elements exist across depth and respond to physical hand proximity, raycast alignment, and 3D actuation:

```
[Default] ──(Hand approaches <0.3m)──→ [Proximity Active]
    │                                          │
 (Raycast / Gaze lock)                  (Contact Touch)
    ↓                                          ↓
[Raycast Focus] ──(Click / Pinch)──→ [Active / Pressed]
    │                                          │
 (Disabled flag)                            (Submit)
    ↓                                          ↓
[Disabled]                             [Loading / Orbiting]
```

| State | Visual Signatures in 3D Space | Spatial Audio & Haptic Feedback |
| :--- | :--- | :--- |
| **1. Default** | Base resting depth (`--depth-base`), resting material emission. | Silent. |
| **2. Proximity** | User's virtual hand or avatar approaches within 0.3m: Button elevates forward along Z-axis by +10mm; ambient particle glow. | Subtle proximity drone (very soft 400Hz tone, fading with distance). |
| **3. Raycast Focus / Gaze** | Laser pointer or eye-gaze locks onto 3D collider: High-contrast outline glow, +15mm forward float, scale up 1.05x. | Short high-frequency chirp (800Hz, 30ms); subtle haptic pulse on controller. |
| **4. Active / Pressed** | Physical button depresses -10mm inward along Z-axis with spring resistance, or pinch gesture snaps closed. | Sharp mechanical snap click (1200Hz); firm haptic click impulse. |
| **5. Disabled** | 30% desaturated material, recessed -5mm into panel chassis, colliders deactivated (`isTrigger = false`). | Dull rejection thud if targeted. |
| **6. Loading / Processing**| Component surface displays an orbiting 3D volumetric wireframe ring or pulsating glowing wave. | Continuous rhythmic ambient pulse until complete. |

---

## 2. Core 3D Interactive Primitives

### 2.1. 3D Physical Push Button
- **Dimensions**: 60mm x 60mm x 15mm (depth).
- **Physical Spring Mechanics**:
  - Unpressed resting surface at $Z = 0\text{mm}$.
  - Maximum compression travel: $Z = -10\text{mm}$.
  - Actuation trigger fired when depth surpasses $-8\text{mm}$ with spring release return.
- **Visual Styling**: Chamfered bevels with emissive edge lines.

### 2.2. Floating Spatial Slate / Panel
- **Dimensions**: Scalable based on content (e.g., 0.6m width x 0.4m height x 0.01m depth).
- **Material**: Translucent frosted glass with dynamic fresnel highlight border.
- **Grabbable Bar**: Top or bottom handle mesh (40mm thickness) for 6DoF repositioning and depth push/pull.
- **Parallax Layering**: Internal card elements positioned +5mm to +20mm in front of the slate base.

### 2.3. 3D Spatial Slider / Rotary Dial
- **Slider Track**: Physical 3D grooved rail (length 0.3m, depth 8mm).
- **Handle Thumb**: Ergonomic spherical or cylindrical knob (diameter 44mm).
- **Detents / Notches**: Discrete haptic clicks and audio ticks at every step increment.

### 2.4. 3D Spatial Hotspot Pin
- **Structure**: Floating beacon (pulsing diamond or beacon pin).
- **Behavior**:
  - Distance > 10m: Compact glowing dot with spherical billboarding.
  - Distance 2m - 10m: Expands into icon + brief title card.
  - User gaze / click: Expands into full 3D informational slate oriented towards user.
