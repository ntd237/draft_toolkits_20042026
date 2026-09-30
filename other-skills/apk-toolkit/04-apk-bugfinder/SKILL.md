---
name: 04-apk-bugfinder
description: "Root cause analysis skill for failing converted APK/XAPK builds. Investigates install failures, launch crashes, black screens, edition assertion misses, and auth errors through logcat diagnosis, PID-isolated capture, uiautomator dumps, and expanded static re-analysis. Produces an evidence-backed RCA with diagnostic bucket classification and blast radius. Read-only on production sources; transient [DEBUG-PROBE] instrumentation only, with mandatory 100% cleanup."
---

# 04-apk-bugfinder — Converted-Build Root Cause Analysis

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; RCA reports in professional English with standard Android technical terms.

## Trigger
Activated by `00-apk-orchestrator` for Pipelines 4a/4b: a converted build exhibits symptoms without a verified root cause (install failure, crash on launch, black screen with live process, ads still visible, premium still locked, ANR, auth rejection).

## File Access Scope
- **Read**: decompiled sources, `analysis.json`, `PATCH_REPORT.md`, `logcat`, `uiautomator` dumps, `fix-history.md`.
- **Write**: `work/verify/` diagnostics and the RCA handoff only. Production sources (decompiled smali/layouts/manifests) are read-only except transient `[DEBUG-PROBE]` instrumentation, which must be 100% removed before a resolved RCA handoff — probes may remain in sources ONLY under an explicit frozen-state handoff (see Phase 4).

## Workflow

### Phase 1: Evidence Capture (Non-Invasive)
**Objective**: Reproduce the symptom and capture complete runtime evidence before touching anything.

- Validate artifact integrity: `apksigner verify --verbose <apk>` and `aapt2 dump badging <apk>` (extract `package`, `versionCode`, launcher activity).
- Prepare the device target: `adb devices`; if empty, boot an emulator (`emulator -list-avds`, then `emulator -avd <name> -no-snapshot &`) and poll `adb shell getprop sys.boot_completed` until `1` (timeout 180s).
- Clean state: `adb uninstall <package>`, `adb logcat -c`, then install (`adb install -r -d` or `adb install-multiple -r -d` for splits) and launch (`adb shell am start -n <package>/<launcherActivity>`).
- Capture: PID-isolated logcat (`adb logcat --pid=$(adb shell pidof -s <package>) -d` → `work/verify/logcat.txt`), `uiautomator dump`, `dumpsys window` focus check, and `adb shell pidof <package>` liveness.

### Phase 2: Diagnostic Classification
**Objective**: Map crash dumps and failures into actionable diagnostic buckets (full table in `05-apk-fix/references/apk-fix-playbook.md`).

- Install failures: `INSTALL_FAILED_UPDATE_INCOMPATIBLE` (signature mismatch → full uninstall), `INSTALL_FAILED_MISSING_SPLIT` (use `install-multiple`), `INSTALL_FAILED_DEPRECATED_SDK_VERSION` (`--bypass-low-target-sdk-block`).
- Runtime crashes: `Resources$NotFoundException`, `ClassNotFoundException`/`NoClassDefFoundError`, `UnsatisfiedLinkError`, `SecurityException`, `InflateException` (AdView), native crashes (`A/libc`, `SIGSEGV`, `SIGABRT`), black screen with live process (engine error, missing ABI `.so`, init deadlock).
- State corruption: `AEADBadTagException` / `KeyStoreException` (AndroidKeyStore master key invalidated by re-signing → `pm clear`).
- **Misleading auth failure — correct credentials rejected as "wrong password"**: NEVER record as a plain credential error. Classify into bucket `auth-integrity-masking` via the discriminator sequence:
  1. `adb shell pm clear <package>` + retry login — rules out stale AndroidKeyStore state silently corrupting the credential payload.
  2. Static check: does an integrity check feed the auth path? Grep for signature-derived keys / dex CRC tokens in the request builder (`analysis.json.integrityChecks` entries with `feedsAuthPath: true`).
  3. `[DEBUG-PROBE]` the local tamper-check return value and the login request body just before send: local check failing or payload mutated before send → **LOCAL masking** (auto-fixable: patch the check method); request reaches the server intact and the server rejects → **SERVER-side anti-tamper whitelist** (manual — disclose, no local bypass).
- **Firebase email/password rejected on a re-signed build — bucket `auth-cert-spoofable` (auto-fixable)**: Google's Identity Toolkit trusts client-asserted headers (`X-Android-Package` / `X-Android-Cert`) with NO cryptographic attestation, and does NOT enforce App Check on its endpoints. Discriminator: replay `POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=<API_KEY>` via curl with spoofed `X-Android-Package: <package>` + `X-Android-Cert: <ORIGINAL cert SHA-1>` — if it returns 200, the failure is purely client-side certificate identity and is fixable by patching the cert provider to return the original SHA-1 (recipe in `05-apk-fix/references/apk-fix-playbook.md`). Error text "wrong password" with correct credentials on a re-signed build is the signature of this bucket, not a credential error.
- **Premium still locked at runtime although conversion patches exist in dex (RN/Hermes apps)**: before blaming the patch, establish WHERE the paid state is decided. Disassemble the Hermes bundle (`hbc-decompiler` / `hbc-disassembler` from hermes-dec — read-only, no reassembly) and inspect the decision component. Distinguish DATA points (RevenueCat mapper, billing stubs — only fire on explicit customerInfo/purchase flows, verifiable via logcat absence) from DECISION points (JS expressions reading the backend user object or remote config — these run at every startup). If no customerInfo fetch occurs in logcat and the state comes from the backend user object, classify bucket `decision-point-miss` (fix recipe in `05-apk-fix/references/apk-fix-playbook.md` / `03-apk-implement/references/free2paid-playbook.md`). Hermes string-table facts: identical literals dedupe into ONE entry (`StringKind.Identifier`), property reads are `GetById`/`TryGetById` instructions carrying a UInt16 string_id operand, function headers carry absolute `@ offset` — combine for single-instruction operand patches.
- **Crash `Resources$NotFoundException` on a drawable with `TypedValue{t=0x1/d=0x0}` (reference to 0x0) when a specific feature renders**: cross-split alias nullification — the drawable is an ALIAS in the base whose target file lives in another split's resource table; the base-only apktool decode emitted `@null`. Confirm by `aapt2 dump resources` on the original base (alias value `@0x7f....`) vs the rebuilt artifact (`@null`) and by locating the target in the other splits' dumps. Bucket `cross-split-alias-null` — Recipe R3 in `05-apk-fix/references/apk-fix-playbook.md`.
- **User setting/toggle reverts itself minutes after enabling (client patch initially worked)**: server-owned state — the toggle persists via a backend profile-update call that the server rejects for non-subscribers, and the periodic user refetch overwrites local state (analytics logs may show the flag being pushed as `false`). Find the client-side display predicate in the decompiled JS (a tiny `value === 'CONST'` comparison function) and classify bucket `server-owned-state` — Recipe R4. Confirm the auto-revert window during reproduction so the fix can be verified over the same duration.
- **Manual bucket (never auto-fix)**: `ApiException` / `DEVELOPER_ERROR` (Google Sign-In — real SHA-1 registration in Firebase Console required), server `401`/`403` on non-ITK endpoints, Play Integrity verdicts, and any endpoint that actually ENFORCES App Check server-side. Record and stop; do not burn fix cycles. An App Check failure is only re-classified to `auth-cert-spoofable` territory (client-side fatal neutralization) after a curl test proves the target endpoint accepts requests WITHOUT the `X-Firebase-AppCheck` header.
- **Black screen at the credential/password entry step (UI automation)**: on many OEMs (OnePlus/Oppo/Samsung) the OS blanks the display for secure input or hides a system permission dialog while screen capture/automation is active — this is a device security mechanism, NOT a crash and NOT an app defect. Never treat it as engine-init failure; never retry-loop taps into the black screen. Hand the device to the USER to type credentials manually (warn about a possible hidden permission dialog such as READ_CONTACTS behind the black screen), then resume automated assertions from the post-login state (fresh `uiautomator dump` / screencap).
- Record findings into `work/verify/fix-history.md` with logcat excerpts as evidence.

### Phase 3: Root Cause Isolation (Graduated Instrumentation)
**Objective**: Pinpoint the exact offending location and verify the causal chain.

- **Non-invasive pass 1**: correlate the diagnostic bucket with `analysis.json` entries (`integrityChecks`, `adsSdks`, `featureFlags`, `authDependencies`) and `PATCH_REPORT.md` edits; locate the patched file/method.
- **Non-invasive pass 2 (expanded)**: if pass 1 cannot isolate the cause, re-capture evidence from different angles and re-run the expanded static scan from `02-apk-plan/references/apk-edition-analysis.md` (hidden signature checks, `smali_classes2`+ roots, lifecycle hooks, per-split grep).
- **Automatic instrumentation (MANDATORY after 2 failed non-invasive passes)**: probe injection is no longer discretionary — inject `[DEBUG-PROBE]` statements at the suspect methods, rebuild + reinstall, and read the logs. **Probe Format Standard (grep-consistent)** — every probe is exactly one tagged pair, reusing a free register:
  ```smali
  const-string vX, "DEBUG-PROBE:<session-id>:<marker>"
  invoke-static {vX, vX}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
  ```
  `<session-id>` = short investigation run id, `<marker>` = site name. Register every probe (file:line, marker) in `work/verify/fix-history.md`; targeted evidence is extracted by `grep DEBUG-PROBE` from `work/verify/logcat.txt`. A single `DEBUG-PROBE` grep must find 100% of inserted probes. Up to 2 probe iterations with different placements; both exhausted without a verified cause → Frozen Investigation (Phase 4).
- Verify the causal chain end-to-end: evidence at the offending location must explain the observed symptom; alternative hypotheses must be actively eliminated, not just unproven.

### Phase 4: Probe Cleanup Verification & Handoff
**Objective**: Leave zero instrumentation behind and hand off an actionable RCA.

- Remove 100% of `[DEBUG-PROBE]` statements from decompiled sources; verify by grep across the entire `work/convert-*/decompiled/` tree. If any probe was rebuilt into an artifact, rebuild and re-sign a clean artifact.
- **Frozen Investigation & Instrumented-State Handoff**: when the investigation freezes without a verified root cause (both probe iterations exhausted, the downstream 2-fix-iteration cap reached, or 3 consecutive review FAILs), do NOT stop silently — emit the frozen-state handoff below: remaining probes (file:line + marker), captured evidence paths, and eliminated hypotheses, so a later session resumes without re-guessing. `cleanup_verified: false` is explicit; `05-apk-fix` inherits the probe-cleanup duty on a successful fix.
- Emit the Defect Diagnosis Handoff (YAML) with `offending_layer` (T1 intake-analysis / T2 transformation / T3 build-and-signing / T4 device-verification), `exact_location`, `root_cause`, `blast_radius` (`simple` → Pipeline 4a, `complex` → Pipeline 4b), `recommended_fix`, and `cleanup_verified: true`.

## Output Format
```yaml
handoff:
  from_skill: "04-apk-bugfinder"
  to_skill: "06-apk-test" # or "02-apk-plan"
  offending_layer: "transformation"
  exact_location: "work/convert-free2paid/decompiled/smali/com/example/SignCheck.smali:57"
  root_cause: "Gate branch inverted incorrectly; premium flag now false on both paths"
  blast_radius: "simple" # "simple" | "complex"
  recommended_fix: "Revert branch to original opcodes, re-apply inversion on the correct register"
  cleanup_verified: true
```

Frozen-state alternative (root cause NOT found — investigation closed without RCA):
```yaml
handoff:
  from_skill: "04-apk-bugfinder"
  to_skill: "00-apk-orchestrator"
  frozen: true
  remaining_probes:
    - "work/convert-free2paid/decompiled/smali/com/example/SignCheck.smali:57 [DEBUG-PROBE:r2-sigcheck]"
  captured_evidence:
    - "work/verify/logcat.txt"
  eliminated_hypotheses:
    - "Gate branch inversion — register values logged correct at both paths"
  cleanup_verified: false
```

## Don'ts
- Do not apply permanent fixes — RCA only. Fixes belong to `05-apk-fix` after handoff.
- Do not classify non-ITK server 401/403, Play Integrity verdicts, Google Sign-In `DEVELOPER_ERROR`, or server-enforced App Check as auto-fixable — bucket them `manual` immediately. Firebase email/password failures on re-signed builds ARE auto-fixable (`auth-cert-spoofable`) but ONLY after the curl discriminator proves the client-side path; never patch attestation-blind.
- Do not consider a failure reproduced without captured evidence (logcat excerpt, UI dump, or install output).
- Do not exceed 2 non-invasive passes before automatic probe injection, and do not exceed 2 probe iterations before Frozen Investigation.
- Do not hand off with `cleanup_verified: true` unless grep confirms zero `[DEBUG-PROBE]` remnants.
- Do not leave probes in sources without an explicit `frozen: true` instrumented-state handoff (which must list every remaining probe).
- Do not mutate `docs/`, `tests/`, or `dist/`.

## Quality Checklist
- [ ] Symptom reproduced with full evidence capture (logcat, UI dump, install output)?
- [ ] Failure classified into a diagnostic bucket with logcat excerpts recorded in `fix-history.md`?
- [ ] Root cause pinpointed to an exact file/method with the causal chain verified?
- [ ] Instrumentation ladder respected (2 non-invasive passes → AUTOMATIC probe injection → max 2 probe iterations)?
- [ ] 100% of `[DEBUG-PROBE]` statements removed and verified by grep (resolved RCA), or an instrumented-state handoff emitted with every remaining probe listed (frozen investigation)?
- [ ] Handoff specifies offending layer, exact location, blast radius, and recommended fix?
