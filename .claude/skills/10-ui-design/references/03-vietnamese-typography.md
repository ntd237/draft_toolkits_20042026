# Phase 3 — Vietnamese Typography

## Objective

Choose, load, and tune fonts so Vietnamese reads cleanly across every size and weight, on every platform class. Vietnamese stacks marks above and below base letters (ố, ầ, ễ, ặ, ữ, ụ); a font that "looks fine in English" can collapse, clip, or collide once those marks land.

By the end of this phase you must have:

- A primary sans family with **complete Vietnamese diacritic coverage**
- Optional secondary (heading or display) family, also Vietnamese-safe
- A monospace family with Vietnamese coverage (for code/data UIs)
- A font-loading strategy per platform class (Web / Desktop / Mobile)
- A type scale tuned for Vietnamese line-heights and weights
- Verified rendering with the standardized Vietnamese diacritic test string

---

## Section A — Font Selection Criteria

### A.1 — Required: Full Vietnamese Coverage

Every Vietnamese vowel can take 5 tone marks (acute, grave, hook above, tilde, dot below) on top of 3 base modifications (ă, â, ê, ô, ơ, ư, đ). The font must support **all** stacked combinations, not just basic accents shared with French/Spanish.

### A.2 — Standard Diacritic Test String

Render this string at every size you plan to ship:

```
Bạn cần tài khoản — Đăng nhập để tiếp tục, hoặc tạo mới ngay.
Nguyễn Trường Dũng — Cộng đồng người dùng Việt Nam.
ố ầ ễ ặ ữ ụ ợ ử ằ ỗ ẩ ọ ẹ ỉ ỳ ỵ
ĐẢM BẢO ĐỦ DẤU CHÌM VÀ DẤU NỔI Ở MỌI KÍCH THƯỚC.
```

If any of: tone marks fall on the cap line, marks merge into the letter above, dots-below clash with descenders, or the bottom dot in `ạ`/`ụ` is missing — **pick a different font**.

### A.3 — Curated Vietnamese-Capable Families (Open Source)

Recommended primary (sans) families — all Google Fonts, all confirmed for full Vietnamese:

| Family | Notes | Best for |
|---|---|---|
| **Be Vietnam Pro** | Designed in Vietnam; tone marks tuned; 9 weights | Vietnamese-first products |
| **Inter** | Excellent Vietnamese coverage; OpenType features rich | General product UI |
| **IBM Plex Sans** | Strong neutral; good x-height; full coverage | Documentation, productivity |
| **Manrope** | Geometric, modern; full coverage | Marketing surfaces |
| **Roboto / Roboto Flex** | Battle-tested; default on Android | Mobile-leaning products |
| **Public Sans** | US Government library; strong defaults | Civic / serious products |
| **Source Sans 3** | Adobe; excellent legibility | Long-form reading |
| **Nunito Sans / Nunito** | Friendly, rounded | Consumer apps |
| **DM Sans** | Compact, modern | Information-dense layouts |

For headings or display, also Vietnamese-safe:

| Family | Best for |
|---|---|
| **Be Vietnam Pro (Bold/Black)** | Titles in Vietnamese-first apps |
| **Lora** (serif) | Editorial / long-form |
| **Source Serif 4** | Reading-heavy documents |
| **Bricolage Grotesque** | Marketing / brand display |

For mono (code, monospaced data):

| Family | Notes |
|---|---|
| **JetBrains Mono** | Vietnamese coverage; ligatures |
| **Fira Code** | Vietnamese coverage; ligatures |
| **IBM Plex Mono** | Pairs with IBM Plex Sans |

### A.4 — Avoid

- Display / handwriting / decorative fonts unless explicitly asked.
- Fonts that ship Vietnamese only via fallback (marks render in a different family — visible metric jump).
- Variable fonts whose `wght` axis pushes diacritics into the body at high weights.
- "Latin-only" fonts paired with system fallback for Vietnamese — produces inconsistent metrics across letters in the same word.

---

## Section B — Loading Strategy by Platform

### B.1 — Web — Google Fonts CDN

Always include both `latin-ext` and `vietnamese` subsets. Do **not** rely on `latin` alone.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link
  href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap&subset=vietnamese,latin-ext,latin"
  rel="stylesheet"
>
```

`display=swap` avoids invisible-text-flash. For above-the-fold critical text, prefer `display=optional` and self-host so layout never shifts.

### B.2 — Web — Self-Hosting (preferred for production)

Self-hosting eliminates third-party requests and lets you ship only the subsets you need. Generate woff2 subsets via `glyphhanger`, `fonttools`, or download Google's split files.

```css
@font-face {
  font-family: "Be Vietnam Pro";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("/fonts/be-vietnam-pro/latin.woff2") format("woff2");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: "Be Vietnam Pro";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("/fonts/be-vietnam-pro/latin-ext.woff2") format("woff2");
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: "Be Vietnam Pro";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("/fonts/be-vietnam-pro/vietnamese.woff2") format("woff2");
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
```

Repeat per weight (400, 500, 600, 700). Do not preload more than 2 weights for the critical path.

### B.3 — Web — Next.js (`next/font`)

```ts
// app/fonts.ts
import { Be_Vietnam_Pro } from "next/font/google";

export const sans = Be_Vietnam_Pro({
  subsets: ["latin", "latin-ext", "vietnamese"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-sans",
  display: "swap",
});
```

```tsx
// app/layout.tsx
import { sans } from "./fonts";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className={sans.variable}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

### B.4 — Web — Variable Fonts

```css
@font-face {
  font-family: "Inter Variable";
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url("/fonts/inter-variable.woff2") format("woff2-variations");
  unicode-range: /* Vietnamese range */;
}
```

Single variable file ≪ multiple static weights for total bytes.

### B.5 — Web Performance Budget

- Total font weight ≤ 120 KB on critical path (gzip)
- Preload **only** the Latin + Latin-Ext + Vietnamese subset for the primary weight (400) and one heading weight (600 or 700)
- Lazy-load other weights via normal `<link>`
- Use `font-display: swap` (not `block`)

### B.6 — Flutter

Bundle font files in `assets/fonts/` and declare in `pubspec.yaml`:

```yaml
flutter:
  fonts:
    - family: Be Vietnam Pro
      fonts:
        - asset: assets/fonts/BeVietnamPro-Regular.ttf
        - asset: assets/fonts/BeVietnamPro-Medium.ttf
          weight: 500
        - asset: assets/fonts/BeVietnamPro-SemiBold.ttf
          weight: 600
        - asset: assets/fonts/BeVietnamPro-Bold.ttf
          weight: 700
```

Use in `ThemeData(fontFamily: 'Be Vietnam Pro')`. Verify the TTF includes the `vietnamese` subset (some "free" downloads ship Latin only).

### B.7 — React Native

```bash
# expo
npx expo install expo-font
```

```tsx
import { useFonts } from "expo-font";

const [loaded] = useFonts({
  "BeVietnamPro-Regular": require("./assets/fonts/BeVietnamPro-Regular.ttf"),
  "BeVietnamPro-SemiBold": require("./assets/fonts/BeVietnamPro-SemiBold.ttf"),
});
```

### B.8 — SwiftUI / UIKit

1. Add the `.ttf` / `.otf` files to the Xcode project.
2. Register them in `Info.plist` under `UIAppFonts`:

```xml
<key>UIAppFonts</key>
<array>
  <string>BeVietnamPro-Regular.ttf</string>
  <string>BeVietnamPro-SemiBold.ttf</string>
  <string>BeVietnamPro-Bold.ttf</string>
</array>
```

3. Use:

```swift
Text("Đăng nhập").font(.custom("BeVietnamPro-Regular", size: 16))
```

### B.9 — Jetpack Compose / Android XML

1. Drop fonts in `app/src/main/res/font/be_vietnam_pro_regular.ttf`.
2. Define a font family resource:

```xml
<!-- res/font/be_vietnam_pro.xml -->
<font-family xmlns:android="http://schemas.android.com/apk/res/android">
  <font android:fontStyle="normal" android:fontWeight="400" android:font="@font/be_vietnam_pro_regular"/>
  <font android:fontStyle="normal" android:fontWeight="600" android:font="@font/be_vietnam_pro_semibold"/>
  <font android:fontStyle="normal" android:fontWeight="700" android:font="@font/be_vietnam_pro_bold"/>
</font-family>
```

Use in Compose typography:

```kotlin
val BeVietnamPro = FontFamily(
  Font(R.font.be_vietnam_pro_regular, FontWeight.Normal),
  Font(R.font.be_vietnam_pro_semibold, FontWeight.SemiBold),
  Font(R.font.be_vietnam_pro_bold, FontWeight.Bold),
)
```

### B.10 — PyQt5 / PySide6

```python
from PyQt5.QtGui import QFontDatabase, QFont

# At app start
QFontDatabase.addApplicationFont("resources/fonts/BeVietnamPro-Regular.ttf")
QFontDatabase.addApplicationFont("resources/fonts/BeVietnamPro-SemiBold.ttf")
QFontDatabase.addApplicationFont("resources/fonts/BeVietnamPro-Bold.ttf")

app.setFont(QFont("Be Vietnam Pro", 14))
```

For Tauri/Electron desktop apps: ship the woff2 files in the bundled webview and use the same `@font-face` strategy as Web.

### B.11 — WPF

Place TTFs in the project, set Build Action to `Resource`. Reference:

```xml
<TextBlock FontFamily="pack://application:,,,/Resources/Fonts/#Be Vietnam Pro"
           FontSize="14" Text="Đăng nhập"/>
```

---

## Section C — Type Scale Tuned for Vietnamese

The base scale from `02-design-system-foundations.md` already targets line-heights ≥ 1.5 for body. Vietnamese-specific overrides:

| Role | Size | Line-height | Tracking | Weight ceiling |
|---|---|---|---|---|
| caption / xs | 12 px | 1.55 | 0 | 600 |
| body sm | 14 px | 1.55 | 0 | 600 |
| body base | 16 px | 1.6 | 0 | 700 |
| body lg | 18 px | 1.6 | 0 | 700 |
| heading h6 / h5 | 18–20 px | 1.5 | 0 | 700 |
| heading h4 | 24 px | 1.4 | -0.005em | 700 |
| heading h3 | 30 px | 1.3 | -0.01em | 700 |
| heading h2 | 36 px | 1.25 | -0.01em | 700 |
| heading h1 | 48 px | 1.2 | -0.015em | 700 |
| display | 60 px+ | 1.1 | -0.02em | 700 |

Notes:

- **Do not tighten body tracking below 0** for Vietnamese.
- For headings, mild negative tracking is fine if the font's marks are designed for it (Be Vietnam Pro, Inter both handle this).
- For weights ≥ 700 at sizes < 14 px, switch to a font tuned for small Vietnamese (Be Vietnam Pro Semibold) or drop one weight step.

---

## Section D — Locale Conventions (`vi-VN`)

### D.1 — Language Attribution

Web:
```html
<html lang="vi">
```

For pages mixing Vietnamese and English, set page-level `lang="vi"` and use `<span lang="en">English content</span>` on inline foreign-language fragments — screen readers switch voice profiles.

iOS / Android: set the app's primary language in localization config; specify `Locale("vi", "VN")`.

Flutter: configure `localizationsDelegates` and `supportedLocales: [Locale('vi', 'VN'), Locale('en', 'US')]`.

### D.2 — Numbers

Vietnamese uses **dot** for thousands and **comma** for decimal:

| Value | English | Vietnamese |
|---|---|---|
| 1234567.89 | `1,234,567.89` | `1.234.567,89` |
| 0.5 | `0.5` | `0,5` |

```js
new Intl.NumberFormat("vi-VN").format(1234567.89);
// → "1.234.567,89"
```

```dart
import 'package:intl/intl.dart';
NumberFormat('#,##0.##', 'vi_VN').format(1234567.89);
// → "1.234.567,89"
```

### D.3 — Currency

VND uses the `₫` suffix; do not show decimal places:

```js
new Intl.NumberFormat("vi-VN", {
  style: "currency", currency: "VND", maximumFractionDigits: 0,
}).format(1234567);
// → "1.234.567 ₫"
```

### D.4 — Dates

Default `dd/MM/yyyy`, e.g., `18/05/2026`. For long form: `Thứ Hai, ngày 18 tháng 5 năm 2026`. Use 24-hour time (`14:30`).

```js
new Intl.DateTimeFormat("vi-VN").format(new Date());
// → "18/5/2026"

new Intl.DateTimeFormat("vi-VN", { dateStyle: "full" }).format(new Date());
// → "Thứ Hai, 18 tháng 5, 2026"
```

### D.5 — Sorting (collation)

```js
const collator = new Intl.Collator("vi", { sensitivity: "base" });
items.sort((a, b) => collator.compare(a.name, b.name));
```

Vietnamese collation orders `Đ` immediately after `D`, and tone-bearing vowels follow their base.

### D.6 — Plurals

Vietnamese has **no grammatical plural**. Do not pluralize:

```
✅ "3 sản phẩm"
❌ "3 sản phẩms"
```

`Intl.PluralRules("vi")` returns `"other"` for every count.

---

## Section E — Label & Microcopy Craft

Vietnamese UI labels are 20–35% longer than English. Account for this in buttons, table headers, navigation items.

| English | Vietnamese | Char delta |
|---|---|---|
| Sign in | Đăng nhập | ~ |
| Sign up | Đăng ký | ~ |
| Submit | Gửi / Xác nhận | ~ |
| Cancel | Huỷ | shorter |
| Forgot password? | Quên mật khẩu? | longer |
| Create account | Tạo tài khoản | longer |
| Edit profile | Chỉnh sửa hồ sơ | much longer |
| Delete | Xoá | shorter |
| Settings | Cài đặt | ~ |
| Notifications | Thông báo | ~ |
| Search | Tìm kiếm | longer |
| Save changes | Lưu thay đổi | longer |
| Continue | Tiếp tục | ~ |
| Get started | Bắt đầu | shorter |

### E.1 — Verb-led action labels

Vietnamese reads naturally with verb-first labels: `Đăng nhập`, `Tạo tài khoản`, `Xác nhận thanh toán`. Avoid noun-first translations of English ("Account creation" → bad).

### E.2 — Form field labels

Use full labels — not abbreviations. Vietnamese diacritics make abbreviations harder to disambiguate:

| Avoid | Prefer |
|---|---|
| SĐT | Số điện thoại |
| MK | Mật khẩu |
| TK | Tài khoản |
| ĐN | Đăng nhập |

For tight spaces, use icon + tooltip, not abbreviation.

### E.3 — Error / status messages

Be specific and actionable:

```
✅ "Mật khẩu phải có ít nhất 8 ký tự."
❌ "Mật khẩu không hợp lệ."

✅ "Email này đã được sử dụng. Đăng nhập hoặc dùng email khác."
❌ "Email lỗi."

✅ "Không thể tải dữ liệu. Kiểm tra kết nối và thử lại."
❌ "Có lỗi xảy ra."
```

### E.4 — Friendly microcopy without being childish

Vietnamese product copy works well with calm, helpful tone:

- Empty state: `Chưa có đơn hàng nào ở đây. Tạo đơn đầu tiên để bắt đầu.`
- Loading: `Đang tải dữ liệu của bạn…`
- Success: `Đã lưu thay đổi.`
- Confirmation: `Bạn chắc chắn muốn xoá mục này?` + `Xoá` / `Huỷ`

Avoid robotic system-speak (`Hệ thống đã thực thi yêu cầu của người dùng thành công`).

---

## Section F — Rendering Verification Checklist

Before signing off on typography, render and visually inspect at every breakpoint and platform:

- [ ] Body 16 px / 400 weight — Vietnamese tone marks have ≥ 2 px clearance from line above
- [ ] Body 16 px / 700 weight — marks do not blob into letter strokes
- [ ] Caption 12 px — `ạ` and `ụ` dots visible, not clipped
- [ ] Heading h1 — diacritics align with cap-height, no collisions with line above
- [ ] Buttons — Vietnamese labels (`Đăng ký`, `Xác nhận`) fit without wrapping at the smallest button size
- [ ] Form labels — long Vietnamese labels (`Số điện thoại`, `Địa chỉ liên hệ`) do not truncate
- [ ] Tables — Vietnamese column headers fit; if they wrap, leading is not crushed
- [ ] Mixed Vietnamese + Latin in same paragraph — no metric jumps
- [ ] Dark theme rendering — sub-pixel rendering on dark backgrounds is harder; bump weight ≥ 500 for body if needed

---

## Required Practices

- Always include the `vietnamese` subset (or full coverage equivalent) in font loading.
- Always test the diacritic string at every type-scale size before signing off.
- Always set `lang="vi"` (Web) / `Locale("vi", "VN")` (native) on the root.
- Always use `Intl.*` APIs (or platform equivalents) for dates, numbers, currency, collation.
- Always design assuming Vietnamese labels are ~30% longer than English equivalents.

## Prohibited Practices

- Do not pick a font without verifying full diacritic coverage with a real test string.
- Do not tighten body tracking below 0 for Vietnamese.
- Do not auto-hyphenate Vietnamese text.
- Do not abbreviate Vietnamese form labels (SĐT, MK, TK) unless space is genuinely impossible.
- Do not pluralize Vietnamese nouns based on count.
- Do not pair Vietnamese with a system-fallback font; the metrics jump is visible and unprofessional.
