---
name: 03-apk-paid2free
description: Convert a paid-edition APK/XAPK into a free edition by injecting ad SDK stubs/components, re-gating premium features behind paywalls, neutralizing signature checks, and producing signed installable release artifacts. Handles programmatic vs full injection modes, obfuscation, and XAPK splits. Requires analysis.json.
---

# Skill: 03-apk-paid2free

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard Android technical terms.

## Trigger
User asks to convert a paid APK to free edition, inject ads, re-gate premium features, or runs `/03-apk-paid2free`.

## Workflow

### Phase 1: Workspace Initialization & Keystore Generation
**Objective**: Decompile APK, establish clean workspace backup, and create a dedicated signing keystore.

- Load `work/analyze/analysis.json` (invoke `01-apk-edition-analyzer` first if absent).
- Create workspace directories: `work/convert-paid2free/` and `dist/`.
- Back up input package to `work/convert-paid2free/original.apk` (or `.xapk`).
- Decompile package: `java -jar apktool.jar d <input> -o work/convert-paid2free/decompiled -f` (for XAPK, decompile each split to `decompiled-<split>`).
- Generate fresh signing keystore (never reuse original cert):
  - Run `keytool` to generate `work/convert-paid2free/release.keystore` (or load user-specified keystore).
  - Record the certificate SHA-256 fingerprint in the patch report.
  - If Google Sign-In or Firebase Auth is detected, document that the new SHA-1 fingerprint must be added to Firebase Console (`ApiException 10`).

### Phase 2: Ad Injection Strategy & Implementation
**Objective**: Safely inject ad components according to SDK presence in dex bytecode.

- Determine Injection Mode:
  - Check whether AdMob/GMS ads classes exist in bytecode via `analysis.json.adsSdks` and smali grep (`com/google/android/gms/ads`).
  - **SDK Present (Full Mode)**: Inject `com.google.android.gms.ads.AdView` into main layout containers (`res/layout/activity_main.xml`). Use a dedicated container (`FrameLayout`) and ensure unique view IDs.
  - **SDK Absent (Programmatic-Only Mode)**: Do NOT inject XML `<AdView>` tags (prevents fatal `InflateException`). Inject an `AdHelper.smali` wrapper wrapped in try/catch invoked from the launcher activity `onCreate`.
- Manifest Injection (both modes):
  - Ensure `INTERNET` and `AD_ID` permissions exist; declare `AD_ID` if missing.
  - Declare AdMob `AdActivity`:
    ```xml
    <!-- PATCH paid2free: ad activity injected -->
    <activity android:name="com.google.android.gms.ads.AdActivity"
        android:configChanges="keyboard|keyboardHidden|orientation|screenLayout|uiMode|screenSize|smallestScreenSize"/>
    ```
  - Inject mandatory `APPLICATION_ID` meta-data under `<application>` (prevents `InitializationException` on startup):
    ```xml
    <!-- PATCH paid2free: required ads app id meta-data -->
    <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID"
        android:value="ca-app-pub-3940256099942544~3347511713"/>
    ```
- Smali and Resources Injection:
  - Inject ad initialization in launcher `Activity.onCreate` with test ad units.
  - Provide `res/values/ads.xml` with placeholder ad IDs; document replacement notice for production release.

### Phase 3: Premium Re-Gating & Integrity Handling
**Objective**: Reinstate paywall guards on premium features and neutralize self-signature checks for the new cert.

- Neutralize Self-Signature Checks:
  - Patch detected self-signature check methods to return true for the new signing certificate.
  - If custom `X509TrustManager` validates the APK certificate, patch to accept the new cert.
  - Document server-side attestation limitations (Play Integrity, SafetyNet) in limitations.
- Re-Gate Premium Features:
  - Update `BuildConfig` smali: set `IS_PREMIUM`, `FLAVOR`, `IS_PAID` fields to `false` / `"free"`.
  - Restore conditional guards (`if-eqz isPremium -> goto :paywall`) on premium entry points. If original code lacks paywalls, insert boolean checks routing premium actions to paywall dialogs or `BillingClient.launchBillingFlow`.
  - Re-hide premium UI elements and keep `BillingClient` intact to allow future in-app purchases.

### Phase 4: Package Refactoring & Multi-Split Handling
**Objective**: Handle package name adjustments, preserve native dependencies, and patch split configurations.

- Package Name Handling:
  - If package rename is chosen (`<orig>.free`), update `AndroidManifest.xml`, `apktool.yml`, and smali references. Skip if keeping original package.
- Obfuscation & Native Libraries:
  - Preserve all native libraries from `lib/<abi>/*.so`.
  - For XAPK packages, apply smali and layout patches to the `base` split while keeping resource-only splits intact.

### Phase 5: Rebuild, Align, Sign & Report
**Objective**: Assemble modified sources, align binary data, sign with the new keystore, and generate audit report.

- Rebuild package: `java -jar apktool.jar b work/convert-paid2free/decompiled -o work/convert-paid2free/unsigned.apk`.
- Align archive: `zipalign -p -f 4 work/convert-paid2free/unsigned.apk work/convert-paid2free/aligned.apk`.
- Sign with the new keystore:
  - Copy unsigned artifact to `dist/app-free-debug-unsigned.apk`.
  - Sign aligned artifact to `dist/app-free-release-signed.apk` using `apksigner` or `uber-apk-signer.jar`.
  - For XAPK: rebuild each split, package with original `manifest.json`, and emit both unsigned and signed `.xapk`.
- Verify signature: `apksigner verify --verbose dist/app-free-release-signed.apk`.
- Generate `work/convert-paid2free/PATCH_REPORT.md` documenting injection points, mode, test IDs, and certificate fingerprints.

## Output Format
- `dist/app-free-debug-unsigned.apk` (or `.xapk`)
- `dist/app-free-release-signed.apk` (or `.xapk`)
- `work/convert-paid2free/PATCH_REPORT.md`

## Don'ts
- Do not inject XML `<com.google.android.gms.ads.AdView>` tags when the ads SDK classes are absent from dex (causes fatal `InflateException`).
- Do not omit the `com.google.android.gms.ads.APPLICATION_ID` manifest meta-data (causes fatal `InitializationException`).
- Do not reuse or extract the original APK certificate; sign exclusively with a fresh keystore.
- Do not inject production ad unit IDs; use Google test IDs by default.
- Do not remove `BillingClient` code; retain it to support paywall purchase flows.
- Do not produce only one artifact; always emit both debug-unsigned and release-signed builds.

## Quality Checklist
- [ ] `analysis.json` evaluated and correct injection mode selected (full vs programmatic-only)?
- [ ] `APPLICATION_ID` meta-data and `AdActivity` declared in Manifest?
- [ ] Test ad IDs used and replacement notice included in report?
- [ ] Premium features re-gated with conditional branch guards or paywall triggers?
- [ ] Self-signature validation methods patched to return pass?
- [ ] APK rebuilt, zipaligned, and verified with `apksigner verify --verbose`?
- [ ] Fresh keystore used and SHA-256 fingerprint recorded in `PATCH_REPORT.md`?
