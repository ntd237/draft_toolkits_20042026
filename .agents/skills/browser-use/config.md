# Browser-Use Configuration & Operational Policies

All operational parameters, timeout policies, retry mechanisms, file paths, and security filters for the `browser-use` skill are centralized in this configuration file. Hardcoding operational values into instructions or scripts is strictly prohibited.

---

## 1. Browser Environment & Session Parameters

| Parameter | Type | Default Value | Description |
|---|---|---|---|
| `browser_engine` | string | `"chromium"` | Target browser engine (`chromium`, `firefox`, `webkit`). |
| `headless` | boolean | `true` | Headless execution flag (set to `false` for visual inspection). |
| `viewport_width` | integer | `1280` | Standard viewport width in pixels. |
| `viewport_height` | integer | `800` | Standard viewport height in pixels. |
| `device_scale_factor` | float | `1.0` | Display pixel density ratio (DPI scaling). |
| `user_agent` | string | `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"` | Standard User-Agent identifier string. |
| `ignore_https_errors` | boolean | `false` | Ignore invalid SSL certificates for local/staging environments. |
| `locale` | string | `"en-US"` | Browser interface locale. |
| `timezone_id` | string | `"Asia/Ho_Chi_Minh"` | Default timezone identifier for browser context. |

---

## 2. Timeouts & Synchronization Policies

| Policy Key | Type | Value (ms) | Description |
|---|---|---|---|
| `navigation_timeout_ms` | integer | `30000` | Maximum wait time for page loading and navigation. |
| `action_timeout_ms` | integer | `10000` | Maximum wait time for user interactions (click, fill, hover, select). |
| `element_wait_timeout_ms` | integer | `5000` | Maximum wait time when querying an element by selector. |
| `network_idle_timeout_ms` | integer | `5000` | Maximum wait time for network requests to settle into quiet state. |
| `network_quiet_window_ms` | integer | `500` | Consecutive quiet window with no new requests required to satisfy network idle. |
| `dom_hydration_timeout_ms` | integer | `8000` | Maximum wait time for client-side frontend framework hydration. |
| `animation_settle_timeout_ms` | integer | `300` | Wait duration for CSS transitions/animations to finish settling before click. |

---

## 3. Retry & Flakiness Recovery Policies

| Policy Key | Type | Value | Description |
|---|---|---|---|
| `max_action_retries` | integer | `3` | Maximum retry attempts for transiently failed operations. |
| `retry_backoff_base_ms` | integer | `1000` | Base wait time before the first retry attempt. |
| `retry_backoff_multiplier` | float | `1.5` | Exponential backoff multiplier across consecutive retries. |
| `retryable_errors` | list | `["TimeoutError", "TargetClosedError", "ElementNotInteractableError", "StaleElementReferenceError"]` | Explicit list of recoverable exceptions eligible for auto-retry. |

---

## 4. File System & Artifact Paths

| Setting | Type | Value | Description |
|---|---|---|---|
| `artifact_base_dir` | string | `".browser_session"` | Root directory storing session evidence and diagnostic artifacts. |
| `screenshot_dir` | string | `".browser_session/screenshots"` | Directory storing pre-action, post-action, and failure screenshots. |
| `telemetry_dir` | string | `".browser_session/telemetry"` | Directory storing raw console and network telemetry logs (JSON). |
| `dom_snapshot_dir` | string | `".browser_session/snapshots"` | Directory storing pruned DOM and Accessibility tree snapshots. |
| `downloads_dir` | string | `".browser_session/downloads"` | Directory storing exported and downloaded files. |
| `trace_dir` | string | `".browser_session/traces"` | Directory storing Playwright execution trace archives (`trace.zip`). |
| `filename_timestamp_format` | string | `"%Y%m%d_%H%M%S"` | Timestamp format string for artifact filenames. |
| `screenshot_format` | string | `"png"` | Visual evidence image format (`png` or `jpeg`). |
| `screenshot_full_page` | boolean | `true` | Capture full scrollable page on error diagnoses. |
| `enable_tracing` | boolean | `true` | Record comprehensive Playwright execution traces (screenshots, snapshots, sources). |

---

## 5. Security & Sensitive Data Redaction Policies

| Rule | Type | Pattern / Value | Action |
|---|---|---|---|
| `mask_auth_headers` | regex | `"(?i)(authorization:\s*(Bearer|Basic)\s+)[^\s\r\n]+"` | Replaces authorization token with `[REDACTED_BEARER_TOKEN]`. |
| `mask_cookie_values` | regex | `"(?i)(cookie:\s*.*?(sessionid|token|jwt|auth)=)[^;\s]+"` | Replaces session cookie values with `[REDACTED_COOKIE]`. |
| `mask_json_tokens` | regex | `"\"(token|access_token|secret|password|apiKey)\":\s*\"[^\"]+\""` | Replaces sensitive JSON property values with `"[REDACTED_SECRET]"`. |
| `mask_password_inputs` | boolean | `true` | Strictly forbids logging raw character inputs targeted at `input[type="password"]`. |

---

## 6. HTTP Status & Network Error Classification

| Category | HTTP Codes / Error Signals | Diagnostic Severity | Recommended Handling |
|---|---|---|---|
| `CLIENT_ERROR` | `400`, `401`, `403`, `404`, `422` | Warning / Critical | Verify authentication credentials, permissions, or requested endpoint URL. |
| `SERVER_ERROR` | `500`, `502`, `503`, `504` | Critical | Identify backend service fault, extract request payload and response body. |
| `CORS_ERROR` | `CORS policy blocked`, `Missing Allow-Origin` | High | Inspect preflight `OPTIONS` request and server response headers. |
| `NETWORK_TIMEOUT` | `ERR_CONNECTION_TIMED_OUT`, `ERR_NAME_NOT_RESOLVED` | High | Diagnose network reachability, DNS configuration, or service availability. |
