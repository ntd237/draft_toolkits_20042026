# paid2free Conversion Playbook

Convert a paid-edition APK/XAPK into a free edition: inject ad components, re-gate premium features behind paywalls, neutralize self-signature checks. Requires `work/analyze/analysis.json`.

## Phase 1: Ad Injection Strategy & Implementation

### Determine Injection Mode
- Check whether AdMob/GMS ads classes exist in bytecode via `analysis.json.adsSdks` and smali grep (`com/google/android/gms/ads`).
- **SDK Present (Full Mode)**: inject `com.google.android.gms.ads.AdView` into main layout containers (`res/layout/activity_main.xml`). Use a dedicated container (`FrameLayout`) and ensure unique view IDs.
- **SDK Absent (Programmatic-Only Mode)**: do NOT inject XML `<AdView>` tags (prevents fatal `InflateException`). Inject an `AdHelper.smali` wrapper wrapped in try/catch, invoked from the launcher activity `onCreate`.

### Manifest Injection (both modes)
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

### Smali & Resources Injection
- Inject ad initialization in launcher `Activity.onCreate` with test ad units.
- Provide `res/values/ads.xml` with placeholder ad IDs; document a replacement notice for production release in `PATCH_REPORT.md`.
- Never inject production ad unit IDs; use Google test IDs by default (production IDs require explicit user-owned ad account confirmation in the spec).

## Phase 2: Premium Re-Gating & Integrity Handling

### Neutralize Self-Signature Checks
- Patch detected self-signature check methods to return true for the new signing certificate.
- If a custom `X509TrustManager` validates the APK certificate, patch it to accept the new cert.
- Document server-side attestation limitations (Play Integrity, SafetyNet) — never attempt a bypass.

### Re-Gate Premium Features
- Update `BuildConfig` smali: set `IS_PREMIUM`, `FLAVOR`, `IS_PAID` fields to `false` / `"free"`.
- Restore conditional guards (`if-eqz isPremium -> goto :paywall`) on premium entry points. If original code lacks paywalls, insert boolean checks routing premium actions to paywall dialogs or `BillingClient.launchBillingFlow`.
- Re-hide premium UI elements and keep `BillingClient` intact to allow future in-app purchases.

## Phase 3: Multi-Split & Native Safeguards
- Preserve all native libraries from `lib/<abi>/*.so`.
- For XAPK: apply smali and layout patches to the `base` split while keeping resource-only splits intact.

## Re-Gating Edge Cases
- **Premium without a local paywall UI**: if the original code has no paywall screen, route gated actions to the least-invasive existing surface — `BillingClient.launchBillingFlow` when billing classes exist (keep them intact per Prohibitions), otherwise a minimal dialog/toast stating the feature requires the paid edition. Never crash or silently drop the action.
- **Server-driven premium state**: when the paid state comes from the backend user object (mirror of `decision-point-miss` in `apk-fix-playbook.md`), gate on the client-side derivation point: intercept the state read (Hermes predicate or smali gate branch) and route truthy-server-state to the paywall path regardless of the server verdict. Do not rewrite server responses for paid2free (the direction adds ads, not removes entitlements) — re-gating stays purely client-side.
- **Trial/ introductory entitlements**: treat intro-offer and trial states as paid for gating purposes (`if-nez trialFlag` → paywall) so the free edition does not leak premium through trial code paths.

## Prohibitions
- Do not inject XML `<com.google.android.gms.ads.AdView>` tags when the ads SDK classes are absent from dex (fatal `InflateException`).
- Do not omit the `com.google.android.gms.ads.APPLICATION_ID` meta-data (fatal `InitializationException`).
- Do not remove `BillingClient` code; retain it to support paywall purchase flows.
- Do not inject production ad unit IDs without explicit spec confirmation.
- Do not hardcode or log keystore credentials.
