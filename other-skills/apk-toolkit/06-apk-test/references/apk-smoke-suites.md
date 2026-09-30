# APK Smoke Suite Specification (S1–S5)

Executable on-device test suites for converted APK/XAPK artifacts, authored by `06-apk-test` as bash + adb scripts under the root `tests/` directory. Each script exits 0 (PASS) / 1 (FAIL) and writes evidence paths to stdout.

## Common Pre-Flight
1. Artifact integrity: `apksigner verify --verbose <apk>` and `aapt2 dump badging <apk>` (extract `package`, `versionCode`, launcher activity).
2. Device: `adb devices`; if empty, boot AVD and poll `adb shell getprop sys.boot_completed` == `1` (timeout 180s).
3. Clean state: `adb uninstall <package>`; `adb logcat -c`.
4. Install:
   - Single APK: `adb install -r -d <apk>`.
   - Split bundle / XAPK: `adb install-multiple -r -d <base.apk> <config.*.apk> ...`.
   - `INSTALL_FAILED_UPDATE_INCOMPATIBLE` → `adb uninstall --user 0 <package>` (or full uninstall) and retry.
   - `INSTALL_FAILED_DEPRECATED_SDK_VERSION` → retry with `--bypass-low-target-sdk-block`.
5. Launch: `adb shell am start -n <package>/<launcherActivity>`; confirm liveness after 5s: `adb shell pidof <package>`.

## S1 — Rendered UI & Crash-Free Execution (mandatory, never skippable)
- Process presence alone is insufficient (black screen apps pass the PID check).
- Require `adb shell uiautomator dump /sdcard/window_dump.xml` with a visible node hierarchy (pull and verify non-trivial node count).
- Confirm window focus via `dumpsys window` belongs to the target package.
- Check logcat for zero `FATAL` / `AndroidRuntime`, zero native crashes (`A/libc`, `SIGSEGV`, `SIGABRT`, `tombstoned`), zero `ANR`.
- Check framework tags for zero errors: Flutter (`flutter`, `FlutterEngine`), React Native (`ReactNativeJS`), Unity (`Unity`, `UnityMain`).

## S2 — Navigation & View Stability
- Inspect key UI nodes via `uiautomator`.
- Stress with `adb shell monkey -p <package> 50` and confirm the process remains alive with no crashes.

## S3 — Edition Correctness (parameterized by direction)
- **Paid edition (free2paid output)**: UI dump must NOT contain ad views; premium features and menus must be accessible.
- **Free edition (paid2free output)**: UI dump must display ad containers; premium buttons must trigger paywall/purchase flow.
- **Paid-at-startup assertion (S3b pattern)**: with a logged-in session, `force-stop` + relaunch must render the paid edition WITHOUT any purchase/restore. Detect the free-edition upsell marker (paywall banner, upgrade prompt) and assert its absence.
- **Image-only UI markers (critical false-pass trap)**: upsell banners/cards are often rendered as images WITHOUT text nodes or content-desc — `uiautomator` text grep silently passes. Assert via **pixel metrics** instead: screencap the marker region, compute a calibrated color signature (e.g. mean color difference between banner and standard rows) and fail when the marker is present. Calibrate on the free build FIRST (Red must fail with the marker detected), and include controls from marker-free regions of the same screenshot.
- **False-pass guards (mandatory)**: before the assertion, verify the app is actually foreground (`dumpsys activity activities` contains the package), the process is alive (`pidof`), and zero `FATAL EXCEPTION` in PID-isolated logcat — a crashed app falling back to the home launcher otherwise produces a bogus "marker absent" PASS (observed in practice).
- Patch-verification pairs: S3 assertions should pair a STATIC check (marker bytes present in the installed artifact, e.g. patched Hermes operand / class string in dex via pulled-APK inspection) with the RUNTIME check above — static alone proves presence, runtime alone can false-pass.
- **State-persistence assertions (for server-owned settings)**: a patched toggle/setting must be verified over TIME and across restarts, not with a single immediate screenshot: (a) measure the auto-revert window during Red reproduction, (b) after the fix, re-check the state at ≥ that window AND after a fresh `force-stop` + relaunch — both must show the state intact. Pixel-metric assertions (S3b pattern) work well for image-rendered indicators (badges, icons) whose state text is absent from the UI dump.
- **Feature-audit sweep (post-fix regression)**: walk every premium screen (picker grids, theme pickers, management views, media playback) with screencaps + PID-isolated logcat; assert 0 `FATAL EXCEPTION` and 0 `Resources$NotFoundException` per screen. `uiautomator dump` may fail on RN screens ("could not get idle state") — fall back to screencaps.

## S4 — Auth & Integrity Smoke Test
- Clean stale sandbox state before auth tests: `adb shell pm clear <package>` (prevents `AEADBadTagException` / `KeyStoreException` from AndroidKeyStore master key invalidation after re-signing).
- Verify auth/login screens render with accessible input fields.
- If test account credentials are provided in the spec, attempt login.
- Grep logcat for auth failure signals: `ApiException`, `DEVELOPER_ERROR` (new keystore SHA-1 missing in Firebase Console), `401`, `403`, `Play Integrity`, `AppCheck`, `CertificateException`.
- **False-negative guard (misleading "wrong password")**: if spec-provided credentials are rejected with invalid-password/invalid-credential errors, do NOT record as a plain auth failure — retry once after `adb shell pm clear <package>`; still failing → flag suspected `auth-integrity-masking` in `VERIFY_REPORT.md` with logcat evidence and route to `00-apk-orchestrator` for `04-apk-bugfinder` (correct credentials + wrong-password error is the signature of an integrity check masking login). On a re-signed build also suspect `auth-cert-spoofable` (`API_KEY_ANDROID_APP_BLOCKED`) — see the Auth Preservation Recipes in `05-apk-fix/references/apk-fix-playbook.md`.
- **Black screen during credential/password entry (UI automation)**: OEM security blanks the display for secure input (and may hide a system permission dialog such as READ_CONTACTS behind it) when screen capture/automation is active. This is a DEVICE mechanism, not a crash — do NOT classify as engine-init, do NOT retry-loop taps, and do NOT fail the suite for it. Procedure: stop UI automation at the password step, ask the USER to type the credentials directly on the device (mention the hidden permission dialog → tap "Allow"/"Cho phép" if it appears), then resume automated assertions from the post-login state (screencap / fresh `uiautomator dump` showing authenticated content). Record "credential entry performed manually by user (device secure-input mechanism)" in `VERIFY_REPORT.md`.
- `uiautomator dump` on RN/Flutter release builds may repeatedly fail with "could not get idle state" — retry in a bounded loop, then fall back to `adb exec-out screencap -p` + image inspection for assertions.

## S5 — Clean-Device Portability (mandatory before review of the portable deliverable)
- Install on a **pristine environment**: fresh AVD without snapshot, or full `adb uninstall <package>` + `adb shell pm clear` on the current device — no prior install of the app, its splits, or its OBB.
- Install the portable deliverable exactly as an end user would: `.xapk` → `adb install-multiple -r -d` with ALL contained splits; if OBB present, push it first to `/sdcard/Android/obb/<package>/`.
- Verify single-pass install success, then run S1 (launch + rendered UI) on this clean device.
- Coverage comparison — assert the artifact covers the target device:
  - ABI: artifact ABI set (from `aapt2 dump badging` `native-code` of base + splits) must cover `adb shell getprop ro.product.cpu.abilist`, or the deliverable contains a universal fallback.
  - Density/locale: `config.*.apk` coverage must include the device density (`ro.sf.lcd_density`) and locale (`getprop persist.sys.locale`), or the base carries them.
- Record any uncovered axis in `VERIFY_REPORT.md`. S5 failure while S1–S4 passed on the prior device → `portability-gap` bucket (`05-apk-fix`); parts never collected at intake → `incomplete-input`.

## Evidence Export
- PID-isolated logcat: `adb logcat --pid=$(adb shell pidof -s <package>) -d` → `work/verify/logcat.txt` (fall back to package grep if the PID filter is unsupported).
- UI dumps → `work/verify/` alongside `VERIFY_REPORT.md`.

## Verdict Rules
- `PASSED` requires: rendered-UI proof (S1 dump + window focus), zero FATAL/ANR/native crash/engine errors, and every spec'd suite assertion passing.
- Any S1 failure → `FAILED` regardless of other suites.
- Any S5 install failure on the clean device → `FAILED` with portability evidence (coverage table vs device properties).
- Failures on `DEVELOPER_ERROR` / server `401`/`403` / Play Integrity are recorded as `manual` bucket findings, not auto-fix failures.
