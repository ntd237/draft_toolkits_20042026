# 3D Spatial Ergonomics, Comfort Zones & Interaction Modalities

Ergonomic standards for field-of-view (FoV), depth planes, interaction modalities, and cyber sickness mitigation in 3D and spatial computing environments.

---

## 1. Spatial Field of View (FoV) & Comfort Cones

In 3D viewports and XR headsets, placing interactive elements outside natural eye/head ranges causes rapid neck and eye fatigue:

```
                  ┌───────────────────────────────┐
                  │      MAX EYE ROTATION (±20°)  │
                  │   ┌───────────────────────┐   │
                  │   │   COMFORT CONE (±15°) │   │
                  │   │   ┌───────────────┐   │   │
                  │   │   │  CENTER FOCUS │   │   │
                  │   │   └───────────────┘   │   │
                  │   └───────────────────────┘   │
                  └───────────────────────────────┘
```

- **Optimal Visual Comfort Zone**:
  - **Horizontal**: Within **±30°** of resting forward gaze line.
  - **Vertical**: Within **±15°** of horizontal eye level (preferably slightly downward at -5° to -15° for natural resting neck posture).
- **Maximum Acceptable Range (Requiring Head Turn)**:
  - Horizontal: **±55°**. Never place persistent HUD or interactive UI beyond ±55°.
  - Vertical: **±25°** upward, **±35°** downward.

---

## 2. Depth Planes & Vergence-Accommodation Mitigation

Stereoscopic 3D displays can cause eye strain when focal distance (accommodation) does not match the 3D depth of convergence (vergence):

### 2.1. Standard Depth Tiers
1. **Near Touch Zone (< 0.5 meters)**:
   - Reserved for direct physical manipulation (virtual keyboards, tactile 3D buttons pushed with index fingers).
   - Use sparingly for short bursts; prolonged arm extension causes "gorilla arm" fatigue.
2. **Primary Comfort Workspace (1.2 to 1.8 meters)**:
   - **The Gold Standard Plane** for floating UI panels, text windows, and primary menus.
   - Minimizes the vergence-accommodation conflict in all modern XR headsets.
   - Users interact via distant raycast pointer or gaze-and-pinch.
3. **Far Environment Zone (> 3.0 meters)**:
   - Used for environmental waypoints, landmarks, skybox status notifications.
   - Text must be dynamically scaled up proportionally to distance to retain visual angular size.

---

## 3. 3D Interaction Modalities

| Modality | Typical Hardware | Interaction Mechanism | Ergonomic Consideration |
| :--- | :--- | :--- | :--- |
| **Mouse / Touch Raycast** | Web3D on Desktop/Mobile | Screen-to-world 3D raycast with bounding box hit-test | Fast, precise, zero fatigue; lacks direct depth perception. |
| **6DoF Controller Laser** | Meta Quest, HTC Vive, PCVR | Parabolic or straight ray projected from handheld controller | Reliable, high precision; requires hand elevation. |
| **Gaze & Pinch** | Apple VisionOS | Eye-tracking targets element + subtle index-thumb pinch | Lowest physical effort; requires large focus targets (>= 44pt). |
| **Direct Physics Touch** | VR / Mixed Reality | 3D hand mesh collides with spring-loaded physical button | High tactile immersion; prone to fatigue if overused. |

---

## 4. Cyber Sickness (Motion Sickness) Prevention Rules

- **Fixed Reference Frame**: When the virtual camera moves, provide a stable visual anchor (cockpit frame, vehicle dashboard, or subtle nose/vignette overlay) to reduce sensory vestibular conflict.
- **Never Force Camera Motion**: Never rotate, tilt, or accelerate the user's camera viewpoint programmatically without direct user input.
- **Snap Turn Option**: For discrete 3D navigation, offer discrete 30°/45° snap turns alongside smooth turning.
- **Dynamic Field-of-View Reduction**: Automatically contract peripheral vision (tunneling / vignette) during rapid virtual translation or sprinting.
