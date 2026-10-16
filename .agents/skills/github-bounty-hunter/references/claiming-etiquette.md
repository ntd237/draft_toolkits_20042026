# Issue Claiming Protocol & Human-in-the-Loop (HITL) Gate

This guide governs communication etiquette, proposal drafting, human authorization boundaries, and pre-claim validations across all task categories (bug fixes, features, documentation) when claiming paid open-source issues.

## 1. Zero AI Spamming Policy (Mandatory)

Open-source maintainers face high volumes of low-effort, AI-generated spam. Violating maintainer trust leads to blocked accounts and rejected submissions.

### Prohibited Behaviors:
- **Never** post generic interest messages: `"I would like to work on this issue"`, `"Assign me please"`, or `"Can I take this?"`.
- **Never** claim multiple issues simultaneously across repositories. Work on one issue at a time (`runtime_policy.max_concurrent_tasks = 1`).
- **Never** trigger automated comments without prior local baseline verification and human approval.

---

## 2. Pre-Claim Technical & Eligibility Audit

Before drafting any claim comment, verify the following prerequisites:
1. **Verification Evidence**:
   - For bugs: Red proof captured (test failure log or repro script output).
   - For features: Baseline test suite passing and target module interfaces identified.
   - For documentation: Target files/sections and technical specifications audited.
2. **Funded Escrow Confirmation**: Bounty bot confirmed active with real escrow backing (not empty pledge).
3. **CLA / DCO Willingness**: Check repository `CONTRIBUTING.md` for CLA or DCO requirements. Ensure ability to sign off (`git commit -s`).
4. **Payout Route Verified**: Recipient account linked to Stripe Express via Algora or Polar console.

---

## 3. Mandatory Human-in-the-Loop (HITL) Approval Gate

Before any comment, reaction, or bot command is dispatched to GitHub, the agent **MUST** halt and present the drafted message to the human operator for review:

```text
[AGENT INTERRUPT: HITL Gate - Claim Confirmation Required]
Target Repository: owner/repo
Issue Number: #123 (Title: ...)
Task Category: Feature / Bug Fix / Documentation
Bounty Amount: $100 (via Algora / Polar - Funded)
Verification Status: Baseline verified locally
Autonomous Engine: goal-driven (Pipeline 1-8)
Proposed Comment Draft:
--------------------------------------------------
<Drafted proposal text>
--------------------------------------------------
Actions: [Approve & Send] / [Edit Draft] / [Abort]
```

Execution proceeds ONLY upon explicit human consent.

---

## 4. Tailored Claim Proposal Templates

### Template A: Bug Fix Proposal
```markdown
Hi @maintainer,

I have reproduced this issue locally on `[OS/Environment]` using `[Runtime Version]`.

- **Root Cause**: The issue originates in `[path/to/file.ext]` where `[functionName]` fails to `[specific mechanism failure]`.
- **Proposed Solution**: 
  1. Add a regression test in `[path/to/test.ext]` covering `[edge case scenario]`.
  2. Modify `[path/to/file.ext]` to properly handle `[expected logic]` with surgical changes.
  3. Ensure zero regressions across the existing test suite and adhere to all contribution guidelines (DCO/CLA).

May I proceed with this implementation?
```

### Template B: Feature / Enhancement / Refactoring Proposal
```markdown
Hi @maintainer,

I would like to work on implementing this capability. I have set up the project locally and verified the baseline test suite passes.

- **Proposed Architecture**:
  1. Implement `[feature name]` in `[path/to/module.ext]` adhering to existing design patterns.
  2. Add comprehensive unit and integration tests in `[path/to/test.ext]` covering all boundary conditions.
  3. Ensure backward compatibility and complete conformance with project linting and typing standards.

May I be assigned to this issue?
```

### Template C: Documentation Proposal
```markdown
Hi @maintainer,

I would like to work on updating this documentation.

- **Scope of Changes**:
  1. Update `[path/to/doc.md]` to include complete guides/specifications for `[feature/API]`.
  2. Ensure code examples and CLI snippets are verified against current releases.
  3. Format documentation in accordance with repository style guides.

May I proceed with this PR?
```

### Bot-Specific Claiming Directives:
- **Algora**: If the repository specifies bot commands, combine the command with your technical proposal:
  ```markdown
  /attempt
  
  I have verified this locally and mapped the solution in `[file/module]`. Proposing implementation via `[strategy]`.
  ```
- **Polar**: If the maintainer requires assigning via comment, submit the proposal above and wait for explicit maintainer assignment before beginning extensive implementation.
