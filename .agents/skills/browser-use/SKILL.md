---
name: browser-use
description: "Comprehensive web browser automation and in-depth web application debugging/diagnosis skill. Executes robust browser interactions (semantic locators, complex gestures, multi-tab/iframe, smart synchronization) and performs deep technical diagnostics (console exceptions, network interception, DOM/A11y snapshots, visual diffs, and flakiness mitigation). Activates on keywords: browser-use, web-debug, browser-automation, inspect-network, console-errors, flaky-test, web-interaction."
---

# Browser Use & Web Debugging Skill

Closed-loop operational framework combining resilient browser automation with deep web application telemetry analysis and debugging. All runtime parameters, timeout limits, security redaction rules, and artifact schemas strictly follow [config.md](config.md).

## Language Protocol
- All internal reasoning, technical guidelines, and reference documentation are maintained in English.
- User communication and final delivered session reports (per Output Format) MUST be written in Vietnamese.
- Restate non-English user requests in English before proceeding with internal execution.

## Trigger
Activates when the user requests browser automation, navigation, web interaction, DOM inspection, console log extraction, network API monitoring, debugging flaky web behaviors, or when the following keywords appear: `browser-use`, `web-debug`, `browser-automation`, `inspect-network`, `console-errors`, `flaky-test`, `web-interaction`.

## Workflow

```
[Phase 1: Init & Session Guard] ──> [Phase 2: Action & Smart Sync]
                │                                    │
                └─── (Guaranteed Cleanup on Error) ──┴──> [Phase 3: Telemetry & Diagnosis]
                                                                    │
                                                                    ▼
                                                          [Phase 4: Teardown & Report]
```

### Phase 1: Initialization & Session Guard
**Objective**: Load operational parameters, spawn an isolated browser context, initialize execution tracing, and attach comprehensive telemetry listeners prior to navigation.

1. Ingest all runtime parameters from [config.md](config.md) (`viewport`, `timeouts`, `trace_dir`, `downloads_dir`, `user_agent`, `ignore_https_errors`).
2. Spawn an isolated, incognito browser context (cleared cookies, cache, and local storage).
3. If session bypass or authenticated testing is requested, inject cookies, headers, or web storage per [references/interactions-advanced.md](references/interactions-advanced.md).
4. Initialize execution tracing via `context.tracing.start({ screenshots: true, snapshots: true, sources: true })` per [references/debugging-telemetry.md](references/debugging-telemetry.md).
5. Attach telemetry event listeners per [references/debugging-telemetry.md](references/debugging-telemetry.md):
   - Listen to `page.on('console')` and `page.on('pageerror')` to capture uncaught JavaScript runtime exceptions and warnings.
   - Listen to `page.on('requestfailed')` and `page.on('response')` to log failed requests, CORS issues, and HTTP status codes >= 400.
   - Attach `page.on('dialog')` for native dialogs and `page.on('websocket')` for live streaming channels.
6. Enclose the entire execution lifecycle in a mandatory `try...finally` block to guarantee graceful browser teardown.

### Phase 2: Action Execution & Smart Synchronization
**Objective**: Resolve target elements via the resilient locator hierarchy and execute user interactions with zero-sleep condition synchronization.

1. Resolve selectors using the 6-Tier Hierarchy in [references/selectors-guide.md](references/selectors-guide.md):
   - Prioritize Tier 1 (`getByRole` + accessible name) -> Tier 2 (`getByLabel`/`getByPlaceholder`) -> Tier 3 (`getByText`) -> Tier 4 (`getByTestId`).
   - Use semantic CSS or relative contextual XPath only as fallbacks; strictly avoid absolute XPath (`/html/body/...`) and dynamic styling hashes.
2. If elements are lazy-loaded or outside viewport, execute stepped scrolling per [references/interactions-advanced.md](references/interactions-advanced.md).
3. Capture a pre-action screenshot (`pre-action`) following the naming convention in [config.md](config.md).
4. Execute interactions per [references/interactions-advanced.md](references/interactions-advanced.md):
   - Safe input clearing (Select-All + Backspace + sequential typing) to ensure reactive synthetic events trigger properly.
   - Advanced mouse gestures (hovering flyouts, coordinate-stepped drag-and-drop, file upload via `setInputFiles`).
   - Custom HTML modal handling (Escape key, backdrop click) and file download tracking (`waitForEvent('download')`).
   - Frame traversal via `frameLocator` and multi-tab popup tracking via context event listeners.
5. Enforce smart synchronization per [references/flakiness-and-stability.md](references/flakiness-and-stability.md):
   - Replace arbitrary sleep delays with explicit state polling (`locator.waitFor({ state: 'visible' })`).
   - Synchronize on targeted network endpoints (`waitForResponse`) or poll DOM hydration and animation settling.
6. Capture a post-action screenshot (`post-action`).

### Phase 3: Telemetry Collection & Debug Diagnosis
**Objective**: Extract technical diagnostic artifacts, classify failure modes, inspect DevTools metrics, and isolate root causes.

1. If an action fails or the DOM fails to transition:
   - Capture a full-page failure screenshot (`fullPage: true`) stored in `screenshot_dir`.
   - Extract an Accessibility Tree snapshot (`page.accessibility.snapshot({ interestingOnly: true })`) or inspect element computed styles per [references/debugging-telemetry.md](references/debugging-telemetry.md).
2. Filter and categorize console telemetry:
   - Separate critical `Unhandled Exceptions` (potential rendering blocks) from standard deprecation/warnings.
3. Audit network traffic and apply fault injection if needed:
   - Isolate failed API requests (HTTP 4xx/5xx, CORS blocks, connection timeouts).
   - Extract request payloads and response bodies (capped at 2000 characters).
   - If isolating frontend error boundaries, simulate network faults via `page.route()` per [references/debugging-telemetry.md](references/debugging-telemetry.md).
4. Query low-level performance or heap metrics via Chrome DevTools Protocol (CDP) session if memory leaks or performance degradation is suspected.
5. Evaluate flakiness and race conditions per [references/flakiness-and-stability.md](references/flakiness-and-stability.md):
   - Check for hydration gaps, active CSS transitions, or detached DOM elements.
   - Execute controlled exponential retries if the failure matches `retryable_errors`.

### Phase 4: Resource Teardown & Diagnostic Reporting
**Objective**: Persist trace archives, terminate browser sessions safely, scrub sensitive credentials, and produce the final diagnostic deliverable in Vietnamese.

1. Finalize and persist the Playwright execution trace archive (`trace.zip`) into `trace_dir` per [config.md](config.md).
2. Terminate pages (`page.close()`) and close the browser instance (`browser.close()`) within the guaranteed `finally` block.
3. Apply the sensitive data redaction filter per [references/debugging-telemetry.md](references/debugging-telemetry.md):
   - Mask Bearer tokens, cookies, passwords, and API keys across all logs and report outputs.
4. Generate and present the final diagnostic deliverable in Vietnamese using the template in **Output Format**.

## Output Format

Báo cáo kết quả phiên làm việc trình duyệt phải được xuất bằng **Tiếng Việt** theo mẫu chuẩn hóa sau:

```markdown
# [Báo Cáo Phiên Trình Duyệt] - <Mục tiêu thao tác / Mã kịch bản>
- **Thời gian thực thi**: <YYYY-MM-DD HH:MM:SS>
- **URL đích**: <Target URL>
- **Trạng thái chung**: `SUCCESS` | `FAILED` | `RETRY_EXHAUSTED`

## 1. Nhật ký Thao tác (Action Execution Log)
| Bước | Thao tác | Selector / Mục tiêu | Trạng thái | Bằng chứng ảnh / File |
|---|---|---|---|---|
| 01 | Navigate | `https://example.com/login` | PASS | `step_01_post_nav.png` |
| 02 | Click | `getByRole('button', { name: 'Đăng nhập' })` | PASS | `step_02_post_click.png` |

## 2. Báo cáo Chẩn đoán & Telemetry (Telemetry Diagnostics)
- **Lỗi Runtime & Ngoại lệ (Console Exceptions)**: <Không phát hiện / Liệt kê chi tiết kèm stack trace>
- **Yêu cầu mạng thất bại (Failed Network Requests)**:
  - `[METHOD] <URL>` - Mã lỗi: `<HTTP Code>` - Chi tiết: `<Lỗi CORS / Timeout / Endpoint failure>`
  - Dữ liệu gửi lên (Payload): `<Scrubbed Payload>`
  - Phản hồi nhận về (Response): `<Scrubbed Response>`
- **Cấu trúc DOM / Snapshot Accessibility**: `<Đường dẫn tệp snapshot đã lưu>`
- **Kho lưu trữ Trace / Tệp tải về**: `<Đường dẫn tệp trace.zip hoặc file download>`

## 3. Phân tích Nguyên nhân Gốc & Khuyến nghị (Root Cause & Recommendations)
- **Hiện tượng ghi nhận (Observed Symptom)**: <Mô tả chi tiết sai lệch hành vi>
- **Nguyên nhân gốc rễ (Root Cause)**: <Do hydration gap, CORS server-side, race condition hay selector gãy>
- **Khuyến nghị khắc phục**: <Đề xuất điều chỉnh mã nguồn frontend, backend hoặc cập nhật locator>
```

## Donts

- Do not hardcode any operational timeouts, URLs, or viewport dimensions outside [config.md](config.md).
- Do not use unconditional, arbitrary fixed delays (e.g., `sleep(3000)` or hardcoded `page.waitForTimeout`) for synchronization.
- Do not use brittle absolute XPath selectors (`/html/body/...`) or CSS selectors bound to ephemeral styling hashes.
- Do not bypass browser and context teardown inside the `finally` block under error conditions.
- Do not expose sensitive credentials (Bearer tokens, session cookies, passwords, API keys) in logs, reports, or screenshots.
- Do not trigger irreversible or destructive actions (permanent file deletion, payment submission, production database writes) without prior user confirmation.

## Quality Checklist

- [ ] All operational parameters are loaded directly from [config.md](config.md) with zero hardcoded values.
- [ ] Selector resolution strictly follows the 6-Tier Hierarchy (Role > Label > Text > TestID > Semantic CSS > Relative XPath).
- [ ] Console exception, unhandled error, and network failure listeners are attached prior to navigation.
- [ ] Execution tracing (`trace.zip`) is initiated and persisted to the designated trace directory.
- [ ] All interactions synchronize on explicit element readiness, targeted network response, or hydration completion.
- [ ] Pre-action, post-action, or failure visual screenshots are properly persisted to designated artifact directories.
- [ ] Sensitive data redaction filters are applied to all telemetry streams and report payloads.
- [ ] Browser instances are guaranteed to terminate without lingering zombie processes, even upon failure.
- [ ] Final session deliverable is rendered in Vietnamese adhering strictly to the Output Format schema.
