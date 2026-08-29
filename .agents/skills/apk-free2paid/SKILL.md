---
name: apk-free2paid
description: Convert a FREE edition APK/XAPK (with ads, limited features) into a PAID edition (no ads, all premium unlocked). Handles obfuscation, XAPK splits, native libs, and flexible package/signing. Requires analysis.json from apk-edition-analyzer.
---

# APK Free → Paid Converter

## Context & Role
You are a **Senior Android Build & Patch Engineer**. Your job is to convert a FREE edition APK/XAPK (ads + feature-gated) into a PAID edition (no ads + premium unlocked) that builds, signs, and runs without crash.

> **Scope guard:** Only operate on apps the user legally owns. Refuse if the user confirms the APK is not theirs.

## Task Description
- **Input:** One `.apk` or `.xapk` (free edition) + `work/analyze/analysis.json` from `apk-edition-analyzer`. If `analysis.json` is missing, run the analyzer first.
- **Output:**
  - `dist/app-paid-debug-unsigned.apk` (or `.xapk`) — unsigned, for local testing
  - `dist/app-paid-release-signed.apk` (or `.xapk`) — zipaligned + signed, install-ready
  - `work/convert/PATCH_REPORT.md` — every change with file, line, and reason
- **Stack:** Auto-detect per `analysis.json` (`native` / `flutter` / `react-native` / `unity`). Must handle XAPK splits, R8/ProGuard obfuscation, and native `.so`.

## Workflow

### Step 1 — Prepare Workspace & Resolve Config
1. Load `work/analyze/analysis.json`. If absent, run `apk-edition-analyzer` and then continue.
2. Create `work/convert/` and `dist/`. Backup original as `work/convert/original.apk` (or `.xapk`).
3. Decode: `java -jar apktool.jar d <input> -o work/convert/decompiled -f`. For XAPK: decode each split under `work/convert/decompiled-<split>`.
4. Ask about signing (flexible mode):
   - `Reuse original cert` — extract cert from input if available
   - `Provide keystore` — ask for path + alias + passwords
   - `Create debug keystore` — generate `work/convert/debug.keystore` via `keytool`
   - Default to debug keystore if user does not respond.

### Step 2 — Patch: Remove Ads
1. **Manifest:** Remove or comment ad `Activity`/`Service`/`Receiver` entries and `AD_ID` permission only if no other code needs it. Keep `INTERNET`.
2. **Layouts:** In `res/layout*/`, remove `com.google.android.gms.ads.AdView` and other ad view tags. Replace with `<!-- PATCH free2paid: ad view removed -->`.
3. **Smali — obfuscation-safe:** Do NOT rely on class names when `isObfuscated=true`. Instead:
   - NOP calls matching `const-string "admob"/"ads"` → `invoke-* AdRequest` / `loadAd` / `show` / `initialize`.
   - Stub `loadAd` methods to `return-void` immediately; stub `isAdLoaded` to return `true` or bypass.
4. **Resources:** Remove ad-related string/drawable entries only if safe; otherwise keep to avoid `Resources$NotFoundException`.
5. Tag every edit with `// PATCH free2paid: <reason>` in smali comments or XML comments.

### Step 3 — Patch: Unlock Premium Features
1. Find flags from `analysis.json` (`IS_PREMIUM`, `isPremium`, `FLAVOR`, `BillingClient` gates).
2. **BuildConfig smali:** Set `IS_PREMIUM` / `FLAVOR` / `IS_PAID` fields to `true` / `paid`.
3. **Gate branches:** For each `if-eqz isPremium -> goto :premium_locked`, invert or NOP the branch so premium path always executes. When obfuscated, locate gates via string proximity (`"premium"`, `"pro"`, `"billing"`).
4. **UI:** Unhide premium menu items / buttons hidden by `setVisibility(GONE)` gated on premium check.
5. Do NOT break billing code — keep `BillingClient` intact but bypass the entitlement check so features are unlocked without purchase.

### Step 4 — Handle Package, Obfuscation & Native
1. **Package name:** `analysis.json` is flexible. Ask: `Keep <original> or change to <original>.paid?` If changing, patch `AndroidManifest.xml` `package`, `apktool.yml` `packageInfo`, and `R` class references in smali. Skip if user says keep.
2. **Obfuscation:** Never rename obfuscated classes. Patch by string/const and method signature only. Verify with `jadx` decompile spot-check if needed.
3. **Native libs:** Copy `lib/<abi>/*.so` from original if any were stripped. Do not modify `.so` — only ensure required ABIs are present in the rebuilt APK.
4. **XAPK:** Apply patches to `base` split; leave `config.*` splits untouched unless they contain ad resources.

### Step 5 — Rebuild, Align & Sign
1. Rebuild: `java -jar apktool.jar b work/convert/decompiled -o work/convert/unsigned.apk`.
2. Align: `zipalign -p -f 4 work/convert/unsigned.apk work/convert/aligned.apk` (skip if `zipalign` unavailable — note in report).
3. Sign twice:
   - Copy `aligned.apk` → `dist/app-paid-debug-unsigned.apk` (leave unsigned as debug artifact).
   - Sign: `java -jar uber-apk-signer.jar -a work/convert/aligned.apk --ks <keystore> --ksAlias <alias> -o dist/` or `apksigner sign --ks ... --out dist/app-paid-release-signed.apk work/convert/aligned.apk`.
4. For XAPK: rebuild each split, re-zip with original `manifest.json`, output both unsigned and signed `.xapk`.
5. Verify: `apksigner verify --verbose dist/app-paid-release-signed.apk` and `aapt2 dump badging`.

### Step 6 — Emit Report
Write `work/convert/PATCH_REPORT.md` with: summary, package decision, signing choice, table of changed files (path, lines, what & why), obfuscation handling notes, and verification results.

## Output Format
- `dist/app-paid-debug-unsigned.apk` (and `.xapk` variant if input was XAPK)
- `dist/app-paid-release-signed.apk` (and `.xapk` variant)
- `work/convert/PATCH_REPORT.md`

## Important Rules

### MUST
- Keep `work/convert/original.apk` untouched as backup.
- Every smali/XML edit must have a `PATCH free2paid` comment with reason.
- Increment `versionCode` by 1 to avoid install downgrade issues.
- Validate with `apksigner verify` before declaring success.

### STRICTLY PROHIBITED
- Do NOT hardcode or log keystore passwords.
- Do NOT delete `BillingClient` code — only bypass entitlement checks.
- Do NOT rename obfuscated classes or assume class names are stable.
- Do NOT produce only one artifact — always emit BOTH debug-unsigned and release-signed.

## Quality Checklist
- [ ] `analysis.json` was loaded and all flagged ads/features were addressed?
- [ ] APK rebuilds and `apksigner verify` passes?
- [ ] Ad views removed and ad load calls stubbed without crash on launch?
- [ ] Premium gates bypassed and premium UI visible?
- [ ] `PATCH_REPORT.md` lists every changed file with evidence?
