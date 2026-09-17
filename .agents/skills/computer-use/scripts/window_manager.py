"""Window management and Focus Guard module implemented with native Windows User32 APIs (Zero external dependencies)."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Any

user32 = ctypes.windll.user32


class RECT(ctypes.Structure):
    """Win32 RECT structure representing coordinates of a rectangle."""

    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


# Configure Win32 API signatures for 64-bit compatibility
user32.GetForegroundWindow.restype = wintypes.HWND
user32.GetForegroundWindow.argtypes = []

user32.GetWindowTextLengthW.restype = ctypes.c_int
user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]

user32.GetWindowTextW.restype = ctypes.c_int
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]

user32.GetClassNameW.restype = ctypes.c_int
user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]

user32.GetWindowRect.restype = wintypes.BOOL
user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT)]

user32.SetForegroundWindow.restype = wintypes.BOOL
user32.SetForegroundWindow.argtypes = [wintypes.HWND]


class WindowManager:
    """Manages window state, focus detection, and window geometry using native Win32 User32 APIs."""

    def __init__(self) -> None:
        try:
            from config_loader import get_config

            self.config = get_config()
        except Exception:
            self.config = None

    def _get_foreground_hwnd(self) -> int:
        """Retrieve HWND of the current foreground window."""
        hwnd = user32.GetForegroundWindow()
        return int(hwnd) if hwnd else 0

    def _get_window_text(self, hwnd: int) -> str:
        """Retrieve window title text for given HWND."""
        if not hwnd:
            return ""
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return ""
        buf = ctypes.create_unicode_buffer(length + 1)
        ret = user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value if ret > 0 else ""

    def _get_class_name(self, hwnd: int) -> str:
        """Retrieve window class name for given HWND."""
        if not hwnd:
            return ""
        buf = ctypes.create_unicode_buffer(256)
        ret = user32.GetClassNameW(hwnd, buf, 256)
        return buf.value if ret > 0 else ""

    def get_window_rect(self, hwnd: int) -> dict[str, int] | None:
        """Retrieve bounding rectangle and dimensions of a window by handle."""
        if not hwnd or hwnd <= 0:
            return None
        rect = RECT()
        ret = user32.GetWindowRect(hwnd, ctypes.byref(rect))
        if not ret:
            return None
        return {
            "left": int(rect.left),
            "top": int(rect.top),
            "right": int(rect.right),
            "bottom": int(rect.bottom),
            "width": int(rect.right - rect.left),
            "height": int(rect.bottom - rect.top),
        }

    def get_foreground_window_info(self) -> dict[str, Any]:
        """Retrieve comprehensive metadata about current foreground window."""
        hwnd = self._get_foreground_hwnd()
        if not hwnd:
            return {
                "hwnd": 0,
                "title": "",
                "class_name": "",
                "rect": None,
            }
        title = self._get_window_text(hwnd)
        class_name = self._get_class_name(hwnd)
        rect = self.get_window_rect(hwnd)
        return {
            "hwnd": hwnd,
            "title": title,
            "class_name": class_name,
            "rect": rect,
        }

    def is_window_focused(self, expected_title_contains: str, case_sensitive: bool = False) -> bool:
        """Check whether the active foreground window title contains expected substring."""
        if not expected_title_contains:
            return False
        info = self.get_foreground_window_info()
        title = info.get("title", "")
        if not title:
            return False
        if case_sensitive:
            return expected_title_contains in title
        return expected_title_contains.lower() in title.lower()

    def set_foreground_window(self, hwnd: int) -> bool:
        """Bring target window to foreground by HWND."""
        if not hwnd or hwnd <= 0:
            return False
        ret = user32.SetForegroundWindow(hwnd)
        return bool(ret)


# Module-level convenience functions
_default_manager: WindowManager | None = None


def get_default_manager() -> WindowManager:
    """Retrieve or lazily initialize the default WindowManager singleton."""
    global _default_manager
    if _default_manager is None:
        _default_manager = WindowManager()
    return _default_manager


def get_foreground_window_info() -> dict[str, Any]:
    """Retrieve metadata about the current foreground window."""
    return get_default_manager().get_foreground_window_info()


def is_window_focused(expected_title_contains: str, case_sensitive: bool = False) -> bool:
    """Check if the active foreground window title contains the expected text."""
    return get_default_manager().is_window_focused(expected_title_contains, case_sensitive=case_sensitive)


def get_window_rect(hwnd: int) -> dict[str, int] | None:
    """Retrieve coordinates and dimensions of a window by handle."""
    return get_default_manager().get_window_rect(hwnd)


def set_foreground_window(hwnd: int) -> bool:
    """Bring the window with given handle to foreground."""
    return get_default_manager().set_foreground_window(hwnd)
