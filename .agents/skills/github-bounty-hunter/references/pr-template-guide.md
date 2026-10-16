# Pull Request Submission & CI Review Guide

This guide specifies the structure for Pull Requests (PRs), git fork and remote orchestration, mandatory issue-linking keywords, harness log exclusion, DCO/CLA sign-off, CI monitoring procedures, and maintainer feedback handling.

## 1. Fork & Remote Management Workflow

When contributing to third-party open-source projects, contributors do not possess direct write access to upstream repositories. The standard fork workflow must be followed:

1. **Fork Upstream Repository**:
   ```bash
   gh repo fork <owner>/<repo> --clone=false
   ```
2. **Configure Git Remotes**:
   Inside the local clone directory:
   ```bash
   # origin points to the contributor fork
   git remote set-url origin https://github.com/<contributor>/<repo>.git
   # upstream points to the authoritative source repository
   git remote add upstream https://github.com/<owner>/<repo>.git
   git fetch upstream
   ```
3. **Synchronize Base Branch**:
   Ensure local branch is cut from the latest upstream default branch:
   ```bash
   git checkout main || git checkout master
   git pull upstream main || git pull upstream master
   git checkout -b fix/bounty-issue-<id>-<slug>
   ```
4. **Push Branch to Contributor Fork**:
   ```bash
   git push -u origin fix/bounty-issue-<id>-<slug>
   ```
5. **Open PR Targeting Upstream**:
   ```bash
   gh pr create --repo <owner>/<repo> --base main --head <contributor>:fix/bounty-issue-<id>-<slug> --title "fix: ..." --body-file pr_body.md
   ```

---

## 2. Commit Discipline & DCO / CLA Compliance

Many major open-source foundations (Linux Foundation, CNCF, Apache, etc.) enforce Developer Certificate of Origin (DCO) or Contributor License Agreements (CLA).

### Developer Certificate of Origin (DCO) Sign-Off
- When `git_policy.require_dco_signoff` is enabled in `config.json`, every commit **MUST** include a sign-off header.
- Execute commit using the `-s` flag:
  ```bash
  git commit -s -m "fix: resolve #123 handle edge case in parser"
  ```
- This automatically appends:
  ```text
  Signed-off-by: Contributor Name <contributor.email@example.com>
  ```

### Contributor License Agreement (CLA) Check
- Check `CONTRIBUTING.md` for CLA requirements.
- Upon opening the PR, monitor for CLA bot comments (`cla-assistant`, `easycla`). Complete electronic CLA signatures promptly if requested.

---

## 3. Harness Log & Transient Artifact Exclusion Protocol

When operating under autonomous engine skills (such as `goal-driven` or `00-orchestrator`), execution logs are saved to `docs/harness-logs/` for local observability. These files belong to the agent harness and must **NEVER** be committed or pushed to contributor forks or upstream repositories.

### Exclusion Rules:
1. **Local Git Exclude**:
   Add `docs/harness-logs/` to `.git/info/exclude` in the cloned target repository so it is ignored locally without altering the project's tracked `.gitignore`:
   ```bash
   echo "docs/harness-logs/" >> .git/info/exclude
   ```
2. **Strict Selective Staging**:
   - Only stage modified production and test files explicitly:
     ```bash
     git add src/affected_file.ts tests/affected_file.test.ts
     ```
   - **PROHIBITED**: Never run `git add .` or `git add -A`.
3. **Pre-Push Validation Command**:
   Before pushing, verify that no files from `docs/harness-logs/` exist in git index or commit history:
   ```bash
   git diff --name-only upstream/main...HEAD | grep -E "docs/harness-logs|harness-logs"
   ```
   If this command returns any output, halt execution and remove the files from the git index:
   ```bash
   git rm -r --cached docs/harness-logs/
   git commit --amend --no-edit
   ```

---

## 4. Mandatory Issue-Linking Keywords

Bounty platforms (Algora, Polar) and GitHub rely on automated webhook parsers to trigger payouts upon merge. PR bodies **must** contain an explicit resolution keyword:

- `Fixes #<issue_id>`
- `Closes #<issue_id>`
- `Resolves #<issue_id>`

*If working from a fork targeting upstream, specify the full upstream repository target if needed: `Fixes <owner>/<repo>#<issue_id>`.*

---

## 5. Standard PR Description Template

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
- [x] DCO Signed-off: `git commit -s` verified
- [x] Harness log exclusion verified: zero telemetry committed

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

## 6. Pre-Submission Quality Gate

Before submitting any PR:
1. **Clean Diff Check**: Run `git diff upstream/main...HEAD` (or `upstream/master`) and confirm:
   - No commented-out code or debug prints (`console.log`, `print`, `dbg!`).
   - No unintended formatting shifts in untouched functions.
   - No accidental commits of secrets, `.env` files, or binary artifacts.
   - Zero files from `docs/harness-logs/` in diff.
2. **DCO Verification**: Check `git log -1 --pretty=fuller` to ensure `Signed-off-by:` line exists.
3. **Mandatory HITL Gate**: Present the full PR title, description, and diff summary to the human operator for final authorization before pushing.

---

## 7. CI Monitoring & Review Iteration Protocol

1. **GitHub Actions Monitoring**:
   - Immediately after opening the PR, monitor the CI check suite (`gh pr checks` or web UI).
   - If CI fails: Inspect logs immediately, categorize the failure (Lint, Test, TypeCheck, Build), reproduce locally, and push an atomic fix commit using `05-fix` with DCO sign-off.
2. **Responding to Maintainer Feedback**:
   - Maintain a constructive, polite, and responsive tone.
   - Address every review comment directly. If a requested change is completed, reply with the commit hash resolving it.
   - Never argue subjectively against established project style guides; adapt strictly to repository conventions.
