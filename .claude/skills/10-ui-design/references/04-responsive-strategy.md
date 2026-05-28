# Phase 4 — Responsive Strategy (PC / Tablet / Mobile)

## Objective

Define breakpoints, grids, container patterns, and per-bucket layout decisions so the UI works at **320 px and at 1920 px+** without ever feeling stretched, squished, or out of place.

By the end of this phase you must have:

- Confirmed breakpoint tokens
- A grid system (12-col PC, 8-col Tablet, 4-col Mobile by default)
- Per-bucket layout adaptations for every surface in scope
- A navigation pattern decision per bucket
- Touch-target and reach-zone rules
- Decisions on adaptive vs. responsive vs. container-query approaches

---

## Section A — Breakpoint Architecture

### A.1 — Tokens (from `02-design-system-foundations.md`)

```
breakpoint.xs  → 0       (mobile portrait)
breakpoint.sm  → 640 px  (mobile landscape / small tablet)
breakpoint.md  → 768 px  (tablet portrait)
breakpoint.lg  → 1024 px (PC / tablet landscape — KEY transition)
breakpoint.xl  → 1280 px (PC wide)
breakpoint.2xl → 1536 px (PC ultra-wide)
```

### A.2 — Three-Tier Bucketing

For most product UIs, three buckets are enough:

| Bucket | Width | Layout signal | Density | Input |
|---|---|---|---|---|
| **Mobile** | 320–639 px | single column, stacked | comfortable | touch |
| **Tablet** | 640–1023 px | 2-col split, drawer nav | comfortable | touch (often) |
| **PC** | 1024 px+ | multi-col, sidebar + content + aside | compact-comfortable | mouse + keyboard |

The `1024 px` boundary is the most important — nav patterns, density, and grid all change at that line.

### A.3 — When to use 4 or 5 buckets

Use more granular buckets when:

- The product has both mobile and ultra-wide PC use cases (e.g., dashboard + mobile companion)
- Content density meaningfully differs between 1280 px and 1920 px
- Sidebar can be persistent at PC wide but auto-collapse at PC narrow

Do not multiply buckets without a reason; each bucket multiplies QA effort.

---

## Section B — Grid System

### B.1 — Default Grid Per Bucket

| Bucket | Columns | Gutter | Margin |
|---|---|---|---|
| Mobile | 4 | 16 px | 16 px |
| Tablet | 8 | 24 px | 24 px |
| PC | 12 | 24 px | 32 px |
| PC ultra-wide | 12 | 24 px | auto (centered, max 1280–1440 px) |

### B.2 — Container Max-Widths

```
container.max.sm  → 640 px
container.max.md  → 768 px
container.max.lg  → 1024 px
container.max.xl  → 1200 px
container.max.2xl → 1280 px       ← cap content here; do not stretch indefinitely
container.reading-max → 70ch       ← for long-form text, cap at ~70 characters
```

### B.3 — When to use CSS Grid vs. Flexbox

| Case | Tool |
|---|---|
| Page-level layout (sidebar + content + aside) | CSS Grid (named template areas) |
| Card grid that flows | CSS Grid `repeat(auto-fit, minmax(N, 1fr))` |
| Toolbar / row of items aligned | Flexbox |
| List of stacked items | Flexbox column |
| Component that needs to know its own width (not viewport) | Container queries |

---

## Section C — Layout Patterns Per Bucket

### C.1 — Mobile (≤ 639 px)

**Default**: single-column stacked layout.

```
┌─────────────────┐  Top app bar (height: 56–64 px)
├─────────────────┤
│                 │
│    Content      │  Single column
│   (scrollable)  │  Padding: 16 px each side
│                 │
│                 │
├─────────────────┤
│  Bottom nav     │  Height: 56–64 px (when used)
└─────────────────┘
```

Key rules:

- **One primary action per screen** — surface it as a sticky button or FAB.
- **Touch targets ≥ 44×44 px** (iOS HIG) / ≥ 48×48 dp (Material).
- **Reach zone**: bottom 1/3 of the screen is the easy-thumb area; primary actions and nav go there.
- **Drawer / hamburger** menu OK for ≥ 7 destinations; bottom nav better for 3–5.
- **Forms**: one field per row; labels above inputs; full-width buttons; no two-column form layouts.
- **Tables**: convert to cards. Each row → a card with the row's key fields.

Vietnamese-specific: ensure buttons are wide enough for `Xác nhận thanh toán` (~16 chars) without truncation at 320 px width.

### C.2 — Tablet (640–1023 px)

**Default**: 2-column split or expanded single column.

Two viable archetypes:

**Master-detail** (email, file browser, settings):
```
┌──────────┬──────────────────────┐
│ List     │   Detail             │
│ (1/3)    │   (2/3)              │
│          │                      │
│          │                      │
└──────────┴──────────────────────┘
```

**Stacked** (consumer apps, content):
```
┌─────────────────────────────────┐
│  Header                         │
├─────────────────────────────────┤
│  Hero / primary content         │
├─────────────────────────────────┤
│  Card grid (2 columns)          │
└─────────────────────────────────┘
```

Key rules:

- **Side drawer** OK at this size; many apps keep bottom nav for portrait, side rail for landscape.
- **2-column forms** acceptable when fields are clearly grouped.
- **Tables**: usable but compress columns and prioritize 4–6 visible columns; rest behind expand.
- **Tablet landscape (≥ 900 px)** can adopt a near-PC pattern.

### C.3 — PC (≥ 1024 px)

**Default**: sidebar + content (+ optional aside). Density is a feature.

```
┌────┬────────────────────────────────┬─────────┐
│Side│ Top bar (search, user, alerts) │         │
│nav │────────────────────────────────│  Aside  │
│    │                                │ (filters│
│    │   Main content                 │  / info)│
│    │   12-col grid                  │         │
│    │   Multi-pane                   │         │
│    │                                │         │
└────┴────────────────────────────────┴─────────┘
   240–280 px         flex/auto              280–320 px
```

Key rules:

- **Sidebar persistent** at ≥ 1024 px; collapsible at user request.
- **Top bar** holds global search, notifications, user menu.
- **Aside / right panel** for filters, contextual info, activity stream.
- **Content max-width 1280–1440 px** centered; do not span 1920 px content edge-to-edge for reading text.
- **Hover states** are first-class (mouse input).
- **Keyboard shortcuts** documented in the UI (e.g., `cmd/ctrl + K` for command palette).
- **Tables** with full feature set: sort, filter, multi-select, bulk action, sticky header, pagination.

### C.4 — PC ultra-wide (≥ 1920 px)

Two strategies — pick one, document choice:

1. **Cap content** at `container.max.2xl` (1280 px), center it. Sidebar pushed left; right area is gutter.
2. **Multi-pane** layout: sidebar + main content + secondary content side-by-side. Productivity tools (IDEs, dashboards) prefer this.

Never just stretch text columns to 1800 px wide. Reading line length stays at ≤ 70 characters.

---

## Section D — Navigation Patterns Per Bucket

| Bucket | Nav 3–5 destinations | Nav 6+ destinations |
|---|---|---|
| Mobile | bottom nav | drawer (hamburger) |
| Tablet portrait | bottom nav OR left drawer | left drawer (always) |
| Tablet landscape | left rail (icon-only) | left drawer (icon + label) |
| PC | left sidebar (icon + label) | left sidebar with sections |
| PC ultra-wide | left sidebar (icon + label) | left sidebar with sections |

### D.1 — Bottom Nav (Mobile)

- 3–5 items max
- Icon + short label
- Active item visually distinct (filled icon + brand color)
- Persistent across primary screens
- Hides when keyboard opens
- Vietnamese: labels like `Trang chủ`, `Tìm kiếm`, `Đơn hàng`, `Tài khoản` fit; verify ellipsis-free

### D.2 — Drawer / Hamburger (Mobile + Tablet portrait)

- Slide-in from left (or right for RTL)
- Backdrop overlay closes on tap-outside
- Swipe-from-edge to open (mobile)
- Sections grouped if > 7 items
- Account / settings near bottom

### D.3 — Sidebar (PC)

- Persistent, 240–280 px wide (collapsible to ~64 px icon-only rail)
- Logo + product name at top
- Sections with subtle dividers
- Active item: bg highlight + 4 px left accent bar
- Account / settings at bottom

### D.4 — Top Nav (Web marketing surfaces, content sites)

- Use when navigation is shallow (5–8 items)
- Mobile: collapses into hamburger
- Tablet/PC: horizontal items
- Sticky on scroll preferred for product pages

### D.5 — Tabs / Segmented Control (within a screen)

- 2–5 segments work; more = use a dropdown or sidebar
- Underline tabs for content categories
- Pill / segmented tabs for filter switching
- Mobile: scroll horizontally if labels overflow

---

## Section E — Touch Targets & Reach Zones

### E.1 — Touch Target Sizes

| Platform | Minimum |
|---|---|
| iOS (HIG) | 44 × 44 pt |
| Android (Material 3) | 48 × 48 dp |
| Web (WCAG 2.1 AA "Target Size — Enhanced") | 44 × 44 CSS px (recommendation) |
| Web (WCAG 2.2 AA "Target Size — Minimum") | 24 × 24 CSS px (true minimum) |

**Use 44×44 px as the practical floor across platforms.** Smaller targets cause repeat misses, especially on Vietnamese keyboards which are dense with diacritic input.

Spacing between adjacent touch targets: ≥ 8 px to prevent accidental activation.

### E.2 — Reach Zones (Mobile)

On phones held one-handed:

- **Easy zone**: bottom 1/3 of screen — comfortable thumb reach
- **OK zone**: middle 1/3
- **Stretch zone**: top 1/3 — requires hand shift on large phones

Place primary actions in the easy zone (bottom). Place destructive / rare actions out of the easy zone (top-right) to reduce accidental taps.

---

## Section F — Adaptive vs. Responsive vs. Container-Query

### F.1 — Responsive (default)

CSS reacts to viewport width. Same DOM, different layout per breakpoint. Best for content-driven UIs.

```css
.grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); gap: 24px; }
}
```

### F.2 — Adaptive

Different DOM / components per device class. Best when phone and desktop UX are fundamentally different (e.g., a chart that becomes a list on mobile).

```tsx
const isMobile = useMediaQuery("(max-width: 639px)");
return isMobile ? <MobileFlow /> : <DesktopFlow />;
```

Cost: more code paths, more QA. Use only when truly different UX is required.

### F.3 — Container Queries

Component reacts to its **own** width, not the viewport. Best for components reused in different contexts (sidebar, main, modal):

```css
.card-list { container-type: inline-size; }

@container (min-width: 480px) {
  .card-list .card { display: grid; grid-template-columns: 120px 1fr; }
}
```

Use when the same component lives in narrow + wide contexts on the same page.

### F.4 — Decision Rule

- Default to **responsive**.
- Use **container queries** for reusable components in variable contexts.
- Use **adaptive** only when phone + desktop need fundamentally different UX (rare).

---

## Section G — Density Patterns

| Density | Use case | Row height (lists/tables) | Padding |
|---|---|---|---|
| Spacious | Onboarding, marketing, hero | 56–64 px | 24 px |
| Comfortable | Default consumer apps | 40–48 px | 16 px |
| Compact | Productivity tools, data tables | 32–36 px | 8–12 px |

Allow user-adjustable density on data-heavy desktop tools (Linear, Notion both do this).

---

## Section H — Page-Level Layouts (Common Templates)

### H.1 — Dashboard

```
[Sidebar] [Top bar: search + user]
         [KPI cards row — 2 cols mobile, 4 cols PC]
         [Main chart — full width]
         [Activity / table — split or stacked]
```

Mobile: KPIs become a horizontal-scroll carousel; chart full-width; table converts to list-of-cards.

### H.2 — Wizard / Step Flow

```
[Top: progress indicator — N of M]
[Single content area — current step]
[Bottom bar: "Quay lại" | "Tiếp tục"]
```

Mobile: same layout; bottom bar sticky.
Desktop: form fits comfortably in 480–640 px centered column.

### H.3 — Master-Detail

```
[List 1/3] | [Detail 2/3]
```

Mobile: list is the screen; tap item → push detail screen.
Tablet: split view stays.
PC: split view with persistent list.

### H.4 — Form-Heavy

```
[Section header]
[Field group — single column on mobile, 2-col on PC for related fields]
[Sticky bottom bar: Save | Cancel]
```

### H.5 — Bento Grid (Dashboard / Portfolio)

Cards of varying spans (1×1, 2×1, 1×2, 2×2) on a 6-col grid.

```css
.bento {
  display: grid;
  grid-template-columns: repeat(2, 1fr);  /* mobile: 2 col */
  gap: 16px;
}
@media (min-width: 1024px) {
  .bento { grid-template-columns: repeat(6, 1fr); gap: 24px; }
}
.bento .span-2 { grid-column: span 2; }
.bento .span-3 { grid-column: span 3; }
.bento .row-2  { grid-row: span 2; }
```

Mobile: collapse all spans to 1 col or 2 col simple grid; do not try to preserve bento spans on small screens.

### H.6 — Empty Hero / Marketing

```
[Hero: large headline + subhead + 1 CTA + illustration]
[Feature row — 3 cards]
[Social proof / testimonials]
[Footer]
```

Mobile: stacked; illustration above or below text; CTA full-width.

---

## Section I — Responsive Imagery

- Use `srcset` / `<picture>` to serve appropriately sized images per device.
- Default to AVIF or WebP with PNG/JPG fallback.
- Aspect ratio reserved with `aspect-ratio: 16/9` to prevent CLS.
- Hero illustrations: provide a phone-portrait crop, not just shrink desktop hero.

---

## Section J — Verification

For every surface in scope, verify at:

- 320 × 568 px (oldest iPhone SE)
- 360 × 800 px (typical Android)
- 414 × 896 px (iPhone Pro Max)
- 768 × 1024 px (iPad portrait)
- 1024 × 1366 px (iPad landscape)
- 1280 × 800 px (typical laptop)
- 1440 × 900 px (PC wide)
- 1920 × 1080 px (PC ultra-wide)

A surface that passes at 360 px and fails at 320 px is not done.

---

## Required Practices

- Always design mobile-first; PC is a progressive enhancement.
- Always meet ≥ 44×44 px touch targets.
- Always cap reading content at ~70 characters per line.
- Always design Tablet explicitly; never rely on mobile or PC layout alone.
- Always document the navigation pattern per bucket.

## Prohibited Practices

- Do not stretch desktop content edge-to-edge on ultra-wide screens.
- Do not require hover for primary actions; mobile users have no hover.
- Do not place primary actions in the top-right on mobile (out of reach zone).
- Do not introduce a new breakpoint without justifying why three are not enough.
- Do not use the same row height across all densities; that's a missed opportunity.
