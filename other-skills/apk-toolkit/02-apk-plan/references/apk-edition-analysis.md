# APK Edition Analysis Playbook

Deep static reverse-engineering procedure for Android APK/XAPK packages, executed by `02-apk-plan` (and re-run with expanded scope by `04-apk-bugfinder`). Outputs `work/analyze/analysis.json` and `work/analyze/REPORT.md`. Read-only: never patches, rebuilds, or re-signs.

## Phase A: Validate, Unpack & Layout Inspection

- Verify input file exists with `.apk` or `.xapk` extension. Confirm legal ownership; halt if not confirmed.
- If `.xapk`: extract to `work/analyze/unpacked/`, list splits (`config.*.apk`) and `obb/` assets. Select primary `base.apk` for deep decompilation while recording split layouts.
- If single `.apk`: select the input file directly for decompilation.

## Phase B: Manifest & Signature Fingerprinting

- Run `aapt2 dump badging <apk>` and `aapt2 dump xmltree --file AndroidManifest.xml <apk>` to extract:
  - `package`, `versionCode`, `versionName`, `applicationId`, launcher activity.
  - Declared permissions (specifically `INTERNET`, `AD_ID`, `BILLING`).
  - `minSdk`, `targetSdk`, `extractNativeLibs`, and supported ABIs from `native-code`.
- Run `apksigner verify --print-certs <apk>` to record signature schemes (v1/v2/v3/v4) and certificate fingerprints.
- Record whether the build is debuggable and whether it uses split or app bundle format.

## Phase C: Decompile & Tech Stack Identification

- Run `apktool d <apk> -o work/analyze/decompiled -f` and `jadx --no-res -d work/analyze/jadx <apk>`.
- Detect tech stack from disassembled artifacts:
  - `lib/<abi>/libflutter.so` or `assets/flutter_assets/` → `flutter`
  - `assets/index.android.bundle` or `libreactnativejni.so` → `react-native`
  - `lib/<abi>/libunity.so` or `assets/bin/Data/` → `unity`
  - Otherwise → `native`
- Assess obfuscation level: check for shortened class hierarchies (e.g., `smali/a/b/c.smali`) and `apktool.yml` framework markers. Set `isObfuscated` and classify `obfuscationLevel` as `none`, `light`, or `heavy`.

## Phase D: Scan Ads, Flags, Integrity & Auth Dependencies

- **Ads & Mediation SDKs** — grep `AndroidManifest.xml`, `smali/**/*.smali`, and `resources.arsc` for:
  - AdMob (`com.google.android.gms.ads`), Facebook (`com.facebook.ads`), AppLovin (`com.applovin`), Unity Ads (`com.unity3d.ads`), IronSource (`com.ironsource`), Pangle (`com.bytedance.sdk.openadsdk`).
  - Mediation adapters & listeners: AppLovin MAX (`com.applovin.mediation`), IronSource Mediation (`com.ironsource.mediationsdk`), Unity Services (`com.unity3d.services.ads`).
  - Record each SDK with file path, matched pattern, caller method (`loadAd`, `show`, `initialize`), and registered ad listener callbacks.
- **Feature Flags & Premium Gates** — grep for `BuildConfig`, `FLAVOR`, `IS_PREMIUM`, `isPremium`, `isPro`, `billing`, `BillingClient`, `purchases`. Record target file, field name, default value, and gating branch opcodes (`if-eqz` / `if-nez`).
- **Self-Signature & Tamper Checks**:
  - Java/Smali: grep for `PackageManager.GET_SIGNATURES`, `getSigningCertificateHistory`, `signingInfo`, `hasSigningCertificate`, and custom comparisons on `signatures[0].toByteArray()`.
  - Checksum/Tamper: grep for `classes.dex` CRC32/SHA checks, `META-INF` integrity verification, and debuggable detection (`ApplicationInfo.FLAG_DEBUGGABLE`).
  - Pinpoint the exact method returning the validation boolean (target method for converter patching).
- **Auth-Path Integrity Scan (misleading-login detector)** — determine whether any detected check feeds the login/credential flow:
  - Grep for signature-derived crypto keys near request builders (`signatures[0]` / `signingInfo` feeding `Cipher`/`Mac`/`MessageDigest` used on credential payloads).
  - Grep for dex/package integrity tokens embedded in request parameters (`classes.dex` CRC/SHA sent alongside credentials, custom "device fingerprint" headers computed locally).
  - Grep for local tamper checks executing before login calls (`FirebaseAuth.signIn*`, custom login API invocations).
  - Record every hit in `integrityChecks` with `"feedsAuthPath": true` — converters must patch these before auth testing, and `04-apk-bugfinder` prioritizes them when diagnosing "correct credentials rejected".
- **Platform Attestation & Cert Pinning**:
  - Grep for `play.core.integrity`, `safetynet`, `firebase.appcheck` (flag `bypassable: false`).
  - Grep for `okhttp3.CertificatePinner`, `network_security_config.xml`, and custom `X509TrustManager` implementations.
- **Authentication Dependencies**:
  - Grep for `FirebaseAuth`, `GoogleSignIn`, `CredentialManager`.
  - Flag requirement: re-signing invalidates Google Sign-In unless the new keystore SHA-1 is added to Firebase Console (`ApiException 10`).

## Phase E: Native Library Mapping & Artifact Synthesis

- Scan `lib/<abi>/*.so`, checking binary architecture, stripped symbol status, and string references:
  - Monetization & licensing routines.
  - Native signature verification: search `.so` binaries for string constants or JNI calls referencing `GET_SIGNATURES`, `signatures`, `classes.dex`, `META-INF/`, or custom OpenSSL/mbedTLS cert pinning.
- Determine `editionGuess` (`free` vs `paid`) with confidence (`high`, `medium`, `low`) backed by at least two independent evidence signals.
- Synthesize `work/analyze/analysis.json` and `work/analyze/REPORT.md`.

## `work/analyze/analysis.json` Schema

```json
{
  "inputFile": "app.apk",
  "isXapk": false,
  "splits": [],
  "obbFiles": [],
  "packageName": "com.example.app",
  "versionCode": 42,
  "versionName": "1.2.0",
  "minSdk": 21,
  "targetSdk": 34,
  "abiList": ["arm64-v8a", "armeabi-v7a"],
  "extractNativeLibs": true,
  "techStack": "native",
  "isObfuscated": true,
  "obfuscationLevel": "heavy",
  "signingScheme": "v2+v3",
  "certFingerprint": "SHA-256:...",
  "editionGuess": "free",
  "editionConfidence": "high",
  "adsSdks": [
    {"sdk": "admob", "evidence": "smali/com/example/AdHelper.smali: loadAd call"}
  ],
  "mediationSdks": [
    {"network": "applovin-max", "listener": "MaxAdListener", "evidence": "smali/com/example/MaxHelper.smali"}
  ],
  "permissions": ["INTERNET", "AD_ID"],
  "featureFlags": [
    {"name": "IS_PREMIUM", "file": "smali/com/example/BuildConfig.smali", "value": "false", "gate": "if-eqz"}
  ],
  "integrityChecks": [
    {"type": "self-signature", "file": "smali/com/example/SignCheck.smali", "method": "check()Z", "bypassable": true}
  ],
  "nativeIntegrityChecks": [
    {"lib": "libnative.so", "pattern": "GET_SIGNATURES", "bypassable": false}
  ],
  "authDependencies": [
    {"kind": "google-signin", "evidence": "res/values/strings.xml: default_web_client_id"}
  ],
  "nativeLibs": [
    {"abi": "arm64-v8a", "name": "libnative.so", "stripped": true}
  ],
  "needsManualReview": []
}
```

## `work/analyze/REPORT.md` Structure
Markdown document structured with: Summary, Input Metadata, Tech Stack Findings, Ads & Mediation SDK Inventory, Feature Flag Ledger, Integrity Checks & Re-Signing Risks (Java & Native), Native Libraries, Obfuscation Profile, Suggested Conversion Path.

## Expanded Re-Analysis (used by `04-apk-bugfinder`)
When a converted build fails with symptoms not explained by the current `analysis.json`, re-run this playbook with an expanded scan: additional lifecycle hooks (`attachBaseContext`, `onCreate` of custom `Application` classes), hidden signature checks in second-level smali directories (`smali_classes2`+), runtime-downloaded configuration, and per-split grep across all `smali*/` roots. Update `analysis.json` in place and record `needsManualReview` entries for anything unverifiable statically.
