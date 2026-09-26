# Game UI / HUD Design & Ergonomics

Standards for Heads-Up Display (HUD) architecture, in-game menus, and ergonomic controller navigation across Desktop (PC/Console) and Mobile gaming platforms.

---

## 1. 4-Corner HUD Safe Zones

Game HUDs serve as graphic overlays on top of a dynamic real-time rendering scene. Information modules must be anchored firmly to the 4 corners of the viewport, preserving the central screen area strictly for gameplay vision.

```
┌─────────────────────────────────────────────────────────────┐
│ [TOP-LEFT ANCHOR]                               [TOP-RIGHT] │
│ • Character Avatar                              • Minimap   │
│ • Health (HP) / Resource (Mana)                 • Ping / FPS│
│ • Level & Active Buffs                          • Objectives│
│                                                             │
│                    [CENTRAL VISION ZONE]                    │
│                 Crosshair / Player Avatar                   │
│             Critical immediate alerts only                  │
│                                                             │
│ [BOTTOM-LEFT ANCHOR]                         [BOTTOM-RIGHT] │
│ • Chat Box / Combat Log                      • Skill Cluster│
│ • Ammo / Stance Indicator                    • Action Buttons│
│                                              • Ultimate (Ult)│
└─────────────────────────────────────────────────────────────┘
```

### 1.1. Hardware Safe Zone Offsets
- **Margin Offset**: Minimum **32px to 48px** offset from all screen edges to avoid display overscan on televisions and rounded monitor corners.
- **Aspect Ratio Scaling (16:9 to 21:9 Ultrawide)**:
  - 16:9 (1920x1080) represents the baseline canvas.
  - On **21:9 Ultrawide (2560x1080 / 3440x1440)**: Provide a user toggle: either lock the HUD clusters to the 16:9 central zone (reducing eye strain) or anchor to the extreme edges of 21:9.

---

## 2. Desktop Game UI: Gamepad Navigation & In-Game Menus

### 2.1. Controller Focus Rings
- **Seamless Gamepad Transition**: When gamepad input is detected:
  - The mouse cursor disappears immediately.
  - The focused item receives a high-contrast glowing **Focus Ring** (Scale 1.05 + luminous highlight border) and auditory click feedback.
  - D-pad / thumbstick 4-way traversal (Up/Down/Left/Right) must remain unbroken with zero dead-ends.
- **Button Prompts**: Display standardized platform glyphs (`A` Select, `B` Back, `X` Options, `LB/RB` Tab shift).

### 2.2. In-Game Menus (Pause, Inventory, Skill Trees)
- **3D World Legibility**: Underlay menus with a darkened background mask (60-80% black overlay + gaussian blur) to separate UI text from underlying scene geometry.
- **Grid Inventories**: Uniform slot grids displaying contextual item comparison tooltips on focus.

---

## 3. Mobile Game UI: Dual Thumb Ergonomics

```
┌─────────────────────────────────────────────────────────────┐
│ [Pause] [Score/Wave]                          [Settings] 🔋 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                                                             │
│                                                             │
│    ┌─────────┐                                ┌─────────┐   │
│    │ Virtual │                                │ Action  │   │
│    │ D-pad   │                                │ Skill   │   │
│    │ Joystick│                                │ Cluster │   │
│    └─────────┘                                └─────────┘   │
└─────────────────────────────────────────────────────────────┘
  ▲ Left Thumb Zone                       ▲ Right Thumb Zone
```

### 3.1. Dual Thumb Control Zones
- **Landscape Ergonomics**:
  - **Left Hand**: Floating virtual joystick spawning directly under the thumb contact point.
  - **Right Hand**: Arc-shaped skill button cluster (Primary attack 64x64px, secondary abilities 48x48px arrayed along natural thumb reach).
- **Bevel Separation**: Minimum 24-32px clearance from physical device edges to prevent hand cramping.

### 3.2. Performance & Visual Clarity
- **Texture Atlases**: Bundle all HUD icons and frames into a unified texture atlas to minimize GPU draw calls.
- **Semi-Transparency**: Maintain 60-70% opacity on informational panels to keep threats visible behind the UI.
- **Haptic Feedback**: Trigger subtle vibration pulses upon skill actuation or taking damage.
