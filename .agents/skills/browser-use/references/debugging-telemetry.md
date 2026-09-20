# Browser Debugging & Telemetry Analysis Guide

Comprehensive technical reference covering telemetry collection, network traffic auditing, DOM/Accessibility tree snapshot extraction, visual evidence recording, Chrome DevTools Protocol (CDP), trace recording, and fault injection.

---

## 1. Console Log Collection & Classification

All messages and exceptions emitted by the browser runtime must be captured from initial context creation and classified into 4 severity tiers:

### 1.1 Attaching Console Listeners
```javascript
const consoleLogs = [];
page.on('console', msg => {
  consoleLogs.push({
    type: msg.type(), // 'error', 'warning', 'info', 'log'
    text: msg.text(),
    location: msg.location(),
    timestamp: new Date().toISOString()
  });
});

page.on('pageerror', error => {
  consoleLogs.push({
    type: 'unhandled_exception',
    text: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString()
  });
});
```

### 1.2 Classification & Action Priority
1. **Unhandled Exceptions / Page Errors (Severity: Critical):**
   - Uncaught JavaScript runtime errors (`TypeError: Cannot read properties of undefined`, `ReferenceError`).
   - Impact: Frequently causes complete UI rendering failures, unresponsive action buttons, or blank pages (White Screen of Death).
2. **Console Errors (Severity: High):**
   - `console.error()` invocations from frontend code or third-party SDKs.
   - Resource loading failures (404/403 on scripts, fonts, stylesheets).
3. **Security & CSP Warnings (Severity: Medium):**
   - Content Security Policy violations (`Refused to load script...`), missing Cookie SameSite attributes.
4. **Deprecation & Framework Warnings (Severity: Low):**
   - Deprecated web API notices, duplicate render warnings in framework development modes.

---

## 2. Network Traffic Auditing & Inspection

### 2.1 Capturing Failed Requests and HTTP Error Responses
Agents must track all anomalous or unsuccessful network events to determine underlying failure points:

```javascript
const failedRequests = [];
page.on('requestfailed', request => {
  failedRequests.push({
    url: request.url(),
    method: request.method(),
    failureText: request.failure()?.errorText || 'Unknown failure',
    resourceType: request.resourceType(),
    timestamp: new Date().toISOString()
  });
});

page.on('response', async response => {
  const status = response.status();
  if (status >= 400) {
    let responseBody = '';
    try {
      responseBody = await response.text();
    } catch (e) {
      responseBody = '[Unable to read body: connection closed or streamed]';
    }
    failedRequests.push({
      url: response.url(),
      method: response.request().method(),
      status: status,
      statusText: response.statusText(),
      postData: response.request().postData(),
      responseBody: responseBody.slice(0, 2000), // capped to prevent context overflow
      timestamp: new Date().toISOString()
    });
  }
});
```

### 2.2 Diagnosing Common Network Failure Patterns
- **401 Unauthorized / 403 Forbidden:**
  - Expired JWT token, missing `Authorization: Bearer <token>` header, or invalidated session cookie.
- **422 Unprocessable Entity / 400 Bad Request:**
  - Client payload schema mismatch or missing mandatory fields. Compare `postData` against the API specification.
- **500 Internal Server Error / 502 Bad Gateway:**
  - Backend runtime exception or upstream service failure.
- **CORS (Cross-Origin Resource Sharing) Errors:**
  - Indicated by `failureText: "net::ERR_FAILED"` accompanied by console message: `No 'Access-Control-Allow-Origin' header is present`.
  - Check whether the preflight `OPTIONS` request received valid headers from the server.
- **Connection Timeout:**
  - Aborted requests exceeding timeout thresholds (`net::ERR_CONNECTION_TIMED_OUT`).

---

## 3. DOM & Accessibility Tree Snapshot Extraction

When UI state deviates from expectations or element queries fail, reading the entire raw HTML tree wastes context tokens. Instead, extract the Accessibility Tree or scoped DOM element states:

### 3.1 Accessibility Tree Snapshot (Recommended Primary Diagnostic)
Yields a clean representation of all interactive nodes (role, accessible name, value, disabled status, focused state):
```javascript
const snapshot = await page.accessibility.snapshot({
  interestingOnly: true // eliminates purely decorative wrapper nodes
});
// Serialized to .browser_session/snapshots/a11y_snapshot_<timestamp>.json
```

### 3.2 Element State Extraction
Inspect live computed styles and visibility attributes of a problematic node:
```javascript
const elementState = await locator.evaluate(el => {
  const style = window.getComputedStyle(el);
  const rect = el.getBoundingClientRect();
  return {
    tagName: el.tagName,
    isVisible: rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none',
    opacity: style.opacity,
    pointerEvents: style.pointerEvents,
    zIndex: style.zIndex,
    boundingBox: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
    textContent: el.textContent?.trim(),
    classList: Array.from(el.classList),
    disabled: el.hasAttribute('disabled') || el.getAttribute('aria-disabled') === 'true'
  };
});
```

---

## 4. Visual Evidence Recording

Visual evidence is mandatory before and after critical actions, as well as upon encountering diagnostic failures:

1. **Pre-action Screenshot:**
   - Filename: `.browser_session/screenshots/step_{N}_pre_{action_name}.png`
2. **Post-action Screenshot:**
   - Filename: `.browser_session/screenshots/step_{N}_post_{action_name}.png`
3. **Failure Screenshot:**
   - Capture full scrollable view (`fullPage: true`) to preserve entire visual context:
     ```javascript
     await page.screenshot({
       path: `.browser_session/screenshots/error_${timestamp}.png`,
       fullPage: true
     });
     ```

---

## 5. Secrets Scrubbing & Sensitive Data Isolation

Before telemetry logs or screenshots are written to artifacts or presented to users, all content must pass through the redaction filter defined in [config.md](../config.md):

```javascript
function scrubSensitiveData(rawText) {
  if (typeof rawText !== 'string') rawText = JSON.stringify(rawText);
  return rawText
    .replace(/(authorization:\s*(Bearer|Basic)\s+)[^\s\r\n]+/gi, '$1[REDACTED_BEARER_TOKEN]')
    .replace(/(cookie:\s*.*?(sessionid|token|jwt|auth)=)[^;\s]+/gi, '$1[REDACTED_COOKIE]')
    .replace(/"(token|access_token|secret|password|apiKey)":\s*"[^"]+"/gi, '"$1":"[REDACTED_SECRET]"');
}
```
- Password Input Masking: Never log text strings typed into `input[type="password"]`.

---

## 6. Playwright Trace Recording & Chrome DevTools Protocol (CDP)

1. **Full-Timeline Trace Recording:**
   Playwright Traces provide millisecond-by-millisecond visual timelines, DOM action snapshots, and network streams:
   ```javascript
   // In Phase 1: Initialize tracing
   if (config.enable_tracing) {
     await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
   }

   // In Phase 4: Stop and persist trace archive
   if (config.enable_tracing) {
     const tracePath = `${config.trace_dir}/trace_${timestamp}.zip`;
     await context.tracing.stop({ path: tracePath });
     console.log(`Trace archive recorded at: ${tracePath}`);
   }
   ```
2. **Low-Level Telemetry via CDP Session:**
   Directly query browser performance and memory footprint:
   ```javascript
   const cdpSession = await page.context().newCDPSession(page);
   await cdpSession.send('Performance.enable');
   const { metrics } = await cdpSession.send('Performance.getMetrics');
   const heapUsed = metrics.find(m => m.name === 'JSHeapUsedSize')?.value;
   console.log(`Live JS Heap Consumption: ${(heapUsed / 1024 / 1024).toFixed(2)} MB`);
   ```

---

## 7. Fault Injection & Network Route Mocking

To verify frontend resilience against backend outages or simulate edge-case network conditions:
1. **Simulate HTTP 500 Backend Error:**
   ```javascript
   await page.route('**/api/v1/checkout', route => {
     route.fulfill({
       status: 500,
       contentType: 'application/json',
       body: JSON.stringify({ error: 'Database lock timeout' })
     });
   });
   ```
2. **Simulate Connection Drop / Aborted Request:**
   ```javascript
   await page.route('**/api/v1/metrics', route => route.abort('failed'));
   ```

---

## 8. WebSocket & EventStream (SSE) Telemetry

For real-time dashboards and chat interfaces:
```javascript
page.on('websocket', ws => {
  console.log(`WebSocket opened: ${ws.url()}`);
  ws.on('framereceived', event => console.log(`WS Incoming Frame: ${event.payload}`));
  ws.on('framesent', event => console.log(`WS Outgoing Frame: ${event.payload}`));
  ws.on('close', () => console.log('WebSocket connection terminated'));
});
```
