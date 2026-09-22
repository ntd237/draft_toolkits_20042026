# TDD Cheating Audit Signals

Used in Phase 3 of `07-review` to detect falsified Red-Green-Refactor cycles.

## Test-Level Signals

- Meaningless assertions: `assert True`, `expect(true).toBe(true)`, comparing a value against itself.
- Mocks/stubs masking the logic under test (e.g., mocking the entire function under test rather than external dependencies).
- Tests asserting only that "no exception is thrown" without validating actual values or behavior.
- Tests commented out or skipped (`@skip`, `xit`, dangling `.only`) without documented justifications.
- Test cases failing to cover edge cases specified in acceptance criteria (e.g., testing only happy paths, ignoring required empty/null/boundary inputs).

## Change-History Signals (When commit history or run logs exist)

- Test contents modified (assertions altered, expected inputs changed) in the same commit or immediately after failing, instead of correcting implementation code.
- No evidence that tests were Red prior to the appearance of implementation code (for units claiming standard TDD, not under exceptions).
- For units under TDD exceptions: no verification tests added after implementation — the verification phase was omitted entirely.

## When Cheating Signals Are Detected

Do not fix autonomously. Explicitly flag: which unit, what signal was observed, and recommend returning to `06-test` to author compliant tests, followed by `03-implement`/`05-fix` to achieve Green via genuine implementation fixes.
