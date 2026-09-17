---
name: computer-use
description: "Automate and control desktop computers via an end-to-end observation-action-verification loop: screen capture, GUI element detection, coordinate mapping, and safe mouse/keyboard execution with failsafe mechanisms. Activates when interacting with desktop/OS interfaces, clicking buttons, filling software forms, automating GUI workflows, or triggered by keywords: computer-use, desktop-automation, gui-control, mouse-click, screen-capture."
---

# Computer Use Skill

Automates desktop computer control through an observation-action-verification loop, combining high-speed screen capture, accurate coordinate mapping, and failsafe-guarded mouse and keyboard execution.

All system parameters, directory paths, safety policies, and validation rules strictly follow [config.md](config.md).

## Trigger
Activates when the user requests GUI desktop interaction, clicking specific buttons or UI controls, typing text into desktop software, capturing screenshots for interaction, or whenever the following keywords appear: `computer-use`, `desktop-automation`, `gui-control`, `mouse-click`, `screen-capture`, `os-automation`.

## Workflow

```
[Phase 1: Observe] ──> [Phase 2: Analyze & Map] ──> [Phase 3: Execute] ──> [Phase 4: Verify]
       ▲                                                                            │
       └──────────────────────── (Retry if UI not updated) ─────────────────────────┘
```

### Phase 1: Observation & Screen Capture
**Objective**: Capture current screen state and extract display geometry, monitor index, and scale factor for visual grounding.

1. Initialize configuration and activate Per-Monitor DPI Awareness via [scripts/config_loader.py](scripts/config_loader.py) to prevent coordinate drift.
2. Query active monitor geometry:
   `python scripts/controller.py info`
3. Capture the current display state and save to the output directory defined in `config.md`:
   `python scripts/controller.py screen --monitor 1 --step <step_id> --resize 1920`
4. Parse the output JSON to record `file_path`, `original_width`, `original_height`, and `scale_factor`.

### Phase 2: GUI Analysis & Coordinate Mapping
**Objective**: Detect target UI elements from the screenshot and transform normalized coordinates to global physical/logical pixel coordinates.

1. Locate the target UI element (button, input field, menu item, icon) on the captured image.
2. Extract the bounding box `[x1, y1, x2, y2]` and calculate geometric center coordinates per [references/coordinates-and-display.md](references/coordinates-and-display.md):
   - $x_{\text{center}} = \lfloor (x_1 + x_2) / 2 \rfloor$
   - $y_{\text{center}} = \lfloor (y_1 + y_2) / 2 \rfloor$
3. Adjust for image resizing and multi-monitor display offsets:
   - $x_{\text{pixel}} = \lfloor x_{\text{center}} / \text{scale\_factor} \rfloor + \text{monitor\_left}$
   - $y_{\text{pixel}} = \lfloor y_{\text{center}} / \text{scale\_factor} \rfloor + \text{monitor\_top}$
4. Validate that calculated coordinates reside within target monitor boundaries before passing to execution.

### Phase 3: Action Execution with Safety Guardrails
**Objective**: Dispatch mouse or keyboard events to the operating system guarded by emergency failsafe and human confirmation gates.

1. Evaluate the Destructive Actions Gate per [references/safety-and-failsafe.md](references/safety-and-failsafe.md):
   - For high-risk operations (permanent file deletion, format, payment submission, UAC/sudo elevation, external dispatch): **HALT IMMEDIATELY** and request explicit confirmation from the user.
2. For mouse actions (click, double click, right click, drag, scroll):
   - Apply natural easing and safe move duration:
     `python scripts/controller.py click --x <x> --y <y> --button left`
3. For text entry and keyboard commands:
   - Use standard typing for short ASCII text:
     `python scripts/controller.py type --text "<content>" --interval 0.05`
   - Use clipboard paste for multi-line, special symbols, or Unicode text:
     `python scripts/controller.py paste --text "<unicode_content>"`
   - Use key combinations for navigation:
     `python scripts/controller.py hotkey --keys "ctrl,s"`
4. In case of emergency or unexpected cursor behavior, moving the cursor to any screen corner triggers `failsafe_aborted`.

### Phase 4: Feedback Verification & Error Recovery
**Objective**: Capture post-action screenshot, verify that UI state transitioned as expected, and handle recovery if needed.

1. Wait for UI repaint (minimum 0.5s pause).
2. Capture a verification screenshot labeled `<step_id>_verify`.
3. Visually compare pre-action and post-action states:
   - Did the target dialog open?
   - Did the text field acquire cursor focus?
   - Did the application view update?
4. If the state did not change, retry up to 3 times with exponential backoff `[1.0s, 2.0s, 3.0s]`.
5. If state remains unchanged after 3 attempts, halt execution and report diagnostic details with screenshots for user intervention.

## Output Format

### 1. Step Action Log
For every execution cycle, output a structured summary:
- **Step**: `[Step Name / Step ID]`
- **Action**: `click | double_click | type | paste | hotkey | scroll`
- **Target Coordinates**: `(x, y)` and target UI element description
- **Artifacts**: Relative file paths to pre-action and post-action screenshots
- **Status**: `SUCCESS | RETRY | BLOCKED_BY_CONFIRMATION_GATE | FAILSAFE_ABORTED`

### 2. File Artifacts
- Screenshots stored under `docs/computer_use/screenshots/`.
- Session execution logs stored under `docs/computer_use/logs/session_<timestamp>.jsonl`.

## Don'ts
- Do not perform blind clicking without analyzing a freshly captured screenshot.
- Do not bypass DPI scaling awareness; uncompensated coordinates will miss targets on High-DPI screens.
- Do not execute destructive actions (Shift+Delete, rm -rf, format, financial submission, Admin privilege grants) without explicit user confirmation.
- Do not type complex Unicode or multi-byte text directly with `pyautogui.write()`; use clipboard paste instead.
- Do not disable `FAILSAFE_ENABLED` under any circumstances.
- Do not hardcode absolute paths; use relative paths resolved from workspace and skill roots.

## Quality Checklist
- [ ] `config.md` exists and defines all 5 policies (File System, Naming, Runtime, Validation, Workflow) using relative paths.
- [ ] `references/coordinates-and-display.md` documents absolute/normalized coordinates, DPI scaling, and multi-monitor offsets.
- [ ] `references/safety-and-failsafe.md` documents emergency failsafe triggers, human-in-the-loop gates, and natural pacing.
- [ ] `scripts/` contains modular scripts (`config_loader.py`, `screen.py`, `mouse.py`, `keyboard.py`, `controller.py`).
- [ ] Per-Monitor DPI Awareness is automatically initialized before coordinate calculations.
- [ ] Unicode text entry uses safe clipboard paste mechanisms.
- [ ] PyAutoGUI `FailSafeException` is handled gracefully in all script entry points.
- [ ] `SKILL.md` is under 300 lines with zero extraneous boilerplate.
