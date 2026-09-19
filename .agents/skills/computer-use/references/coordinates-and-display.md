# Technical Reference: Coordinate Mapping, DPI Scaling, and Multi-Monitor Handling

Technical guide detailing display coordinate mathematics, conversions between logical and physical coordinate spaces, and coordinate normalization for Vision-Language Models (VLMs), as implemented by this skill's pure Win32 (ctypes) scripts on Windows.

---

## 1. Coordinate Systems: Absolute vs. Normalized

### 1.1. Absolute Coordinates
- **Definition**: Raw pixel coordinates `(x, y)` directly on the display device, where origin `(0, 0)` defaults to the top-left corner of the primary monitor.
- **Axes**:
  - `X` Axis: Increases horizontally from left to right (`0 -> screen_width - 1`).
  - `Y` Axis: Increases vertically from top to bottom (`0 -> screen_height - 1`).
- **Use Case**: Used directly by operating system input drivers and automation APIs (Win32 `SetCursorPos`, `SendInput`) to dispatch mouse movements and clicks.
- **Limitation**: Tightly coupled to hardware resolution; cannot be transferred across environments without scaling.

### 1.2. Normalized Coordinates
- **Definition**: Coordinates scaled to a standardized dimension independent of physical monitor resolutions.
- **Two Standard Conventions in AI Computer-Use**:
  1. **Unit Scale [0.0, 1.0]**: Standard in computer vision pipelines and object bounding boxes:
     $$\bar{x} = \frac{x_{\text{pixel}}}{W}, \quad \bar{y} = \frac{y_{\text{pixel}}}{H}$$
  2. **1000-Point Scale [0, 1000]**: Common in VLM Computer-Use APIs (Anthropic, Gemini GUI Grounding) to optimize integer token reasoning:
     $$x_{1000} = \operatorname{round}\left(\frac{x_{\text{pixel}}}{W} \times 1000\right), \quad y_{1000} = \operatorname{round}\left(\frac{y_{\text{pixel}}}{H} \times 1000\right)$$

### 1.3. Bi-Directional Conversion Formulas

```python
def normalized_to_absolute(x_norm: float, y_norm: float, width: int, height: int, scale: int = 1000) -> tuple[int, int]:
    """Convert normalized coordinates back to absolute physical/logical pixel coordinates."""
    abs_x = int((x_norm / scale) * width)
    abs_y = int((y_norm / scale) * height)
    # Clamp within display boundaries
    abs_x = max(0, min(width - 1, abs_x))
    abs_y = max(0, min(height - 1, abs_y))
    return abs_x, abs_y

def absolute_to_normalized(abs_x: int, abs_y: int, width: int, height: int, scale: int = 1000) -> tuple[int, int]:
    """Convert absolute pixel coordinates to normalized scale."""
    norm_x = int((abs_x / width) * scale)
    norm_y = int((abs_y / height) * scale)
    return norm_x, norm_y
```

These formulas are implemented in `scripts/grounding_helper.py` (`normalized_to_pixel` / `pixel_to_normalized`) with strict clamping within `[0, width - 1]` and `[0, height - 1]`.

### 1.4. Bounding Box Center Calculation
When a vision model predicts an element bounding box `[ymin, xmin, ymax, xmax]` or `[x1, y1, x2, y2]`, the most reliable target click point is the **geometric center** to avoid clicking borders or margins:

$$x_{\text{click}} = \left\lfloor \frac{x_1 + x_2}{2} \right\rfloor, \quad y_{\text{click}} = \left\lfloor \frac{y_1 + y_2}{2} \right\rfloor$$

---

## 2. DPI Scaling (Display Scaling)

### 2.1. Root Cause of DPI Drift
On modern high-density panels (High-DPI, 2K, 4K, Retina), Windows applies a display scale factor (125%, 150%, 200%) to maintain readable UI element sizes. This creates a disparity between:
- **Physical Resolution**: Actual hardware panel pixels (e.g., $3840 \times 2160$).
- **Logical Resolution (DIPs / Points)**: Virtualized coordinates reported to non-DPI-aware applications (e.g., at 150%: $2560 \times 1440$).

### 2.2. Coordinate Drift in Automation
Without explicit DPI-awareness registered for the process:
1. Native GDI capture (`BitBlt` from the screen DC) grabs the frame at **physical resolution** ($3840 \times 2160$).
2. The AI vision model identifies a target button at $(1500, 800)$ on the physical image.
3. `SetCursorPos` dispatches the cursor at $(1500, 800)$ in **logical coordinate space** (the coordinates a non-DPI-aware process sees).
4. Result: The mouse clicks at physical location $(2250, 1200)$—completely missing the target!

### 2.3. Per-Monitor DPI Awareness Initialization on Windows

Always execute DPI awareness registration before any screen capture or coordinate evaluation (implemented in `scripts/config_loader.py`):

```python
import ctypes
import platform

def enable_dpi_awareness():
    """Register Per-Monitor DPI Awareness with the Windows kernel."""
    if platform.system() != "Windows":
        return
    try:
        # Windows 10 Creators Update (1703+) V2
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except Exception:
        try:
            # Windows 8.1 / 10 Per-Monitor Awareness
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                # Windows Vista / 7 Basic Awareness
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception as err:
                print(f"Failed to enable DPI awareness: {err}")
```

### 2.4. DPI Awareness Cascade in This Skill
`scripts/config_loader.py` attempts the three awareness levels in order (Per-Monitor V2 → Shcore Per-Monitor → basic `SetProcessDPIAware`) and stops at the first success. Once any level is active, `GetSystemMetrics`, `EnumDisplayMonitors`, `GetWindowRect`, and `SetCursorPos` all operate in the **same physical coordinate space** as the GDI capture, so no post-hoc scale compensation is required for the raw screen image. The only remaining scale factor is the **VLM downscale** (`IMAGE_MAX_DIMENSION = 1920`), compensated via `scale_factor` during mapping.

---

## 3. Multi-Monitor Topologies (Virtual Desktop Coordinates)

### 3.1. Virtual Desktop Coordinate Space
Multi-monitor configurations are represented as a unified virtual desktop rectangle:
- **Primary Monitor**: Always contains origin `(0, 0)`.
- **Right Secondary Monitor**: Has $X \ge W_{\text{primary}}$.
- **Left Secondary Monitor**: Has $X < 0$ (negative coordinate values on Windows).
- **Above Secondary Monitor**: Has $Y < 0$.

```
                 [-1920, 0]                       [0, 0]             [1920, 0]
                 ┌────────────────────────┐      ┌──────────────────────┐
                 │  Secondary (Left)      │      │  Primary Monitor     │
                 │  Width: 1920           │      │  Width: 1920         │
                 │  Height: 1080          │      │  Height: 1080        │
                 │  X: -1920 .. -1        │      │  X: 0 .. 1919        │
                 └────────────────────────┘      └──────────────────────┘
```

### 3.2. Monitor Enumeration in This Skill
`scripts/screen.py` (`ScreenCapture.get_monitors_info()`) enumerates monitors with this convention:
- `index 0`: Entire virtual desktop bounding box (from `SM_XVIRTUALSCREEN`/`SM_YVIRTUALSCREEN`/`SM_CXVIRTUALSCREEN`/`SM_CYVIRTUALSCREEN`, metrics 76–79).
- `index 1`: Primary monitor.
- `index 2..N`: Additional physical displays, enumerated via `EnumDisplayMonitors`.

Each monitor profile provides:
```python
{"index": int, "left": int, "top": int, "width": int, "height": int, "is_virtual_all": bool}
```

`MouseController.get_monitors()` (`scripts/mouse.py`) exposes the same physical monitors (without the virtual entry) for failsafe corner checks and coordinate boundary validation.

### 3.3. Mapping Local Bounding Boxes to Global Coordinates

When targeting a specific monitor `K`:
1. Capture target display: `python scripts/controller.py screen --monitor K --step <step_id>`.
2. Vision model infers local coordinates `(local_x, local_y)` relative to that screenshot.
3. Compute global dispatch coordinates by adding monitor offsets:
   $$x_{\text{global}} = \text{left}_K + \text{local\_x}$$
   $$y_{\text{global}} = \text{top}_K + \text{local\_y}$$

```python
def map_local_to_global_coords(local_x: int, local_y: int, monitor_info: dict) -> tuple[int, int]:
    """Apply display offsets to map localized image coordinates to global desktop space."""
    global_x = monitor_info["left"] + local_x
    global_y = monitor_info["top"] + local_y
    return global_x, global_y
```

---

## 4. End-to-End Safe Coordinate Resolution Pipeline

1. **Bootstrap**: `config_loader.get_config()` runs `enable_dpi_awareness()` before anything else.
2. **Identify Target Monitor**: `python scripts/controller.py info` returns all monitor geometry and the foreground window.
3. **Capture**: `python scripts/controller.py screen --monitor <K> --step <step_id>` saves the image and returns metadata `(original_width, original_height, scale_factor, monitor_left, monitor_top)`.
4. **VLM Optimization**: Captures larger than `IMAGE_MAX_DIMENSION = 1920` are downscaled; the returned `scale_factor` (scaled / original) must be preserved.
5. **Inference Unpacking**:
   - For resized-image coordinates: `orig_x = model_x / scale_factor`.
   - For 1000-point normalized values: `orig_x = (norm_x / 1000) * width`.
6. **Offset Compensation**: `python scripts/controller.py map --norm-x <x> --norm-y <y> --width <w> --height <h> --scale-factor <sf> --monitor-left <left> --monitor-top <top>` returns `desktop_x, desktop_y` in global coordinates.
7. **Boundary Guard (enforced)**: `MouseController` validates that every dispatched point lies within one physical monitor (Validation Policy 4.1) and rejects out-of-bounds coordinates with an error before any input event is sent.
