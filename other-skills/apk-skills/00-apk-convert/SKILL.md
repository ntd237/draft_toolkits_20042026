---
name: 00-apk-convert
description: End-to-end orchestrator for free↔paid APK/XAPK conversion. Coordinates analysis, edition conversion (ads removal/injection, premium gating/ungating), signing, and on-device verification with auto-fix loops into a single unified pipeline. Use when the user requests a complete conversion from a single APK/XAPK file.
---

# Skill: 00-apk-convert

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard Android technical terms.

## Trigger
User asks to convert an APK or XAPK between free and paid editions, or runs `/00-apk-convert` specifying an input package and optional conversion direction.

## Workflow

### Phase 1: Intake & Environment Preflight
**Objective**: Validate legal ownership, inspect input package structure, verify toolchain availability, and resolve conversion parameters.

- Verify the input file exists and ends with `.apk` or `.xapk`. Confirm the user legally owns the application; halt execution if ownership is not confirmed.
- Verify CLI toolchain availability: `java`, `apktool.jar`, `keytool`, `zipalign`, `apksigner` (or `uber-apk-signer.jar`), `aapt2`, and `adb`. Halt immediately with an actionable error naming any missing binary.
- Resolve conversion parameters:
  - `direction`: `free2paid`, `paid2free`, or `auto` (inferred from analyzer output).
  - `signing`: generate fresh keystore (default) or user-provided keystore. Never offer or attempt to reuse the original APK certificate.
  - `package`: `keep` (default) or append `.paid` / `.free`.
  - `test account`: optional credentials for auth smoke tests.
- Initialize namespaced workspace directories: `work/analyze/`, `work/convert-<direction>/`, `work/verify/`, and `dist/`.

### Phase 2: Static Analysis & Route Resolution
**Objective**: Map app internals via static analysis and lock conversion direction.

- Check `work/analyze/analysis.json`; reuse existing data if newer than input, otherwise invoke `01-apk-edition-analyzer`.
- Extract `editionGuess`, `techStack`, `isObfuscated`, `adsSdks`, `integrityChecks`, and `authDependencies`.
- If `direction` is `auto`: map `free` → `free2paid`, `paid` → `paid2free`. Confirm with the user if the inferred direction conflicts with an explicit user choice.

### Phase 3: Edition Conversion Execution
**Objective**: Execute code, layout, and manifest transformations according to the selected direction.

- Route to `02-apk-free2paid` for free→paid or `03-apk-paid2free` for paid→free, forwarding `analysis.json`, package decision, and signing settings.
- Ensure the converter creates a pristine backup at `work/convert-<direction>/original.apk`.
- Apply direction-specific patches, neutralize self-signature checks, bump `versionCode` by 1, rebuild via `apktool` (with `--keep-broken-res` if resource ID shifts occur), align with `zipalign`, and sign with the fresh or user-provided keystore enabling both v1 and v2 schemes (`--v1-signing-enabled true --v2-signing-enabled true`).
- Run `apksigner verify --verbose` on the resulting release build before advancing to verification.

### Phase 4: Device Verification & Auto-Fix
**Objective**: Perform installation, multi-signal smoke testing, and iterative auto-fixing on a target device or emulator.

- Invoke `04-apk-verify-fix` on the generated release build (`dist/app-*-release-signed.apk`).
- Verifier handles clean environment setup: clears app data (`pm clear`) to prevent `AEADBadTagException` on `EncryptedSharedPreferences`, resolves `INSTALL_FAILED_UPDATE_INCOMPATIBLE` by full uninstall, and installs via `adb install -r -d` (or `adb install-multiple` for split XAPKs).
- Verifier launches main activity and executes smoke suites:
  - S1: Rendered UI verification, process alive check, zero `FATAL` / ANR / native crash / stack engine error.
  - S2: UI navigation and screen rendering.
  - S3: Edition-specific ad visibility and premium feature state verification.
  - S4: Authentication and login smoke test.
- If failures occur, verifier enters an auto-fix loop with workspace snapshot/rollback (restoring resources/classes, adjusting layout placeholders, handling missing permissions) up to 5 iterations.

### Phase 5: Summarize & Deliver
**Objective**: Produce an execution summary, catalog all generated artifacts, and surface manual operational requirements.

- Format delivery summary table: input package, detected edition, chosen direction, package decision, new keystore SHA-256 fingerprint, signing schemes enabled (v1+v2), and verify status (`PASSED` or `FAILED`).
- Document Known Limitations:
  - Server-side entitlement checks cannot be bypassed locally.
  - Google Sign-In / Firebase Auth requires registering the new keystore SHA-1 in Firebase Console (`ApiException 10`).
  - SafetyNet / Play Integrity server enforcement cannot be bypassed locally.
- Print absolute paths to all deliverables and provide the direct install command (`adb install -r dist/app-*-release-signed.apk` or `adb install-multiple` for split bundles).

## Output Format
Project-relative file layout and delivery summary structure:
```
work/analyze/analysis.json
work/analyze/REPORT.md
work/convert-<direction>/PATCH_REPORT.md
work/convert-<direction>/original.apk
work/convert-<direction>/release.keystore
dist/app-<edition>-debug-unsigned.apk
dist/app-<edition>-release-signed.apk
work/verify/VERIFY_REPORT.md
work/verify/logcat.txt
work/verify/fix-history.md
```

## Don'ts
- Do not guess conversion direction without running or inspecting `analysis.json`.
- Do not reuse or extract the original APK certificate; always generate or use a fresh keystore.
- Do not log or echo keystore passwords, private keys, or secret tokens into terminal or report outputs.
- Do not loop verification and auto-fixing beyond 5 iterations; escalate with detailed diagnostic logcat.
- Do not mark pipeline as successful if any phase failed, was skipped, or if S1 rendered-UI validation failed.
- Do not operate on APKs that the user does not legally own.

## Quality Checklist
- [ ] Toolchain preflight verified all required CLI binaries before analysis?
- [ ] `analysis.json` generated and `editionGuess` verified with supporting evidence?
- [ ] Correct converter dispatched and both debug-unsigned and release-signed builds generated?
- [ ] Fresh keystore generated/applied and its SHA-256 fingerprint documented in `PATCH_REPORT.md`?
- [ ] Signing performed with both v1 and v2 schemes enabled, and `apksigner verify --verbose` passed on release artifact?
- [ ] `VERIFY_REPORT.md` shows `PASSED` with proof of rendered UI, zero FATAL/ANR, clean data isolation, and S1-S4 checks passed?
- [ ] Split bundles installed via `adb install-multiple` or merged cleanly without resource ID collisions?
- [ ] Delivery report includes absolute paths to all artifacts and documents Firebase SHA-1 / Play Integrity limitations?

