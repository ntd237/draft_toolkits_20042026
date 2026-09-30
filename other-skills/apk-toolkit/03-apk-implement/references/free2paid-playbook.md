# free2paid Conversion Playbook

Convert a free-edition APK/XAPK into a paid edition: neutralize ads, bypass premium gates, neutralize self-signature checks. Requires `work/analyze/analysis.json`.

## Phase 1: Non-Destructive Ad Neutralization

### Manifest Preservation
- Do NOT delete ad `Activity`, `Service`, or `Receiver` entries, or the `AD_ID` permission. Preserving components prevents `ClassNotFoundException` or `ActivityNotFoundException` from internal references.

### Layout Placeholder Substitution
- For every ad view element (`com.google.android.gms.ads.AdView`, Facebook AdView, etc.) in `res/layout/*.xml`, replace the tag with a generic `<View>` keeping the exact `android:id` and constraints:
  ```xml
  <!-- PATCH free2paid: ad view replaced with same-id placeholder -->
  <View android:id="@+id/<original-ad-id>"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:visibility="gone" />
  ```

### Smali Bytecode Stubbing
- Match methods by string constants and descriptor signatures rather than class names when obfuscated.
- Stub `loadAd` and `show` methods to `return-void` (or return matching register type).
- Force `isLoaded` and `isAdLoaded` methods to return boolean `false` (`const/4 v0, 0x0; return v0`). Never return `true` — it triggers `show()` crashes on uninitialized ad instances.
- If mediation callbacks exist (`analysis.json.mediationSdks`), ensure listeners (`onAdLoaded`, `onAdDisplayed`) trigger or loading guards bypass waiting to prevent app startup deadlock.
- Wrap SDK `initialize` calls in try/catch blocks to protect environments lacking Google Play Services.
- Keep all ad drawables and string resources to prevent `Resources$NotFoundException`.

## Phase 2: Integrity Neutralization & Premium Feature Unlock

### Neutralize Self-Signature Checks
- For each entry in `analysis.json.integrityChecks` marked `type: self-signature`, locate the check method (e.g., `check()Z`) and patch it to return true (`const/4 v0, 0x1; return v0`).
- If a custom `X509TrustManager` pins the app's own certificate, patch it to trust the new certificate.
- Note unbypassable server-side attestation (Play Integrity, SafetyNet) in limitations — never attempt a bypass.

### Unlock Premium Flags & Bypass Gates
- Update `BuildConfig` smali: set `IS_PREMIUM`, `FLAVOR`, `IS_PAID` fields to `true` / `"paid"`.
- Locate branching opcodes gating premium features (`if-eqz` / `if-nez`); invert or NOP branches so premium paths execute unconditionally.
- Unhide premium UI elements (menus, actions, premium panels).
- Bypass entitlement checks around `BillingClient` without deleting billing classes; ensure downstream consumers handle null purchase tokens safely.

### 4 Client-Side Paid-Unlock Techniques (Real-World Modded-Build Methods)
When the app checks its paid state client-side, a data-point-only patch (waiting for a purchase/restore flow) leaves the app rendering as FREE at launch if it reads the subscription state from the backend at login. To make the app open and render as PAID immediately after login, apply one of the following 4 techniques:

#### Technique 1: Patch the Decision Point Directly in Hermes Bytecode (most common on React Native)
- **Mechanism**: disassemble `index.android.bundle` with a tool such as `hermes-dec` (`hbc-decompiler` / `hbc-disassembler`) or `hbctool`. Locate the function handling the backend user response (where the subscription/entitlement state is read) and force it to always return the subscribed state ("Gold = true" / "is_paid = true" / any truthy value).
- **Surgical procedure (no full-bundle reassembly needed)**:
  1. Identify the instruction reading the subscription property (e.g. a `GetById`/`TryGetById` carrying the string_id of the subscription field).
  2. Look up the string table for the string_id of an identifier that ALWAYS exists and is truthy in the user object (e.g. `username`, `id`, `email`).
  3. Overwrite the instruction's operand bytes in place with the new string_id (patch exactly the UInt16-LE operand at the computed file offset).
  4. Leave the write-path (`PutById`) untouched so purchase-time logic keeps its original semantics.
- **Result**: right after login, even though the backend reports "free", the app reads the repointed truthy property and activates the paid edition at launch. No purchase, no restore required.

#### Technique 2: Hook the Native Bridge Module at Smali Level (Native Bridge Interception)
- **Mechanism**: instead of touching the JS bundle, patch the native module that feeds data to JS (the app's API client module, network interceptor, or native purchases bridge) to forge the response BEFORE it crosses the bridge into JS.
- **Procedure**:
  1. Locate the smali class of the native module receiving the user/profile response from the server (or the corresponding bridge module).
  2. Intercept the callback or the Java/Kotlin→JS mapper (`WritableMap` / `ReadableMap`).
  3. Add or overwrite entitlement/subscription fields in the payload before the promise resolves to JS.
- **Result**: equivalent effect to Technique 1 — JS receives modified data from the native layer; slightly harder to detect when scanning JS sources.

#### Technique 3: Forge the Local RevenueCat / In-App Purchases Cache
- **Mechanism**: purchase SDKs (e.g. RevenueCat) cache subscription info (`CustomerInfo`) on disk and push it to listeners as soon as the app starts.
- **Procedure**:
  1. Ship or pre-seed a forged cache containing an active entitlement with a far-future expiration date.
  2. Intercept the SDK's native initialization point to load this cache into disk/memory before the app finishes its cold start.
  3. The SDK then emits an entitled `CustomerInfo` at startup instead of waiting for a network response or a purchase flow.
- **Result**: subscription listeners observe an active state immediately at app launch.

#### Technique 4: Backend Proxy / MITM (lab-only — requires explicit approval)
- **Mechanism**: repack the app, strip certificate pinning (remove Network Security Config or patch the trust manager in smali), and route traffic through an intercepting proxy that rewrites backend API responses for the client.
- **Scope guard (two-tier doctrine, README Hard Rule 3)**: this technique never bypasses platform attestation (Play Integrity / SafetyNet / App Check / native attestation — `bypassable: false` entries stay untouchable). It is permitted ONLY when ALL of the following hold:
  1. The approved spec explicitly opts in to server-response rewriting and states the testing/ownership context.
  2. The proxy infrastructure is external to this toolkit and is NOT part of the deliverable.
  3. Usage is disclosed verbatim in `PATCH_REPORT.md` (Known Limitations section).
  4. The portable deliverable must still install and run correctly WITHOUT the proxy — proxy-dependent functionality is a disclosed limitation, never bundled.
- **Scope**: rarely used in offline conversions because it requires a runtime proxy or network infrastructure, but it is the only option when the feature logic is fully validated server-side and Techniques 1–3 cannot reach the decision point.

## Phase 3: Auth Preservation for Re-Signed Builds (proactive — apply BEFORE first build)
When `analysis.json.authDependencies` contains Firebase and the spec chooses a fresh keystore, the re-signed build will be rejected by Firebase endpoints whose API key is Android-restricted (`400 API_KEY_ANDROID_APP_BLOCKED`) and by client-side App Check attestation — the app then misleadingly reports "wrong password" with correct credentials. Prevent the bug instead of fixing it post-hoc:

1. Extract the ORIGINAL cert SHA-1 from the pristine input: `apksigner verify --print-certs work/convert-<direction>/original.apk`.
2. Apply Recipe R1 from `05-apk-fix/references/apk-fix-playbook.md` during Phase 2 (patch the obfuscated cert provider to return the original SHA-1 bytes) so every Firebase REST call carries `X-Android-Cert: <original SHA-1>`.
3. If the app uses react-native-firebase with App Check enabled, also apply Recipe R2 (dummy-token resolve in `RNFBAppCheckModule` d/e) — valid because Identity Toolkit does not enforce App Check server-side.
4. Scope guard: this covers email/password (and similar client-asserted-header) auth only. Google Sign-In still requires the owner to register the new SHA-1 in Firebase Console (`ApiException 10` — manual), and endpoints enforcing Play Integrity / App Check server-side remain blocked. Verify with the curl discriminator (see `04-apk-bugfinder`) when unsure which case applies.
5. UI-automation guard for the login smoke path: at the password entry step the device may go black (OEM secure-input mechanism, possibly with a hidden permission dialog behind it) — hand credential entry to the user, do not automate or retry-tap (see S4 in `06-apk-test/references/apk-smoke-suites.md`).

## Phase 4: Multi-Split & Native Safeguards
- Preserve all native libraries from `lib/<abi>/*.so`.
- For XAPK: apply smali and layout patches to the `base` split while keeping resource-only splits intact.
- **Post-decode resource integrity sweep (run BEFORE the first build)**: scan `res/values/drawables.xml` and `res/values/styles.xml` for `@null`-valued items whose original values were resource references — these are cross-split aliases apktool could not resolve from the base alone (targets live in another split's table, e.g. density splits). Repair proactively per Recipe R3 in `05-apk-fix/references/apk-fix-playbook.md`; every unrepaired alias is a latent `Resources$NotFoundException` crash on the feature that inflates it (media player controls are the classic victim).
- **Server-owned state audit**: enumerate all premium settings/toggles whose state is persisted via backend profile-update calls (`changeProfileInfo`-style). For each, the patched UI must derive from a client-side predicate (Recipe R4), never from the server-returned user object — otherwise the server silently reverts the state minutes later. Also never let the patched UI block on the server's verdict; absorb rejections silently.

## Prohibitions
- Do not delete ad components from Manifest or ad view IDs from layouts.
- Do not stub `isLoaded` / `isAdLoaded` to return `true`.
- Do not strip or delete `BillingClient` structures.
- Do not rename obfuscated classes or rely on unstable class identifiers.
- Do not hardcode or log keystore credentials.
