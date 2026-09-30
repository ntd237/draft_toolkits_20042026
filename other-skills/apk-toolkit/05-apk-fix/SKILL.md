---
name: 05-apk-fix
description: "Green + Refactor execution skill for defect resolution in converted APK/XAPK builds. Applies targeted surgical patches per confirmed RCA or review defect report, using snapshot/rollback safety, diagnostic bucket playbooks, versionCode bumps, rebuild + re-sign with the SAME fresh keystore, and capped fix iterations. Exclusive Green skill for all bug pipelines (4a, 4b, 5, 6) and the Post-Review Bug Loop."
---

# 05-apk-fix — Converted-Build Defect Resolution

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; fix history in professional English with standard Android technical terms.

## Trigger
Activated by `00-apk-orchestrator` for Pipelines 4a, 4b, 5, or 6, or by the Post-Review Bug Loop when `07-apk-review` returns FAIL. Requires either a `04-apk-bugfinder` RCA handoff or a `07-apk-review` defect report with a confirmed root cause — never invoked for speculative patching.

## File Access Scope
- **Read**: RCA handoff / review report, `analysis.json`, `PATCH_REPORT.md`, `work/convert-<direction>/original.apk` (restore source), `fix-history.md`.
- **Write**: decompiled sources under `work/convert-<direction>/`, snapshots under `work/verify/snapshot-iter-<N>/`, `dist/` rebuilt artifacts, `work/verify/fix-history.md`. Never write to `docs/` or `tests/`.

## Workflow

### Phase 1: Snapshot Isolation & Fix Target Confirmation
**Objective**: Make every fix attempt reversible and confirm the RCA contract before editing.

- Read the RCA handoff or review report; confirm `root_cause` is concrete (exact file/method or review location with evidence). If only symptoms are present, halt and request `04-apk-bugfinder` routing.
- Before applying any fix at iteration N, snapshot the decompiled sources to `work/verify/snapshot-iter-<N>/`. If iteration N fails to assemble or introduces syntax regressions, roll back to the snapshot before testing another strategy.

### Phase 2: Targeted Patch Application
**Objective**: Apply the minimal surgical patch mapped from the diagnostic bucket (full playbook in `references/apk-fix-playbook.md`).

- Missing resource/class/`.so`: restore from `work/convert-<direction>/original.apk`.
- Missing permission: restore the permission tag in `AndroidManifest.xml`.
- Ad inflate crash (`InflateException`): convert layout ad injection to programmatic-only mode.
- Corrupted gate branch: revert to original opcodes, then correctly rewrite the smali branching logic.
- Signature mismatch on install: full `adb uninstall <package>` (device-side; no source patch).
- Never address `manual` bucket failures (Firebase SHA-1, Play Integrity, server 401/403) with patches — surface them to the user.
- Tag every edit with `// FIX iter-<N>: <reason>`.

### Phase 3: Escalation Guard
**Objective**: Prevent blind patch loops.

- After 2 failed fix iterations (the cap), MANDATORY re-route to `04-apk-bugfinder` with the full `fix-history.md` evidence — never attempt a 3rd patch on the same RCA.
- A further fix round is permitted only after a NEW RCA handoff from `04-apk-bugfinder` (which may arrive as an instrumented-state `frozen: true` report); until then, no patching.

### Phase 4: Rebuild, Re-Sign & Retest Loop
**Objective**: Deliver a corrected signed artifact and verify against the failing assertions.

- Bump `versionCode` by 1 in `apktool.yml` / `AndroidManifest.xml`.
- Rebuild via `apktool b` (with `--keep-broken-res` if resource ID shifts occur), align with `zipalign`, and re-sign with the **SAME fresh keystore** used by `03-apk-implement`, enabling both v1 and v2 schemes.
- Reinstall (`adb install -r -d` or `adb install-multiple` for splits) and hand the rebuilt artifact to `06-apk-test` to re-execute the failing suite.
- **TDD Active mode**: iterate Red → Green per atomic fix until the targeted assertions pass. **TDD Skipped mode** (`user-request`): emit the Scenario A handoff to `06-apk-test` for bug-fix confirmation tests. `manual` failures: deliver manual verification evidence instead.
- Terminate at Green or at the 2-iteration cap (`FAILED` with diagnostic escalation).

### Phase 5: Probe-Cleanup Gate, Symptom Proof & Handoff
**Objective**: Leave zero instrumentation behind, prove the fix, and hand off for review.

- **Probe-cleanup gate (mandatory before every Green handoff)**: grep the entire `work/convert-*/decompiled/` tree for `DEBUG-PROBE`. If probes remain (e.g., inherited from a `frozen: true` instrumented-state handoff of `04-apk-bugfinder`) or any probe was rebuilt into an artifact, remove them, then rebuild + align + re-sign (same keystore) before proceeding; record the cleanup in `fix-history.md`.
- Update `work/verify/fix-history.md`: every attempt with failure cause, applied patch, rebuild outcome, and iteration number.
- Emit the Green & Verified Handoff to `07-apk-review` including `symptom_proof` (mandatory): evidence that the originally failing assertion now passes and no regression was introduced in previously passing suites.

## Output Format
- Updated `dist/app-*-debug-unsigned.apk` and `dist/app-*-release-signed.apk`
- `work/verify/fix-history.md` (complete attempt log)

## Don'ts
- Do not patch without a confirmed RCA or review defect report.
- Do not apply patches without a workspace snapshot for clean rollback.
- Do not re-sign with a different keystore than `03-apk-implement` used (breaks upgrade path and evidence chain).
- Do not waste fix iterations on `manual` bucket failures (attestation, Firebase SHA-1, server auth).
- Do not exceed 2 total fix iterations; escalate with detailed logcat diagnostics.
- Do not emit a Green handoff while any `[DEBUG-PROBE]` remains in sources or in a signed artifact.
- Do not log or print keystore passwords or private keys.
- Do not delete user data beyond `adb uninstall` of the specific target package.

## Quality Checklist
- [ ] Root cause confirmed from RCA handoff or review report before any edit?
- [ ] Workspace snapshot created before each fix iteration?
- [ ] Fix applied from the diagnostic bucket playbook and tagged `// FIX iter-<N>: <reason>`?
- [ ] Escalation guard respected (2 failed fix iterations → mandatory re-route to `04-apk-bugfinder`; no 3rd attempt without a NEW RCA handoff)?
- [ ] Rebuild + zipalign + re-sign (same keystore, v1+v2) and reinstall completed per iteration?
- [ ] Probe-cleanup gate passed (`grep DEBUG-PROBE` = zero) before the Green handoff, with rebuild/re-sign if probes had reached an artifact?
- [ ] fix-history.md updated with cause, patch, and outcome per attempt?
- [ ] Green achieved or 2-iteration cap honored with escalation, and `symptom_proof` delivered to `07-apk-review`?
