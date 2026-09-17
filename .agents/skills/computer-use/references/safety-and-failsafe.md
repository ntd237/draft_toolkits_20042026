# Technical Reference: Safety Principles, Emergency Fail-Safe, and Access Control

Comprehensive guide specifying mandatory safety principles, emergency fail-safe designs, human-in-the-loop approval gates, and risk-mitigation strategies for desktop computer automation.

---

## 1. Emergency Fail-Safe Mechanism

### 1.1. Risks of Automated GUI Interactions
Simulated mouse and keyboard events are low-level operating system input interrupts. If an AI agent encounters visual hallucinations, infinite decision loops, or misidentified interactive elements, unchecked cursor execution can cause rapid, unintended changes outside user control.

### 1.2. PyAutoGUI Fail-Safe Behavior
- **Mechanism**: When `pyautogui.FAILSAFE = True`, the library queries the current cursor position before dispatching any input event. If the mouse cursor is located in the top-left corner `(0, 0)`, the library immediately throws a `pyautogui.FailSafeException`.
- **Four-Corner Extension**: In practical desktop operations, users naturally slam the mouse toward whichever screen corner is nearest. The safety module extends corner detection to all four display corners:
  - Top-Left: `x <= 3 and y <= 3`
  - Top-Right: `x >= screen_width - 4 and y <= 3`
  - Bottom-Left: `x <= 3 and y >= screen_height - 4`
  - Bottom-Right: `x >= screen_width - 4 and y >= screen_height - 4`

### 1.3. Multi-Monitor Four-Corner Fail-Safe Implementation
In modern desktop environments with multi-monitor setups, users instinctively slam the mouse cursor to the nearest corner of whatever monitor they are looking at. The system enumerates all connected physical displays via `EnumDisplayMonitors` and verifies cursor boundaries against every monitor corner:

```python
def check_multimonitor_failsafe(cursor_pos: tuple[int, int], monitors: list[dict], tolerance: int = 3) -> bool:
    """Verify whether the cursor is in any corner of ANY connected physical display."""
    cx, cy = cursor_pos
    for mon in monitors:
        ml, mt = mon["left"], mon["top"]
        mr = mon["left"] + mon["width"] - 1
        mb = mon["top"] + mon["height"] - 1
        corners = [(ml, mt), (mr, mt), (ml, mb), (mr, mb)]
        for corner_x, corner_y in corners:
            if abs(cx - corner_x) <= tolerance and abs(cy - corner_y) <= tolerance:
                return True
    return False
```

### 1.4. FailSafeTriggered Exception Protocol
Upon catching `FailSafeTriggered`:
1. Immediately abort pending input queues.
2. Release all pressed mouse buttons (`mouse_up` for left, right, middle) and modifier keys (`key_up` for Ctrl, Alt, Shift, Win) to prevent stuck input states.
3. Write an emergency audit record with status `ABORTED_BY_USER_FAILSAFE`.
4. Relinquish total control to the user and present a clear termination notice.

---

## 2. Human-in-the-Loop Confirmation Gate

### 2.1. Action Risk Classification Matrix

| Level | Risk Tier | Action Types | Execution Policy |
|---|---|---|---|
| **Level 0** | Safe Read-Only | Screen capture, scrolling, cursor hovering, reading text | Autonomous execution permitted |
| **Level 1** | Low Impact | Switching tabs, activating view windows, focusing search bars | Autonomous execution with audit log |
| **Level 2** | Medium Impact | Typing draft content, saving temporary files, non-destructive dialogs | Brief execution notification |
| **Level 3** | High / Destructive | Deleting files, overwriting data, sending emails, submitting orders | **MANDATORY HALT: AWAIT USER CONFIRMATION** |
| **Level 4** | Critical Security | OS elevation (UAC/sudo), Registry edits, entering credentials | **MANDATORY HALT: REQUIRE DIRECT MANUAL USER INPUT** |

### 2.2. Destructive Actions Blacklist
If a planned action matches any of the following patterns, the agent **MUST NOT EXECUTE IT AUTONOMOUSLY**:

1. **Permanent Deletion Shortcuts**:
   - `Shift + Delete` (permanent file deletion bypassing Trash/Recycle Bin).
   - Indiscriminate process termination: `Alt + F4` on critical OS or IDE processes.
2. **High-Risk Shell Commands**:
   - `rm -rf`, `del /f /s /q`, `rmdir /s /q`.
   - Disk operations: `format`, `fdisk`, `diskpart`, `mkfs`.
   - Destructive VCS: `git reset --hard`, `git push --force`.
   - Unbounded database drops: `DROP DATABASE`, `TRUNCATE TABLE`, `DELETE FROM` without WHERE.
3. **Financial and Purchasing Actions**:
   - Clicking "Pay Now", "Place Order", "Confirm Wire Transfer", "Checkout".
   - Submitting credit card information (CVV, PAN), OTP codes, or crypto seed phrases.
4. **Security Elevation and Identity**:
   - Auto-filling master passwords, banking credentials, or cloud secrets.
   - Clicking "Yes" on Windows UAC (User Account Control) dialogs or typing `sudo` passwords.

### 2.3. Confirmation Gate Workflow
When entering a Level 3 or Level 4 condition:
1. Capture an evidence screenshot of the target interface.
2. Freeze all automated input loops.
3. Present a structured proposal to the user:
   - **Proposed Action**: Exact operation to be performed (e.g., "Click 'Delete Database' button").
   - **Target Coordinates & UI**: Coordinates `(x, y)` and bounding element name.
   - **Risk Assessment**: Irreversible state change or potential data loss.
   - **Requirement**: Await explicit affirmative input (`Y` / `Confirm`) from user before proceeding.

---

## 3. Natural Interaction Pacing and Rate Limiting

### 3.1. Preventing OS Event Drop
Operating system window managers and web browsers require finite processing windows for event dispatch:
- Dispatching `mouseDown` and `mouseUp` within microseconds frequently fails to register click handlers.
- Emitting 1000 keystrokes instantaneously overflows OS message queues or triggers anti-bot heuristics.

### 3.2. Pacing Standards
- **Action Pause**: Default $0.3 - 0.5$ seconds pause between separate command invocations.
- **Mouse Motion Tweening**: Use smooth easing functions (`easeInOutQuad`) over $0.2 - 0.4$ seconds rather than instant coordinate teleportation.
- **Keystroke Intervals**: $0.03 - 0.08$ seconds between consecutive keys. For text sequences exceeding 50 characters, use clipboard pasting to eliminate typing latency and accent drops.

---

## 4. Error Recovery and Rollback Strategies

### 4.1. Loss of Window Focus
- **Symptom**: An unexpected notification, background update, or transient modal interrupts target focus.
- **Remediation**:
  1. Inspect the active window title (`GetActiveWindow()`).
  2. If the active window differs from target application, pause mouse actions and attempt window refocus.
  3. If focus cannot be restored after 2 attempts, pause and alert the user.

### 4.2. Stale State / Unresponsive Click
- If the verification screenshot remains identical to the pre-action screenshot:
  - **Attempt 1**: Re-verify coordinates and perform click with longer click duration (100ms hold).
  - **Attempt 2**: Check if the target element requires a double-click.
  - **Attempt 3**: Attempt equivalent keyboard activation (e.g., `Enter` or accelerator keys).
  - **Exceeded 3 attempts**: Halt execution and escalate diagnostic state to user.
