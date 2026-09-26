# Application UX Recipes: Web, Mobile & Desktop

Design recipes for three core application software environments: Web Apps (SaaS/Admin), Mobile Apps (iOS/Android), and Desktop Apps (Windows/macOS/Linux).

---

## 1. Web App & Enterprise SaaS UX

Optimized for web-based productivity software requiring high data density.

### 1.1. Data Tables & High Density
- **Sticky Headers & Columns**: Apply `position: sticky` to header rows (`thead`) and primary identification columns (e.g., Record ID, Name).
- **Multi-Tier Filtering**: Inline global search, multi-select status filters, date range pickers, and saved filter views.
- **Pagination & Virtual Scrolling**: Explicit pagination controls or virtualized DOM rendering for datasets exceeding 1,000 records.

### 1.2. Keyboard Productivity & Navigation
- **Command Palette**: `Ctrl + K` (or `Cmd + K`) opens universal quick-action search.
- **Shortcuts**: Standard navigation shortcuts (`J/K` list traversal, `Enter` to open, `Esc` to dismiss modals).
- **Breadcrumbs**: Explicit navigational path display (Home > Workspace > Project > Detail).

---

## 2. Mobile App UX (iOS & Android)

Touch-first ergonomics engineered around physical hand reach and mobile hardware constraints.

### 2.1. Thumb Zone Ergonomics
```
┌───────────────────────┐
│     HARD TO REACH     │ ← Static info, page headers, display banners
├───────────────────────┤
│     NATURAL REACH     │ ← Scrollable card feeds, interactive lists
├───────────────────────┤
│       EASY ZONE       │ ← Primary CTA buttons, Bottom Navigation,
│     (Optimal Touch)   │   Floating Action Buttons (FAB), Form submits
└───────────────────────┘
```
- Anchor critical interactive elements within the **lower third of the physical screen**.

### 2.2. Hardware Safe Area Insets
- **Top Safe Area**: Inset padding avoiding camera cutouts, notches, and dynamic islands (`padding-top: env(safe-area-inset-top);`).
- **Bottom Safe Area**: At least 16-24px padding clear of the OS home gesture indicator (`padding-bottom: env(safe-area-inset-bottom);`).
- **Dialog Conversion**: 100% of mobile dialogs must render as **Bottom Sheets** (swipe down to dismiss) instead of centered modals.

---

## 3. Desktop App UX (Electron, Tauri, Qt, WPF, WinUI)

Designed for native desktop operating system integration.

### 3.1. Custom Window Chrome
- Integrate window title, universal search bar, and OS window control buttons (Minimize, Maximize, Close) into a unified header bar.
- Ensure draggable title regions (`-webkit-app-region: drag`) do not overlap interactive controls (`-webkit-app-region: no-drag`).

### 3.2. Context Menus & System Tray
- **Right-Click Context Menu**: Contextual actions matching the clicked target (Copy, Rename, Delete, Properties).
- **Status Bar**: Pinned to the window bottom, displaying connection state, selected row counts, and zoom controls.
- **DPI Scaling**: Interfaces must scale cleanly without visual blurring or clipping across standard Windows scaling levels: 100%, 125%, 150%, 200%.
