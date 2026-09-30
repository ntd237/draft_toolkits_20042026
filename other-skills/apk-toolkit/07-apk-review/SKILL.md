---
name: 07-apk-review
description: "Multi-tier audit skill for owned-APK conversion deliverables. Read-only audit of patch correctness, signing hygiene (fresh keystore, v1+v2 dual schemes), artifact completeness (debug-unsigned + release-signed), report integrity (PATCH_REPORT, VERIFY_REPORT, fix-history), TDD compliance signals, and limitation disclosure. Issues a PASS/FAIL verdict with [BLOCKING] vs [ADVISORY] findings and hands review defects back to 00-apk-orchestrator."
---

# 07-apk-review — APK Conversion Deliverable Audit

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; review reports in professional English with standard Android technical terms.

## Trigger
Activated by `00-apk-orchestrator` at the end of every pipeline (1–6) after Green is achieved. Audits the complete deliverable set: patched sources, signed artifacts, and all reports.

## File Access Scope
- **Read**: everything — `dist/`, `work/convert-<direction>/`, `work/verify/`, `work/analyze/`, `docs/`, `tests/`.
- **Write**: none. Strictly read-only; issues are reported, never patched.

## Workflow

### Phase 1: Artifact & Signing Audit
**Objective**: Verify the deliverable set and signing hygiene.

- Both artifacts present in `dist/`: `app-<edition>-debug-unsigned.apk` and `app-<edition>-release-signed.apk` (or `.xapk` equivalents for split bundles).
- Run `apksigner verify --verbose` on the release artifact: both v1 and v2 schemes must verify.
- Keystore hygiene: certificate used is NOT the original APK certificate; SHA-256 fingerprint documented in `PATCH_REPORT.md`; no keystore passwords or private keys appear in any report, terminal transcript, or smali string constant.
- `versionCode` bumped by exactly 1 from the input for rebuilt artifacts.

### Phase 2: Patch Correctness & Source Hygiene Audit
**Objective**: Audit the transformation quality against the playbook prohibitions.

- Every edit in decompiled sources carries a `// PATCH <direction>:` or `// FIX iter-<N>:` tag; untagged edits are `[BLOCKING]`.
- free2paid: ad components retained in Manifest, ad view IDs preserved as placeholders, `isLoaded` stubs return `false`, mediation listeners neutralized, `BillingClient` structures intact.
- paid2free: injection mode matches SDK presence in dex, `APPLICATION_ID` meta-data present, test ad unit IDs used, premium re-gating restored.
- Self-signature check methods patched to return pass; no attempted bypass of `bypassable: false` checks (Play Integrity, SafetyNet, native checks) — any attempted bypass is `[BLOCKING]`.
- Zero `[DEBUG-PROBE]` remnants: grep the entire `work/convert-*/decompiled/` tree AND the packaged dex of signed artifacts (`grep -a DEBUG-PROBE` on extracted `classes*.dex`) — unless a `frozen: true` investigation handoff is active.
- Obfuscated code: no renamed classes; patches matched by string constants/descriptors.

### Phase 3: TDD Compliance & Test Quality Audit
**Objective**: Verify testing discipline and detect cheating patterns.

- **TDD Active**: Red handoff exists with observed failures, and the Green artifact passes the same suite (verify `VERIFY_REPORT.md` evidence chain).
- **TDD Skipped**: `tdd_mode: "skipped"` and `skip_reason` declared in handoffs and logs; post-code testing (Scenario A/B) performed unless `no-test-framework` with manual verification evidence attached.
- Cheating patterns classified as `[BLOCKING]`:
  - Tautological assertions (e.g., S-checks that only verify process liveness via `pidof`).
  - Editing S3 edition assertions to match a failing output instead of fixing the patch.
  - Missing post-code tests under Fallback Ordering.
  - State contamination (auth suite run without `pm clear`, polluting subsequent suites).
- Test scripts located per the `tests/` → `test/` → create `tests/` policy.

### Phase 4: Report & Limitation Disclosure Audit
**Objective**: Verify audit trail completeness and honest limitation disclosure.

- `PATCH_REPORT.md`: every patched file/line/reason, keystore fingerprint, signing schemes.
- `VERIFY_REPORT.md`: verdict backed by rendered-UI proof, per-suite results, logcat excerpts.
- `fix-history.md` (if fixes occurred): cause/patch/outcome per attempt, iteration cap respected.
- Known Limitations disclosed verbatim: server-side entitlement, Play Integrity/SafetyNet, Firebase SHA-1 registration (`ApiException 10`).
- Delivery includes absolute paths to all artifacts and the direct install command.

### Phase 5: Verdict & Handoff
**Objective**: Issue the verdict and route defects.

- **PASS**: zero `[BLOCKING]` issues. `[ADVISORY]` findings documented for the user without failing the pipeline.
- **FAIL**: ≥1 `[BLOCKING]` issue → emit the Review Defect Handoff to `00-apk-orchestrator` with `re_entry_pipeline` (4a/4b/5/6) recommended by cause specificity (specific location → 5/6; symptoms only → 4a/4b).
- Present findings grouped by layer (T1–T4) with file/line evidence for every issue.

## Output Format
```yaml
handoff:
  from_skill: "07-apk-review"
  to_skill: "00-apk-orchestrator"
  verdict: "FAIL" # or "PASS"
  re_entry_pipeline: 5 # 4a | 4b | 5 | 6 (FAIL only)
  blocking_issues:
    - severity: "BLOCKING"
      layer: "transformation"
      location: "work/convert-free2paid/decompiled/smali/com/example/AdHelper.smali:44"
      root_cause: "isLoaded stubbed to return true, causing NPE on show()"
      evidence: "const/4 v0, 0x1; return v0 in isLoaded()Z"
  advisory_issues: []
```

## Don'ts
- Do not modify any file — findings are reported, never patched (fixes belong to `05-apk-fix` via `00-apk-orchestrator`).
- Do not issue PASS with any `[BLOCKING]` finding, including S1 rendered-UI evidence gaps.
- Do not accept the original APK certificate, single-scheme signing, or a single emitted artifact.
- Do not accept untagged smali/layout edits or `[DEBUG-PROBE]` remnants.
- Do not accept undeclared TDD skips (missing `tdd_mode`/`skip_reason` in handoffs).
- Do not approve undisclosed limitations — disclosure must be verbatim and complete.

## Quality Checklist
- [ ] Both artifacts present and release build verifies v1+v2 schemes?
- [ ] Fresh keystore confirmed, fingerprint documented, zero secret leakage?
- [ ] All edits tagged and playbook prohibitions respected per direction?
- [ ] Zero `[DEBUG-PROBE]` remnants confirmed by grep?
- [ ] TDD compliance verified (Red→Green chain or declared skip with post-code tests/manual evidence)?
- [ ] Reports complete and Known Limitations disclosed verbatim?
- [ ] Verdict issued with evidence-backed findings and correct re-entry routing on FAIL?
