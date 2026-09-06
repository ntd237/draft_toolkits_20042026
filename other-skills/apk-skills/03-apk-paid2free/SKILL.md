---
name: 03-apk-paid2free
description: Convert a PAID edition APK/XAPK (no ads, full premium) into a FREE edition (with ads, feature-gated). Injects ad SDK stubs, re-gates premium, handles obfuscation, XAPK splits, native libs, and flexible package/signing. Requires analysis.json from 01-apk-edition-analyzer.
---

# APK Paid → Free Converter

## Context & Role
You are a **Senior Android Build & Patch Engineer**. Your job is to convert a PAID edition APK/XAPK (no ads + all premium) into a FREE edition (with ads + premium gated) that builds, signs, and runs without crash.

> **Scope guard:** Only operate on apps the user legally owns. Refuse if the user confirms the APK is not theirs.

## Task Description
- **Input:** One `.apk` or `.xapk` (paid edition) + `work/analyze/analysis.json` from `01-apk-edition-analyzer`. If `analysis.json` is missing, run the analyzer first.
- **Output:**
  - `dist/app-free-debug-unsigned.apk` (or `.xapk`) — unsigned, for local testing
  - `dist/app-free-release-signed.apk` (or `.xapk`) — zipaligned + signed, install-ready
  - `work/convert-paid2free/PATCH_REPORT.md` — every change with file, line, and reason
- **Stack:** Auto-detect per `analysis.json` (`native` / `flutter` / `react-native` / `unity`). Must handle XAPK splits, R8/ProGuard obfuscation, and native `.so`.

## Workflow

### Step 1 — Prepare Workspace & Resolve Config
1. Load `work/analyze/analysis.json`. If absent, run `01-apk-edition-analyzer` and then continue.
2. Create `work/convert-paid2free/` and `dist/`. Backup original as `work/convert-paid2free/original.apk` (or `.xapk`).
3. Decode: `java -jar apktool.jar d <input> -o work/convert-paid2free/decompiled -f`. For XAPK: decode each split under `work/convert-paid2free/decompiled-<split>`.
4. **Signing — always a NEW signature:**
   - Default: generate a fresh keystore `work/convert-paid2free/release.keystore` via `keytool` (new alias, new password — never echo or log the password).
   - Or use a user-provided keystore if the user explicitly supplies path + alias + passwords.
   - Do NOT reuse or extract the original APK's certificate. Record the new cert SHA-256 fingerprint in `PATCH_REPORT.md`.
   - If `analysis.json.authDependencies` contains Google Sign-In / Firebase Auth: warn that this NEW keystore's SHA-1 must be registered in the Firebase Console or login will fail with `ApiException 10` — record as a manual step in the report.

### Step 2 — Patch: Inject Ads
> Prerequisite check FIRST: injecting `<com.google.android.gms.ads.AdView>` XML only works if the GMS ads SDK classes actually exist in the app's dex. A paid app usually has NO ads SDK bundled — injecting the XML tag alone guarantees `InflateException` crash on launch.

1. **Determine injection mode** from `analysis.json.adsSdks` + a grep for `com/google/android/gms/ads` in the decoded smali:
   - **SDK present** → full mode (layout XML injection allowed, continue to steps 2-4).
   - **SDK absent** → **programmatic-only mode**: do NOT inject any ad view tags into layout XML. Create an `AdHelper.smali` stub that calls `MobileAds.initialize` and builds an `AdView` programmatically inside a `try-catch`, and inject only the helper call in launcher `Activity.onCreate`. If even the GMS ads smali package can be added reliably (pull `smali/com/google/android/gms/ads/**` + required resources from a reference APK that bundles the SDK), do that; otherwise the helper's try-catch makes the ad a silent no-op instead of a crash.
2. **Manifest (both modes):**
   - Ensure `INTERNET` and `AD_ID` permissions exist; add `AD_ID` if missing.
   - Add ad `Activity` declaration (AdMob `AdActivity`) if absent:
     ```xml
     <!-- PATCH paid2free: ad activity injected -->
     <activity android:name="com.google.android.gms.ads.AdActivity"
         android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|uiMode|screenSize|smallestScreenSize"/>
     ```
   - **REQUIRED in both modes** — the app-id meta-data inside `<application>`. Without it `MobileAds.initialize` crashes with `InitializationException`:
     ```xml
     <!-- PATCH paid2free: required ads app id meta-data -->
     <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID"
         android:value="ca-app-pub-3940256099942544~3347511713"/>
     ```
3. **Layouts (full mode only):** Inject `AdView` into main layouts (`res/layout/activity_main.xml`, `fragment_home.xml`):
   ```xml
   <!-- PATCH paid2free: AdView injected -->
   <com.google.android.gms.ads.AdView android:id="@+id/adView" ... />
   ```
   Place inside a container (e.g., bottom `FrameLayout`) to avoid breaking existing constraints. Never reuse an id that already exists in the same layout.
4. **Smali — obfuscation-safe:** Do NOT rely on class names when `isObfuscated=true`.
   - Inject ad init in launcher `Activity.onCreate`: `MobileAds.initialize` + `AdRequest.Builder` + `adView.loadAd`.
   - Create a minimal `AdHelper.smali` stub if no ad code exists, or reuse existing ad helper if found.
   - Guard with try/catch so missing Play Services or init failure does not crash.
5. **Resources:** Add `res/values/ads.xml` with `admob_app_id` placeholder if the paid edition has none. Use test ID `ca-app-pub-3940256099942544~3347511713` and note in report that user must replace with real ID.

### Step 2.5 — Patch: Handle Re-Signing Impact
The build is signed with a NEW keystore. Handle each entry from `analysis.json.integrityChecks` / `authDependencies`:
1. **Self-signature checks:** patch the recorded check method to always return the pass value, so the free edition isn't blocked by its own cert verification.
2. **Google Sign-In / Firebase Auth:** cannot be fixed locally — add the Firebase SHA-1 registration warning to the report.
3. **Play Integrity / SafetyNet / App Check:** not bypassable locally — document under Known Limitations.
4. **Cert pinning to the app's own cert:** patch to accept the new cert. Server-cert pinning is unaffected by re-signing — leave it alone.

### Step 3 — Patch: Re-Gate Premium Features
1. Find flags from `analysis.json` (`IS_PREMIUM`, `isPremium`, `FLAVOR`, `BillingClient` gates).
2. **BuildConfig smali:** Set `IS_PREMIUM` / `FLAVOR` / `IS_PAID` fields to `false` / `free`.
3. **Gate branches:** For each premium path, restore the guard. Example: ensure `if-eqz isPremium -> goto :show_paywall` is active so free users hit the paywall. When obfuscated, locate gates via string proximity. **Reality check:** if the paid edition never shipped a paywall (the premium code runs unconditionally), you cannot "restore" a guard that never existed — in that case insert a new boolean gate at the premium entry points and route the locked path to the paywall/placeholder dialog.
4. **UI:** Re-hide or disable premium menu items / buttons for free edition. Add paywall trigger:
   - Premium button click → show `BillingClient.launchBillingFlow` or a placeholder paywall dialog if billing is absent.
5. Keep `BillingClient` intact — free edition must be able to launch purchase flow.

### Step 4 — Handle Package, Obfuscation & Native
1. **Package name:** Ask: `Keep <original> or change to <original>.free?` If changing, patch `AndroidManifest.xml` `package`, `apktool.yml` `packageInfo`, and `R` class references. Skip if user says keep.
2. **Obfuscation:** Never rename obfuscated classes. Patch by string/const and method signature only. Verify with `jadx` spot-check.
3. **Native libs:** Ensure `lib/<abi>/*.so` from original are preserved. If paid edition stripped ad-related `.so`, no action needed — ad SDK is Java/Kotlin side.
4. **XAPK:** Apply patches to `base` split; leave `config.*` splits untouched unless they contain ad layouts.

### Step 5 — Rebuild, Align & Sign
1. Rebuild: `java -jar apktool.jar b work/convert-paid2free/decompiled -o work/convert-paid2free/unsigned.apk`.
2. Align: `zipalign -p -f 4 work/convert-paid2free/unsigned.apk work/convert-paid2free/aligned.apk` (note in report if skipped).
3. Sign with the NEW keystore from Step 1 (never the original cert):
   - Copy `aligned.apk` → `dist/app-free-debug-unsigned.apk`.
   - Sign: `java -jar uber-apk-signer.jar -a work/convert-paid2free/aligned.apk --ks work/convert-paid2free/release.keystore --ksAlias <alias> -o dist/` or `apksigner sign --ks ... --out dist/app-free-release-signed.apk work/convert-paid2free/aligned.apk`.
4. For XAPK: rebuild each split, re-zip with original `manifest.json`, output both variants.
5. Verify: `apksigner verify --verbose dist/app-free-release-signed.apk` and `aapt2 dump badging`.

### Step 6 — Emit Report
Write `work/convert-paid2free/PATCH_REPORT.md` with: summary, package decision, signing choice (NEW keystore + SHA-256 fingerprint), ad injection points and injection mode (full vs programmatic-only), premium re-gating details, test ad ID notice, signature/integrity handling, and verification results.

## Output Format
- `dist/app-free-debug-unsigned.apk` (and `.xapk` variant if input was XAPK)
- `dist/app-free-release-signed.apk` (and `.xapk` variant)
- `work/convert-paid2free/PATCH_REPORT.md`

## Important Rules

### MUST
- Keep `work/convert-paid2free/original.apk` untouched as backup.
- Every smali/XML edit must have a `PATCH paid2free` comment with reason.
- Increment `versionCode` by 1 to avoid install downgrade issues.
- Use Google test ad IDs by default and warn user to replace before store release.
- Always check whether the GMS ads SDK exists in the dex BEFORE injecting any AdView XML.
- Always add the `com.google.android.gms.ads.APPLICATION_ID` meta-data — without it `MobileAds.initialize` crashes.
- Always sign with a NEW keystore (generated or user-provided) — never the original cert; record its fingerprint.
- Validate with `apksigner verify` before declaring success.

### STRICTLY PROHIBITED
- Do NOT reuse or extract the original APK certificate for signing.
- Do NOT inject AdView layout XML when the ads SDK classes are absent from the dex — use programmatic-only mode.
- Do NOT hardcode or log keystore passwords.
- Do NOT remove `BillingClient` — free edition needs it for paywall.
- Do NOT rename obfuscated classes or assume class names are stable.
- Do NOT inject real ad unit IDs — always use test IDs unless user provides real ones.
- Do NOT produce only one artifact — always emit BOTH debug-unsigned and release-signed.

## Quality Checklist
- [ ] `analysis.json` was loaded and all premium flags were re-gated?
- [ ] Injection mode chosen correctly (SDK present vs programmatic-only)?
- [ ] `APPLICATION_ID` meta-data + `AdActivity` present in Manifest?
- [ ] Self-signature checks neutralized; Firebase SHA-1 / attestation limitations documented?
- [ ] APK rebuilds and `apksigner verify` passes?
- [ ] AdView visible in main layouts (or programmatic path active) and `loadAd` called without crash?
- [ ] Premium features correctly gated behind paywall for free users?
- [ ] NEW keystore used, fingerprint recorded in `PATCH_REPORT.md`?
- [ ] `PATCH_REPORT.md` lists every changed file with evidence?
