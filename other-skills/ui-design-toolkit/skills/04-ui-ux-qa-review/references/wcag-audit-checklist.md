# WCAG 2.2 AA Accessibility Audit Checklist

Audit checklist and standard compliance criteria based on Web Content Accessibility Guidelines (WCAG 2.2 Level AA).

---

## 1. Color Contrast Standards (WCAG 1.4.3 & 1.4.11)

| Element Category | Minimum WCAG AA Ratio | Enhanced WCAG AAA Ratio | Measurement Method |
| :--- | :--- | :--- | :--- |
| **Normal Text (< 18pt / 24px)** | **At least 4.5:1** | At least 7.0:1 | Contrast between foreground text (`color`) and immediate surface (`background`). |
| **Large Text (>= 18pt or >= 14pt Bold)**| **At least 3.0:1** | At least 4.5:1 | Applies to Display headings, H1, H2, Title headers. |
| **UI Components & Meaningful Icons**| **At least 3.0:1** | At least 4.5:1 | Applies to form borders, status icons, graphical indicators. |
| **Disabled Elements** | Exempt | Exempt | Disabled controls are legally exempt from contrast thresholds. |

*Core Invariant*: **Never use color as the SOLE means** of communicating meaning, state, or error feedback (always accompany color with text or iconography).

---

## 2. Keyboard Navigation & Focus Accessibility

- [ ] **100% Keyboard Operability (2.1.1)**: Every button, link, menu item, and form input must be operable using `Tab`, `Shift+Tab`, `Enter`, `Space`, and Arrow keys.
- [ ] **No Keyboard Trap (2.1.2)**: When a modal, drawer, or dropdown opens, users must be able to dismiss it using the `Escape` key without getting trapped.
- [ ] **Focus Visible (2.4.7 & 2.4.13)**:
  - Focus ring must have at least **2px** outline thickness with >= 3:1 contrast against adjacent backgrounds.
  - Never apply `outline: none` or `outline: 0` without immediately providing a high-contrast replacement style.
- [ ] **Logical Focus Order (2.4.3)**: Keyboard tab navigation must reflect logical visual reading order (top-to-bottom, left-to-right).

---

## 3. Semantic Structure & Screen Reader ARIA

- [ ] **Alternative Text (1.1.1)**: Informative images require descriptive `alt` text; purely decorative graphics must have `alt=""` or `aria-hidden="true"`.
- [ ] **Form Labels (2.5.3)**: Every form input must have a persistent `<label>` element programmatically linked via `for="id"`; placeholders must not substitute for labels.
- [ ] **State Announcements (ARIA States)**: Collapsible containers, dropdowns, and drawers must bind `aria-expanded="true/false"` and `aria-controls`.
- [ ] **Live Regions (4.1.3)**: Asynchronous status updates (Toasts, notification badges) must use `aria-live="polite"` so screen readers announce changes.

---

## 4. Text Zoom & Target Sizing

- [ ] **200% Text Scaling (1.4.4)**: At 200% browser zoom, content must reflow without clipping, overlapping, or forcing horizontal scrolling.
- [ ] **Target Size Minimum (2.5.8)**: Interactive touch targets must meet at least **44 x 44 px** (inclusive of transparent hit padding).
