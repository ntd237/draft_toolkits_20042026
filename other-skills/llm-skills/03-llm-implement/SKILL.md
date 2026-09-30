---
name: 03-llm-implement
description: "Implements production code for new LLM features, prompt templates, structured output parsers (Pydantic / JSON schemas), vector retrieval pipelines, tool calling, and agent chains. Operates in TDD Green + Refactor mode after 06-llm-test authors Red tests (default), or first when TDD is skipped/inverted. Strictly prohibited from fixing bugs (exclusive to 05-llm-fix) and strictly prohibited from modifying tests to force Green."
---

# 03-llm-implement — LLM Feature Implementation (Green + Refactor)

## Trigger
Invoked by `00-llm-orchestrator` during new implementation pipelines (Pipelines 1, 2, 3) after `06-llm-test` has produced Red tests, or under approved TDD skip / inverted conditions per `references/tdd-exception-and-skip.md`. **Strictly prohibited from being invoked for defect fixing or Post-Review Bug Loop remediation (all defect fixes belong exclusively to `05-llm-fix`).**

## Workflow

### Phase 1: Green — Minimal Implementation with LLM Engineering Rigor
**Objective**: Write the minimal production code necessary to transition targeted tests from Red to Green while enforcing LLM reliability standards.

1. **Inspect Handoff**: Review the failing test specifications, acceptance criteria, and YAML handoff block from `06-llm-test` (or `00-llm-orchestrator` / `02-llm-plan` if TDD is skipped).
2. **Implement Minimal Logic**: Author only the code required to satisfy the failing tests. Avoid speculative features, premature abstractions, or unused configuration hooks.
3. **Enforce LLM Engineering Standards**:
   - *Structured Outputs & Parsers*: Implement robust Pydantic models; strip markdown fences (````json ... ````) and clean whitespace prior to JSON parsing; provide graceful schema validation error handling.
   - *Vector RAG & Retrieval*: Implement clean text chunking with appropriate overlap; ensure metadata dictionaries preserve document sources; normalize embedding vector operations.
   - *Model Gateway & Resilience*: Enforce explicit `max_tokens` limits, temperature parameters, request timeouts, and exponential backoff retry logic.
   - *Agent Tools*: Author strict JSON schemas for tool definitions; validate incoming arguments against expected types before invoking external functions.
4. **Architecture Decoupling**: Keep deterministic parsers and data preprocessors decoupled from live network LLM API calls, interacting via interfaces or dependency injection.
5. **Verify Green**: Execute the test runner (e.g., `pytest`, `npm test`) to confirm all targeted tests pass.

### Phase 2: Refactor & Clean Code
**Objective**: Enhance code structure, readability, and maintainability without altering externally observable behavior.

1. Refactor for clarity, extract reusable prompt partials or Pydantic validators, and conform to project styling.
2. Ensure token counting and prompt formatting logic are computationally efficient.
3. Re-run the entire related test suite (not just the targeted tests) to confirm zero regressions.

### Phase 3: Transition & Handoff
**Objective**: Hand off verified code to the next skill in the pipeline.

1. If running under standard TDD: prepare Green handoff for the next atomic behavior unit or transition to `07-llm-review`.
2. If running under TDD Skipped or Inverted TDD: hand off immediately to `06-llm-test` (Scenario B: Post-Implementation Validation) to author safety tests.

## Implementation Standards
Beyond the resilience rules above, authored code must observe the domain standards in `references/llm-implementation-standards.md` — covering observability & tracing (every LLM invocation traced with model, tokens, latency, cost attribution), prompt management (versioned prompt artifacts, eval-covered prompt changes, rollback), streaming & UX (cancellation stops billing, partial-JSON tolerance), caching (provider prompt caching; semantic cache only for non-personalized read-only queries), fine-tuning workflows (versioned datasets, post-train eval, rollback), and privacy & compliance (PII screening before third-party dispatch, retention rules). Standards never justify scope creep: apply only what the targeted tests and acceptance criteria demand, and report back when a standard conflicts with existing project conventions (project conventions win).

## Output Format
Provide modified files/diffs and a concise summary:
- Implemented LLM behavior, prompt templates, or parsers.
- Resilience measures applied (timeouts, schema validation, token caps).
- Test execution output confirming Green status.
- Refactoring notes and confirmation of zero regressions across the suite.

## Don'ts
- **Absolute Prohibition**: Do not touch, diagnose, or fix bugs, crashes, or review defects — all defect fixing belongs strictly to `05-llm-fix`.
- Do not alter, comment out, or delete test assertions to make tests pass — TDD cheating is strictly prohibited.
- Do not execute live, unmocked LLM network calls inside unit tests without explicit approval.
- Do not interpolate raw, unsanitized user strings directly into system prompts.
- Do not omit `max_tokens` or timeout bounds on model completion requests.
- Do not implement code beyond the current acceptance criteria or failing tests.
- Do not declare completion under Inverted TDD or TDD Skipped without handing off to `06-llm-test` for post-implementation verification.

## Quality Checklist
- [ ] Does the authored code strictly satisfy targeted tests without scope creep?
- [ ] Were zero test assertions modified or weakened to force Green?
- [ ] Are Pydantic schemas, text chunkers, and parsers resilient to malformed outputs?
- [ ] Are model API calls protected with timeouts and token budget limits?
- [ ] Was the entire test suite re-run after refactoring to confirm zero regressions?
- [ ] Is this skill used strictly for new features, never for bug fixing?
