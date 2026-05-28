# Phase 1 — Discovery & Requirements

## Objective

Understand the brief, the user, the project, the platform class(es), and the constraints. No design without context. By the end of this phase you must have a confirmed brief, a stack snapshot, a brand snapshot, a platform-class assignment, an information architecture, and at least one user-flow diagram for the primary task.

---

## Step 1.1 — Restate the Brief

Before reading anything else, restate the user's request and confirm. Use this template:

```
Tôi hiểu yêu cầu là:
- Nền tảng: Web / Desktop / Mobile / hỗn hợp <chọn>
- Phạm vi UI: <trang / flow / component / redesign / new build>
- Mục tiêu người dùng: <task chính họ cần hoàn thành>
- Đối tượng chính: <persona / user type>
- Thiết bị mục tiêu: PC + Tablet + Mobile (mặc định) hoặc <khác>
- Ngôn ngữ: tiếng Việt là ngôn ngữ chính (mặc định) hoặc <khác>
- Đầu ra mong muốn: spec thiết kế + code, hoặc chỉ spec, hoặc chỉ code

Tôi sẽ làm việc ở chế độ UI-only — không sửa backend, không thay đổi API, business rule, hoặc database schema.

Có gì cần điều chỉnh trước khi tôi bắt đầu?
```

Wait for confirmation. Do not proceed until the brief is locked.

---

## Step 1.2 — Inspect the Project

Read first, recommend later.

### Stack signals (`package.json`, `pyproject.toml`, `pubspec.yaml`, `*.csproj`, `Cargo.toml`)

| Signal | Platform class | Implication |
|---|---|---|
| `react`, `next`, `remix`, `vite` | W | React-based web |
| `vue`, `nuxt` | W | Vue-based web |
| `svelte`, `sveltekit`, `solid`, `astro`, `qwik` | W | Other web frameworks |
| `electron`, `tauri`, `wails` | D (web-shell) | Web stack rendered as native window |
| `pyqt5`, `pyside6`, `pyqt6` | D (native) | Qt-based desktop |
| `flutter`, `flutter_*` | M, D (Flutter Desktop) | Cross-platform Flutter |
| `react-native`, `@react-native/*` | M | RN cross-platform |
| `swift`, `swiftui`, `*.xcodeproj` | M (iOS), D (macOS) | Apple native |
| `compose`, `androidx.compose.*` | M (Android) | Jetpack Compose |
| `wpf`, `winui`, `maui`, `xamarin` | D, M | .NET UI |
| `gradio`, `streamlit` | W (lightweight) | Python data UI |
| `tailwindcss`, `tailwind.config.*` | W | Tokens go in the config |
| `@emotion`, `styled-components`, `vanilla-extract`, `panda-css` | W | CSS-in-JS layer |
| `@mui/*`, `@chakra-ui/*`, `antd`, `@radix-ui/*`, `shadcn/ui` | W | Existing component library |
| `lucide`, `@heroicons/*`, `phosphor-react`, `iconify`, `material-symbols` | any | Existing icon system |
| `framer-motion`, `motion`, `auto-animate` | W | Existing motion library |
| `i18next`, `next-intl`, `react-intl`, `vue-i18n`, `flutter_localizations` | any | i18n already wired |
| `zod`, `yup`, `valibot`, `react-hook-form`, `formik` | W | Form/validation choice |

### Native platform signals

- iOS: `Info.plist`, `Assets.xcassets`, SwiftUI files, `*.xcodeproj`
- Android: `AndroidManifest.xml`, `res/values/themes.xml`, `res/values/colors.xml`, Compose files
- macOS: `*.xcodeproj` with macOS deployment target
- Windows WPF: `App.xaml`, `*.csproj` with `<UseWPF>true</UseWPF>`
- Linux GTK / Qt: `*.ui` files, glade files

### Style layer signals

`tailwind.config.*`, `postcss.config.*`, `:root { --… }` blocks, `theme.ts/js`, `tokens.*` files, design-tokens JSON, Storybook config, Flutter `ThemeData`, native `Color+Theme.swift` extensions, Android `colors.xml`, PyQt5 `*.qss` stylesheets.

### Brand signals

- `public/`, `static/`, `assets/`, `Assets.xcassets/`, `app/src/main/res/drawable/` — logos, illustrations, font files
- `*.svg` named like `logo*`
- `README.md` or `BRAND.md` with brand notes
- A Storybook story labeled "Foundations" / "Tokens" / "Brand"

### Typography signals

- `<link rel="stylesheet" href="https://fonts.googleapis.com/...">` in HTML head
- `next/font` imports
- Self-hosted font files in `public/fonts/`, `assets/fonts/`, `Resources/Fonts/`, `fonts/` (Flutter)
- `@font-face` declarations
- `font-family` token already declared

If a font is already loaded, **do not** introduce a new one without asking. Extend what exists.

### Existing components inventory

Enumerate `src/components/**`, `src/ui/**`, `src/design-system/**`, `packages/ui/**`, `lib/widgets/**` (Flutter), `app/src/main/java/**/ui/**` (Android), Swift `*View.swift` files. For each existing primitive (Button, Input, Card, Modal, etc.), record:

- Its API (props/parameters)
- Its variants/sizes
- Whether it has all states (default / hover / focus-visible / active / disabled / loading / error / success)
- Whether it is accessible

This becomes your component inventory in Phase 6.

---

## Step 1.3 — Classify the Scope

| Class | Examples | Implication |
|---|---|---|
| **New screen** | Add a checkout page | Reuse existing tokens + components; add only what is missing |
| **New component** | Add a date-range picker | Add to component library; document API + states |
| **Redesign** | Refresh dashboard layout | Diff old vs. new; keep tokens stable unless redesigning system |
| **System foundation** | Set up tokens + base components | Largest scope; produce design system before screens |
| **Responsive fix** | Make settings page work on mobile | Layout-focused; minimal token changes |
| **Cross-platform port** | Port a web flow to mobile native | Re-design for platform conventions, not just resize |
| **A11y fix** | Make form keyboard-navigable | Targeted; no visual redesign unless required |
| **Polish pass** | Improve micro-interactions, empty states, copy | Surgical; do not redesign IA |

Each class has a different deliverable shape; do not over-deliver beyond the class.

---

## Step 1.4 — Assign Platform Class

Each surface in scope gets a class assignment:

- **W (Web)** — runs in a browser, follows web conventions, supports keyboard + mouse + touch
- **D (Desktop)** — runs as a native window with menu bar / system tray / multi-window
  - **D-shell** (Electron, Tauri): Web stack rendered native; follow Web conventions but add desktop affordances
  - **D-native** (PyQt5, WPF, JavaFX, Cocoa): Native widgets; follow OS HIG
- **M (Mobile)** — runs as a phone/tablet app
  - **M-native iOS**: SwiftUI/UIKit; follow Apple HIG
  - **M-native Android**: Jetpack Compose / View; follow Material 3
  - **M-cross-platform**: Flutter / RN / MAUI; pick platform-adaptive widgets

Hybrid is allowed: e.g., "primary surface is W, but a Tauri-wrapped desktop view is also in scope." Note both.

---

## Step 1.5 — Information Architecture

For surfaces beyond a single component, produce an IA artifact.

### IA recipe

1. **Site map / screen map** — every screen reachable in the in-scope flows
2. **Navigation model** — primary nav (4–7 destinations), secondary nav (per area), utility nav (account, settings, search)
3. **Content model** — for data-heavy surfaces, sketch the entity-relationship: Order has Items; Item has Variants; etc.
4. **Permissions overlay** — which roles see which destinations

### IA presentation

```
Home
├─ Dashboard
├─ Orders
│  ├─ All orders
│  ├─ Pending
│  └─ Disputes
├─ Customers
│  ├─ All customers
│  └─ Segments
├─ Products
│  ├─ Catalog
│  ├─ Inventory
│  └─ Pricing
└─ Settings
   ├─ Profile
   ├─ Team
   ├─ Billing
   └─ Integrations
```

Surface only the destinations that exist in scope; do not invent IA the project does not have.

---

## Step 1.6 — User Flows

For each primary user task, produce a flow showing happy path + at least two off-path branches (error, alternative entry).

### Flow notation (text-friendly)

```
Flow: First-time signup with email

  [Landing] → click "Tạo tài khoản"
     ↓
  [Signup form]
     ├── invalid email → inline error → stay
     ├── email exists  → "Email này đã được sử dụng" + link "Đăng nhập" → can recover
     └── valid submit ↓
  [Verify email screen] (token sent)
     ├── token expired → resend → loop
     └── token valid ↓
  [Onboarding step 1: Profile]
     └── skip allowed → dashboard with banner
  [Onboarding step 2: Preferences]
  [Dashboard — first-run state]
```

For complex apps, include flows for: signup, login, password reset, primary task (the one the product is about), edit-an-existing-item, delete-an-existing-item, settings change, error recovery.

---

## Step 1.7 — User Personas (Optional but Useful)

When the audience is not obvious, sketch 1–3 personas. Keep them lightweight and relevant.

```
Persona: Linh — Mobile-first shopper
- Vai trò: khách hàng mua lại
- Thiết bị chính: Android mid-range, 360×800 viewport
- Bối cảnh sử dụng: di chuyển, mạng 4G yếu, một tay
- Mục tiêu: tìm và mua lại đơn cũ trong < 60 giây
- Khó khăn hiện tại: phải đăng nhập lại nhiều lần, lịch sử đơn khó tìm
```

Personas drive density, copy tone, error handling. If the user did not provide personas and the audience is clear, skip this step and document the assumption.

---

## Step 1.8 — Confirm Device Matrix

Default targets:

| Bucket | Range | Web | Desktop | Mobile |
|---|---|---|---|---|
| Mobile portrait | 320–428 px | ✓ | – | ✓ |
| Mobile landscape | 568–926 px | ✓ | – | ✓ |
| Tablet portrait | 600–834 px | ✓ | (rare) | ✓ |
| Tablet landscape | 1024–1366 px | ✓ | (rare) | ✓ |
| Laptop / PC | 1280–1439 px | ✓ | ✓ | – |
| PC wide | 1440–1919 px | ✓ | ✓ | – |
| PC ultra-wide | 1920 px+ | ✓ | ✓ | – |

Ask the user:

- Which buckets are required vs. nice-to-have?
- Minimum-supported devices? (e.g., iPhone SE 1st gen at 320 px, 5-year-old Android at 360 px)
- Offline / low-bandwidth constraints?
- Dark mode required?
- Multi-window or split-screen support? (Desktop, iPad)

Record answers — they drive Phase 4 (responsive strategy) and Phase 5 (platform patterns).

---

## Step 1.9 — Confirm Language Strategy

Vietnamese-first is the default per project rules. Confirm:

- Is the UI Vietnamese-only?
- Or multi-language (vi-VN + en-US, or more)?
- If multi-language: longest expected label per element type?
- i18n library already in use? (do not introduce a new one)
- Right-to-left support needed? (rare for Vietnamese projects, but ask if Arabic/Hebrew is in scope)

---

## Step 1.10 — Constraints & Non-Goals

Surface constraints early:

- **Performance budget** (Web): LCP < 2.5s, INP < 200ms, JS bundle < 200KB gzip on mobile, CLS < 0.1
- **Performance budget** (Native): cold-start ≤ 2s, frame rate 60 fps
- **Browser support**: last 2 Chrome/Edge/Firefox/Safari, or include older
- **OS support**: iOS 15+, Android 8+, Windows 10+, macOS 12+, Ubuntu 22.04+
- **Compliance**: WCAG 2.1 AA, AAA, EN 301 549, ADA, GDPR cookie banners
- **Visual constraints**: must match marketing brand book, must not change global navigation
- **Time / scope cap**

Explicit **non-goals**:

```
Non-goals for this design:
- Not redesigning the global navigation
- Not changing the data model
- Not introducing a new UI library
- Not adding new pages outside the requested flow
```

---

## Step 1.11 — Capture Open Questions

Do not silently assume. List open questions:

```
Open Questions:
1. <Question — what the answer would change>
2. <Question — what the answer would change>
```

If a question is **blocking**, ask before Phase 2. If **non-blocking**, document the assumption and continue.

---

## Deliverables

By the end of Phase 1, you must have:

- Confirmed brief restatement
- Stack snapshot (framework, styling, components, icons, motion, i18n)
- Brand snapshot (existing tokens, fonts, colors, logos)
- Scope class
- Platform-class assignment per surface (W / D-shell / D-native / M-iOS / M-Android / M-cross)
- User task statements per surface
- IA artifact (site map / screen map)
- User flow for at least the primary task
- Confirmed device matrix
- Language decision
- Constraints & non-goals
- Open-questions list

These feed every subsequent phase. Do not start Phase 2 without all of them.

---

## Required Practices

- Always restate the brief and confirm before designing.
- Always read the project before suggesting a stack or library.
- Always assign a platform class per surface.
- Always produce an IA artifact for any scope larger than a single component.
- Always declare non-goals; they protect scope from drift.

## Prohibited Practices

- Do not assume the stack from filename heuristics alone — confirm via imports/configs.
- Do not introduce new libraries when the project already has equivalents.
- Do not skip the device-matrix and language-strategy questions.
- Do not start a "complete redesign" when the user asked for a targeted change.
- Do not invent personas when the user has provided clear audience info.
