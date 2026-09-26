# 3D Spatial Typography & Billboarding Guidelines

Technical standards for rendering crisp, legible typography in 3D space, camera billboarding behavior, and Vietnamese diacritical protection.

---

## 1. Signed Distance Field (SDF / MSDF) Font Rendering

Traditional bitmap text textures become blurry when viewed up close and suffer from aliasing artifacts at steep oblique angles in 3D space:

- **Standard Requirement**: All 3D world-space text must use **Multi-channel Signed Distance Field (MSDF)** or **Signed Distance Field (SDF)** text mesh generators (e.g., Unity TextMeshPro, Three.js Troika-Three-Text, Unreal Distance Field Fonts).
- **Benefits**:
  - Infinite vector-sharp scaling from centimeters to kilometers.
  - Efficient single-draw-call rendering per font atlas.
  - Real-time controllable text outlines, drop shadows, and glow shaders via pixel shader distance thresholds.

---

## 2. Camera Billboarding Modes

Billboarding ensures that flat 2D information cards and 3D labels remain readable by continuously orienting towards the active camera:

| Billboarding Mode | Rotation Constraints | Typical Application |
| :--- | :--- | :--- |
| **Spherical (Full 3D)** | Rotates freely on Pitch, Yaw, and Roll to face camera normal directly. | Floating world waypoints, crosshairs, flying player tags. |
| **Cylindrical (Yaw-Only)** | Rotates exclusively around the global Up-axis (Y/Z); Pitch/Roll locked. | Ground-standing NPC nameplates, vertical museum exhibition cards. |
| **Fixed / Transform-Locked**| Rigidly pinned to parent object's local rotation with zero billboarding. | Cockpit dials, in-world computer monitor screens, handheld tablet UI. |

---

## 3. Distance-Adaptive Font Scaling (Constant Angular Size)

To prevent distant 3D text from shrinking into illegible micro-pixels or nearby text from dominating the screen, apply angular size normalization:

$$\text{RenderedScale} = \text{BaseScale} \times \left(\frac{\text{Distance}}{\text{ReferenceDistance}}\right)^{\alpha}$$

- Where $\text{ReferenceDistance} = 1.5\text{m}$.
- For world waypoints: Set $\alpha = 0.8 - 1.0$ so the waypoint maintains a steady visual size on screen regardless of player distance.
- For in-world panels: Set $\alpha = 0$ (pure real-world physical scale) so the text respects physical realism.

---

## 4. Vietnamese Typography in 3D Spaces

### 4.1. 3D Text Mesh Line-Height
- **Mandatory Metric**: Set 3D line-height (`lineSpacing` / `line-height`) between **1.45 and 1.65** in 3D text generators.
- **Why**: Vietnamese stacked diacritics (huyền, sắc, hỏi, ngã, nặng + circumflex mũ ă, â, ê, ô, ơ, ư) vertically protrude above the Latin cap-height. In 3D geometry with tight line spacing, accent marks intersect with the line above or get clipped by mesh bounding boxes.

### 4.2. SDF Font Atlas Glyph Range
Ensure the font generation pipeline explicitly bakes the full **Vietnamese Unicode range**:
- Latin Extended Additional: `U+1EA0` to `U+1EF9`
- Basic Latin & Latin-1 Supplement: `U+0020` to `U+00FF`
- Latin Extended-A & B: `U+0102`, `U+0103`, `U+0110`, `U+0111`, `U+01A0`, `U+01A1`, `U+01AF`, `U+01B0`

### 4.3. 3D Bounding Box Text Expansion
- Vietnamese text expands by **20% to 30%** in length relative to English.
- Always configure 3D text mesh containers with `WordWrap: true` and set the container width with a 30% buffer, or allow automatic horizontal expansion along the local X-axis.
