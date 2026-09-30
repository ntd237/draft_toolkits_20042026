# Evaluation Engineering (Golden Datasets & Eval Regression Gates)

Supports the "LLM Evaluation & Guardrail Assertions" layer of `06-llm-test` and the probabilistic units flagged in brainstorming/planning. Deterministic units follow standard TDD; probabilistic behavior (prompt quality, RAG faithfulness, agent trajectories) is locked in with versioned eval sets.

## Golden Dataset Management
- Golden datasets are versioned artifacts stored under the resolved test directory (e.g., `tests/golden/<feature>/`) or the project's established eval location — never scattered or edited ad hoc inside test code.
- Each case carries: input payload, expected behavior definition (exact output for deterministic cases; rubric/criteria for probabilistic ones), and provenance (where the case came from: production incident, user report, edge-case hardening).
- Grow the dataset from real failures: every `04-llm-bugfinder` root cause on probabilistic behavior contributes a regression case before the fix is accepted.
- Datasets persisting user content follow the privacy standards in `../03-llm-implement/references/llm-implementation-standards.md` (redaction, retention).

## Eval Regression Gate
- **Before merge/acceptance of any change touching prompts, retrieval parameters, or model configuration**, run the feature's golden eval set and compare against the previous recorded scores.
- A significant drop on any metric (threshold set in the plan/spec, e.g., faithfulness ≥ 0.85, answer relevance ≥ 0.80) blocks acceptance — the change routes back through `05-llm-fix`/`02-llm-plan`, not around the gate.
- Record eval scores in the handoff summary: dataset version, per-metric scores, model identifiers used. Scores without a recorded model+prompt version are not comparable and must be re-run.
- Eval runs use the pinned model version(s) declared for the comparison; mixing model versions across a comparison invalidates it.

## LLM-as-Judge Rubric Guidance
- Judges need: the rubric (criteria + scale), few-shot anchor examples per score level, and the definition of pass/fail thresholds — a bare "rate the answer 1-10" prompt is not a valid metric.
- Validate the judge itself against a small human-labeled set before trusting it; report judge agreement, not just judge scores.
- Prefer deterministic assertions where possible (format checks, keyword/leak absence, citation presence) and reserve judge metrics for genuinely subjective quality.
