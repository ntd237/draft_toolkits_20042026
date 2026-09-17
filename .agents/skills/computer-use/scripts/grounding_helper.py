"""Grounding helper module for visual overlays and coordinate mapping (Win32 Native GDI/GDI+).

Zero external dependencies: uses ctypes and Windows Native GDI+ exclusively.
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import os
from pathlib import Path
from typing import Any

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
gdiplus = ctypes.windll.gdiplus


class GdiplusStartupInput(ctypes.Structure):
    _fields_ = [
        ("GdiplusVersion", wintypes.UINT),
        ("DebugEventCallback", ctypes.c_void_p),
        ("SuppressBackgroundThread", wintypes.BOOL),
        ("SuppressExternalCodecs", wintypes.BOOL),
    ]


class CLSID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]


# Standard Windows PNG Encoder CLSID: {557CF406-1A04-11D3-9A73-0000F81EF32E}
PNG_CLSID = CLSID(
    0x557CF406,
    0x1A04,
    0x11D3,
    (wintypes.BYTE * 8)(0x9A, 0x73, 0x00, 0x00, 0xF8, 0x1E, 0xF3, 0x2E),
)


def normalized_to_pixel(
    norm_x: float,
    norm_y: float,
    width: int,
    height: int,
    scale: int = 1000,
) -> tuple[int, int]:
    """
    Convert normalized coordinates to integer pixel coordinates clamped within display bounds.

    Args:
        norm_x: Normalized horizontal coordinate.
        norm_y: Normalized vertical coordinate.
        width: Pixel width of target display/image.
        height: Pixel height of target display/image.
        scale: Coordinate normalization base scale (default: 1000).

    Returns:
        tuple[int, int]: Clamped integer pixel coordinates (pixel_x, pixel_y).
    """
    if width <= 0 or height <= 0:
        return 0, 0

    px = int(round((norm_x / scale) * width))
    py = int(round((norm_y / scale) * height))

    # Clamp strictly within [0, width - 1] and [0, height - 1]
    px = max(0, min(width - 1, px))
    py = max(0, min(height - 1, py))

    return px, py


def pixel_to_normalized(
    pixel_x: int,
    pixel_y: int,
    width: int,
    height: int,
    scale: int = 1000,
) -> tuple[int, int]:
    """
    Convert integer pixel coordinates to normalized scale representation.

    Args:
        pixel_x: Horizontal pixel coordinate.
        pixel_y: Vertical pixel coordinate.
        width: Pixel width of target display/image.
        height: Pixel height of target display/image.
        scale: Coordinate normalization base scale (default: 1000).

    Returns:
        tuple[int, int]: Normalized integer coordinates (norm_x, norm_y).
    """
    if width <= 0 or height <= 0:
        return 0, 0

    norm_x = int(round((pixel_x / width) * scale))
    norm_y = int(round((pixel_y / height) * scale))

    norm_x = max(0, min(scale, norm_x))
    norm_y = max(0, min(scale, norm_y))

    return norm_x, norm_y


def map_to_desktop(
    pixel_x: int,
    pixel_y: int,
    monitor_info: dict[str, Any] | None = None,
    scale_factor: float = 1.0,
) -> tuple[int, int]:
    """
    Map image-local pixel coordinates to global desktop space.

    Compensates for VLM image downscaling and incorporates monitor origin offsets.

    Args:
        pixel_x: Horizontal pixel coordinate in captured/scaled image.
        pixel_y: Vertical pixel coordinate in captured/scaled image.
        monitor_info: Monitor geometry dictionary containing left/top or monitor_left/monitor_top.
        scale_factor: Scale factor between scaled image and original screen (scale = scaled / orig).

    Returns:
        tuple[int, int]: Absolute desktop coordinates (desktop_x, desktop_y).
    """
    if scale_factor and scale_factor > 0:
        orig_x = pixel_x / scale_factor
        orig_y = pixel_y / scale_factor
    else:
        orig_x = float(pixel_x)
        orig_y = float(pixel_y)

    mon_left = 0
    mon_top = 0
    if monitor_info:
        mon_left = int(monitor_info.get("left", monitor_info.get("monitor_left", 0)))
        mon_top = int(monitor_info.get("top", monitor_info.get("monitor_top", 0)))

    desktop_x = int(round(orig_x)) + mon_left
    desktop_y = int(round(orig_y)) + mon_top

    return desktop_x, desktop_y


class GroundingHelper:
    """Helper class providing visual overlay generation and coordinate mapping services."""

    def __init__(self) -> None:
        self._gdi_token = ctypes.c_ulong()
        startup_in = GdiplusStartupInput(1, None, False, False)
        gdiplus.GdiplusStartup(ctypes.byref(self._gdi_token), ctypes.byref(startup_in), None)

    def __del__(self) -> None:
        try:
            if hasattr(self, "_gdi_token") and self._gdi_token:
                gdiplus.GdiplusShutdown(self._gdi_token)
        except Exception:
            pass

    def normalized_to_pixel(
        self,
        norm_x: float,
        norm_y: float,
        width: int,
        height: int,
        scale: int = 1000,
    ) -> tuple[int, int]:
        """Delegate to module-level normalized_to_pixel."""
        return normalized_to_pixel(norm_x, norm_y, width, height, scale)

    def pixel_to_normalized(
        self,
        pixel_x: int,
        pixel_y: int,
        width: int,
        height: int,
        scale: int = 1000,
    ) -> tuple[int, int]:
        """Delegate to module-level pixel_to_normalized."""
        return pixel_to_normalized(pixel_x, pixel_y, width, height, scale)

    def map_to_desktop(
        self,
        pixel_x: int,
        pixel_y: int,
        monitor_info: dict[str, Any] | None = None,
        scale_factor: float = 1.0,
    ) -> tuple[int, int]:
        """Delegate to module-level map_to_desktop."""
        return map_to_desktop(pixel_x, pixel_y, monitor_info, scale_factor)

    def draw_grid_overlay(
        self,
        input_image_path: str,
        output_image_path: str,
        grid_step: int = 100,
        line_color: int = 0x80FF0000,
        line_width: float = 1.0,
    ) -> dict[str, Any]:
        """
        Draw coordinate grid lines onto an input image and save the overlay image using GDI+.

        Args:
            input_image_path: File path of the source image.
            output_image_path: File path where the overlay image will be saved.
            grid_step: Spacing in pixels between consecutive grid lines (default: 100).
            line_color: ARGB color integer for grid lines (default: 0x80FF0000 semi-transparent red).
            line_width: Pen line width in pixels (default: 1.0).

        Returns:
            dict[str, Any]: Execution status, image dimensions, and generated line count.
        """
        if not os.path.exists(input_image_path):
            return {
                "status": "error",
                "message": f"Input image does not exist: {input_image_path}",
            }

        out_path = Path(output_image_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        p_image = ctypes.c_void_p()
        load_status = gdiplus.GdipLoadImageFromFile(
            ctypes.c_wchar_p(str(input_image_path)),
            ctypes.byref(p_image),
        )
        if load_status != 0 or not p_image:
            return {
                "status": "error",
                "message": f"GDI+ failed to load image from {input_image_path} (status: {load_status})",
            }

        p_graphics = ctypes.c_void_p()
        p_pen = ctypes.c_void_p()
        try:
            width_val = ctypes.c_uint32()
            height_val = ctypes.c_uint32()
            gdiplus.GdipGetImageWidth(p_image, ctypes.byref(width_val))
            gdiplus.GdipGetImageHeight(p_image, ctypes.byref(height_val))
            width = width_val.value
            height = height_val.value

            gfx_status = gdiplus.GdipGetImageGraphicsContext(p_image, ctypes.byref(p_graphics))
            if gfx_status != 0 or not p_graphics:
                return {
                    "status": "error",
                    "message": f"GDI+ failed to create graphics context (status: {gfx_status})",
                }

            pen_status = gdiplus.GdipCreatePen1(
                ctypes.c_uint32(line_color),
                ctypes.c_float(line_width),
                2,  # UnitPixel
                ctypes.byref(p_pen),
            )
            if pen_status != 0 or not p_pen:
                return {
                    "status": "error",
                    "message": f"GDI+ failed to create pen (status: {pen_status})",
                }

            lines_count = 0

            # Vertical grid lines
            if grid_step > 0:
                for x in range(grid_step, width, grid_step):
                    gdiplus.GdipDrawLine(
                        p_graphics,
                        p_pen,
                        ctypes.c_float(x),
                        ctypes.c_float(0),
                        ctypes.c_float(x),
                        ctypes.c_float(height),
                    )
                    lines_count += 1

                # Horizontal grid lines
                for y in range(grid_step, height, grid_step):
                    gdiplus.GdipDrawLine(
                        p_graphics,
                        p_pen,
                        ctypes.c_float(0),
                        ctypes.c_float(y),
                        ctypes.c_float(width),
                        ctypes.c_float(y),
                    )
                    lines_count += 1

            save_status = gdiplus.GdipSaveImageToFile(
                p_image,
                ctypes.c_wchar_p(str(out_path)),
                ctypes.byref(PNG_CLSID),
                None,
            )

            if save_status != 0:
                return {
                    "status": "error",
                    "message": f"GDI+ failed to save overlay image to {out_path} (status: {save_status})",
                }

            return {
                "status": "success",
                "input_image": str(input_image_path),
                "output_image": str(out_path),
                "width": width,
                "height": height,
                "grid_step": grid_step,
                "grid_lines_count": lines_count,
            }

        finally:
            if p_pen:
                gdiplus.GdipDeletePen(p_pen)
            if p_graphics:
                gdiplus.GdipDeleteGraphics(p_graphics)
            if p_image:
                gdiplus.GdipDisposeImage(p_image)


def draw_grid_overlay(
    input_image_path: str,
    output_image_path: str,
    grid_step: int = 100,
    line_color: int = 0x80FF0000,
    line_width: float = 1.0,
) -> dict[str, Any]:
    """Module-level helper to draw coordinate grid lines on an image using GDI+."""
    helper = GroundingHelper()
    return helper.draw_grid_overlay(
        input_image_path=input_image_path,
        output_image_path=output_image_path,
        grid_step=grid_step,
        line_color=line_color,
        line_width=line_width,
    )
