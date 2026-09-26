# Responsive Breakpoints & Adaptive Layout Matrix

Technical standards for viewport breakpoints, fluid column grids, and adaptive layout transitions spanning Mobile, Tablet, PC, and Ultrawide displays.

---

## 1. Standard Breakpoint System

| Breakpoint | Viewport Range | Target Devices | Grid Columns | Gutter / Margin |
| :--- | :--- | :--- | :--- | :--- |
| **Mobile (xs/sm)** | `< 768px` (360px - 767px) | iPhone, Android phones (Portrait) | 4 columns | 16px |
| **Tablet (md)** | `768px - 1024px` | iPad, Galaxy Tab, Mobile (Landscape) | 8 columns | 24px |
| **Desktop (lg/xl)**| `1024px - 1920px`| Laptops, Workstation Monitors | 12 columns | 32px (Max width: 1280px-1440px) |
| **Ultrawide (2xl)**| `> 1920px` (2560px, 3440px) | Ultrawide, Curved Displays | 12 / 16 columns | Centered max-width container |

---

## 2. Adaptive Layout Transitions

```
[Mobile < 768px]            [Tablet 768px - 1024px]             [Desktop > 1024px]
┌──────────────┐            ┌────────┬─────────────┐            ┌──────┬────────┬─────────────┐
│ Header (Logo)│            │ Rail   │ Header      │            │ Side │ Header │ Top Actions │
├──────────────┤            │ ┌────┐ ├─────────────┤            │ bar  ├────────┴─────────────┤
│ 1-Col Stack  │            │ │ 🏠 │ │ Master-     │            │ ┌──┐ │ 3-Col Data Grid     │
│ Card 1       │   ───→     │ │ 📂 │ │ Detail      │   ───→     │ │  │ │ ┌───┐ ┌───┐ ┌───┐   │
│ Card 2       │            │ │ 👤 │ │ (2 Columns) │            │ │  │ │ │ 1 │ │ 2 │ │ 3 │   │
├──────────────┤            │ └────┘ │             │            │ └──┘ │ └───┘ └───┘ └───┘   │
│ Bottom Nav   │            └────────┴─────────────┘            └──────┴─────────────────────┘
└──────────────┘
```

### 2.1. Navigation Architecture Shifts
- **Mobile (<768px)**: Fixed **Bottom Navigation Bar** (3–5 quick actions) pinned to viewport bottom. Secondary links tucked into a slide-over **Drawer Menu**.
- **Tablet (768px - 1024px)**: Bottom Navigation converts into a left-aligned **Navigation Rail** (slim 64-72px vertical icon bar).
- **Desktop (>1024px)**: Expands into a full **Persistent Sidebar** (240-280px width) displaying both icons and labels, optionally collapsible.

### 2.2. Content Layout Adaptations
- **Mobile**: Single-column vertical stack. Cards stretch across 100% width minus margins. Tabular data transforms into vertical card lists.
- **Tablet**: 2-Column Split View (Master-Detail). Record list on the left, active item detail on the right.
- **Desktop**: Multi-column grids (3-4 columns). Dense data tables display all columns with inline sorting, filtering, and bulk actions.

---

## 3. Container Queries & Modular Components

When components are embedded across variable parent widths, use Container Queries rather than viewport media queries:
```css
@container (max-width: 400px) {
  .product-card {
    flex-direction: column;
  }
}
@container (min-width: 401px) {
  .product-card {
    flex-direction: row;
  }
}
```
*Rule*: Decouple widget responsiveness from global browser window dimensions wherever possible.
