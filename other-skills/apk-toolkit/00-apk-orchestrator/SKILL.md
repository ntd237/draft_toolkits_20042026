---
name: 00-apk-orchestrator
description: "Master orchestrator and Domain Gatekeeper for owned-APK/XAPK free↔paid conversion engineering (edition analysis, ad neutralization/injection, premium gating/ungating, signature-check bypass, rebuild/zipalign/sign, and on-device smoke verification). Classifies requests into 3 groups, assesses blast radius across package tiers, coordinates 6 canonical pipelines, enforces TDD discipline with skip and inverted mechanisms, manages approval checkpoints, and drives the Post-Review Bug Loop. Mandatory entrypoint for all APK conversion tasks."
---

# 00-apk-orchestrator — APK Edition Conversion Orchestrator

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard Android technical terms.

## Trigger
Triggers for any request involving free↔paid edition conversion of legally owned Android packages (`.apk` / `.xapk`): edition detection and static analysis, ad SDK removal or injection, premium flag gating/ungating, self-signature check neutralization, rebuild + zipalign + signing with a fresh keystore, and on-device installation/smoke verification with auto-fix. Mandatory entrypoint before any child skill (01–07) executes.

## Workflow

### Phase 1: Domain Gatekeeper & Legal Preflight
**Objective**: Verify the request falls strictly within owned-APK conversion boundaries.

1. **In-Scope Evaluation**: Accepts tasks operating on `.apk` / `.xapk` packages the user legally owns: edition analysis, free→paid conversion (ad removal, premium unlock), paid→free conversion (ad injection, premium re-gating), signature-check bypass for re-signed builds, keystore generation, rebuild/align/sign, and on-device verification with auto-fix.
2. **Out-of-Scope Rejection**: If the task is unrelated to APK edition conversion (e.g., developing a new Android app from scratch, generic reverse engineering for research, scraping store listings, modifying packages the user does not own) → politely decline, declare that this toolkit specializes exclusively in owned-APK edition conversion, and halt.
3. **Legal Ownership Gate**: Before any decompilation, confirm the user legally owns the target application. If ownership is not confirmed, halt and request confirmation. Never proceed on third-party or store-pirated packages.
4. **Toolchain Preflight**: Verify CLI availability: `java`, `apktool.jar`, `keytool`, `zipalign`, `apksigner` (or `uber-apk-signer.jar`), `aapt2`, `adb`. Halt immediately with an actionable error naming any missing binary.
5. **Input Completeness Gate (Split APK Protection)**: Before classification, verify the input is a complete package, not a lone base split from a Play Store split install:
   - **Provenance check**: confirm where the package came from. If it was copied from an app installed on a device (MTP copy or a single-path `adb pull`), treat it as potentially incomplete — device-installed apps are usually split APKs (`base.apk` + `config.*.apk` per ABI/density/language).
   - **Split recovery**: on the source device run `adb shell pm path <package>`; if it returns multiple paths, pull EVERY path (`adb pull <path>` for each) and treat the full set as the input (later installed via `adb install-multiple`). A lone `base.apk` MUST NOT enter the pipeline — halt and guide the user through split recovery, or request an `.xapk` bundle.
   - **Heuristic pre-check** for an unaccompanied `.apk`: if `aapt2 dump badging` shows no `native-code` line and no `densities`/locale coverage while the app is expected to ship ABIs (per user declaration), or the manifest declares `android:isolatedSplits="true"`, halt and request the complete split set before proceeding. Heuristics are secondary to provenance — a clean badging does not prove completeness.
   - `.xapk` inputs shipping all splits with `manifest.json` are complete by construction; record the split inventory for `02-apk-plan`.
6. **Output Completeness Standard (Portable Deliverable)**: the pipeline's end goal is a self-contained build that installs and runs on ANY other device (or the current device) — not merely a converted APK:
   - A **complete build** = patched base + EVERY config split collected at intake + OBB/expansion files (if present) + ABI/density/locale coverage that covers the target device (or a universal bundle).
   - Default portable deliverable: a packaged `.xapk` (base + all patched splits + updated `manifest.json`) or `.apks` — **never a lone patched APK when the source was a split app**.
   - A merged/universal single APK is allowed only when technically feasible, with the trade-off documented in `PATCH_REPORT.md`.
   - Server-only components (Play-distributed dynamic feature modules, Play Integrity, server-side entitlement) are limitations to disclose — never promised as bundled. Per the two-tier doctrine (README Hard Rule 3): client-side decision-point patches for server-gated state are in scope; attestation itself is never bypassed, and backend-response rewriting (Technique 4, MITM) is lab-only with explicit spec opt-in and verbatim `PATCH_REPORT.md` disclosure.
7. **Hybrid Handling**: If the request bundles unrelated work (e.g., "convert the APK and also rebuild the landing page"), restrict this toolkit to the APK conversion pipeline and delegate other tasks to their respective toolkits.

### Phase 2: Request Classification (3 Groups)
**Objective**: Classify the request into 1 of 3 operational groups:

1. **Group 1: New Implementation**: A new conversion run (free2paid or paid2free), a re-conversion with changed parameters (new package name, new keystore, different injection mode), or an extension of the patch playbooks.
2. **Group 2: Unknown-Cause Bug**: The converted build exhibits symptoms without a verified root cause (install failure, crash on launch, black screen, ads still visible, premium still locked, ANR) → mandatory routing to `04-apk-bugfinder`.
3. **Group 3: Known-Cause Bug**: Defect with confirmed root cause and exact location from `logcat`, a diagnostic bucket in `work/verify/fix-history.md`, or a `[BLOCKING]` finding from a `07-apk-review` report.

### Phase 3: Blast Radius & Conversion Risk Assessment
**Objective**: Determine whether `01-apk-brainstorm` and/or `02-apk-plan` are mandatory based on `references/apk-pipeline-routing.md`.

- **Ambiguous Scope** (direction `auto` not resolvable from `analysis.json`, unclear package naming, unknown signing preference, undefined ad unit strategy for paid2free) → mandatory `01-apk-brainstorm`.
- **Complex / High Risk** (XAPK multi-split packages, heavy obfuscation, native integrity checks marked `bypassable: false`, auth dependencies such as Firebase/Google Sign-In, server-side attestation present) → mandatory `02-apk-plan`.
- **Simple & Localized** (single clean APK, light/no obfuscation, direction and parameters fully specified) → bypass planning and enter TDD directly.

### Phase 4: Route to 6 Canonical Pipelines & Checkpoint Gates
**Objective**: Direct work through exactly 1 of 6 canonical pipeline flows:

| # | Pipeline Name | Skill Execution Sequence |
|---|---|---|
| **1** | Simple Conversion | `06-apk-test` (Red) → `03-apk-implement` (Green+Refactor)* → `07-apk-review` |
| **2** | Ambiguous Conversion | `01-apk-brainstorm` → User Approval → `06-apk-test` (Red) → `03-apk-implement` (Green+Refactor)* → `07-apk-review` |
| **3** | Complex / Multi-Split Conversion | `01-apk-brainstorm` → User Approval → `02-apk-plan` → User Approval → [TDD Waves: `06-apk-test` Red → `03-apk-implement` Green+Refactor]* → `07-apk-review` |
| **4a** | Unknown Bug (Simple) | `04-apk-bugfinder` → `06-apk-test` (Red) → `05-apk-fix` (Green+Refactor)* → `07-apk-review` |
| **4b** | Unknown Bug (Complex) | `04-apk-bugfinder` → `02-apk-plan` → User Approval → [Bug Waves: `06-apk-test` Red → `05-apk-fix` Green]* → `07-apk-review` |
| **5** | Known Bug (Simple) | `06-apk-test` (Red) → `05-apk-fix` (Green+Refactor)* → `07-apk-review` |
| **6** | Known Bug (Complex) | `02-apk-plan` → User Approval → [Bug Waves: `06-apk-test` Red → `05-apk-fix` Green]* → `07-apk-review` |

(*) Repeat per atomic behavior unit. For TDD skip criteria or Inverted TDD, consult `references/apk-pipeline-routing.md`.

#### Mandatory Approval Checkpoints:
1. **Brainstorm Gate (`01-apk-brainstorm`)**: Formulates conversion parameter options with open write-in choices and trade-offs, and pauses until explicit user approval before saving `docs/specs/spec-<name>.md`.
2. **Plan Gate (`02-apk-plan`)**: Generates an execution plan (`docs/plans/plan-<name>.md`) covering analysis findings, patch waves, build/sign steps, verification scope, and documented limitations (Play Integrity, Firebase SHA-1), and strictly pauses until the user approves the wave breakdown.

### Phase 5: Post-Review Bug Loop Governance
**Objective**: Guarantee that review failures are remediated strictly through bug-fix pipelines.

1. When `07-apk-review` returns `FAIL` (due to ≥1 `[BLOCKING]` issue such as missing dual signing schemes, single emitted artifact, untagged smali patches, secret leakage in reports, or failed S1 rendered-UI evidence), the orchestrator **must** re-route to a bug-fix pipeline (4a, 4b, 5, or 6).
2. The root cause is extracted directly from the review defect report.
3. **Strict Skill Binding**: Defect fixes to decompiled sources must be executed exclusively by `05-apk-fix` (never `03-apk-implement`).
4. **Max 3 Iterations**: If review fails 3 consecutive times on the same issue, halt execution and escalate to the user.

## Execution Log (Harness Log Mechanism)
**Objective**: Persist a per-run harness execution log in `docs/harness-logs/` for every pipeline run.

**MANDATORY LOGGING RULE**:
1. Before dispatching the first skill of any pipeline (1–6), **Read `references/execution-log.md`** and follow its schema verbatim: create `docs/harness-logs/<category>_<task_name>_<yyyymmdd>_<hhmmss>.md` — creating this log file before the first skill runs is **100% MANDATORY for pipelines 1–6**.
2. **Append** one per-skill section immediately after each skill completes (never batch at the end), and the Pipeline summary template when the run concludes (PASS / FAIL / PARTIAL).
3. Take the timestamp from a real shell command — never hardcode or guess it.
4. One log file per pipeline run; single-skill read-only advisory tasks (pure explanation, ad-hoc Q&A) are exempt.
5. In-chat YAML handoff blocks **NEVER** exempt or replace the log file.
6. Log content in Vietnamese; skill names, file paths, commands, and status keywords (COMPLETED, FAILED, PARTIAL, PASS, FAIL) stay in English.

## Output Format
Before invoking child skills, emit a structured coordination block:
- **Domain Gate**: Pass / Reject (ownership confirmed, toolchain preflight, input completeness verified)
- **Classification**: New Implementation / Unknown-Cause Bug / Known-Cause Bug
- **Blast Radius**: Simple / Complex (split packages, obfuscation, integrity checks, auth dependencies)
- **Selected Pipeline**: Scenario # (1–6)
- **Harness Log**: `docs/harness-logs/<category>_<task_name>_<yyyymmdd>_<hhmmss>.md`
- **Next Skill**: First skill to invoke + transition handoff

## Handoff Contract Schemas

### 1. TDD Red Handoff (`06-apk-test` → `03-apk-implement` / `05-apk-fix`)
```yaml
handoff:
  from_skill: "06-apk-test"
  to_skill: "03-apk-implement" # or "05-apk-fix"
  tdd_mode: "active"
  target_files:
    - "work/convert-free2paid/decompiled/smali/com/example/AdHelper.smali"
  failing_test_file: "tests/s3-edition-assertions.sh"
  failing_test_name: "S3 paid edition must show zero ad views in UI dump"
  run_command: "bash tests/s3-edition-assertions.sh dist/app-paid-release-signed.apk"
  observed_failure: "UI dump contains com.google.android.gms.ads.AdView node on main screen"
  next_behavior: "Replace layout AdView tags with same-id gone View placeholders"
```

### 2. TDD Skipped Code Handoff (`00-apk-orchestrator` / `02-apk-plan` → `03` / `05`)
```yaml
handoff:
  from_skill: "00-apk-orchestrator" # or "02-apk-plan"
  to_skill: "03-apk-implement" # or "05-apk-fix"
  tdd_mode: "skipped"
  skip_reason: "no-test-framework" # "user-request" | "no-test-framework" | "config-only"
  target_files:
    - "work/convert-paid2free/decompiled/AndroidManifest.xml"
  task_goal: "Inject AdMob AdActivity declaration and APPLICATION_ID meta-data"
  acceptance_criteria:
    - "Manifest declares com.google.android.gms.ads.AdActivity with configChanges"
    - "meta-data com.google.android.gms.ads.APPLICATION_ID present with test ad unit"
```

### 3. TDD Skipped Test Handoff (`03-apk-implement` / `05-apk-fix` → `06-apk-test`)
```yaml
handoff:
  from_skill: "03-apk-implement" # or "05-apk-fix"
  to_skill: "06-apk-test"
  tdd_mode: "skipped"
  scenario: "B" # "A" for Bug Fix Confirmation | "B" for Post-Implementation Validation
  target_files:
    - "work/convert-free2paid/decompiled/smali/"
  files_modified:
    - "work/convert-free2paid/decompiled/smali/com/example/SignCheck.smali"
  implemented_behavior: "Self-signature check method patched to return true"
  run_command: "bash tests/run-smoke-suite.sh dist/app-paid-release-signed.apk"
```

### 4. Defect Diagnosis Handoff (`04-apk-bugfinder` → `06-apk-test` / `02-apk-plan`)
```yaml
handoff:
  from_skill: "04-apk-bugfinder"
  to_skill: "06-apk-test" # or "02-apk-plan"
  offending_layer: "build-and-signing" # domain tier: intake-analysis | transformation | build-and-signing | device-verification
  exact_location: "work/convert-free2paid/decompiled/res/layout/activity_main.xml:31"
  root_cause: "AdView XML tag retained while SDK classes were stubbed, causing InflateException"
  blast_radius: "simple" # "simple" (Pipeline 4a) | "complex" (Pipeline 4b)
  recommended_fix: "Replace AdView tag with same-id View placeholder, visibility gone"
  cleanup_verified: true # Confirms 100% of [DEBUG-PROBE] instrumentation removed
```

### 5. Review Defect Handoff (`07-apk-review` FAIL → `00-apk-orchestrator`)
```yaml
handoff:
  from_skill: "07-apk-review"
  to_skill: "00-apk-orchestrator"
  verdict: "FAIL"
  re_entry_pipeline: 5 # 4a | 4b | 5 | 6
  blocking_issues:
    - severity: "BLOCKING"
      layer: "build-and-signing"
      location: "dist/app-paid-release-signed.apk"
      root_cause: "APK signed with v2 scheme only; devices below Android 7 fail to install"
      evidence: "apksigner verify --verbose output lists 'Verified using v1 scheme: false'"
```

## Don'ts
- Do not accept conversion tasks on packages the user does not legally own.
- Do not run the pipeline on a lone `base.apk` pulled from a split install — recover the full split set first (Input Completeness Gate, Phase 1.5).
- Do not dispatch `03-apk-implement` to fix bugs or remediate `07-apk-review` defects — all defect fixes belong strictly to `05-apk-fix`.
- Do not bypass `04-apk-bugfinder` when converted-build symptoms have unverified root causes.
- Do not advance past approval gates of `01-apk-brainstorm` or `02-apk-plan` without explicit user sign-off.
- Do not apply Fallback Ordering while TDD is active without recording an approved skip reason (`user-request`, `no-test-framework`, or `config-only`).
- Do not allow the Post-Review Bug Loop to exceed 3 iterations on the same defect.
- Do not run any pipeline (1–6) without creating the harness log in `docs/harness-logs/` first and appending a section after each skill completes — in-chat YAML handoffs never replace the log file.
- Do not log or echo keystore passwords, private keys, or secret tokens into terminal or report outputs.

## Quality Checklist
- [ ] Has the Domain Gate confirmed legal ownership and verified the full CLI toolchain?
- [ ] Was the Input Completeness Gate applied (provenance check, split recovery or heuristic pre-check) before classification?
- [ ] Is the request categorized accurately into 1 of the 3 groups?
- [ ] Does the selected pipeline match 1 of the 6 canonical scenarios?
- [ ] Are mandatory approval checkpoints enforced for conversion specs and patch plans?
- [ ] Does the Post-Review Bug Loop route defects exclusively to `05-apk-fix`?
- [ ] Are structured YAML handoff blocks populated across all skill transitions?
- [ ] Was the harness execution log created in `docs/harness-logs/` before the first skill ran, with a section appended per skill and a pipeline summary at completion (per `references/execution-log.md`)?
