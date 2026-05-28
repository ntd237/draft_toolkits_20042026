# Phase 7 — Interaction & Motion

## Objective

Design the **feel** of the UI — micro-interactions, transitions, motion language — so the product is responsive, tactile, and trustworthy. Motion serves perception, not decoration. Anything that doesn't help the user understand what just happened is noise.

---

## Section A — Motion Principles

### A.1 — Five rules

1. **Purposeful** — every motion answers "what just happened?" or "where did it go?".
2. **Fast** — perceived performance > literal performance; users prefer 200 ms over 500 ms.
3. **Natural** — eased curves, not linear; objects accelerate then decelerate.
4. **Consistent** — same action = same motion language across the product.
5. **Respectful** — `prefers-reduced-motion` always wins; offer a static fallback for every animation > 200 ms.

### A.2 — Duration Tokens (from Phase 2)

```
motion.duration.instant  → 50 ms     ← imperceptible feedback (hover color)
motion.duration.fast     → 150 ms    ← micro-interactions (button press, focus ring)
motion.duration.medium   → 250 ms    ← state changes (modal open/close, expand)
motion.duration.slow     → 400 ms    ← page-level transitions
motion.duration.slowest  → 600 ms    ← hero animations, onboarding only
```

### A.3 — Easing Tokens

```
motion.easing.standard  → cubic-bezier(0.4, 0, 0.2, 1)        ← default in-out
motion.easing.entrance  → cubic-bezier(0, 0, 0.2, 1)           ← out (objects coming in)
motion.easing.exit      → cubic-bezier(0.4, 0, 1, 1)           ← in (objects going out)
motion.easing.spring    → cubic-bezier(0.34, 1.56, 0.64, 1)    ← bouncy (use sparingly)
```

Use `entrance` when an element appears (modal in, toast in). Use `exit` when an element leaves (modal out, toast out). Use `standard` for state changes (hover, expand).

### A.4 — Transformations to Animate

Animate cheap properties only:

| Cheap (use freely) | Expensive (avoid in animations) |
|---|---|
| `transform: translate / scale / rotate` | `width`, `height`, `top`, `left`, `margin` (cause layout) |
| `opacity` | `box-shadow` change of size (causes paint) |
| `filter: blur / brightness` (modern GPUs handle) | `background` color change of large area |
| `clip-path` | `border-width` |

Promote to a separate compositor layer when an element is animated heavily: `will-change: transform`, `transform: translateZ(0)`. Remove `will-change` after animation ends.

---

## Section B — Micro-Interaction Catalog

### B.1 — Button Press

```
Default → Hover (mouse only): bg shifts to .hover, 150 ms standard
Click / tap: scale(0.98) for 80 ms then back, bg shifts to .active during press
Release: returns to hover or default
```

Native: leverage platform's tactile press (haptic on iOS, ripple on Android).

### B.2 — Input Focus

```
Default → Focus-visible: border color shifts to border.focus + 2 px focus ring at 2 px offset
Animation: 150 ms standard, on `border-color, box-shadow, transform`.
Don't animate the input height; that causes layout shift.
```

### B.3 — Dropdown / Select Expand

```
Open: 200 ms entrance — translateY(-4px → 0) + opacity 0 → 1
Close: 150 ms exit — opacity → 0 (skip translate; faster perceived dismissal)
```

### B.4 — Modal / Dialog

```
Backdrop: 200 ms — opacity 0 → 0.6
Modal:    250 ms entrance — scale 0.96 → 1.0 + opacity 0 → 1
Close:    200 ms exit — reverse, both
```

Mobile bottom sheet:
```
Open: 300 ms entrance — translateY(100% → 0)
Close: 250 ms exit — translateY(0 → 100%)
Drag-to-dismiss: follow finger; release → snap to nearest snap point with spring easing.
```

### B.5 — Toast / Snackbar

```
Enter: 250 ms — translateY(20px → 0) + opacity 0 → 1
Exit:  200 ms — translateY(0 → -10px) + opacity → 0
Auto-dismiss: 4–6 seconds (longer for messages with actions)
```

### B.6 — Tab Switch

```
Indicator slide: 200 ms standard easing, transform translateX
Content cross-fade: 150 ms — old fades out, new fades in
On mobile: optional translateX content swap matching tab direction
```

### B.7 — Accordion / Collapsible

```
Expand: 250 ms — height auto via grid template rows (0fr → 1fr)
Collapse: 200 ms — reverse
```

Use `grid-template-rows: 0fr → 1fr` instead of `max-height` hack; it animates true height without flicker.

### B.8 — Skeleton Shimmer

```
Background: linear-gradient(90deg, bg.surface.muted, bg.surface, bg.surface.muted)
Animation: 1500 ms linear infinite, translateX(-100% → 100%)
Reduced-motion: replace with static bg.surface.muted
```

### B.9 — Page Transition (Web SPA)

```
Default: 200 ms cross-fade between routes
Hierarchical (push): 300 ms — slide-in from right + previous slides out left
Hierarchical (pop):  300 ms — reverse
```

Don't animate every route change; only when there's a clear hierarchy.

### B.10 — Drag and Drop

```
Drag start: 100 ms — scale(1.02) + shadow.lg
During drag: follow cursor
Hover over droppable: target border highlights + bg.surface.muted
Drop: 200 ms snap-into-place + scale back to 1.0
Reject (invalid drop): 200 ms shake (translateX ±4 px three times)
```

---

## Section C — Page-Level Patterns Per Platform

### C.1 — Web

- Route transitions: 200 ms cross-fade default; longer for storytelling pages.
- Scroll-triggered fade-in for sections: only when reduced-motion OFF; threshold 30% in viewport; fade + 16 px translateY.
- Avoid scroll-jacking; never override the scrollbar speed.

### C.2 — iOS

- Push: 350 ms native — leverage UINavigationController / SwiftUI NavigationStack default.
- Modal: native sheet animation; don't reinvent.
- Tab change: instant.

### C.3 — Android

- Activity / Fragment transitions: shared element transitions for hierarchy.
- Material motion: container transform (linking elements via shared bounds).
- FAB → screen transform when FAB launches a creation flow.

### C.4 — Desktop

- Window-level transitions are minimal — opening a modal animates 200 ms; switching tabs in-window is instant.
- Avoid full-window slide animations; users on Desktop expect snappy.
- Keyboard shortcuts should not animate; instant feedback is the contract.

---

## Section D — Gesture Catalog (Mobile Native)

| Gesture | Action |
|---|---|
| Tap | Primary trigger |
| Double-tap | Zoom (images, maps) — rarely as primary action |
| Long-press | Context menu, multi-select start |
| Swipe-left / -right (list row) | Reveal actions (delete, archive) |
| Swipe-up (bottom sheet) | Expand to full |
| Swipe-down (modal/sheet) | Dismiss |
| Swipe-from-edge (iOS) | Back navigation |
| Pull-down at top of list | Refresh |
| Pinch | Zoom (images, maps) |
| Two-finger pan | Map pan / canvas pan |

Document a gesture before relying on it; new users will not discover it without a hint (subtle animation, coach mark on first run).

---

## Section E — Keyboard / Pointer Patterns (Desktop / Web)

| Input | Action |
|---|---|
| Tab / Shift+Tab | Focus traversal |
| Enter | Activate focused button / submit form |
| Space | Activate focused button / toggle checkbox |
| Esc | Close modal / dropdown / cancel |
| Arrow keys | Navigate within composite widgets (menu, listbox, radiogroup) |
| Home / End | Jump to first / last in a list |
| `cmd/ctrl + K` | Command palette / global search |
| `?` (no modifier) | Show keyboard shortcuts cheatsheet |
| Right-click | Context menu (Web + Desktop) |
| Hover | Tooltip / hover state |
| Drag | Move / select range |
| Scroll | Page scroll (do not capture) |

---

## Section F — Reduced-Motion Strategy

CSS guard:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

This zero-duration approach turns every transition into instant state changes, which is the safest fallback. For specific experiences (skeleton shimmer, hero animations) that are core to the design, replace with static equivalents:

```css
.skeleton {
  background: var(--color-bg-surface-muted);
  animation: shimmer 1500ms linear infinite;
}
@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; background: var(--color-bg-surface-muted); }
}
```

Also disable parallax, autoplay videos, automatic carousel rotation under reduced-motion.

Native:
- iOS: `UIAccessibility.isReduceMotionEnabled` — replace transitions with `.linear` cross-fade.
- Android: `Settings.Global.ANIMATOR_DURATION_SCALE == 0` — skip non-essential animations.
- Flutter: `MediaQuery.of(context).disableAnimations`.

---

## Section G — Performance Budget

- Animations must run at 60 fps. Test on low-end devices (4-year-old Android mid-range).
- `transform` and `opacity` only on the hot path.
- Use `requestAnimationFrame` (Web) / `Choreographer` (Android) / `CADisplayLink` (iOS) for JS-driven animations; avoid `setInterval`.
- Avoid CSS animation on > 50 elements at once; consider Lottie / video for complex sequences.
- Promote to compositor layer with `will-change: transform`, but remove after animation completes — many promoted layers cost memory.

---

## Section H — Loading Patterns by Duration

| Wait time | Pattern |
|---|---|
| < 200 ms | No indicator (perceived as instant) |
| 200–1000 ms | Skeleton matching final layout |
| 1–5 s | Skeleton + cancellable affordance |
| > 5 s | Progress bar (% if measurable, indeterminate otherwise) + retry option + status update |
| Long-running background | Toast on completion + status icon during work |

Skeleton vs spinner:
- Skeleton wins when the layout is known (cards, lists, forms).
- Spinner is OK for unknown layouts (modal opening with dynamic content).
- A spinner alone for > 1 s feels broken; replace with skeleton or progress.

---

## Section I — Empty / Error / Success Animation

- Empty state appearing: 200 ms fade-in + 8 px translateY. Don't bounce.
- Error toast: 200 ms enter + subtle 100 ms shake (translateX ±2 px three times) for emphasis on critical errors only.
- Success toast: 250 ms enter + check icon scales 0 → 1 with spring easing 300 ms.

---

## Section J — Sound (Mobile Native, optional)

- iOS: `UISelectionFeedbackGenerator` for tab switches, `UINotificationFeedbackGenerator` for success/warning/error.
- Android: `View.performHapticFeedback(...)`.
- Sound effects rare in Vietnamese productivity apps; consumer-game UIs may use them.
- Always respect system silent / mute / accessibility settings.

---

## Required Practices

- Always pair every animation > 200 ms with a `prefers-reduced-motion` fallback.
- Always animate transform/opacity over layout-affecting properties.
- Always use entrance easing for "in" and exit easing for "out".
- Always design for the unloaded / loading / loaded / error states with motion-aware transitions.
- Always cap animations at 60 fps; profile on a mid-range device.

## Prohibited Practices

- Do not animate `width`, `height`, `top`, `left`, `margin` for visual transitions.
- Do not use durations > 400 ms for routine state changes.
- Do not chain more than 2 animations on the same element at once.
- Do not autoplay video / parallax / carousel rotation without a pause control.
- Do not override the system's scroll behavior.
- Do not bounce / spring on every element — reserve for delight moments (success confirmation, onboarding).
