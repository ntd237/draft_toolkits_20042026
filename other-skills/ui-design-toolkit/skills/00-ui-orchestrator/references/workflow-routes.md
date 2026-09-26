# UI Design Workflow Routes

Work-routing matrix for the UI/UX Design Toolkit. Use this reference to choose an optimal execution route and control output depth.

## 1. Full Design Lifecycle (Default Route)

Applied for greenfield product design or comprehensive redesigns:

```
[00-ui-orchestrator]
       ↓
[01-ux-flow-architecture]  →  Identify Personas, JTBD, Sitemap/IA, User Flows & Wireframes
       ↓
[02-ui-design-system]      →  Establish Tokens (60-30-10 Colors, Vietnamese Typography), 6-State Components
       ↓
[03-ui-platform-responsive]→  Responsive Layout (Mobile/Tablet/PC) & Platform Adaptation (Web/App/Game)
       ↓
[04-ui-ux-qa-review]       →  Audit WCAG 2.2 AA, 10 Nielsen Heuristics, Vietnamese & Responsive Stress Tests
       ↓
[Consolidated system_design.md]
       ↓ (user opt-in only — Phase 4 consent gate)
[05-ui-example-generator]  →  Static sample pages (vanilla HTML/CSS/JS) in docs/ui-design/examples/
```

## 2. Narrow-Scope Routes

When a request focuses on a specific design sub-domain, execute only the relevant specialist skill(s):

| Request Focus | Triggered Skills | Expected Deliverable |
| :--- | :--- | :--- |
| **UX flows, Wireframes & Sitemap only** | `01-ux-flow-architecture` → `04-ui-ux-qa-review` | User Flows (Happy + Error recovery paths), Structural Wireframes, Ethical UX audit. |
| **Design System & Component Library** | `02-ui-design-system` → `04-ui-ux-qa-review` | Design Tokens (CSS/JSON), Vietnamese typography rules, Component specifications (6 states). |
| **Color System & Typography only** | `02-ui-design-system` (Tokens focus) → `04-ui-ux-qa-review` | 60-30-10 Palette with Light/Dark contrast, Font stack, 1.4-1.6 line-height rules. |
| **Responsive Layout Optimization** | `03-ui-platform-responsive` → `04-ui-ux-qa-review` | Breakpoint matrix, fluid grid behaviors, navigation adaptation, container queries. |
| **Desktop App Design (Electron/Tauri/Qt/WPF)** | `02-ui-design-system` → `03-ui-platform-responsive` → `04` | Titlebar chrome, Menu bar, Context menu, keyboard shortcuts, DPI scaling, data tables. |
| **Mobile App Design (iOS / Android)** | `01-ux-flow-architecture` → `02` → `03` → `04` | Thumb zone, Bottom navigation, Safe area insets, Touch targets >= 44-48px, Bottom sheets. |
| **Game HUD & In-game UI (Desktop/Mobile)** | `01-ux-flow-architecture` (HUD) → `02` → `03` → `04` | 4-Corner HUD anchors, Gamepad focus ring, Hardware safe zones, Dual thumb touch controls. |
| **Accessibility & Usability Audit (QA Review)**| `04-ui-ux-qa-review` | WCAG 2.2 AA audit report (Contrast, Keyboard, Alt), 10 Heuristics, Vietnamese stress test. |
| **Sample Interface Generation (opt-in)** | `05-ui-example-generator` | Static sample pages (vanilla HTML/CSS/JS) in `docs/ui-design/examples/`, faithful to the approved `system_design.md`. |

## 3. Handoff Criteria Across Skills

Each skill must package its deliverables as clean inputs for downstream skills:
- `01` hands off to `02`: Screen inventory, required component list, and error scenarios.
- `02` hands off to `03`: Component tokens, target dimensions, and spacing values for layout scaling.
- `03` hands off to `04`: Layout specifications and component states across breakpoints for verification.
- `04` hands off to `00`: Compliance score, prioritized issue ledger (P0/P1/P2) for final `system_design.md` synthesis.
- `00` hands off to `05` (only after explicit user opt-in): Approved `system_design.md` path, screen inventory, and target responsive scope.
