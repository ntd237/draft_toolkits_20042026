"""Keyboard automation module implemented with native Windows User32 APIs (Zero external dependencies)."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import time
from typing import Any

from config_loader import get_config
from sendinput import send_key

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
user32.GetClipboardData.restype = ctypes.c_void_p
user32.GetClipboardData.argtypes = [wintypes.UINT]
user32.IsClipboardFormatAvailable.restype = wintypes.BOOL
user32.IsClipboardFormatAvailable.argtypes = [wintypes.UINT]
user32.OpenClipboard.restype = wintypes.BOOL
user32.OpenClipboard.argtypes = [wintypes.HWND]
user32.CloseClipboard.restype = wintypes.BOOL
user32.CloseClipboard.argtypes = []
user32.EmptyClipboard.restype = wintypes.BOOL
user32.EmptyClipboard.argtypes = []

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
    "printscreen": 0x2C,
    "prtscr": 0x2C,
    "numlock": 0x90,
    "scrolllock": 0x91,
    "pause": 0x13,
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
for i in range(10):
    VK_CODES[f"numpad{i}"] = 0x60 + i

FORBIDDEN_COMBINATIONS = [
    {"shift", "delete"},
]


def get_clipboard_text() -> str | None:
    """Retrieve UTF-16LE text from Win32 clipboard with retry loop."""
    for _ in range(5):
        if user32.OpenClipboard(0):
            try:
                if not user32.IsClipboardFormatAvailable(CF_UNICODETEXT):
                    return None
                h_mem = user32.GetClipboardData(CF_UNICODETEXT)
                if not h_mem:
                    return None
                p_mem = kernel32.GlobalLock(h_mem)
                if not p_mem:
                    return None
                try:
                    return ctypes.wstring_at(p_mem)
                finally:
                    kernel32.GlobalUnlock(h_mem)
            finally:
                user32.CloseClipboard()
        time.sleep(0.02)
    return None


def set_clipboard_text(text: str) -> bool:
    """Store Unicode text string into Windows system clipboard with retry loop."""
    opened = False
    for _ in range(5):
        if user32.OpenClipboard(0):
            opened = True
            break
        time.sleep(0.02)

    if not opened:
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


class KeyboardController:
    """Manages keystrokes, key combinations, and Unicode clipboard insertion via Win32 APIs."""

    def __init__(self) -> None:
        self.config = get_config()

    def get_clipboard_text(self) -> str | None:
        """Retrieve UTF-16LE text from Win32 clipboard with retry loop."""
        return get_clipboard_text()

    def set_clipboard_text(self, text: str) -> bool:
        """Store Unicode text string into Windows system clipboard."""
        return set_clipboard_text(text)

    def paste_text(self, text: str, restore_clipboard: bool = True) -> dict[str, Any]:
        """
        Paste arbitrary text through system clipboard and simulated Ctrl+V.

        Guarantees accurate rendering for Unicode, Vietnamese accents, and multi-line strings.
        When restore_clipboard is True, backs up previous clipboard content and restores it after paste.
        """
        try:
            previous_text = self.get_clipboard_text() if restore_clipboard else None

            if not self.set_clipboard_text(text):
                return {"status": "error", "message": "Failed to set clipboard data"}

            time.sleep(0.05)
            # Dispatch Ctrl+V
            send_key(VK_CODES["ctrl"])
            send_key(VK_CODES["v"])
            time.sleep(0.05)
            send_key(VK_CODES["v"], KEYEVENTF_KEYUP)
            send_key(VK_CODES["ctrl"], KEYEVENTF_KEYUP)

            if restore_clipboard:
                time.sleep(0.1)
                if previous_text is not None:
                    self.set_clipboard_text(previous_text)

            time.sleep(self.config.pause_between_actions)

            return {"status": "success", "action": "paste_text", "length": len(text)}

        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def key_down(self, key_name: str) -> dict[str, Any]:
        """Hold down a key without releasing."""
        k = key_name.strip().lower()
        vk = VK_CODES.get(k)
        if vk is None:
            return {"status": "error", "message": f"Unknown key name: '{key_name}'"}

        try:
            send_key(vk)
            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "key_down", "key": k}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def key_up(self, key_name: str) -> dict[str, Any]:
        """Release a held key."""
        k = key_name.strip().lower()
        vk = VK_CODES.get(k)
        if vk is None:
            return {"status": "error", "message": f"Unknown key name: '{key_name}'"}

        try:
            send_key(vk, KEYEVENTF_KEYUP)
            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "key_up", "key": k}
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
                send_key(vk)
                time.sleep(0.05)
                send_key(vk, KEYEVENTF_KEYUP)
                if presses > 1:
                    time.sleep(interval)

            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "press_key", "key": k, "presses": presses}

        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def type_text(self, text: str, interval: float | None = None) -> dict[str, Any]:
        """Type ASCII text character by character with configurable interval.

        When the text contains characters without a virtual-key mapping (Unicode,
        Vietnamese accents, unmapped punctuation), fall back to a single safe
        clipboard paste of the whole string to avoid per-character clipboard churn
        (Runtime Policy: TYPE_TEXT_FALLBACK_PASTE).
        """
        if interval is None:
            interval = self.config.default_typing_interval

        if self.config.type_text_fallback_paste and any(
            VK_CODES.get(ch.lower()) is None for ch in text
        ):
            paste_result = self.paste_text(text)
            paste_result["action"] = "type_text_paste_fallback"
            return paste_result

        try:
            for char in text:
                k = char.lower()
                vk = VK_CODES.get(k)
                if vk is not None:
                    is_upper = char.isupper()
                    if is_upper:
                        send_key(VK_CODES["shift"])

                    send_key(vk)
                    time.sleep(0.02)
                    send_key(vk, KEYEVENTF_KEYUP)

                    if is_upper:
                        send_key(VK_CODES["shift"], KEYEVENTF_KEYUP)
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
                send_key(vk)
                time.sleep(0.02)

            time.sleep(0.05)

            # Release up sequence in reverse order
            for vk in reversed(vk_sequence):
                send_key(vk, KEYEVENTF_KEYUP)
                time.sleep(0.02)

            time.sleep(self.config.pause_between_actions)
            return {"status": "success", "action": "hotkey", "keys": normalized_keys}

        except Exception as exc:
            # Attempt to release pressed keys on failure
            for vk in vk_sequence:
                try:
                    send_key(vk, KEYEVENTF_KEYUP)
                except Exception:
                    pass
            return {"status": "error", "message": str(exc)}


if __name__ == "__main__":
    kc = KeyboardController()
    print("Keyboard controller initialized successfully.")