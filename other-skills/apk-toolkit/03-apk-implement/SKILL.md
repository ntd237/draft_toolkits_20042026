---
name: 03-apk-implement
description: "Green + Refactor execution skill for NEW owned-APK edition conversions. Applies direction-specific patch playbooks (free2paid: ad neutralization + premium unlock; paid2free: ad injection + premium re-gating), neutralizes self-signature checks, rebuilds via apktool, zipaligns, and signs with a fresh keystore (v1+v2) producing both debug-unsigned and release-signed artifacts. Strictly prohibited from bug fixing — all defects belong to 05-apk-fix."
---

# 03-apk-implement — APK Conversion Patch & Build Execution

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; patch reports in professional English with standard Android technical terms.

## Trigger
Activated by `00-apk-orchestrator` or `02-apk-plan` for Pipelines 1, 2, or 3 (new conversion implementations), in both TDD Green mode (after `06-apk-test` Red) and skipped-TDD fallback mode. Never invoked for defect fixes or Post-Review Bug Loop remediation — those belong exclusively to `05-apk-fix`.

## File Access Scope
- **Read**: `work/analyze/analysis.json`, approved spec/plan, `work/convert-<direction>/original.apk` (restore source only).
- **Write**: `work/convert-<direction>/` (decompiled sources, keystore, patch reports) and `dist/` (built artifacts). Never write to `docs/`, `tests/`, or `work/verify/`.

## Workflow

### Phase 1: Workspace Initialization & Keystore Generation
**Objective**: Decode the package, back up the original binary, and create clean signing material.

- Load `work/analyze/analysis.json` (if absent, halt and request `02-apk-plan` analysis — never patch unanalyzed packages).
- Create `work/convert-<direction>/` and `dist/`; back up the input to `work/convert-<direction>/original.apk`.
- Decompile: `java -jar apktool.jar d <input> -o work/convert-<direction>/decompiled -f` (XAPK: decompile each split to `decompiled-<split>`).
- Generate a fresh signing keystore via `keytool` at `work/convert-<direction>/release.keystore` (or load the user-provided keystore per spec). Record the certificate SHA-256 fingerprint in the patch report. Never reuse or extract the original APK certificate. Pass keystore credentials via environment variables only.
- If `analysis.json.authDependencies` contains Google Sign-In / Firebase Auth, note the Firebase Console SHA-1 registration requirement in the report.

### Phase 2: Direction-Specific Transformation
**Objective**: Apply the conversion playbook matching the resolved direction.

- **free2paid**: follow `references/free2paid-playbook.md` — non-destructive ad neutralization (layout placeholder substitution, smali stubbing with correct register types, mediation listener handling), integrity neutralization, premium flag unlock and gate-branch bypass.
- **paid2free**: follow `references/paid2free-playbook.md` — injection mode selection (full XML vs programmatic-only based on SDK presence in dex), manifest permission/activity/meta-data injection, ad initialization with test ad units, premium re-gating with paywall routing.
- Match methods by string constants and descriptor signatures rather than class names when obfuscated.
- Tag every edit with `// PATCH <direction>: <reason>` for auditability by `07-apk-review`.

### Phase 3: Package Refactoring & Multi-Split Handling
**Objective**: Apply package naming decisions and safeguard native/split structure.

- If package rename is chosen in the spec (`<orig>.paid` / `<orig>.free`), update `AndroidManifest.xml` package attribute, `apktool.yml` packageInfo, and smali `R` class references. Skip if `keep`.
- Preserve all native libraries from `lib/<abi>/*.so`.
- For XAPK packages: apply smali and layout patches to the `base` split while keeping resource-only splits intact.

### Phase 4: Rebuild, Align, Sign & Package Portable Deliverable
**Objective**: Produce both required artifacts with dual-scheme signing, packaged for portability per the Output Completeness Standard (`00-apk-orchestrator` Phase 1.6).

- Rebuild: `java -jar apktool.jar b work/convert-<direction>/decompiled -o work/convert-<direction>/unsigned.apk` (append `--keep-broken-res` if resource ID shifts occur on obfuscated builds).
- Align: `zipalign -p -f 4 unsigned.apk aligned.apk`.
- Emit artifacts:
  - `dist/app-<edition>-debug-unsigned.apk` (copy of unsigned build).
  - `dist/app-<edition>-release-signed.apk`:
    ```bash
    apksigner sign --ks work/convert-<direction>/release.keystore --ks-key-alias <alias> \
      --ks-pass pass:<pass> --key-pass pass:<pass> \
      --v1-signing-enabled true --v2-signing-enabled true dist/app-<edition>-release-signed.apk
    ```
- Verify: `apksigner verify --verbose dist/app-<edition>-release-signed.apk` must pass both schemes before handoff. If the input used v3/v4 signing (`analysis.json.signingScheme`), document the downgrade to v1+v2 in `PATCH_REPORT.md` (key-rotation-dependent install paths may be affected).
- For XAPK: rebuild each split, sign each aligned split, package with the original `manifest.json`, and emit both unsigned and signed `.xapk`.
- **Portable packaging (mandatory for split sources)**: emit `dist/app-<edition>-portable.xapk` containing the patched base + EVERY aligned/signed split + updated `manifest.json` (versionCode/versionName) — the portable artifact is what travels to other devices; a merged single APK is emitted only when technically feasible with the trade-off documented.
- **OBB handling**: if the source shipped OBB/expansion files, copy them to `dist/obb/` and document placement in `PATCH_REPORT.md` (`/sdcard/Android/obb/<package>/` on the target device).
- **Coverage disclosure**: record in `PATCH_REPORT.md` the ABI/density/locale coverage of the deliverable and whether it covers the target device's `ro.product.cpu.abilist`.

### Phase 5: TDD Green Loop & Patch Report
**Objective**: Turn failing smoke assertions Green, refactor safely, and document every patch.

- **TDD Active mode**: run the failing suite from the Red handoff (`06-apk-test` executes it; this skill consumes the failure contract). Apply minimal patches until the targeted assertions pass; repeat per atomic unit. During Refactor, clean up patch debris (dead stubs, duplicate placeholders) without changing observable behavior, and re-verify the signature.
- **TDD Skipped mode**: emit the Code Handoff to `06-apk-test` (Scenario B) for mandatory post-implementation verification, or attach manual verification evidence when `skip_reason: "no-test-framework"`.
- Generate `work/convert-<direction>/PATCH_REPORT.md`: every patched file, line, and reason; keystore SHA-256 fingerprint; signing schemes; test ad IDs (paid2free); Known Limitations (server-side entitlement, Play Integrity, Firebase SHA-1).

## Output Format
- `dist/app-<edition>-debug-unsigned.apk` (or `.xapk`)
- `dist/app-<edition>-release-signed.apk` (or `.xapk`)
- `dist/app-<edition>-portable.xapk` (mandatory for split sources) + `dist/obb/` (if OBB present)
- `work/convert-<direction>/PATCH_REPORT.md` (incl. coverage disclosure)

## Don'ts
- Do not fix bugs or remediate `07-apk-review` defects — hand off to `00-apk-orchestrator` for routing to `05-apk-fix`.
- Do not reuse or extract the original APK certificate for signing.
- Do not delete ad components from Manifest or ad view IDs from layouts (prevents `ClassNotFoundException` and layout inflation crashes).
- Do not stub `isLoaded` / `isAdLoaded` to return `true` (causes NPE when callers trigger `show()` on uninitialized ads).
- Do not strip or delete `BillingClient` structures; bypass or re-gate entitlement checks instead of removing classes.
- Do not rename obfuscated classes or rely on unstable class identifiers.
- Do not produce only a single artifact; always emit both debug-unsigned and release-signed builds.
- Do not log or echo keystore passwords or private keys into reports or terminal.

## Quality Checklist
- [ ] `analysis.json` loaded and all detected ads SDKs, mediation listeners, and premium gates addressed?
- [ ] Direction playbook followed with every edit tagged `// PATCH <direction>: <reason>`?
- [ ] APK rebuilt, zipaligned, and signed with v1 and v2 schemes enabled (`apksigner verify --verbose` passed)?
- [ ] Fresh keystore used and SHA-256 fingerprint recorded in `PATCH_REPORT.md`?
- [ ] Both debug-unsigned and release-signed artifacts emitted to `dist/`?
- [ ] Portable deliverable packaged (base + all splits + `manifest.json`) and OBB copied with placement instructions; coverage disclosed in `PATCH_REPORT.md`?
- [ ] TDD Green achieved on targeted assertions (or Scenario B handoff / manual evidence delivered)?
