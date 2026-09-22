---
name: 01-apk-edition-analyzer
description: Deep static reverse-engineering analyzer for Android APK/XAPK packages. Maps ads SDKs, feature flags, premium gates, obfuscation, native libraries, integrity checks, and authentication dependencies. Outputs machine-readable analysis.json and human-readable REPORT.md for downstream converters. Read-only.
---

# Skill: 01-apk-edition-analyzer

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard Android technical terms.

## Trigger
User asks to analyze an APK/XAPK to detect its edition, inspect ads/premium gates, or runs `/01-apk-edition-analyzer`.

## Workflow

### Phase 1: Validate, Unpack & Layout Inspection
**Objective**: Unpack package structures and isolate primary APK and split bundles.

- Verify input file exists with `.apk` or `.xapk` extension. Confirm app legal ownership; halt execution if ownership is not confirmed.
- If `.xapk`: extract to `work/analyze/unpacked/`, list splits (`config.*.apk`) and `obb/` assets. Select primary `base.apk` for deep decompilation while recording split layouts.
- If single `.apk`: select input file directly for decompilation.

### Phase 2: Manifest & Signature Fingerprinting
**Objective**: Extract package metadata, permissions, launch points, ABI support, and signature schemes.

- Run `aapt2 dump badging <apk>` and `aapt2 dump xmltree --file AndroidManifest.xml <apk>` to extract:
  - `package`, `versionCode`, `versionName`, `applicationId`, launcher activity.
  - Declared permissions (specifically `INTERNET`, `AD_ID`, `BILLING`).
  - `minSdk`, `targetSdk`, `extractNativeLibs`, and supported ABIs from `native-code`.
- Run `apksigner verify --print-certs <apk>` to record signature schemes (v1/v2/v3/v4) and certificate fingerprints.
- Record whether the build is debuggable and whether it uses split or app bundle format.

### Phase 3: Decompile & Tech Stack Identification
**Objective**: Disassemble bytecode and resources, determine framework type, and evaluate obfuscation level.

- Run `apktool d <apk> -o work/analyze/decompiled -f` and `jadx --no-res -d work/analyze/jadx <apk>`.
- Detect tech stack from disassembled artifacts:
  - `lib/<abi>/libflutter.so` or `assets/flutter_assets/` → `flutter`
  - `assets/index.android.bundle` or `libreactnativejni.so` → `react-native`
  - `lib/<abi>/libunity.so` or `assets/bin/Data/` → `unity`
  - Otherwise → `native`
- Assess obfuscation level:
  - Check for shortened class hierarchies (e.g. `smali/a/b/c.smali`) and `apktool.yml` framework markers.
  - Set `isObfuscated: true/false` and classify `obfuscationLevel` as `none`, `light`, or `heavy`.

### Phase 4: Scan Ads, Flags, Integrity & Auth Dependencies
**Objective**: Map monetization components, premium branch logic, integrity validation, and auth dependencies.

- Scan Ads & Mediation SDKs: grep `AndroidManifest.xml`, `smali/**/*.smali`, and `resources.arsc` for known ad and mediation networks:
  - AdMob (`com.google.android.gms.ads`), Facebook (`com.facebook.ads`), AppLovin (`com.applovin`), Unity Ads (`com.unity3d.ads`), IronSource (`com.ironsource`), Pangle (`com.bytedance.sdk.openadsdk`).
  - Mediation adapters & listeners: AppLovin MAX (`com.applovin.mediation`), IronSource Mediation (`com.ironsource.mediationsdk`), Unity Services (`com.unity3d.services.ads`).
  - Record each SDK with file path, matched pattern, caller method (`loadAd`, `show`, `initialize`), and registered ad listener callbacks.
- Scan Feature Flags & Premium Gates: grep for `BuildConfig`, `FLAVOR`, `IS_PREMIUM`, `isPremium`, `isPro`, `billing`, `BillingClient`, `purchases`.
  - Record target file, field name, default value, and the gating branch opcodes (`if-eqz` / `if-nez`).
- Scan Self-Signature & Tamper Checks:
  - Java/Smali: grep for `PackageManager.GET_SIGNATURES`, `getSigningCertificateHistory`, `signingInfo`, `hasSigningCertificate`, and custom comparisons on `signatures[0].toByteArray()`.
  - Checksum/Tamper: grep for `classes.dex` CRC32/SHA checks, `META-INF` integrity verification, and debuggable detection (`ApplicationInfo.FLAG_DEBUGGABLE`).
  - Pinpoint the exact method returning the validation boolean (target method for converter patching).
- Scan Platform Attestation & Cert Pinning:
  - Grep for `play.core.integrity`, `safetynet`, `firebase.appcheck` (flag `bypassable: false`).
  - Grep for `okhttp3.CertificatePinner`, `network_security_config.xml`, and custom `X509TrustManager` implementations.
- Scan Authentication Dependencies:
  - Grep for `FirebaseAuth`, `GoogleSignIn`, `CredentialManager`.
  - Flag requirement: re-signing will invalidate Google Sign-In unless the new keystore SHA-1 is added to Firebase Console (`ApiException 10`).

### Phase 5: Native Library Mapping & Artifact Synthesis
**Objective**: Catalog compiled native binaries and compile structured analysis outputs.

- Scan `lib/<abi>/*.so`, checking binary architecture, stripped symbol status, and string references:
  - Monetization & licensing routines.
  - Native signature verification: search `.so` binaries for string constants or JNI calls referencing `GET_SIGNATURES`, `signatures`, `classes.dex`, `META-INF/`, or custom OpenSSL/mbedTLS cert pinning.
- Determine `editionGuess` (`free` vs `paid`) with confidence level (`high`, `medium`, `low`) backed by at least two independent evidence signals.
- Synthesize `work/analyze/analysis.json` and `work/analyze/REPORT.md`.

## Output Format

### `work/analyze/analysis.json`
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
    {"type": "self-signature", "file": "smali/com/example/SignCheck.smali", "method": "check()Z", "bypassable": true},
    {"type": "play-integrity", "file": "smali/...", "method": "unknown", "bypassable": false}
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

### `work/analyze/REPORT.md`
Markdown document structured with: Summary, Input Metadata, Tech Stack Findings, Ads & Mediation SDK Inventory, Feature Flag Ledger, Integrity Checks & Re-Signing Risks (Java & Native), Native Libraries, Obfuscation Profile, Suggested Conversion Path.

## Don'ts
- Do not modify, patch, rebuild, or re-sign the APK within this skill (read-only enforcement).
- Do not guess class names or method signatures on obfuscated code; resolve via string constants and descriptor signatures.
- Do not declare ad SDKs, flags, or integrity checks without concrete grep evidence (file path + smali line/snippet).
- Do not analyze packages without confirming legal ownership.

## Quality Checklist
- [ ] `analysis.json` contains all required schema keys including mediationSdks and nativeIntegrityChecks?
- [ ] Every ad SDK, mediation network, and feature flag lists concrete file and smali evidence?
- [ ] Self-signature checks pinpoint the exact validation method to patch?
- [ ] Re-signing risks (Google Sign-In SHA-1, Play Integrity, App Check, native signature checks) explicitly flagged?
- [ ] Tech stack and obfuscation levels accurately deduced from binary/smali artifacts?
- [ ] `editionGuess` justified by at least two independent indicators?

