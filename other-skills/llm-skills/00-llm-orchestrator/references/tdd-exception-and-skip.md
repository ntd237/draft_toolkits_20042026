# LLM TDD Exceptions, Skip Criteria & Inverted Testing

## 1. Standard TDD Policy (Default)
In LLM and GenAI application engineering, all deterministic logic components MUST follow the standard **Red → Green → Refactor** cycle:
1. `06-llm-test` authors a failing unit/integration test (Red).
2. `03-llm-implement` or `05-llm-fix` writes the minimal production code to pass (Green) and optimizes (Refactor).
3. `07-llm-review` audits implementation and test fidelity.

### Target Deterministic Components:
- **Output Parsers & Validators**: Pydantic models, JSON schema extractors, regex fallback cleaners.
- **RAG Preprocessing & Chunking**: Recursive text splitters, token length estimators, metadata extractors.
- **Tool Calling & Agent Routers**: Tool parameter schemas, dispatcher functions, router conditional branches.
- **Guardrails & Filters**: Regex sanitizers, keyword blocklists, prompt injection heuristic checks.

---

## 2. Permissible TDD Skip Criteria
Skipping the test-first Red phase is permitted IF AND ONLY IF one of the following 3 criteria is formally met and recorded in the handoff:

| Skip Reason Code | Condition Description | Required Handoff Field |
|---|---|---|
| `user-request` | The user explicitly directs the agent to bypass TDD for this task. | `skip_reason: "user-request"` |
| `no-test-framework` | The project lacks a test runner (e.g., pytest, jest) and the user explicitly declines installing one. | `skip_reason: "no-test-framework"` |
| `config-only` | The changes are strictly confined to non-executable configuration: provider API keys, model parameters (`temperature`, `top_p`, `max_tokens`), or purely cosmetic prompt wording changes with no testable behavioral logic. | `skip_reason: "config-only"` |

### Fallback Ordering when TDD is Skipped
When TDD is skipped under an approved criterion, the execution order shifts to Fallback Ordering. **Skipping subsequent testing is strictly prohibited** unless `no-test-framework` applies:

1. **New Implementation / Refactoring**:
   `03-llm-implement` → `06-llm-test` (Scenario B: Post-Implementation Validation) → `07-llm-review`.
2. **Defect Fixing**:
   `05-llm-fix` → `06-llm-test` (Scenario A: Bug Fix Confirmation) → `07-llm-review`.

> **Critical Rule**: If `no-test-framework` applies, `06-llm-test` is omitted, but `03-llm-implement` / `05-llm-fix` must provide a comprehensive **Manual Verification Protocol** (sample prompt queries, expected JSON outputs, and curl/CLI invocation commands).

---

## 3. Inverted TDD Protocol (Prompt Spikes & Exploratory Reasoning)
Certain generative behaviors cannot be specified upfront via deterministic unit tests prior to empirical experimentation with the target model. Inverted TDD (Implement First → Author Tests Immediately After) is permitted for specific atomic units:

### Permitted Inverted TDD Scenarios:
1. **Model Capability & Reasoning Spikes**:
   - Evaluating whether a new model version (e.g., Claude 3.5 Sonnet vs GPT-4o vs Gemini 1.5 Pro) can accurately follow complex multi-step reasoning zero-shot.
   - Prototyping few-shot exemplars to discover optimal in-context learning patterns.
2. **Exploratory Free-Form Generation & Tone Tuning**:
   - Authoring creative copywriting chains, persona tone styling, or synthetic dataset generation prompts.
3. **Complex Agentic Chain-of-Thought Prototyping**:
   - Exploring raw agent scratchpad loops and tool selection before locking down strict state transitions.

### Inverted TDD Guardrails:
- The unit must be flagged as `inverted_tdd: true` in the plan or brainstorm spec.
- Production prompt or chain code is authored first by `03-llm-implement` (features) or `05-llm-fix` (fixes).
- Immediately upon completing the spike, `06-llm-test` **must** execute to author characterization tests or LLM evaluation assertions (e.g., validating Pydantic output compliance, non-empty response, absence of leaked system instructions, or Ragas faithfulness threshold) to lock in behavior.
- Bypassing subsequent verification after an inverted implementation is strictly prohibited.
