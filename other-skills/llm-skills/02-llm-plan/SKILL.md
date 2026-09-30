---
name: 02-llm-plan
description: "Produces execution-ready implementation and risk mitigation plans for complex LLM systems (RAG pipelines, multi-agent workflows, tool integrations, and architectural defects). Decouples deterministic logic from probabilistic model calls, plans model risks (fallback models, rate limits, token quotas, prompt injection), partitions work into parallel TDD waves, and halts at a mandatory Plan Approval Gate before execution. Saves plan to docs/plans/plan-<name>.md in Vietnamese Markdown. Read-only on production code."
---

# 02-llm-plan — LLM Architecture & Wave Planning

## Trigger
Invoked by `00-llm-orchestrator` for complex features (Pipeline 3), complex unknown-cause bug investigations (Pipeline 4b), or complex known defects (Pipeline 6). Receives input from `01-llm-brainstorm` (specification in `docs/specs/spec-<name>.md`) or `04-llm-bugfinder` (defect diagnosis). Read-only on production code; writes plans exclusively to `docs/plans/`.

## Workflow

### Phase 1: Architectural Decoupling & Unit Decomposition
**Objective**: Break down requirements into atomic, independently testable units by decoupling deterministic logic from non-deterministic LLM API invocations.

1. **Architecture Decoupling**: Isolate pure deterministic business logic (text chunking, metadata extraction, Pydantic schemas, tool dispatchers, token estimators, score rerankers) from probabilistic LLM calls. Deterministic units run in fast, zero-token isolated tests without external API dependencies.
2. **Decomposition**: Partition work into atomic units covering:
   - *Data & Retrieval Tier*: Document loaders, chunking splitters, vector store adapters, embedding clients, hybrid searchers, rerankers.
   - *Model & Gateway Tier*: Provider clients (OpenAI, Anthropic, Gemini, LiteLLM), router, retry with exponential backoff, fallback chains, rate limiter / token bucket.
   - *Structured Schema & Parser Tier*: Pydantic models, JSON schema extractors, repair parsers.
   - *Agent & Tool Orchestration Tier*: Tool definitions, state graphs (LangGraph/CrewAI), memory managers, human approval hooks.
   - *Guardrails & Evaluation Tier*: Sanitizers, prompt injection filters, evaluation metrics.
3. **Dependency Mapping**: Establish prerequisite links between units to determine which can run in parallel versus those requiring sequential ordering.

### Phase 2: LLM Risk & Migration Planning
**Objective**: Identify and mitigate LLM provider, token budget, and security risks.

1. **Provider Outages & Rate Limits**:
   - HTTP 429 rate-limiting, token quota limits, exponential backoff with jitter.
   - Fallback chain configuration (e.g., Primary: OpenAI GPT-4o → Fallback: Anthropic Claude 3.5 Sonnet → Local: vLLM).
2. **Context Window & Token Budgeting**:
   - Enforce hard limits on prompt tokens, retrieved chunks count (`top_k`), and maximum generation length (`max_tokens`).
   - Sliding-window and summarization policies for multi-turn conversation memory.
3. **Security & Prompt Injection Defense**:
   - Sanitize untrusted user input before prompt interpolation.
   - Indirect prompt injection defense for untrusted retrieved documents (XML tagging, system prompt hardening).
   - Secret redaction (preventing API keys, PII, or internal system prompts from leaking into model responses).
4. **Vector Database & Schema Migration**:
   - If embedding models change (e.g., dimension switch from 1536 to 3072): plan vector collection recreation, re-indexing scripts, and rollback strategies.
5. **Observability & Tracing**: assign tracing coverage to the relevant waves — every new LLM invocation path registers spans/metadata (model, tokens, latency, feature identifier) in the project's tracing layer (Langfuse/LangSmith/OpenTelemetry) so `04-llm-bugfinder` Tier 0 can operate without code probes, and token cost is attributable per feature.
6. **Privacy & Compliance Screening**: if user content flows to third-party model APIs, plan the PII/secret redaction layer at the gateway, the retention choice (provider zero-retention endpoints where required), and routing of sensitive workloads to self-hosted models per the model selection decision.

### Phase 3: Wave Sequencing & Plan Artifact Generation
**Objective**: Group units into executable waves and generate the comprehensive plan artifact.

1. **Wave Ordering**: Group independent units into concurrent waves (Wave 1: Deterministic Parsers & Preprocessors → Wave 2: Vector DB & Retrieval Logic → Wave 3: Model Client, Router & Fallback → Wave 4: Agent Chains & Guardrails).
2. **TDD Mode Assignment**: Tag each unit as standard TDD (`tdd_mode: "active"`), skipped (`tdd_mode: "skipped"` with reason), or Inverted TDD (`inverted_tdd: true` for prompt spikes).
3. **Artifact Generation**: Save the complete plan document to `docs/plans/plan-<name>.md` (e.g., `docs/plans/plan-rag-pipeline.md`).
4. **Language Protocol**: The entire content of `docs/plans/plan-<name>.md` must be written in **Vietnamese Markdown**.

### Phase 4: Mandatory Plan Review & Approval Gate
**Objective**: Present the plan to the user and halt until explicit confirmation is granted.

1. Present a concise plan summary and a clickable link to `docs/plans/plan-<name>.md` in chat.
2. **Mandatory User Approval Gate**: Strictly pause execution. **Do not advance to TDD waves, test authoring (`06-llm-test`), or code implementation without explicit user review and approval.**
3. If the user requests adjustments or scope changes, update `docs/plans/plan-<name>.md` and re-confirm.

## Output Format
Save the plan file to `docs/plans/plan-<name>.md` in **Vietnamese Markdown** containing:
- Tổng quan kiến trúc & phạm vi (các hệ thống LLM liên quan, tách biệt logic xác định khỏi lời gọi mô hình).
- Kế hoạch rủi ro LLM (Fallback models, Rate limits, Token quotas, Chống prompt injection).
- Kế hoạch observability & privacy (tracing/cost attribution cho từng wave; redaction & retention khi gửi dữ liệu người dùng cho API bên thứ ba).
- Kế hoạch migration Vector DB & Embeddings (nếu có thay đổi schema/dimension).
- Phân chia các Wave thực thi chi tiết (danh sách unit, tệp mục tiêu, acceptance criteria, chế độ TDD).
- Thứ tự thực thi đề xuất cho `00-llm-orchestrator`.

In chat: Provide a summary and file link, then **halt execution and prompt the user for approval.**

## Don'ts
- Do not create, modify, or execute production code, prompt templates, or configuration files.
- Do not proceed to wave execution or invoke `06-llm-test` / `03-llm-implement` before receiving explicit user approval.
- Do not bundle dependent units into the same parallel wave.
- Do not omit fallback models, rate limit mitigations, or prompt injection defenses from the plan.
- Do not write the plan file in any language other than Vietnamese Markdown.
- Do not design monolithic functions that entangle Pydantic parsing with live LLM API calls.

## Quality Checklist
- [ ] Is the plan saved at `docs/plans/plan-<name>.md` in Vietnamese Markdown?
- [ ] Are deterministic components decoupled from live LLM network calls?
- [ ] Are fallback models, rate limits, and token budgets addressed?
- [ ] Are prompt injection and security defenses incorporated into the plan?
- [ ] Are tracing coverage and privacy screening (redaction, retention, sensitive-workload routing) assigned to waves whenever the corresponding dimensions were flagged in brainstorming?
- [ ] Are units structured into dependency-ordered waves with concrete acceptance criteria?
- [ ] Did execution strictly halt at the Approval Gate awaiting explicit user sign-off?
