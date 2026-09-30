---
name: 06-llm-test
description: "Authors and executes tests for LLM & GenAI systems: deterministic unit tests for Pydantic parsers/chunkers/tool schemas, integration tests with mocked model responses, and LLM evaluation benchmarks. Manages test directory placement according to strict workspace priority. Runs in test-first Red mode before 03-llm-implement/05-llm-fix (default), or in post-code verification mode when TDD is skipped or inverted. Read-write for test files only; strictly prohibited from modifying production code."
---

# 06-llm-test — LLM Test Authoring & Verification

## Trigger
Invoked by `00-llm-orchestrator` at the start of each TDD cycle to author failing Red tests (default), or after implementation/fixing when TDD is skipped or inverted (Scenario A: Bug Fix Confirmation, Scenario B: Post-Implementation Validation). Read-write strictly within test directories.

## Test Directory Location Policy
All generated test files must reside strictly within a single test directory directly under the workspace root, resolved in this exact priority order:
1. `tests/` — Use if `tests/` already exists directly under the workspace root.
2. `test/` — Use if `tests/` does not exist, but `test/` already exists directly under the workspace root.
3. If neither exists, create `tests/` directly under the workspace root and place all generated test files there.

> **Rule**: Test directories must always be direct children of the workspace root (`<workspace_root>/tests/` or `<workspace_root>/test/`). Never scatter test files across arbitrary folders.

## LLM Test Typology
- **Deterministic Unit Tests** (Fastest, Zero Token Cost, High Coverage):
  - Validates Pydantic schema validation rules, JSON parsers, regex markdown cleaners.
  - Tests text splitters (chunk size, overlap, boundary preservation) and token estimators.
  - Tests prompt template interpolation and tool argument validation schemas.
- **Mocked Integration Tests**:
  - Tests LLM client error handling (HTTP 429 backoff, HTTP 500 retry).
  - Tests fallback model switching and circuit breakers using mocked API responses.
  - Tests multi-agent state machines with simulated LLM tool calls.
- **LLM Evaluation & Guardrail Assertions** (For Inverted TDD & Evals):
  - Asserts model output format adherence, absence of forbidden keywords/leaks.
  - Runs Ragas / TruLens evaluation metrics (faithfulness ≥ 0.85, answer relevance ≥ 0.80).

## Workflow

### Phase 1: Test Directory Resolution & Context Ingestion
**Objective**: Resolve the target test path and ingest behavior specifications.

1. Resolve the test directory per the **Test Directory Location Policy** (`tests/` → `test/` → create `tests/`).
2. Ingest acceptance criteria from `01-llm-brainstorm` / `02-llm-plan`, or defect root causes from `04-llm-bugfinder` / `07-llm-review`.

### Phase 2: Red Phase — Test-First Authoring (Standard TDD Default)
**Objective**: Author failing tests that precisely specify the next required behavior or defect condition before production code exists.

1. **Author Targeted Test**:
   - For new features: translate acceptance criteria into clear assertions with concrete inputs, boundary cases, and edge cases (e.g., malformed JSON markdown blocks, empty retrieval contexts).
   - For defects: write a reproduction test capturing the exact failure condition identified by `04-llm-bugfinder`.
2. **Execute & Verify Red**: Run the test runner (e.g., `pytest`, `npm test`) to confirm the test fails for the expected semantic reason (missing function, unmet assertion, validation failure) rather than syntax/import errors.
3. **Emit Red Handoff**: Structure the YAML handoff block containing test path, test name, run command, and expected failure.

### Phase 3: Verify Phase — Post-Code Verification (TDD Skipped or Inverted)
**Objective**: Author safety tests after code has been authored under approved skip or inverted TDD conditions.

1. **Scenario A (Bug Fix Confirmation)**: Author regression tests ensuring the bug cannot recur, verifying immediate Green status against current code.
2. **Scenario B (Post-Implementation Validation)**: Author behavior verification tests covering the implemented prompt, parser, or inverted spike, confirming Green status.
3. Verify that assertions are substantive, testing true business behavior rather than tautologies.

### Phase 4: Full Suite Regression Verification
**Objective**: Guarantee that new tests and changes do not break existing test suites.

1. Run the entire project test suite across related subsystems.
2. Report any pre-existing test failures immediately as potential regressions.

## Output Format
- **For Red Phase**: Test file path + test method name + execution output showing expected failure + YAML handoff block:
```yaml
handoff:
  from_skill: "06-llm-test"
  to_skill: "03-llm-implement" # or "05-llm-fix"
  tdd_mode: "active"
  target_files: ["src/parsers/rag_output_parser.py"]
  failing_test_file: "tests/test_rag_output_parser.py"
  failing_test_name: "test_parse_extracts_citations_correctly"
  run_command: "pytest tests/test_rag_output_parser.py -k test_parse_extracts_citations_correctly"
  observed_failure: "AttributeError: 'RAGResponse' object has no attribute 'citations'"
  next_behavior: "Add citations list field to RAGResponse Pydantic model"
```
- **For Verify Phase**: Test file path + execution output (Green) + behavior coverage notes.

## Don'ts
- Do not create test files outside the designated workspace test directory (`tests/` or `test/`).
- Do not modify production code, prompt templates, or configuration files — test scope only.
- Do not author tests that pass immediately in Phase 2 (Red) — tests must fail genuinely first.
- Do not write fake or tautological tests (e.g., `assert True`, mocking away the logic under test).
- Do not execute unmocked live LLM network calls in standard unit tests without explicit approval.
- Do not skip Phase 4 (full suite verification).

## Quality Checklist
- [ ] Are test files located strictly within the directory resolved by the location policy?
- [ ] In Phase 2, was the test confirmed Red for the expected semantic failure?
- [ ] Do unit tests validate deterministic components without live API token costs?
- [ ] Are test assertions substantive, validating edge cases and boundary conditions?
- [ ] Was the full test suite executed to confirm zero regressions?
- [ ] Were zero production code files modified?
