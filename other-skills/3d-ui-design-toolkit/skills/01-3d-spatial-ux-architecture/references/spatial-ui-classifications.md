# 3D UI Classifications & Spatial Interaction Models

Architectural taxonomy based on the Fagerholt & Lorentzon framework for categorizing interfaces across 3D games, XR spatial computing, and Web3D applications.

---

## 1. The 4 Classes of 3D User Interfaces

```
                  ┌──────────────────────┬──────────────────────┐
                  │    IN 3D WORLD       │     ON 2D CAMERA     │
                  │   GEOMETRY/SPACE     │     SCREEN PLANE     │
┌─────────────────┼──────────────────────┼──────────────────────┤
│ IN THE FICTION  │     DIEGETIC         │        META          │
│ (Story Reality) │ (Wrist device,       │ (Blood splatters on  │
│                 │  Cockpit gauges)     │  visor, Water drops) │
├─────────────────┼──────────────────────┼──────────────────────┤
│ OUT OF FICTION  │      SPATIAL         │     NON-DIEGETIC     │
│ (Abstract Data) │ (Floating waypoints, │ (Screen-space HP,    │
│                 │  Player nameplates)  │  Universal Pause)    │
└─────────────────┴──────────────────────┴──────────────────────┘
```

### 1.1. Diegetic UI (Full Immersion)
- **Definition**: Elements that exist physically within the 3D game world and are perceived by both the user and the virtual avatar.
- **Classic Examples**: Wristwatch health/radiation monitor (Metro), holographic ammo counter mounted directly on weapons (Dead Space, Halo), in-cockpit tactical instrument dials (Flight simulators, Elite Dangerous).
- **Design Guidelines**:
  - Bound rigidly to moving 3D bone/mesh transforms.
  - Scale realistically to physical human dimensions (e.g., wristwatch display: 40-50mm).
  - Use emissive or lighted PBR materials that respond naturally to ambient in-world lighting.

### 1.2. Spatial UI (World-Anchored Augmented Data)
- **Definition**: Digital elements positioned at coordinates in 3D world space, but not perceived by characters within the fictional world.
- **Classic Examples**: Floating objective waypoint markers, player floating health bars/nameplates, AR world-anchored spatial cards (Apple VisionOS, Meta Quest).
- **Design Guidelines**:
  - Must apply **Billboarding**: Constrain rotation to face the active camera viewpoint.
  - Implement **Distance-based Scaling**: Apply dynamic scale adjustments so markers remain legible at distances without obscuring distant terrain.
  - Integrate **Occlusion Handling**: Fade or render semi-transparent silhouettes when occluded by world geometry.

### 1.3. Non-Diegetic UI (High-Speed Utility)
- **Definition**: Traditional orthographic 2D overlay rendered on the camera plane, existing outside the 3D world fiction.
- **Classic Examples**: Persistent screen-space HUD (HP bar, ammo count, minimap), universal pause menus, settings screens.
- **Design Guidelines**:
  - Preferred when immediate, instantaneous readability is critical (esports, twitch-reflex combat).
  - Unaffected by camera movement, lighting variations, or in-world physics.

### 1.4. Meta UI (Camera-Plane Narrative Feedback)
- **Definition**: Visual representations rendered directly on the camera viewport that represent sensations experienced by the avatar.
- **Classic Examples**: Blood vignettes on the screen when taking critical damage, frosted screen edges in arctic environments, cracked goggle glass.
- **Design Guidelines**:
  - Purely informational and non-interactive.
  - Keep center screen transparent (minimum 80% clear vision).

---

## 2. Decision Matrix: Selecting UI Taxonomy

| Experience Goal | Recommended UI Model | Primary Trade-Off |
| :--- | :--- | :--- |
| **Maximum Cinematic Immersion** | **Diegetic UI** | Requires in-world head/hand movement; slower to read under chaotic combat. |
| **Augmented Spatial Awareness** | **Spatial UI** | Requires billboarding and occlusion culling; risk of scene clutter. |
| **High-Precision Competitive Play** | **Non-Diegetic UI** | Breaks world immersion; feels like a video game screen rather than virtual reality. |
| **Sensory Status Feedback** | **Meta UI** | Passive; cannot contain interactive controls or text prompts. |
