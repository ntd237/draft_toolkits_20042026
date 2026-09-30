# LLM Pipeline Routing Matrix & Blast Radius

## Overview
This document defines the routing matrix, blast radius evaluation, and decision heuristics for `00-llm-orchestrator` across Large Language Model (LLM) and Generative AI applications.

## 3 Request Groups & Pipeline Mapping

| Request Group | Description | Selected Pipeline | Primary Skills |
|---|---|---|---|
| **Group 1: New Implementation** | New RAG retriever, prompt template, Pydantic parser, vector integration, or agent workflow | Pipeline 1 (Simple)<br>Pipeline 2 (Ambiguous)<br>Pipeline 3 (Complex/Risky) | `06-llm-test` (Red) → `03-llm-implement` (Green+Refactor) → `07-llm-review` |
| **Group 2: Unknown-Cause Bug** | Hallucination, context window truncation, schema validation failure, prompt injection leakage, rate-limit/timeout | Pipeline 4a (Simple RCA)<br>Pipeline 4b (Complex RCA) | `04-llm-bugfinder` → (`06-llm-test` Red → `05-llm-fix` Green)* → `07-llm-review` |
| **Group 3: Known-Cause Bug** | Defect with confirmed root cause, exact stack trace, or review defect report | Pipeline 5 (Simple defect)<br>Pipeline 6 (Complex defect) | (`06-llm-test` Red → `05-llm-fix` Green)* → `07-llm-review` |

---

## 6 Canonical Pipeline Scenarios

### Pipeline 1: Simple LLM Implementation (Localized)
- **Condition**: Clear prompt/parser logic, touches 1 isolated component, deterministic parsing or utility, zero vector schema migration.
- **Sequence**: `06-llm-test` (Red) → `03-llm-implement` (Green + Refactor)* → `07-llm-review`.

### Pipeline 2: Ambiguous LLM Requirements
- **Condition**: Model selection unclear, prompt constraints or temperature undefined, output schema ambiguous, or evaluation metric unformulated.
- **Sequence**: `01-llm-brainstorm` → User Approval Gate (`docs/specs/spec-<name>.md`) → `06-llm-test` (Red) → `03-llm-implement` (Green + Refactor)* → `07-llm-review`.

### Pipeline 3: Complex / Multi-Agent / RAG Implementation
- **Condition**: Spans ≥2 subsystems (e.g., Vector DB + Chunking + Reranking + Agent Loop), introduces external tools, changes embedding models requiring re-indexing, or manages shared agent memory.
- **Sequence**: `01-llm-brainstorm` → User Approval Gate (`docs/specs/spec-<name>.md`) → `02-llm-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Parallel/Sequential Waves: `06-llm-test` (Red) → `03-llm-implement` (Green + Refactor)]* → `07-llm-review`.

### Pipeline 4: Unknown-Cause Bug Investigation & Resolution
- **Condition**: LLM symptom reported without verified cause (e.g., random output JSON parsing failure, context degradation across conversation turns, unexpected hallucination).
- **Sequence**: `04-llm-bugfinder` → Evaluates Blast Radius:
  - **4a (Simple / Localized)**: `06-llm-test` (Red) → `05-llm-fix` (Green + Refactor)* → `07-llm-review`.
  - **4b (Complex / Multi-System)**: `02-llm-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Bug-Fix Waves: `06-llm-test` (Red) → `05-llm-fix` (Green)]* → `07-llm-review`.

### Pipeline 5: Known-Cause Bug (Simple)
- **Condition**: Exact location and root cause identified (traceback, failing unit test, or review report), localized to 1 parser, regex, prompt string, or API client parameter.
- **Sequence**: `06-llm-test` (Red) → `05-llm-fix` (Green + Refactor)* → `07-llm-review`.

### Pipeline 6: Known-Cause Bug (Complex / Architectural)
- **Condition**: Confirmed defect spanning vector retrieval pipelines, agent state machine deadlock, runaway recursion in tool calling, or multi-provider fallback cascading errors.
- **Sequence**: `02-llm-plan` → User Approval Gate (`docs/plans/plan-<name>.md`) → [Bug-Fix Waves: `06-llm-test` (Red) → `05-llm-fix` (Green)]* → `07-llm-review`.

---

## LLM Blast Radius Decision Matrix

Evaluate the following technical signals to distinguish **Simple** vs **Complex / High Risk**:

| Signal / Axis | Simple (Pipeline 1, 4a, 5) | Complex / High Risk (Pipeline 3, 4b, 6) |
|---|---|---|
| **Subsystems Touched** | 1 isolated module (e.g., Output parser, text cleaner) | ≥2 systems (e.g., Embeddings + Vector DB + Agent State + Tools) |
| **Model Invocations** | Single static completion or chat call | Multi-agent coordination, recursive tool loops, dynamic routing |
| **Token Budget & Risk** | Short fixed prompts (<2k tokens), deterministic | Dynamic RAG context (>16k tokens), risk of context overflow or runaway cost |
| **Vector DB & Indexing** | Query-only against existing vector collection | Schema re-indexing, dimension mismatch, hybrid search migration |
| **Tool Calling & Side Effects** | Read-only calculation or schema formatting | State-mutating tools (database write, HTTP POST, shell commands) |
| **Error Handling & Fallbacks** | Standard single-provider retry | Multi-provider fallback (OpenAI → Claude → local vLLM), circuit breaking |
| **Security Surface** | Internal static prompt without user interpolation | Untrusted user input, prompt injection risk, PII / API key exposure |
| **Evaluation Complexity** | Deterministic unit tests (Pydantic, regex) | LLM-as-a-judge, Ragas metrics (faithfulness, recall), semantic evals |

> **Rule**: If ≥1 criterion falls under "Complex / High Risk", the orchestrator MUST route through `02-llm-plan`.
