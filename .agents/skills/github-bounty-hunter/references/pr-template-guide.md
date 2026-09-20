# Pull Request Submission & CI Review Guide

This guide specifies the structure for Pull Requests (PRs), mandatory issue-linking keywords, CI monitoring procedures, and maintainer feedback handling.

## 1. Pull Request Packaging Standards

### Mandatory Issue-Linking Keywords
Bounty platforms (Algora, Polar) and GitHub rely on automated webhook parsers to trigger payouts upon merge. PR bodies **must** contain an explicit resolution keyword:

- `Fixes #<issue_id>`
- `Closes #<issue_id>`
- `Resolves #<issue_id>`

*Never omit or misspell this keyword. If fixing in a fork, link to the upstream issue: `Fixes upstream-owner/upstream-repo#<issue_id>`.*

---

## 2. Standard PR Description Template

````markdown
## Description
<!-- Provide a clear summary of the changes made -->
This PR resolves #[issue_id] by [brief explanation of fix/feature].

Fixes #[issue_id]

## Root Cause
[Explain what caused the issue, referencing exact files and functions]

## Changes Made
- [List specific changes made]
- Added regression test in `[test_file]` to prevent recurrence.

## Verification & Test Results
- [x] Baseline test suite passed
- [x] New regression test passed: `[test name]`
- [x] Linter and code formatting verified: `[command run]`

<details>
<summary>Test Output Logs</summary>

```text
[Paste terminal test execution output here]
```
</details>

## Media (Required for UI / Frontend changes)
<!-- Attach screenshot or GIF showing Before vs After behavior -->
- **Before**: [Image / Description]
- **After**: [Image / Description]
````

---

## 3. Pre-Submission Quality Gate

Before submitting any PR:
1. **Clean Diff Check**: Run `git diff main...HEAD` and confirm:
   - No commented-out code or debug prints (`console.log`, `print`, `dbg!`).
   - No unintended formatting shifts in untouched functions.
   - No accidental commits of secrets, `.env` files, or binary artifacts.
2. **Mandatory HITL Gate**: Present the full PR title, description, and diff summary to the human operator for final authorization before pushing.

---

## 4. CI Monitoring & Review Iteration Protocol

1. **GitHub Actions Monitoring**:
   - Immediately after opening the PR, monitor the CI check suite (`gh pr checks` or web UI).
   - If CI fails: Inspect logs immediately, categorize the failure (Lint, Test, TypeCheck, Build), reproduce locally, and push an atomic fix commit (`fix: resolve CI lint error`).
2. **Responding to Maintainer Feedback**:
   - Maintain a constructive, polite, and responsive tone.
   - Address every review comment directly. If a requested change is completed, reply with the commit hash resolving it.
   - Never argue subjectively against established project style guides; adapt strictly to repository conventions.
