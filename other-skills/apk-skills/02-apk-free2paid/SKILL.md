---
name: 02-apk-free2paid
description: Convert a free-edition APK/XAPK into a paid edition by neutralizing ads, bypassing premium feature gates, neutralizing self-signature checks, and producing signed installable release artifacts. Handles obfuscated code, native libraries, and XAPK split packages. Requires analysis.json.
---

# Skill: 02-apk-free2paid

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard Android technical terms.

## Trigger
User asks to convert a free APK to paid edition, remove ads and unlock premium features, or runs `/02-apk-free2paid`.

## Workflow

### Phase 1: Workspace Initialization & Keystore Generation
**Objective**: Decode package sources, back up original binary, and generate a clean signing keystore.

- Load `work/analyze/analysis.json` (invoke `01-apk-edition-analyzer` first if absent).
- Create workspace directories: `work/convert-free2paid/` and `dist/`.
- Back up input package to `work/convert-free2paid/original.apk` (or `.xapk`).
- Decompile package: `java -jar apktool.jar d <input> -o work/convert-free2paid/decompiled -f` (for XAPK, decompile each split to `decompiled-<split>`).
- Generate fresh signing keystore (never reuse original cert):
  - Run `keytool` to generate `work/convert-free2paid/release.keystore` (or load user-specified keystore).
  - Extract and record the certificate SHA-256 fingerprint in the patch report.
  - If `analysis.json.authDependencies` contains Google Sign-In or Firebase Auth, flag that the new SHA-1 fingerprint must be added to Firebase Console (`ApiException 10`).

### Phase 2: Non-Destructive Ad Neutralization
**Objective**: Neutralize ad presentation and network requests while preserving layout hierarchy and manifest structure.

- Manifest preservation:
  - Do NOT delete ad `Activity`, `Service`, or `Receiver` entries, or the `AD_ID` permission. Preserving components prevents `ClassNotFoundException` or `ActivityNotFoundException` from internal references.
- Layout placeholder substitution:
  - For every ad view element (`com.google.android.gms.ads.AdView`, Facebook AdView, etc.) in `res/layout/*.xml`, replace the tag with a generic `<View>` keeping the exact `android:id` and constraints:
    ```xml
    <!-- PATCH free2paid: ad view replaced with same-id placeholder -->
    <View android:id="@+id/<original-ad-id>"
          android:layout_width="match_parent"
          android:layout_height="0dp"
          android:visibility="gone" />
    ```
- Smali bytecode stubbing:
  - Match methods by string constants and descriptor signatures rather than class names when obfuscated.
  - Stub `loadAd` and `show` methods to `return-void` (or return matching register type).
  - Force `isLoaded` and `isAdLoaded` methods to return boolean `false` (`const/4 v0, 0x0; return v0`). Never return `true` as it triggers `show()` crashes on uninitialized ad instances.
  - If ads mediation callbacks exist (`analysis.json.mediationSdks`), ensure listeners (`onAdLoaded`, `onAdDisplayed`) trigger or loading guards bypass waiting to prevent app startup deadlock.
  - Wrap SDK `initialize` calls in try/catch blocks to protect environments lacking Google Play Services.
  - Tag every edit with `// PATCH free2paid: <reason>`. Keep all ad drawables and string resources to prevent `Resources$NotFoundException`.

### Phase 3: Integrity Neutralization & Premium Feature Unlock
**Objective**: Bypass local self-signature validations and unlock premium feature flags and entitlement gates.

- Neutralize Self-Signature Checks:
  - For each entry in `analysis.json.integrityChecks` marked `type: self-signature`, locate the check method (e.g. `check()Z`) and patch it to return true (`const/4 v0, 0x1; return v0`).
  - If custom `X509TrustManager` pins the app's own certificate, patch it to trust the new certificate.
  - Note unbypassable server-side attestation (Play Integrity, SafetyNet) in limitations.
- Unlock Premium Flags & Bypass Gates:
  - Update `BuildConfig` smali: set `IS_PREMIUM`, `FLAVOR`, `IS_PAID` fields to `true` / `"paid"`.
  - Locate branching opcodes gating premium features (`if-eqz` / `if-nez`); invert or NOP branches so premium paths execute unconditionally.
  - Unhide premium UI elements (menus, actions, premium panels).
  - Bypass entitlement checks around `BillingClient` without deleting billing classes; ensure downstream consumers handle null purchase tokens safely.

### Phase 4: Package Refactoring & Multi-Split Handling
**Objective**: Update package identifiers if requested, safeguard native libraries, and patch split configurations.

- Package Name Handling:
  - If package rename is chosen (`<orig>.paid`), update `AndroidManifest.xml` package attribute, `apktool.yml` packageInfo, and smali `R` class references. Skip if keeping original package.
- Obfuscation & Native Libraries:
  - Preserve all native libraries from `lib/<abi>/*.so`.
  - For XAPK packages, apply smali and layout patches to the `base` split while keeping resource-only splits intact.

### Phase 5: Rebuild, Align, Sign & Report
**Objective**: Compile smali back to APK, align uncompressed data, sign with the new keystore, and generate the patch audit report.

- Rebuild package: `java -jar apktool.jar b work/convert-free2paid/decompiled -o work/convert-free2paid/unsigned.apk` (if resource ID shifting occurs on obfuscated builds, append `--keep-broken-res`).
- Align archive: `zipalign -p -f 4 work/convert-free2paid/unsigned.apk work/convert-free2paid/aligned.apk`.
- Sign with the new keystore enabling both v1 and v2 schemes:
  - Copy unsigned artifact to `dist/app-paid-debug-unsigned.apk`.
  - Sign aligned artifact to `dist/app-paid-release-signed.apk`:
    ```bash
    apksigner sign --ks work/convert-free2paid/release.keystore --ks-key-alias <alias> --ks-pass pass:<pass> --key-pass pass:<pass> --v1-signing-enabled true --v2-signing-enabled true dist/app-paid-release-signed.apk
    ```
  - For XAPK: rebuild each split, sign each aligned split, package with original `manifest.json`, and emit both unsigned and signed `.xapk`.
- Verify signature: `apksigner verify --verbose dist/app-paid-release-signed.apk`.
- Generate `work/convert-free2paid/PATCH_REPORT.md` detailing every patched file, line, reason, keystore fingerprint, and limitations.

## Output Format
- `dist/app-paid-debug-unsigned.apk` (or `.xapk`)
- `dist/app-paid-release-signed.apk` (or `.xapk`)
- `work/convert-free2paid/PATCH_REPORT.md`

## Don'ts
- Do not reuse or extract the original APK certificate for signing.
- Do not delete ad components from Manifest or ad view IDs from layouts (prevents `ClassNotFoundException` and layout inflation crashes).
- Do not stub `isLoaded` or `isAdLoaded` to return `true` (causes NPE when callers trigger `show()` on uninitialized ads).
- Do not strip or delete `BillingClient` structures; bypass entitlement checks instead of removing classes.
- Do not hardcode or log keystore credentials in reports or terminal.
- Do not rename obfuscated classes or rely on unstable class identifiers.
- Do not produce only a single artifact; always emit both debug-unsigned and release-signed builds.

## Quality Checklist
- [ ] `analysis.json` loaded and all detected ads SDKs, mediation listeners, and premium gates addressed?
- [ ] Ad views in layout replaced with same-ID View placeholders without deleting view IDs?
- [ ] `isLoaded` methods stubbed to return `false` with exact smali register types?
- [ ] Mediation listeners/loading guards neutralized to prevent startup deadlocks?
- [ ] Self-signature validation methods patched to return pass?
- [ ] Premium flags set to true and gate branches bypassed?
- [ ] APK rebuilt, zipaligned, and signed with v1 and v2 schemes enabled (`apksigner verify --verbose` passed)?
- [ ] Fresh keystore used and SHA-256 fingerprint recorded in `PATCH_REPORT.md`?

