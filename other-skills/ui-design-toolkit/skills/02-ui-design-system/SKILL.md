---
name: 02-ui-design-system
description: "Generate token-based design systems, 60-30-10 color palettes, Vietnamese-ready typography, microcopy guidelines, and full-state component libraries."
---

# UI Design System & Components

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs to create or update design tokens (Colors, Spacing, Radius, Shadow), configure Vietnamese typography rules, author full-state component specifications (6 states), or standardize interface microcopy and error patterns.

Skip when the task focuses purely on raw wireframe user flows or late-stage accessibility audit reports.

## Workflow

### Phase 1: Design Tokens & Visual Foundations
**Objective**: Engineer an interoperable design token architecture covering 60-30-10 colors, base-8 spacing, border radius, and elevation.

1. Construct the semantic color system following the 60-30-10 distribution rule:
   - 60% Dominant Neutral: Canvas backgrounds, card surfaces, subtle dividers.
   - 30% Secondary: Typography hierarchy, borders, supporting controls.
   - 10% Accent: Primary call-to-action (CTA) buttons, active highlights, key links.
   - Map both Light Theme and Dark Theme contrast compliance using `references/token-spec-dtcg.md`.
2. Define the Spacing scale adhering to the Base-8 grid (4px, 8px, 12px, 16px, 24px, 32px, 48px).
3. Establish Border Radius (`sm`, `md`, `lg`, `full`) and Elevation Shadows (`sm`, `md`, `lg`) matching the project's visual direction.

### Phase 2: Vietnamese Typography & Content Standards
**Objective**: Establish a robust type scale, eliminate diacritics clipping, and define localized content rules.

1. Configure font stacks supporting complete Vietnamese Unicode sets (e.g., `Be Vietnam Pro`, `Inter`, system native).
2. Define the modular type scale with the mandatory rule: Line-height for Vietnamese body copy and labels must remain between **1.4 and 1.6** per `references/vietnamese-typography.md`.
3. Apply anti-overflow safeguards for Vietnamese text expansion: Avoid fixed-width buttons; support 20-30% longer strings without layout breakage.
4. Standardize regional formatting: Currency (`100.000 ₫`), dates (`DD/MM/YYYY`), 24-hour time format.

### Phase 3: Component Specifications & State Matrix
**Objective**: Produce detailed component blueprints ensuring complete 6-state coverage and platform target sizing.

1. Specify core UI components: Buttons (Primary, Secondary, Destructive), Text Inputs, Selects, Cards, Modals/Sheets, Data Tables, Navigation Bars, Toasts.
2. For every interactive component, define all 6 states per `references/component-states-matrix.md`:
   - `Default` → `Hover` → `Active/Pressed` → `Focus-visible` → `Disabled` → `Loading/Error`.
3. Enforce physical target minimums: At least 44x44px for touch (mobile/tablet), 32x32px for pointer (desktop).
4. Specify dynamic component behavior: Center modals automatically convert into swipeable Bottom Sheets on mobile screens.

## Output Format
Design tokens (CSS Custom Properties or DTCG JSON) paired with Component Specification Tables (Component -> Target Size -> Token Mapping -> 6 Interaction States).

## Don'ts
- Do not introduce raw hex values or arbitrary pixel numbers instead of semantic tokens.
- Do not set `line-height` below 1.4 for Vietnamese text, which clips diacritical marks.
- Do not omit `focus-visible` outline rings or `loading` states for interactive elements.
- Do not hardcode fixed widths on buttons containing localized Vietnamese labels.

## Quality Checklist
- [ ] Color system follows 60-30-10 distribution with verified Light and Dark mappings
- [ ] Text contrast meets WCAG 2.2 AA standards (>= 4.5:1 for normal text)
- [ ] Font stack supports Vietnamese Unicode with line-height calibrated between 1.4 and 1.6
- [ ] All interactive components define all 6 required states
- [ ] Touch target sizes reach minimum 44x44px on touch platforms
- [ ] Currency and date formatting conform to Vietnamese regional standards
