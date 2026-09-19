"""Unified input dispatch module using native Windows SendInput API.

Replaces the deprecated `mouse_event` / `keybd_event` entry points with the
modern `SendInput` Win32 API (zero external dependencies).
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

# Input types
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

# Keyboard event flags
KEYEVENTF_KEYUP = 0x0002

# Mouse event flags (MOUSEINPUT.dwFlags)
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class _INPUTUnion(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", _INPUTUnion),
    ]


# Configure SendInput signature for 64-bit compatibility
user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
user32.SendInput.restype = wintypes.UINT


def send_mouse(dw_flags: int, mouse_data: int = 0) -> bool:
    """Dispatch a single mouse input event (button down/up, wheel) via SendInput.

    Args:
        dw_flags: Mouse event flag (MOUSEEVENTF_*).
        mouse_data: Wheel delta for MOUSEEVENTF_WHEEL; ignored otherwise.
            Negative wheel deltas are normalized to unsigned DWORD representation.

    Returns:
        True if the event was successfully inserted into the input stream.
    """
    inp = INPUT(type=INPUT_MOUSE)
    inp.union.mi = MOUSEINPUT(
        0,
        0,
        mouse_data & 0xFFFFFFFF,
        dw_flags & 0xFFFFFFFF,
        0,
        None,
    )
    return bool(user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT)))


def send_key(vk: int, dw_flags: int = 0) -> bool:
    """Dispatch a single keyboard input event (key down / key up) via SendInput.

    Args:
        vk: Virtual-key code.
        dw_flags: Keyboard event flags (KEYEVENTF_KEYUP).

    Returns:
        True if the event was successfully inserted into the input stream.
    """
    inp = INPUT(type=INPUT_KEYBOARD)
    inp.union.ki = KEYBDINPUT(vk, 0, dw_flags & 0xFFFFFFFF, 0, None)
    return bool(user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT)))
