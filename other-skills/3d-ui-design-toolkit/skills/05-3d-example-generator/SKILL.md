---
name: 05-3d-example-generator
description: "Generate runnable in-browser sample interfaces from the synthesized 3d_system_design.md specification using vanilla HTML/CSS/JS with optional locally vendored Three.js (WebGL). Triggered after 00-3d-ui-orchestrator completes and the user explicitly opts in."
---

# 3D Example Generator

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates only when the user consents to sample interface generation after `00-3d-ui-orchestrator` has delivered an approved `3d_system_design.md`, or when the user explicitly asks to build runnable browser samples from an existing 3D specification.

Skip when no `3d_system_design.md` exists, when the specification has not been approved, or when the user asks for production engine code (Unity C#, Unreal Blueprints, native XR apps) — that is outside this skill's scope.

## Workflow

### Phase 1: Spec Intake & Stack Selection
**Objective**: Extract every implementable decision from the specification and lock the per-page tech stack before writing code.

1. Read `docs/3d-ui-design/3d_system_design.md` and extract: spatial tokens (metric 1m = 1 unit, depth planes Near/Comfort/Far), UI classification (Diegetic/Non-diegetic/Spatial/Meta), material and shader assignments (unlit/frosted glass/holographic), SDF typography rules, component states, engine recipe, and QA contrast constraints.
2. If the spec is missing, incomplete (no spatial tokens or no UI classification), or unapproved, stop and report what is missing — never invent unspecified design decisions.
3. Select the stack per page and record it in the examples README:
   - Spec targets **Web3D or 3D in-game HUD** (real 3D scene, dynamic lighting): HTML/CSS/JS overlay layer + **Three.js (WebGL)** scene layer, with a UMD/global `three.min.js` vendored locally into `docs/3d-ui-design/examples/lib/` and loaded via a plain `<script>` tag.
   - Spec targets **Unity / Unreal / XR headsets** (not runnable in a browser): vanilla HTML/CSS/JS static screen-space mockup of that UI layer (HUD placement, focus ring, depth zoning as 2D/quasi-3D CSS transforms), with per-page simulation-limit notes.
   - Pure screen-space UI needing no 3D scene: vanilla HTML/CSS/JS only — do not load Three.js.

### Phase 2: Sample Page Generation
**Objective**: Implement the inventoried UI as standalone pages that faithfully render the spec in a browser.

1. Write all output to `docs/3d-ui-design/examples/` (create the directory if missing), one page per inventoried UI layer or screen, with `index.html` as the entry point listing links to all sample pages and their stacks.
2. Author all code in **vanilla HTML, CSS, and JavaScript** (plus vendored Three.js where stack selection requires it):
   - Express spatial tokens as CSS variables and/or Three.js scene constants; keep the metric scale (1 unit = 1 meter) and the spec's depth plane assignments.
   - With Three.js: build the materials the spec defines (unlit/emissive for critical text, frosted glass, holographic), add basic orbit/camera controls in plain JS so viewers can evaluate UI in space, and verify text stays legible under the spec's lighting scenarios.
   - With CSS mockups: simulate the spec's materials (backdrop blur, translucency, emissive accents) and annotate simulation limits on the page.
   - Demonstrate all 6 interactive states (default, hover/proximity, active/pressed, focus/raycast, disabled, loading/error) for each primary 3D interactive component.
   - Follow SDF-style typography rules and the QA contrast requirements from `04-3d-spatial-qa-optimization`.
3. Reference assets relatively only (no absolute paths, no CDN, no npm, no bundler, no module importmaps); every page must open directly via `file://`.

### Phase 3: Verification & Delivery
**Objective**: Confirm the samples open and behave standalone, then hand back a file report.

1. Verify each page has no broken relative links, no external network requests, and no dev-server dependency.
2. Cross-check every page against the spec: metric scale, depth planes, material assignments, component states, and contrast constraints.
3. Report to the user: list of created files under `docs/3d-ui-design/examples/`, the stack chosen per page, which spec sections each page demonstrates, and any spec decisions that cannot be represented in a browser sample (especially XR head-mounted ergonomics and engine-specific behaviors).

## Output Format
- `docs/3d-ui-design/examples/index.html` — gallery entry point linking all sample pages
- One standalone page (HTML + CSS + JS, optionally vendored Three.js) per inventoried UI layer
- A short `docs/3d-ui-design/examples/README.md` declaring the per-page stack, how to open the samples, and simulation limitations
- `docs/3d-ui-design/examples/lib/three.min.js` — only when the stack selection requires Three.js

## Don'ts
- Do not use bundlers, build tools, npm, module importmaps, or CDN resources — samples must run by opening `index.html` directly in a browser.
- Do not introduce spatial tokens, materials, or components absent from `3d_system_design.md`.
- Do not modify `3d_system_design.md` or any skill file while generating examples.
- Do not generate sample pages for UI layers outside the approved specification.

## Quality Checklist
- [ ] `3d_system_design.md` exists and was read in full before generation
- [ ] Stack selection recorded per page in the examples README (Three.js scene vs CSS mockup vs pure screen-space)
- [ ] All output files live under `docs/3d-ui-design/examples/` with an `index.html` entry point
- [ ] Every page uses only vanilla HTML/CSS/JS plus locally vendored Three.js, with zero external requests and `file://` compatibility
- [ ] Metric scale, depth planes, material assignments, 6 component states, and contrast rules match the spec exactly
- [ ] Simulation-limit notes present for Unity/Unreal/XR-derived mockup pages
- [ ] Final report lists every created file, its stack, and its corresponding spec section
