---
name: 01-brainstorm
description: "Clarifies ambiguous requirements and analyzes architectural / tech-stack trade-offs for full-stack web features (frontend/backend/database) prior to implementation. Triggers when 00-orchestrator routes here (requirements lack acceptance criteria, responsible layer is unclear, or multiple architectural options exist). Read-only — analyzes and proposes only, does not create/modify code files or execute migrations."
---

# 01-brainstorm — Requirement Clarification & Architectural Trade-offs

## Trigger
Invoked by `00-orchestrator` when implementation requirements are ambiguous (Scenario #2) or complex / high risk (Scenario #3, prior to `02-plan`). Does not trigger automatically for bug fixes (handled by `04-bugfinder`).

## Workflow

### Phase 1: Gap Analysis
**Objective**: Accurately identify missing information required to specify acceptance criteria.

1. Cross-examine the original request against 3 questions: What is the business goal? Which layer has primary responsibility (frontend/backend/database/multi-tier)? What are the existing technical constraints (stack, project conventions)?
2. Enumerate at most 2–3 core ambiguities — avoid scattered questions over minor details.

### Phase 2: Trade-off Analysis
**Objective**: Propose 2–3 viable architectural / tech-stack options with explicit trade-offs.

1. For each option: state the approach, affected layers, advantages, disadvantages, and cost of change (DB schema, API contract, frontend components).
2. Recommend 1 preferred option with rationale, leaving the final decision to the user.

### Phase 3: Acceptance Criteria Drafting
**Objective**: Translate clarified findings into concrete acceptance criteria sufficient for `06-test` to author Red tests.

1. Write acceptance criteria in Given/When/Then format or as an expected behavior list, mapped to each involved layer.
2. Explicitly flag criteria that cannot be tested upfront (spikes / exploratory UI) so `00-orchestrator` can apply TDD exceptions.

## Output Format
A summary block containing: Clarified ambiguities → Architectural options (comparison table if ≥2 options) → Recommendation → Acceptance criteria (list, mapped to layers) → Notes on criteria requiring TDD exceptions. Conclude with an approval request before transitioning to `02-plan` or `06-test`.

## Don'ts
- Do not create, modify, or delete code files, migrations, or configs — analyze and propose via text only.
- Do not make architectural decisions on behalf of the user when multiple viable options exist — always present trade-offs and await a decision.
- Do not write detailed implementation code (that is the responsibility of `03-implement`) — describe approaches at the architectural level only.

## Quality Checklist
- [ ] Has the primary responsible layer for the request been clearly identified?
- [ ] Are at least 2 architectural options compared when multiple viable paths exist?
- [ ] Are acceptance criteria concrete enough for direct Red test authoring without remaining ambiguities?
- [ ] Are items requiring TDD exceptions clearly flagged (if any)?
- [ ] Were zero code or migration files created or modified during this process?
