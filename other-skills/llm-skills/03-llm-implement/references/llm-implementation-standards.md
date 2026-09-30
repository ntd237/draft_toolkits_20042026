# LLM Implementation Standards

Applied by `03-llm-implement` (and `05-llm-fix` where a fix touches the same concerns), alongside the resilience rules already in SKILL.md (max_tokens, timeouts, backoff, fence stripping). These are minimum standards — apply what the current unit's tests and acceptance criteria demand; flag conflicts with existing project conventions instead of silently overriding either side.

## Observability & Tracing
- Every LLM invocation path emits a trace through the project's tracing layer (Langfuse, LangSmith, or OpenTelemetry GenAI conventions): prompt template identifier + version, model + parameters, token usage (prompt/completion), latency, and outcome (success/error type).
- A new subsystem without tracing is incomplete: register its spans/metadata so `04-llm-bugfinder` Tier 0 (log/trace inspection) can operate without code probes.
- Cost attribution: tag traces with feature/agent identifiers so token spend is attributable per feature, not just per provider account.
- Logging: never log raw user input or completions containing PII/secrets unredacted (see Privacy below); log redacted payloads with a correlation id linking to the full trace in the tracing store.

## Prompt Management
- Prompts that carry business behavior are versioned artifacts (template files with version identifiers, or a prompt registry) — not string literals scattered across call sites; extract reusable prompt partials during Refactor.
- A prompt change that alters model behavior ships like a code change: it gets eval coverage (see `06-llm-test` golden datasets) and can be rolled back by reverting the version, not by hunting literals.
- When the project supports staged rollout, prompt versions are released behind the same canary/flag mechanism as code; document the rollback prompt version in the handoff summary.

## Streaming & UX
- Streaming responses (SSE/chunked) must handle client cancellation: abort the upstream request to stop token billing, and persist already-generated partial state safely.
- Parsers consuming streamed output must tolerate partial JSON (buffer until parseable, or use a partial-parse strategy) — never assume a single complete completion string.
- Surface provider failures mid-stream to the UX layer explicitly (error event), rather than silently truncating output.

## Caching
- Long static context (>1024 tokens, per `../07-llm-review/references/llm-audit-signals.md`) uses provider prompt caching where supported.
- Semantic caching (embedding-similarity response reuse) is permitted only for read-only, non-personalized queries — never cache personalized or permission-scoped answers, and never cache responses to injectable user content without normalization.

## Fine-Tuning Workflows (when the plan selects fine-tuning per `01-llm-brainstorm` Phase 2)
- Treat any fine-tuning change as Pipeline 3 (Complex): dataset preparation, training job, and post-training evaluation are separate planned waves.
- Training datasets are versioned artifacts with documented provenance (source, license, PII screening); eval the fine-tuned model against the same golden dataset used for the base model before swapping it into any environment (see `../06-llm-test/references/evaluation-engineering.md`).
- Model version swaps are configuration changes with explicit rollback (previous model identifier retained in config).

## Privacy & Compliance
- Sending user content to third-party model APIs must respect the project's data policy: screen for PII/secrets before dispatch (redaction layer at the gateway), honor documented retention choices (provider zero-retention endpoints where required).
- Never send data classified as sensitive (credentials, health/financial PII without legal review) to external providers; route such workloads to self-hosted models per the model selection decision.
- Trace/eval datasets persisting user content follow the same redaction and retention rules as logs.
