---
name: computer-use
description: "Automate and control desktop computers via an end-to-end observation-action-verification loop: screen capture, GUI element detection, coordinate mapping, and safe mouse/keyboard execution with failsafe mechanisms. Activates when interacting with desktop/OS interfaces, clicking buttons, filling software forms, automating GUI workflows, or triggered by keywords: computer-use, desktop-automation, gui-control, mouse-click, screen-capture."
---

# Computer Use Skill

Automates desktop computer control through an observation-action-verification loop, combining high-speed native Win32 screen capture, accurate coordinate mapping with visual grid overlays, failsafe-guarded mouse/keyboard execution, and automated visual diff verification.

All system parameters, directory paths, safety policies, and validation rules strictly follow [config.md](config.md).

## Trigger
Activates when the user requests GUI desktop interaction, clicking specific buttons or UI controls, typing text into desktop software, capturing screenshots for interaction, or whenever the following keywords appear: `computer-use`, `desktop-automation`, `gui-control`, `mouse-click`, `screen-capture`, `os-automation`.

## Workflow

```
[Phase 1: Observe] ──> [Phase 2: Analyze & Ground] ──> [Phase 3: Execute & Guard] ──> [Phase 4: Verify & Diff]
       ▲                                                                                            │
       └────────────────────────────── (Retry if UI not updated) ───────────────────────────────────┘
```

### Phase 1: Observation & Screen Capture
**Objective**: Capture current screen state or active window, extracting display geometry, monitor layout, and scale factor.

1. Initialize configuration and activate Per-Monitor DPI Awareness via [scripts/config_loader.py](scripts/config_loader.py) to prevent coordinate drift.
2. Query active monitor geometry and foreground window:
   `python scripts/controller.py info`
3. Capture the current display state or specific window:
   - Full monitor capture:
     `python scripts/controller.py screen --monitor 1 --step <step_id> --resize 1920`
   - Active window capture by HWND:
     `python scripts/controller.py screen --window-hwnd <hwnd> --step <step_id>`
4. Parse the output JSON to record `file_path`, `original_width`, `original_height`, `scale_factor`, `monitor_left`, and `monitor_top`.

### Phase 2: GUI Analysis & Coordinate Grounding
**Objective**: Detect target UI elements accurately using visual grid overlays and transform normalized coordinates to global desktop coordinates.

1. If target elements are small or ambiguous, generate a Coordinate Grid Overlay image:
   `python scripts/controller.py overlay --input <screen_path> --output <overlay_path> --step 100`
2. Extract element bounding box center or normalized coordinates `[norm_x, norm_y]` on a 1000-point scale.
3. Automatically map normalized coordinates to physical desktop pixel coordinates:
   `python scripts/controller.py map --norm-x <x> --norm-y <y> --width <orig_w> --height <orig_h> --scale-factor <scale_factor> --monitor-left <left> --monitor-top <top>`
4. Validate that output coordinates reside within valid target monitor boundaries before dispatch.

### Phase 3: Action Execution with Safety Guardrails
**Objective**: Dispatch mouse or keyboard events guarded by Multi-Monitor Failsafe, Focus Guard, and Human Confirmation gates.

1. Evaluate the Destructive Actions Gate per [references/safety-and-failsafe.md](references/safety-and-failsafe.md):
   - For high-risk operations (permanent file deletion, format, payment submission, UAC/sudo elevation, external dispatch): **HALT IMMEDIATELY** and request explicit confirmation from the user.
2. Verify Foreground Window Focus to prevent typing or clicking into unintended popup windows:
   `python scripts/controller.py window --check "<Expected_Title>"`
3. For mouse actions (click, move, drag, scroll):
   - Click:
     `python scripts/controller.py click --x <x> --y <y> --button left`
   - Drag and drop:
     `python scripts/controller.py drag --start-x <x1> --start-y <y1> --end-x <x2> --end-y <y2> --duration 0.5`
   - Scroll at target coordinates:
     `python scripts/controller.py scroll --clicks -3 --x <x> --y <y>`
4. For text entry and keyboard commands:
   - Use standard typing for short ASCII text:
     `python scripts/controller.py type --text "<content>" --interval 0.05`
   - Use safe clipboard paste for Unicode/Vietnamese text (automatically backs up and restores previous clipboard):
     `python scripts/controller.py paste --text "<unicode_content>"`
   - Use keyboard shortcuts:
     `python scripts/controller.py hotkey --keys "ctrl,s"`
5. Emergency Multi-Monitor Failsafe: Moving the cursor to any corner of ANY connected monitor immediately triggers `FailSafeTriggered` and releases all pressed inputs.

### Phase 4: Feedback Verification & Error Recovery
**Objective**: Capture post-action screenshot, measure visual diff change ratio, and handle automated retry/backoff if UI has not updated.

1. Wait for UI repaint (minimum 0.5s pause).
2. Capture a verification screenshot labeled `<step_id>_verify`.
3. Compute visual diff between pre-action and post-action screenshots:
   `python scripts/controller.py diff --img1 <pre_path> --img2 <verify_path> --output <diff_path> --threshold 0.01`
4. Inspect diff output:
   - If `has_changed` is `True` and expected dialog/element appeared: proceed to next step.
   - If `has_changed` is `False` (UI did not transition): retry up to 3 times with exponential backoff `[1.0s, 2.0s, 3.0s]`.
5. If state remains unchanged after 3 attempts, halt execution and report diagnostic details with visual diff artifacts for user intervention.

## Output Format

### 1. Step Action Log
For every execution cycle, output a structured summary:
- **Step**: `[Step Name / Step ID]`
- **Action**: `click | drag | type | paste | hotkey | scroll`
- **Target Coordinates**: `(x, y)` and target UI element description
- **Artifacts**: Relative paths to pre-action, post-action, and visual diff screenshots
- **Change Ratio**: Percentage of changed pixels measured by Visual Diff
- **Status**: `SUCCESS | RETRY | BLOCKED_BY_CONFIRMATION_GATE | FAILSAFE_ABORTED`

### 2. File Artifacts
- Screenshots stored under `docs/computer_use/screenshots/`.
- Visual diffs stored under `docs/computer_use/screenshots/diff_*.png`.
- Session execution logs stored under `docs/computer_use/logs/session_<timestamp>.jsonl`.

## Don'ts
- Do not perform blind clicking without analyzing a freshly captured screenshot.
- Do not bypass DPI scaling awareness; uncompensated coordinates will miss targets on High-DPI screens.
- Do not execute destructive actions (Shift+Delete, rm -rf, format, financial submission, Admin privilege grants) without explicit user confirmation.
- Do not type complex Unicode or Vietnamese text with direct typing; use `controller.py paste` to prevent IME corruption.
- Do not disable `FAILSAFE_ENABLED` under any circumstances.
- Do not hardcode absolute paths; use relative paths resolved from workspace and skill roots.

## Quality Checklist
- [ ] `config.md` exists and defines all 5 policies (File System, Naming, Runtime, Validation, Workflow) using relative paths.
- [ ] `references/coordinates-and-display.md` documents absolute/normalized coordinates, DPI scaling, and multi-monitor offsets.
- [ ] `references/safety-and-failsafe.md` documents multi-monitor failsafe triggers, human-in-the-loop gates, and natural pacing.
- [ ] `scripts/` contains complete modular zero-dependency scripts (`config_loader.py`, `screen.py`, `mouse.py`, `keyboard.py`, `grounding_helper.py`, `visual_diff.py`, `window_manager.py`, `controller.py`).
- [ ] `tests/` contains automated unit tests covering all modules with 100% pass rate.
- [ ] Multi-Monitor Failsafe checks 4 corners across all connected displays in Virtual Desktop.
- [ ] Unicode text entry uses safe clipboard paste with pre-existing clipboard backup and restore.
- [ ] Visual Diff verifies UI state transition before completing an action step.
- [ ] `SKILL.md` is concise, actionable, and under 300 lines.
