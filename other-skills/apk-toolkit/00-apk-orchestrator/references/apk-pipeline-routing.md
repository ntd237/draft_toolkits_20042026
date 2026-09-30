# APK Pipeline Routing Matrix & Blast Radius

## Overview
This document defines the routing matrix, blast radius evaluation, and decision heuristics for `00-apk-orchestrator` across owned-APK free↔paid edition conversion tasks.

## Domain Tiers
The APK conversion pipeline replaces the classic Frontend/Backend/Database triad with 4 domain tiers:

| Tier | Name | Contents |
|---|---|---|
| T1 | **Intake & Analysis** | Package unpacking (XAPK splits, OBB), manifest fingerprinting, decompilation (`apktool`, `jadx`), ads/flag/integrity/auth scanning, `work/analyze/analysis.json` |
| T2 | **Transformation** | Smali patching, layout placeholder substitution, manifest edits, premium gating/ungating, package rename |
| T3 | **Build & Signing** | `apktool b` rebuild, `zipalign`, keystore generation, `apksigner` v1+v2 signing, signature verification |
| T4 | **Device Verification** | adb install, smoke suites S1–S5, logcat diagnosis, edition assertions |

## 3 Request Groups & Pipeline Mapping

| Request Group | Description | Selected Pipeline | Primary Skills |
|---|---|---|---|
| **Group 1: New Implementation** | New conversion run (free2paid / paid2free), re-conversion with changed parameters, playbook extension | Pipeline 1 (Simple)<br>Pipeline 2 (Ambiguous)<br>Pipeline 3 (Complex/Risky) | `06-apk-test` (Red) → `03-apk-implement` (Green+Refactor) → `07-apk-review` |
| **Group 2: Unknown-Cause Bug** | Converted build shows unverified symptoms: install failure, launch crash, black screen, ads still visible, premium still locked | Pipeline 4a (Simple RCA)<br>Pipeline 4b (Complex RCA) | `04-apk-bugfinder` → (`06-apk-test` Red → `05-apk-fix` Green)* → `07-apk-review` |
| **Group 3: Known-Cause Bug** | Defect with confirmed root cause: logcat trace mapped to a diagnostic bucket, `fix-history.md` entry, or review defect report | Pipeline 5 (Simple defect)<br>Pipeline 6 (Complex defect) | (`06-apk-test` Red → `05-apk-fix` Green)* → `07-apk-review` |

## 6 Canonical Pipeline Scenarios (Domain-Instantiated)

### Pipeline 1: Simple Conversion
- **Condition**: Single clean APK, direction and parameters fully specified, light/no obfuscation, no auth dependencies, TDD runtime (device/emulator) available.
- **Sequence**: `06-apk-test` (Red: baseline edition assertions) → `03-apk-implement` (Green: patch + build + sign)* → `07-apk-review`.

### Pipeline 2: Ambiguous Conversion
- **Condition**: Direction `auto` cannot be resolved without analysis, signing preference or package naming undecided, ad unit strategy unclear for paid2free.
- **Sequence**: `01-apk-brainstorm` → User Approval Gate (`docs/specs/spec-<name>.md`) → `06-apk-test` (Red) → `03-apk-implement` (Green + Refactor)* → `07-apk-review`.

### Pipeline 3: Complex / Multi-Split Conversion
- **Condition**: XAPK multi-split package, heavy obfuscation, native integrity checks, Firebase/Google Sign-In dependencies, or multiple sequential patch waves required.
- **Sequence**: `01-apk-brainstorm` → User Approval Gate (`docs/specs/spec-<name>.md`) → `02-apk-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Waves: `06-apk-test` (Red) → `03-apk-implement` (Green + Refactor)]* → `07-apk-review`.

### Pipeline 4: Unknown-Cause Bug Investigation & Resolution
- **Condition**: Converted build symptom reported without verified cause (crash on launch, `INSTALL_FAILED_*`, black screen with live process, edition assertions failing unexpectedly).
- **Sequence**: `04-apk-bugfinder` → Evaluates Blast Radius:
  - **4a (Simple / Single-Tier)**: `06-apk-test` (Red: reproduce failure) → `05-apk-fix` (Green: targeted patch + re-sign)* → `07-apk-review`.
  - **4b (Complex / Multi-Tier)**: `02-apk-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Bug-Fix Waves: `06-apk-test` (Red) → `05-apk-fix` (Green)]* → `07-apk-review`.

### Pipeline 5: Known-Cause Bug (Simple)
- **Condition**: Exact location and root cause identified (logcat stack mapped to one diagnostic bucket, one file to patch), localized to a single tier.
- **Sequence**: `06-apk-test` (Red) → `05-apk-fix` (Green + Refactor)* → `07-apk-review`.

### Pipeline 6: Known-Cause Bug (Complex / Architectural)
- **Condition**: Confirmed defect spanning multiple tiers (e.g., corrupted resource IDs in T2 requiring rebuild strategy change in T3 and re-verification scope change in T4), or requiring multi-wave fixes.
- **Sequence**: `02-apk-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Bug-Fix Waves: `06-apk-test` (Red) → `05-apk-fix` (Green)]* → `07-apk-review`.

---

## APK Blast Radius Decision Matrix

Evaluate the following signals to distinguish **Simple** vs **Complex / High Risk**:

| Signal / Axis | Simple (Pipeline 1, 4a, 5) | Complex / High Risk (Pipeline 3, 4b, 6) |
|---|---|---|
| **Package Format** | Single `.apk` | `.xapk` with splits (`config.*.apk`) and/or OBB assets |
| **Obfuscation** | `obfuscationLevel: none` or `light` | `heavy` (shortened smali hierarchies, unstable identifiers) |
| **Integrity Checks** | None, or self-signature checks marked `bypassable: true` | Native (`.so`) signature checks or Play Integrity / SafetyNet / App Check (`bypassable: false`) |
| **Auth Dependencies** | None | FirebaseAuth / GoogleSignIn / CredentialManager (requires Firebase Console SHA-1 registration) |
| **Tech Stack** | `native` (java/kotlin) | `flutter`, `react-native`, or `unity` (engine-level error surfaces) |
| **Tiers Touched** | 1 isolated tier | ≥2 interdependent tiers |
| **Splits Affected** | base split only | Multiple splits requiring coordinated rebuild + `install-multiple` |
| **Rollback Feasibility** | `work/convert-<direction>/original.apk` pristine backup sufficient | Repeated re-sign/install cycles may contaminate device state (`pm clear` required) |

> **Rule**: If ≥1 criterion falls under "Complex / High Risk", the orchestrator MUST route through `02-apk-plan`.

---

## TDD Mode in the APK Domain

The domain "test framework" is an executable on-device smoke suite (`06-apk-test`, scripts under the root `tests/` directory, run via `adb` against a built artifact). Consult `06-apk-test/references/apk-smoke-suites.md` for the S1–S5 suite specification.

- **TDD Active (default)**: `06-apk-test` authors the smoke suite scripts and runs them against the input artifact to establish Red (edition assertions fail against the original edition), then `03-apk-implement` / `05-apk-fix` patches until Green.
- **Skip criteria mapping**:
  - `user-request`: user explicitly asked to patch directly without baseline suite runs.
  - `no-test-framework`: no device or emulator is available (`adb devices` empty and no AVD bootable); fallback to manual verification evidence (install log, screenshots) delivered to `07-apk-review`.
  - `config-only`: changes restricted to metadata (`apktool.yml` versionCode bump, manifest meta-data) with no behavioral patch.
- **Inverted TDD**: permitted for exploratory patching of unfamiliar engine stacks (flutter/react-native/unity) where the failing surface cannot be asserted before a build exists — `03-apk-implement` patches first, then `06-apk-test` authors and runs the substantive regression suite (never token tests).
