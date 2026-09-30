---
name: 07-llm-review
description: "Performs comprehensive architectural, security, and performance code reviews for LLM & Generative AI applications. Audits prompt injection defenses, content moderation, secret leaks, runaway token budget traps, exponential backoff/fallback handling, observability (tracing, cost attribution), prompt management (versioning, rollback), RAG/schema integrity, and verifies genuine TDD compliance without cheated tests. Issues strict PASS/FAIL verdicts, triggering the Post-Review Bug Loop on FAIL. Read-only — reports findings without modifying code."
---

# 07-llm-review — LLM Code & Architecture Review

## Trigger
Mandatory final step across all 6 pipeline scenarios (#1 through #6), invoked by `00-llm-orchestrator` once `03-llm-implement` or `05-llm-fix` achieves Green and tests are verified. Read-only on production code and test files.

## Workflow

### Phase 1: Security & Guardrails Audit
**Objective**: Audit code changes against LLM security risks and secret exposure per `references/llm-audit-signals.md`.

1. **Prompt Injection & Instruction Overrides**:
   - Inspect all prompt assembly locations where user input is formatted.
   - Verify user strings are properly enclosed in boundary delimiters (e.g., XML tags `<user_query>...</user_query>`) and sanitized.
   - For RAG systems, check for indirect prompt injection defenses against untrusted retrieved content.
   - Flag unshielded prompt interpolation as `[BLOCKING]`.
2. **Credential & Secret Exposure**:
   - Audit for hardcoded provider API keys (`sk-...`, `Bearer ...`).
   - Check for unredacted PII or system prompt leakage in user-facing responses.
   - Flag any hardcoded API key or credential leak as `[BLOCKING]`.
3. **Content Safety & Moderation**: for user-facing generation fed by user-generated content, verify a moderation/output-filter layer exists per `references/llm-audit-signals.md` section 4 — shipping unfiltered generation when a filter was a stated requirement is `[BLOCKING]`.

### Phase 2: Token Budget, Cost & Resilience Audit
**Objective**: Ensure changes prevent runaway token consumption and handle model provider failures gracefully.

1. **Token Exhaustion & Runaway Loops**:
   - Verify every model invocation specifies an explicit `max_tokens` limit.
   - Check agent loops and tool-calling chains for hard cycle limits (e.g., `max_iterations=10`) to prevent infinite recursion.
   - Flag unbounded loops or missing token ceilings as `[BLOCKING]`.
2. **Rate Limits, Timeouts & Fallbacks**:
   - Verify API calls include explicit timeouts and exponential backoff retry logic on HTTP 429 / 5xx errors.
   - Check that multi-provider fallback chains catch provider-specific errors cleanly.
3. **Observability**: verify new invocation paths emit traces (model, tokens, latency, feature attribution) per `references/llm-audit-signals.md` section 5 — untraced paths when tracing was a stated plan requirement are `[BLOCKING]`; unattributed token spend is `[ADVISORY]`.

### Phase 3: RAG Retrieval & Structured Schema Integrity Audit
**Objective**: Confirm retrieval pipelines and structured parsers adhere to robustness standards.

1. **Structured Outputs & Schema Validation**:
   - Audit Pydantic models for explicit field types, boundary validators, and handling of unexpected markdown fences.
2. **Context Window & Chunking Discipline**:
   - Verify chunk sizes and retrieval `top_k` do not exceed model context window bounds.
   - Ensure metadata (document ID, page, source URL) is preserved for citation tracking.
3. **Prompt Management**: verify behavior-carrying prompts are versioned artifacts rather than scattered literals, and that prompt changes ship with eval coverage and a rollback path per `references/llm-audit-signals.md` section 5.

### Phase 4: TDD Compliance & Test Integrity Audit
**Objective**: Detect TDD cheating and verify test substantive value.

1. **TDD Cheating Detection**:
   - Audit test files for meaningless assertions (`assert True`, `expect(x).toBe(x)`).
   - Confirm tests do not mock away the core class or parser under test.
   - Cross-check git history/diffs to ensure test assertions were not altered to force Green.
2. **Post-Code Verification (TDD Skipped/Inverted)**:
   - If TDD was skipped or inverted, verify that rigorous verification tests were added by `06-llm-test`.
3. **Severity Tagging**:
   - Any TDD cheating or missing post-code verification is classified as `[BLOCKING]`.

### Phase 5: Verdict Determination & Post-Review Bug Loop Handoff
**Objective**: Issue a decisive PASS or FAIL verdict.

- **PASS**: Granted if and only if **0 `[BLOCKING]` issues exist** (even if `[ADVISORY]` recommendations are present).
- **FAIL**: Mandated if **≥1 `[BLOCKING]` issue exists**. Formulate the structured Review Defect Handoff block to trigger the Post-Review Bug Loop in `00-llm-orchestrator`:
```yaml
handoff:
  from_skill: "07-llm-review"
  to_skill: "00-llm-orchestrator"
  verdict: "FAIL"
  re_entry_pipeline: 5 # 4a | 4b | 5 | 6
  blocking_issues:
    - severity: "BLOCKING"
      subsystem: "Security / Prompt Injection"
      location: "src/prompts/qa_prompt.py:28"
      root_cause: "Raw user input directly interpolated into prompt without delimiter encapsulation"
      evidence: "f'You are an expert. Answer {user_input}' leaves system instructions vulnerable to prompt override"
```

## Output Format
Review report structured as:
- **Security & Guardrails Audit**: Prompt injection, secrets, PII findings (`[BLOCKING]` or `[ADVISORY]`).
- **Token Budget & Cost Resilience Audit**: Token limits, loop recursion guards, retry/backoff.
- **RAG & Schema Integrity Audit**: Pydantic validation resilience, context window bounds.
- **TDD Compliance Audit**: Verification of genuine Red-Green-Refactor cycles.
- **Final Verdict**: Explicit **PASS** or **FAIL** with YAML handoff block if FAIL.

## Don'ts
- Do not modify, patch, or refactor code within this skill — read-only; all fixes belong to `05-llm-fix`.
- Do not issue an ambiguous verdict like "conditionally approved" — state PASS or FAIL decisively.
- Do not downgrade `[BLOCKING]` issues (prompt injection, token runaway loop, hardcoded secret, TDD cheating) to `[ADVISORY]`.
- Do not ignore missing `max_tokens` or unbounded agent iteration loops.
- Do not overlook unshielded raw user input in system prompts.

## Quality Checklist
- [ ] Were prompt injection defenses and boundary tags verified?
- [ ] Were API keys and secrets checked for hardcoding or exposure?
- [ ] Were token budget limits (`max_tokens`) and loop limits verified?
- [ ] Were retry backoff and rate-limiting protections audited?
- [ ] When tracing, prompt versioning, or content moderation were stated requirements, were the corresponding signals (`references/llm-audit-signals.md` sections 4–5) audited — or explicitly reported as not applicable?
- [ ] Was TDD compliance verified and checked for cheating signals?
- [ ] Are findings strictly tagged with `[BLOCKING]` or `[ADVISORY]`?
- [ ] If ≥1 `[BLOCKING]` issue exists, is FAIL issued with the YAML handoff block?
- [ ] Were zero code files modified within this review skill?
