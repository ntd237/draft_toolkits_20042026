---
name: 04-3d-spatial-qa-optimization
description: "Audit 3D UI performance (draw calls, overdraw, LOD), spatial contrast against 3D lighting, and cyber sickness comfort standards."
---

# 3D Spatial QA & Performance Optimization

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs to audit 3D interface rendering performance (draw calls, transparent overdraw, texture atlasing, LOD), evaluate spatial accessibility (contrast against dynamic 3D scenes, angular target sizes), or eliminate cyber sickness risks before final delivery.

Skip during initial spatial concept phases before 3D scene hierarchy and asset budgets are defined.

## Workflow

### Phase 1: 3D Rendering Performance & Draw Call Audit
**Objective**: Profile and enforce GPU/CPU rendering budgets for 3D UI per `references/3d-rendering-performance.md`.

1. Measure UI draw call count against platform hardware ceilings (Max 10-25 for Web3D/Mobile, Max 10-20 for standalone XR).
2. Audit texture memory and batching: Confirm all UI iconography shares a unified texture atlas, and text meshes share a global SDF font atlas.
3. Inspect transparent overdraw: Verify that stacked translucent layers do not exceed 2 layers in any line of sight.
4. Validate distance-based LOD and culling: Confirm 3D markers beyond 15m collapse detail and occluded markers are culled.

### Phase 2: Spatial Accessibility & Contrast Audit
**Objective**: Guarantee universal interface legibility and operability across dynamic 3D lighting conditions.

1. Test text contrast per `references/spatial-accessibility-comfort.md`: Confirm text maintains >= 4.5:1 contrast against both dark and bright lighting states via unlit backing plates or high-contrast outlines.
2. Verify angular target sizing: Confirm interactive colliders maintain an angular size of at least **1.5° to 2.0°** with >= 0.5° separation.
3. Validate multi-sensory feedback: Ensure all 3D positional audio cues have visual graphic equivalents.

### Phase 3: Cyber Sickness & Comfort Verification
**Objective**: Audit physiological comfort factors in stereoscopic 3D and moving virtual environments.

1. Verify camera motion independence: Confirm zero programmatic camera acceleration or unrequested camera tilting.
2. Check depth vergence: Confirm no high-attention reading panels are positioned closer than 0.75m.
3. Construct the Prioritized Issue Ledger:
   - **P0 - Blocker**: Frame rate drop below target budget, nausea-inducing camera rotation, completely occluded interaction targets.
   - **P1 - Major**: Text contrast failure under scene lighting changes, excessive overdraw throttling GPU, controls outside comfort cone.
   - **P2 - Minor**: Minor billboarding lag, decorative z-fighting, subtle audio balance discrepancies.

## Output Format
Spatial QA & Performance Report containing:
1. Performance Scorecard (Draw calls, Overdraw layers, FPS budget)
2. Spatial Accessibility Scorecard (Contrast against lighting, Angular target size, Sensory redundancy)
3. Prioritized Spatial Issue Ledger (ID -> Element -> Severity P0/P1/P2 -> Description -> Fix Recommendation)
4. Final Sign-off Verdict (PASS / ACTION REQUIRED)

## Don'ts
- Do not pass a 3D interface that introduces forced programmatic camera tilts or rotational acceleration.
- Do not permit more than 2 stacked transparent panel layers on mobile or standalone XR hardware.
- Do not approve floating text that lacks backing plates or outline shaders against changing 3D scene lighting.

## Quality Checklist
- [ ] UI draw calls verified within target platform budget (<= 25 draw calls)
- [ ] All 3D UI icons packed into a single texture atlas
- [ ] Transparent overdraw bounded to maximum 2 layers
- [ ] 3D text contrast verified >= 4.5:1 across dark and bright scene lighting
- [ ] Interactive targets reach minimum 1.5° visual angular diameter
- [ ] Stereoscopic text positioned beyond 0.75m to avoid vergence-accommodation strain
- [ ] All P0 blocker issues resolved before sign-off
