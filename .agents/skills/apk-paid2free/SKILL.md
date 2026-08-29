---
name: apk-paid2free
description: Convert a PAID edition APK/XAPK (no ads, full premium) into a FREE edition (with ads, feature-gated). Injects ad SDK stubs, re-gates premium, handles obfuscation, XAPK splits, native libs, and flexible package/signing. Requires analysis.json from apk-edition-analyzer.
---

# APK Paid → Free Converter

## Context & Role
You are a **Senior Android Build & Patch Engineer**. Your job is to convert a PAID edition APK/XAPK (no ads + all premium) into a FREE edition (with ads + premium gated) that builds, signs, and runs without crash.

> **Scope guard:** Only operate on apps the user legally owns. Refuse if the user confirms the APK is not theirs.

## Task Description
- **Input:** One `.apk` or `.xapk` (paid edition) + `work/analyze/analysis.json` from `apk-edition-analyzer`. If `analysis.json` is missing, run the analyzer first.
- **Output:**
  - `dist/app-free-debug-unsigned.apk` (or `.xapk`) — unsigned, for local testing
  - `dist/app-free-release-signed.apk` (or `.xapk`) — zipaligned + signed, install-ready
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

### Step 2 — Patch: Inject Ads
1. **Manifest:** Ensure `INTERNET` and `AD_ID` permissions exist; add `AD_ID` if missing. Add ad `Activity` declarations (AdMob `AdActivity`) if absent:
   ```xml
   <!-- PATCH paid2free: ad activity injected -->
   <activity android:name="com.google.android.gms.ads.AdActivity"
       android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|uiMode|screenSize|smallestScreenSize"/>
   ```
2. **Layouts:** Inject `AdView` into main layouts (`res/layout/activity_main.xml`, `fragment_home.xml`):
   ```xml
   <!-- PATCH paid2free: AdView injected -->
   <com.google.android.gms.ads.AdView android:id="@+id/adView" ... />
   ```
   Place inside a container (e.g., bottom `FrameLayout`) to avoid breaking existing constraints.
3. **Smali — obfuscation-safe:** Do NOT rely on class names when `isObfuscated=true`.
   - Inject ad init in launcher `Activity.onCreate`: `MobileAds.initialize` + `AdRequest.Builder` + `adView.loadAd`.
   - Create a minimal `AdHelper.smali` stub if no ad code exists, or reuse existing ad helper if found.
   - Guard with try/catch so missing Play Services does not crash.
4. **Resources:** Add `res/values/ads.xml` with `admob_app_id` placeholder if the paid edition has none. Use test ID `ca-app-pub-3940256099942544~3347511713` and note in report that user must replace with real ID.

### Step 3 — Patch: Re-Gate Premium Features
1. Find flags from `analysis.json` (`IS_PREMIUM`, `isPremium`, `FLAVOR`, `BillingClient` gates).
2. **BuildConfig smali:** Set `IS_PREMIUM` / `FLAVOR` / `IS_PAID` fields to `false` / `free`.
3. **Gate branches:** For each premium path, restore the guard. Example: ensure `if-eqz isPremium -> goto :show_paywall` is active so free users hit the paywall. When obfuscated, locate gates via string proximity.
4. **UI:** Re-hide or disable premium menu items / buttons for free edition. Add paywall trigger:
   - Premium button click → show `BillingClient.launchBillingFlow` or a placeholder paywall dialog if billing is absent.
5. Keep `BillingClient` intact — free edition must be able to launch purchase flow.

### Step 4 — Handle Package, Obfuscation & Native
1. **Package name:** Ask: `Keep <original> or change to <original>.free?` If changing, patch `AndroidManifest.xml` `package`, `apktool.yml` `packageInfo`, and `R` class references. Skip if user says keep.
2. **Obfuscation:** Never rename obfuscated classes. Patch by string/const and method signature only. Verify with `jadx` spot-check.
3. **Native libs:** Ensure `lib/<abi>/*.so` from original are preserved. If paid edition stripped ad-related `.so`, no action needed — ad SDK is Java/Kotlin side.
4. **XAPK:** Apply patches to `base` split; leave `config.*` splits untouched unless they contain ad layouts.

### Step 5 — Rebuild, Align & Sign
1. Rebuild: `java -jar apktool.jar b work/convert/decompiled -o work/convert/unsigned.apk`.
2. Align: `zipalign -p -f 4 work/convert/unsigned.apk work/convert/aligned.apk` (note in report if skipped).
3. Sign twice:
   - Copy `aligned.apk` → `dist/app-free-debug-unsigned.apk`.
   - Sign: `java -jar uber-apk-signer.jar -a work/convert/aligned.apk --ks <keystore> --ksAlias <alias> -o dist/` or `apksigner sign --ks ... --out dist/app-free-release-signed.apk work/convert/aligned.apk`.
4. For XAPK: rebuild each split, re-zip with original `manifest.json`, output both variants.
5. Verify: `apksigner verify --verbose dist/app-free-release-signed.apk` and `aapt2 dump badging`.

### Step 6 — Emit Report
Write `work/convert/PATCH_REPORT.md` with: summary, package decision, signing choice, ad injection points, premium re-gating details, test ad ID notice, and verification results.

## Output Format
- `dist/app-free-debug-unsigned.apk` (and `.xapk` variant if input was XAPK)
- `dist/app-free-release-signed.apk` (and `.xapk` variant)
- `work/convert/PATCH_REPORT.md`

## Important Rules

### MUST
- Keep `work/convert/original.apk` untouched as backup.
- Every smali/XML edit must have a `PATCH paid2free` comment with reason.
- Increment `versionCode` by 1 to avoid install downgrade issues.
- Use Google test ad IDs by default and warn user to replace before store release.
- Validate with `apksigner verify` before declaring success.

### STRICTLY PROHIBITED
- Do NOT hardcode or log keystore passwords.
- Do NOT remove `BillingClient` — free edition needs it for paywall.
- Do NOT rename obfuscated classes or assume class names are stable.
- Do NOT inject real ad unit IDs — always use test IDs unless user provides real ones.
- Do NOT produce only one artifact — always emit BOTH debug-unsigned and release-signed.

## Quality Checklist
- [ ] `analysis.json` was loaded and all premium flags were re-gated?
- [ ] APK rebuilds and `apksigner verify` passes?
- [ ] AdView visible in main layouts and `loadAd` called without crash?
- [ ] Premium features correctly gated behind paywall for free users?
- [ ] `PATCH_REPORT.md` lists every changed file with evidence?
