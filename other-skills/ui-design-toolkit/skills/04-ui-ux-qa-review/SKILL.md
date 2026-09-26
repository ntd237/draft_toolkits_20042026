---
name: 04-ui-ux-qa-review
description: "Audit UI/UX against WCAG 2.1/2.2 AA accessibility standards, Nielsen usability heuristics, and responsive edge-case stability."
---

# UI/UX QA & Accessibility Review

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates when the user needs to audit UI/UX design quality, evaluate WCAG 2.2 AA accessibility compliance (color contrast, keyboard traversal, screen reader semantics), verify Nielsen's 10 usability heuristics, or stress-test Vietnamese typography and responsive layout stability before delivery.

Skip when the task involves initial brainstorming or token scaffolding before concrete layouts exist.

## Workflow

### Phase 1: Accessibility & Contrast Audit (WCAG 2.2 AA)
**Objective**: Measure and verify digital accessibility compliance against WCAG 2.2 AA standards per `references/wcag-audit-checklist.md`.

1. Measure Color Contrast Ratios:
   - Regular text (<18pt): Minimum **4.5:1** against underlying surface.
   - Large text (>=18pt or >=14pt Bold): Minimum **3.0:1**.
   - Essential UI components and icons (Input borders, status icons, focus rings): Minimum **3.0:1**.
   - Verify that color is never the sole indicator of state or error.
2. Verify Keyboard & Peripheral Operability:
   - Ensure 100% of interactive elements are reachable via `Tab` with a distinct, high-contrast focus ring (>= 2px outline).
   - Test for keyboard traps in Modals, Drawers, and Dropdowns; verify `Escape` dismisses overlays.
3. Validate Assistive Semantics:
   - Form inputs have programmatically associated `<label>` tags.
   - Images possess meaningful `alt` text or `aria-hidden="true"`.
   - Collapsible elements define `aria-expanded` and dynamic toasts utilize `aria-live="polite"`.

### Phase 2: Usability Heuristics Evaluation
**Objective**: Detect user friction points using Nielsen's 10 Usability Heuristics per `references/usability-heuristics.md`.

1. Visibility of system status: Clear loading indicators during asynchronous latency; immediate feedback on button press.
2. Error prevention and recovery: Destructive actions protected by confirmation dialogs; non-technical error messages explaining causes and offering direct recovery buttons.
3. Consistency: Uniform action colors, button alignments, icon meanings, and typography hierarchy across screens.
4. User control and freedom: Provide explicit exit paths (Cancel, Close 'X', Back button) for every interaction flow.

### Phase 3: Stress Testing & Issue Ledger
**Objective**: Execute stress tests for Vietnamese typography and viewport scaling, compiling findings into a prioritized issue ledger.

1. Vietnamese Typography Stress Test:
   - Test diacritics stacking (huyền, sắc, hỏi, ngã, nặng, mũ ă, â, ê, ô, ơ, ư) across multiple font sizes to confirm zero vertical clipping.
   - Test string expansion (+20% to 30%): Confirm buttons and titles wrap or expand without overflowing or truncating awkwardly.
2. Viewport Scaling Stress Test:
   - Verify layout stability at 320px minimum mobile width and under 200% browser text zoom.
3. Construct the Prioritized Issue Ledger:
   - **P0 - Blocker**: Critical WCAG failure or blocked primary task (mandatory fix before release).
   - **P1 - Major**: Severe friction, clipped Vietnamese tone marks, missing loading feedback (resolve in current cycle).
   - **P2 - Minor**: Spacing inconsistency, cosmetic polish (track in backlog).

## Output Format
UI/UX QA Audit Report containing:
1. Compliance Scorecard (WCAG 2.2 AA, Nielsen Heuristics, Vietnamese Typography, Responsive Stability)
2. Prioritized Issue Ledger (Issue ID -> Location -> Severity P0/P1/P2 -> Failure Description -> Concrete Fix Recommendation)
3. Final Verdict (PASS / ACTION REQUIRED)

## Don'ts
- Do not excuse color contrast failures below 4.5:1 under the guise of "artistic aesthetics".
- Do not pass an interface where interactive elements are unreachable via keyboard or controller navigation.
- Do not issue a passing verdict without explicitly verifying unclipped Vietnamese diacritical rendering.

## Quality Checklist
- [ ] Color contrast measured for each text/background pair and verified >= 4.5:1
- [ ] Confirmed absence of keyboard traps in modals and overlays
- [ ] All form inputs bound to persistent programmatic labels
- [ ] Touch targets reach at least 44x44px on touch interfaces
- [ ] Vietnamese text stress test confirms zero clipping of accent marks and zero label overflow
- [ ] Layout verified stable at 200% zoom without loss of functionality
- [ ] All P0 blocker issues resolved before sign-off
