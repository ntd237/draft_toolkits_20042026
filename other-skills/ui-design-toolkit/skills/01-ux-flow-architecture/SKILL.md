---
name: 01-ux-flow-architecture
description: "Define user journeys, task flows with error/recovery paths, information architecture, navigation trees, and ethical UX wireframes."
---

# UX Flow & Information Architecture

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs persona definition, user journeys, information architecture (IA/sitemap), task flows with comprehensive error handling, structural wireframing, or ethical consent UX patterns.

Skip when the task involves styling existing layouts, picking color palettes, or polishing visual typography.

## Workflow

### Phase 1: User Context & Information Architecture
**Objective**: Establish primary user personas, core jobs-to-be-done (JTBD), and map the hierarchical information architecture.

1. Define primary user personas and their highest-priority task (Core Job-to-be-Done).
2. Structure the Information Architecture (IA):
   - Categorize screens into 3 depth levels: Level 1 (Global/Tab Nav) → Level 2 (Section/List Views) → Level 3 (Detail/Action Modals).
   - Ensure the user reaches primary actions in at most 3 interactions.
3. Map device-appropriate navigation models (Bottom tab bar for mobile, persistent sidebar for web/desktop, hub-menu for games).

### Phase 2: Task Flows & Edge-Case Mapping
**Objective**: Engineer end-to-end task flows from trigger to resolution, explicitly defining error and recovery paths.

1. Map step-by-step task flows for critical paths (Onboarding, Search/Filter, Form completion, Checkout, Settings).
2. Construct the error-response matrix following `references/user-flows-patterns.md`:
   - Validation failures: Highlight input inline without clearing entered user values.
   - Network / Server errors: Preserve form state, surface friendly notification with a direct "Retry" action.
   - Zero / Empty states: Provide helpful illustration, explanatory text, and a primary creation CTA.
3. Audit UX ethics following `references/ethical-consent-ux.md`: Verify absence of deceptive patterns (pre-ticked boxes, hidden cancellation, manipulative copy).

### Phase 3: Structural Wireframing
**Objective**: Generate low-to-mid fidelity structural wireframe layouts (ASCII/text-based) defining spatial hierarchy.

1. Draft wireframes for core screens, establishing clear zones: Global Navigation, Main Content Canvas, Primary Actions (CTA), and Feedback areas.
2. Position interaction anchors: Safe zone offsets for Game HUDs or bottom Thumb-zone positioning for Mobile Apps.
3. Package structural specifications for handoff to `02-ui-design-system` and `03-ui-platform-responsive`.

## Output Format
Markdown document containing:
1. Information Architecture Sitemap tree
2. Step-by-Step Task Flow Table (Step -> User Action -> System State -> Error/Recovery Path)
3. Structural ASCII Wireframes for primary views

## Don'ts
- Do not produce happy-path flows without defining corresponding error, network loss, and empty recovery states.
- Do not exceed 3 levels of navigation hierarchy without providing direct shortcut mechanisms.
- Do not introduce dark patterns (confirmshaming, roach motels, hidden fees, pre-checked opt-ins).

## Quality Checklist
- [ ] Core persona and primary JTBD identified
- [ ] Information Architecture depth bounded to <= 3 levels
- [ ] Every critical user flow includes explicit error states and recovery paths
- [ ] Empty/Zero state defined with guidance and creation action
- [ ] Anti-dark-patterns audit completed and confirmed compliant
