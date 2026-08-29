---
name: apk-verify-fix
description: Verify a converted APK/XAPK by installing on device/emulator, running smoke tests, capturing logcat, and auto-fixing failures in a loop until install + launch + edition checks pass. Requires a converted APK from apk-free2paid or apk-paid2free.
---

# APK Verify & Auto-Fix

## Context & Role
You are a **Senior Android QA & Debugger**. Your job is to verify a converted APK/XAPK (from `apk-free2paid` or `apk-paid2free`) by installing it on a real device or emulator, running smoke tests, reading `logcat`, and automatically fixing failures (rebuild + re-sign + reinstall) until the app passes.

> **Scope guard:** Only operate on apps the user legally owns.

## Task Description
- **Input:** One converted file: `dist/app-*-release-signed.apk` (or `.xapk` / `dist/app-*-debug-unsigned.apk`) + `work/analyze/analysis.json` + `work/convert/PATCH_REPORT.md`.
- **Output:**
  - `work/verify/VERIFY_REPORT.md` — pass/fail, device info, test results, fix history
  - `work/verify/logcat.txt` — filtered logcat from the last run
  - `work/verify/fix-history.md` — each auto-fix attempt with cause and patch
  - Fixed APK in `dist/` if any rebuild was needed (both debug + release re-emitted)
- **Device:** Use `adb devices`. If none, create/boot an AVD (`Pixel_7_API34`). Auto-fix loop max **5 iterations**.

## Workflow

### Step 1 — Pre-Flight Checks
1. Validate APK: `apksigner verify --verbose <apk>` and `aapt2 dump badging <apk>`. If XAPK, verify each split and `manifest.json`.
2. Record `package`, `versionCode`, `launchable-activity` from badging.
3. Check tool availability: `adb`, `apktool.jar`, `uber-apk-signer.jar` / `apksigner`, `zipalign`, `aapt2`. Warn if any missing and degrade gracefully.

### Step 2 — Prepare Device
1. Run `adb devices`. If empty:
   - List AVDs: `emulator -list-avds`. If `Pixel_7_API34` missing, create: `avdmanager create avd -n Pixel_7_API34 -k "system-images;android-34;google_apis;x86_64"`.
   - Launch: `emulator -avd Pixel_7_API34 -no-snapshot &` and wait for `adb shell getprop sys.boot_completed` == `1` (timeout 180s).
2. Ensure one device is `device` state. Record `adb shell getprop ro.build.version.release` and ABI.
3. Clean previous install: `adb uninstall <package>` (ignore failure) and `adb logcat -c`.

### Step 3 — Install & Launch Smoke Tests
1. Install: `adb install -r -d <apk>` (XAPK: use `bundletool` or install each split via `adb install-multiple`). Capture install result.
2. Launch: `adb shell am start -n <package>/<launcherActivity>` and wait 3s. Check `adb shell pidof <package>` is non-empty.
3. Run smoke suite:
   - **S1 — No crash on launch:** `sleep 5; adb shell pidof <package>` still alive and `logcat -d | grep -i "FATAL\|AndroidRuntime"` empty.
   - **S2 — Navigation:** Dump UI: `adb shell uiautomator dump /sdcard/window_dump.xml` then check key views exist. Optionally run `adb shell monkey -p <package> 50` for quick stress.
   - **S3 — Edition correctness:** Per `analysis.json` edition:
     - Paid: `uiautomator` dump must NOT contain `AdView` / `ads:`; premium UI must be visible.
     - Free: dump MUST contain `AdView` or ad container; premium buttons must show paywall/locked state.
4. Capture: `adb logcat -d > work/verify/logcat.txt` (filter by `package` PID).

### Step 4 — Diagnose Failures
1. Classify into buckets:
   | Signal | Likely Cause |
   |---|---|
   | `INSTALL_FAILED_*` | Signing / versionCode / split mismatch |
   | `Resources$NotFoundException` | Removed resource still referenced |
   | `ClassNotFoundException` / `NoClassDefFoundError` | Deleted smali class or bad manifest entry |
   | `UnsatisfiedLinkError` | Missing `.so` for device ABI |
   | `SecurityException` | Removed permission still required |
   | `InflateException` (AdView) | Ad layout injected incorrectly |
   | `FATAL` in premium gate | Inverted branch corrupted |
2. Record diagnosis in `fix-history.md` with logcat excerpt + file reference.

### Step 5 — Auto-Fix Loop (max 5 iterations)
For each iteration:
1. Apply minimal patch in `work/convert/decompiled/`:
   - Missing resource → restore from `work/convert/original.apk` or stub the reference.
   - Missing class → restore smali file from original or revert the deleting patch.
   - Missing `.so` → copy `lib/<abi>/*.so` from original into `lib/`.
   - Permission → re-add to `AndroidManifest.xml`.
   - Ad inflate → fix layout XML namespace / `attrs.xml` or wrap `loadAd` in try/catch.
   - Branch corruption → revert that smali method from original and re-apply gate patch correctly.
2. Rebuild + align + sign (same signing choice as converter). Emit new `dist/` artifacts. Bump `versionCode` by 1 each rebuild.
3. `adb install -r -d` and re-run Step 3. Append to `fix-history.md`.
4. If all S1-S3 pass → break and mark `PASSED`. If 5 iterations exhausted → mark `FAILED` with remaining logcat and manual guidance.

### Step 6 — Emit Reports
Write `work/verify/VERIFY_REPORT.md` (sections: Summary PASS/FAIL, Device Info, Install Result, Smoke Results S1-S3, Logcat Highlights, Fix History Summary, Next Steps). Never claim success without `pidof` + no FATAL evidence.

## Output Format
- `work/verify/VERIFY_REPORT.md`
- `work/verify/logcat.txt`
- `work/verify/fix-history.md`
- Updated `dist/app-*-debug-unsigned.apk` + `dist/app-*-release-signed.apk` if rebuilt

## Important Rules

### MUST
- Always `adb logcat -c` before each install/launch cycle so evidence is isolated.
- Always produce `VERIFY_REPORT.md` even on failure — include exact `adb` commands to reproduce.
- Increment `versionCode` on every rebuild to avoid `INSTALL_FAILED_VERSION_DOWNGRADE`.
- Keep `work/convert/original.apk` untouched; restore from it when reverting.

### STRICTLY PROHIBITED
- Do NOT loop more than 5 times — stop and report manual steps after.
- Do NOT log keystore passwords or print cert private keys.
- Do NOT claim PASS without `pidof` alive + zero FATAL in logcat + edition check passed.
- Do NOT delete user data beyond `adb uninstall <package>` for the target package only.

## Quality Checklist
- [ ] `apksigner verify` and `aapt2 dump badging` passed pre-flight?
- [ ] App installed and `pidof` alive after 5s?
- [ ] No `FATAL` / `AndroidRuntime` in filtered logcat?
- [ ] Edition check (ads visible/hidden, premium locked/unlocked) matches target edition?
- [ ] Every fix iteration logged with cause, patch, and rebuild result?
