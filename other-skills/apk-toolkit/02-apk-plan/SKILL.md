---
name: 02-apk-plan
description: "Planning and static-analysis skill for owned-APK free↔paid conversion. Runs the deep reverse-engineering analysis playbook (edition detection, ads/mediation SDK mapping, feature flags, integrity checks, auth dependencies, native libraries) to produce work/analyze/analysis.json + REPORT.md, then decomposes the conversion into zero-collision TDD waves with risk, rollback, and limitation planning. Pauses at a mandatory plan approval gate before executing docs/plans/plan-<name>.md."
---

# 02-apk-plan — APK Conversion Analysis & Wave Planning

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; plan artifacts in Vietnamese — keep in English: skill names, file paths, shell commands, error messages, and standard Android technical terms.

## Trigger
Activated by `00-apk-orchestrator` for Pipeline 3, 4b, or 6 (complex/high-risk conversions and multi-tier bug fixes), or whenever `work/analyze/analysis.json` does not exist yet and a conversion requires grounding facts before planning.

## File Access Scope
- **Read**: input package, approved `docs/specs/spec-<name>.md`, prior plans.
- **Write**: `work/analyze/` artifacts (`analysis.json`, `REPORT.md`) and `docs/plans/plan-<kebab-case-name>.md` only. Never mutate decompiled sources, `dist/`, or `docs/specs/`.

## Workflow

### Phase 1: Static Analysis & Edition Detection
**Objective**: Produce machine-readable package intelligence per the full playbook in `references/apk-edition-analysis.md`.

- If a valid `work/analyze/analysis.json` newer than the input package exists, reuse it and skip to Phase 2.
- Otherwise execute the playbook end-to-end: validate ownership and input, unpack XAPK splits, fingerprint manifest and signature (`aapt2`, `apksigner verify --print-certs`), decompile (`apktool d`, `jadx --no-res`), identify tech stack and obfuscation level, scan ads/mediation SDKs, feature flags and premium gates, self-signature and tamper checks, platform attestation, auth dependencies, and native libraries.
- Emit `work/analyze/analysis.json` (full schema in the playbook) and `work/analyze/REPORT.md`.
- **Read-only invariant**: no patching, rebuilding, or re-signing in this phase.

### Phase 2: Route Resolution & Feasibility Assessment
**Objective**: Lock the conversion direction and flag anything that makes local conversion infeasible.

- Resolve direction: explicit user choice wins; otherwise map `editionGuess` (`free` → `free2paid`, `paid` → `paid2free`). Confirm with the user on conflict with the approved spec.
- Feasibility gate: if `integrityChecks` or `nativeIntegrityChecks` contain entries with `bypassable: false` (Play Integrity, SafetyNet, App Check, native signature verification), record them as Accepted Limitations in the plan — do not plan to bypass them. Per the two-tier doctrine (README Hard Rule 3): server-side *entitlement* gating without attestation is not automatically a limitation — plan client-side decision-point patches (Techniques 1–3) as in-scope waves; Technique 4 (MITM) requires explicit spec opt-in, external proxy infrastructure, and verbatim disclosure — plan it as a manual, non-bundled step or exclude it.
- If `authDependencies` include Google Sign-In / Firebase Auth, add a manual registration step: new keystore SHA-1 must be added in Firebase Console (`ApiException 10` otherwise).

### Phase 3: Wave Decomposition
**Objective**: Break the conversion into atomic TDD units mapped to domain tiers with zero file collisions.

- Decompose into units sized for one Red-Green-Refactor cycle, each mapped to a tier:
  - T1 Intake & Analysis: `analysis.json` completeness (ads, mediation, flags, integrity, auth).
  - T2 Transformation: one unit per patch family (ad layout placeholders, ad smali stubbing, premium flag/gate unlock or re-gating, signature-check neutralization, manifest edits, package rename).
  - T3 Build & Signing: rebuild, zipalign, keystore generation, dual-scheme signing, signature verification.
  - T4 Device Verification: smoke suite S1–S5 execution scope.
- Enforce the Zero-Collision Invariant: units in the same wave must touch strictly disjoint file sets (e.g., separate waves for `res/layout/*` edits and `smali/<pkg>/*` edits when both are large); serialize overlapping units into consecutive waves.
- For bug pipelines (4b/6): group fixes by diagnostic bucket from the RCA report into waves with per-wave re-verification.

### Phase 4: Risk, Rollback & Limitation Plan
**Objective**: Make every wave reversible and every unfixable risk explicit.

- Rollback strategy: pristine backup at `work/convert-<direction>/original.apk` before first decompile; `05-apk-fix` snapshots before each fix iteration.
- Risk ledger: obfuscation level, split handling strategy, resource ID shift contingency (`apktool b --keep-broken-res`), keystore credential handling (environment variables only, never logged).
- Auto-fix budget: cap verification→fix loop at 2 iterations; classify backend attestation / Firebase failures as `manual` immediately (do not burn fix cycles).
- Document Known Limitations verbatim from Phase 2.

### Phase 5: Plan Approval Gate (Mandatory Pause)
**Objective**: Persist the plan, link it, and halt for explicit user approval.

- Save `docs/plans/plan-<kebab-case-name>.md` (e.g., `plan-appx-free2paid-conversion.md`) with: analysis summary, route decision, wave table (unit, tier, exclusive files, verify command), risk/rollback ledger, limitations.
- Provide a clickable link to the plan in chat and **halt execution**. No `06-apk-test` (Red), `03-apk-implement`, or `05-apk-fix` command may run before explicit user confirmation.

## Output Format
`docs/plans/plan-<name>.md` structured as:
```markdown
# Plan: <Conversion Title>
- Spec: docs/specs/spec-<name>.md | Direction: <direction> | Blast Radius: <simple|complex>
- Analysis Summary: edition, tech stack, obfuscation, ads SDKs, integrity, auth
## Waves
| Wave | Unit | Tier | Exclusive Files | Verify Command |
## Risk & Rollback
## Accepted Limitations
```

## Don'ts
- Do not plan or perform any patch, rebuild, or re-sign in this skill (analysis is read-only).
- Do not guess class names or method signatures on obfuscated code; resolve via string constants and descriptor signatures.
- Do not declare ad SDKs, flags, or integrity checks without concrete grep evidence (file path + smali line/snippet).
- Do not plan bypasses for `bypassable: false` checks; record them as Accepted Limitations.
- Do not advance past the Plan Approval Gate without explicit user sign-off.
- Do not create waves with overlapping file sets.

## Quality Checklist
- [ ] `analysis.json` contains all required schema keys with concrete evidence per finding?
- [ ] `editionGuess` justified by at least two independent indicators with confidence level?
- [ ] Route resolution consistent with the approved spec (conflicts surfaced, not silently resolved)?
- [ ] Waves decomposed into zero-collision atomic units mapped to domain tiers?
- [ ] Rollback strategy, auto-fix budget, and keystore credential handling planned?
- [ ] Plan saved, linked in chat, and execution halted for explicit user approval?
