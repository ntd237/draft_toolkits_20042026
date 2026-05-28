---
name: debug-en
description: "Activate session debug logging and guide the user through systematic investigation of issues in the current Claude Code session."
---

# Debug — Session Issue Investigation

## What This Skill Does

This skill enables debug logging for the current Claude Code session and walks through a structured process to identify and explain issues the user is experiencing.

Debug logging was OFF before this invocation. Nothing prior to `/debug` was captured.

---

## Step 1 — Logging Is Now Active

Inform the user:

- Debug logging is now enabled for this session.
- The session debug log is at:
  ```
  C:\Users\<username>\.claude\debug\<session-id>.txt
  ```
- No log file exists yet — it will be created once events occur.

If the user cannot reproduce the issue in this session, advise them to restart with:

```bash
claude --debug
```

This captures logs from startup.

---

## Step 2 — Ask the User to Reproduce the Issue

Ask the user to reproduce the problem now so events are written to the active log.

Wait for the user to confirm they have reproduced it before proceeding.

---

## Step 3 — Read the Debug Log

Read the log file at the path from Step 1.

Search for:

- `[ERROR]` lines — hard failures
- `[WARN]` lines — non-fatal warnings
- Stack traces — call chains leading to failures
- Repeated patterns — correlated sequences suggesting root cause

---

## Step 4 — Analyze and Explain

From the log content:

1. Identify the specific error or warning matching the reported issue.
2. Understand the context: what happened before the failure, what state the session was in.
3. Explain findings in plain language — what was found, what it means, what triggered it.

---

## Step 5 — Suggest Fixes or Next Steps

Provide:

- Concrete fix suggestions (config changes, command corrections, environment fixes).
- Next steps if root cause is still unclear.

Reference settings files if relevant:

- User: `C:\Users\<username>\.claude\settings.json`
- Project: `<project-root>\.claude\settings.json`
- Local: `<project-root>\.claude\settings.local.json`

---

## Optional

If deeper context about a Claude Code feature is needed, launch the `claude-code-guide` subagent to research the relevant feature before explaining findings.

---

## Rules

- This skill is read-only. Do not modify any project files.
- Only events after `/debug` invocation are available in the log.
- If the log is empty after reproduction, inform the user and suggest `claude --debug` restart.
- Explain findings in plain language. Avoid raw log dumps without interpretation.
