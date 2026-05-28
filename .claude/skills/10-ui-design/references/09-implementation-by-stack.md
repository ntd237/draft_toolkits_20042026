# Phase 9 — Implementation by Stack

## Objective

Translate design into implementation that fits the project's stack — or produce specs precise enough that another engineer can implement without questions.

This file gives a **minimal but production-ready** starting pattern per stack. Adapt to project conventions; do not rewrite the project's architecture.

---

## Section A — Web — React + Tailwind + CSS Vars

### A.1 — Token File

```css
/* src/styles/tokens.css */
:root {
  --color-bg-canvas:        #f8fafc;
  --color-bg-surface:       #ffffff;
  --color-text-primary:     #0f172a;
  --color-text-secondary:   #334155;
  --color-text-muted:       #64748b;
  --color-border-subtle:    #e2e8f0;
  --color-border-default:   #cbd5e1;
  --color-border-focus:     #3b82f6;
  --color-action-primary:        #2563eb;
  --color-action-primary-hover:  #1d4ed8;
  --color-action-primary-active: #1e40af;
  --color-action-primary-fg:     #ffffff;
  --color-feedback-danger:       #dc2626;
  --color-feedback-success:      #16a34a;
  --color-feedback-warning:      #d97706;

  --font-sans: "Be Vietnam Pro", "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-xl: 16px;
  --shadow-sm: 0 1px 3px rgba(15,23,42,.08), 0 1px 2px rgba(15,23,42,.06);
  --shadow-md: 0 4px 6px rgba(15,23,42,.07), 0 2px 4px rgba(15,23,42,.05);
  --shadow-lg: 0 10px 15px rgba(15,23,42,.08), 0 4px 6px rgba(15,23,42,.05);

  --duration-fast: 150ms;
  --duration-medium: 250ms;
  --easing-standard: cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="dark"] {
  --color-bg-canvas:      #020617;
  --color-bg-surface:     #0f172a;
  --color-text-primary:   #f8fafc;
  --color-text-secondary: #cbd5e1;
  --color-text-muted:     #94a3b8;
  --color-border-subtle:  #1e293b;
  --color-border-default: #334155;
  /* ... */
}
```

### A.2 — `tailwind.config.ts`

```ts
import type { Config } from "tailwindcss";

export default {
  content: ["./src/**/*.{ts,tsx}"],
  darkMode: ["class", '[data-theme="dark"]'],
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
          muted: "var(--color-text-muted)",
        },
        border: {
          subtle: "var(--color-border-subtle)",
          DEFAULT: "var(--color-border-default)",
          focus: "var(--color-border-focus)",
        },
        action: {
          primary: {
            DEFAULT: "var(--color-action-primary)",
            hover: "var(--color-action-primary-hover)",
            active: "var(--color-action-primary-active)",
            fg: "var(--color-action-primary-fg)",
          },
        },
        feedback: {
          danger: "var(--color-feedback-danger)",
          success: "var(--color-feedback-success)",
          warning: "var(--color-feedback-warning)",
        },
      },
      fontFamily: { sans: ["var(--font-sans)"], mono: ["var(--font-mono)"] },
      borderRadius: {
        sm: "var(--radius-sm)",
        DEFAULT: "var(--radius-md)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)",
      },
      boxShadow: {
        sm: "var(--shadow-sm)",
        DEFAULT: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
      },
      transitionDuration: { fast: "150ms", DEFAULT: "250ms" },
      transitionTimingFunction: {
        standard: "cubic-bezier(0.4, 0, 0.2, 1)",
        entrance: "cubic-bezier(0, 0, 0.2, 1)",
        exit: "cubic-bezier(0.4, 0, 1, 1)",
      },
      screens: {
        sm: "640px", md: "768px", lg: "1024px", xl: "1280px", "2xl": "1536px",
      },
    },
  },
} satisfies Config;
```

### A.3 — Button Component (full states)

```tsx
// src/components/ui/Button.tsx
import { forwardRef, type ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leadingIcon?: React.ReactNode;
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { variant = "primary", size = "md", isLoading, leadingIcon, className, children, disabled, ...rest },
    ref
  ) => {
    const variants: Record<string, string> = {
      primary:
        "bg-action-primary text-action-primary-fg hover:bg-action-primary-hover active:bg-action-primary-active",
      secondary:
        "bg-bg-surface text-text-primary border border-border hover:bg-bg-surface/90",
      ghost: "text-text-primary hover:bg-bg-surface/80",
      destructive:
        "bg-feedback-danger text-white hover:opacity-90 active:opacity-80",
    };
    const sizes: Record<string, string> = {
      sm: "h-8  px-3 text-sm",
      md: "h-10 px-4 text-base",
      lg: "h-12 px-5 text-base",
    };
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        aria-busy={isLoading}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded font-semibold",
          "transition-colors duration-fast ease-standard",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus focus-visible:ring-offset-2",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          variants[variant],
          sizes[size],
          className
        )}
        {...rest}
      >
        {isLoading ? <Spinner aria-hidden /> : leadingIcon}
        <span>{children}</span>
      </button>
    );
  }
);
Button.displayName = "Button";
```

---

## Section B — Web — Next.js + `next/font`

```tsx
// app/fonts.ts
import { Be_Vietnam_Pro } from "next/font/google";
export const sans = Be_Vietnam_Pro({
  subsets: ["latin", "latin-ext", "vietnamese"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-sans",
  display: "swap",
});

// app/layout.tsx
import { sans } from "./fonts";
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className={sans.variable} suppressHydrationWarning>
      <body className="bg-bg-canvas text-text-primary font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
```

---

## Section C — Web — Vue 3 + Nuxt + Tailwind

```vue
<!-- components/Button.vue -->
<script setup lang="ts">
withDefaults(defineProps<{
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  disabled?: boolean
}>(), { variant: 'primary', size: 'md' })
</script>

<template>
  <button
    :disabled="disabled || isLoading"
    :aria-busy="isLoading"
    :class="[
      'inline-flex items-center justify-center gap-2 rounded font-semibold',
      'transition-colors duration-150 ease-[cubic-bezier(0.4,0,0.2,1)]',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus focus-visible:ring-offset-2',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      variantClasses[variant],
      sizeClasses[size],
    ]"
  >
    <slot />
  </button>
</template>
```

Locale config in `nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  app: { head: { htmlAttrs: { lang: 'vi' } } },
  modules: ['@nuxtjs/i18n'],
  i18n: {
    locales: [{ code: 'vi', iso: 'vi-VN', name: 'Tiếng Việt' }],
    defaultLocale: 'vi',
  },
})
```

---

## Section D — Desktop — Electron / Tauri

Same React/Vue stack as Web. Add desktop-specific overrides:

```ts
// src/lib/desktop.ts
export function setWindowDraggable(selector: string) {
  // CSS approach
  document.querySelectorAll(selector).forEach((el) => {
    (el as HTMLElement).style.webkitAppRegion = "drag";
  });
}
```

```css
/* Custom title bar */
.titlebar {
  -webkit-app-region: drag;
  height: 32px;
}
.titlebar button { -webkit-app-region: no-drag; }
```

Wire native menus (Tauri example):

```rust
// src-tauri/src/main.rs
use tauri::{Menu, MenuItem, Submenu};

let menu = Menu::new()
  .add_submenu(Submenu::new("File", Menu::new()
    .add_item(MenuItem::new("Mới", "new").accelerator("CmdOrCtrl+N"))
    .add_item(MenuItem::new("Mở", "open").accelerator("CmdOrCtrl+O"))));
```

---

## Section E — Desktop — PyQt5 / PySide6

### E.1 — Token QSS

```css
/* resources/styles/tokens.qss */

* {
  font-family: "Be Vietnam Pro";
  font-size: 14px;
  color: #0F172A;
}

QMainWindow, QDialog { background: #F8FAFC; }

QFrame[role="card"] {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 16px;
}

QPushButton[variant="primary"] {
  background: #2563EB;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  min-height: 32px;
}
QPushButton[variant="primary"]:hover  { background: #1D4ED8; }
QPushButton[variant="primary"]:pressed { background: #1E40AF; }
QPushButton[variant="primary"]:disabled {
  background: #94A3B8;
  color: #E2E8F0;
}

QPushButton[variant="secondary"] {
  background: #FFFFFF;
  color: #0F172A;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 500;
  min-height: 32px;
}
QPushButton[variant="secondary"]:hover { background: #F1F5F9; }

QLineEdit {
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  padding: 6px 12px;
  min-height: 32px;
}
QLineEdit:focus { border-color: #3B82F6; outline: none; }
QLineEdit:disabled { background: #F1F5F9; color: #94A3B8; }
```

### E.2 — App bootstrap (Vietnamese fonts + QSS)

```python
# main.py
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont

def load_fonts():
    fonts_dir = Path(__file__).parent / "resources" / "fonts"
    for f in fonts_dir.glob("BeVietnamPro-*.ttf"):
        QFontDatabase.addApplicationFont(str(f))

def load_qss(app: QApplication):
    qss_path = Path(__file__).parent / "resources" / "styles" / "tokens.qss"
    app.setStyleSheet(qss_path.read_text(encoding="utf-8"))

def main():
    app = QApplication(sys.argv)
    load_fonts()
    app.setFont(QFont("Be Vietnam Pro", 14))
    load_qss(app)
    # ... main window setup
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
```

### E.3 — Responsive PyQt window

```python
from PyQt5.QtWidgets import QStackedWidget, QSplitter
from PyQt5.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    BREAKPOINT_TABLET = 768
    BREAKPOINT_PC = 1024

    def resizeEvent(self, event):
        w = self.width()
        if w < self.BREAKPOINT_TABLET:
            self.apply_mobile_layout()
        elif w < self.BREAKPOINT_PC:
            self.apply_tablet_layout()
        else:
            self.apply_pc_layout()
        super().resizeEvent(event)
```

---

## Section F — Mobile — Flutter

### F.1 — Theme

```dart
// lib/theme/tokens.dart
import 'package:flutter/material.dart';

class AppColors {
  static const bgCanvas      = Color(0xFFF8FAFC);
  static const bgSurface     = Color(0xFFFFFFFF);
  static const textPrimary   = Color(0xFF0F172A);
  static const textSecondary = Color(0xFF334155);
  static const actionPrimary = Color(0xFF2563EB);
  static const actionPrimaryHover = Color(0xFF1D4ED8);
  static const actionPrimaryFg    = Color(0xFFFFFFFF);
  static const borderDefault = Color(0xFFCBD5E1);
  static const borderFocus   = Color(0xFF3B82F6);
}

ThemeData buildLightTheme() {
  return ThemeData(
    useMaterial3: true,
    fontFamily: 'Be Vietnam Pro',
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.actionPrimary,
      brightness: Brightness.light,
    ),
    textTheme: const TextTheme(
      displayLarge:  TextStyle(fontSize: 60, height: 1.15, fontWeight: FontWeight.w700),
      headlineLarge: TextStyle(fontSize: 36, height: 1.25, fontWeight: FontWeight.w600),
      bodyLarge:     TextStyle(fontSize: 16, height: 1.6),
      bodyMedium:    TextStyle(fontSize: 14, height: 1.55),
      labelLarge:    TextStyle(fontSize: 14, height: 1.4, fontWeight: FontWeight.w500),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.actionPrimary,
        foregroundColor: AppColors.actionPrimaryFg,
        minimumSize: const Size(0, 48),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        textStyle: const TextStyle(fontWeight: FontWeight.w600),
      ),
    ),
  );
}
```

### F.2 — Locale + responsive layout

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

class App extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ứng dụng',
      theme: buildLightTheme(),
      darkTheme: buildDarkTheme(),
      locale: const Locale('vi', 'VN'),
      supportedLocales: const [Locale('vi', 'VN'), Locale('en', 'US')],
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      home: const HomeShell(),
    );
  }
}

// Responsive shell
class HomeShell extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth >= 1024) return PcLayout();
        if (constraints.maxWidth >= 640)  return TabletLayout();
        return MobileLayout();
      },
    );
  }
}
```

---

## Section G — Mobile — React Native (Expo)

### G.1 — Theme provider

```tsx
// theme/index.ts
export const tokens = {
  color: {
    bgCanvas: "#F8FAFC",
    bgSurface: "#FFFFFF",
    textPrimary: "#0F172A",
    actionPrimary: "#2563EB",
    actionPrimaryFg: "#FFFFFF",
    borderDefault: "#CBD5E1",
    borderFocus: "#3B82F6",
  },
  font: {
    sans: "BeVietnamPro-Regular",
    sansMedium: "BeVietnamPro-Medium",
    sansSemibold: "BeVietnamPro-SemiBold",
    sansBold: "BeVietnamPro-Bold",
  },
  radius: { sm: 4, md: 8, lg: 12, xl: 16 },
  spacing: { 1: 4, 2: 8, 3: 12, 4: 16, 6: 24, 8: 32 },
};
```

### G.2 — Button

```tsx
// components/Button.tsx
import { Pressable, Text, StyleSheet, ActivityIndicator } from "react-native";
import { tokens } from "../theme";

export function Button({
  variant = "primary",
  isLoading = false,
  onPress,
  children,
}) {
  return (
    <Pressable
      onPress={onPress}
      disabled={isLoading}
      style={({ pressed }) => [
        styles.base,
        variant === "primary" && styles.primary,
        pressed && styles.pressed,
      ]}
    >
      {isLoading
        ? <ActivityIndicator color={tokens.color.actionPrimaryFg} />
        : <Text style={styles.label}>{children}</Text>}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    minHeight: 48,
    paddingHorizontal: 20,
    borderRadius: tokens.radius.md,
    alignItems: "center",
    justifyContent: "center",
  },
  primary: { backgroundColor: tokens.color.actionPrimary },
  pressed: { opacity: 0.92 },
  label: {
    color: tokens.color.actionPrimaryFg,
    fontFamily: tokens.font.sansSemibold,
    fontSize: 16,
  },
});
```

---

## Section H — Mobile — SwiftUI

### H.1 — Color + Font extensions

```swift
// Theme/Color+Tokens.swift
extension Color {
  static let bgCanvas    = Color(red: 0.97, green: 0.98, blue: 0.99)
  static let bgSurface   = Color.white
  static let textPrimary = Color(red: 0.06, green: 0.09, blue: 0.16)
  static let actionPrimary = Color(red: 0.15, green: 0.39, blue: 0.92)
  static let actionPrimaryFg = Color.white
}

// Theme/Font+Tokens.swift
extension Font {
  static func appBody(size: CGFloat = 16) -> Font {
    .custom("BeVietnamPro-Regular", size: size)
  }
  static func appButton() -> Font {
    .custom("BeVietnamPro-SemiBold", size: 16)
  }
}
```

### H.2 — Button

```swift
import SwiftUI

struct AppButton: View {
  enum Variant { case primary, secondary }
  let title: String
  var variant: Variant = .primary
  var isLoading: Bool = false
  let action: () -> Void

  var body: some View {
    Button(action: action) {
      ZStack {
        if isLoading { ProgressView().tint(.actionPrimaryFg) }
        else { Text(title).font(.appButton()) }
      }
      .frame(maxWidth: .infinity, minHeight: 48)
      .background(variant == .primary ? Color.actionPrimary : Color.bgSurface)
      .foregroundColor(variant == .primary ? .actionPrimaryFg : .textPrimary)
      .cornerRadius(8)
    }
    .disabled(isLoading)
    .accessibilityLabel(Text(title))
  }
}
```

---

## Section I — Mobile — Jetpack Compose (Android)

### I.1 — Theme

```kotlin
// ui/theme/Tokens.kt
object AppColors {
  val BgCanvas = Color(0xFFF8FAFC)
  val BgSurface = Color(0xFFFFFFFF)
  val TextPrimary = Color(0xFF0F172A)
  val ActionPrimary = Color(0xFF2563EB)
  val ActionPrimaryFg = Color(0xFFFFFFFF)
}

val BeVietnamPro = FontFamily(
  Font(R.font.be_vietnam_pro_regular, FontWeight.Normal),
  Font(R.font.be_vietnam_pro_semibold, FontWeight.SemiBold),
  Font(R.font.be_vietnam_pro_bold, FontWeight.Bold),
)

val AppTypography = Typography(
  bodyLarge = TextStyle(fontFamily = BeVietnamPro, fontSize = 16.sp, lineHeight = 25.sp),
  labelLarge = TextStyle(fontFamily = BeVietnamPro, fontSize = 16.sp, fontWeight = FontWeight.SemiBold),
  headlineMedium = TextStyle(fontFamily = BeVietnamPro, fontSize = 28.sp, lineHeight = 36.sp, fontWeight = FontWeight.SemiBold),
)

@Composable
fun AppTheme(useDark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
  val colors = if (useDark) {
    darkColorScheme(primary = AppColors.ActionPrimary, background = Color(0xFF020617))
  } else {
    lightColorScheme(
      primary = AppColors.ActionPrimary,
      background = AppColors.BgCanvas,
      surface = AppColors.BgSurface,
      onBackground = AppColors.TextPrimary,
    )
  }
  MaterialTheme(colorScheme = colors, typography = AppTypography, content = content)
}
```

### I.2 — Button

```kotlin
@Composable
fun AppButton(
  text: String,
  modifier: Modifier = Modifier,
  isLoading: Boolean = false,
  onClick: () -> Unit,
) {
  Button(
    onClick = onClick,
    enabled = !isLoading,
    modifier = modifier.heightIn(min = 48.dp),
    colors = ButtonDefaults.buttonColors(
      containerColor = AppColors.ActionPrimary,
      contentColor = AppColors.ActionPrimaryFg,
    ),
    shape = RoundedCornerShape(8.dp),
  ) {
    if (isLoading) {
      CircularProgressIndicator(modifier = Modifier.size(20.dp), color = AppColors.ActionPrimaryFg)
    } else {
      Text(text)
    }
  }
}
```

---

## Section J — Lightweight Web — Gradio / Streamlit

### J.1 — Gradio (custom CSS)

```python
import gradio as gr

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap&subset=vietnamese');
* { font-family: 'Be Vietnam Pro', sans-serif; }
.gradio-container { background: #F8FAFC; }
.primary-btn {
  background: #2563EB !important;
  color: #FFF !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  min-height: 44px;
}
.primary-btn:hover { background: #1D4ED8 !important; }
"""

with gr.Blocks(css=custom_css, title="Ứng dụng") as demo:
    gr.Markdown("# Trợ lý AI tiếng Việt")
    with gr.Row():
        with gr.Column(scale=2):
            inp = gr.Textbox(label="Câu hỏi", placeholder="Nhập câu hỏi...")
            btn = gr.Button("Gửi", elem_classes="primary-btn")
        with gr.Column(scale=3):
            out = gr.Textbox(label="Trả lời", interactive=False)
    btn.click(fn=lambda q: f"Đã nhận: {q}", inputs=inp, outputs=out)

demo.launch()
```

### J.2 — Streamlit (custom CSS)

```python
import streamlit as st

st.set_page_config(page_title="Ứng dụng", layout="wide")
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap&subset=vietnamese" rel="stylesheet">
<style>
* { font-family: 'Be Vietnam Pro', sans-serif; }
.stButton > button {
  background: #2563EB; color: #FFF; border: none;
  border-radius: 8px; padding: 10px 20px; font-weight: 600;
  min-height: 44px;
}
.stButton > button:hover { background: #1D4ED8; }
</style>
""", unsafe_allow_html=True)
```

---

## Section K — Asset Management & Performance

- Icons: ship as SVG via icon font (subsetted) or per-icon imports (lucide-react, @heroicons).
- Illustrations: SVG when geometric, AVIF/WebP for raster, with PNG fallback.
- Fonts: see `references/03-vietnamese-typography.md` — subset and `font-display: swap`.
- Images: `<picture>` with `srcset` for Web; `Image` widget with caching for Flutter; `react-native-fast-image` for RN; native cached image for SwiftUI / Compose.
- Lazy-load below-the-fold images and components.

---

## Required Practices

- Always declare scope before writing implementation files.
- Always reference tokens, never raw values, in component code.
- Always include accessibility attributes (`aria-*`, `accessibilityLabel`, `Modifier.semantics`).
- Always meet platform's minimum touch target (44 / 48 px).
- Always include the Vietnamese subset when loading fonts.
- Always export tokens in the format the project's stack consumes natively.

## Prohibited Practices

- Do not write tokens to a file in a format the project doesn't consume (e.g., JSON when the project is Tailwind-only).
- Do not introduce a new component framework when the project already has one.
- Do not hardcode pixel values inside component code.
- Do not skip ARIA / accessibility hooks because "the design didn't mention them".
- Do not write large stack-specific code blocks without first confirming the user wants code (versus specs).
