"""Keyboard automation module implemented with native Windows User32 APIs (Zero external dependencies)."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import time
from typing import Any

from config_loader import get_config

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Configure 64-bit pointer return types and parameter types
kernel32.GlobalAlloc.restype = ctypes.c_void_p
kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32.SetClipboardData.restype = ctypes.c_void_p
user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]

# Win32 Constants
CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

# Virtual Key Codes
VK_CODES: dict[str, int] = {
    "enter": 0x0D,
    "return": 0x0D,
    "esc": 0x1B,
    "escape": 0x1B,
    "tab": 0x09,
    "space": 0x20,
    "backspace": 0x08,
    "delete": 0x2E,
    "insert": 0x2D,
    "home": 0x24,
    "end": 0x23,
    "pageup": 0x21,
    "pagedown": 0x22,
    "up": 0x26,
    "down": 0x28,
    "left": 0x25,
    "right": 0x27,
    "shift": 0x10,
    "ctrl": 0x11,
    "control": 0x11,
    "alt": 0x12,
    "win": 0x5B,
    "windows": 0x5B,
    "capslock": 0x14,
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
}

# Add standard alphanumeric keys
for c in "abcdefghijklmnopqrstuvwxyz":
    VK_CODES[c] = ord(c.upper())
for d in "0123456789":
    VK_CODES[d] = ord(d)

FORBIDDEN_COMBINATIONS = [
    {"shift", "delete"},
]


class KeyboardController:
    """Manages keystrokes, key combinations, and Unicode clipboard insertion via Win32 APIs."""

    def __init__(self) -> None:
        self.config = get_config()

    def set_clipboard_text(self, text: str) -> bool:
        """Store Unicode text string into Windows system clipboard."""
        if not user32.OpenClipboard(0):
            return False
        try:
            user32.EmptyClipboard()
            encoded_bytes = (text + "\0").encode("utf-16le")
            h_mem = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(encoded_bytes))
            if not h_mem:
                return False
            p_mem = kernel32.GlobalLock(h_mem)
            if not p_mem:
                return False
            ctypes.memmove(p_mem, encoded_bytes, len(encoded_bytes))
            kernel32.GlobalUnlock(h_mem)
            user32.SetClipboardData(CF_UNICODETEXT, h_mem)
            return True
        finally:
            user32.CloseClipboard()

    def paste_text(self, text: str) -> dict[str, Any]:
        """
        Paste arbitrary text through system clipboard and simulated Ctrl+V.

        Guarantees accurate rendering for Unicode, Vietnamese accents, and multi-line strings.
        """
        try:
            if not self.set_clipboard_text(text):
                return {"status": "error", "message": "Failed to set clipboard data"}

            time.sleep(0.05)
            # Dispatch Ctrl+V
            user32.keybd_event(VK_CODES["ctrl"], 0, 0, 0)
            user32.keybd_event(VK_CODES["v"], 0, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(VK_CODES["v"], 0, KEYEVENTF_KEYUP, 0)
            user32.keybd_event(VK_CODES["ctrl"], 0, KEYEVENTF_KEYUP, 0)
            time.sleep(self.config.pause_between_actions)

            return {"status": "success", "action": "paste_text", "length": len(text)}

        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def press_key(self, key_name: str, presses: int = 1, interval: float = 0.1) -> dict[str, Any]:
        """Press and release a single key."""
        k = key_name.strip().lower()
        vk = VK_CODES.get(k)
        if vk is None:
            return {"status": "error", "message": f"Unknown key name: '{key_name}'"}

        try:
            for _ in range(presses):
                user32.keybd_event(vk, 0, 0, 0)
                time.sleep(0.05)
                user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
                if presses > 1:
                    time.sleep(interval)

            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "press_key", "key": k, "presses": presses}

        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def type_text(self, text: str, interval: float | None = None) -> dict[str, Any]:
        """Type ASCII text character by character with configurable interval."""
        if interval is None:
            interval = self.config.default_typing_interval

        try:
            for char in text:
                k = char.lower()
                vk = VK_CODES.get(k)
                if vk is not None:
                    is_upper = char.isupper()
                    if is_upper:
                        user32.keybd_event(VK_CODES["shift"], 0, 0, 0)

                    user32.keybd_event(vk, 0, 0, 0)
                    time.sleep(0.02)
                    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)

                    if is_upper:
                        user32.keybd_event(VK_CODES["shift"], 0, KEYEVENTF_KEYUP, 0)
                else:
                    # Fallback for characters not directly mapped in ASCII table
                    self.paste_text(char)

                time.sleep(interval)

            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "type_text", "length": len(text)}

        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def hotkey(self, *keys: str, allow_destructive: bool = False) -> dict[str, Any]:
        """Dispatch combination of keys simultaneously (e.g., ctrl, c)."""
        normalized_keys = [k.strip().lower() for k in keys if k.strip()]
        key_set = set(normalized_keys)

        for forbidden in FORBIDDEN_COMBINATIONS:
            if forbidden.issubset(key_set) and not allow_destructive:
                return {
                    "status": "blocked_by_safety_policy",
                    "message": f"Key combination {normalized_keys} is blocked by safety policy. Human confirmation required.",
                }

        vk_sequence: list[int] = []
        for k in normalized_keys:
            vk = VK_CODES.get(k)
            if vk is None:
                return {"status": "error", "message": f"Unrecognized key in combination: '{k}'"}
            vk_sequence.append(vk)

        try:
            # Press down sequence
            for vk in vk_sequence:
                user32.keybd_event(vk, 0, 0, 0)
                time.sleep(0.02)

            time.sleep(0.05)

            # Release up sequence in reverse order
            for vk in reversed(vk_sequence):
                user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
                time.sleep(0.02)

            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "hotkey", "keys": normalized_keys}

        except Exception as exc:
            # Attempt to release pressed keys on failure
            for vk in vk_sequence:
                try:
                    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
                except Exception:
                    pass
            return {"status": "error", "message": str(exc)}


if __name__ == "__main__":
    kc = KeyboardController()
    print("Keyboard controller initialized successfully.")
