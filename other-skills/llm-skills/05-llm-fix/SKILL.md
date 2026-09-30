---
name: 05-llm-fix
description: "Permanently resolves defects, hallucinations, parser validation crashes, prompt injection vulnerabilities, and review findings in LLM applications based on root cause analysis from 04-llm-bugfinder or 07-llm-review defect reports. Sole authorized Green + Refactor skill for all bug-fix pipelines (4a, 4b, 5, 6) and Post-Review Bug Loops. Strictly prohibits modifying tests to evade logic fixes and prohibits patching surface symptoms."
---

# 05-llm-fix — LLM Defect Remediation (Green + Refactor)

## Trigger
Invoked by `00-llm-orchestrator` in defect resolution pipelines (Pipelines 4a, 4b, 5, 6) and during every iteration of the Post-Review Bug Loop. **Sole authorized skill for writing defect-fixing code — `03-llm-implement` is strictly forbidden from executing bug fixes.**

## Workflow

### Phase 1: Root Cause Verification
**Objective**: Validate root cause clarity before modifying any production prompts, schemas, or application code.

1. **Verify Handoff Details**: Inspect the incoming YAML handoff from `04-llm-bugfinder`, `00-llm-orchestrator`, or `07-llm-review`. Ensure the report contains:
   - Exact file path, line number, or prompt template identifier.
   - Root cause description (not merely surface symptoms).
   - Confirmation of probe cleanup (`cleanup_verified: true` if coming from `04-llm-bugfinder`).
2. **Reject Insufficient Inputs**: If the input contains only vague symptoms (e.g., "model output is sometimes inaccurate") without specific diagnostic evidence, decline to proceed and request routing to `04-llm-bugfinder`. Do not guess.

### Phase 2: Green — Surgical Root Cause Remediation
**Objective**: Fix the root cause directly to transition targeted failing tests from Red to Green while adhering to LLM engineering best practices.

1. **Surgical Fix**: Apply changes directly to the offending prompt template, parser logic, chunking rule, or gateway configuration.
2. **LLM Remediation Compliance**:
   - *Hallucination Fixes*: Add explicit grounding constraints ("Answer solely using the provided context. If unknown, state 'Information not found'"), strict refusal boundaries, or few-shot grounding exemplars.
   - *Structured Output / Parser Fixes*: Implement regex markdown fence stripping (````json````), Pydantic field validators with sensible defaults, or JSON repair utilities.
   - *Vector Retrieval Fixes*: Re-tune chunk size/overlap parameters, fix metadata filter operators, or integrate a reranking step.
   - *Gateway & Resilience Fixes*: Configure exponential backoff with jitter on HTTP 429, implement fallback provider models, and enforce request timeouts.
   - *Security & Prompt Injection Fixes*: Enclose user input inside strict XML tags (`<user_input>...</user_input>`), sanitize delimiter characters, and mask sensitive credentials.
3. **No Surface Masking**: Do not swallow exceptions with empty `except Exception:` blocks or return fabricated fake responses. Fix the underlying parsing or invocation logic.
4. **Execute Tests**: Run the targeted regression test suite to verify Green status.

### Phase 3: Multi-Site Consistency & Regression Verification
**Objective**: Propagate fixes across all related locations and verify zero regressions.

1. **Impact Scope Propagation**: If the root cause pattern exists across multiple prompt templates, agent tools, or output parsers (identified in blast radius), apply identical, consistent fixes to all affected modules.
2. **Full Suite Regression Check**: Execute the entire related test suite to guarantee that fixing the defect did not break adjacent prompt chains, parsers, or vector searches.
3. **Handoff**: Transition to `07-llm-review` (or to `06-llm-test` under Scenario A if TDD was skipped).
4. When the fix touches concerns covered by `../03-llm-implement/references/llm-implementation-standards.md` (tracing, prompt versioning, streaming handling, caching boundaries, privacy screening), the corrected code must comply with those standards as well.

## Output Format
Provide code diffs and a structured remediation summary:
- **Root Cause Addressed**: File path and line number/prompt corrected.
- **Remediation Details**: Explanation of the fix and prevention of hallucinations/schema crashes.
- **Multi-Site Updates**: List of additional files or prompt templates updated for consistency.
- **Verification Evidence**: Test runner output showing targeted and regression tests passing Green.

## Don'ts
- **Absolute Prohibition**: Do not alter, weaken, or delete test assertions to make tests pass — all fixes must be achieved by correcting production code or prompt templates.
- Do not apply surface patches (e.g., catching `ValidationError` and returning an empty dummy object) that mask deeper LLM instruction flaws.
- Do not guess or attempt fixes without a verified root cause from `04-llm-bugfinder` or explicit diagnostic evidence.
- Do not remove security guardrails or prompt injection protections to make test strings pass.
- Do not leave raw unhandled API errors or infinite retry loops without backoff limits.

## Quality Checklist
- [ ] Is the fix targeted directly at the verified root cause rather than surface symptoms?
- [ ] Were zero test assertions modified to circumvent fixing production code?
- [ ] Does the fix prevent hallucinations, schema errors, or prompt injection vulnerabilities?
- [ ] Were consistent fixes applied to all related locations identified in the blast radius?
- [ ] Did the targeted test transition to Green, and did the regression suite pass completely?
- [ ] Was `05-llm-fix` used exclusively for this defect work (never `03-llm-implement`)?
