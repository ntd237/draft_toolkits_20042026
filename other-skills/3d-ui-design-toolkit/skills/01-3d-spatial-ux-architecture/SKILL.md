---
name: 01-3d-spatial-ux-architecture
description: "Define 3D spatial user journeys, 4-tier UI classifications (Diegetic, Non-Diegetic, Spatial, Meta), depth planes, and ergonomic comfort zones."
---

# 3D Spatial UX Architecture

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs to structure spatial user journeys, classify 3D interface components (Diegetic, Non-diegetic, Spatial, Meta), establish viewing depth planes, or design ergonomic comfort zones and interaction modalities across 3D and XR environments.

Skip when designing flat 2D viewport overlays without world-space coordinate or spatial depth requirements.

## Workflow

### Phase 1: Spatial Mapping & UI Taxonomy Classification
**Objective**: Categorize all interface elements into the 4 architectural classes based on narrative immersion and utility needs.

1. Classify interface components using `references/spatial-ui-classifications.md`:
   - **Diegetic UI**: In-world physical meshes (vehicle dashboards, wristwatch monitors, terminals).
   - **Spatial UI**: World-anchored digital overlays (floating waypoints, interactive 3D pins, spatial cards).
   - **Non-Diegetic UI**: Orthographic camera-plane HUDs (speedometer, emergency alerts, pause menus).
   - **Meta UI**: Camera-plane narrative status feedback (damage vignettes, night-vision visor effects).
2. Establish the anchor coordinate system for each element: World-space transform, bone-attached socket, or camera-space canvas.

### Phase 2: Ergonomics, Comfort Cones & Depth Planes
**Objective**: Map viewing distance tiers and angular field-of-view comfort cones to prevent user fatigue.

1. Partition interactive elements across depth planes per `references/3d-ergonomics-comfort-zones.md`:
   - Near Touch Zone (< 0.5m): Direct physical manipulation and tactile controls.
   - Primary Comfort Plane (1.2m - 1.8m): Floating UI panels, reading content, and primary selection cards.
   - Far Environment Zone (> 3.0m): Environmental markers and spatial waypoints.
2. Verify angular FoV placement: Restrict high-frequency UI interactions to ±30° horizontal and ±15° vertical of center gaze.
3. Integrate cyber sickness mitigations: Stable visual reference anchors, snap-turn support, and peripheral tunneling during locomotion.

### Phase 3: Spatial Interaction Flow & Wireframing
**Objective**: Design end-to-end spatial interaction flows and produce 3D ASCII spatial layout schematics.

1. Define interaction mechanics per element: Mouse raycasting, 6DoF laser pointers, gaze-and-pinch, or direct physics touch.
2. Specify hover/proximity transitions, distance-based level of detail (LOD), and occlusion behavior when objects move behind 3D world geometry.
3. Package spatial layout blueprints for handoff to `02-3d-design-system-materials` and `03-3d-platform-engine-recipes`.

## Output Format
Spatial UX Architecture Document containing:
1. 4-Tier UI Classification Inventory
2. Ergonomic Depth & FoV Placement Map (Near / Comfort / Far tiers)
3. 3D Spatial Wireframe Layout (ASCII diagram illustrating spatial anchors relative to camera)

## Don'ts
- Do not place persistent UI elements outside the ±30° horizontal comfort cone, forcing continuous head rotation.
- Do not place high-density reading text closer than 0.75m in stereoscopic 3D, inducing vergence-accommodation eye strain.
- Do not animate or rotate the player's 3D camera programmatically without direct user input.

## Quality Checklist
- [ ] Every UI element mapped to one of the 4 classes (Diegetic, Non-diegetic, Spatial, Meta)
- [ ] Primary floating panels anchored within the 1.2m - 1.8m comfort plane
- [ ] Interactive elements placed within ±30° horizontal and ±15° vertical of center gaze
- [ ] Occlusion handling rules specified for world-space markers
- [ ] Cyber sickness safeguards incorporated for moving camera environments
