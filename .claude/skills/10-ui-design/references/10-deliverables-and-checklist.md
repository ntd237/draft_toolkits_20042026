# Phase 10 — Deliverables & QA Checklist

## Objective

Consolidate every output of Phases 1–9 into a single, predictable Markdown deliverable at the canonical path. Run the QA checklist before sign-off. Produce a short Vietnamese summary in chat.

```
docs/plan/plan_ui_design_<ui-name>_<yyyymmdd>.md
```

The file lives in the **project**, not the toolkit. Create the `docs/ui-design/` directory if it does not exist.

---

## Section A — File Naming

- Format: `ui-design_<yyyymmdd>_<hhmmss>.md`
- Example: `ui-design_20260519_143000.md`
- Use local time at the moment the report is generated.

---

## Section B — Full Deliverable Template

Use this exact structure. Sections may be empty (write "Không có" / "None") but must be present.

```markdown
# UI/UX Design Deliverable — <project name or surface>

- **Generated**: <yyyy-mm-dd hh:mm local>
- **Designer**: ui-ux-design skill (Claude)
- **Surface**: <screen / flow / component / system>
- **Platform class**: <Web | Desktop-shell | Desktop-native | Mobile-iOS | Mobile-Android | Mobile-cross | mixed>
- **Scope**: <files / areas in scope>
- **Out of scope**: <files / areas excluded>

---

## 1. Brief & Goals

### 1.1 Restated Brief
<2–6 câu tiếng Việt: vấn đề, đối tượng, kết quả mong muốn, tiêu chí thành công.>

### 1.2 User Task Statements
- Người dùng X cần làm Y để Z.
- ...

### 1.3 Personas (if any)
<List of 1–3 lightweight personas, or "Không sử dụng personas — đối tượng đã rõ ràng.">

### 1.4 Success Metrics
- <Metric — target, e.g., "Hoàn tất đăng ký < 90 giây trên mobile".>

---

## 2. Stack & Tokens

### 2.1 Stack Snapshot
- Framework: <e.g., React 18 + Next.js 14>
- Style layer: <Tailwind v3 + CSS variables>
- Component library: <existing — extend>
- Icon set: <Lucide>
- Motion: <Framer Motion / native>
- i18n: <next-intl>

### 2.2 Brand Snapshot
- Existing tokens: <yes — at src/styles/tokens.css | no — proposing new>
- Brand colors: <hex / OKLCH>
- Brand voice: <calm/serious/friendly/playful>

### 2.3 Tokens (Primitives + Semantics)

#### 2.3.1 Color (light theme)

| Semantic | Value | Maps to primitive | Light contrast vs. text.primary | WCAG |
|---|---|---|---|---|
| color.bg.canvas       | #F8FAFC | neutral.50  | 16.78 | AAA |
| color.bg.surface      | #FFFFFF | neutral.0   | 18.34 | AAA |
| color.text.primary    | #0F172A | neutral.900 | —     | —   |
| color.text.secondary  | #334155 | neutral.700 | 11.40 | AAA |
| color.action.primary.bg     | #2563EB | brand.600 | 5.18 (vs. white) | AA |
| color.action.primary.fg     | #FFFFFF | neutral.0 | —    | —   |
| color.feedback.danger.bg    | #DC2626 | danger.600 | 4.83 (vs. white) | AA |
| ...                   |         |             |       |     |

#### 2.3.2 Color (dark theme)

| Semantic | Value | Maps to primitive | Dark contrast vs. text.primary | WCAG |
|---|---|---|---|---|
| color.bg.canvas | #020617 | neutral.950 | — | — |
| color.text.primary | #F8FAFC | neutral.50 | 17.92 | AAA |
| ... | | | | |

#### 2.3.3 Type Scale

| Role | Size | Line | Weight | Tracking |
|---|---|---|---|---|
| display    | 60 px | 1.15 | 700 | -0.02em |
| heading.h1 | 48 px | 1.20 | 700 | -0.015em |
| body       | 16 px | 1.60 | 400 | 0 |
| body.sm    | 14 px | 1.55 | 400 | 0 |
| caption    | 12 px | 1.55 | 400 | 0 |

#### 2.3.4 Spacing / Radius / Shadow / Motion / Breakpoints

(Tables omitted in summary — full tables in earlier phases)

### 2.4 Token Export

- Format: <CSS vars / Tailwind config / Flutter ThemeData / SwiftUI / Compose / QSS / XML>
- File path: <src/styles/tokens.css>
- Sample: <link to file or inline snippet>

---

## 3. Vietnamese Typography

### 3.1 Font Selection
- Primary: Be Vietnam Pro (400, 500, 600, 700)
- Mono: JetBrains Mono
- Coverage: full Vietnamese diacritic ranges verified

### 3.2 Loading Strategy
<Google Fonts CDN | self-hosted | next/font | platform native>

### 3.3 Diacritic Test Renderings
- [ ] body 16 px / 400: tone marks ≥ 2 px clearance, dots-below not clipped
- [ ] body 16 px / 700: marks do not blob into letter strokes
- [ ] caption 12 px: `ạ`, `ụ` dots visible
- [ ] heading 48 px: marks align with cap-height
- [ ] mixed Vietnamese + Latin paragraph: no metric jumps

### 3.4 Locale Decisions
- `lang="vi"` set on document root
- Date: dd/MM/yyyy — `Intl.DateTimeFormat("vi-VN")`
- Currency: `1.234.567 ₫` — no decimal places for VND
- Numbers: dot thousands, comma decimal — `Intl.NumberFormat("vi-VN")`
- Sorting: `Intl.Collator("vi", { sensitivity: "base" })`
- No grammatical plural — "3 sản phẩm"

### 3.5 Microcopy Style
- Verb-first action labels: "Đăng nhập", "Xác nhận thanh toán"
- Full forms over abbreviations (no SĐT, MK, TK)
- Errors actionable + specific
- Friendly system voice — not robotic

---

## 4. Responsive Strategy

### 4.1 Breakpoints

| Bucket | Range | Anchor |
|---|---|---|
| Mobile | 320–639 px | design anchor |
| Tablet | 640–1023 px | designed |
| PC | 1024 px+ | designed |
| PC ultra-wide | 1920 px+ | content capped at 1280–1440 px |

### 4.2 Per-Bucket Layout

#### Mobile
- Layout: single column
- Nav: <bottom-nav 4 destinations | drawer>
- Density: comfortable (40 px row height)
- Touch targets: ≥ 44×44 CSS px

#### Tablet
- Layout: <master-detail | stacked>
- Nav: <left rail | drawer>
- Density: comfortable

#### PC
- Layout: <sidebar + content | sidebar + content + aside>
- Sidebar: 240 px
- Content max: 1280 px centered on ultra-wide
- Density: <compact | comfortable>

### 4.3 Adaptive vs. Responsive
- <Responsive default | Container queries on Card grid | Adaptive on Mobile vs. PC for X reason>

---

## 5. Platform Patterns

<Per-class section, only fill those used>

### 5.1 Web
- Routing: <SPA / SSR>
- SEO: <yes / no>
- Form: native HTML5 input types + autocomplete

### 5.2 Desktop (if D-shell or D-native)
- Window chrome: <native title bar / custom>
- Native menus: File / Edit / View / Window / Help (mac), in-window (Windows)
- Keyboard shortcuts: <list>
- System tray: <yes / no>

### 5.3 Mobile (if M-* class)
- iOS conventions: <tab bar / nav stack / sheets / haptics>
- Android conventions: <Material 3 / FAB / snackbar>
- Cross-platform strategy: <adaptive-per-OS / brand-first>

---

## 6. Information Architecture & Flows

### 6.1 Site Map / Screen Map
```
Home
├─ ...
└─ ...
```

### 6.2 Primary User Flows
```
Flow: <name>
[Start] → ... → [End]
   ├── error path: ...
   └── alt path: ...
```

---

## 7. Components

For each component in scope:

### 7.x <Component name>
- **Purpose**: <one line>
- **Anatomy**: <parts>
- **Variants**: <list>
- **Sizes**: <sm/md/lg with heights>
- **States**: default / hover / focus-visible / active / disabled / loading / error / success
- **Tokens used**: <semantic tokens>
- **Responsive rules**: <bucket-specific>
- **A11y**: <role, aria, focus>
- **Vietnamese notes**: <longest-label fits at sm size?>
- **Acceptance criteria**: <list>

---

## 8. Interaction & Motion

### 8.1 Motion Tokens Used
- duration.fast (150 ms): button press, focus ring
- duration.medium (250 ms): modal enter, dropdown expand
- duration.slow (400 ms): page transitions

### 8.2 Micro-Interactions
- <list per component>

### 8.3 Reduced-Motion Strategy
- All transitions > 200 ms have a static fallback
- `prefers-reduced-motion` global guard active
- Per-component fallbacks for skeleton, toast, page transitions

---

## 9. Accessibility (WCAG 2.1 AA)

### 9.1 Contrast Audit
<Pass/fail table per text/background pair, both themes>

### 9.2 Keyboard Map
- Tab / Shift+Tab: focus traversal — verified
- Enter / Space: activate — verified
- Esc: close modal — verified
- Arrow keys: navigation in <listbox / tabs / menu>
- `cmd/ctrl + K`: command palette
- `?`: keyboard shortcuts cheatsheet

### 9.3 Semantic & ARIA Decisions
- <component>: native <element>, role <if any>, aria-* <attrs>

### 9.4 Live Regions
- Toasts: `role="status"` (polite) for info/success, `role="alert"` (assertive) for errors
- Form submit failure: focus moved to first invalid field with summary in `role="alert"`

### 9.5 Language
- `<html lang="vi">` (Web)
- Inline `lang="en"` on foreign fragments
- Native locale: `vi-VN` configured

### 9.6 Notes
- Manual testing with assistive technologies and expert review required for full WCAG compliance verification.

---

## 10. Implementation

### 10.1 Files Created / Modified
- `<path>` — <description>
- ...

### 10.2 Files Out of Scope (Touched-Up Only)
- <none, or list if minimal edits>

### 10.3 Backend / Business Logic
- Not modified (UI scope only).

### 10.4 Open Implementation Questions
- <Question — what answer would change>
- ...

---

## 11. Acceptance Criteria

For each surface in scope, list testable criteria:

- [ ] Renders correctly at 320 px, 360 px, 768 px, 1024 px, 1440 px, 1920 px widths
- [ ] All Vietnamese sample text renders without truncation or diacritic clipping
- [ ] All interactive elements reachable via keyboard
- [ ] Focus-visible distinct from hover; ≥ 3:1 contrast
- [ ] Error / Empty / Loading / Success states implemented
- [ ] Color contrast WCAG 2.1 AA pass on text and meaningful UI
- [ ] `prefers-reduced-motion` respected for all animations
- [ ] `lang="vi"` set on document
- [ ] Touch targets ≥ 44×44 CSS px
- [ ] Date / currency / number formats locale-correct (`vi-VN`)
- [ ] No backend / API contract changed
- [ ] Existing component library extended, not replaced

---

## 12. Statement of Limitations

- Visual rendering verified through static code review; final pixel-perfect verification requires running the app.
- Full WCAG 2.1 AA compliance requires manual assistive-tech testing and expert accessibility review beyond automated checks.
- Performance budgets (LCP, INP, CLS, frame rate) require real-device measurement after build.
- No backend, API, or business-logic files were modified.
- No project content was sent to third-party services.
```

---

## Section C — Conversation Summary Template (Vietnamese)

After the file is written, post a short message in chat. Brief, not detailed — the file is the artifact.

```
Đã hoàn tất thiết kế UI/UX cho: <surface>

Phạm vi:
- Nền tảng: <Web / Desktop / Mobile / hỗn hợp>
- Thiết bị: PC + Tablet + Mobile
- Ngôn ngữ: tiếng Việt (vi-VN)

Đầu ra chính:
- Token system (color/type/space/radius/shadow/motion) — kiểm tra contrast WCAG 2.1 AA
- Font tiếng Việt: Be Vietnam Pro với đầy đủ dấu
- <N> components với đầy đủ states (default/hover/focus/active/disabled/loading/error/success)
- Responsive layouts cho mobile/tablet/PC
- Motion language với prefers-reduced-motion fallback
- <code đã viết / chỉ spec>

Câu hỏi mở:
- <if any>

Báo cáo đầy đủ: [docs/plan/plan_ui_design_<ui-name>_<yyyymmdd>.md](docs/plan/plan_ui_design_<ui-name>_<yyyymmdd>.md)

Lưu ý: Đây là rà soát thiết kế tĩnh; kiểm thử thực tế với người dùng và assistive tech vẫn cần thực hiện trước khi release.
```

---

## Section D — Final QA Checklist

Run before delivery. Every item must be **Pass / N/A** with a one-line note. Anything **Fail** blocks delivery.

### D.1 — Brief & Scope
- [ ] Brief restated and confirmed
- [ ] Platform class confirmed per surface
- [ ] Stack inspected (not assumed)
- [ ] Brand assets inspected (not invented)
- [ ] Scope class declared
- [ ] Non-goals declared

### D.2 — Tokens
- [ ] Two-tier model: primitives + semantics
- [ ] Light theme tokens complete
- [ ] Dark theme tokens complete (or non-goal documented)
- [ ] Every token has a purpose; no dead tokens
- [ ] Token export shape matches the project's stack

### D.3 — Color & Contrast
- [ ] Every text/background semantic pair verified ≥ 4.5:1 (body) or ≥ 3:1 (large)
- [ ] Focus ring contrast ≥ 3:1 vs. background
- [ ] Status conveyed by more than color alone (icon + text)

### D.4 — Vietnamese Typography
- [ ] Font has full Vietnamese diacritic coverage (verified with test string)
- [ ] `vietnamese` subset loaded
- [ ] Body line-height ≥ 1.5
- [ ] Body tracking ≥ 0
- [ ] Diacritic test string renders without clipping at every size
- [ ] `lang="vi"` set on document root
- [ ] Locale formats: dd/MM/yyyy, `1.234.567 ₫`, dot thousands

### D.5 — Responsive
- [ ] Mobile (≤ 639 px) single-column-first
- [ ] Tablet (640–1023 px) explicitly designed
- [ ] PC (≥ 1024 px) explicitly designed
- [ ] PC ultra-wide caps content at 1280–1440 px
- [ ] Touch targets ≥ 44×44 CSS px
- [ ] Long Vietnamese labels fit at smallest button size

### D.6 — Platform Patterns
- [ ] Native menu bar on macOS Desktop (if D-class)
- [ ] iOS conventions on M-iOS
- [ ] Material 3 on M-Android
- [ ] System back gesture/button honored on Mobile
- [ ] Browser shortcuts not hijacked on Web

### D.7 — Components
- [ ] All eight states for every interactive component
- [ ] Empty / Loading / Error / Success states for every data view
- [ ] Components reference tokens, never raw values
- [ ] Loading buttons cannot be re-clicked
- [ ] Icon-only buttons have `aria-label` / `accessibilityLabel`

### D.8 — Motion
- [ ] All animations use transform/opacity (no layout-affecting)
- [ ] Default durations: 150 ms (micro), 250 ms (state), 400 ms (page)
- [ ] `prefers-reduced-motion` fallback for every animation > 200 ms
- [ ] No autoplay carousel / video / parallax without pause control

### D.9 — Accessibility
- [ ] Native HTML / native widgets used; ARIA only where necessary
- [ ] Focus-visible visible and distinct from hover on every focusable element
- [ ] Keyboard reachability verified (mental walk-through or actual test)
- [ ] No `outline: none` without replacement
- [ ] No `tabindex` > 0
- [ ] Heading hierarchy h1 → h2 → h3 unbroken
- [ ] Live regions for dynamic content
- [ ] Image alt text appropriate per image type
- [ ] Forms: every input has a `<label>`, errors via `aria-describedby`

### D.10 — Microcopy
- [ ] Verb-first action labels ("Đăng nhập", "Xác nhận thanh toán")
- [ ] Errors specific and actionable
- [ ] No abbreviations like SĐT / MK / TK
- [ ] No grammatical plurals on Vietnamese nouns
- [ ] Friendly tone, not robotic

### D.11 — Delivery
- [ ] File saved to `docs/plan/plan_ui_design_<ui-name>_<yyyymmdd>.md`
- [ ] All sections of the template filled (or "Không có" / "None")
- [ ] Acceptance criteria are testable, not aspirational
- [ ] Statement of Limitations included
- [ ] Conversation summary in Vietnamese
- [ ] No backend / API / business-logic files modified

### D.12 — If Code Was Written
- [ ] Scope was declared upfront and respected
- [ ] No new component library introduced when one already exists
- [ ] No raw pixel values inside component code
- [ ] Tokens exported in the format the project's stack consumes
- [ ] Accessibility hooks present (`aria-*`, `accessibilityLabel`, `Modifier.semantics`)
- [ ] Existing project conventions matched (file structure, naming, imports)

---

## Required Practices

- Always create `docs/ui-design/` if it does not exist before writing.
- Always include a "Statement of Limitations" section — design verification is not the same as user testing.
- Always link the report path with the relative-path Markdown link form `[path](path)` so the user can click it.
- Always run the full QA checklist before delivery.
- Always summarize, don't dump tool output.

## Prohibited Practices

- Do not write the deliverable outside `docs/ui-design/`.
- Do not omit the Statement of Limitations.
- Do not declare WCAG compliance without manual assistive-tech testing and expert review.
- Do not deliver code without an accompanying token + acceptance-criteria spec.
- Do not write more than one deliverable per design run.
