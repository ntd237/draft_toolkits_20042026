# Technical Reference: Coordinate Mapping, DPI Scaling, and Multi-Monitor Handling

Technical guide detailing display coordinate mathematics, conversions between logical and physical coordinate spaces, coordinate normalization for Vision-Language Models (VLMs), and cross-platform compatibility solutions for Windows, macOS, and Linux.

---

## 1. Coordinate Systems: Absolute vs. Normalized

### 1.1. Absolute Coordinates
- **Definition**: Raw pixel coordinates `(x, y)` directly on the display device, where origin `(0, 0)` defaults to the top-left corner of the primary monitor.
- **Axes**:
  - `X` Axis: Increases horizontally from left to right (`0 -> screen_width - 1`).
  - `Y` Axis: Increases vertically from top to bottom (`0 -> screen_height - 1`).
- **Use Case**: Used directly by operating system input drivers and automation libraries (`PyAutoGUI`, `pynput`, `Win32 API`) to dispatch mouse movements and clicks.
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

### 1.4. Bounding Box Center Calculation
When a vision model predicts an element bounding box `[ymin, xmin, ymax, xmax]` or `[x1, y1, x2, y2]`, the most reliable target click point is the **geometric center** to avoid clicking borders or margins:

$$x_{\text{click}} = \left\lfloor \frac{x_1 + x_2}{2} \right\rfloor, \quad y_{\text{click}} = \left\lfloor \frac{y_1 + y_2}{2} \right\rfloor$$

---

## 2. DPI Scaling (Display Scaling)

### 2.1. Root Cause of DPI Drift
On modern high-density panels (High-DPI, 2K, 4K, Retina), modern operating systems apply a display scale factor (125%, 150%, 200%) to maintain readable UI element sizes. This creates a disparity between:
- **Physical Resolution**: Actual hardware panel pixels (e.g., $3840 \times 2160$).
- **Logical Resolution (DIPs / Points)**: Virtualized coordinates reported to non-DPI-aware applications (e.g., at 150%: $2560 \times 1440$).

### 2.2. Coordinate Drift in Automation
Without explicit DPI-awareness:
1. Fast screen grabbers (`mss`) capture at **physical resolution** ($3840 \times 2160$).
2. The AI vision model identifies a target button at $(1500, 800)$ on the physical image.
3. `PyAutoGUI` dispatches the cursor to $(1500, 800)$ in **logical coordinate space**.
4. Result: The mouse clicks at physical location $(2250, 1200)$—completely missing the target!

### 2.3. Per-Monitor DPI Awareness Initialization on Windows

Always execute DPI awareness registration before any screen capture or coordinate evaluation:

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

### 2.4. macOS Retina Scaling
On macOS, Pillow and PyAutoGUI operate in logical points, whereas `mss` captures raw Retina pixels (2x factor). Normalize coordinates via:
$$\text{click\_x} = \frac{x_{\text{mss}}}{2}, \quad \text{click\_y} = \frac{y_{\text{mss}}}{2}$$

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

### 3.2. Monitor Representation in `mss`
In `mss`, monitor indices follow this convention:
- `monitors[0]`: Entire virtual desktop encompassing all connected displays.
- `monitors[1]`: Primary monitor.
- `monitors[2..N]`: Additional secondary displays.

Each monitor profile provides:
```python
{"left": int, "top": int, "width": int, "height": int}
```

### 3.3. Mapping Local Bounding Boxes to Global Coordinates

When targeting a specific monitor `K`:
1. Capture target display: `bbox = sct.monitors[K]`.
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

1. **Bootstrap**: Execute `enable_dpi_awareness()`.
2. **Identify Target Monitor**: Retrieve display geometry via `mss.monitors`.
3. **Capture**: Capture image and record metadata `(width, height, left, top)`.
4. **Model Optimization**: Resize if dimensions exceed threshold (`IMAGE_MAX_DIMENSION = 1920`) and preserve `scale_factor`.
5. **Inference Unpacking**:
   - For resized image coordinates: `orig_x = model_x / scale_factor`.
   - For 1000-point normalized values: `orig_x = (norm_x / 1000) * width`.
6. **Offset Compensation**: Add display origins: `target_x = orig_x + monitor["left"]`.
7. **Boundary Guard**: Validate that target coordinates reside within valid display geometry before clicking.
