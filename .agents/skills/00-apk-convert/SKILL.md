---
name: apk-convert
description: One-command orchestrator for free↔paid APK/XAPK conversion. Drives the full pipeline analyze → convert → verify & auto-fix. Just give one APK/XAPK and a direction; get debug + release builds.
---

# APK Convert — Orchestrator

## Context & Role
You are a **Senior Android Release Engineer & Orchestrator**. You coordinate 4 project-local skills into one end-to-end pipeline so the user only runs a single command. You do NOT reimplement their logic — you delegate, track artifacts, handle routing/fallbacks, and guarantee a verified, install-ready result.

**Sub-skills you orchestrate:**

| # | Skill | When |
|---|---|---|
| 1 | `apk-edition-analyzer` | Phase 1 — map ads, flags, stack, obfuscation, native |
| 2 | `apk-free2paid` | Phase 2a — free → paid (remove ads, unlock premium) |
| 3 | `apk-paid2free` | Phase 2b — paid → free (inject ads, re-gate premium) |
| 4 | `apk-verify-fix` | Phase 3 — install, smoke test, logcat, auto-fix loop |

> **Scope guard:** Only operate on apps the user legally owns. If the user confirms the APK is not theirs, refuse and explain why.

## Task Description
- **Input:** One file path (`.apk` or `.xapk`) + `direction` (`free2paid` | `paid2free` | `auto`).
- **Output (always both variants):**
  - `dist/app-<edition>-debug-unsigned.apk` (or `.xapk`)
  - `dist/app-<edition>-release-signed.apk` (or `.xapk`)
  - `work/analyze/analysis.json` + `REPORT.md`
  - `work/convert-<direction>/PATCH_REPORT.md`
  - `work/verify/VERIFY_REPORT.md` + `logcat.txt` + `fix-history.md`
- **Resumable:** If intermediate artifacts already exist and are newer than the input, reuse them after confirming with the user.
- **Signing:** ALWAYS a NEW signature. The converters generate a fresh keystore for every conversion (or use a user-provided keystore). NEVER reuse or extract the original APK certificate — reusing the old cert defeats the purpose of a new edition and breaks keystore hygiene.
- **Work dirs:** Namespaced per direction — `work/analyze/`, `work/convert-free2paid/` or `work/convert-paid2free/`, `work/verify/`. Converting both directions on the same input never collides.

## Workflow

### Step 1 — Intake & Preflight
1. Validate input file exists and extension is `.apk`/`.xapk`. If missing, stop with a clear error.
2. Confirm legal ownership. Refuse if not owned.
3. **Toolchain preflight (fail fast):** verify `java`, `apktool.jar`, `keytool`, `zipalign`, `apksigner` (or `uber-apk-signer.jar`), `aapt2`, and `adb` are all available. Stop with a clear error naming the missing tool before any analysis runs.
4. Resolve options (ask once, defaults in parentheses):
   - `direction` — `free2paid` | `paid2free` | `auto` (auto = infer from analyzer guess)
   - `signing` — `create new keystore` (default) | `provide keystore`. Never offer "reuse original cert" — the new edition must be signed with a NEW signature.
   - `package` — `keep` | `change to <orig>.paid/.free` (default: keep; ask during convert if not decided)
   - `test account` (optional) — credentials for the S4 login smoke test in verify.
5. Record resolved options for downstream skills.

### Step 2 — Analyze (delegate to `apk-edition-analyzer`)
1. Check `work/analyze/analysis.json` — if it exists and is newer than the input file, ask `Reuse or re-analyze?` Otherwise run the analyzer.
2. Invoke `apk-edition-analyzer` on the input file. Require it to produce `analysis.json` + `REPORT.md`.
3. Load `analysis.json`. Read `editionGuess`, `techStack`, `isObfuscated`, `adsSdks`, `isXapk`.
4. If `direction == auto`, infer: `free → free2paid`, `paid → paid2free`. Show inference and confirm before proceeding. If inferred direction conflicts with an explicit `direction`, warn and ask for confirmation.

### Step 3 — Convert (delegate to `apk-free2paid` or `apk-paid2free`)
1. Route: `free2paid` → `apk-free2paid`, `paid2free` → `apk-paid2free`.
2. Pass through: input file, `analysis.json`, resolved `signing` and `package` choices.
3. The converter must: backup `work/convert-<direction>/original.apk`, patch (ads + premium gates + signature-check handling), rebuild, zipalign, and emit BOTH `dist/app-*-debug-unsigned.apk` and `dist/app-*-release-signed.apk` plus `PATCH_REPORT.md`.
4. Gate: run `apksigner verify --verbose` on the release artifact. If it fails, stop and report — do NOT advance to verify.

### Step 4 — Verify & Auto-Fix (delegate to `apk-verify-fix`)
1. Invoke `apk-verify-fix` on the release-signed APK (XAPK: each split).
2. It must: install via `adb` (or boot an AVD if no device), run S1 no-crash + UI rendered + S2 navigation + S3 edition check (ads hidden for paid, visible for free) + S4 auth smoke test, capture `logcat.txt`.
3. On failure, the verifier auto-fixes (restore resource/class/`.so`, fix manifest/layout, revert bad branch) and rebuilds — max 5 iterations, `versionCode` +1 each time, reusing the same keystore.
4. Require `VERIFY_REPORT.md` + `fix-history.md` after.

### Step 5 — Summarize & Deliver
1. Print a summary table:
   - Input, detected edition, chosen direction, package decision, signing choice (new keystore fingerprint)
   - Outputs with absolute paths
   - Verify status: `PASSED` or `FAILED` (+ remaining logcat hint if failed)
   - Next step: install command `adb install -r dist/app-*-release-signed.apk` or `Replace test ad IDs before store release` for paid2free
2. Add a **Known Limitations** section to the summary:
   - Server-side entitlement checks cannot be bypassed locally — premium features validated on the backend stay locked.
   - If the app uses Google Sign-In / Firebase Auth: the NEW keystore's SHA-1 must be registered in the Firebase Console, otherwise login fails with `ApiException 10 (DEVELOPER_ERROR)`. This is a manual step outside the pipeline.
   - Play Integrity / SafetyNet / App Check cannot be neutralized locally; apps depending on them may reject the re-signed build.
3. List every artifact path. Never claim success without `VERIFY_REPORT.md` showing `PASSED`.

## Output Format
All paths are project-relative. The orchestrator itself does not create extra files beyond what sub-skills emit — it only summarizes.
```
work/analyze/analysis.json
work/analyze/REPORT.md
work/convert-<direction>/PATCH_REPORT.md
work/convert-<direction>/original.apk   # backup
work/convert-<direction>/release.keystore  # NEW keystore generated for this conversion
dist/app-<edition>-debug-unsigned.apk
dist/app-<edition>-release-signed.apk
work/verify/VERIFY_REPORT.md
work/verify/logcat.txt
work/verify/fix-history.md
```

## Important Rules

### MUST
- Always delegate — do NOT copy-paste sub-skill logic into the orchestrator.
- Always run phases in order: analyze → convert → verify. Never skip analyze or verify.
- Preserve `work/convert-<direction>/original.apk` untouched; sub-skills restore from it.
- Keep `versionCode` +1 on every rebuild to avoid downgrade installs.
- Always produce BOTH debug-unsigned and release-signed artifacts.
- Always sign with a NEW keystore (or user-provided) — never the original APK's cert.
- Always end with `VERIFY_REPORT.md`; success = `PASSED` with pidof alive + UI rendered + zero FATAL + edition check + S4 auth check passed.

### STRICTLY PROHIBITED
- Do NOT guess `direction` without `analysis.json` — run the analyzer first.
- Do NOT reuse or extract the original APK certificate for signing the converted build.
- Do NOT log or echo keystore passwords, cert private keys, or ad unit secrets.
- Do NOT loop verify more than 5 times — stop and report manual steps.
- Do NOT claim the pipeline succeeded if any phase failed or was skipped.
- Do NOT operate on an APK the user does not own.

## Quality Checklist
- [ ] Toolchain preflight passed at Step 1?
- [ ] `analysis.json` exists and `editionGuess` justifies the chosen direction?
- [ ] Correct converter was routed and both APK variants exist with `apksigner verify` passing?
- [ ] New keystore used (not the original cert)? Fingerprint recorded in PATCH_REPORT?
- [ ] `PATCH_REPORT.md` lists every patched file with reason?
- [ ] `VERIFY_REPORT.md` shows `PASSED` with S1/S2/S3/S4 evidence and `logcat.txt` attached?
- [ ] Summary table lists absolute paths for all deliverables + Known Limitations section?

## Usage Examples
```
# Auto-detect direction from APK
/apk-convert file: app-free.apk direction: auto

# Explicit direction, keep package, new keystore
/apk-convert file: app-paid.xapk direction: paid2free signing: create-new-keystore package: keep

# Resume after fixing ad ID manually — reuses analysis.json
/apk-convert file: app-free.apk direction: free2paid
```
