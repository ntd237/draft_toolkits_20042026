"""Screen capture module implemented with native Windows GDI/GDI+ (Zero external dependencies)."""

from __future__ import annotations

import datetime
from ctypes import wintypes
import ctypes
from pathlib import Path
from typing import Any

from config_loader import get_config

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


class ScreenCapture:
    """Acquires screen captures and extracts display metadata using native Win32 APIs."""

    def __init__(self) -> None:
        self.config = get_config()
        self._gdi_token = ctypes.c_ulong()
        startup_in = GdiplusStartupInput(1, None, False, False)
        gdiplus.GdiplusStartup(ctypes.byref(self._gdi_token), ctypes.byref(startup_in), None)

    def __del__(self) -> None:
        try:
            if hasattr(self, "_gdi_token") and self._gdi_token:
                gdiplus.GdiplusShutdown(self._gdi_token)
        except Exception:
            pass

    def get_monitors_info(self) -> list[dict[str, Any]]:
        """Enumerate geometric layout and bounds of all connected displays."""
        monitors: list[dict[str, Any]] = []

        # Index 0: Virtual desktop spanning all displays
        vx = user32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
        vy = user32.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN
        vw = user32.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
        vh = user32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN

        monitors.append({
            "index": 0,
            "left": vx,
            "top": vy,
            "width": vw,
            "height": vh,
            "is_virtual_all": True,
        })

        raw_monitors: list[dict[str, int]] = []

        def _enum_proc(h_monitor: Any, hdc_monitor: Any, lprc_monitor: Any, dw_data: Any) -> bool:
            rect = lprc_monitor.contents
            raw_monitors.append({
                "left": rect.left,
                "top": rect.top,
                "width": rect.right - rect.left,
                "height": rect.bottom - rect.top,
            })
            return True

        monitor_enum_proc = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HMONITOR,
            wintypes.HDC,
            ctypes.POINTER(wintypes.RECT),
            wintypes.LPARAM,
        )
        user32.EnumDisplayMonitors(None, None, monitor_enum_proc(_enum_proc), 0)

        for idx, mon in enumerate(raw_monitors, start=1):
            monitors.append({
                "index": idx,
                "left": mon["left"],
                "top": mon["top"],
                "width": mon["width"],
                "height": mon["height"],
                "is_virtual_all": False,
            })

        return monitors

    def capture(
        self,
        monitor_index: int | None = None,
        region: tuple[int, int, int, int] | None = None,
        step_id: str = "step",
        resize_max: int | None = None,
    ) -> dict[str, Any]:
        """
        Capture display area using native GDI BitBlt and encode directly to PNG via GDI+.

        Returns metadata dictionary containing the saved image file path.
        """
        if monitor_index is None:
            monitor_index = self.config.default_monitor_index

        if resize_max is None:
            resize_max = self.config.image_max_dimension

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_{timestamp}_{step_id}.png"
        output_path = self.config.screenshots_dir / filename

        monitors = self.get_monitors_info()

        if region is not None:
            src_x, src_y, src_w, src_h = region
        else:
            selected_monitor = None
            for mon in monitors:
                if mon["index"] == monitor_index:
                    selected_monitor = mon
                    break
            if selected_monitor is None:
                selected_monitor = monitors[1] if len(monitors) > 1 else monitors[0]

            src_x = selected_monitor["left"]
            src_y = selected_monitor["top"]
            src_w = selected_monitor["width"]
            src_h = selected_monitor["height"]

        # Capture desktop bitmap via GDI BitBlt
        hdc_screen = user32.GetDC(0)
        hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
        hbm = gdi32.CreateCompatibleBitmap(hdc_screen, src_w, src_h)
        hbm_old = gdi32.SelectObject(hdc_mem, hbm)

        # SRCCOPY = 0x00CC0020
        gdi32.BitBlt(hdc_mem, 0, 0, src_w, src_h, hdc_screen, src_x, src_y, 0x00CC0020)

        # Create GDI+ Bitmap from HBITMAP
        p_bitmap = ctypes.c_void_p()
        gdiplus.GdipCreateBitmapFromHBITMAP(hbm, 0, ctypes.byref(p_bitmap))

        orig_w = src_w
        orig_h = src_h
        final_w = src_w
        final_h = src_h
        scale_factor = 1.0

        # Optional downscaling to conserve VLM tokens
        p_final_bitmap = p_bitmap
        if resize_max > 0 and (src_w > resize_max or src_h > resize_max):
            if src_w >= src_h:
                final_w = resize_max
                final_h = int(src_h * (resize_max / src_w))
            else:
                final_h = resize_max
                final_w = int(src_w * (resize_max / src_h))
            scale_factor = final_w / src_w

            p_resized = ctypes.c_void_p()
            status = gdiplus.GdipGetImageThumbnail(
                p_bitmap,
                final_w,
                final_h,
                ctypes.byref(p_resized),
                None,
                None,
            )
            if status == 0:
                p_final_bitmap = p_resized

        # Save to PNG file directly through GDI+ PNG encoder
        save_status = gdiplus.GdipSaveImageToFile(
            p_final_bitmap,
            ctypes.c_wchar_p(str(output_path)),
            ctypes.byref(PNG_CLSID),
            None,
        )

        # Cleanup allocated GDI and GDI+ resources
        if p_final_bitmap != p_bitmap:
            gdiplus.GdipDisposeImage(p_final_bitmap)
        gdiplus.GdipDisposeImage(p_bitmap)

        gdi32.SelectObject(hdc_mem, hbm_old)
        gdi32.DeleteObject(hbm)
        gdi32.DeleteDC(hdc_mem)
        user32.ReleaseDC(0, hdc_screen)

        if save_status != 0:
            return {
                "status": "error",
                "message": f"GDI+ failed to save image to {output_path} (code: {save_status})",
            }

        return {
            "status": "success",
            "file_path": str(output_path),
            "file_name": filename,
            "width": final_w,
            "height": final_h,
            "original_width": orig_w,
            "original_height": orig_h,
            "scale_factor": scale_factor,
            "monitor_left": src_x,
            "monitor_top": src_y,
            "timestamp": timestamp,
        }


if __name__ == "__main__":
    import json
    sc = ScreenCapture()
    print("Monitors detected:", json.dumps(sc.get_monitors_info(), indent=2))
    res = sc.capture(step_id="test_native")
    print("Capture output:", json.dumps(res, indent=2))
