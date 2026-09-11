---
name: 04-apk-verify-fix
description: On-device verification and automated iterative debugging engine for converted APK/XAPK packages. Performs installation, multi-signal smoke testing (rendered UI, navigation, edition status, auth), logcat diagnosis, and targeted auto-fix loops (up to 5 iterations). Requires a converted APK artifact.
---

# Skill: 04-apk-verify-fix

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard Android technical terms.

## Trigger
User asks to test, verify, or auto-fix a converted APK/XAPK on device/emulator, or runs `/04-apk-verify-fix`.

## Workflow

### Phase 1: Pre-Flight Validation & Target Device Setup
**Objective**: Validate APK signature/metadata integrity and prepare target device/emulator environment.

- Validate artifact integrity: run `apksigner verify --verbose <apk>` and `aapt2 dump badging <apk>`.
- Extract `package`, `versionCode`, and launcher activity from badging.
- Read `analysis.json` integrity checks and auth dependencies to establish test expectations (self-signature patched, Firebase SHA-1 requirement, Play Integrity limitations).
- Prepare testing target:
  - Run `adb devices`. If empty, inspect `emulator -list-avds` and boot an emulator (e.g., `emulator -avd Pixel_7_API34 -no-snapshot &`).
  - Poll `adb shell getprop sys.boot_completed` until return is `1` (timeout: 180s).
- Clean state: execute `adb uninstall <package>` and clear logcat buffer with `adb logcat -c`.

### Phase 2: Installation & Multi-Signal Smoke Testing
**Objective**: Install package, launch main activity, and execute comprehensive S1-S4 smoke test suite.

- Install package:
  - Run `adb install -r -d <apk>`. If installation fails with `INSTALL_FAILED_DEPRECATED_SDK_VERSION`, retry with `--bypass-low-target-sdk-block`.
- Launch main activity:
  - Run `adb shell am start -n <package>/<launcherActivity>`. Verify process existence with `adb shell pidof <package>`.
- Execute Smoke Suites:
  - **S1 — Rendered UI & Crash-Free Execution**:
    - Process presence alone is insufficient (black screen apps pass PID check).
    - Require `adb shell uiautomator dump /sdcard/window_dump.xml` with visible node hierarchy.
    - Confirm window focus via `dumpsys window` belongs to target package.
    - Check logcat for zero `FATAL` / `AndroidRuntime`, zero native crashes (`A/libc`, `SIGSEGV`, `SIGABRT`, `tombstoned`), and zero `ANR`.
    - Check framework tags for zero errors: Flutter (`flutter`, `FlutterEngine`), React Native (`ReactNativeJS`), Unity (`Unity`, `UnityMain`).
  - **S2 — Navigation & View Stability**:
    - Inspect key UI nodes via `uiautomator`. Optionally stress with `adb shell monkey -p <package> 50` and confirm process remains alive with no crashes.
  - **S3 — Edition Correctness**:
    - Paid edition: UI dump must NOT contain ad views; premium features and menus must be accessible.
    - Free edition: UI dump must display ad containers; premium buttons must trigger paywall/purchase flow.
  - **S4 — Auth & Integrity Smoke Test**:
    - Verify auth/login screens render with accessible input fields.
    - If test account credentials are provided, attempt login.
    - Grep logcat for auth failure signals: `ApiException`, `DEVELOPER_ERROR` (new keystore SHA-1 missing in Firebase Console), `401`, `403`, `Play Integrity`, `AppCheck`, `CertificateException`.
- Export filtered logcat to `work/verify/logcat.txt`.

### Phase 3: Diagnostic Classification & Failure Triage
**Objective**: Map logcat crash dumps and test failures into actionable diagnostic buckets.

- Classify failure signals:
  - `INSTALL_FAILED_*`: Signing failure, `versionCode` downgrade, or deprecated SDK level.
  - `Resources$NotFoundException`: Missing resource, drawable, or invalid ID reference.
  - `ClassNotFoundException` / `NoClassDefFoundError`: Deleted class or invalid manifest component.
  - `UnsatisfiedLinkError`: Missing native `.so` library for device ABI.
  - `SecurityException`: Missing manifest or runtime permission.
  - `InflateException` (AdView): Ad layout XML injected without SDK classes present in dex.
  - Process alive with black screen: Engine error, missing ABI `.so`, or init deadlock.
  - Native crash (`A/libc`, `SIGSEGV`): Missing native library or corrupted JNI bridge.
  - `ApiException` / `DEVELOPER_ERROR` / server `401`/`403`: Firebase SHA-1 mismatch or server attestation rejection (classify as `manual` bucket; do not burn auto-fix cycles).
- Record findings into `work/verify/fix-history.md`.

### Phase 4: Targeted Auto-Fix Iteration Loop
**Objective**: Apply surgical patches, bump versionCode, re-sign, and reinstall until tests pass or iteration limit is reached.

- Apply targeted patch in decompiled workspace:
  - Missing resource/class/`.so`: restore from `work/convert-<direction>/original.apk`.
  - Missing permission: restore permission tag in `AndroidManifest.xml`.
  - Ad inflate crash: convert layout ad injection to programmatic-only mode.
  - Corrupted gate branch: revert and correctly rewrite smali branching logic.
- Escalation Guard:
  - If 2 consecutive iterations fail in the identical diagnostic bucket, halt blind patching.
  - Re-run `01-apk-edition-analyzer` with an expanded scan to uncover hidden signature checks or lifecycle hooks. A 3rd consecutive attempt without new diagnosis is prohibited.
- Rebuild, Sign & Retest:
  - Bump `versionCode` by 1 in `apktool.yml` / `AndroidManifest.xml`.
  - Rebuild via `apktool b`, align with `zipalign`, and re-sign with the SAME fresh keystore.
  - Reinstall with `adb install -r -d` and re-execute Phase 2 smoke tests.
  - Terminate loop when all suites pass (`PASSED`) or upon reaching 5 iterations (`FAILED`).

### Phase 5: Verification Reporting & Artifact Handoff
**Objective**: Document test verdicts, logcat evidence, fix chronology, and necessary manual operational steps.

- Synthesize `work/verify/VERIFY_REPORT.md` (Summary verdict, device specifications, install outcome, S1-S4 test results, logcat excerpts, manual registration notices).
- Update deliverables in `dist/` if auto-fixing generated new builds.

## Output Format
- `work/verify/VERIFY_REPORT.md`
- `work/verify/logcat.txt`
- `work/verify/fix-history.md`
- Updated `dist/app-*-debug-unsigned.apk` and `dist/app-*-release-signed.apk` (if rebuild occurred)

## Don'ts
- Do not loop auto-fixing beyond 5 iterations; escalate with detailed logcat diagnostics.
- Do not waste fix iterations on backend attestation or Firebase SHA-1 failures (`DEVELOPER_ERROR`, `401/403`, Play Integrity); classify as `manual` immediately.
- Do not consider an app verified based solely on process existence (`pidof`); UI rendering and absence of engine errors are mandatory.
- Do not log or print keystore passwords or private keys.
- Do not claim `PASSED` status without concrete evidence from S1-S4 checks.
- Do not delete user data beyond `adb uninstall` of the specific target package.

## Quality Checklist
- [ ] Target package installed and PID confirmed alive after 5 seconds?
- [ ] UI verified as rendered via non-empty `uiautomator` dump and non-black screen?
- [ ] Logcat verified free of `FATAL`, native crashes (`A/libc`, `SIGSEGV`), ANR, and stack engine errors?
- [ ] Edition-specific assertions (ads visibility, premium gating) validated?
- [ ] S4 auth test executed and Firebase/integrity logcat signals evaluated?
- [ ] Consecutive failures in the same diagnostic bucket capped at 2 before re-analysis?
- [ ] Every fix attempt logged with failure cause, applied patch, and rebuild outcome?
