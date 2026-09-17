"""Visual diff module implemented with native Windows GDI/GDI+ (Zero external dependencies)."""

from __future__ import annotations

import array
import ctypes
from ctypes import wintypes
from pathlib import Path
from typing import Any

try:
    from config_loader import get_config
except ImportError:
    get_config = None

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

PixelFormat32bppARGB = 0x0026200A
ImageLockModeRead = 0x0001
ImageLockModeWrite = 0x0002


class GpRect(ctypes.Structure):
    _fields_ = [
        ("X", ctypes.c_int),
        ("Y", ctypes.c_int),
        ("Width", ctypes.c_int),
        ("Height", ctypes.c_int),
    ]


class BitmapData(ctypes.Structure):
    _fields_ = [
        ("Width", wintypes.UINT),
        ("Height", wintypes.UINT),
        ("Stride", ctypes.c_int),
        ("PixelFormat", ctypes.c_int),
        ("Scan0", ctypes.c_void_p),
        ("Reserved", ctypes.c_void_p),
    ]


class VisualDiff:
    """Performs visual comparison between images and generates highlight diffs using Win32 GDI+."""

    def __init__(self) -> None:
        self.config = get_config() if get_config else None
        self._gdi_token = ctypes.c_ulong()
        startup_in = GdiplusStartupInput(1, None, False, False)
        gdiplus.GdiplusStartup(ctypes.byref(self._gdi_token), ctypes.byref(startup_in), None)

    def __del__(self) -> None:
        try:
            if hasattr(self, "_gdi_token") and self._gdi_token:
                gdiplus.GdiplusShutdown(self._gdi_token)
        except Exception:
            pass

    def compare(
        self,
        img1_path: str | Path,
        img2_path: str | Path,
        diff_output_path: str | Path | None = None,
        threshold: float = 0.01,
    ) -> dict[str, Any]:
        """
        Compare two images pixel-by-pixel using native GDI+.

        Args:
            img1_path: Path to baseline / before image.
            img2_path: Path to current / after image.
            diff_output_path: Optional path to save visual diff PNG with red highlights.
            threshold: Fraction threshold (e.g. 0.01 = 1%) for has_changed flag.

        Returns:
            Dictionary containing changed_pixels, total_pixels, change_ratio, has_changed, etc.
        """
        p1 = Path(img1_path)
        p2 = Path(img2_path)

        if not p1.is_file():
            raise FileNotFoundError(f"Base image not found: {img1_path}")
        if not p2.is_file():
            raise FileNotFoundError(f"Target image not found: {img2_path}")

        p_bmp1 = ctypes.c_void_p()
        p_bmp2 = ctypes.c_void_p()

        st1 = gdiplus.GdipCreateBitmapFromFile(ctypes.c_wchar_p(str(p1.resolve())), ctypes.byref(p_bmp1))
        if st1 != 0 or not p_bmp1:
            raise RuntimeError(f"GDI+ failed to load image 1: {img1_path} (status: {st1})")

        st2 = gdiplus.GdipCreateBitmapFromFile(ctypes.c_wchar_p(str(p2.resolve())), ctypes.byref(p_bmp2))
        if st2 != 0 or not p_bmp2:
            gdiplus.GdipDisposeImage(p_bmp1)
            raise RuntimeError(f"GDI+ failed to load image 2: {img2_path} (status: {st2})")

        try:
            w1 = wintypes.UINT()
            h1 = wintypes.UINT()
            w2 = wintypes.UINT()
            h2 = wintypes.UINT()

            gdiplus.GdipGetImageWidth(p_bmp1, ctypes.byref(w1))
            gdiplus.GdipGetImageHeight(p_bmp1, ctypes.byref(h1))
            gdiplus.GdipGetImageWidth(p_bmp2, ctypes.byref(w2))
            gdiplus.GdipGetImageHeight(p_bmp2, ctypes.byref(h2))

            width1, height1 = w1.value, h1.value
            width2, height2 = w2.value, h2.value

            if width1 != width2 or height1 != height2:
                raise ValueError(
                    f"Image dimensions do not match: img1 is {width1}x{height1}, img2 is {width2}x{height2}"
                )

            rect = GpRect(0, 0, width1, height1)
            bdata1 = BitmapData()
            bdata2 = BitmapData()

            st_lock1 = gdiplus.GdipBitmapLockBits(
                p_bmp1,
                ctypes.byref(rect),
                ImageLockModeRead,
                PixelFormat32bppARGB,
                ctypes.byref(bdata1),
            )
            if st_lock1 != 0:
                raise RuntimeError("GDI+ failed to lock bitmap 1 bits.")

            try:
                st_lock2 = gdiplus.GdipBitmapLockBits(
                    p_bmp2,
                    ctypes.byref(rect),
                    ImageLockModeRead,
                    PixelFormat32bppARGB,
                    ctypes.byref(bdata2),
                )
                if st_lock2 != 0:
                    raise RuntimeError("GDI+ failed to lock bitmap 2 bits.")

                try:
                    total_pixels = width1 * height1
                    total_bytes = total_pixels * 4

                    raw1 = ctypes.string_at(bdata1.Scan0, total_bytes)
                    raw2 = ctypes.string_at(bdata2.Scan0, total_bytes)

                    arr1 = array.array("I")
                    arr1.frombytes(raw1)
                    arr2 = array.array("I")
                    arr2.frombytes(raw2)

                    changed_indices = [
                        i for i, (p1_val, p2_val) in enumerate(zip(arr1, arr2)) if p1_val != p2_val
                    ]
                    changed_pixels = len(changed_indices)
                    change_ratio = (changed_pixels / total_pixels) if total_pixels > 0 else 0.0
                    has_changed = change_ratio > threshold

                    if diff_output_path is not None:
                        diff_path = Path(diff_output_path)
                        diff_path.parent.mkdir(parents=True, exist_ok=True)

                        # Highlight changed pixels in pure red (0xFFFF0000 in ARGB format)
                        diff_arr = array.array("I", arr2)
                        red_pixel = 0xFFFF0000
                        for idx in changed_indices:
                            diff_arr[idx] = red_pixel

                        p_diff_bmp = ctypes.c_void_p()
                        st_create = gdiplus.GdipCreateBitmapFromScan0(
                            width1,
                            height1,
                            0,
                            PixelFormat32bppARGB,
                            None,
                            ctypes.byref(p_diff_bmp),
                        )
                        if st_create == 0 and p_diff_bmp:
                            try:
                                bdata_diff = BitmapData()
                                st_lock_diff = gdiplus.GdipBitmapLockBits(
                                    p_diff_bmp,
                                    ctypes.byref(rect),
                                    ImageLockModeWrite,
                                    PixelFormat32bppARGB,
                                    ctypes.byref(bdata_diff),
                                )
                                if st_lock_diff == 0:
                                    try:
                                        diff_raw = diff_arr.tobytes()
                                        ctypes.memmove(bdata_diff.Scan0, diff_raw, len(diff_raw))
                                    finally:
                                        gdiplus.GdipBitmapUnlockBits(p_diff_bmp, ctypes.byref(bdata_diff))

                                gdiplus.GdipSaveImageToFile(
                                    p_diff_bmp,
                                    ctypes.c_wchar_p(str(diff_path.resolve())),
                                    ctypes.byref(PNG_CLSID),
                                    None,
                                )
                            finally:
                                gdiplus.GdipDisposeImage(p_diff_bmp)

                    return {
                        "status": "success",
                        "width": width1,
                        "height": height1,
                        "total_pixels": total_pixels,
                        "changed_pixels": changed_pixels,
                        "change_ratio": change_ratio,
                        "has_changed": has_changed,
                        "threshold": threshold,
                        "diff_output_path": str(diff_output_path) if diff_output_path else None,
                    }
                finally:
                    gdiplus.GdipBitmapUnlockBits(p_bmp2, ctypes.byref(bdata2))
            finally:
                gdiplus.GdipBitmapUnlockBits(p_bmp1, ctypes.byref(bdata1))
        finally:
            gdiplus.GdipDisposeImage(p_bmp1)
            gdiplus.GdipDisposeImage(p_bmp2)


def compare_images(
    img1_path: str | Path,
    img2_path: str | Path,
    diff_output_path: str | Path | None = None,
    threshold: float = 0.01,
) -> dict[str, Any]:
    """Convenience function delegating image comparison to VisualDiff."""
    differ = VisualDiff()
    return differ.compare(
        img1_path=img1_path,
        img2_path=img2_path,
        diff_output_path=diff_output_path,
        threshold=threshold,
    )
