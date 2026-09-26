---
name: 02-3d-design-system-materials
description: "Engineer 3D spatial design tokens, unlit/PBR materials, HRTF 3D audio, SDF typography, and full-state 3D interactive components."
---

# 3D Design System & Spatial Materials

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs to define 3D spatial tokens (scale, depth layers), select material shaders (Unlit emissive, frosted glass, holographic), configure 3D spatial audio, implement SDF typography with Vietnamese diacritics support, or specify 3D interactive components with physical actuation states.

Skip when the task focuses purely on high-level spatial sitemaps or performance profiling without asset styling.

## Workflow

### Phase 1: Spatial Tokens & Material Shaders
**Objective**: Establish a standardized token architecture for spatial scale, depth layering, material shaders, and 3D positional audio.

1. Configure spatial depth tokens per `references/3d-spatial-tokens.md` using the metric scale (1 unit = 1 meter) with local Z-axis depth layers (`--depth-base`, `--depth-interactive`, `--depth-focus`).
2. Assign material shader profiles:
   - Unlit Emissive for mission-critical text and buttons to guarantee readability in all scene lighting conditions.
   - Frosted Glassmorphic PBR (translucent with roughness 0.25 and fresnel rim) for XR spatial canvases.
   - Holographic additive shaders for sci-fi HUDs and in-game tactical projections.
3. Map 3D positional audio tokens (HRTF) for hover (800Hz), select snap (1200Hz), and error states.

### Phase 2: Spatial Typography & Billboarding Standards
**Objective**: Implement razor-sharp distance field text rendering and camera-facing billboarding behaviors.

1. Mandate Signed Distance Field (SDF / MSDF) font rendering per `references/spatial-typography-legibility.md` to prevent pixelation at extreme angles and distances.
2. Configure billboarding modes based on component role:
   - Spherical billboarding for floating waypoints and spatial status tags.
   - Cylindrical billboarding (Yaw-axis only) for ground-anchored markers and NPC labels.
   - Fixed transform for in-cockpit instruments and virtual tablet screens.
3. Enforce Vietnamese typography protection: Set 3D line-height between **1.45 and 1.65** and provide a 30% text container buffer along the local X-axis.

### Phase 3: 3D Component Specifications & States
**Objective**: Produce specifications for interactive 3D primitives covering physical depth travel and multi-modal feedback.

1. Specify core 3D components: 3D Physical Push Buttons, Floating Spatial Slates, 3D Spatial Sliders, and World Hotspot Pins.
2. For each 3D component, define all 6 spatial states per `references/3d-component-states-matrix.md`:
   - `Default` → `Proximity` (<0.3m approach) → `Raycast Focus / Gaze` → `Active / Pressed` (-10mm physical compression) → `Disabled` → `Loading / Orbiting`.
3. Verify target dimensions: Minimum 44mm for direct finger touch; 60mm for distant raycast / gaze targeting at 1.5m.

## Output Format
3D Design System Document containing:
1. Spatial Scale & Depth Tokens (Metric CSS / JSON)
2. Material & Shader Specification Table (Shader model, roughness, emission, blend mode)
3. Spatial Typography & Billboarding Configuration
4. 3D Component Specification Matrix (Dimensions, travel depth, 6 interaction states)

## Don'ts
- Do not use lit PBR shaders on small text elements that turn unreadable in dark or intensely shadowed 3D environments.
- Do not set 3D line-height below 1.45 for Vietnamese text meshes, which causes accent mark collisions.
- Do not design 3D buttons without visual depth travel (Z-axis compression) or audio/haptic feedback during actuation.

## Quality Checklist
- [ ] Metric spatial units established (1 unit = 1 meter) with local Z-depth layers
- [ ] Critical text elements utilize unlit/emissive shaders for universal legibility
- [ ] Typography specifies SDF/MSDF font rendering with billboarding mode declared
- [ ] Vietnamese 3D line-height set between 1.45 and 1.65 with +30% expansion margin
- [ ] Interactive 3D components specify all 6 spatial states including proximity and physical press travel
- [ ] Positional 3D audio tokens mapped to interaction events
