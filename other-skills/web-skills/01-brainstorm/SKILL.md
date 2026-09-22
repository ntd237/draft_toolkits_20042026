---
name: 01-brainstorm
description: "Clarifies ambiguous requirements and analyzes architectural / tech-stack trade-offs for full-stack web features (frontend/backend/database) prior to implementation. Ensures all questions provide a custom write-in option, presents a comprehensive summary for mandatory user review and supplementation, and upon explicit approval saves the final specification to docs/specs/spec-<name>.md in Vietnamese Markdown. Triggers when 00-orchestrator routes here. Read/write for spec files only — does not create or modify production code."
---

# 01-brainstorm — Requirement Clarification & Architectural Trade-offs

## Trigger
Invoked by `00-orchestrator` when implementation requirements are ambiguous (Scenario #2) or complex / high risk (Scenario #3, prior to `02-plan`). Does not trigger automatically for bug fixes (handled by `04-bugfinder`).

## Workflow

### Phase 1: Gap Analysis & Interactive Clarification
**Objective**: Identify missing information and clarify requirements with the user.

1. Cross-examine the original request against 3 core questions: What is the business goal? Which layer has primary responsibility (frontend/backend/database/multi-tier)? What are the existing technical constraints (stack, project conventions)?
2. Formulate at most 2–3 core clarifying questions or option sets.
3. **Mandatory Write-in Option**: For every question or set of options presented, **always provide an open option for the user to input their custom or desired answer** if they disagree with the proposed suggestions (e.g., "[Custom] Write-in your own preference/answer").

### Phase 2: Trade-off Analysis
**Objective**: Propose 2–3 viable architectural / tech-stack options with explicit trade-offs.

1. For each option: state the approach, affected layers, advantages, disadvantages, and cost of change (DB schema, API contract, frontend components).
2. Always allow the user to propose an alternative or hybrid approach via an open custom option.
3. Recommend 1 preferred option with rationale, leaving the final decision to the user.

### Phase 3: Acceptance Criteria Drafting & Synthesis
**Objective**: Synthesize clarified findings and draft concrete acceptance criteria.

1. Write acceptance criteria in Given/When/Then format or as an expected behavior list, mapped to each involved layer.
2. Explicitly flag criteria that cannot be tested upfront (spikes / exploratory UI) so `00-orchestrator` can apply TDD exceptions.

### Phase 4: Mandatory Review Gate & Spec Artifact Generation
**Objective**: Summarize all findings, obtain explicit user approval/supplementation, and save the final specification artifact.

1. **Mandatory Summary & Review Gate**: After asking and resolving all clarifying questions, present a comprehensive summary of all decisions, architecture, and acceptance criteria to the user. **Strictly pause and wait for the user to review, approve, or provide additions/supplements (mandatory gate).** Do not proceed without explicit user approval.
2. If the user provides additions, feedback, or modifications, incorporate them and re-confirm with the user.
3. **Save Spec Artifact**: Only after the user explicitly approves, create and save the finalized specification to `docs/specs/spec-<name>.md` (where `<name>` is a descriptive kebab-case identifier of the task, e.g., `spec-user-auth.md`).
4. **The entire content of `docs/specs/spec-<name>.md` must be written in Vietnamese using standard Markdown.**

## Output Format
1. **Clarification Phase**: Questions/options where every question includes an open write-in option for user custom input.
2. **Review Gate Phase**: A comprehensive summary block containing:
   - Tóm tắt yêu cầu nghiệp vụ & phạm vi đã làm rõ
   - Phương án kiến trúc đã thống nhất
   - Acceptance criteria chi tiết gắn với từng tầng
   - Danh sách tiêu chí ngoại lệ TDD (nếu có)
   - **Yêu cầu bắt buộc**: Chờ người dùng duyệt và bổ sung nếu cần trước khi tạo file spec.
3. **Artifact Generation Phase**: Once approved by the user, save the complete specification to `docs/specs/spec-<name>.md` in **Vietnamese Markdown**, and provide a clickable link to `docs/specs/spec-<name>.md` in chat before `00-orchestrator` transitions to `02-plan` or `06-test`.

## Don'ts
- Do not ask questions without providing an open write-in option for the user to input their desired answer.
- Do not skip summarizing all questions or bypass the mandatory user review/supplementation gate.
- Do not create `docs/specs/spec-<name>.md` or advance to the next skill before the user has explicitly approved the summary.
- Do not write the spec artifact in any language other than Vietnamese Markdown.
- Do not save the spec file outside `docs/specs/spec-<name>.md` or use an arbitrary naming convention.
- Do not create, modify, or delete production code, migrations, or application configs — file writes are strictly restricted to `docs/specs/spec-<name>.md`.
- Do not unilaterally decide architectural directions when multiple viable options exist — always present trade-offs and wait for the user's choice.

## Quality Checklist
- [ ] Did every question presented include an open write-in option for user-provided answers?
- [ ] Was a comprehensive summary presented after all questions, pausing for mandatory user approval and additions?
- [ ] Was `docs/specs/spec-<name>.md` created only AFTER explicit user approval?
- [ ] Is the entire content of `docs/specs/spec-<name>.md` written in Vietnamese Markdown?
- [ ] Are acceptance criteria concrete enough for direct Red test authoring?
- [ ] Were zero production code or migration files created or modified?
