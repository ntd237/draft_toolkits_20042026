# Component Specifications & 6-States Matrix

Specification standards for component interaction states and physical target dimensions across platforms.

---

## 1. Mandatory 6-States Interaction Matrix

Every interactive component (Buttons, Inputs, Checkboxes, Selects, Table Rows, Cards) must define all 6 states:

```
[Default] ──(Hover)──→ [Hover] ──(Press/Click)──→ [Active / Pressed]
    │                                                    │
 (Tab/Nav)                                            (Submit)
    ↓                                                    ↓
[Focus-visible]                                    [Loading / Processing]
    │                                                    │
 (Disable condition)                                  (Result)
    ↓                                                    ↓
[Disabled]                                         [Success / Error]
```

| State | Purpose & Visual Signatures | Technical Rule |
| :--- | :--- | :--- |
| **1. Default** | Base resting state of the element. | Meets WCAG 2.2 AA contrast ratios. |
| **2. Hover** | Mouse cursor hovers over element (pointer devices only). | Lighten/darken background by 8-12%, elevate shadow. |
| **3. Active / Pressed**| Pointer click down or physical touch contact. | Slight compression (`transform: scale(0.98)`), 15% darker background. |
| **4. Focus-visible** | Keyboard navigation (`Tab`) or Gamepad controller selection. | Distinct outline ring: `outline: 2px solid var(--color-brand); outline-offset: 2px;` (Contrast ratio >= 3:1). |
| **5. Disabled** | Element temporarily unavailable for interaction. | `opacity: 0.4 - 0.5`, `cursor: not-allowed`, removed from Tab order (`tabindex="-1"`). |
| **6. Loading / Error** | Asynchronous operation in progress or validation failure. | Loading: Spinner replaces icon, click locked (`pointer-events: none`). Error: Red border + contextual error copy below. |

---

## 2. Target Sizing Minimums

| Platform / Input Model | Minimum Dimensions | Recommended Target |
| :--- | :--- | :--- |
| **Touch Screen (Mobile, Tablet, Mobile Game)** | 44 x 44 px (iOS) / 48 x 48 dp (Android) | **48 x 48 px** with at least 8px separation between adjacent touch points. |
| **Pointer / Mouse (Desktop, Web)** | 32 x 32 px | **36 x 36 px** or **40 x 40 px** for primary operational targets. |
| **Gamepad Focus (Game Desktop / Console)** | 48 x 48 px | **60 x 60 px** with a 3px glowing Focus Ring visible from 2-3 meters. |

---

## 3. Core Component Blueprints

### 3.1. Primary, Secondary & Destructive Buttons
- **Primary**: Background `var(--color-brand-default)`, text `var(--color-brand-contrast)`. Reserved for the single most important action on a view (Submit, Continue, Purchase).
- **Secondary / Outline**: Transparent background, border `1px solid var(--border-subtle)`, text `var(--text-primary)`. Used for secondary actions (Cancel, Back, Export).
- **Destructive**: Red background `var(--color-error)` or red border. Reserved strictly for irreversible destructive actions (Delete account, Discard draft). Requires confirmation dialog.

### 3.2. Form Inputs & Error Messaging
- **Height**: 40px (Desktop), 48px (Mobile).
- **Structure**:
  - `Label`: Positioned above input, text `var(--text-secondary)`, size 12-14px.
  - `Input Field`: Rounded `var(--radius-md)`, border `1px solid var(--border-subtle)`, text `var(--text-primary)`.
  - `Helper / Error Text`: Displayed beneath field. On error, border turns red and error text appears alongside an alert icon.

### 3.3. Modals & Dialogs
- **Backdrop**: `background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px);`.
- **Scroll Lock**: Body scroll is locked while modal is mounted.
- **Focus Trap**: Keyboard `Tab` cycles exclusively within the modal; `Escape` key immediately closes it.
- **Mobile Adaptation**: On mobile viewports, center modals automatically convert into **Bottom Sheets** (swipe down to dismiss).
