# Mobile Game Implementation Standards

Applied by `03-mobile-game-implement` (and `05-mobile-game-fix` where a fix touches the same concerns), alongside the zero-GC rules already in SKILL.md. These are minimum standards — apply what the current unit's tests and acceptance criteria demand; flag conflicts with existing project conventions instead of silently overriding either side.

## Engine Parity
- Examples in this toolkit are Unity-centric; when the project is Godot (C#/GDScript) or a custom C++ engine, apply the same discipline with the engine's equivalents (e.g., Unity `Update()` → Godot `_process()`; `ObjectPool<T>` → custom/engine pool; `PlayerPrefs` → `ConfigFile`/`FileAccess`; Unity Test Framework → GUT). State the mapping decision in the handoff summary.

## Monetization (IAP / Ads)
- Purchases go through the platform SDK flow with the store's sandbox/test accounts in dev builds — never production product IDs in development.
- Entitlements are granted only after receipt/purchase validation per the plan's flow (server-side or platform SDK verification); grant logic is idempotent and persisted so a crash mid-grant cannot lose or duplicate a purchase.
- Rewarded-ad callbacks are validated via the SDK's server-side verification where available; client-only reward callbacks are limited to non-economy rewards.
- Prices, product IDs, and ad unit IDs come from configuration/remote config — not hardcoded per feature.

## Live Ops (Remote Config / Feature Flags)
- Tunable values exposed in the feature (drop rates, timers, prices, difficulty) read from the project's remote config layer with safe local defaults — the game must remain playable offline with defaults.
- Feature flags gate incomplete or risky content so it can be disabled post-release without a store update.
- Remote config fetch failures fall back to cached/last-known-good values and never block the game loop (no synchronous network on startup paths).

## Analytics & Crash Reporting
- New subsystems register with the project's crash-reporting SDK (breadcrumbs/context for the subsystem) so production crashes are attributable.
- Analytics events follow the project's event naming convention and the acceptance criteria's tracking plan; identifiers are sent only after platform consent (ATT on iOS, ad ID consent on Android).
- Event emission is fire-and-forget/batched — never blocking gameplay or per-frame allocation (zero-GC rules still apply).

## Audio
- New audio sources route through the project's mixer/bus structure (SFX/BGM/UI categories), respecting persisted volume settings.
- BGM uses streaming load; short SFX use compressed-in-memory; simultaneous one-shots are bounded via voice limiting/priority.
- Audio respects lifecycle mute behavior (`OnApplicationPause`).

## Localization
- Player-facing strings go through the project's localization system (keys/tables), never inline literals; plurals and interpolation use the system's mechanisms.
- Layouts tolerate text expansion and RTL where the project targets those languages.

## Store Build & Release (App-Level)
- Build variants (dev/staging/release) differ only in configuration: debug cheats gated behind build flags (`#if DEVELOPMENT_BUILD`/`#if UNITY_EDITOR` or equivalents) and compiled out of release.
- Signing material (keystore, provisioning profiles) referenced from environment/CI secrets, never committed; version codes/bundle identifiers follow the project's release convention.
- Store listing assets (icons, screenshots, metadata files) are generated/updated per the store's spec; no player-facing store text bypasses localization.
- A release build must state its verification path in the handoff summary: which build variant, which device(s), which smoke checks (launch, core loop, IAP sandbox, save round-trip).

## Client-Side Networking (when the game uses online features)
- The client treats all server responses as untrusted: validate payloads before applying to game state; never apply server data without schema checks.
- Reconnection: transient network loss pauses/marks state rather than corrupting it; requests idempotent where retried; UI reflects offline/reconnecting state instead of hanging.
- Server-authoritative boundaries follow the plan (and `../07-mobile-game-review/references/game-security-checklist.md`): client never self-asserts competitive outcomes.
