---
name: 01-llm-brainstorm
description: "Clarifies ambiguous LLM requirements, formulates prompt strategies, and analyzes architectural trade-offs (Closed vs Open-source models, RAG vs Fine-tuning, Latency vs Token Cost, Context Window size) before implementation. Enforces open write-in options on all questions, halts at a mandatory Review Gate for user approval, and saves the specification to docs/specs/spec-<name>.md in Vietnamese Markdown. Read-only on production code."
---

# 01-llm-brainstorm — LLM Problem Discovery & Architectural Trade-offs

## Trigger
Invoked by `00-llm-orchestrator` when prompt requirements, model selection, retrieval strategies, or agent architectures are ambiguous (Pipeline 2), or prior to planning complex RAG/multi-agent systems (Pipeline 3). Read-only on production code; creates only specification files in `docs/specs/`.

## Workflow

### Phase 1: LLM Problem Discovery & Requirement Elicitation
**Objective**: Clarify undefined LLM requirements, interaction models, and domain constraints.

1. **Problem Scoping**: Cross-examine the request against the core LLM capabilities:
   - Task nature: Information extraction, RAG question answering, creative generation, agentic reasoning, code synthesis, or structured classification.
   - Input/Output modalities: Plain text, streaming tokens, multi-modal images/documents, structured JSON/Pydantic schemas.
   - Knowledge freshness: Static model weights sufficient vs dynamic external knowledge required.
2. **Interaction & Prompt Vectors**:
   - System persona, guardrail boundaries, tone of voice.
   - Context window constraints: Expected conversation history length, token budget per query.
   - Tool calling permissions: Read-only data lookups vs destructive API actions.
3. **Mandatory Write-in Option**: For every question or set of options presented, **always include an open custom write-in option** enabling the user to specify their own preference (e.g., `[Custom] Tùy chỉnh theo yêu cầu riêng`).

### Phase 2: Architectural & Engineering Trade-offs
**Objective**: Propose 2–3 viable design options balancing accuracy, latency, privacy, and token cost.

1. **Model Selection Trade-off (Closed vs Open-source)**:
   - *Proprietary APIs* (OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, Google Gemini 1.5 Pro): Frontier reasoning, zero infra management, but recurring token cost and external data transit.
   - *Open-Source Self-Hosted* (Llama 3, Mistral, Qwen hosted via vLLM / Ollama): Complete data sovereignty, predictable fixed GPU compute cost, but lower reasoning ceilings and self-managed infra.
2. **Knowledge Architecture Trade-off (Prompting vs RAG vs Fine-Tuning)**:
   - Few-shot in-context learning vs Vector RAG (hybrid dense + BM25, rerankers) vs LoRA / Full Fine-tuning.
3. **Latency vs Cost vs Quality Profile**:
   - Tiered model routing: Small fast models (GPT-4o-mini, Claude Haiku, Gemini Flash) for triage/extraction vs frontier models for deep synthesis.
   - Token optimization: Prompt caching, context pruning, semantic chunking.
4. **Recommendation**: Present options with explicit trade-offs and recommend 1 preferred approach, allowing user customization.

### Phase 3: Acceptance Criteria & TDD Boundary Formulation
**Objective**: Formulate concrete, testable behaviors for subsequent skills.

1. Draft acceptance criteria in structured Given/When/Then format or explicit rule checklists.
2. Clearly categorize criteria into:
   - **Deterministic Logic**: Pydantic schema validation, text chunking bounds, token budget estimators, regex output extraction, tool schema validators (strictly standard TDD test-first).
   - **Inverted TDD Candidates**: Prompt spikes, exploratory zero-shot reasoning, persona tone calibration (flagged for Inverted TDD per `references/tdd-exception-and-skip.md`).

### Phase 4: Mandatory Review Gate & Spec Generation
**Objective**: Present findings, pause for user review, and generate the final specification.

1. **Mandatory Summary & Pause**: Present a complete summary of clarified scope, model choices, architectural trade-offs, and acceptance criteria in chat. **Strictly pause and await explicit user review, additions, and approval.**
2. If the user provides feedback or adjustments, update the proposal and re-confirm.
3. **Artifact Generation**: Only after explicit approval, save the finalized specification to `docs/specs/spec-<name>.md` (where `<name>` is a descriptive kebab-case identifier, e.g., `spec-rag-hybrid-search.md`).
4. **The entire content of `docs/specs/spec-<name>.md` must be written in Vietnamese using standard Markdown.**

## Output Format
1. **Interactive Questions**: Focused questions with explicit open write-in options.
2. **Review Gate Block**:
   - Tóm tắt bài toán LLM & yêu cầu nghiệp vụ đã làm rõ.
   - Phân tích đánh đổi kiến trúc (Closed vs Open model, RAG vs Fine-tuning, Latency vs Chi phí token).
   - Danh sách Acceptance Criteria chi tiết (phân tách deterministic vs probabilistic).
   - Đánh dấu các unit áp dụng ngoại lệ TDD / Inverted TDD (nếu có).
   - **Yêu cầu dừng bắt buộc**: Chờ người dùng xác nhận và bổ sung trước khi lưu file spec.
3. **Artifact Generation**: Clickable link to `docs/specs/spec-<name>.md` in Vietnamese Markdown once approved.

## Don'ts
- Do not present questions without providing an open write-in option for user custom input.
- Do not create `docs/specs/spec-<name>.md` or advance to subsequent skills before receiving explicit user approval.
- Do not write the spec artifact in any language other than Vietnamese Markdown.
- Do not modify, create, or delete production code, prompt templates, or configuration files.
- Do not ignore token budget exhaustion, latency SLA, or prompt injection risks during design analysis.

## Quality Checklist
- [ ] Did every question include an open custom write-in option?
- [ ] Were LLM trade-offs (Closed vs Open models, RAG vs Fine-tuning, Latency vs Cost) analyzed?
- [ ] Were acceptance criteria separated into deterministic logic and probabilistic spikes?
- [ ] Did execution halt at the Review Gate for explicit user review and approval?
- [ ] Is `docs/specs/spec-<name>.md` authored in Vietnamese Markdown after approval?
- [ ] Were zero production code files modified?
