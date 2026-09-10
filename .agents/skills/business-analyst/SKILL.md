---
name: business-analyst
description: Comprehensive Business Analysis (BA) and Solution Architecture skill for Web, Mobile, Game, and AI (Computer Vision, NLP/LLM, GenAI, ML). Turns high-level project concepts into execution-ready specifications — business workflows, actor use cases, Mermaid diagrams, business rules, edge cases, acceptance criteria, and system architecture. Triggers when the user describes a new project, feature, or system and needs a structured BA spec before implementation.
---

# Skill: business-analyst

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard English technical terms (entity names, status codes, Mermaid node keys).

## Trigger
User describes a project concept, feature, or system (Web, Mobile, Game, or AI/CV/LLM) and needs a structured business specification — workflows, actors, rules, edge cases, acceptance criteria, and architecture guidance — before engineering begins.

## Workflow

### Phase 1: Clarify & Detect Domain
**Objective**: Lock scope and identify which domain lenses apply before generating any specification.

- If the prompt is brief, ambiguous, or missing critical scope details, ask 2–3 targeted questions (target users, scale, deployment, key business rules). Cap at 2 rounds; if still ambiguous, proceed with best-supported interpretation.
- If the user is unavailable (autonomous execution), proceed immediately with documented assumptions recorded in Section 13.
- Identify primary and secondary domain lenses:
  - **Web**: Auth/Session, RBAC, Caching, SEO, Multi-tenancy, REST/GraphQL contracts, Rate limiting.
  - **Mobile**: Offline-first, Sync conflict, Push notifications, Background services, Permissions, Battery/Network.
  - **Game**: Core gameplay loop, Player state, Economy/Inventory, Progression, Tick rate/Physics, Multiplayer sync.
  - **Computer Vision**: Frame sampling FPS, Detection/Tracking/Segmentation, NMS/ByteTrack, ROI filtering, Edge vs Cloud inference, Hardware acceleration (TensorRT/OpenVINO/ONNX), Camera disconnect recovery, False-positive suppression, Annotation feedback loop.
  - **NLP/LLM/GenAI**: Token budgeting, Prompt/Context window, RAG pipeline (Chunking, Vector DB, Hybrid search, Rerank), Hallucination guardrails, Streaming, Tool calling/Agentic.
  - **Compliance & Privacy** (always active cross-domain): PII inventory, GDPR/PDPA consent, right-to-erasure, audit logging, data residency, role-based data access.
  - **Data/Analytics**: Event taxonomy, ETL/ELT, aggregation windows, SLA dashboards, data quality/drift.
- When 2+ lenses are detected: rank as primary (drives architecture, fills main Domain Deep Dive) and secondary (each gets own sub-section covering only what primary doesn't). When lenses conflict, record conflict and chosen resolution in Section 13.

### Phase 2: Select Depth & Generate Specification
**Objective**: Produce the specification report using the correct depth mode.

- **Lite mode** — single module, ≤ 3 actors, no cross-system integration, one clear goal. Output sections 1, 3, 8, 9 only.
- **Full mode** — ≥ 3 actors, multiple modules/integrations, stateful data lifecycle, or compliance-sensitive data. Output all 13 sections.
- State the chosen mode and reason at the top of the report. Never silently pick one.

See `references/spec-template.md` for the full 13-section and Lite 4-section output template.

### Phase 3: Self-Check Before Delivery
**Objective**: Validate the spec against structural rules before presenting.

Run the Quality Checklist below. Fix any failure, then re-check.

## Output Format
The 13-section (Full) or 4-section (Lite) Markdown specification from `references/spec-template.md`, with mode stated at the top.

## Reference Files
- `references/spec-template.md` — the full 13-section and Lite 4-section output template with all section headers and guidance.

## Don'ts
- Do not write vague instructions like "handle errors properly" or "optimize performance" — specify exact mechanisms (e.g., "3-round exponential backoff with jitter", "Filter detections with confidence < 0.6").
- Do not assume network, user input, external APIs, or camera feeds are always reliable — every feature must include explicit failure modes and edge paths.
- Do not recommend architectures exceeding required scale — no unnecessary microservices or single-use abstractions.
- Do not skip Mermaid diagrams — at least one `flowchart` or `sequenceDiagram` is required.
- Do not write acceptance criteria in any format other than Given-When-Then.

## Quality Checklist
- [ ] Every actor in Section 2 participates in at least one workflow (Section 3) or user story (Section 4)?
- [ ] Every workflow has at least one explicit edge/exception path?
- [ ] Every edge case in Section 8 maps to at least one Gherkin scenario in Section 9?
- [ ] Every state in Section 6 has defined entry triggers and exit transitions (no dead-end states)?
- [ ] Every edge case in Section 8 has a concrete fallback/retry/notification mechanism (no generic statements)?
- [ ] Every NFR in Section 10 is measurable (a number or threshold, not "fast"/"scalable"/"secure")?
- [ ] Every Must-Have in Section 11 traces to at least one user story?
- [ ] MVP slice listed explicitly in Section 11?
- [ ] Chosen mode (Full/Lite) stated with reason at the top, and only allowed sections are present?
- [ ] All assumptions made without user confirmation recorded in Section 13?
- [ ] At least one Mermaid diagram included?
