# Computer Use Skill Configuration

Central configuration document (Single Source of Truth) defining all system specifications, relative file paths, validation rules, runtime parameters, naming conventions, and workflow policies for the `computer-use` skill.
All execution phases within this skill MUST adhere strictly to the policies defined in this file. Hardcoding values that belong to runtime, validation, workflow, naming, or file system policies is strictly prohibited.

---

## 1. File System Policy

- **Skill Root Directory**: Dynamically resolved relative to the location of this skill directory (`<skill_root>/`).
- **References Directory**: `<skill_root>/references/`
- **Scripts Directory**: `<skill_root>/scripts/`
- **Tests Directory**: `<skill_root>/tests/`
- **Base Output Directory**: `docs/computer_use/` (relative to workspace root, NOT skill root)
- **Screenshots Directory**: `docs/computer_use/screenshots/`
- **Action Logs Directory**: `docs/computer_use/logs/`
- **Supported Image Formats**: `.png`, `.jpg`, `.jpeg`
- **Metadata and Log Formats**: `.json`, `.jsonl`, `.md`

---

## 2. Naming Policy

- **Screenshot File Pattern**: `screen_<timestamp>_<step_id>.png`
  - Example: `screen_20260916_143000_step01.png`
- **Visual Diff File Pattern**: `diff_<timestamp>_<step_id>.png`
- **Coordinate Grid Overlay File Pattern**: `overlay_<timestamp>_<step_id>.png`
- **Session Log File Pattern**: `session_<yyyymmdd>_<session_slug>.jsonl` — one JSONL audit line per CLI invocation; `<session_slug>` comes from the `COMPUTER_USE_SESSION_SLUG` environment variable (default: `default`).
- **Coordinate Output Representation**:
  - Absolute Coordinates: `{"x": int, "y": int, "coord_type": "absolute"}`
  - Normalized Coordinates: `{"x_norm": float, "y_norm": float, "coord_type": "normalized", "scale": 1000}`

---

## 3. Runtime Policy

### 3.1. Core Safety Defaults
- `FAILSAFE_ENABLED`: `True` (Moving cursor into any corner of ANY display in Virtual Desktop immediately aborts execution).
- `FAILSAFE_CORNER_TOLERANCE`: 3 pixels from screen edges.
- `MULTI_MONITOR_FAILSAFE`: `True` (Enumerates and checks corners across all connected physical monitors).
- `CLIPBOARD_BACKUP_ENABLED`: `True` (Safely backs up and restores pre-existing clipboard text during Unicode paste actions).
- `FOCUS_GUARD_ENABLED`: `True` (Verifies target foreground window title before dispatching keystrokes or clicks).
- `TYPE_TEXT_FALLBACK_PASTE`: `True` (`type` automatically falls back to one safe clipboard paste when text contains characters without virtual-key mapping, e.g. Unicode/Vietnamese).
- `SESSION_SLUG_ENV`: `COMPUTER_USE_SESSION_SLUG` (Environment variable selecting the session log slug; default slug: `default`).
- `PAUSE_BETWEEN_ACTIONS`: 0.5 seconds (minimum pause between consecutive low-level commands to allow UI rendering).
- `DEFAULT_MOUSE_MOVE_DURATION`: 0.25 seconds (smooth mouse movement with quadratic ease-in-out curve).
- `DEFAULT_TYPING_INTERVAL`: 0.05 seconds/character (simulating natural human typing speed).

### 3.2. Screen Capture Configuration
- `ENGINE`: `Win32 Native GDI/GDI+` (Zero external dependencies; sub-20ms capture speed and direct PNG encoding).
- `DEFAULT_MONITOR_INDEX`: 1 (Primary monitor index; index 0 represents the full virtual screen bounding box).
- `IMAGE_MAX_DIMENSION`: 1920 (Maximum dimension to scale down large displays and optimize VLM token consumption).
- `IMAGE_JPEG_QUALITY`: 85 (Applied when compression is required).

### 3.3. Multi-Monitor & DPI Settings
- `DPI_AWARE_ENABLED`: `True` (Automatically enables Per-Monitor DPI Awareness V2 on Windows via ctypes).
- `SUPPORTED_OS`: `Windows` (Pure Win32 ctypes implementation; zero external C-extension dependencies).

---

## 4. Validation Policy

### 4.1. Coordinate Boundary Verification
- Action coordinates `(x, y)` must lie strictly within the geometric boundaries of the target display:
  - `monitor_left <= x <= monitor_left + monitor_width`
  - `monitor_top <= y <= monitor_top + monitor_height`
- Coordinates outside valid monitor boundaries must be rejected with an error.

### 4.2. Destructive Actions Gate (Human-in-the-Loop Confirmation)
Execution must halt and require explicit human confirmation before executing any of the following actions:
1. **Permanent Data Deletion**: Keyboard shortcut `Shift + Delete`, clicking "Delete" or "Empty Recycle Bin", terminal commands `rm -rf`, `format`, `drop database`.
2. **Sensitive Credentials / Financial Transactions**: Entering account passwords, credit card details, API keys, or clicking "Payment", "Transfer", "Confirm Order".
3. **OS System Configuration**: Interacting with Windows UAC elevation prompts, Registry Editor, firewall configuration, software uninstallation.
4. **External Data Dispatch**: Clicking "Send", "Publish", or submitting public forms and emails.

---

## 5. Workflow Policy

### 5.1. Closed-Loop 4-Phase Cycle (Observe-Analyze-Execute-Verify)
1. **Phase 1 - Observe**: Capture current screen state or active window, retrieve display dimensions and DPI scale factor.
   - CLI: `python scripts/controller.py screen --step <step_id>`
2. **Phase 2 - Analyze & Grounding**: Locate target UI element, draw grid overlay if needed, map normalized coordinates to physical/desktop pixel coordinates.
   - CLI: `python scripts/controller.py overlay --input <in.png> --output <out.png>`
   - CLI: `python scripts/controller.py map --norm-x <x> --norm-y <y> --width <w> --height <h>`
3. **Phase 3 - Execute**: Dispatch mouse movement, click, drag, scroll, or keystrokes with safe delays, clipboard backup, and multi-monitor failsafe guards.
   - CLI: `python scripts/controller.py window --check "<Title>"`
   - CLI: `python scripts/controller.py click --x <x> --y <y>`
   - CLI: `python scripts/controller.py drag --start-x <x1> --start-y <y1> --end-x <x2> --end-y <y2>`
   - CLI: `python scripts/controller.py paste --text "<unicode_content>"`
4. **Phase 4 - Verify**: Capture verification screenshot and compare state with Visual Diff. Trigger retry logic if the UI did not transition.
   - CLI: `python scripts/controller.py diff --img1 <pre.png> --img2 <post.png> --output <diff.png>`

### 5.2. Retry Policy & Failure Handling
- `MAX_RETRY_ATTEMPTS`: 3 attempts per atomic UI step.
- `RETRY_BACKOFF_SECONDS`: [1.0, 2.0, 3.0] (incremental delay for slow-loading interfaces).
- If the UI remains unchanged after 3 attempts (`has_changed == False`): Abort the pipeline and report failure to the user with the visual diff screenshot.
