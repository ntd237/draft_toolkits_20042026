"""Central command-line controller connecting screen capture, mouse, and keyboard automation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Ensure local module resolution regardless of invocation directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from keyboard import KeyboardController
from mouse import MouseController
from screen import ScreenCapture


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Computer-Use CLI Controller: Safe screen capture, mouse, and keyboard automation."
    )
    subparsers = parser.add_subparsers(dest="command", help="Automation subcommand to execute")

    # Subcommand: info
    subparsers.add_parser("info", help="Retrieve display geometry, monitor layout, and mouse position")

    # Subcommand: screen
    screen_parser = subparsers.add_parser("screen", help="Capture display screenshot")
    screen_parser.add_argument("--monitor", type=int, default=1, help="Target monitor index (1 is primary)")
    screen_parser.add_argument("--step", type=str, default="step", help="Step identifier tag for screenshot file")
    screen_parser.add_argument("--resize", type=int, default=1920, help="Maximum image dimension in pixels")

    # Subcommand: click
    click_parser = subparsers.add_parser("click", help="Click mouse button at (x, y)")
    click_parser.add_argument("--x", type=int, default=None, help="Target X coordinate")
    click_parser.add_argument("--y", type=int, default=None, help="Target Y coordinate")
    click_parser.add_argument("--button", type=str, default="left", choices=["left", "right", "middle"])
    click_parser.add_argument("--clicks", type=int, default=1, help="Number of clicks")

    # Subcommand: move
    move_parser = subparsers.add_parser("move", help="Move cursor smoothly to (x, y)")
    move_parser.add_argument("--x", type=int, required=True, help="Target X coordinate")
    move_parser.add_argument("--y", type=int, required=True, help="Target Y coordinate")
    move_parser.add_argument("--duration", type=float, default=0.25, help="Move duration in seconds")

    # Subcommand: type
    type_parser = subparsers.add_parser("type", help="Type string using simulated keystrokes")
    type_parser.add_argument("--text", type=str, required=True, help="Text string to type")
    type_parser.add_argument("--interval", type=float, default=0.05, help="Delay between characters")

    # Subcommand: paste
    paste_parser = subparsers.add_parser("paste", help="Paste Unicode text via system clipboard")
    paste_parser.add_argument("--text", type=str, required=True, help="Text content to paste")

    # Subcommand: hotkey
    hotkey_parser = subparsers.add_parser("hotkey", help="Dispatch keyboard shortcut combination")
    hotkey_parser.add_argument("--keys", type=str, required=True, help="Comma-separated keys (e.g. ctrl,c)")
    hotkey_parser.add_argument("--allow-destructive", action="store_true", help="Explicitly permit destructive shortcuts")

    # Subcommand: scroll
    scroll_parser = subparsers.add_parser("scroll", help="Scroll vertical wheel up or down")
    scroll_parser.add_argument("--clicks", type=int, required=True, help="Scroll clicks (negative: down, positive: up)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    result: dict[str, Any] = {}
    screen_cap = ScreenCapture()
    mouse_ctrl = MouseController()
    kb_ctrl = KeyboardController()

    try:
        if args.command == "info":
            monitors = screen_cap.get_monitors_info()
            mouse_x, mouse_y = mouse_ctrl.get_position()
            result = {
                "status": "success",
                "monitors": monitors,
                "current_mouse_position": {"x": mouse_x, "y": mouse_y},
            }

        elif args.command == "screen":
            result = screen_cap.capture(
                monitor_index=args.monitor,
                step_id=args.step,
                resize_max=args.resize,
            )

        elif args.command == "click":
            result = mouse_ctrl.click(
                x=args.x,
                y=args.y,
                button=args.button,
                clicks=args.clicks,
            )

        elif args.command == "move":
            result = mouse_ctrl.move(x=args.x, y=args.y, duration=args.duration)

        elif args.command == "type":
            result = kb_ctrl.type_text(text=args.text, interval=args.interval)

        elif args.command == "paste":
            result = kb_ctrl.paste_text(text=args.text)

        elif args.command == "hotkey":
            keys = [k.strip() for k in args.keys.split(",") if k.strip()]
            result = kb_ctrl.hotkey(*keys, allow_destructive=args.allow_destructive)

        elif args.command == "scroll":
            result = mouse_ctrl.scroll(clicks=args.clicks)

    except Exception as exc:
        result = {"status": "error", "message": str(exc)}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("status") in ["error", "failsafe_aborted", "blocked_by_safety_policy"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
