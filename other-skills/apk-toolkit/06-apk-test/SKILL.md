---
name: 06-apk-test
description: "Test authorship and execution skill for owned-APK conversions. TDD Red phase: authors executable on-device smoke suites (S1 rendered UI/crash-free, S2 navigation, S3 edition correctness, S4 auth, S5 clean-device portability) under the root tests/ directory and establishes the baseline failure. Post-code modes: Scenario A (bug fix confirmation) and Scenario B (post-implementation validation). Enforces the tests/ → test/ → create tests/ directory policy and evidence-backed verdicts."
---

# 06-apk-test — On-Device Smoke Suite Authorship & Execution

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; test scripts and verdicts in professional English with standard Android technical terms.

## Trigger
- **TDD Red (default)**: after pipeline selection, before `03-apk-implement`/`05-apk-fix` — author the failing suite and establish the Red baseline against the input artifact.
- **Scenario A**: after `05-apk-fix` — bug-fix confirmation suite.
- **Scenario B**: after `03-apk-implement` under skipped-TDD fallback — post-implementation validation (mandatory unless `skip_reason: "no-test-framework"`).

## File Access Scope
- **Read**: spec/plan, `analysis.json`, artifacts in `dist/`, RCA handoff.
- **Write**: root `tests/` directory (executable smoke scripts) and `work/verify/` evidence (`VERIFY_REPORT.md`, `logcat.txt`). Never write to decompiled sources or `docs/`.

## Workflow

### Phase 1: Test Directory & Environment Setup
**Objective**: Place suites per the strict location policy and prepare the device target.

- Test Directory Location Policy (strict 3-step priority): use `tests/` if it exists at workspace root; else use `test/` if it exists; else create `tests/`. Never scatter test files in source subdirectories; never maintain dual test roots.
- Prepare target: `adb devices`; if empty, boot an AVD (`emulator -list-avds`, `emulator -avd <name> -no-snapshot &`) and poll `adb shell getprop sys.boot_completed` until `1` (timeout 180s). Clean state: `adb uninstall <package>`, `adb logcat -c`.

### Phase 2: Suite Authorship
**Objective**: Author executable smoke scripts per the S1–S5 specification in `references/apk-smoke-suites.md`.

- One executable script per suite (bash + adb) under the root test directory, each with a machine-readable PASS/FAIL exit and captured evidence paths.
- S3 edition assertions are parameterized by target edition from the spec (`free2paid` expects zero ad views + accessible premium; `paid2free` expects ad containers + paywall routing).
- S4 auth suite requires explicit test credentials from the spec; otherwise author it as render-only (no credential login attempt).
- S5 clean-device portability suite runs against a pristine environment (fresh emulator or full uninstall + `pm clear`, no prior app/splits/OBB) and asserts artifact coverage vs the target device (`ro.product.cpu.abilist`, density, locale) — mandatory for the portable deliverable before `07-apk-review`.
- Tests must assert substantive behavior — never tautological checks (asserting process existence alone is insufficient and prohibited).

### Phase 3: Mode Execution
**Objective**: Establish Red, confirm fixes, or validate post-code.

- **TDD Red**: run the suite against the input artifact (pre-conversion) and the expected post-conversion assertions; record observed failures with exact commands and output (e.g., "S3 paid assertion fails: UI dump contains AdView node"). Emit the TDD Red Handoff to `03-apk-implement`/`05-apk-fix`.
- **Scenario A** (bug fix confirmation): run the suite that previously failed against the rebuilt artifact from `05-apk-fix`; confirm targeted assertions pass and previously passing suites do not regress.
- **Scenario B** (post-implementation): run the full spec'd suite (S1–S5 subset) against the release-signed artifact; any failure emits a handoff back to `00-apk-orchestrator` for `04-apk-bugfinder` routing.
- Install handling per `references/apk-smoke-suites.md` (`install-multiple` for splits, signature-mismatch purge, low-SDK bypass).

### Phase 4: Verdict & Evidence Report
**Objective**: Produce an evidence-backed verdict, never a claim without proof.

- Synthesize `work/verify/VERIFY_REPORT.md`: summary verdict (`PASSED`/`FAILED`), device specifications, install outcome, per-suite S1–S5 results, logcat excerpts, manual registration notices (Firebase SHA-1).
- Export PID-isolated logcat (`adb logcat --pid=$(adb shell pidof -s <package>) -d`) to `work/verify/logcat.txt`.
- **Hard verdict rules**: `PASSED` requires rendered-UI proof (non-empty `uiautomator` dump, window focus on target), zero `FATAL`/ANR/native crash/engine errors, and all spec'd suite assertions passing. Process liveness alone never constitutes a pass.
- Emit the Verified Handoff to `07-apk-review` with `test_status` and evidence paths.

## Output Format
- `tests/` (executable smoke scripts S1–S5 subset)
- `work/verify/VERIFY_REPORT.md`, `work/verify/logcat.txt`
- YAML handoff blocks (TDD Red / Verified) at each transition

## Don'ts
- Do not write tautological tests or rely on process existence (`pidof`) as a pass criterion.
- Do not place test scripts outside the root test directory policy (`tests/` → `test/` → create `tests/`).
- Do not claim `PASSED` without concrete evidence from all spec'd suites.
- Do not attempt credential login without explicit test account credentials in the spec.
- Do not modify decompiled sources, keystore files, or `dist/` artifacts.
- Do not skip post-code testing (Scenario A/B) unless `skip_reason: "no-test-framework"` applies — then deliver manual verification evidence to `07-apk-review` instead.

## Quality Checklist
- [ ] Test directory policy followed (single root test folder, 3-step priority)?
- [ ] S1–S5 suites authored per specification with machine-readable PASS/FAIL?
- [ ] Red baseline established with exact run commands and observed failures (TDD active)?
- [ ] Install handling correct for splits and signature mismatches?
- [ ] S5 clean-device portability executed on a pristine environment with coverage comparison evidence?
- [ ] VERIFY_REPORT.md verdict backed by rendered-UI proof, zero FATAL/ANR/native crashes, and all assertions?
- [ ] Handoffs emitted with test status and evidence paths?
