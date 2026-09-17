"""Central command-line controller connecting screen capture, mouse, keyboard, and vision automation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

# Ensure local module resolution regardless of invocation directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from grounding_helper import GroundingHelper, map_to_desktop, normalized_to_pixel
from keyboard import KeyboardController
from mouse import MouseController
from screen import ScreenCapture
from visual_diff import VisualDiff
from window_manager import WindowManager


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Computer-Use CLI Controller: Safe screen capture, mouse, keyboard, and vision automation."
    )
    subparsers = parser.add_subparsers(dest="command", help="Automation subcommand to execute")

    # Subcommand: info
    subparsers.add_parser("info", help="Retrieve display geometry, monitor layout, and mouse position")

    # Subcommand: screen
    screen_parser = subparsers.add_parser("screen", help="Capture display screenshot")
    screen_parser.add_argument("--monitor", type=int, default=1, help="Target monitor index (1 is primary)")
    screen_parser.add_argument("--step", type=str, default="step", help="Step identifier tag for screenshot file")
    screen_parser.add_argument("--resize", type=int, default=1920, help="Maximum image dimension in pixels")
    screen_parser.add_argument("--region", type=str, default=None, help="Comma-separated region: x,y,w,h")
    screen_parser.add_argument("--window-hwnd", type=int, default=None, help="Target window handle HWND to capture")

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

    # Subcommand: drag
    drag_parser = subparsers.add_parser("drag", help="Drag mouse from (start_x, start_y) to (end_x, end_y)")
    drag_parser.add_argument("--start-x", type=int, required=True, help="Starting X coordinate")
    drag_parser.add_argument("--start-y", type=int, required=True, help="Starting Y coordinate")
    drag_parser.add_argument("--end-x", type=int, required=True, help="Ending X coordinate")
    drag_parser.add_argument("--end-y", type=int, required=True, help="Ending Y coordinate")
    drag_parser.add_argument("--duration", type=float, default=0.5, help="Drag duration in seconds")

    # Subcommand: type
    type_parser = subparsers.add_parser("type", help="Type string using simulated keystrokes")
    type_parser.add_argument("--text", type=str, required=True, help="Text string to type")
    type_parser.add_argument("--interval", type=float, default=0.05, help="Delay between characters")

    # Subcommand: paste
    paste_parser = subparsers.add_parser("paste", help="Paste Unicode text via system clipboard")
    paste_parser.add_argument("--text", type=str, required=True, help="Text content to paste")
    paste_parser.add_argument("--no-restore", action="store_true", help="Do not restore previous clipboard text")

    # Subcommand: hotkey
    hotkey_parser = subparsers.add_parser("hotkey", help="Dispatch keyboard shortcut combination")
    hotkey_parser.add_argument("--keys", type=str, required=True, help="Comma-separated keys (e.g. ctrl,c)")
    hotkey_parser.add_argument("--allow-destructive", action="store_true", help="Explicitly permit destructive shortcuts")

    # Subcommand: scroll
    scroll_parser = subparsers.add_parser("scroll", help="Scroll vertical wheel up or down")
    scroll_parser.add_argument("--clicks", type=int, required=True, help="Scroll clicks (negative: down, positive: up)")
    scroll_parser.add_argument("--x", type=int, default=None, help="Optional X coordinate to move before scrolling")
    scroll_parser.add_argument("--y", type=int, default=None, help="Optional Y coordinate to move before scrolling")

    # Subcommand: overlay
    overlay_parser = subparsers.add_parser("overlay", help="Draw coordinate grid overlay on an image")
    overlay_parser.add_argument("--input", type=str, required=True, help="Input screenshot path")
    overlay_parser.add_argument("--output", type=str, required=True, help="Output image path with grid overlay")
    overlay_parser.add_argument("--step", type=int, default=100, help="Grid step interval in pixels")

    # Subcommand: map
    map_parser = subparsers.add_parser("map", help="Convert normalized coordinates to physical/desktop pixel coordinates")
    map_parser.add_argument("--norm-x", type=float, required=True, help="Normalized X coordinate")
    map_parser.add_argument("--norm-y", type=float, required=True, help="Normalized Y coordinate")
    map_parser.add_argument("--width", type=int, required=True, help="Image/monitor width")
    map_parser.add_argument("--height", type=int, required=True, help="Image/monitor height")
    map_parser.add_argument("--scale", type=int, default=1000, help="Normalization scale factor (1000 or 1)")
    map_parser.add_argument("--scale-factor", type=float, default=1.0, help="Image resize scale factor")
    map_parser.add_argument("--monitor-left", type=int, default=0, help="Monitor left offset in virtual desktop")
    map_parser.add_argument("--monitor-top", type=int, default=0, help="Monitor top offset in virtual desktop")

    # Subcommand: diff
    diff_parser = subparsers.add_parser("diff", help="Compute visual diff between pre and post action screenshots")
    diff_parser.add_argument("--img1", type=str, required=True, help="Pre-action screenshot path")
    diff_parser.add_argument("--img2", type=str, required=True, help="Post-action screenshot path")
    diff_parser.add_argument("--output", type=str, default=None, help="Optional output visual diff image path")
    diff_parser.add_argument("--threshold", type=float, default=0.01, help="Change ratio threshold to indicate UI update")

    # Subcommand: window
    window_parser = subparsers.add_parser("window", help="Query or verify active foreground window")
    window_parser.add_argument("--check", type=str, default=None, help="Check if foreground window title contains this string")
    window_parser.add_argument("--case-sensitive", action="store_true", help="Case-sensitive window title check")
    window_parser.add_argument("--hwnd", type=int, default=None, help="Specific window HWND to query geometry")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    result: dict[str, Any] = {}
    screen_cap = ScreenCapture()
    mouse_ctrl = MouseController()
    kb_ctrl = KeyboardController()
    wm = WindowManager()
    grounding = GroundingHelper()
    visual_diff = VisualDiff()

    try:
        if args.command == "info":
            monitors = screen_cap.get_monitors_info()
            mouse_x, mouse_y = mouse_ctrl.get_position()
            fg_info = wm.get_foreground_window_info()
            result = {
                "status": "success",
                "monitors": monitors,
                "current_mouse_position": {"x": mouse_x, "y": mouse_y},
                "foreground_window": fg_info,
            }

        elif args.command == "screen":
            parsed_region = None
            if args.region:
                parts = [int(p.strip()) for p in args.region.split(",")]
                if len(parts) == 4:
                    parsed_region = (parts[0], parts[1], parts[2], parts[3])

            result = screen_cap.capture(
                monitor_index=args.monitor,
                region=parsed_region,
                window_hwnd=args.window_hwnd,
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

        elif args.command == "drag":
            result = mouse_ctrl.drag(
                start_x=args.start_x,
                start_y=args.start_y,
                end_x=args.end_x,
                end_y=args.end_y,
                duration=args.duration,
            )

        elif args.command == "type":
            result = kb_ctrl.type_text(text=args.text, interval=args.interval)

        elif args.command == "paste":
            result = kb_ctrl.paste_text(text=args.text, restore_clipboard=not args.no_restore)

        elif args.command == "hotkey":
            keys = [k.strip() for k in args.keys.split(",") if k.strip()]
            result = kb_ctrl.hotkey(*keys, allow_destructive=args.allow_destructive)

        elif args.command == "scroll":
            result = mouse_ctrl.scroll(clicks=args.clicks, x=args.x, y=args.y)

        elif args.command == "overlay":
            result = grounding.draw_grid_overlay(
                input_image_path=args.input,
                output_image_path=args.output,
                grid_step=args.step,
            )

        elif args.command == "map":
            pix_x, pix_y = normalized_to_pixel(
                norm_x=args.norm_x,
                norm_y=args.norm_y,
                width=args.width,
                height=args.height,
                scale=args.scale,
            )
            monitor_info = {"left": args.monitor_left, "top": args.monitor_top}
            desk_x, desk_y = map_to_desktop(
                pixel_x=pix_x,
                pixel_y=pix_y,
                monitor_info=monitor_info,
                scale_factor=args.scale_factor,
            )
            result = {
                "status": "success",
                "pixel_x": pix_x,
                "pixel_y": pix_y,
                "desktop_x": desk_x,
                "desktop_y": desk_y,
            }

        elif args.command == "diff":
            result = visual_diff.compare(
                img1_path=args.img1,
                img2_path=args.img2,
                diff_output_path=args.output,
                threshold=args.threshold,
            )

        elif args.command == "window":
            if args.hwnd:
                rect = wm.get_window_rect(args.hwnd)
                result = {"status": "success", "hwnd": args.hwnd, "rect": rect}
            elif args.check:
                is_focused = wm.is_window_focused(args.check, case_sensitive=args.case_sensitive)
                fg_info = wm.get_foreground_window_info()
                result = {
                    "status": "success",
                    "expected_title": args.check,
                    "is_focused": is_focused,
                    "current_window": fg_info,
                }
            else:
                fg_info = wm.get_foreground_window_info()
                result = {"status": "success", "foreground_window": fg_info}

    except Exception as exc:
        result = {"status": "error", "message": str(exc)}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("status") in ["error", "failsafe_aborted", "blocked_by_safety_policy"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
