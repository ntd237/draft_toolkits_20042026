# 3D UI Design Workflow Routes

Execution routing matrix for the 3D UI Design Toolkit. Use this reference to determine workflow depth based on the 3D application medium and input modality.

---

## 1. Full 3D Design Lifecycle (Default Route)

Applied for greenfield 3D projects, major spatial computing apps, or complete game interface overhauls:

```
[00-3d-ui-orchestrator]
       ↓
[01-3d-spatial-ux-architecture]  → Classify 4 UI Types (Diegetic/Non-diegetic/Spatial/Meta), Ergonomic FoV & Depth
       ↓
[02-3d-design-system-materials]  → Spatial Tokens (Scale, Depth, Unlit/PBR Materials, Audio), Billboarding & 3D Components
       ↓
[03-3d-platform-engine-recipes]  → Engine Integration (Web3D Three.js/R3F, Unity World Canvas, Unreal UMG, XR/VisionOS)
       ↓
[04-3d-spatial-qa-optimization]  → Audit Draw Calls, Transparent Overdraw, Vergence Conflict, Cyber Sickness
       ↓
[Consolidated 3d_system_design.md]
       ↓ (user opt-in only — Phase 4 consent gate)
[05-3d-example-generator]        → In-browser sample pages (vanilla HTML/CSS/JS + optional vendored Three.js) in docs/3d-ui-design/examples/
```

---

## 2. Specialized 3D Execution Routes

| Request Focus | Triggered Skills | Expected Deliverable |
| :--- | :--- | :--- |
| **Diegetic In-Game UI (Cockpits, Wrist, Terminals)** | `01-3d-spatial-ux-architecture` → `02` → `03` → `04` | In-world mesh UI specification, texture mapping, physical interaction flow. |
| **Web 3D / Product Configurator / Digital Twin** | `01-3d-spatial-ux-architecture` → `02` → `03` (Web3D) → `04` | Orbit camera UI, 3D hot-spots, HTML overlay vs Canvas mapping, Three.js/R3F recipe. |
| **XR / Spatial Computing (VisionOS / Meta Quest)** | `01-3d-spatial-ux-architecture` → `02` → `03` (XR) → `04` | Window/Volume/Space model, gaze & pinch targeting, 1.5m comfort plane, audio feedback. |
| **3D Floating World Markers & Spatial Waypoints** | `01-3d-spatial-ux-architecture` → `02` → `03` → `04` | Spherical/cylindrical billboarding rules, distance-based LOD scaling, occlusion culling. |
| **3D UI Performance & Draw Call Optimization** | `04-3d-spatial-qa-optimization` | Draw call audit, texture atlas consolidation, transparent overdraw elimination report. |
| **Sample Interface Generation (opt-in)** | `05-3d-example-generator` | In-browser sample pages (vanilla HTML/CSS/JS + optional vendored Three.js) in `docs/3d-ui-design/examples/`, faithful to the approved `3d_system_design.md`. |

---

## 3. Downstream Handoff Criteria

- `01` hands off to `02`: Spatial zoning, camera interaction distance (near/comfort/far), and classified UI taxonomy.
- `02` hands off to `03`: 3D mesh geometry bounds, material shaders (Unlit vs PBR), typography billboarding, and input state maps.
- `03` hands off to `04`: Engine-specific scene hierarchy, canvas render modes, and shader configurations for performance profiling.
- `04` hands off to `00`: Final performance scorecard (draw calls, frame budgets) and comfort sign-off for `3d_system_design.md`.
- `00` hands off to `05` (only after explicit user opt-in): Approved `3d_system_design.md` path, UI classification inventory, and per-layer stack candidates.
