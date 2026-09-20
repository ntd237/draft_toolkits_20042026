# Web Flakiness Mitigation & Stability Guide

Comprehensive technical reference covering methods to eliminate flaky test behaviors, handle race conditions, stabilize dynamic animations, and implement controlled retry policies.

---

## 1. Root Causes of Web Flakiness

Erratic automation behaviors typically stem from 4 technical phenomena:

| Failure Root Cause | Underlying Mechanism | Typical Symptoms | Standard Resolution |
|---|---|---|---|
| **Hydration Gap** | HTML is server-rendered (SSR), but the client JavaScript bundle has not finished attaching event handlers. | Element is visible; clicks do not error but trigger no state change. | Await framework hydration completion or check readiness flags (e.g., `[data-hydrated="true"]`). |
| **Animation Blocking Pointer Events** | Active CSS transitions or transforms alter coordinates during interaction. | `element is not receiving pointer events` or clicking incorrect overlay layers. | Await element bounding box stabilization or listen for `transitionend`. |
| **API Race Conditions** | Subsequent steps execute before asynchronous network calls resolve. | Stale data renders, empty tables display, or infinite spinners persist. | Await targeted API responses via `waitForResponse`. |
| **Stale Element Reference** | Client framework re-renders and swaps DOM nodes during agent evaluation. | `Element is detached from DOM` or `TargetClosed`. | Re-query elements through automated retry wrappers. |

---

## 2. Smart Synchronization Mechanisms (Zero Fixed Sleeps)

**Strict Policy:** Never introduce arbitrary fixed delays (`sleep(5000)` or unconditional `page.waitForTimeout`). All waits must bind to explicit state conditions:

### 2.1 Explicit Element State Wait
```javascript
// Await full visibility and readiness (visible and interactive)
await locator.waitFor({
  state: 'visible',
  timeout: config.element_wait_timeout_ms
});
```

### 2.2 Targeted Network Response Synchronization
Instead of waiting for arbitrary network silence, await the specific business API endpoint:
```javascript
const [response] = await Promise.all([
  page.waitForResponse(resp => resp.url().includes('/api/v1/orders') && resp.status() === 200, {
    timeout: config.network_idle_timeout_ms
  }),
  submitButton.click()
]);
const orderData = await response.json();
```

### 2.3 Custom Function Polling
Used to evaluate internal application flags or DOM stabilization states:
```javascript
await page.waitForFunction(() => {
  const spinner = document.querySelector('.loading-spinner');
  return !spinner || window.getComputedStyle(spinner).display === 'none';
}, { timeout: config.dom_hydration_timeout_ms });
```

---

## 3. Dynamic Animation Settling

When interacting with expanding accordions, slide-out drawers, or fading modals:
```javascript
async function waitForElementToSettle(locator, timeout = 3000) {
  const startTime = Date.now();
  let previousBox = null;

  while (Date.now() - startTime < timeout) {
    const currentBox = await locator.boundingBox();
    if (!currentBox) throw new Error('Element is not currently rendered in layout');

    if (previousBox &&
        previousBox.x === currentBox.x &&
        previousBox.y === currentBox.y &&
        previousBox.width === currentBox.width &&
        previousBox.height === currentBox.height) {
      // Coordinates and dimensions have remained identical across sampling windows
      return;
    }
    previousBox = currentBox;
    await page.waitForTimeout(config.animation_settle_timeout_ms); // short sampling interval
  }
  throw new Error(`Element failed to stabilize position within ${timeout}ms`);
}
```

---

## 4. Controlled Retry Pattern

When an operation triggers an exception matching the `retryable_errors` list in [config.md](../config.md):
- Apply exponential backoff with a base interval.
- Do not retry unrecoverable failures (e.g., permanent 401 Unauthorized or strict schema assertion failures).

```javascript
async function executeWithRetry(actionFn, actionName, maxRetries = 3) {
  let attempt = 0;
  while (attempt < maxRetries) {
    try {
      return await actionFn();
    } catch (error) {
      attempt++;
      const isRetryable = config.retryable_errors.some(errName => error.name.includes(errName) || error.message.includes(errName));
      if (!isRetryable || attempt >= maxRetries) {
        console.error(`[CRITICAL] Operation '${actionName}' failed after ${attempt} attempts:`, error.message);
        throw error;
      }
      const delayMs = config.retry_backoff_base_ms * Math.pow(config.retry_backoff_multiplier, attempt - 1);
      console.warn(`[RETRY] Operation '${actionName}' encountered recoverable error. Retrying ${attempt}/${maxRetries} after ${delayMs}ms...`);
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
}
```

---

## 5. Step-by-Step Bug Reproduction Protocol

When investigating intermittent defects or reported web bugs:
1. **Initialize Clean Context:**
   - Launch an isolated browser context free of cached storage or stale cookies.
2. **Activate Comprehensive Telemetry:**
   - Attach console listeners, network request/response tracking, and pre/post action screenshots.
3. **Execute Minimal Reproduction Script:**
   - Capture pre-action screenshot prior to each action.
   - Capture post-action screenshot following each action.
4. **Symptom Verification & Fault Triggering:**
   - If the defect manifests: immediately dump the accessibility snapshot, console errors, and failed network payloads.
   - If the defect fails to reproduce: replay the sequence under simulated Network Throttling (Fast 3G) or CPU Throttling (4x) to provoke race conditions.
