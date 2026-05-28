# Phase 8 — Accessibility (WCAG 2.1 AA)

## Objective

Apply **WCAG 2.1 Level AA** as the floor across color, contrast, focus, keyboard, semantics, motion, and Vietnamese language attribution. Accessibility is a feature, not a checkbox at the end.

By the end of this phase you must have:

- Verified contrast on every text/background pair
- Focus-visible style per interactive element
- Keyboard map per screen
- Semantic HTML / ARIA / native-accessibility decisions per pattern
- `lang="vi"` / locale strategy
- Reduced-motion + reduced-transparency variants
- Screen-reader announcements for live regions

---

## Section A — The Four POUR Principles (WCAG)

| Principle | Means | Examples |
|---|---|---|
| **Perceivable** | User can sense the content | text alternatives, captions, contrast |
| **Operable** | User can interact with it | keyboard, no time traps, no seizure-inducing flash |
| **Understandable** | User can comprehend it | clear labels, predictable navigation, error help |
| **Robust** | Works across user agents | valid markup, ARIA, future-proof |

---

## Section B — Color & Contrast (WCAG 1.4.3 / 1.4.11)

### B.1 — Contrast Targets

| Use | Min ratio | WCAG criterion |
|---|---|---|
| Body text < 18 pt regular / < 14 pt bold | **4.5 : 1** | 1.4.3 AA |
| Large text ≥ 18 pt regular / ≥ 14 pt bold | **3 : 1** | 1.4.3 AA |
| Non-text UI (icons, focus rings, meaningful borders) | **3 : 1** | 1.4.11 AA |
| Body text (AAA target) | **7 : 1** | 1.4.6 AAA |

Verify every text/background pair from the token table (Phase 2). Document the result.

### B.2 — Color Is Not the Only Channel (WCAG 1.4.1)

State must never be conveyed by color alone.

✅ Required field: red asterisk + label `(bắt buộc)`.
✅ Error input: red border + error icon + error text below.
✅ Required form indicator: not just bold; add a visible marker.

❌ "Click the green button" — do not depend on color name.
❌ Status dot only (red/green/yellow) without a label or icon.

### B.3 — Don't Rely on Hover

Hover-only affordances exclude touch users entirely. Every hover-revealed control must have an alternative path:
- Focus reveals it (via Tab).
- An "always visible on touch" version exists.
- A right-click / long-press menu exposes the action.

---

## Section C — Focus Management (WCAG 2.4.7 / 2.4.11)

### C.1 — Focus Visible (WCAG 2.4.7 AA)

Every focusable element must have a **visible** focus indicator, distinct from hover.

```css
:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
  border-radius: inherit;
}
```

Token-driven version:

```css
:focus-visible {
  outline: var(--focus-ring-width) solid var(--color-border-focus);
  outline-offset: var(--focus-ring-offset);
}
```

Rules:
- Focus ring contrast vs. bg ≥ 3:1.
- Focus ring not obscured by surrounding chrome (offset prevents this).
- Different from hover style (hover often shifts background; focus adds the ring).
- Never `outline: none` without replacement.

### C.2 — Focus Trap (Modals)

When a modal is open:
- Tab cycles within modal contents.
- Shift+Tab cycles in reverse.
- Escape closes and returns focus to the trigger.
- Background scroll is locked; clicks outside don't pass through.

### C.3 — Focus Order

Tab order must follow the visual reading order (top-down, left-to-right for Vietnamese / English).

If absolutely necessary, use `tabindex="0"` (in flow) or skip to specific elements; never use `tabindex` > 0 (creates an unmaintainable parallel order).

### C.4 — Skip Links

Provide a "Skip to main content" link as the first focusable element on each page:

```html
<a href="#main" class="skip-link">Bỏ qua đến nội dung chính</a>
```

Hidden until focused; jumps focus past header/nav directly to main content.

---

## Section D — Keyboard Operation (WCAG 2.1.1 / 2.1.2)

### D.1 — All Interactions Reachable

Every interaction must work with keyboard alone:

- Buttons: Tab to focus + Enter/Space to activate.
- Links: Tab + Enter.
- Form inputs: Tab + type.
- Checkboxes / radios: Tab + Space (radios: arrow keys to change selection within group).
- Dropdowns: Tab + Enter/Space to open + arrows to navigate + Enter to select + Esc to close.
- Modals: Tab cycles + Esc closes.
- Tabs: Tab to tablist + arrow keys to switch tabs.
- Tooltips: visible on focus, not just hover.

### D.2 — No Keyboard Traps (WCAG 2.1.2)

If keyboard focus enters a region (modal, embed, component), it must be able to leave via standard keys (Tab, Esc, Shift+Tab). Test every custom widget for this.

### D.3 — Custom Shortcuts Discoverable

If the app uses custom shortcuts (`cmd/ctrl + K`, `?`, `/` etc.), document them:

- Inline tooltip with shortcut: `Tìm kiếm (Ctrl + K)`.
- A "Phím tắt" / "Keyboard shortcuts" cheatsheet behind `?` key.

Avoid hijacking standard browser shortcuts.

---

## Section E — Semantic Structure (WCAG 1.3.1 / 4.1.2)

### E.1 — Use Native Elements

| Need | Use | Avoid |
|---|---|---|
| Click target | `<button>` | `<div onclick>` |
| Navigation link | `<a href>` | `<button>` (if it changes URL) |
| Header | `<header>` | `<div class="header">` |
| Nav | `<nav>` | `<div class="nav">` |
| Main content | `<main>` | `<div class="main">` |
| Content section | `<section>` | `<div>` |
| Article-like content | `<article>` | `<div>` |
| Footer | `<footer>` | `<div class="footer">` |
| Form | `<form>` | `<div>` |
| Input | `<input>` / `<textarea>` / `<select>` | contenteditable div |
| Heading | `<h1>` … `<h6>` | styled `<div>` |
| List | `<ul>` / `<ol>` / `<li>` | divs |

Native elements come with focus, keyboard, and screen-reader support for free.

### E.2 — Heading Hierarchy

- One `<h1>` per page (or main view).
- Don't skip levels (h2 → h4 — bad).
- Headings describe section content, not act as styling shortcuts.

### E.3 — Landmarks

Every page has `<header>`, `<nav>`, `<main>`, `<aside>` (where applicable), `<footer>`. Screen-reader users navigate by landmark.

### E.4 — ARIA: Last Resort

> The first rule of ARIA is: don't use ARIA.

Reach for ARIA only when native HTML cannot express the pattern. When you do:

- `aria-label` for icon-only buttons.
- `aria-labelledby` to point at a visible text node serving as label.
- `aria-describedby` to attach extra context (help text).
- `aria-expanded`, `aria-haspopup`, `aria-controls` for disclosure widgets.
- `aria-live` (`polite` or `assertive`) for dynamic regions.
- `role="dialog"` + `aria-modal="true"` for modals.
- `aria-current="page"` on the active nav item.

Never assign a role that contradicts the element's native semantics (`<button role="link">` — wrong; use `<a>`).

### E.5 — Form Semantics

```html
<label for="email">Email <span aria-hidden="true" class="req">*</span></label>
<input
  id="email" type="email" required
  aria-describedby="email-help email-error"
  aria-invalid="false"
>
<p id="email-help" class="help">Nhập email bạn dùng để đăng ký.</p>
<p id="email-error" class="error" hidden>Email này không tồn tại trong hệ thống.</p>
```

When validation fails, set `aria-invalid="true"` and show the error text via `aria-describedby`.

### E.6 — Image Alt Text

- Decorative image: `alt=""` (empty, not omitted).
- Functional image (icon button): describe the action: `alt="Xoá đơn hàng"`.
- Content image: describe what the image shows: `alt="Biểu đồ tăng trưởng doanh thu Q1 2026"`.
- Complex images (charts): provide a long description nearby or via `aria-describedby` linking to a paragraph.

---

## Section F — Live Regions & Dynamic Content (WCAG 4.1.3)

### F.1 — Announcing Changes

When content changes without a page reload, screen readers don't know unless told:

```html
<!-- Polite announcement (waits for SR pause) -->
<div role="status" aria-live="polite">
  Đã lưu thay đổi.
</div>

<!-- Assertive (interrupts) — use sparingly, only for critical errors -->
<div role="alert">
  Không thể kết nối đến máy chủ.
</div>
```

### F.2 — Status / Toast Patterns

- Success / info toasts: `role="status"` (polite).
- Error toasts: `role="alert"` (assertive) — interrupts SR.
- Loading / busy: `aria-busy="true"` on the parent container.

### F.3 — Form Submission Errors

After submit failure:
- Move focus to a summary banner OR to the first invalid field.
- Banner: `role="alert"` with the error count + first 3 errors listed.
- Each invalid field gets `aria-invalid="true"` + error text via `aria-describedby`.

---

## Section G — Touch Target Size (WCAG 2.5.5 / 2.5.8)

| Spec | Min |
|---|---|
| WCAG 2.1 AAA Target Size — Enhanced | 44 × 44 CSS px |
| WCAG 2.2 AA Target Size — Minimum | 24 × 24 CSS px |
| iOS HIG | 44 × 44 pt |
| Material Design | 48 × 48 dp |

Use **44 × 44 px** as the practical floor. Spacing between adjacent targets ≥ 8 px.

---

## Section H — Forms Specific

### H.1 — Required Fields

- Mark required visually (asterisk + "(bắt buộc)" or label both clearly).
- HTML `required` attribute or framework equivalent.
- If both required and optional fields exist, mark only one consistently (don't mix).

### H.2 — Error Messages

- Inline beneath each field, not in a top-only banner.
- Specific and actionable (`Mật khẩu phải có ít nhất 8 ký tự` not `Lỗi nhập`).
- Persist until corrected; don't disappear on focus-out.

### H.3 — Autocomplete

```html
<input autocomplete="email" type="email">
<input autocomplete="current-password" type="password">
<input autocomplete="new-password" type="password">
<input autocomplete="one-time-code" inputmode="numeric">
<input autocomplete="postal-code">
<input autocomplete="address-line1">
```

Improves form fill speed and reduces input errors.

---

## Section I — Vietnamese Language Attribution

### I.1 — Web

```html
<html lang="vi">
```

For inline foreign content:
```html
<p>Bạn có thể đọc thêm trong tài liệu <span lang="en">"Quick Start Guide"</span>.</p>
```

Screen readers switch voice/pronunciation profile based on `lang`. Without `lang="vi"`, English-pronouncing voices butcher Vietnamese.

### I.2 — Native

- iOS: declare `vi-VN` as supported localization in `Info.plist`.
- Android: provide `res/values-vi/strings.xml`.
- Flutter: `supportedLocales: [Locale('vi', 'VN')]` + `localizationsDelegates`.

---

## Section J — Reduced-Motion / Reduced-Transparency

### J.1 — Reduced Motion (already in Phase 7)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### J.2 — Reduced Transparency (macOS, iOS)

For glassmorphism / transparency effects, provide an opaque fallback:

```css
.glass {
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.6);
}

@media (prefers-reduced-transparency: reduce) {
  .glass {
    backdrop-filter: none;
    background: var(--color-bg-surface);
  }
}
```

---

## Section K — Native Platform Accessibility

### K.1 — iOS / SwiftUI

- VoiceOver: every interactive view has `accessibilityLabel`, `accessibilityHint`, `accessibilityValue`.
- Dynamic Type: support text size scaling up to "Accessibility Sizes" tier.
- High-contrast mode: design alternate colors via `Color(.systemBackground)` + Asset Catalog appearances.
- Button shapes: tappable areas remain 44 × 44 pt.

### K.2 — Android / Compose

- `Modifier.semantics { contentDescription = "Xoá" }` on icon-only buttons.
- `TalkBack` testing pass.
- Support `fontScale` up to 200%.
- Use `Modifier.minimumInteractiveComponentSize()` to enforce 48 dp.

### K.3 — Desktop

- Native widgets carry their accessibility tree automatically; custom paint widgets must implement `QAccessible` (PyQt5) / `AutomationProperties` (WPF).
- Keyboard shortcuts visible in menu items.
- High-contrast theme support (Windows).

---

## Section L — Testing Approach

Cannot replace human testing, but automate what you can:

| Tool | Purpose |
|---|---|
| `axe DevTools` (browser ext) | Catches ~57% of WCAG violations |
| Lighthouse (Chrome) | Accessibility audit score |
| `eslint-plugin-jsx-a11y` | Catch issues at lint time (React) |
| `vue-axe` | Vue equivalent |
| `pa11y` | CLI batch testing |
| Storybook a11y addon | Component-level checks |
| Manual screen reader test | NVDA (Windows free), VoiceOver (mac), TalkBack (Android) |
| Manual keyboard test | unplug mouse for 30 minutes |

For full validation: WCAG compliance requires **manual testing with assistive technologies** and expert review. Automated tools find roughly half the issues.

---

## Section M — A11y Statement Template

For public products, include an accessibility statement page:

```
Cam kết về khả năng tiếp cận

[Tên sản phẩm] tuân thủ Hướng dẫn Tiếp cận Nội dung Web (WCAG) phiên bản 2.1 mức AA.
Chúng tôi liên tục cải tiến trải nghiệm cho mọi người dùng, bao gồm người dùng
sử dụng công nghệ trợ giúp.

Nếu bạn gặp khó khăn khi sử dụng sản phẩm, xin vui lòng liên hệ:
- Email: a11y@example.com
- Phản hồi: <link>

Cập nhật lần cuối: <date>.
```

---

## Required Practices

- Always use native HTML/native widgets first; reach for ARIA / custom only when necessary.
- Always provide a visible focus-visible style with ≥ 3:1 contrast.
- Always verify color contrast for every text/background pair.
- Always set `lang="vi"` (Web) or platform-equivalent locale (native).
- Always provide alternative paths for hover-only affordances.
- Always test with keyboard alone before sign-off.
- Always announce dynamic state changes via live regions or platform equivalents.

## Prohibited Practices

- Do not use `outline: none` without a replacement focus style.
- Do not rely on color alone to convey meaning.
- Do not rely on hover for primary affordances.
- Do not use `tabindex` > 0.
- Do not skip heading levels (h1 → h3).
- Do not autoplay video or carousel without pause control.
- Do not use animations that ignore reduced-motion.
- Do not declare WCAG compliance without manual assistive-tech testing.
