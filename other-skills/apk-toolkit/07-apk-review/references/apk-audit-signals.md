# APK Audit Signals

Reference for `07-apk-review` Phase 2–3: blocking vs advisory classification for owned-APK conversion deliverables.

## [BLOCKING] Signals (mandate FAIL)

| Signal | Observable Pattern | Layer |
|---|---|---|
| **Original certificate reuse** | Signing keystore derived from or identical to the input APK certificate | Build & Signing |
| **Single-scheme signing** | `apksigner verify --verbose` shows v1 or v2 missing on the release artifact | Build & Signing |
| **Incomplete artifact set** | Only one of debug-unsigned / release-signed emitted in `dist/` | Build & Signing |
| **Secret leakage** | Keystore password, private key, or alias credential present in any report, smali string, or log | All |
| **Untagged edits** | Smali/layout/manifest edits lacking `// PATCH <direction>:` or `// FIX iter-<N>:` tags | Transformation |
| **Component deletion** | Ad Activity/Service/Receiver removed from Manifest, ad view IDs deleted from layouts, `BillingClient` classes stripped | Transformation |
| **Unsafe stubbing** | `isLoaded`/`isAdLoaded` returning `true`; XML AdView injected without SDK classes in dex | Transformation |
| **Forbidden bypass attempt** | Patching targeting `bypassable: false` checks (Play Integrity, SafetyNet, App Check, native attestation) | Transformation |
| **Probe remnants in source** | Any `DEBUG-PROBE` tag found by grep in decompiled sources without an active `frozen: true` investigation handoff | Transformation |
| **Probe remnants in signed artifact** | `DEBUG-PROBE` string found in packaged dex (`grep -a DEBUG-PROBE` on extracted `classes*.dex`) or in `VERIFY_REPORT.md` logcat evidence | Build & Signing |
| **Incomplete input patched** | Pipeline patched/rebuilt a lone base split — `analysis.json` shows empty `splits` while provenance indicates a device split install; deliverable cannot install or run standalone | Intake & Analysis |
| **Incomplete deliverable** | Portable artifact missing a split or OBB present in the source inventory (`analysis.json` `splits`/`obbFiles` not packaged into the deliverable) | Build & Signing |
| **Tautological verification** | PASS verdict based on process liveness (`pidof`) without rendered-UI dump and window-focus proof | Device Verification |
| **Assertion editing** | S3 edition expectations modified to match a failing output instead of fixing the patch | Testing |
| **Missing post-code tests** | Fallback Ordering used but zero Scenario A/B evidence in `VERIFY_REPORT.md` | Testing |
| **State contamination** | Auth suite executed without `pm clear`, polluting results across suites | Testing |
| **Undeclared TDD skip** | Code-first ordering without `tdd_mode: "skipped"` + `skip_reason` in handoffs/logs | Process |
| **Iteration cap violation** | `fix-history.md` showing >2 fix iterations within one RCA round, or a 3rd attempt in the same bucket without a NEW RCA handoff (per the Escalation Guard in `05-apk-fix`; cumulative counts across separate RCA rounds are legitimate and NOT violations) | Process |

## [ADVISORY] Signals (documented, non-failing)

| Signal | Observable Pattern |
|---|---|
| Production ad unit IDs | paid2free artifact using non-test ad units with explicit spec confirmation |
| Package rename collateral | `<orig>.paid`/`.free` suffix limiting store upgrade paths (expected trade-off) |
| Heavy obfuscation residue | Patches matched by string constants with residual ambiguity flagged in `needsManualReview` |
| Split drift | Resource-only splits rebuilt when base-only patching would suffice |
| ABI coverage gap | Deliverable ABI set does not cover the target device's `ro.product.cpu.abilist` and no universal fallback exists (S5 coverage table documents it) |
| Auth registration pending | Firebase Console SHA-1 registration documented but not yet performed by the user |
| Signing scheme downgrade | Input APK verified with v3/v4 schemes (`analysis.json.signingScheme`) but deliverable signed only v1+v2 — key-rotation-dependent install paths may be affected; acceptable when documented in `PATCH_REPORT.md` |

## Verdict Rules
1. Any single `[BLOCKING]` signal → verdict `FAIL` with Review Defect Handoff (`re_entry_pipeline` 4a/4b/5/6).
2. `[ADVISORY]`-only → verdict `PASS` with findings documented for the user.
3. All findings must cite file/line or command-output evidence; unproven suspicions are not findings.
