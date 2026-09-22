# TDD Exception Handling & Complexity Decision Table

## When Inverting Red-Green-Refactor to Implement/Fix → Test Is Permitted

TDD (test-first) is the **preferred default**, not a rigid dogma. Inverting the sequence for a specific atomic behavior unit is permitted when at least one condition is met:

1. **Technical spike**: Exploratory code is needed to understand how an API, library, or behavior works before knowing what assertions to write.
2. **Exploratory UI/Aesthetics**: Tuning layout, animation, or styling where "correctness" is judged visually with no clear assertion to write beforehand.
3. **External environment dependency**: Integrating with a third-party service lacking a stable sandbox or mock for pre-testing.
4. **Acceptance criteria insufficiently specific** even after brainstorming — though returning to brainstorming for clarity should be prioritized; invert TDD only when further clarification yields no benefit.

When inverting the sequence: `03-implement`/`05-fix` runs first, after which `06-test` **must** run to author verification tests for the newly implemented behavior — skipping the test phase entirely is strictly prohibited. Tests written after implementation must still rigorously cover the target behavior rather than serving as mere token tests.

## Complexity & Risk Decision Table (Used in Phase 3)

| Signal | Simple | Complex / High Risk |
|---|---|---|
| Layers touched | 1 layer | ≥2 layers (frontend+backend, backend+DB, ...) |
| Modules/files count | 1-2 files, localized scope | Multiple modules, requires parallel coordination |
| DB Schema | Unchanged | Add/alter/drop column or table, migrations |
| API Contract | Unchanged | Add/modify endpoint impacting other consumers |
| Business Flow | Does not touch critical flows | Touches auth, payment, sensitive data |
| Rollback Feasibility | Easy to revert | Hard to revert, affects production data |

Falling into the "Complex / High Risk" column for ≥1 criterion is sufficient to mandate `02-plan`.

## Handling Ambiguous Signals Between "Unknown Bug" and "Known Bug"

If the user describes symptoms accompanied by a speculative cause without concrete evidence (traceback, logs, query results) — treat it as an **unknown cause**, mandating routing through `04-bugfinder`. Only classify as "known" when concrete evidence directly pinpoints the exact failure location.
