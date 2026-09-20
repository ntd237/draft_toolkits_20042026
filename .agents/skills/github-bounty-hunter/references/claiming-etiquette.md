# Issue Claiming Protocol & Human-in-the-Loop (HITL) Gate

This guide governs communication etiquette, proposal drafting, and human authorization boundaries when claiming paid open-source issues.

## 1. Zero AI Spamming Policy (Mandatory)

Open-source maintainers face high volumes of low-effort, AI-generated spam. Violating maintainer trust leads to blocked accounts and rejected submissions.

### Prohibited Behaviors:
- **Never** post generic interest messages: `"I would like to work on this issue"`, `"Assign me please"`, or `"Can I take this?"`.
- **Never** claim multiple issues simultaneously across repositories. Work on one issue at a time.
- **Never** trigger automated comments without prior local reproduction and human approval.

---

## 2. Mandatory Human-in-the-Loop (HITL) Approval Gate

Before any comment, reaction, or bot command is dispatched to GitHub, the agent **MUST** halt and present the drafted message to the human operator for review:

```text
[AGENT INTERRUPT: HITL Gate - Claim Confirmation Required]
Target Repository: owner/repo
Issue Number: #123 (Title: ...)
Bounty Amount: $100 (via Algora)
Proposed Comment Draft:
--------------------------------------------------
<Drafted proposal text>
--------------------------------------------------
Actions: [Approve & Send] / [Edit Draft] / [Abort]
```

Execution proceeds ONLY upon explicit human consent.

---

## 3. High-Value Claim Proposal Template

A valid claim proposal must demonstrate technical understanding, local reproduction, and a concrete fix plan.

### Template:
```markdown
Hi @maintainer,

I have reproduced this issue locally on `[OS/Environment]` using `[Runtime Version]`.

- **Root Cause**: The issue originates in `[path/to/file.ext]` where `[functionName]` fails to `[specific mechanism failure]`.
- **Proposed Solution**: 
  1. Add a regression test in `[path/to/test.ext]` covering `[edge case scenario]`.
  2. Modify `[path/to/file.ext]` to properly handle `[expected logic]`.
  3. Ensure no regressions across the existing test suite.

May I proceed with this implementation?
```

### Bot-Specific Claiming Directives:
- **Algora**: If the repository specifies bot commands, combine the command with your technical proposal:
  ```markdown
  /attempt
  
  I have reproduced this issue locally and verified the root cause in `[file]`. Proposing fix via `[strategy]`.
  ```
- **Polar**: If the maintainer requires assigning via comment, submit the proposal above and wait for explicit assignment.
