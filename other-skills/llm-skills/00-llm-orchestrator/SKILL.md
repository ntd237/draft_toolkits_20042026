---
name: 00-llm-orchestrator
description: "Master orchestrator and Domain Gatekeeper for LLM & Generative AI applications (RAG architectures, multi-agent workflows, tool/function calling, prompt engineering, context window management, and LLM evaluation). Classifies requests into 3 groups, assesses blast radius across token budgets and model dependencies, coordinates 6 canonical pipelines, enforces TDD discipline with skip and inverted mechanisms, manages approval checkpoints, drives the Post-Review Bug Loop, and owns the mandatory harness execution log mechanism (docs/harness-logs/). Mandatory entrypoint for all LLM/GenAI tasks."
---

# 00-llm-orchestrator — LLM & GenAI Systems Orchestrator

## Trigger
Triggers for any request involving Large Language Models (LLMs) and Generative AI systems: RAG pipelines, multi-agent orchestrations, tool/function calling, prompt templates, structured outputs/Pydantic schemas, vector databases, embeddings, context window management, guardrails, and model evaluations. Mandatory entrypoint before any child skill (01–07) executes.

## Workflow

### Phase 1: Domain Gatekeeper
**Objective**: Verify the request falls strictly within LLM and GenAI engineering boundaries.

1. **In-Scope Evaluation**: Accepts tasks involving LLM application frameworks (LangChain, LlamaIndex, LiteLLM, Vercel AI SDK), model providers (OpenAI, Anthropic Claude, Google Gemini, Ollama, vLLM), vector databases (Qdrant, Pinecone, Chroma, pgvector), prompt engineering, structured parsing, agentic tool calling, context compression, guardrails, and LLM-as-a-judge evaluations.
2. **Out-of-Scope Rejection**: If the task is unrelated to LLM/GenAI (e.g., pure frontend CSS styling, native mobile UI layouts, traditional relational CRUD without AI, OS automation scripts) → politely decline, declare that this toolkit specializes exclusively in LLM & GenAI applications, and halt.
3. **Hybrid Handling**: If an application bundles web/mobile frontends with LLM backends (e.g., "build a React chat UI connected to a RAG API"), restrict this toolkit to the LLM/RAG backend architecture and delegate UI tasks to web/mobile toolkits.

### Phase 2: Request Classification (3 Groups)
**Objective**: Classify the request into 1 of 3 operational groups:

1. **Group 1: New Implementation**: New RAG retrievers, agent chains, tool integrations, Pydantic schemas, prompt templates, or refactoring.
2. **Group 2: Unknown-Cause Bug**: Symptoms reported without verified root causes (hallucination, context truncation, JSON schema validation error, prompt injection vulnerability, vector retrieval latency, rate-limit/timeout) → mandatory routing to `04-llm-bugfinder`.
3. **Group 3: Known-Cause Bug**: Defect with confirmed root cause, exact stack trace, or review defect report.

### Phase 3: Blast Radius & Model Risk Assessment
**Objective**: Determine whether `01-llm-brainstorm` and/or `02-llm-plan` are mandatory based on `references/llm-pipeline-routing.md`.

- **Ambiguous Scope** (unclear prompt constraints, uncertain model selection, undefined parsing schema) → mandatory `01-llm-brainstorm`.
- **Complex / High Risk** (touches multi-agent state machines, changes vector index embeddings schema, introduces external tool execution, or risks runaway token loops) → mandatory `02-llm-plan`.
- **Simple & Localized** (single prompt adjustment, isolated Pydantic validator, deterministic helper function) → bypass planning and enter TDD directly.

### Phase 4: Route to 6 Canonical Pipelines & Checkpoint Gates
**Objective**: Direct work through exactly 1 of 6 canonical pipeline flows:

| # | Pipeline Name | Skill Execution Sequence |
|---|---|---|
| **1** | Simple Implementation | `06-llm-test` (Red) → `03-llm-implement` (Green+Refactor)* → `07-llm-review` |
| **2** | Ambiguous Implementation | `01-llm-brainstorm` → User Approval → `06-llm-test` (Red) → `03-llm-implement` (Green+Refactor)* → `07-llm-review` |
| **3** | Complex / Multi-Agent / RAG | `01-llm-brainstorm` → User Approval → `02-llm-plan` → User Approval → [TDD Waves: `06-llm-test` Red → `03-llm-implement` Green+Refactor]* → `07-llm-review` |
| **4a** | Unknown Bug (Simple) | `04-llm-bugfinder` → `06-llm-test` (Red) → `05-llm-fix` (Green+Refactor)* → `07-llm-review` |
| **4b** | Unknown Bug (Complex) | `04-llm-bugfinder` → `02-llm-plan` → User Approval → [Bug Waves: `06-llm-test` Red → `05-llm-fix` Green]* → `07-llm-review` |
| **5** | Known Bug (Simple) | `06-llm-test` (Red) → `05-llm-fix` (Green+Refactor)* → `07-llm-review` |
| **6** | Known Bug (Complex) | `02-llm-plan` → User Approval → [Bug Waves: `06-llm-test` Red → `05-llm-fix` Green]* → `07-llm-review` |

(*) Repeat per atomic behavior. For TDD skip criteria or Inverted TDD, consult `references/tdd-exception-and-skip.md`.

#### Mandatory Approval Checkpoints:
1. **Brainstorm Gate (`01-llm-brainstorm`)**: Formulates options with open write-in choices, trade-offs (closed vs open models, latency vs cost), and pauses until explicit user approval before saving `docs/specs/spec-<name>.md` (in Vietnamese Markdown).
2. **Plan Gate (`02-llm-plan`)**: Generates an execution plan (`docs/plans/plan-<name>.md` in Vietnamese Markdown) decoupling deterministic logic from LLM calls, and strictly pauses until the user approves the wave breakdown.

### Phase 5: Post-Review Bug Loop Governance
**Objective**: Guarantee that review failures are remediated strictly through bug-fix pipelines.

1. When `07-llm-review` returns `FAIL` (due to ≥1 `[BLOCKING]` issue such as prompt injection risk, runaway token loop, unhandled rate-limit, unsafe parser, or TDD cheating), the orchestrator **must** re-route to a bug-fix pipeline (4a, 4b, 5, or 6).
2. The root cause is extracted directly from the review defect report.
3. **Strict Skill Binding**: Defect code fixes must be executed exclusively by `05-llm-fix` (never `03-llm-implement`).
4. **Max 3 Iterations**: If review fails 3 consecutive times on the same issue, halt execution and escalate to the user.

## Output Format
Before invoking child skills, emit a structured coordination block:
- **Domain Gate**: Pass / Reject (with technical rationale)
- **Classification**: New Implementation / Unknown-Cause Bug / Known-Cause Bug
- **Blast Radius**: Simple / Complex (token budget, model dependencies, tool execution risk)
- **Selected Pipeline**: Scenario # (1–6)
- **Next Skill**: First skill to invoke + transition handoff

## Handoff Contract Schemas

### 1. TDD Red Handoff (`06-llm-test` → `03-llm-implement` / `05-llm-fix`)
```yaml
handoff:
  from_skill: "06-llm-test"
  to_skill: "03-llm-implement" # or "05-llm-fix"
  tdd_mode: "active"
  target_files: ["src/parsers/action_parser.py"]
  failing_test_file: "tests/test_action_parser.py"
  failing_test_name: "test_parse_valid_json_with_markdown_fence"
  run_command: "pytest tests/test_action_parser.py -k test_parse_valid_json_with_markdown_fence"
  observed_failure: "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"
  next_behavior: "Strip markdown fences (```json ... ```) before parsing Pydantic model"
```

### 2. TDD Skipped Code Handoff (`00-llm-orchestrator` / `02-llm-plan` → `03` / `05`)
```yaml
handoff:
  from_skill: "00-llm-orchestrator" # or "02-llm-plan"
  to_skill: "03-llm-implement" # or "05-llm-fix"
  tdd_mode: "skipped"
  skip_reason: "user-request" # "user-request" | "no-test-framework" | "config-only"
  target_files: ["src/config/model_config.py"]
  task_goal: "Add temperature and max_tokens parameters to LiteLLM router config"
  acceptance_criteria: "Router exposes max_tokens=4096 and temperature=0.2 across fallback models"
```

### 3. TDD Skipped Test Handoff (`03-llm-implement` / `05-llm-fix` → `06-llm-test`)
```yaml
handoff:
  from_skill: "03-llm-implement" # or "05-llm-fix"
  to_skill: "06-llm-test"
  tdd_mode: "skipped"
  scenario: "B" # "A" for Bug Fix Confirmation | "B" for Post-Implementation Validation
  target_files: ["src/config/model_config.py"]
  files_modified: ["src/config/model_config.py"]
  implemented_behavior: "Default model parameters clamped within provider limits"
  run_command: "pytest tests/test_model_config.py"
```

### 4. Defect Diagnosis Handoff (`04-llm-bugfinder` → `06-llm-test` / `02-llm-plan`)
```yaml
handoff:
  from_skill: "04-llm-bugfinder"
  to_skill: "06-llm-test" # or "02-llm-plan"
  offending_system: "RAG Retrieval / Context Window"
  exact_location: "src/rag/retriever.py:78"
  root_cause: "Top-k=20 retrieval without chunk truncation overflows model 8k context window"
  blast_radius: "simple" # "simple" | "complex"
  recommended_fix: "Apply token-budget truncation and reranking before prompt assembly"
  cleanup_verified: true
```

### 5. Review Defect Handoff (`07-llm-review` FAIL → `00-llm-orchestrator`)
```yaml
handoff:
  from_skill: "07-llm-review"
  to_skill: "00-llm-orchestrator"
  verdict: "FAIL"
  re_entry_pipeline: 5 # 4a | 4b | 5 | 6
  blocking_issues:
    - severity: "BLOCKING"
      subsystem: "Security / Prompt Injection"
      location: "src/agents/user_agent.py:45"
      root_cause: "Raw user input directly interpolated into system prompt without sanitization"
      evidence: "f'System: You are an assistant. {user_input}' allows prompt override"
```

## Harness Execution Log (Mandatory)
Every pipeline run (Pipelines #1–#6) MUST produce a harness execution log file — in-chat YAML handoff blocks NEVER exempt or replace it.

1. **Before routing to the first skill**, Read `references/execution-log.md` and follow its schema verbatim: create `docs/harness-logs/<category>_<task_name>_<yyyymmdd>_<hhmmss>.md` (timestamp from a real shell command, never guessed), creating the directory if needed.
2. **After each child skill completes**, append its per-skill section immediately (do not batch at the end) — the orchestrator appends on behalf of the child skills.
3. **At pipeline completion** (including FAIL outcomes and Post-Review Bug Loop re-routes), append the pipeline summary section. For review-fail re-routes, keep the same log file and append the re-route sections — never create a second file for the same task.
4. Log content is written in Vietnamese; skill names, file paths, commands, and status keywords (COMPLETED, FAILED, PARTIAL, PASS, FAIL) stay in English.
5. Single-skill, read-only advisory tasks (pure explanation, ad-hoc Q&A) do not require a log.

## Don'ts
- Do not accept non-LLM/GenAI tasks (e.g., pure CSS/React layout, native iOS/Android, standard SQL without AI) without passing the Domain Gate.
- Do not dispatch `03-llm-implement` to fix bugs or remediate `07-llm-review` defects — all defect fixes belong strictly to `05-llm-fix`.
- Do not bypass `04-llm-bugfinder` when root causes are unverified symptoms (e.g., "model hallucinates on PDF inputs").
- Do not advance past approval gates of `01-llm-brainstorm` or `02-llm-plan` without explicit user sign-off.
- Do not apply Fallback Ordering while TDD is active without recording an approved skip reason (`user-request`, `no-test-framework`, or `config-only`).
- Do not allow the Post-Review Bug Loop to exceed 3 iterations on the same defect.
- Do not run any pipeline (1–6) without creating the harness execution log in `docs/harness-logs/` before the first skill runs and appending each skill section after completion — the in-chat YAML handoff never replaces the log file.
- Do not create a second log file for the same task on Post-Review Bug Loop re-routes — append to the existing one.

## Quality Checklist
- [ ] Has the Domain Gate confirmed the request belongs to LLM & GenAI engineering?
- [ ] Is the request categorized accurately into 1 of the 3 groups?
- [ ] Does the selected pipeline match 1 of the 6 canonical scenarios?
- [ ] Are mandatory approval checkpoints enforced for brainstorm specs and implementation plans?
- [ ] Does the Post-Review Bug Loop route defects exclusively to `05-llm-fix`?
- [ ] Are structured YAML handoff blocks populated across all skill transitions?
- [ ] Was the harness execution log created in `docs/harness-logs/` before the first skill ran, with one section appended per completed skill and the pipeline summary appended at the end (per `references/execution-log.md`)?
