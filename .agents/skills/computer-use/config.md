# Computer Use Skill Configuration

Central configuration document (Single Source of Truth) defining all system specifications, relative file paths, validation rules, runtime parameters, naming conventions, and workflow policies for the `computer-use` skill.
All execution phases within this skill MUST adhere strictly to the policies defined in this file. Hardcoding values that belong to runtime, validation, workflow, naming, or file system policies is strictly prohibited.

---

## 1. File System Policy

- **Skill Root Directory**: Dynamically resolved relative to the location of this skill directory (`<skill_root>/`).
- **References Directory**: `<skill_root>/references/`
- **Scripts Directory**: `<skill_root>/scripts/`
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
- **Session Log File Pattern**: `session_<timestamp>_<session_slug>.jsonl`
- **Coordinate Output Representation**:
  - Absolute Coordinates: `{"x": int, "y": int, "coord_type": "absolute"}`
  - Normalized Coordinates: `{"x_norm": float, "y_norm": float, "coord_type": "normalized", "scale": 1000}`

---

## 3. Runtime Policy

### 3.1. Core Safety Defaults
- `FAILSAFE_ENABLED`: `True` (Moving the mouse cursor to any screen corner: (0, 0), (max_x, 0), (0, max_y), (max_x, max_y) immediately aborts execution).
- `FAILSAFE_CORNER_TOLERANCE`: 3 pixels from screen edges.
- `PAUSE_BETWEEN_ACTIONS`: 0.5 seconds (minimum pause between consecutive PyAutoGUI commands to allow UI rendering).
- `DEFAULT_MOUSE_MOVE_DURATION`: 0.25 seconds (smooth mouse movement to avoid drop-event issues in UI frameworks).
- `DEFAULT_TYPING_INTERVAL`: 0.05 seconds/character (simulating natural human typing speed).

### 3.2. Screen Capture Configuration
- `ENGINE`: `mss` (Primary choice for sub-30ms capture speed and robust multi-monitor support).
- `FALLBACK_ENGINE`: `Pillow` / `PyAutoGUI`.
- `DEFAULT_MONITOR_INDEX`: 1 (Primary monitor index in MSS; index 0 represents the full virtual screen bounding box).
- `IMAGE_MAX_DIMENSION`: 1920 (Maximum dimension to scale down large displays and optimize VLM token consumption).
- `IMAGE_JPEG_QUALITY`: 85 (Applied when compression is required).

### 3.3. Multi-Monitor & DPI Settings
- `DPI_AWARE_ENABLED`: `True` (Automatically enables Per-Monitor DPI Awareness on Windows via ctypes).
- `SUPPORTED_OS`: `Windows`, `macOS`, `Linux`.

---

## 4. Validation Policy

### 4.1. Coordinate Boundary Verification
- Action coordinates `(x, y)` must lie strictly within the geometric boundaries of the target display:
  - `0 <= x <= screen_width`
  - `0 <= y <= screen_height`
- Coordinates outside valid monitor boundaries must be rejected with a `CoordinateOutOfBoundsError`.

### 4.2. Destructive Actions Gate (Human-in-the-Loop Confirmation)
Execution must halt and require explicit human confirmation before executing any of the following actions:
1. **Permanent Data Deletion**: Keyboard shortcut `Shift + Delete`, clicking "Delete" or "Empty Recycle Bin", terminal commands `rm -rf`, `format`, `drop database`.
2. **Sensitive Credentials / Financial Transactions**: Entering account passwords, credit card details, API keys, or clicking "Payment", "Transfer", "Confirm Order".
3. **OS System Configuration**: Interacting with Windows UAC elevation prompts, Registry Editor, firewall configuration, software uninstallation.
4. **External Data Dispatch**: Clicking "Send", "Publish", or submitting public forms and emails.

---

## 5. Workflow Policy

### 5.1. Closed-Loop 4-Phase Cycle (Observe-Action-Verify)
1. **Phase 1 - Observe**: Capture current screen state, retrieve display dimensions and DPI scale factor.
2. **Phase 2 - Analyze & Map**: Locate target UI element, map normalized coordinates to physical/logical pixel coordinates.
3. **Phase 3 - Execute**: Issue mouse movement, click, drag, scroll, or keystrokes with safe delays and failsafe guards.
4. **Phase 4 - Verify**: Capture verification screenshot and compare state. Trigger retry logic if the UI did not transition.

### 5.2. Retry Policy & Failure Handling
- `MAX_RETRY_ATTEMPTS`: 3 attempts per atomic UI step.
- `RETRY_BACKOFF_SECONDS`: [1.0, 2.0, 3.0] (incremental delay for slow-loading interfaces).
- If the UI remains unchanged after 3 attempts: Abort the pipeline and report failure to the user with the latest screenshot.
