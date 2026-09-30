# Non-Functional Review Checklists (Audio / Localization / Game Accessibility)

Used by `07-mobile-game-review` for the dimensions flagged in acceptance criteria (`01-mobile-game-brainstorm` Phase 3) or the plan (`02-mobile-game-plan` Phase 2). Severity rule from SKILL.md applies: violating a *stated* acceptance criterion is BLOCKING; gaps in dimensions never agreed on are ADVISORY.

## Audio
Check only audio touched by the change:
- **Lifecycle**: audio mutes/pauses correctly on `OnApplicationPause(true)` and restores on resume; no BGM continuation during phone calls or backgrounding (mirrors the lifecycle audit in SKILL.md Phase 3).
- **Mixing & buses**: SFX/BGM/UI audio routed through the project's mixer/bus structure; a new sound source respects existing volume categories (no hardcoded volume bypassing buses).
- **Voice count & priority**: simultaneous one-shot sounds are bounded (voice limiting/priority assigned); no unbounded audio source spawning on events like mass enemy deaths.
- **Resource weight**: BGM uses streaming/compressed load path (Vorbis/MP3 streaming for music); short SFX use compressed-in-memory; no raw WAV in bundles flagged by `04-mobile-game-bugfinder` memory profiles.
- **Persisted settings**: volume settings persist via the save system and apply on startup.

## Localization
Check only when the project ships multiple languages or localization was a stated criterion:
- **No hardcoded player-facing strings**: new UI/gameplay text goes through the project's localization system (table/key lookup), not inline literals — one inline string is ADVISORY; a full new feature of inline strings is ADVISORY with a migration note.
- **Pluralization & interpolation**: plural rules and variable interpolation use the localization system's mechanisms, not string concatenation.
- **RTL & length tolerance**: layouts tolerate text expansion (~+30% for German) and RTL scripts when the project targets those languages; test keys, not only default language.
- **Metadata**: new store-facing strings follow the store assets process (`02`/deployment standards), not hardcoded in build settings.

## Game Accessibility
- **Text legibility**: player-facing text respects the project's font-size scale; no fixed tiny sizes for critical instructions; subtitles (if any) can be resized or are within legible bounds.
- **Color independence**: information is not conveyed by color alone (damage states, rarity, match-3 hint colors) — pair with icons/shapes/text; color-blind-critical feedback is flagged at minimum ADVISORY when gameplay-critical.
- **Input accessibility**: all interactions achievable with the project's supported control schemes (touch-only must not require multi-finger precision unless stated; alternatives for gesture-only mechanics noted).
- **Motion comfort**: new camera effects/shake respect any existing photosensitivity/motion-reduction setting the project exposes.
- **Audio cues**: gameplay-critical audio cues have visual counterparts (or vice versa).
