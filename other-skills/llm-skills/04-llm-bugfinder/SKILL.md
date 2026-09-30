---
name: 04-llm-bugfinder
description: "Investigates and isolates the true root cause of LLM system defects (hallucinations, context window truncation, JSON schema validation errors, prompt injection vulnerabilities, vector retrieval bottlenecks, and rate-limit/timeout cascades). Operates a 3-tier diagnostic ladder (non-invasive observation → transient [DEBUG-PROBE] instrumentation → reproduction evaluation) with a mandatory Cleanup Gate. Product-read-only — strictly prohibited from implementing permanent code fixes."
---

# 04-llm-bugfinder — LLM Root Cause Investigation

## Trigger
Mandatorily invoked by `00-llm-orchestrator` when an LLM defect or performance degradation occurs with unknown or unverified causes (Pipeline 4a/4b). Read-only on production logic; temporary transient instrumentation is strictly governed by the Cleanup Gate.

## LLM Defect Domains
Covers the primary failure vectors of LLM and Generative AI applications:
- **Hallucinations & Ungrounded Claims**: Model answering outside retrieved RAG context, ignoring grounding constraints, or inventing fictitious facts.
- **Context Window Truncation & Drop**: Excessive retrieved chunks overflowing context bounds, silent truncation by the LLM client, or "lost-in-the-middle" attention degradation.
- **Structured Output & Schema Failures**: Pydantic validation errors caused by markdown fences (````json````), trailing commas, unescaped quotes, or hallucinated enum values.
- **Prompt Injection & Security Leaks**: Direct instruction override, indirect prompt injection embedded inside untrusted retrieved RAG chunks, or leakage of system prompt/API credentials.
- **Vector Retrieval Bottlenecks & Low Recall**: Suboptimal chunking splitting critical semantic units, embedding dimension mismatch, inappropriate distance metric, or overly restrictive metadata filters.
- **API Timeouts & Rate-Limit Cascades**: HTTP 429 rate-limiting, unhandled provider outages, lack of backoff jitter, or runaway recursive agent loops exhausting token credits.

## Workflow

### Phase 1: Symptom Capture & Subsystem Localization
**Objective**: Ingest diagnostic evidence and isolate the offending tier.

1. **Artifact Ingestion**: Collect prompt templates, raw user inputs, retrieved context chunks with similarity scores, raw unparsed model completion strings, token usage statistics, and provider HTTP error codes.
2. **Subsystem Isolation**: Pinpoint whether the fault originates in:
   - *Prompt / Assembly Tier*: Missing constraints, excessive tokens, ambiguous instructions.
   - *Retrieval / Vector Tier*: Low chunk relevance, missing documents, embedding mismatch.
   - *Gateway / Provider Tier*: Rate-limiting, connection timeouts, model availability.
   - *Parser / Schema Tier*: Pydantic validation failure, JSON syntax error.
   - *Agent / Tool Tier*: Tool execution exception, recursive loop, bad arguments.
3. **Reproduction Validation**: If reproduction conditions are missing, formulate specific diagnostic queries rather than speculating.

### Phase 2: Diagnostic Ladder & Root Cause Pinpointing
**Objective**: Traverse the 3-tier diagnostic ladder to isolate the exact prompt, query, or parsing rule causing the defect.

1. **Tier 0 (Non-Invasive Observation)**: Inspect application logs, token usage traces, vector search similarity scores, and raw model completion texts without touching source files.
2. **Tier 1 (Transient Debug Probes)**: If non-invasive methods cannot isolate intermittent issues (e.g., streaming parser errors, dynamic prompt interpolation values):
   - Insert temporary read-only probe statements tagged strictly with `# [DEBUG-PROBE]` (Python) or `// [DEBUG-PROBE]` (TS/JS).
   - Probes must only log raw prompt strings, token lengths, or unparsed LLM responses — **never alter prompt text, mutate system state, or change model parameters**.
3. **Tier 2 (Reproduction Evaluation)**: Create an isolated, reproducible test script or prompt payload reproducing the failure deterministically.
4. **Identify True Cause**: Distinguish symptoms from root causes (e.g., "Pydantic ValidationError: field 'summary' missing" is a symptom; "System prompt failed to mandate JSON output mode when calling `gpt-4o-mini`, causing it to reply in markdown bullets" is the root cause).

### Phase 3: Blast Radius Assessment
**Objective**: Determine whether the fix requires simple or complex routing.

- **Simple (Pipeline 4a)**: Localized defect in 1 prompt template, 1 Pydantic model, or 1 regex cleaner.
- **Complex (Pipeline 4b)**: Defect involving vector index re-embedding, multi-agent state graph transitions, or multi-provider fallback architecture.

### Phase 4: Mandatory Cleanup Gate & Handoff
**Objective**: Ensure 100% of temporary probe instrumentation is removed prior to handoff.

1. Search the entire codebase for `[DEBUG-PROBE]` to locate all injected probes.
2. Delete every probe statement and revert modified files to their exact pre-investigation state.
3. Run `git diff` / inspection to confirm zero residual debug probes remain (`cleanup_verified: true`).

## Output Format
Emit an investigation report:
- **Observed Symptoms & Environment**: Model name, temperature, provider, error message.
- **Offending Subsystem**: Prompt / Retrieval / Gateway / Parser / Agent.
- **Exact Root Cause**: File path, line number, offending logic/prompt, and technical rationale.
- **Blast Radius**: Simple (→ Pipeline 4a) or Complex (→ Pipeline 4b).
- **Recommended Remediation**: Architectural fix guidance (do not write fix code).
- **YAML Handoff Block**:
```yaml
handoff:
  from_skill: "04-llm-bugfinder"
  to_skill: "06-llm-test" # or "02-llm-plan" if complex
  offending_system: "Structured Outputs / Parser"
  exact_location: "src/parsers/json_parser.py:42"
  root_cause: "Model wraps JSON in markdown fences (```json ... ```) which json.loads fails to parse"
  blast_radius: "simple" # "simple" | "complex"
  recommended_fix: "Use regex to extract JSON block from markdown fences before parsing"
  cleanup_verified: true
```

## Don'ts
- Do not implement permanent fixes or refactor code — investigation only; all fixing belongs to `05-llm-fix`.
- Do not leave any `[DEBUG-PROBE]` statements in the codebase — 100% removal is mandatory.
- Do not inject probe code that mutates state, executes logic, or alters prompt instructions.
- Do not stop at surface symptoms (e.g., reporting "API returned 429" without identifying lack of exponential backoff or missing rate-limiter).
- Do not skip Blast Radius evaluation — this determines routing between Pipeline 4a and 4b.

## Quality Checklist
- [ ] Were raw prompt inputs and model completions analyzed prior to inserting transient probes?
- [ ] Were all temporary probes tagged with `[DEBUG-PROBE]` and 100% removed (Cleanup Gate passed)?
- [ ] Is the root cause isolated to an exact file, prompt template, or parsing function?
- [ ] Is the distinction between symptom and root cause clearly articulated?
- [ ] Was the blast radius accurately classified to guide orchestrator branching (4a vs 4b)?
- [ ] Is `cleanup_verified: true` present in the YAML handoff block?
