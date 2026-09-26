# UX User Flows & Wireframe Patterns

Reference patterns for mapping user journeys, information architecture (IA), task flows, and structural wireframes for digital products.

---

## 1. Interaction Flow Mapping Patterns

Every critical user flow must follow a 5-phase structure:
`Trigger → User Action → System Processing → Edge/Error Handling → Completion/Handoff`.

### 1.1. Flow State Matrix
```
[User Action] ──(Valid)──→ [System Processing] ──→ [Success View]
       │
   (Invalid / Error)
       ↓
[Inline Error Banner] ──→ [Provide Recovery Action] ──→ (User Retries)
```

| Step | User Action | System State | Risk / Fail Point | Recovery Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **S1: Initiation** | Click primary action (e.g., "Checkout", "Create Item") | Display input modal / form view | Unauthenticated or expired session | Modal login in-place; do not redirect away and wipe form state |
| **S2: Data Entry** | Fill required input fields | Validate format inline on blur | Missing field, invalid format | Inline red border + contextual error message beneath input |
| **S3: Submission** | Click submit action | Button switches to loading spinner | Network loss / request timeout | Retain all entered data, surface toast error + direct "Retry" button |
| **S4: Completion** | View outcome | Navigate to success screen or update list | Server lag before database sync | Optimistic UI update or skeleton loader during synchronization |

---

## 2. Information Architecture (IA Patterns)

### 2.1. Hierarchical Tree Architecture
Standard for SaaS, Web Apps, E-commerce, and Desktop productivity tools:
- **Level 1 (Global Nav)**: Persistent Sidebar / Header (Dashboard, Projects, Analytics, Settings).
- **Level 2 (Section Nav)**: Tabs or sub-navigation within module (Overview, Details, Members, Audit Log).
- **Level 3 (Contextual Actions)**: In-page panels, filter drawers, detail modals.
*Rule*: The user should reach any primary job-to-be-done within at most **3 interactions**.

### 2.2. Hub-and-Spoke & Flat Architecture
- **Mobile App**: Home screen serves as Hub (Bottom Tab Bar 3–5 items), branching into child screens (Spokes), returning via Back button or edge swipe gesture.
- **Game HUD / Menu**: Main Menu serves as Hub leading to Gameplay, Inventory, Skill Tree, Settings. During gameplay, HUD operates as an overlay layer over the rendering scene.

---

## 3. Structural Wireframe Blueprints

### 3.1. Web App / Desktop Tool Wireframe (High Data Density)
```
┌─────────────────────────────────────────────────────────────┐
│ [Logo] [Search Bar......................] [Notifications] [User] │
├──────────────┬──────────────────────────────────────────────┤
│ • Dashboard  │ Breadcrumb: Home > Projects > Project Alpha  │
│ • Projects   │ ┌──────────────────────────────────────────┐ │
│ • Analytics  │ │ [Page Title]             [+ Action Button]│ │
│ • Settings   │ ├──────────────────────────────────────────┤ │
│              │ │ [Filters...] [Search in table...] [Export]│ │
│              │ │ ┌──────────────────────────────────────┐ │ │
│              │ │ │ Table Header (Sortable)              │ │ │
│              │ │ │ Row 1: Col A | Col B | Col C | [...] │ │ │
│              │ │ │ Row 2: Col A | Col B | Col C | [...] │ │ │
│              │ │ └──────────────────────────────────────┘ │ │
│              │ │ Pagination: < 1 2 3 4 5 >                  │ │
│              │ └──────────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────────┘
```

### 3.2. Mobile App Wireframe (Thumb-Friendly Ergonomics)
```
┌───────────────────────┐
│ 09:41           🔋 5G │ ← Status Bar (Safe Area)
├───────────────────────┤
│ [Title]           [🔍]│ ← Top App Bar
├───────────────────────┤
│ [Banner / Highlight]  │
│ ┌───────────────────┐ │
│ │ Card Info         │ │
│ └───────────────────┘ │
│                       │
│ Quick Categories      │
│ [A] [B] [C] [D]       │
│                       │
│ Content List          │
│ ┌───────────────────┐ │
│ │ Item 1            │ │
│ ├───────────────────┤ │
│ │ Item 2            │ │
│ └───────────────────┘ │
├───────────────────────┤
│ [🏠]  [📂]  [🔔]  [👤]│ ← Bottom Navigation Bar (Thumb Zone)
│          ▬            │ ← Home Indicator (Bottom Safe Area)
└───────────────────────┘
```
