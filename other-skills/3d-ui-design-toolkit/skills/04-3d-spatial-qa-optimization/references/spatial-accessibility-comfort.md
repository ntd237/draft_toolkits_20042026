# Spatial Accessibility & Comfort Audit Matrix

Guidelines for auditing spatial accessibility, visual contrast against dynamic 3D scenes, cyber sickness hazards, and issue severity classifications.

---

## 1. 3D Spatial Accessibility Standards (Spatial WCAG)

### 1.1. Contrast Against Dynamic 3D Environments
- **Challenge**: Unlike static 2D screens, 3D world lighting dynamically shifts as the sun sets, flashlights pass, or explosions occur.
- **Rule**: Text rendered in 3D world space must never rely on transparency alone without an underlying backing plate:
  - Provide a semi-opaque dark backing quad (`rgba(0,0,0,0.65)`) behind text.
  - Or render high-contrast black outlines around white SDF text characters (outline width: 10-15% of glyph stroke).
  - Guarantee minimum **4.5:1** contrast ratio against the darkest and brightest anticipated scene backgrounds.

### 1.2. Angular Target Sizing (Visual Angle Minimums)
Physical millimeters mean nothing if the user is 5 meters away. Interactive 3D targets must maintain visual angular dimensions:
- **Minimum Target Angular Diameter**: **1.5° to 2.0°** of the user's visual field (equivalent to ~44mm at 1.2 meters).
- **Target Separation**: Minimum **0.5°** angular gap between adjacent 3D colliders to prevent mis-clicks with 6DoF rays.

### 1.3. Dual-Channel Sensory Redundancy
- Never rely solely on 3D positional audio cues to signal critical game/app state; always pair with a visual 3D indicator (e.g., sound direction arrow, spatial wave pulse).
- Support closed captions attached to the speaking NPC's head with cylindrical billboarding.

---

## 2. Cyber Sickness (VR/XR Simulator Sickness) Audit

Verify whether the 3D application introduces physiological nausea triggers:

- [ ] **No Unrequested Camera Rotation**: Camera yaw, pitch, and roll are driven strictly by player physical head/mouse rotation.
- [ ] **Vergence-Accommodation Check**: No high-attention text or interactive menus placed closer than 0.75m in stereoscopic 3D.
- [ ] **Peripheral Tunneling / Vignette**: Peripheral field-of-view automatically narrows during artificial locomotion or rapid camera acceleration.
- [ ] **Resting Frame of Reference**: A stable visual anchor (cockpit canopy, vehicle hood, subtle floor grid) is present during high-speed travel.

---

## 3. 3D Issue Severity Matrix (P0 / P1 / P2)

- **P0 - Blocker (Motion Sickness Hazard / Critical Occlusion)**:
  - Forced programmatic camera tilting inducing nausea; UI frame rate dropping below 60/72 FPS; critical interactive element completely occluded inside 3D wall collision geometry.
  - *Action*: Mandatory resolution before release.
- **P1 - Major (Legibility Barrier / Ergonomic Strain)**:
  - 3D text unreadable due to scene lighting changes (contrast < 3:1); interactive button placed outside the ±30° comfort cone; transparent overdraw causing GPU thermal throttling.
  - *Action*: Fix in the active development cycle.
- **P2 - Minor (Spatial Polish)**:
  - Slight spatial audio attenuation discrepancy; sub-optimal billboarding easing during fast turns; minor z-fighting on decorative trims.
  - *Action*: Record in spatial debt backlog.
