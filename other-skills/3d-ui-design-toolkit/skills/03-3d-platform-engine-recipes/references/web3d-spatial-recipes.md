# Web3D Spatial UI Recipes (Three.js, R3F, Babylon.js & Spline)

Integration recipes for embedding responsive, interactive 3D interfaces into modern web applications.

---

## 1. React Three Fiber (R3F) & Three.js Architecture

Web3D interfaces typically bridge standard DOM HTML and 3D WebGL/WebGPU canvases.

### 1.1. In-Canvas 3D Spatial UI (`@react-three/drei`)
For floating interactive elements embedded directly into the 3D scene graph:

```tsx
import { Html, Text } from '@react-three/drei'

// 1. Projected 3D Text (Troika MSDF)
export function SpatialLabel({ text, position }) {
  return (
    <Text
      position={position}
      fontSize={0.14} // 14cm in world space
      lineHeight={1.5} // Vietnamese diacritics safety
      font="/fonts/BeVietnamPro-SemiBold.woff"
      color="#FFFFFF"
      anchorX="center"
      anchorY="middle"
    >
      {text}
    </Text>
  )
}

// 2. Transformed HTML Component in 3D Space
export function SpatialCard({ position, children }) {
  return (
    <Html
      position={position}
      transform // Projects HTML directly into 3D world space
      occlude // Automatically hides when obstructed by 3D meshes
      distanceFactor={1.5} // Normalizes apparent scale across distance
    >
      <div className="spatial-glass-card">
        {children}
      </div>
    </Html>
  )
}
```

### 1.2. Hybrid Viewport Overlay
- **Pattern**: Render 3D scene in background `<Canvas>`; render HUD controls (camera angle resets, part selector, price display) in high-speed 2D HTML/CSS above the canvas.
- **Bi-directional Sync**: Use Zustand or lightweight reactive state to pass mouse raycast hover events from 3D canvas to 2D UI panels without re-rendering the canvas.

---

## 2. Babylon.js 3D GUI Module

Babylon.js provides a dedicated, highly optimized 3D GUI manager (`BABYLON.GUI.GUI3DManager`):

```javascript
// Initialize 3D GUI Manager
const manager = new BABYLON.GUI.GUI3DManager(scene);

// Create Holographic 3D Button
const button = new BABYLON.GUI.HolographicButton("spatialBtn");
manager.addControl(button);
button.position = new BABYLON.Vector3(0, 1.2, 2.0); // 1.2m height, 2m depth
button.text = "Khám phá mô hình"; // Vietnamese text

// Configure Hover and Click
button.onPointerEnterObservable.add(() => {
    button.scaling = new BABYLON.Vector3(1.05, 1.05, 1.05);
});
```

---

## 3. Spline 3D Web Integration

For artistic interactive 3D models with embedded UI hotspots:
- Export with **Runtime API**: Embed via `@splinetool/react-spline`.
- Bind UI events: Listen to `onSplineMouseDown` on specific 3D mesh object names (e.g., `"Hotspot_Engine"`, `"Door_Handle"`).
- Smooth camera orbit: Trigger pre-configured Spline camera state transitions on 2D button clicks.
