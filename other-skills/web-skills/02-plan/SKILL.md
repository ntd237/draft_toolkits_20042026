---
name: 02-plan
description: "Creates detailed implementation plans for complex, high-risk, or cross-layer requirements (frontend/backend/database) in the full-stack web pipeline, saving the plan artifact to docs/plans/plan-<name>.md in Vietnamese Markdown. Triggers when 00-orchestrator identifies that a requirement (implementation or bug fix) is complex enough to mandate planning — following 01-brainstorm or 04-bugfinder. Decomposes work into atomic waves/behaviors for parallel TDD execution. Read/write for plan files only — does not create or modify production code."
---

# 02-plan — Multi-Tier Implementation Planning

## Trigger
Mandatorily invoked by `00-orchestrator` when: requirements span multiple tiers (frontend+backend, backend+DB, ...), alter DB schema or API contracts, impact critical business flows, or require coordinating multiple parallel work waves (Scenarios #3, #4b, #6). Receives input from `01-brainstorm` (acceptance criteria + selected approach) or `04-bugfinder` (root cause + blast radius).

## Workflow

### Phase 1: Task Decomposition
**Objective**: Break down requirements into atomic behavior units, each small enough to run an independent TDD cycle.

1. For implementations: partition along natural layer boundaries (e.g., "API endpoint returning data" is 1 unit in backend; "component rendering data" is 1 unit in frontend) and business behaviors, rather than arbitrary granular technical files.
2. For complex bug fixes: partition by distinct root causes identified by `04-bugfinder`.
3. Identify dependencies between units (e.g., frontend unit depends on whether backend API already exists) to group them into waves — independent units share a wave to run in parallel.

### Phase 2: Risk & Migration Planning
**Objective**: Establish dedicated planning for high-risk changes (DB schema, API contracts).

1. If schema changes occur: define safe migration sequencing (backward-compatible first, cleanup later), including rollback plans.
2. If API contract changes occur: identify whether breaking changes exist, whether versioning is required, and who the affected consumers are (internal frontend, third parties).

### Phase 3: Wave Sequencing & Plan Artifact Generation
**Objective**: Output the final execution sequence and save the complete plan artifact to `docs/plans/plan-<name>.md`.

1. List waves in sequential order, each containing: unit list + involved layers + specific acceptance criteria per unit.
2. Clearly mark waves that must complete prior to subsequent waves (due to dependencies) versus waves that can run in parallel.
3. Save the generated plan file to `docs/plans/plan-<name>.md` (where `<name>` is a descriptive kebab-case identifier of the feature or bug, e.g., `plan-auth-flow.md`).
4. **The entire content of the plan file in `docs/plans/plan-<name>.md` must be written in Vietnamese using standard Markdown.**

## Output Format
The plan file MUST be created and saved at `docs/plans/plan-<name>.md`, with its entire content written in **Vietnamese Markdown**.

The plan document structure must include:
- Tổng quan phạm vi (tầng liên quan, mức độ rủi ro, bối cảnh kỹ thuật)
- Kế hoạch rủi ro & migration (nếu có thay đổi DB schema hoặc API contract)
- Danh sách các wave thực thi (mỗi wave gồm: danh sách unit, tầng phụ trách, acceptance criteria chi tiết, phụ thuộc giữa các unit)
- Thứ tự thực thi đề xuất cho `00-orchestrator`

In chat, provide a concise summary linking to the created plan file: `docs/plans/plan-<name>.md`, followed by an explicit request for user approval before `00-orchestrator` begins wave-by-wave TDD loops.

## Don'ts
- Do not create, modify, or execute production code or DB migrations — scope is strictly writing the plan artifact to `docs/plans/plan-<name>.md`.
- Do not save the plan outside `docs/plans/plan-<name>.md` or use an arbitrary naming convention.
- Do not write the plan artifact content in any language other than Vietnamese Markdown.
- Do not group units with cross-dependencies into the same parallel wave — this causes real-world implementation conflicts.
- Do not omit the migration/contract risk plan when DB schema or API changes are detected — this is mandatory, not optional.

## Quality Checklist
- [ ] Is the plan saved as an artifact at `docs/plans/plan-<name>.md`?
- [ ] Is the entire content of `docs/plans/plan-<name>.md` written in Vietnamese Markdown?
- [ ] Is each unit in the plan small enough to run an independent TDD cycle (Red-Green-Refactor)?
- [ ] Are dependencies between units explicitly identified, with parallel waves containing no mutually dependent units?
- [ ] If DB schema or API contract changes exist, is a dedicated migration/risk plan provided?
- [ ] Are acceptance criteria for each unit concrete enough for `06-test` to write Red tests directly?
