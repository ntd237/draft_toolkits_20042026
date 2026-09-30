# Game Security & Integrity Audit Checklist

Used by `07-mobile-game-review` whenever the reviewed change touches security-sensitive game code (IAP/purchases, save data, player identity, currency/economy, analytics identity). The mobile game client is an **untrusted environment**: assume players can inspect memory, tamper with local files, and forge client requests. Every check must yield a concrete verdict (pass / finding with file:line evidence). Confirmed integrity-critical flaws (client-trusted currency, unsigned saves for competitive state, secrets in build) are BLOCKING; hardening gaps without a live exploit path are ADVISORY.

## 1. In-App Purchases & Store Integrity
- **Receipt validation is server-side (or verified through the platform SDK) before granting entitlements** — client-side validation alone is never trusted; flag client-trusted IAP as BLOCKING.
- Sandbox/testing purchases use the store's sandbox accounts and test product IDs — no production product IDs hardcoded in dev builds.
- Consumables/entitlements reconciliation: purchase grants are idempotent and persisted (survive crash mid-grant).
- Ads SDK callbacks (rewarded video) are validated via the SDK's server-side verification where available; client-only "reward granted" callbacks on security-sensitive rewards are flagged.

## 2. Save Data & Local State Protection
- Save files for progression-sensitive state (currency, level, PvP rank) carry integrity protection (checksum/HMAC at minimum; platform-protected storage where available) — tamper with obvious plaintext JSON for currency is flagged at minimum ADVISORY, BLOCKING for competitive/economy-critical values.
- Save schema changes follow the migration plan (`02-mobile-game-plan` Phase 2): versioned, backward-compatible, rollback-safe — a migration that can corrupt or wipe player saves is BLOCKING.
- No sensitive tokens (session, purchase receipts, user identifiers) written to unprotected plaintext storage when the platform offers a secure alternative.

## 3. Client Trust Boundary & Anti-Cheat Basics
- Client-authoritative state is limited to cosmetic/single-player semantics; anything scoring into leaderboards, PvP, or economy must be (or be planned as) server-authoritative — a client-authoritative leaderboard submit is BLOCKING if the leaderboard is competitive.
- Speedhack/memory-edit sensitive paths (win/loss detection, score submission) do not rely solely on client-side checks; note required server/obfuscation controls in the report.
- Debug cheats/dev commands are compiled out or gated behind build flags for release variants (`#if DEVELOPMENT_BUILD`, `#if UNITY_EDITOR` or engine equivalents) — a live debug menu in release is BLOCKING.

## 4. Secrets & Build Hygiene
- No API keys, signing passwords, or service credentials hardcoded in scripts, scene files, or version control; platform SDK keys that must ship client-side are the only exception and must be the least-privilege, restricted-key kind.
- Signing material (keystore, provisioning profiles) referenced via environment/CI secrets, not committed.
- Logging never emits tokens, receipts, or full user identifiers; logs are disabled or minimized in release builds.

## 5. Analytics & Identity Privacy
- Player identifiers sent to analytics/ads SDKs follow the platform consent rules already planned (ATT on iOS, Android ad ID consent) — sending identifiers before consent is BLOCKING.
- Personal data collection is limited to what the analytics plan documents; no unencrypted transmission of personal data.
