---
name: 03-ui-platform-responsive
description: "Architect responsive multi-screen layouts (Mobile, Tablet, PC) and specialized interface recipes for Web Apps, Mobile Apps, Desktop Apps, and Game UIs."
---

# UI Platform & Responsive Layout

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs responsive grid systems across Mobile, Tablet, PC, and Ultrawide viewports, adaptive navigation transitions, or specialized interface recipes for Web Apps, Mobile Apps, Desktop Apps, Desktop Games, or Mobile Games.

Skip when the task focuses purely on color palette selection, primitive token extraction, or review checks without layout implications.

## Workflow

### Phase 1: Responsive Breakpoints & Fluid Grids
**Objective**: Establish viewport breakpoint thresholds and adaptive layout transitions from compact mobile to ultrawide monitors.

1. Define 4 standard breakpoint tiers following `references/responsive-breakpoints.md`:
   - Mobile (< 768px): 4-column grid, 16px margins, single-column vertical stack.
   - Tablet (768px - 1024px): 8-column grid, 24px margins, 2-column Master-Detail split view.
   - Desktop (1024px - 1920px): 12-column grid, 32px margins, multi-column grid with sidebar.
   - Ultrawide (> 1920px): 12/16-column grid, centered container capped at max-width 1440px.
2. Establish navigation adaptation logic:
   - Mobile: Fixed Bottom Navigation Bar + slide-over Drawer menu.
   - Tablet: Navigation Rail (slim 64-72px icon bar on left edge).
   - Desktop: Persistent Sidebar (240-280px width, collapsible).
3. Apply Container Queries for modular, reusable component cards.

### Phase 2: Application Platform Adaptation (Web, Mobile, Desktop)
**Objective**: Implement platform-specific ergonomic conventions and native input models per `references/desktop-mobile-apps.md`.

1. **Web App (SaaS/Admin)**:
   - Optimize for high information density, pointer precision, and keyboard traversal.
   - Design data tables with sticky headers, multi-tier sorting/filtering, and pagination.
   - Integrate universal quick-action search (`Command Palette Ctrl+K`), shortcuts, and breadcrumbs.
2. **Mobile App (iOS/Android)**:
   - Apply Thumb Zone ergonomics: Position high-frequency primary actions within the lower third of the screen.
   - Enforce hardware safe area insets avoiding camera cutouts, dynamic islands, and home indicator bars.
   - Convert all modal dialogs into swipeable Bottom Sheets on mobile viewports.
3. **Desktop App (Windows/macOS/Linux)**:
   - Design custom window chrome integrating window title, search, and native controls.
   - Provide right-click context menus, system tray integration, and bottom status bars.
   - Ensure pixel-crisp rendering across standard DPI scaling levels (100%, 125%, 150%, 200%).

### Phase 3: Game UI & HUD Adaptation (Desktop & Mobile)
**Objective**: Engineer Heads-Up Display (HUD) overlays and in-game menus optimized for gaming hardware per `references/game-ui-hud-ergonomics.md`.

1. **Desktop Game (PC/Console)**:
   - Anchor HUD modules to the 4 corners (Avatar/HP top-left, Minimap top-right, Chat bottom-left, Skills bottom-right), keeping the center clear for gameplay.
   - Apply hardware safe zone offsets (minimum 32-48px margin).
   - Support 21:9 Ultrawide scaling (edge-anchored or 16:9 center-locked).
   - Engineer controller focus rings with unbroken 4-way D-pad navigation.
2. **Mobile Game (Dual Thumb Touch)**:
   - Establish dual thumb zones: Floating virtual joystick on lower left, arc-shaped skill buttons on lower right.
   - Enforce oversized button targets (48-64px) with 60-70% opacity to maintain field of vision.
   - Integrate haptic feedback triggers and maintain safe distance from screen bevels.

## Output Format
Responsive Breakpoint Matrix (Breakpoint -> Columns -> Navigation -> Component Adaptation) paired with Platform UX Recipes.

## Don'ts
- Do not apply mouse hover states to touch-driven interfaces (Mobile, Tablet, Mobile Game).
- Do not place mission-critical game HUD controls outside the hardware safe zone.
- Do not hardcode fixed pixel widths that break when rendered on tablets or ultrawide screens.
- Do not deploy center popups on mobile apps when a bottom sheet is appropriate.

## Quality Checklist
- [ ] Breakpoint behaviors defined across Mobile, Tablet, Desktop, and Ultrawide
- [ ] Adaptive navigation transitions (Bottom Bar → Rail → Sidebar) explicitly mapped
- [ ] Safe area insets respected for mobile devices and game HUD overlays
- [ ] Web and Desktop apps leverage high data density and keyboard productivity
- [ ] Game Desktop specifies 4-corner HUD anchors and controller focus rings
- [ ] Game Mobile adheres to dual-thumb ergonomics with targets >= 48px
