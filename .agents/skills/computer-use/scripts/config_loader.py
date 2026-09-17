"""Configuration loader and runtime safety setup for computer-use skill."""

from __future__ import annotations

import ctypes
import os
import platform
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ComputerUseConfig:
    """Central configuration entity adhering strictly to config.md."""

    # File System Policy
    skill_root: Path
    references_dir: Path
    scripts_dir: Path
    output_dir: Path
    screenshots_dir: Path
    logs_dir: Path

    # Runtime Policy
    failsafe_enabled: bool = True
    failsafe_corner_tolerance: int = 3
    pause_between_actions: float = 0.5
    default_mouse_move_duration: float = 0.25
    default_typing_interval: float = 0.05
    default_monitor_index: int = 1
    image_max_dimension: int = 1920
    image_jpeg_quality: int = 85
    dpi_aware_enabled: bool = True

    # Validation Policy
    max_retry_attempts: int = 3


def enable_dpi_awareness() -> bool:
    """Register Per-Monitor DPI Awareness on Windows operating systems."""
    if platform.system() != "Windows":
        return False

    try:
        user32 = ctypes.windll.user32
        hdesk = user32.OpenInputDesktop(0, False, 0x01FF)
        if hdesk:
            user32.SetThreadDesktop(hdesk)
    except Exception:
        pass

    # Attempt Per-Monitor V2 awareness (Windows 10 1703+)
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
        return True
    except Exception:
        pass

    # Attempt Shcore Per-Monitor awareness (Windows 8.1 / 10 legacy)
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return True
    except Exception:
        pass

    # Attempt basic User32 DPI awareness (Windows Vista / 7)
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        return True
    except Exception:
        return False


def get_config() -> ComputerUseConfig:
    """Initialize and retrieve runtime configuration with dynamically resolved paths."""
    # Skill root resolved dynamically from script location
    current_script_path = Path(__file__).resolve()
    skill_root = current_script_path.parent.parent

    # Workspace root resolved from environment or current working directory
    workspace_root = Path(os.environ.get("WORKSPACE_ROOT", Path.cwd())).resolve()

    # Base output directory designated under docs/computer_use/
    output_dir = Path(os.environ.get("COMPUTER_USE_OUTPUT_DIR", workspace_root / "docs" / "computer_use")).resolve()
    screenshots_dir = output_dir / "screenshots"
    logs_dir = output_dir / "logs"

    # Ensure output directories exist
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Activate DPI Awareness on Windows
    enable_dpi_awareness()

    return ComputerUseConfig(
        skill_root=skill_root,
        references_dir=skill_root / "references",
        scripts_dir=skill_root / "scripts",
        output_dir=output_dir,
        screenshots_dir=screenshots_dir,
        logs_dir=logs_dir,
    )
