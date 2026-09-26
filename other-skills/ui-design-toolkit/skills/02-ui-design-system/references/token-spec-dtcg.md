# Design Tokens Specification (DTCG & CSS Standard)

Standardized specification for defining Design Tokens following the W3C Design Tokens Community Group (DTCG) model and CSS Custom Properties mapping.

---

## 1. Token Hierarchy Tiers

1. **Global Tokens (Primitive)**: Raw literal values: `blue-500: #3b82f6`, `space-4: 16px`.
2. **Semantic Tokens (System)**: Contextual purpose and intent: `color-brand-primary: {blue-500}`, `bg-surface-card: {neutral-0}`.
3. **Component Tokens**: Scoped to individual components: `button-primary-bg: {color-brand-primary}`.

---

## 2. 60-30-10 Color System & Light / Dark Mapping

The color palette adheres to the 60-30-10 visual distribution rule:
- **60% Dominant Neutral**: Canvas backgrounds, container surfaces, subtle dividing lines.
- **30% Secondary Structure**: Primary/secondary text, card borders, secondary buttons, structural chrome.
- **10% Accent / Action**: Primary call-to-action (CTA) buttons, active highlights, key links.

### 2.1. Standard CSS Tokens (Light & Dark Theme)
```css
:root {
  /* 60% Dominant Neutral */
  --bg-app: #F8FAFC;
  --bg-surface: #FFFFFF;
  --border-subtle: #E2E8F0;

  /* 30% Secondary */
  --text-primary: #0F172A;     /* Contrast ratio >= 12:1 against bg-surface */
  --text-secondary: #475569;   /* Contrast ratio >= 5.5:1 */
  --text-muted: #64748B;

  /* 10% Accent */
  --color-brand-default: #2563EB;
  --color-brand-hover: #1D4ED8;
  --color-brand-active: #1E40AF;
  --color-brand-contrast: #FFFFFF;

  /* Feedback Semantics */
  --color-success: #16A34A;
  --color-warning: #D97706;
  --color-error: #DC2626;
  --color-info: #0284C7;
}

[data-theme="dark"] {
  /* 60% Dominant Neutral */
  --bg-app: #020617;
  --bg-surface: #0F172A;
  --border-subtle: #1E293B;

  /* 30% Secondary */
  --text-primary: #F8FAFC;     /* Contrast ratio >= 12:1 against bg-surface */
  --text-secondary: #94A3B8;   /* Contrast ratio >= 5.5:1 */
  --text-muted: #64748B;

  /* 10% Accent (lighter tint for dark theme contrast) */
  --color-brand-default: #3B82F6;
  --color-brand-hover: #60A5FA;
  --color-brand-active: #2563EB;
  --color-brand-contrast: #0F172A;

  /* Feedback Semantics */
  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #38BDF8;
}
```

---

## 3. Spacing, Radius, Shadow & Motion Tokens

### 3.1. Base-8 Spacing Scale
Built on an 8px grid system with 4px micro-increments:
- `--space-1: 4px` (Gap between icon and label)
- `--space-2: 8px` (Compact button padding, label-to-input gap)
- `--space-3: 12px` (Dense card padding)
- `--space-4: 16px` (Standard card and input field padding)
- `--space-6: 24px` (Section gap on mobile displays)
- `--space-8: 32px` (Section gap on desktop displays)
- `--space-12: 48px` (Page outer margins, hero section offsets)

### 3.2. Border Radius & Elevation Shadows
- `--radius-sm: 4px` (Tags, checkboxes, badges)
- `--radius-md: 8px` (Buttons, inputs, dropdown items)
- `--radius-lg: 12px` (Cards, dialogs, bottom sheets)
- `--radius-full: 9999px` (Avatars, pill badges)
- `--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05)`
- `--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)`
- `--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)`

### 3.3. Motion Tokens
- `--motion-duration-fast: 150ms` (Hover feedback, active button press, tooltips)
- `--motion-duration-normal: 250ms` (Modal presentation, slide drawer, dropdown collapse)
- `--motion-duration-slow: 400ms` (Page transition, major view expansions)
- `--motion-easing-standard: cubic-bezier(0.2, 0, 0, 1)`
- Mandatory accessibility support: Override durations to `0.01ms` under `@media (prefers-reduced-motion: reduce)`.
