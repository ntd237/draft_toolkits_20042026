---
name: 01-apk-brainstorm
description: "Interactive clarification skill for owned-APK free↔paid conversion requests. Surfaces ambiguous conversion parameters (direction, package naming, signing strategy, ad injection mode, verification scope), formulates 2-3 viable options with trade-offs per question, and pauses at a mandatory approval gate before saving docs/specs/spec-<name>.md. Read-write docs scope only (docs/specs/)."
---

# 01-apk-brainstorm — APK Conversion Requirements Clarification

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; spec content in Vietnamese — keep in English: skill names, file paths, shell commands, error messages, and standard Android technical terms.

## Trigger
Activated by `00-apk-orchestrator` for Pipeline 2 or Pipeline 3 when conversion scope is ambiguous: direction unresolved, parameters undefined, signing strategy unclear, or verification expectations unset. Never invoked for fully specified simple conversions (Pipeline 1).

## File Access Scope
- **Read**: input package metadata, existing `work/analyze/analysis.json`, prior `docs/specs/` artifacts.
- **Write**: `docs/specs/spec-<kebab-case-name>.md` only. Never mutate packages, `work/`, `dist/`, or production code.

## Workflow

### Phase 1: Context Survey (Read-Only)
**Objective**: Ground the clarification in concrete package facts before asking anything.

- Inspect the input file name, size, and extension (`.apk` / `.xapk`).
- If `work/analyze/analysis.json` exists, read `editionGuess`, `editionConfidence`, `adsSdks`, `integrityChecks`, `authDependencies`, `isObfuscated`, and tech stack to seed informed option sets.
- If `analysis.json` is absent, list what is unknown and defer fact-finding to `02-apk-plan`; do not guess edition or direction.

### Phase 2: Interactive Conversion Survey
**Objective**: Clarify every parameter that changes the patch plan. Every question MUST include an open write-in option.

Ask only questions whose answers are not already determined. Standard question sets:

1. **Conversion Direction** (if not explicit):
   - Option A: `free2paid` — remove ads, unlock premium.
   - Option B: `paid2free` — inject ads, re-gate premium behind paywall.
   - Option C: `auto` — infer from `analysis.json.editionGuess` and confirm.
   - *Write-in*: user may specify a custom direction or constraint.
2. **Package Naming**:
   - Option A: `keep` original applicationId (required for some device-side upgrade flows).
   - Option B: append suffix (`.paid` / `.free`) to allow side-by-side installation.
   - *Write-in*: custom package name.
3. **Signing Strategy**:
   - Option A: generate a fresh keystore (default; the original certificate is never reusable).
   - Option B: user-provided keystore path + alias (credentials via environment variable, never inline).
   - *Write-in*: custom scheme. State plainly: re-signing invalidates Google Sign-In unless the new SHA-1 is registered in Firebase Console (`ApiException 10`).
4. **Ad Unit Strategy** (paid2free only):
   - Option A: Google test ad unit IDs (safe default; mandatory for any artifact not headed to production).
   - Option B: user-supplied production ad unit IDs (requires explicit ownership confirmation of the ad account).
   - *Write-in*: custom strategy.
5. **Verification Scope** (S1 is always mandatory):
   - Option A: full suite S1–S5 including auth smoke test (requires optional test account credentials).
   - Option B: S1–S3 excluding authentication (no credentials available).
   - *Write-in*: custom suite subset.

### Phase 3: Trade-off Analysis & Recommendation
**Objective**: Present 2–3 viable option bundles with blast radius before recommending a default.

- Bundle the answered parameters into coherent conversion profiles (e.g., "clean unlock: keep package + fresh keystore + full S1–S5").
- For each bundle, state benefits, drawbacks, and blast radius using the matrix in `00-apk-orchestrator/references/apk-pipeline-routing.md` (split packages, obfuscation, `bypassable: false` integrity checks, auth dependencies → Pipeline 3).
- Surface Known Limitations per the two-tier doctrine (README Hard Rule 3): platform attestation (Play Integrity / SafetyNet / server-enforced App Check) and Google Sign-In SHA-1 registration are absolute limitations; server-side *entitlement* gating is overcomable via client-side decision-point patches (Techniques 1–3 in scope; Technique 4 lab-only — confirm explicit opt-in, external proxy infrastructure, and disclosure acceptance in the spec).
- Recommend one default bundle with rationale.

### Phase 4: Approval Gate & Spec Creation (Mandatory Pause)
**Objective**: Consolidate findings, halt for explicit approval, persist the spec only after sign-off.

- Present a consolidated summary: resolved parameters, chosen profile, limitations, verification scope.
- **Halt the turn.** Do not save the spec or advance to `02-apk-plan` / `06-apk-test` until the user grants explicit approval.
- On approval, save `docs/specs/spec-<kebab-case-name>.md` (e.g., `spec-appx-free2paid.md`) containing: resolved parameters table, conversion profile, verification scope, accepted limitations, and open risks.

## Output Format
`docs/specs/spec-<name>.md` structured as:
```markdown
# Spec: <Conversion Title>
- Input Package: <path> (edition guess, confidence)
- Direction: free2paid | paid2free
- Parameters: package naming, signing, ad units, versionCode bump
- Verification Scope: S1-S5 subset
- Accepted Limitations: server-side entitlement, Play Integrity, Firebase SHA-1
- Open Risks / Write-ins: <any user-provided overrides>
```

## Don'ts
- Do not ask questions already answered by `analysis.json` or the user's request.
- Do not present any question or option set without an open write-in option.
- Do not save `docs/specs/spec-<name>.md` before explicit user approval of the summary.
- Do not recommend reusing or extracting the original APK certificate under any option.
- Do not mutate any file outside `docs/specs/`.
- Do not promise bypass of server-side attestation (Play Integrity, SafetyNet, App Check).

## Quality Checklist
- [ ] Survey grounded in `analysis.json` facts (or explicitly deferred to `02-apk-plan`)?
- [ ] Every question offered 2–3 options plus an open write-in?
- [ ] Trade-off bundles include blast radius and Known Limitations?
- [ ] Execution paused for explicit user approval before saving the spec?
- [ ] Spec persisted to `docs/specs/spec-<kebab-case-name>.md` with all resolved parameters?
