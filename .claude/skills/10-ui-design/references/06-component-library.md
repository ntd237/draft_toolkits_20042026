# Phase 6 — Component Library

## Objective

Specify the reusable components — full anatomy, variants, sizes, **all states**, responsive rules, accessibility hooks. Each component references **tokens only**, never raw values.

A component is "done" only when it can be dropped into any screen, in any density, in any theme, and behave correctly.

---

## Section A — Component Inventory

A reasonable starter inventory. Mark which ones the project already has during Phase 1; only design the missing ones, or specify changes for existing ones.

### Inputs
- Button (primary / secondary / tertiary / ghost / destructive / icon-only)
- IconButton
- TextField (single-line)
- Textarea
- Number input
- Search field
- Select / Dropdown
- Combobox / Autocomplete
- Multi-select / Tag input
- Checkbox
- Radio group
- Switch / Toggle
- Slider
- Date picker
- Time picker
- File upload / Dropzone
- Color picker
- Rich text editor (when needed)

### Containers
- Card
- Panel
- Section / Box
- Divider
- Accordion / Collapsible
- Tabs
- Stepper / Wizard
- Bento item

### Overlays
- Modal / Dialog
- Drawer / Side panel
- Bottom sheet (mobile)
- Popover
- Tooltip
- Menu / Context menu
- Toast / Snackbar
- Banner / Alert
- Inline notification

### Navigation
- App bar / Top bar
- Side nav / Sidebar
- Bottom nav
- Breadcrumb
- Pagination
- Tabs (already in Containers; nav-purpose subset)
- Segmented control
- Command palette

### Data
- Table (sortable, filterable, paginatable, selectable)
- List (simple, with leading/trailing, with description)
- DataGrid (advanced: virtualized, editable cells)
- Tree
- Calendar / Date grid
- Timeline
- Chart wrapper (delegate rendering to charts lib)

### Feedback
- Alert
- Toast
- Spinner
- Progress bar (linear, circular, indeterminate)
- Skeleton loader
- Empty state
- Error state
- Success state
- Onboarding tooltip / coach mark

### Display
- Avatar (single, group)
- Badge / Chip / Tag
- KBD (keyboard shortcut display)
- Code block
- Stat / Metric card
- Image with placeholder
- Icon

---

## Section B — Component Spec Template

Use this template per component:

```
### Component Name

**Purpose**: One-line description of when to use this.

**Anatomy** (parts):
- Container
- Leading slot (icon)
- Label
- Trailing slot (icon, badge, kbd)

**Variants**: primary, secondary, tertiary, ghost, destructive
**Sizes**: sm (32 px), md (40 px), lg (48 px) — minimum touch target on mobile

**States**:
- default
- hover (mouse only)
- focus-visible (keyboard)
- active / pressed
- disabled
- loading
- readonly (where applicable)
- error
- success

**Tokens used**:
- bg: color.action.primary.bg
- bg-hover: color.action.primary.bg.hover
- fg: color.action.primary.fg
- radius: radius.button
- font: typography.button
- focus-ring: 2px solid color.border.focus, offset 2px

**Responsive rules**:
- Mobile: full-width by default in form contexts; min-height 44 px
- PC: auto-width; padding 12px 20px

**A11y**:
- Role: button (or native <button>)
- Focus-visible: distinct from hover, ≥ 3:1 contrast vs. background
- Disabled: aria-disabled + visual treatment
- Loading: aria-busy + spinner

**Vietnamese notes**:
- "Đăng nhập" fits in sm size
- "Xác nhận thanh toán" needs md or lg size
```

---

## Section C — Detailed Specs for Core Components

### C.1 — Button

**Purpose**: Trigger an action.

**Variants**:
- `primary` — main action of a screen / form (one per visible context)
- `secondary` — supporting action (Cancel, Back, Skip)
- `tertiary` / `ghost` — low-emphasis (toolbar items)
- `destructive` — delete, remove, kick (red)
- `icon-only` — when label would be redundant; provides aria-label

**Sizes**:
| Size | Height | Padding X | Font | Min target |
|---|---|---|---|---|
| sm | 32 px | 12 px | typography.body.sm | 32×32 (mouse contexts only) |
| md | 40 px | 16 px | typography.button | 44×44 with hit-area expansion on mobile |
| lg | 48 px | 20 px | typography.button | 48×48 (touch primary actions) |

**States**:
| State | Visual |
|---|---|
| default | bg=action.primary.bg, fg=action.primary.fg |
| hover | bg=action.primary.bg.hover (mouse) |
| focus-visible | + 2px focus ring (border.focus) at 2px offset |
| active / pressed | bg=action.primary.bg.active, transform: scale(0.98) for 80 ms |
| disabled | opacity 0.5, cursor not-allowed, no hover, no focus animation |
| loading | spinner replaces leading icon; label dims; cursor wait; aria-busy=true |

**Loading guidance**: never let a loading button be re-clickable. Disable interactions while in loading state.

**Vietnamese**: at sm size, fit `Lưu`, `Huỷ`. At md+, fit `Đăng nhập`, `Tạo tài khoản`. For longer like `Xác nhận thanh toán`, use lg or full-width on mobile.

### C.2 — TextField (Input)

**Anatomy**: label (above), description / hint (below label), input, leading icon (optional), trailing icon (optional, for clear / show-password / unit), help text (below input), error text (below help).

**Sizes**: sm (32 px), md (40 px) default, lg (48 px) for primary forms on mobile.

**States**:
- default: border=border.default
- hover: border=border.strong (mouse)
- focus-visible: border=border.focus + 2px ring same color, no outline default
- error: border=feedback.danger.border, error text below
- success: border=feedback.success.border, optional check icon
- disabled: bg=bg.surface.muted, fg=text.disabled
- readonly: like default but no caret, copy still works

**Vietnamese**:
- Label always set (no placeholder-as-label).
- Help text describes constraint: `Mật khẩu phải có ít nhất 8 ký tự, gồm chữ và số.`
- Error text actionable: `Email này đã được sử dụng. Đăng nhập hoặc dùng email khác.`

### C.3 — Modal / Dialog

**Anatomy**: backdrop overlay, modal container, header (title + close), body, footer (action buttons).

**Sizes**: sm (400 px), md (560 px), lg (720 px), xl (920 px), full (mobile).

**Behavior**:
- Open: backdrop fade-in 200 ms (entrance easing) + modal scale-from-0.96 + fade-in 250 ms.
- Close: reverse, 200 ms (exit easing).
- Backdrop click closes (unless critical confirm).
- Escape closes.
- Focus trapped inside; first focusable element receives focus on open.
- On close, restore focus to the trigger.

**Mobile**:
- Modal becomes a full-screen sheet or bottom-sheet at < 640 px.
- Drag-to-dismiss for non-critical bottom sheets.

**A11y**:
- Role: `dialog` with `aria-modal="true"`.
- `aria-labelledby` → header id; `aria-describedby` → body id.
- Live region for any async errors inside.

### C.4 — Table

**Anatomy**: header row (sortable columns with sort indicator), body rows (selectable), footer (pagination + bulk actions when selection > 0).

**Features**:
- Sortable columns (click header → asc/desc/none cycle)
- Filterable (per-column filters in dropdown or top filter bar)
- Selectable rows (checkbox in first column when bulk actions exist)
- Sticky header on scroll
- Pagination (cursor-based or page-based) at bottom
- Empty state when no rows
- Loading state: skeleton rows during fetch

**Responsive**:
- Mobile: convert each row to a card with primary fields stacked.
- Tablet: visible 4–6 columns; rest behind expand/scroll horizontally.
- PC: full feature set.

**Density**: support compact / comfortable / spacious row heights.

### C.5 — Empty State

**Purpose**: friendly affordance when a list / view has no data.

**Anatomy**: illustration (optional), heading, description, primary CTA, secondary link (optional).

**Examples**:

```
[Illustration: empty box]
Chưa có đơn hàng nào ở đây.
Tạo đơn đầu tiên để bắt đầu bán hàng.
[Tạo đơn hàng mới] (primary)
[Xem hướng dẫn] (link)
```

```
[Illustration: search]
Không tìm thấy kết quả cho "iphone 99".
Thử từ khoá khác hoặc xoá bộ lọc.
[Xoá bộ lọc] (secondary)
```

### C.6 — Loading / Skeleton

**Purpose**: communicate work-in-progress without freezing the UI.

**Pattern**:
- < 200 ms: no indicator.
- 200–1000 ms: skeleton matching final layout (shimmer animation if motion allowed; static block if reduced-motion).
- > 1 s: skeleton + cancellable affordance ("Huỷ" link).

**Skeleton rules**:
- Match the shape of real content (don't show a generic 3-line skeleton for a card grid).
- Use a single neutral color (`bg.surface.muted`) with subtle horizontal shimmer.
- Respect `prefers-reduced-motion`: replace shimmer with static block.

### C.7 — Error State

**Purpose**: communicate a failure with a clear next step.

**Anatomy**: icon (alert), heading, description (what failed), action (retry / go back / contact support).

**Examples**:

```
[Icon: cloud-off]
Không thể tải dữ liệu
Kiểm tra kết nối mạng và thử lại.
[Thử lại] (primary)
```

```
[Icon: lock]
Bạn không có quyền xem mục này
Liên hệ quản trị viên để được cấp quyền.
[Quay lại] (secondary)
```

Avoid generic "Đã xảy ra lỗi". Always show what to do next.

### C.8 — Toast / Snackbar

**Purpose**: transient feedback for an action (save success, delete, copy).

**Behavior**:
- Appears at bottom (mobile) or top-right (PC).
- Auto-dismiss after 4–6 seconds.
- Includes optional action button (Undo).
- Stack multiple toasts vertically (max 3 visible).
- Live region: `role="status"` for non-critical, `role="alert"` for errors.

**Variants**: info / success / warning / danger.

### C.9 — Tooltip

**Purpose**: brief explanation for an icon-only control or unfamiliar term.

**Behavior**:
- Mouse: show on hover after 500 ms delay; hide on leave.
- Keyboard: show on focus.
- Touch: do not use tooltips on touch devices; use inline help instead.

**Content**: 1 short sentence; never a paragraph; never required reading.

### C.10 — Form

A composite of fields. Patterns:

- Section headers for groups of related fields.
- One field per row on mobile; 2-col on PC for tightly related fields (e.g., First Name / Last Name — but Vietnamese typically uses single "Họ và tên" field).
- Required fields marked: red asterisk **+** "(bắt buộc)" in label OR optional fields explicitly marked "(tuỳ chọn)" — pick one convention.
- Submit button at the bottom, sticky on mobile when form scrolls.
- Cancel / Back to the left (secondary), Submit to the right (primary).
- Inline validation on blur after first interaction; not on every keystroke.
- Focus jumps to the first error on submit failure.

---

## Section D — Modern Aesthetic Patterns

Use sparingly; brand permission required.

### D.1 — Glassmorphism

```
backdrop-filter: blur(12px);
background: rgba(255, 255, 255, 0.6);
border: 1px solid rgba(255, 255, 255, 0.3);
```

Use on overlays (modal, popover, sticky nav), not on primary surfaces. Always provide a non-blur fallback for browsers that don't support `backdrop-filter`.

### D.2 — Soft Multi-Layer Shadows

Already encoded in the shadow tokens. Two layers (one tight close to surface, one wider for depth) read more natural than a single dark drop shadow.

### D.3 — Gradient Mesh / Vibrant Accents

- Subtle conic / linear gradients on hero areas.
- Vibrant accent dots / chips for categorization.
- Never as background under primary text.

### D.4 — Custom Illustrations

- Use a consistent illustration style (flat, isometric, line, 3D — pick one).
- Vietnamese-context illustrations win trust (people, scenes, objects familiar to the audience).
- Always include alt text.

### D.5 — Friendly Microcopy

Conversational, not robotic:

```
✅ "Chúng tôi đang chuẩn bị dữ liệu cho bạn…"
❌ "Đang xử lý yêu cầu."

✅ "Bạn vừa lưu thay đổi. Tốt!"
❌ "Lưu thành công."

✅ "Chưa có gì ở đây. Hãy bắt đầu bằng việc tạo mục đầu tiên."
❌ "Empty list."
```

---

## Section E — Component Composition Rules

- A complex component is made of primitives — do not bake a button inside a card; pass the button as a slot/child.
- Components do not know their parent's layout — they fill the space given to them.
- Components never set their own outer margin — spacing is the parent's job.
- A component that fetches data is a "container"; a component that renders props is "presentational". Keep them separated.
- Variants are explicit props, not detected via DOM/parents.

---

## Required Practices

- Always design **all eight states** for every interactive component (default / hover / focus-visible / active / disabled / loading / error / success).
- Always reference tokens, never raw values, in component CSS / native styles.
- Always provide `aria-label` for icon-only buttons.
- Always design Empty / Loading / Error states for every data-driven view.
- Always test the longest realistic Vietnamese label in each component at its smallest size.

## Prohibited Practices

- Do not introduce new components when an existing one can be extended.
- Do not depend on hover for primary affordance — touch users have no hover.
- Do not use color alone to convey state.
- Do not let a button stay clickable during loading.
- Do not skip Empty / Error states; they are not optional.
- Do not bake outer margin into a component.
