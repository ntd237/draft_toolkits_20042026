# apk-toolkit — Owned-APK Free↔Paid Edition Conversion Toolkit

Standardized 8-skill agent toolkit for converting legally owned Android packages (`.apk` / `.xapk`) between free and paid editions: static edition analysis, ad neutralization/injection, premium gating/ungating, self-signature check handling, rebuild/zipalign/sign with a fresh keystore, and on-device smoke verification with capped auto-fix.

## Skill Map

| Skill | Responsibility | File Access Scope |
|---|---|---|
| `00-apk-orchestrator` | Domain gatekeeper (legal ownership + toolchain preflight), 3-group classification, 6-pipeline coordination, Post-Review Bug Loop | Read-only |
| `01-apk-brainstorm` | Clarify conversion parameters (direction, package naming, signing, ad units, verification scope); approval gate → `docs/specs/` | `docs/specs/` only |
| `02-apk-plan` | Static analysis playbook (`analysis.json` + `REPORT.md`), wave decomposition, risk/rollback/limitation plan; approval gate → `docs/plans/` | `work/analyze/`, `docs/plans/` |
| `03-apk-implement` | Green + Refactor for NEW conversions: direction playbooks, rebuild, zipalign, fresh-keystore v1+v2 signing, portable `.xapk` packaging + OBB | `work/convert-*/`, `dist/` |
| `04-apk-bugfinder` | RCA for failing converted builds: logcat diagnosis, diagnostic buckets, graduated instrumentation, 100% probe cleanup | Read-only (transient probes) |
| `05-apk-fix` | Defect fixes per RCA/review: snapshot/rollback patches, same-keystore re-sign, 2-iteration cap | `work/convert-*/`, `dist/`, `work/verify/` |
| `06-apk-test` | TDD Red / Scenario A / Scenario B: executable S1–S5 on-device smoke suites (incl. S5 clean-device portability) under root `tests/` | `tests/`, `work/verify/` |
| `07-apk-review` | Multi-tier audit: signing hygiene, patch tags, TDD compliance, limitation disclosure; PASS/FAIL verdict | Read-only |

## Domain Tiers
- **T1 Intake & Analysis** → `02-apk-plan`
- **T2 Transformation** → `03-apk-implement` / `05-apk-fix`
- **T3 Build & Signing** → `03-apk-implement` / `05-apk-fix`
- **T4 Device Verification** → `06-apk-test`

## Hard Rules
1. Only operate on packages the user legally owns.
2. Never reuse or extract the original APK certificate; always sign with a fresh (or user-provided) keystore, v1+v2 schemes.
3. Never attempt to bypass `bypassable: false` checks (Play Integrity, SafetyNet, App Check, native attestation) — they are documented limitations. **Two-tier doctrine for server-side gating**: platform attestation is an absolute no-bypass tier; server-side *entitlement/feature* gating (no attestation involved) is a separate tier — client-side decision-point patches (Techniques 1–3, `free2paid-playbook.md`) are in scope, while backend-response rewriting via MITM proxy (Technique 4) is lab-only: explicit spec opt-in, external proxy infrastructure outside the deliverable, and verbatim `PATCH_REPORT.md` disclosure are mandatory.
4. All defect fixes go through `05-apk-fix`; `03-apk-implement` is prohibited from bug fixing.
5. TDD is the default (baseline smoke suite → patch → Green); skips require a declared reason (`user-request`, `no-test-framework`, `config-only`).
6. Auto-fix is capped at 2 iterations; Firebase/attestation failures are `manual` and never consume fix cycles.
7. Every pipeline run (1–6) writes a harness execution log to `docs/harness-logs/` — created before the first skill runs, one section appended per skill, pipeline summary at completion (in-chat YAML handoffs never replace it).
8. Never patch a lone `base.apk` pulled from a split install — recover the full split set first (Input Completeness Gate in `00-apk-orchestrator`, Phase 1.5).
9. The default deliverable is a portable package (`.xapk`/`.apks`: patched base + all splits + OBB + `manifest.json`), never a lone patched APK from a split source; it must pass the S5 clean-device portability suite before review.

## Language & Artifact Standards
- **Skill definitions & references** (`SKILL.md`, `references/`): professional English.
- **Specs, plans & harness logs** (`docs/specs/`, `docs/plans/`, `docs/harness-logs/`): Vietnamese Markdown — keep in English: skill names, file paths, shell commands, error messages, and status keywords (COMPLETED, FAILED, PARTIAL, PASS, FAIL).
- **Patch / RCA / verification / review reports** (`PATCH_REPORT.md`, RCA handoffs, `VERIFY_REPORT.md`, `fix-history.md`): professional English with standard Android technical terms (per each skill's Language Protocol).

## References
- `00-apk-orchestrator/references/apk-pipeline-routing.md` — routing matrix, blast radius, TDD mode mapping
- `00-apk-orchestrator/references/execution-log.md` — harness execution log standard (file naming, lifecycle, section/summary templates)
- `02-apk-plan/references/apk-edition-analysis.md` — static analysis playbook + `analysis.json` schema
- `03-apk-implement/references/free2paid-playbook.md` — ad neutralization + premium unlock
- `03-apk-implement/references/paid2free-playbook.md` — ad injection + premium re-gating
- `05-apk-fix/references/apk-fix-playbook.md` — diagnostic buckets + targeted patches
- `06-apk-test/references/apk-smoke-suites.md` — S1–S5 suite specification
- `07-apk-review/references/apk-audit-signals.md` — BLOCKING vs ADVISORY audit signals
