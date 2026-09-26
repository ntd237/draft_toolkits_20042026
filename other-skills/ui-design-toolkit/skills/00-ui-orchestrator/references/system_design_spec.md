# [Product Name] — System Design Specification (system_design.md)

Standardized specification artifact for frontend engineers, designers, and AI coding assistants to implement the interface without inventing missing fundamentals.

---

## 1. Product & Platform Context

- **Product Category**: [SaaS / Admin Dashboard / E-commerce / Mobile Utility / Desktop Tool / Game HUD / Web App / ...]
- **Target Platform(s)**: [Web App / Mobile App / Desktop App / Desktop Game / Mobile Game]
- **Responsive Scope**: [Mobile (<768px), Tablet (768-1024px), PC (>1024px), Ultrawide (>1920px)]
- **Visual Direction (Design Posture)**: [Clean & Modern / Enterprise Dense / Cyberpunk High-contrast / Playful / ...]
- **Primary Language**: Vietnamese (mandatory diacritics support, unclipped accent marks, dynamic text expansion).

---

## 2. UX Architecture & User Flows

### 2.1. Information Architecture & Navigation (IA Sitemap)
```
[Home / Dashboard]
  ├── [Primary Branch 1] → [Detail View / Action Flow]
  ├── [Primary Branch 2] → [List / Table View] → [Create Modal]
  └── [Settings / Profile]
```

### 2.2. Critical Task Flow & Error Handling
| Step | User Action | System Response | Error State & Recovery Path |
| :--- | :--- | :--- | :--- |
| **1. Trigger** | Click "Get Started" | Open input modal/form | Offline / Session expired: Show inline re-auth modal without losing context |
| **2. Input** | Enter required fields | Validate inline on blur | Invalid format: Highlight input border in red + contextual helper message |
| **3. Submit** | Click "Confirm" | Show spinner on button | Server failure: Retain form values + Toast notification with "Retry" action |

---

## 3. Design Tokens Specification

### 3.1. 60-30-10 Color System & Contrast Mapping
- **60% Dominant Neutral (Backgrounds & Structural Surfaces)**:
  - Light Theme: Surface `#FFFFFF`, App Background `#F8FAFC`, Border `#E2E8F0`
  - Dark Theme: Surface `#0F172A`, App Background `#020617`, Border `#1E293B`
- **30% Secondary (Typography & Grouping Dividers)**:
  - Text Primary: Light `#0F172A` / Dark `#F8FAFC` (Contrast ratio >= 12:1)
  - Text Secondary: Light `#475569` / Dark `#94A3B8` (Contrast ratio >= 5.5:1)
- **10% Accent (Primary Actions & Interactive Elements)**:
  - Brand Primary: `#2563EB` (Blue 600) | Hover: `#1D4ED8` | Active: `#1E40AF`
  - Feedback: Success `#16A34A`, Warning `#D97706`, Error `#DC2626`

### 3.2. Vietnamese Typography System
- **Font Stack**: `Be Vietnam Pro, Inter, system-ui, -apple-system, sans-serif`
- **Line-Height Standard**: Mandatory **1.4 to 1.6** for body and labels to eliminate diacritics clipping (huyền, sắc, hỏi, ngã, nặng, mũ ă, â, ê, ô, ơ, ư).
- **Type Scale**:
  - Display: `32px / line-height: 44px / font-weight: 700`
  - H1 / Title: `24px / line-height: 34px / font-weight: 600`
  - H2 / Subtitle: `18px / line-height: 26px / font-weight: 600`
  - Body (Default): `14px / line-height: 22px / font-weight: 400`
  - Caption / Small: `12px / line-height: 18px / font-weight: 500`

### 3.3. Spacing, Radius & Elevation
- **Spacing Grid (8px/4px base)**: `4px, 8px, 12px, 16px, 24px, 32px, 48px`
- **Border Radius**: `sm: 4px, md: 8px, lg: 12px, full: 9999px`
- **Elevation Shadows**: `sm (cards), md (dropdown/popover), lg (modals/dialogs)`

---

## 4. Component Specifications & State Matrix

Every interactive component must explicitly define all 6 states:

| Component | Default | Hover | Active / Pressed | Focus-visible | Disabled | Loading / Error |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Button** | Brand BG, White text | Darken 10% | Scale 0.98 | 2px Brand outline | 50% Opacity, not-allowed | Spinner icon, click locked |
| **Text Input** | Neutral border, Primary text | Subtle border highlight | Brand border | 2px Brand outline | Gray background | Red border + error text beneath |
| **Card Item** | Surface BG, Subtle border | Slight shadow + -2px Y | Flat shadow | 2px outline | Grayscale content | Shimmer skeleton placeholder |

- **Target Sizing**:
  - Touch surfaces (Mobile/Tablet/Touch Game): Minimum **44x44px** (iOS) / **48x48dp** (Android).
  - Pointer/Mouse (Desktop/Web): Minimum **32x32px**.

---

## 5. Responsive Layout & Platform Adaptation

### 5.1. Responsive Layout Matrix (Mobile, Tablet, PC)
- **Mobile (<768px)**: Single-column stack, persistent bottom navigation, drawer menu for secondary links, collapsed table cards.
- **Tablet (768px - 1024px)**: 2-Column layout (Master-detail), bottom navigation converts to left Navigation Rail.
- **PC (>1024px)**: Multi-column grid, persistent sidebar (240-280px), dense data tables with direct sort/filter.

### 5.2. Platform Recipes
- **Web App**: Keyboard navigation shortcuts (`Cmd/Ctrl+K`), sticky table headers, breadcrumb trail.
- **Mobile App**: Thumb-zone ergonomics, safe area insets (notch/dynamic island/home bar), modal bottom sheets.
- **Desktop App**: Custom titlebar window chrome, right-click context menus, system tray, DPI scaling support.
- **Game Desktop**: 4-Corner HUD safe zones, controller D-pad focus ring, high-contrast menus, 16:9 & 21:9 ultrawide scaling.
- **Game Mobile**: Dual thumb touch zones, large semi-transparent action buttons, haptic triggers, safe offset from bevels.

---

## 6. QA & Accessibility Sign-off

- [ ] **Color Contrast (WCAG 2.2 AA)**: Minimum 4.5:1 for regular text, 3:1 for large text and UI components.
- [ ] **Keyboard / Controller Navigation**: Clear focus ring on every interactive component, no keyboard traps.
- [ ] **Vietnamese Typography Protection**: All diacritics unclipped; labels accommodate +30% string expansion without overflow.
- [ ] **Error Prevention & Recovery**: Destructive actions protected by confirmation modals; clear error messaging with recovery buttons.
