# Vietnamese Typography & Localization Guidelines

Typography specifications for multi-platform interfaces, engineered to eliminate diacritics clipping and seamlessly handle Vietnamese string lengths.

---

## 1. Diacritics Stacking & Line-Height Standards

Vietnamese utilizes a stacked diacritical tone system (huyền, sắc, hỏi, ngã, nặng) paired with modified vowel base glyphs (ă, â, ê, ô, ơ, ư). The vertical height of compounded glyphs frequently exceeds standard Latin font bounding boxes.

### 1.1. Mandatory Line-Height Rules
- **Absolute Requirement**: Line-height (`line-height`) for Vietnamese body copy, form inputs, and buttons must be set between **1.4 and 1.6** (140% - 160%).
- **Strict Prohibition**: Never apply `line-height: 1.0` or `1.1` to Vietnamese text. Doing so causes severe vertical **clipping of top accent marks or bottom dots** across iOS Safari, Android, and web engines.
- For large headings (Display, H1): Minimum `line-height` is **1.25 to 1.35**.

---

## 2. Modular Type Scale

Recommended scales: **1.200 (Minor Third)** for dense productivity apps; **1.250 (Major Third)** for marketing sites and game menus.

| Style Name | Desktop Size | Mobile Size | Line-height | Font-weight | Usage Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display** | 32px (2.0rem) | 28px (1.75rem)| 44px (1.38) | 700 Bold | Hero headers, main game titles |
| **H1** | 24px (1.5rem) | 22px (1.375rem)| 34px (1.42) | 600 SemiBold| Main view headers, modal titles |
| **H2** | 20px (1.25rem)| 18px (1.125rem)| 28px (1.40) | 600 SemiBold| Card headers, section dividers |
| **H3** | 16px (1.0rem) | 16px (1.0rem) | 24px (1.50) | 600 SemiBold| Subheadings, table headers |
| **Body (Default)**| 14px (0.875rem)| 14px (0.875rem)| 22px (1.57) | 400 Regular | Standard body copy, inputs |
| **Body Medium** | 14px (0.875rem)| 14px (0.875rem)| 22px (1.57) | 500 Medium | Button labels, navigation links |
| **Caption** | 12px (0.75rem)| 12px (0.75rem) | 18px (1.50) | 400 / 500 | Tooltips, timestamps, badge labels |

---

## 3. Recommended Vietnamese Font Stacks

| Purpose | Recommended Font Stack |
| :--- | :--- |
| **System Native (Zero Latency)** | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` |
| **Modern Application (Web/Mobile App)** | `"Be Vietnam Pro", "Inter", "Plus Jakarta Sans", sans-serif` *(Be Vietnam Pro is explicitly engineered for Vietnamese diacritics)* |
| **Game UI / High-Tech Theme** | `"Chakra Petch", "Rajdhani", "Montserrat", sans-serif` *(Verify tone mark alignment during testing)* |
| **Desktop Tool / Monospace** | `"JetBrains Mono", "Fira Code", "SF Mono", Consolas, monospace` |

---

## 4. Text Expansion Engineering

- **String Expansion Factor**: Vietnamese text expands by approximately **20% to 30%** compared to English equivalents (e.g., `Save` → `Lưu thay đổi`, `Settings` → `Cài đặt hệ thống`, `Delete account` → `Xóa tài khoản vĩnh viễn`).
- **Layout Safeguards**:
  1. Never assign fixed width (`width: 120px`) to buttons or action pills. Apply inline padding (`padding: 8px 16px; width: auto; min-width: 80px;`).
  2. Data tables and card headers must support automatic text wrapping (`word-break: break-word; text-overflow: ellipsis;`).
  3. Avoid full uppercase transformation (`text-transform: uppercase`) on long Vietnamese sentences because vertical accent stacking diminishes reading speed.

---

## 5. Regional Formatting Conventions

- **Currency**: `100.000 ₫` or `100.000 VNĐ` (Period as thousands separator, non-breaking space before symbol).
- **Date**: `DD/MM/YYYY` (e.g., `10/09/2026`).
- **Time**: 24-Hour format `14:30` or `14:30:00`.
- **Decimals**: Comma as decimal separator in standard Vietnamese accounting (`3,14`).
