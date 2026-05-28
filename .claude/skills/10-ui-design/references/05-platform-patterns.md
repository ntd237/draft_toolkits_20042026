# Phase 5 — Platform Patterns

## Objective

Apply platform-specific conventions so the UI feels native to its environment. A button that looks right on iOS feels alien on Windows; a menu bar that's natural on macOS is wrong on Android.

By the end of this phase you must have:

- Confirmed platform class per surface (W / D-shell / D-native / M-iOS / M-Android / M-cross)
- Platform-specific patterns documented for nav, dialogs, menus, gestures, shortcuts, system integration
- Decisions on which conventions to follow vs. which to override (and why)

---

## Section A — Web (Class W)

### A.1 — Routing & URL

- Every primary screen has a unique URL — bookmarkable, shareable, deep-linkable.
- Use the History API; do not break Back button.
- Loading states should not steal the URL (preserve param state on navigation).
- 404s must include navigation back to known-good destinations.

### A.2 — Browser Chrome

- Respect the browser's scrollbar — do not hide the native scrollbar without replacement.
- Do not override `cmd/ctrl + F` (find), `cmd/ctrl + L` (URL bar), `cmd/ctrl + R` (refresh).
- Custom scrollbars OK in app-shell areas (sidebar, code blocks); leave the page scrollbar native.

### A.3 — Tabs & Multi-Window

- Persist user state (form drafts) so tabs reopened after crash don't lose work.
- `BroadcastChannel` to sync state across tabs (e.g., logout in one tab → log out in others).

### A.4 — Mobile Web vs. Native App

- If the product also ships native: provide an "Open in app" smart banner on iOS Safari / Android Chrome — never auto-redirect.
- Avoid mobile-web patterns that mimic native (e.g., bottom nav with swipe gestures) when they fight browser chrome.

### A.5 — SEO & Metadata

For public web surfaces:
- Every page has `<title>`, `<meta name="description">`, `<meta property="og:*">` tags.
- Headings follow h1 → h2 → h3 hierarchy; skip-level h1→h3 hurts SEO and a11y.
- Canonical URLs set when a page is reachable via multiple paths.
- Language: `<html lang="vi">` and `hreflang` if multilingual.

### A.6 — Web Forms

- Use native HTML5 input types (`type="email"`, `type="tel"`, `type="number"`) — drives mobile keyboard.
- `inputmode="numeric"`, `inputmode="email"` for finer keyboard control.
- `autocomplete="email"`, `autocomplete="current-password"`, `autocomplete="one-time-code"` — saves users typing.
- Submit on Enter must work; submit button is `type="submit"` inside a `<form>`.

### A.7 — Web Dialogs

- Use `<dialog>` element when supported; fallback to focus-trapped div.
- Backdrop click + Escape close (unless a critical confirm).
- Restore focus to the trigger when dialog closes.

---

## Section B — Desktop, Web-Shell (Class D-shell: Electron, Tauri, Wails)

The UI is HTML/CSS/JS but runs as a native window. Mostly Web conventions, plus desktop affordances.

### B.1 — Window Chrome

- Custom title bar OK (frameless window) — but provide draggable region (`-webkit-app-region: drag`).
- Native title bar acceptable for utility apps; required for accessibility on some Linux DEs.
- Min window size: enforce at OS level so content never breaks below ~720 px width.

### B.2 — Native Menus

A native app needs a native menu bar:

- macOS: top-of-screen menu bar (App / File / Edit / View / Window / Help).
- Windows / Linux: in-window menu bar (or hamburger if app is single-purpose).
- Edit menu must include Undo/Redo/Cut/Copy/Paste/Select All — even if the app doesn't have a custom edit feature, the OS expects them.

### B.3 — Keyboard Shortcuts

Desktop-class apps must support:

- `cmd/ctrl + N` — new document/item
- `cmd/ctrl + O` — open
- `cmd/ctrl + S` — save
- `cmd/ctrl + W` — close window/tab
- `cmd/ctrl + Q` — quit (mac/linux convention)
- `cmd/ctrl + ,` — preferences (mac convention)
- `cmd/ctrl + K` — command palette / search
- `cmd/ctrl + Z`, `cmd/ctrl + Shift + Z` — undo / redo
- `cmd/ctrl + F` — find
- `Esc` — cancel / close modal
- `Tab` / `Shift+Tab` — focus traversal

Document the shortcut map in a help / cheatsheet view.

### B.4 — System Tray

- Icon in tray for background-running apps (chat, sync clients).
- Right-click menu: Open / Status / Quit.
- Click on tray icon opens main window (Windows convention).

### B.5 — Dialogs

- Use OS-native file picker (`showOpenFilePicker`, Electron `dialog.showOpenDialog`).
- Use OS-native confirm/alert for destructive prompts.
- Custom in-app modals OK for content-related actions.

### B.6 — Multi-Window

- Document edits open new windows on macOS (one window per document is HIG).
- On Windows/Linux, MDI or tabbed UI is acceptable.
- Persist window position / size per window across launches.

### B.7 — File-System Integration

- Drag-and-drop files into the window must work.
- Open-with from OS file manager opens the app + the file.
- "Recent files" list persisted across launches.

---

## Section C — Desktop, Native (Class D-native: PyQt5/PySide6, WPF, JavaFX, Cocoa)

All of Section B applies, plus:

### C.1 — Use Native Widgets

- Buttons, inputs, tabs, lists, scrollbars: use the framework's native widget.
- Custom paint only when the native widget cannot express the design.
- Native widgets get accessibility for free; custom-paint requires re-implementing it.

### C.2 — DPI Awareness

- Test at 100%, 125%, 150%, 200% DPI on Windows.
- Test at 1× and 2× retina on macOS.
- Use vector / SVG icons; bitmap icons need 1×, 1.5×, 2×, 3× variants.

### C.3 — High-Contrast Mode

Windows ships High-Contrast themes; the app should:
- Respect user theme by default.
- Provide override only for in-app contrast preference.

### C.4 — PyQt5 / PySide6 Specifics

- Use `QSS` for styling — never inline-style widgets.
- Subclass widgets to add behavior; do not monkey-patch.
- Run in a single QApplication; one event loop.
- Use `QFontDatabase` to load custom fonts (see `03-vietnamese-typography.md`).
- Use `QSizePolicy` to make layouts responsive.
- Test the QSS at every DPI scaling level.

### C.5 — WPF / WinUI3 Specifics

- Use ResourceDictionary for theming.
- Bind via DataContext + INotifyPropertyChanged (MVVM is the norm).
- Use built-in `<Theme>` resources for Light/Dark.

---

## Section D — Mobile, Native iOS (Class M-iOS)

Follow **Apple Human Interface Guidelines (HIG)** strictly. Users expect iOS apps to feel iOS.

### D.1 — Navigation

- **Tab bar** at the bottom: 3–5 tabs.
- **Navigation stack**: push/pop with system back gesture (swipe from left edge).
- **Modal sheets**: half-sheet (`.medium`) or full-sheet (`.large`) for focused tasks.
- Always provide a `Cancel`/`Done` button on modal sheets.

### D.2 — System UI

- Respect safe-area insets (notch, home indicator, Dynamic Island).
- Status bar style: `.dark` on light backgrounds, `.light` on dark backgrounds.
- Large titles on top-level destinations; collapse on scroll.

### D.3 — Gestures

- Swipe-to-go-back on push navigation.
- Swipe actions on list rows (delete, archive).
- Long-press for context menu (preview + actions).
- Pull-to-refresh on scrollable lists.

### D.4 — Common iOS Components

- `UIAlertController` / SwiftUI `Alert` for confirmation.
- `UIAction` with system icons (SF Symbols).
- `NavigationLink` / `NavigationStack` (SwiftUI 4+).
- `Toggle` for on/off switch.
- `Stepper` for numeric increment.
- `Picker` segmented or wheel.

### D.5 — Haptics

- Selection: `.selectionChanged` haptic on tab switch / picker.
- Light impact: button presses on important actions.
- Success / Warning / Error: notification haptics.

### D.6 — Native Iconography

- SF Symbols for icons that exist there.
- Custom SVG only when SF Symbols cannot match the brand.

---

## Section E — Mobile, Native Android (Class M-Android)

Follow **Material Design 3** strictly.

### E.1 — Navigation

- **Bottom navigation bar**: 3–5 destinations.
- **Navigation drawer**: 6+ destinations.
- **Top app bar** with title + actions.
- **Back button**: system bar back + in-app back coexist; both should work.

### E.2 — System UI

- Edge-to-edge layout: content under status bar with translucent overlay.
- System bar color matches app theme.
- Predictive back gesture (Android 14+) — design previews.

### E.3 — Common Material 3 Components

- `Button`, `OutlinedButton`, `TextButton`, `FilledTonalButton`, `ElevatedButton` — pick by emphasis.
- `FloatingActionButton` for primary creation action.
- `Scaffold` provides standard layout slots.
- `BottomSheet` for ad-hoc content.
- `Snackbar` for transient feedback (with optional action).
- `Chip` for filters, tags, suggestions.
- `Card` for grouped content.

### E.4 — Gestures

- Swipe actions on list rows.
- Pull-to-refresh.
- Long-press for selection mode (changes top app bar to action mode).

### E.5 — Iconography

- Material Symbols (rounded / outlined / sharp — pick one).
- Custom SVG only for brand glyphs.

---

## Section F — Mobile, Cross-Platform (Class M-cross: Flutter, RN, MAUI)

Pick a platform-adaptive strategy:

### F.1 — Cupertino + Material on the same codebase

- Flutter: use `Cupertino*` widgets when running on iOS, `Material` otherwise. `Theme.of(context).platform` tells you.
- React Native: separate `Pressable` styles per `Platform.OS`.
- This is the right path for products that want to feel native on each OS.

### F.2 — One look across platforms (brand-first)

Some brands prefer their own consistent look on both. Rules:

- Adopt Material as the underlying interaction model (it generalizes better than iOS HIG).
- Override visual styling (colors, type, radius) per brand.
- Honor system gestures: back gesture on Android, swipe-back on iOS, both must work.

### F.3 — Flutter Specifics

- `MaterialApp` for Material design language; `CupertinoApp` for iOS-only.
- For cross-platform, use `MaterialApp` and adapt key components.
- Use `Adaptive*` widgets (`Switch.adaptive`, `Slider.adaptive`) for free per-platform variants.
- Run on Flutter Desktop / Flutter Web with the same codebase but adjust layouts via `LayoutBuilder` and `MediaQuery`.

### F.4 — React Native Specifics

- `KeyboardAvoidingView` for forms.
- `SafeAreaView` for iOS notch handling.
- Use Reanimated for 60fps gestures.
- Platform-specific files: `Component.ios.tsx`, `Component.android.tsx` for divergent behavior.

---

## Section G — Common Cross-Platform UX Decisions

### G.1 — Date / Time Picker

- iOS: native UIDatePicker (compact / wheel / inline).
- Android: Material Date Picker.
- Web: `<input type="date">` is acceptable; for richer UX, use a library aligned with the design system.
- Always default to today / now, with sensible min/max bounds.
- Vietnamese: format `dd/MM/yyyy`, week starts Monday.

### G.2 — Phone Number Input

- Format as user types: `0987 654 321` (Vietnamese 10-digit format).
- Inline country selector when international numbers are valid.
- Validate on blur, not on every keystroke.
- `inputmode="tel"` on web; `keyboardType: 'phone-pad'` on RN; `KeyboardType.Phone` on Compose.

### G.3 — Currency Input

- Vietnamese: input as plain digits, format with dot thousands on blur (`1.234.567`).
- Append `₫` as visual suffix, not part of the input value.
- Reject decimals for VND; show error if user enters one.

### G.4 — Long Lists

- Virtualize at > 100 items (FlatList in RN, ListView.builder in Flutter, react-window on web).
- Sticky section headers.
- Pull-to-refresh + infinite scroll combine well.
- "Empty state" when no results from filter.

### G.5 — Forms

- Single column on mobile; 2-col on PC for tightly related fields.
- Errors inline beneath each field, not in a top banner.
- Validate on blur (initial) and on input (after first error).
- Submit button disabled when form invalid; show why (link to first error).

### G.6 — Search

- On mobile: dedicated search screen, full-screen, with recent searches.
- On PC: command-palette pattern (`cmd/ctrl + K`).
- Debounce 200–300 ms; show "Đang tìm…" if > 500 ms.
- Empty results: helpful empty state with suggestions.

### G.7 — Pull-to-Refresh

- Standard on mobile lists.
- Skip on web (use a refresh button instead).
- Skip on desktop (use a refresh button in the toolbar).

### G.8 — Loading States

- < 200 ms: no indicator (perceived as instant).
- 200–1000 ms: skeleton loader matching final layout.
- > 1 s: skeleton + cancellable affordance.
- > 5 s: progress indicator with percentage if measurable, with retry option.

### G.9 — Offline State

- Detect: `navigator.onLine` (Web), `Connectivity` packages (Flutter/RN).
- Banner: `Bạn đang ngoại tuyến. Một số tính năng có thể không hoạt động.`
- Queue mutations and replay when back online (where possible).

---

## Section H — Cross-Platform Decisions Summary

| Decision | Web | Desktop | Mobile |
|---|---|---|---|
| Primary nav | top nav / sidebar | sidebar | bottom nav / drawer |
| Form submit | Enter key + button | Enter key + button | bottom sticky button |
| Confirm destructive | modal | OS-native dialog | full-screen confirm |
| Long content | scroll | scroll | scroll + pagination |
| Find | `cmd/ctrl + F` | `cmd/ctrl + F` | search icon → search screen |
| Refresh | reload button | reload button / cmd+R | pull-to-refresh |
| Multi-select | shift/ctrl-click | shift/ctrl-click | long-press → action mode |
| Tooltips | hover | hover | none (use inline help) |
| Right-click | yes (context menu) | yes (context menu) | long-press |

---

## Required Practices

- Always honor system back gesture / button on mobile.
- Always implement the OS's standard keyboard shortcuts on Desktop.
- Always provide native menu bar on macOS Desktop apps.
- Always respect safe-area insets on mobile.
- Always provide haptic feedback for important interactions on mobile native.

## Prohibited Practices

- Do not put primary navigation at the top on mobile (the bottom is reach zone).
- Do not require hover for primary actions on any platform.
- Do not auto-redirect mobile-web users to native app stores; offer a banner.
- Do not override OS keyboard shortcuts (`cmd/ctrl + F`, `cmd/ctrl + L`, `cmd/ctrl + R`) on Web.
- Do not invent custom-paint widgets when native ones can do the job.
- Do not ignore platform conventions just because "consistency across platforms" sounds nice; users live in their OS.
