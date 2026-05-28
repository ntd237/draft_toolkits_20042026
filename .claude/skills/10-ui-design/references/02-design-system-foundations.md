# Phase 2 — Design System Foundations (Tokens)

## Objective

Lock the **design tokens** before drawing any screens. Tokens are the language of the system; if every screen invents its own values, you do not have a design system, you have stickers on a wall.

By the end of this phase you must have:

- Two-tier model: **primitives** (raw values) + **semantic** (meaning aliases)
- Token tables for color, typography, spacing, radius, shadow, motion, breakpoints, z-index
- Light + dark theme mappings
- Verified WCAG 2.1 AA contrast for every text/background pair
- Export shape that matches the project's stack

---

## Section A — Token Tier Model

Always model in two tiers. Primitives are the palette; semantics are how the system uses them.

### Primitives (raw values)

```
color.neutral.0    → #FFFFFF
color.neutral.50   → #F8FAFC
color.neutral.100  → #F1F5F9
color.neutral.200  → #E2E8F0
color.neutral.300  → #CBD5E1
color.neutral.400  → #94A3B8
color.neutral.500  → #64748B
color.neutral.600  → #475569
color.neutral.700  → #334155
color.neutral.800  → #1E293B
color.neutral.900  → #0F172A
color.neutral.950  → #020617

color.brand.50 ... color.brand.950          ← 11 stops, brand hue
color.success.50 ... color.success.950
color.warning.50 ... color.warning.950
color.danger.50 ... color.danger.950
color.info.50 ... color.info.950
```

### Semantics (meaning aliases, mapped per theme)

```
color.bg.canvas        → light: neutral.50      | dark: neutral.950
color.bg.surface       → light: neutral.0       | dark: neutral.900
color.bg.surface.muted → light: neutral.100     | dark: neutral.800
color.bg.surface.raised→ light: neutral.0       | dark: neutral.800
color.bg.overlay       → light: rgba(15,23,42,.6) | dark: rgba(0,0,0,.7)

color.text.primary     → light: neutral.900     | dark: neutral.50
color.text.secondary   → light: neutral.700     | dark: neutral.300
color.text.muted       → light: neutral.500     | dark: neutral.400
color.text.disabled    → light: neutral.400     | dark: neutral.600
color.text.inverse     → light: neutral.0       | dark: neutral.900
color.text.brand       → light: brand.700       | dark: brand.300
color.text.success     → light: success.700     | dark: success.300
color.text.danger      → light: danger.700      | dark: danger.300

color.border.subtle    → light: neutral.200     | dark: neutral.800
color.border.default   → light: neutral.300     | dark: neutral.700
color.border.strong    → light: neutral.400     | dark: neutral.600
color.border.focus     → light: brand.500       | dark: brand.400

color.action.primary.bg          → light: brand.600  | dark: brand.500
color.action.primary.bg.hover    → light: brand.700  | dark: brand.400
color.action.primary.bg.active   → light: brand.800  | dark: brand.300
color.action.primary.fg          → light: neutral.0  | dark: neutral.950

color.action.secondary.bg        → light: neutral.0  | dark: neutral.800
color.action.secondary.bg.hover  → light: neutral.100| dark: neutral.700
color.action.secondary.fg        → light: neutral.900| dark: neutral.50
color.action.secondary.border    → light: neutral.300| dark: neutral.700

color.feedback.success.bg/.fg/.border
color.feedback.warning.bg/.fg/.border
color.feedback.danger.bg/.fg/.border
color.feedback.info.bg/.fg/.border
```

Rules:

- Components reference **semantics only**, never primitives.
- Themes swap **primitives**, never semantics. A button's CSS does not know light vs. dark.
- Add a new semantic only when ≥ 2 components need the same role; otherwise it's an artifact.

---

## Section B — Color Token Recipe

### B.1 — Brand Hue Selection

If the user provides a brand color, derive the 11-stop ramp (50–950) using a perceptual scale (OKLCH or HSL with controlled lightness steps). Avoid naive `lighten()`/`darken()` — they collapse into desaturated mush.

A pragmatic recipe (light → dark):

```
50:  L 97% chroma 2%   hue=brand
100: L 94% chroma 5%
200: L 88% chroma 10%
300: L 80% chroma 15%
400: L 70% chroma 18%
500: L 60% chroma 20%   ← typically "main" stop
600: L 52% chroma 22%   ← typically "accent on light bg"
700: L 42% chroma 22%   ← typically "text on light"
800: L 32% chroma 18%
900: L 22% chroma 12%
950: L 14% chroma 8%
```

If the project already has a brand color set, **do not override**. Read what exists and keep going.

### B.2 — Status Hues

Default mapping (override if the project has them):

| Role | Suggested hue |
|---|---|
| success | green / emerald (~150°) |
| warning | amber / orange (~40°) |
| danger | red / rose (~10°–20°) |
| info | blue / sky (~220°) |

### B.3 — Color Psychology (apply consciously)

| Color | Connotation | Use for |
|---|---|---|
| Blue | trust, calm, productivity | primary brand for fintech, SaaS, gov |
| Green | success, growth, money | success states; finance accents |
| Red | error, urgency, stop | error states, destructive actions, sales accents |
| Yellow / amber | warning, caution | warnings, pending states |
| Purple | premium, creative | premium features, creative tools |
| Gray | neutral, calm | text, borders, backgrounds (the silent majority) |

### B.4 — Modern Aesthetic Decisions (apply when brand allows)

- **Glassmorphism**: frosted overlays — `backdrop-filter: blur(12px)` + `background: rgba(255,255,255,0.6)` + 1px subtle border. Use sparingly: dialogs, hero overlays.
- **Soft shadows**: stack 2 layers (one tight, one wide) instead of one dark drop shadow. Already encoded in elevation tokens (Section F).
- **Gradient mesh / vibrant accents**: use as subtle backdrop on hero or empty-state surfaces; never as primary surface that text sits on.
- **Bento grid layout**: cards of varying spans on dashboards / portfolio surfaces — see `references/04-responsive-strategy.md`.

---

## Section C — Contrast Verification

For every text/background semantic pairing in **both themes**, compute the contrast ratio.

WCAG 2.1 AA targets:

| Use | Min ratio |
|---|---|
| Body text < 18 pt regular / < 14 pt bold | **4.5 : 1** |
| Large text ≥ 18 pt regular / ≥ 14 pt bold | **3 : 1** |
| Non-text UI (icons, focus rings, meaningful borders) | **3 : 1** |

If a pairing fails, adjust the primitive that backs the semantic. Document:

```
| Pair                                  | Ratio  | Pass?  |
|---|---|---|
| text.primary on bg.canvas (light)     | 16.78  | AAA    |
| text.muted   on bg.canvas (light)     |  4.83  | AA     |
| text.brand   on bg.canvas (light)     |  5.21  | AA     |
| action.primary.fg on action.primary.bg|  7.12  | AAA    |
| ...                                   |        |        |
```

---

## Section D — Typography Tokens

Pair with `references/03-vietnamese-typography.md` for font selection and Vietnamese-specific tuning.

### D.1 — Type Scale (mobile-first; scale up on PC where useful)

Modular scale anchored at body 16 px (1 rem):

```
font.size.xs    → 12 px / 0.75 rem    line-height 1.55
font.size.sm    → 14 px / 0.875 rem   line-height 1.55
font.size.base  → 16 px / 1 rem       line-height 1.6
font.size.md    → 18 px / 1.125 rem   line-height 1.6
font.size.lg    → 20 px / 1.25 rem    line-height 1.5
font.size.xl    → 24 px / 1.5 rem     line-height 1.4
font.size.2xl   → 30 px / 1.875 rem   line-height 1.3
font.size.3xl   → 36 px / 2.25 rem    line-height 1.25
font.size.4xl   → 48 px / 3 rem       line-height 1.2
font.size.5xl   → 60 px / 3.75 rem    line-height 1.15
```

For Vietnamese content, **never go below 1.4 line-height on body sizes**; tone marks need vertical room.

### D.2 — Weights

```
font.weight.regular  → 400
font.weight.medium   → 500
font.weight.semibold → 600
font.weight.bold     → 700
```

Avoid 800/900 for small Vietnamese sizes; mark stems thicken and collide.

### D.3 — Semantic typography roles

```
typography.display      → font.size.5xl, weight.bold, line 1.15, letter-spacing -0.01em
typography.heading.h1   → font.size.4xl, weight.bold, line 1.2
typography.heading.h2   → font.size.3xl, weight.semibold, line 1.25
typography.heading.h3   → font.size.2xl, weight.semibold, line 1.3
typography.heading.h4   → font.size.xl, weight.semibold, line 1.4
typography.heading.h5   → font.size.lg, weight.semibold, line 1.5
typography.heading.h6   → font.size.md, weight.semibold, line 1.55
typography.body.lg      → font.size.md, weight.regular, line 1.6
typography.body         → font.size.base, weight.regular, line 1.6
typography.body.sm      → font.size.sm, weight.regular, line 1.55
typography.caption      → font.size.xs, weight.regular, line 1.5
typography.label        → font.size.sm, weight.medium, line 1.4
typography.button       → font.size.base, weight.semibold, line 1.4, letter-spacing 0.01em
typography.code         → mono family, font.size.sm, line 1.5
```

---

## Section E — Spacing Tokens

4 px base scale. Do not invent in-between values.

```
space.0    → 0
space.0.5  → 2 px
space.1    → 4 px
space.1.5  → 6 px
space.2    → 8 px
space.3    → 12 px
space.4    → 16 px
space.5    → 20 px
space.6    → 24 px
space.8    → 32 px
space.10   → 40 px
space.12   → 48 px
space.16   → 64 px
space.20   → 80 px
space.24   → 96 px
space.32   → 128 px
```

Semantic aliases (optional but useful):

```
spacing.gutter.tight    → space.2
spacing.gutter.default  → space.4
spacing.gutter.loose    → space.6
spacing.section.tight   → space.8
spacing.section.default → space.12
spacing.section.loose   → space.20
```

### Density modes

Some apps need a "compact" density (data-heavy desktop tools) and a "comfortable" density (mobile, marketing):

```
density.compact     → multiplier 0.875  (rows shrink to ~32 px)
density.comfortable → multiplier 1.0    (rows ~40 px)
density.spacious    → multiplier 1.125  (rows ~48 px, onboarding)
```

Apply density as a token modifier on container components, not by overriding spacing on each item.

---

## Section F — Radius Tokens

```
radius.none   → 0
radius.sm     → 4 px
radius.md     → 8 px
radius.lg     → 12 px
radius.xl     → 16 px
radius.2xl    → 24 px
radius.full   → 9999 px
```

Semantic mappings:

```
radius.button       → radius.md
radius.input        → radius.md
radius.card         → radius.lg
radius.modal        → radius.xl
radius.avatar       → radius.full
radius.pill         → radius.full
```

A friendly product feel uses radius.md to radius.xl; sharp/serious uses radius.sm to radius.md.

---

## Section G — Shadow / Elevation Tokens

```
shadow.xs  → 0 1px 2px rgba(15,23,42,.05)
shadow.sm  → 0 1px 3px rgba(15,23,42,.08), 0 1px 2px rgba(15,23,42,.06)
shadow.md  → 0 4px 6px rgba(15,23,42,.07), 0 2px 4px rgba(15,23,42,.05)
shadow.lg  → 0 10px 15px rgba(15,23,42,.08), 0 4px 6px rgba(15,23,42,.05)
shadow.xl  → 0 20px 25px rgba(15,23,42,.10), 0 8px 10px rgba(15,23,42,.04)
shadow.2xl → 0 25px 50px rgba(15,23,42,.18)
```

Dark theme: shadows are less visible — keep but reduce alpha by ~40%, add a subtle 1px border for separation.

Elevation semantic levels:

```
elevation.flat       → shadow.none
elevation.raised     → shadow.sm   (cards on canvas)
elevation.overlay    → shadow.lg   (popovers, dropdowns)
elevation.modal      → shadow.xl   (modals)
elevation.toast      → shadow.lg
```

---

## Section H — Motion Tokens

Pair with `references/07-interaction-and-motion.md`.

```
motion.duration.instant  → 50 ms
motion.duration.fast     → 150 ms
motion.duration.medium   → 250 ms
motion.duration.slow     → 400 ms
motion.duration.slowest  → 600 ms

motion.easing.standard  → cubic-bezier(0.4, 0, 0.2, 1)        ← in-out, default
motion.easing.entrance  → cubic-bezier(0, 0, 0.2, 1)           ← out
motion.easing.exit      → cubic-bezier(0.4, 0, 1, 1)           ← in
motion.easing.spring    → cubic-bezier(0.34, 1.56, 0.64, 1)    ← bouncy
```

All animations must respect `prefers-reduced-motion: reduce`.

---

## Section I — Breakpoint Tokens

```
breakpoint.xs  → 0       (mobile)
breakpoint.sm  → 640 px  (tablet)
breakpoint.md  → 768 px  (tablet wide)
breakpoint.lg  → 1024 px (PC)
breakpoint.xl  → 1280 px (PC wide)
breakpoint.2xl → 1536 px (PC ultra-wide)

container.max.xs  → 100%
container.max.sm  → 640 px
container.max.md  → 768 px
container.max.lg  → 1024 px
container.max.xl  → 1200 px
container.max.2xl → 1280 px       ← cap content at 1280; do not stretch indefinitely
```

The `1024 px` cut between Tablet and PC is the most important: nav patterns, density, and grid all change at that line.

---

## Section J — Z-Index Tokens

Always use tokens to avoid the "z-index: 99999" arms race.

```
zIndex.hide          → -1
zIndex.base          → 0
zIndex.docked        → 10   (sticky headers within content)
zIndex.dropdown      → 1000
zIndex.sticky        → 1100 (page-level sticky)
zIndex.banner        → 1200
zIndex.overlay       → 1300
zIndex.modal         → 1400
zIndex.popover       → 1500
zIndex.skipLink      → 1600
zIndex.toast         → 1700
zIndex.tooltip       → 1800
```

---

## Section K — Iconography Tokens

```
icon.size.xs  → 12 px
icon.size.sm  → 16 px
icon.size.md  → 20 px      ← default for inline-with-text
icon.size.lg  → 24 px      ← default for buttons / nav
icon.size.xl  → 32 px
icon.size.2xl → 40 px

icon.stroke.thin   → 1.5 px
icon.stroke.medium → 2 px  ← default
icon.stroke.bold   → 2.5 px
```

Pick a single icon family for the project (Lucide, Phosphor, Heroicons, Material Symbols, SF Symbols) and stay there. Mixed-family icon sets look cheap.

---

## Section L — Export Shapes

Pick the export shape based on the project's stack.

### L.1 — CSS Variables (universal, framework-agnostic)

```css
:root {
  --color-bg-canvas: #f8fafc;
  --color-bg-surface: #ffffff;
  --color-text-primary: #0f172a;
  --color-text-secondary: #334155;
  --color-action-primary-bg: #2563eb;
  --color-action-primary-bg-hover: #1d4ed8;
  --color-action-primary-fg: #ffffff;

  --font-family-sans: "Be Vietnam Pro", "Inter", system-ui, sans-serif;
  --font-size-base: 1rem;
  --line-height-base: 1.6;

  --space-4: 1rem;
  --radius-md: 0.5rem;
  --shadow-sm: 0 1px 3px rgba(15,23,42,.08), 0 1px 2px rgba(15,23,42,.06);

  --duration-fast: 150ms;
  --easing-standard: cubic-bezier(0.4, 0, 0.2, 1);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-canvas: #020617;
    --color-bg-surface: #0f172a;
    --color-text-primary: #f8fafc;
    --color-text-secondary: #cbd5e1;
    /* ... */
  }
}

[data-theme="dark"] {
  /* explicit overrides for theme toggle */
}
```

### L.2 — Tailwind Config

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{ts,tsx,js,jsx,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: {
          canvas: "var(--color-bg-canvas)",
          surface: "var(--color-bg-surface)",
        },
        text: {
          primary: "var(--color-text-primary)",
          secondary: "var(--color-text-secondary)",
        },
        action: {
          primary: {
            DEFAULT: "var(--color-action-primary-bg)",
            hover: "var(--color-action-primary-bg-hover)",
            fg: "var(--color-action-primary-fg)",
          },
        },
      },
      fontFamily: { sans: ["var(--font-family-sans)"] },
      borderRadius: { md: "var(--radius-md)" },
      screens: {
        sm: "640px", md: "768px", lg: "1024px", xl: "1280px", "2xl": "1536px",
      },
    },
  },
} satisfies Config;
```

CSS variables behind Tailwind keep the **single source of truth**.

### L.3 — Flutter `ThemeData`

```dart
// lib/theme/tokens.dart
import 'package:flutter/material.dart';

class AppColors {
  static const bgCanvas = Color(0xFFF8FAFC);
  static const bgSurface = Color(0xFFFFFFFF);
  static const textPrimary = Color(0xFF0F172A);
  static const textSecondary = Color(0xFF334155);
  static const actionPrimaryBg = Color(0xFF2563EB);
  static const actionPrimaryFg = Color(0xFFFFFFFF);
}

ThemeData buildLightTheme() {
  return ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.actionPrimaryBg,
      brightness: Brightness.light,
    ),
    textTheme: const TextTheme(
      displayLarge: TextStyle(fontSize: 60, height: 1.15, fontWeight: FontWeight.w700),
      headlineLarge: TextStyle(fontSize: 36, height: 1.25, fontWeight: FontWeight.w600),
      bodyLarge: TextStyle(fontSize: 16, height: 1.6),
      bodyMedium: TextStyle(fontSize: 14, height: 1.55),
    ),
    fontFamily: 'Be Vietnam Pro',
  );
}
```

### L.4 — SwiftUI

```swift
// Theme/Color+Tokens.swift
extension Color {
  static let bgCanvas    = Color(red: 0.97, green: 0.98, blue: 0.99)
  static let bgSurface   = Color.white
  static let textPrimary = Color(red: 0.06, green: 0.09, blue: 0.16)
  static let actionPrimaryBg = Color(red: 0.15, green: 0.39, blue: 0.92)
}

// Theme/Typography.swift
extension Font {
  static let appBody    = Font.custom("BeVietnamPro-Regular", size: 16)
  static let appHeading = Font.custom("BeVietnamPro-SemiBold", size: 24)
}
```

### L.5 — Jetpack Compose

```kotlin
// ui/theme/Tokens.kt
object AppColors {
  val BgCanvas = Color(0xFFF8FAFC)
  val BgSurface = Color(0xFFFFFFFF)
  val TextPrimary = Color(0xFF0F172A)
  val ActionPrimaryBg = Color(0xFF2563EB)
}

@Composable
fun AppTheme(useDark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
  val colors = if (useDark) darkColorScheme(...) else lightColorScheme(
    primary = AppColors.ActionPrimaryBg,
    background = AppColors.BgCanvas,
    surface = AppColors.BgSurface,
    onBackground = AppColors.TextPrimary
  )
  MaterialTheme(colorScheme = colors, typography = AppTypography, content = content)
}
```

### L.6 — Android XML (View system)

```xml
<!-- res/values/colors.xml -->
<resources>
  <color name="bg_canvas">#F8FAFC</color>
  <color name="bg_surface">#FFFFFF</color>
  <color name="text_primary">#0F172A</color>
  <color name="action_primary_bg">#2563EB</color>
</resources>

<!-- res/values/themes.xml -->
<style name="Theme.App" parent="Theme.Material3.Light.NoActionBar">
  <item name="colorPrimary">@color/action_primary_bg</item>
  <item name="android:colorBackground">@color/bg_canvas</item>
  <item name="android:textColorPrimary">@color/text_primary</item>
  <item name="fontFamily">@font/be_vietnam_pro</item>
</style>
```

### L.7 — PyQt5 / PySide6 (QSS)

```css
/* tokens.qss */
* {
  font-family: "Be Vietnam Pro", "Segoe UI", sans-serif;
  font-size: 14px;
  color: #0F172A;
}

QMainWindow, QDialog { background: #F8FAFC; }
QFrame#card { background: #FFFFFF; border-radius: 12px; padding: 16px; }

QPushButton.primary {
  background: #2563EB;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
}
QPushButton.primary:hover { background: #1D4ED8; }
QPushButton.primary:pressed { background: #1E40AF; }
QPushButton.primary:disabled { background: #94A3B8; color: #E2E8F0; }
```

### L.8 — WPF (XAML resource dictionary)

```xml
<!-- Theme/Tokens.xaml -->
<ResourceDictionary>
  <SolidColorBrush x:Key="BgCanvas"  Color="#F8FAFC"/>
  <SolidColorBrush x:Key="BgSurface" Color="#FFFFFF"/>
  <SolidColorBrush x:Key="TextPrimary" Color="#0F172A"/>
  <SolidColorBrush x:Key="ActionPrimaryBg" Color="#2563EB"/>
  <FontFamily x:Key="FontSans">Be Vietnam Pro, Segoe UI</FontFamily>
  <sys:Double x:Key="FontSizeBase">14</sys:Double>
</ResourceDictionary>
```

### L.9 — Design Tokens JSON (Style Dictionary / DTCG-compatible)

```json
{
  "color": {
    "bg": {
      "canvas":  { "$value": "{color.neutral.50}", "$type": "color" },
      "surface": { "$value": "{color.neutral.0}",  "$type": "color" }
    },
    "text": {
      "primary": { "$value": "{color.neutral.900}", "$type": "color" }
    }
  },
  "space": { "4": { "$value": "16px", "$type": "dimension" } }
}
```

Use this when the project explicitly wants tokens consumable by Figma + code via Style Dictionary or Tokens Studio.

---

## Section M — Theming (Light + Dark)

The token system is theme-agnostic by design. To support dark mode:

1. Define every primitive in both light and dark.
2. Map semantics to primitives **once** per theme.
3. Components reference semantics — they never branch on theme.
4. Toggle theme via `data-theme="dark"` on `<html>` (Web), `Theme.of(context).brightness` (Flutter), `colorScheme` (Compose), `preferredColorScheme` (SwiftUI), `app.setStyleSheet(load_qss(theme))` (PyQt5).
5. Persist user choice; SSR-hydrate without flash on Web.

If the project does not need dark mode, document that as an explicit non-goal so it isn't treated as oversight.

---

## Deliverables

- Primitives table for color / type sizes / spacing / radius / shadow / motion / breakpoints / z-index / icons
- Semantics table mapping per theme
- WCAG contrast verification table
- Export shape ready for the project (CSS vars / Tailwind / Flutter / SwiftUI / Compose / XML / QSS / WPF / JSON)
- Documented decisions on dark mode and any deviations

---

## Required Practices

- Always model in two tiers: primitives + semantics.
- Always verify contrast for every text/background pairing in every theme.
- Always cap content max-width on PC; never stretch text beyond ~70 chars per line.
- Always use OKLCH or perceptual scales when generating ramps from a single brand color.

## Prohibited Practices

- Do not bake raw color values into component CSS / widget files.
- Do not invent in-between spacing values; use the scale.
- Do not theme via component-level conditionals; theme via token swap.
- Do not skip dark mode without an explicit user decision documented as a non-goal.
