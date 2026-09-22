---
name: 02-plan
description: "Creates detailed implementation plans for complex, high-risk, or cross-layer requirements (frontend/backend/database) in the full-stack web pipeline, saving the plan artifact to docs/plans/plan-<name>.md in Vietnamese Markdown. Mandatorily halts after plan creation for user review, supplementation, and explicit approval before any execution can proceed. Decomposes work into atomic waves/behaviors for parallel TDD execution. Read/write for plan files only — does not create or modify production code."
---

# 02-plan — Multi-Tier Implementation Planning

## Trigger
Mandatorily invoked by `00-orchestrator` when: requirements span multiple tiers (frontend+backend, backend+DB, ...), alter DB schema or API contracts, impact critical business flows, or require coordinating multiple parallel work waves (Scenarios #3, #4b, #6). Receives input from `01-brainstorm` (acceptance criteria + selected approach, or `docs/specs/spec-<name>.md`) or `04-bugfinder` (root cause + blast radius).

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

### Phase 4: Mandatory Plan Review & Approval Gate
**Objective**: Present the plan to the user and mandate explicit user review, additions, and approval before proceeding.

1. Once `docs/plans/plan-<name>.md` is saved, present the plan summary and clickable file link in chat.
2. **Mandatory User Approval Gate**: Strictly pause execution and wait for the user to review, request adjustments, or supplement requirements.
3. **No execution may proceed** to wave loops, TDD cycles (`06-test`), or implementation without explicit user approval.
4. If the user requests additions or modifications, update `docs/plans/plan-<name>.md` accordingly and re-verify approval before continuing.

## Output Format
The plan file MUST be created and saved at `docs/plans/plan-<name>.md`, with its entire content written in **Vietnamese Markdown**.

The plan document structure must include:
- Tổng quan phạm vi (tầng liên quan, mức độ rủi ro, bối cảnh kỹ thuật)
- Kế hoạch rủi ro & migration (nếu có thay đổi DB schema hoặc API contract)
- Danh sách các wave thực thi (mỗi wave gồm: danh sách unit, tầng phụ trách, acceptance criteria chi tiết, phụ thuộc giữa các unit)
- Thứ tự thực thi đề xuất cho `00-orchestrator`

In chat, provide a concise summary linking to the created plan file: `docs/plans/plan-<name>.md`. **Halt execution and explicitly prompt the user to review, supplement if needed, and confirm approval before `00-orchestrator` or child skills proceed.**

## Don'ts
- Do not create, modify, or execute production code or DB migrations — scope is strictly writing the plan artifact to `docs/plans/plan-<name>.md`.
- Do not proceed to wave execution, TDD cycles (`06-test`), or implementation before the user has explicitly approved the plan.
- Do not bypass the mandatory user review/supplementation gate after saving `docs/plans/plan-<name>.md`.
- Do not save the plan outside `docs/plans/plan-<name>.md` or use an arbitrary naming convention.
- Do not write the plan artifact content in any language other than Vietnamese Markdown.
- Do not group units with cross-dependencies into the same parallel wave — this causes real-world implementation conflicts.
- Do not omit the migration/contract risk plan when DB schema or API changes are detected — this is mandatory, not optional.

## Quality Checklist
- [ ] Is the plan saved as an artifact at `docs/plans/plan-<name>.md`?
- [ ] Is the entire content of `docs/plans/plan-<name>.md` written in Vietnamese Markdown?
- [ ] Did execution pause for mandatory user review, additions, and explicit approval before any further steps?
- [ ] Is each unit in the plan small enough to run an independent TDD cycle (Red-Green-Refactor)?
- [ ] Are dependencies between units explicitly identified, with parallel waves containing no mutually dependent units?
- [ ] If DB schema or API contract changes exist, is a dedicated migration/risk plan provided?
- [ ] Are acceptance criteria for each unit concrete enough for `06-test` to write Red tests directly?
