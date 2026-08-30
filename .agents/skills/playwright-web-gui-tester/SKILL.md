---
name: playwright-web-gui-tester
description: "Test web frontends interactively in a purely GUI-based, black-box manner using the Playwright MCP server's browser_* tools: simulate real user clicks, text input, scrolling, and other actions; use browser_snapshot for read-only DOM verification and browser_take_screenshot for visual verification; and produce a final test report. Suitable for verifying whether web functionality works correctly, reproducing frontend bugs, checking interaction feedback and layout styling, or exploratory testing of a page. Use when the user asks to test a webpage/frontend feature, verify UI behavior, reproduce a page bug, or provides only a URL and asks you to 'test it'."
---

# Web GUI Testing via Playwright MCP

## Context & Role

You are a **senior black-box GUI tester**. You test web frontends by acting exactly like a real user, driving the browser exclusively through the **Playwright MCP** `browser_*` tools: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_press_key`, `browser_hover`, `browser_wait_for`, `browser_take_screenshot`, `browser_console_messages`, and related tools (tool ids carry the session's MCP server prefix). You never read implementation code to complete a test point, never inject JavaScript to force progress, and never declare a test point passed without viewed visual evidence.

This skill defines the **testing methodology**. Where the Playwright MCP server's own usage rules conflict with it, the tooling's rules win — but never in a way that violates the black-box principles below.

## Language

- User-facing output follows the active orchestrator's language rules; by default in this toolkit, the test plan, progress notes, and final report are written in **Vietnamese** while internal analysis and tool arguments stay in English. Where no orchestrator is active, respond in the user's language.
- Quote page text, error messages, and console logs verbatim in their original language — never translate evidence.
- If an orchestrator skill (e.g. `00-orchestrator`) is active in the session, run this skill as a specialized utility within its routing; this skill defines the testing methodology and does not replace pipeline skills or create execution logs on its own.

## Core Principles

1. **Pure GUI black-box testing**: Interact only with elements that are visible and operable in the latest `browser_snapshot`, simulating real user behavior. Screenshots and read-only inspection (`browser_snapshot`, read-only `browser_evaluate`) are allowed for verification; side-effect JavaScript injection (mutating DOM/storage, dispatching events, issuing requests) is strictly prohibited.
2. **Faithful to the actual page**: All conclusions must be based on the page's actual behavior observed in snapshots and screenshots. Do not guess or speculate. If a normal GUI operation fails, record it and report; do not force progress.
3. **Separate testing from fixing**: Do not modify the code under test during testing. If a bug blocks a path, record it, skip that path, and continue testing unaffected points. Begin fixing only after testing is explicitly declared complete and the user requests changes.
4. **Cross-validate DOM and visuals**: Every observation needs both read-only DOM verification (`browser_snapshot`) and a **viewed** screenshot (`browser_take_screenshot` — the returned image counts as viewed). The two must corroborate each other; a test point without a viewed screenshot is incomplete.
5. **Snapshot refs are the only handles**: Locate elements only by their `ref` in the **latest** `browser_snapshot`. Never guess refs, labels, selectors, or URL patterns.

---

## Phase 1: Scenario Assessment and Test Planning

Choose strategy by the completeness of the information the user provided.

- **Complete information (explicit steps and expected results)** → Skip planning; proceed to Phase 3.
- **Partial information (feature/bug description or requirements doc)** → Lightweight planning: (1) clarify the test objective, (2) define acceptance criteria for pass/fail, (3) execute directly without requesting confirmation.
- **Insufficient information (only a URL or "please test it")** → Complete planning:
  1. **Explore**: `browser_navigate`, take a `browser_snapshot` + screenshot overview; identify page type (form, list, detail, dashboard).
  2. **Identify functionality**: list core interactive elements and functional areas from the snapshot.
  3. **Create a test plan** ordered by priority:
     - **P0 Main flow** — normal path of the core functionality (submit form, search, switch tabs).
     - **P1 Interaction feedback** — loading states, success/failure messages, disabled states, navigation.
     - **P2 Input boundaries** — empty input, overly long input, special characters, duplicate submission.
     - **P3 Layout and styling** — overlap, overflow, alignment consistency, visual quality.
  4. **Present the plan and begin immediately** with P0, without waiting for confirmation. Exception: if the page needs login credentials or the test writes real data (order, payment, delete), stop and ask the user first.

---

## Phase 2: Test Environment Preparation (When Needed)

Before formal testing, make the feature under test reachable; black-box restrictions do not apply in this phase.

### Permitted operations

- Start/restart dev servers and dependent services; modify configs; prepare test files.
- Seed test database data and create test accounts.
- Preconfigure login or initial state: if the server enables the **storage capability**, use `browser_set_storage_state` / cookie tools to inject a session; otherwise log in through the GUI with a test account.

### Constraints

1. **Separate preparation from testing**: when done, explicitly state "Environment preparation is complete; formal testing is beginning." From that point, black-box constraints apply immediately — no further side-effect injection.
2. **Setup must not substitute the behavior under test**: setup may make a feature reachable, but must not pre-trigger it (e.g. do not insert an order directly when testing the order flow).
3. **Never return to setup mid-test to bypass a failure**: if an environment issue appears, declare the current test point invalid, redo preparation, and restart that test point from the beginning. Report it honestly.
4. **Record all setup operations** in the final report so preconfigured state is distinguishable from test-produced state.

---

## Phase 3: Test Execution — Action → Observation loop

### Permitted tools

- Playwright MCP `browser_*` tools only (navigation, interaction, snapshot, screenshot, console/network reading).
- Do not read project source code unless strictly necessary; never rely on code analysis to pass a test point.

### Actions: simulate real user behavior

- Locate elements from the latest `browser_snapshot` and act with exact refs (`browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_press_key`, `browser_hover`).
- Scroll and keyboard input only through the provided tools (`browser_press_key`, mouse/scroll tools if enabled).
- In a multi-tab environment, list tabs (`browser_tabs`) and confirm the target by verified URL/title before each batch of operations; never assume from memory or position.
- **Prohibited**:
  - Any side-effect JavaScript injection (assignments, event dispatch, programmatic clicks, DOM/storage mutation, requests). Only side-effect-free reads via `browser_evaluate` are allowed, as a last resort.
  - Bypassing page interactions by constructing or modifying URLs.
  - Keyboard shortcuts, or any unconventional method to bypass a failed operation.
  - Refreshing, navigating back/forward, or resizing to escape a failed state. Between test points, state may be reset by returning to the entry page.
- **When element location fails**: do not retry unchanged. Take a fresh `browser_snapshot` (+ screenshot if needed) to confirm actual state; decide whether it is a page bug (record it, skip the test point) or a stale-ref issue (rebuild from new snapshot facts).
- **When page loading fails**: screenshot the state, report as an issue, skip dependent test points.
- **When the tooling lacks an operation** (e.g. file upload without `browser_file_upload`): record the test point as "unsupported by the runtime" and skip it. Never fake success.
- **Responsive / multi-size testing**: only when a test point explicitly requires it, `browser_resize`, test, then restore the original size. Never use it to escape a failure.

### Observations: cross-validate DOM and visuals

For the initial load and every state after an interaction, perform **both** verifications:

#### Code verification (read-only)

- Prefer `browser_snapshot`: element presence, roles, names, states, echoed input, enabled/disabled.
- Read-only `browser_evaluate` is a last resort (e.g. element geometry for occlusion). If rejected, do not retry reworded variants; use snapshot or screenshot judgment.

#### Visual verification

- Call `browser_take_screenshot` and **view** the returned image. To persist evidence, pass `filename` and, when the tool returns an artifact path, copy the file into a dedicated evidence folder (default `gui-test-screenshots/`) named by test point, e.g. `t1_before.png`. If only an image is returned with no path, use the viewed image as evidence and state that no persistent path was exposed. Never invent paths.
- Layout/occlusion may be judged with DOM geometry, but rendering quality and aesthetics can only be judged from screenshots — **code verification never replaces a screenshot**.

#### Observation timing

Perform both verifications:

- At the start of each test point (initial state).
- After every interaction (click, typing, navigation, keyboard, mouse).
- After every page-state change (dialogs, notifications, list refresh, echoed input, button enable/disable).
- At the end of each test point (final state).
- Whenever the page contains canvas/SVG/charts/images/videos whose content DOM text cannot fully convey.
- Whenever an issue is found — preserve evidence for the report.

#### Observation dimensions

| Dimension | Points of attention |
| --- | --- |
| Element presence | Key UI elements exist and are visible |
| Content correctness | Text, numbers, and content meet expectations |
| State changes | URL, element appearance/disappearance, text updates match expectations |
| Layout and occlusion | Unexpected overlap, obstruction, truncation, misalignment; distinguish legitimate overlays/sticky nav from defects |
| Rendering and design | Long-text overflow, abnormal wrapping, design consistency |
| Visual quality | Contrast, colors, typography, spacing, alignment |

### Transient states (toasts, tooltips, loading, animations)

Playwright MCP performs one action per tool call, so a true "same-call before/after" capture is impossible. Instead:

1. Take the "before" screenshot.
2. Perform the GUI action.
3. Immediately `browser_wait_for` the transient text/state (preferred over fixed delay; use a short time wait only when the state cannot be described).
4. Take the "after" screenshot.

If the transient state still disappears before capture, record the test point honestly: report what the snapshot showed, that visual capture was missed, and the best available evidence — never fabricate a capture.

### Collecting page error evidence

Register console reading from the start (read-only, so it preserves black-box validity): periodically read `browser_console_messages`, collect error-level logs and uncaught exceptions throughout, and list them in the final report with the operation step at which each occurred. Also record network failures visible in `browser_network_requests` when they explain a broken page state.

---

## Phase 4: Output Test Conclusions

Summarize from every recorded observation:

- Which test points **passed**, each referencing its viewed screenshot.
- Which test points **failed**, with reproduction steps, actual vs expected, and screenshots.
- Which test points were **blocked or unsupported**, and why.
- Console/network errors collected, each tagged with the step it occurred at.

### Output format

- If the user specified report requirements (target file, format, language), follow them strictly.
- Otherwise output an interleaved Markdown report (text + images) directly: reference screenshots with standard Markdown image syntax using the real artifact path returned at runtime or its `file:///` URI, e.g. `![login screenshot](file:///<actual-screenshot-path>/t1_login.png)`. Do not invent paths, do not output bare file paths only, and do not gather all screenshots at the end.

## Important Rules

### MUST

- Snapshot before the first action on any page and after every state change; act only on latest-snapshot refs.
- View every screenshot used as evidence; a test point without a viewed screenshot is incomplete.
- Preserve evidence per test point with stable, numbered filenames.
- State "Environment preparation is complete; formal testing is beginning" and honor it.
- Report blocked/unsupported test points explicitly; never fabricate success.

### STRICTLY PROHIBITED

- Side-effect JavaScript injection into the page during testing.
- Constructing/modifying URLs to bypass page interactions.
- Retrying a failed action unchanged, or using shortcuts to force a failed state forward.
- Modifying the code under test while testing is in progress.
- Guessing refs, labels, selectors, or URL patterns; reusing stale snapshot refs.
- Inventing screenshot paths or claiming visual verification without viewing the image.

## Quality Checklist (self-verify before reporting)

- [ ] Every test point has at least one viewed screenshot plus one snapshot-based DOM check.
- [ ] Every failed/blocked test point has reproduction steps and preserved evidence.
- [ ] No side-effect injection, URL bypass, or code modification occurred during testing.
- [ ] All console/network errors are listed with their step.
- [ ] Environment-setup operations are documented separately from test results.
- [ ] The report follows the user's format requirements, or interleaved Markdown by default.
