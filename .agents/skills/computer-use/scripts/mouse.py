"""Mouse automation module implemented with native Windows User32 APIs (Zero external dependencies)."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import math
import time
from typing import Any

from config_loader import get_config

user32 = ctypes.windll.user32

# Win32 Mouse Event Flags
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
WHEEL_DELTA = 120


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class FailSafeTriggered(Exception):
    """Exception raised when user forces the mouse into an emergency failsafe screen corner."""


class MouseController:
    """Controls mouse positioning, clicking, dragging, and wheel scrolling using native Win32 APIs."""

    def __init__(self) -> None:
        self.config = get_config()

    def get_position(self) -> tuple[int, int]:
        """Retrieve current cursor coordinates."""
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)

    def _check_failsafe(self) -> None:
        """Check if cursor is positioned in any screen corner."""
        if not self.config.failsafe_enabled:
            return

        cx, cy = self.get_position()
        tol = self.config.failsafe_corner_tolerance

        # Primary display dimensions
        sw = user32.GetSystemMetrics(0)  # SM_CXSCREEN
        sh = user32.GetSystemMetrics(1)  # SM_CYSCREEN

        corners = [
            (0, 0),
            (sw - 1, 0),
            (0, sh - 1),
            (sw - 1, sh - 1),
        ]

        for corner_x, corner_y in corners:
            if abs(cx - corner_x) <= tol and abs(cy - corner_y) <= tol:
                raise FailSafeTriggered(
                    f"Mouse cursor at ({cx}, {cy}) triggered emergency failsafe corner ({corner_x}, {corner_y})."
                )

    def move(self, x: int, y: int, duration: float | None = None) -> dict[str, Any]:
        """Move cursor smoothly to target coordinates with quadratic ease-in-out interpolation."""
        if duration is None:
            duration = self.config.default_mouse_move_duration

        try:
            self._check_failsafe()
            start_x, start_y = self.get_position()

            if duration <= 0.01:
                user32.SetCursorPos(x, y)
                return {"status": "success", "action": "move", "x": x, "y": y, "duration": duration}

            steps = max(5, int(duration * 60))
            sleep_interval = duration / steps

            for i in range(1, steps + 1):
                self._check_failsafe()
                t = i / steps
                # Quadratic ease-in-out curve
                ease_t = 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
                curr_x = int(start_x + (x - start_x) * ease_t)
                curr_y = int(start_y + (y - start_y) * ease_t)
                user32.SetCursorPos(curr_x, curr_y)
                time.sleep(sleep_interval)

            user32.SetCursorPos(x, y)
            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "move", "x": x, "y": y, "duration": duration}

        except FailSafeTriggered as e:
            return {"status": "failsafe_aborted", "message": str(e)}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def click(
        self,
        x: int | None = None,
        y: int | None = None,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.1,
    ) -> dict[str, Any]:
        """Click mouse button at current position or designated coordinates."""
        try:
            self._check_failsafe()

            if x is not None and y is not None:
                move_res = self.move(x, y)
                if move_res.get("status") == "failsafe_aborted":
                    return move_res

            cur_x, cur_y = self.get_position()

            down_flag = MOUSEEVENTF_LEFTDOWN
            up_flag = MOUSEEVENTF_LEFTUP
            if button == "right":
                down_flag = MOUSEEVENTF_RIGHTDOWN
                up_flag = MOUSEEVENTF_RIGHTUP
            elif button == "middle":
                down_flag = MOUSEEVENTF_MIDDLEDOWN
                up_flag = MOUSEEVENTF_MIDDLEUP

            for _ in range(clicks):
                self._check_failsafe()
                user32.mouse_event(down_flag, 0, 0, 0, 0)
                time.sleep(0.05)
                user32.mouse_event(up_flag, 0, 0, 0, 0)
                if clicks > 1:
                    time.sleep(interval)

            time.sleep(self.config.pause_between_actions)
            return {
                "status": "success",
                "action": "click",
                "x": cur_x,
                "y": cur_y,
                "button": button,
                "clicks": clicks,
            }

        except FailSafeTriggered as e:
            return {"status": "failsafe_aborted", "message": str(e)}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def double_click(self, x: int | None = None, y: int | None = None) -> dict[str, Any]:
        """Execute double left-click."""
        return self.click(x=x, y=y, button="left", clicks=2, interval=0.15)

    def right_click(self, x: int | None = None, y: int | None = None) -> dict[str, Any]:
        """Execute single right-click."""
        return self.click(x=x, y=y, button="right", clicks=1)

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> dict[str, Any]:
        """Drag with left button held from (start_x, start_y) to (end_x, end_y)."""
        try:
            self._check_failsafe()
            self.move(start_x, start_y, duration=0.1)
            time.sleep(0.05)

            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.05)

            steps = max(5, int(duration * 60))
            sleep_interval = duration / steps

            for i in range(1, steps + 1):
                self._check_failsafe()
                t = i / steps
                curr_x = int(start_x + (end_x - start_x) * t)
                curr_y = int(start_y + (end_y - start_y) * t)
                user32.SetCursorPos(curr_x, curr_y)
                time.sleep(sleep_interval)

            user32.SetCursorPos(end_x, end_y)
            time.sleep(0.05)
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(self.config.pause_between_actions)

            return {
                "status": "success",
                "action": "drag",
                "from": [start_x, start_y],
                "to": [end_x, end_y],
            }

        except FailSafeTriggered as e:
            # Ensure mouse button is released if failsafe triggers during drag
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            return {"status": "failsafe_aborted", "message": str(e)}
        except Exception as exc:
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            return {"status": "error", "message": str(exc)}

    def scroll(self, clicks: int, x: int | None = None, y: int | None = None) -> dict[str, Any]:
        """Scroll vertical mouse wheel (positive: up, negative: down)."""
        try:
            self._check_failsafe()
            if x is not None and y is not None:
                self.move(x, y)

            wheel_amount = clicks * WHEEL_DELTA
            user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, wheel_amount, 0)
            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "scroll", "clicks": clicks}

        except FailSafeTriggered as e:
            return {"status": "failsafe_aborted", "message": str(e)}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}


if __name__ == "__main__":
    mc = MouseController()
    print("Current cursor position:", mc.get_position())
