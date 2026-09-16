# Mode B: Structured Multi-Section Context Enrichment

Comprehensive guide on processing workflow and enrichment techniques for **Mode B (Structured)**, inherited and integrated from the `enhance-prompt` skill standard.

---

## 1. When Mode B Activates

Mode B is activated when:
- The user explicitly provides flags or keywords: `--mode-b`, `--structured`, `--detailed`, `--breakdown`, `structured format`, `detailed breakdown`, `dạng cấu trúc`, `phân rã chi tiết`.
- Or the task involves highly complex technical, architectural, or AI/ML problems requiring strict separation between Role, Task, Input artifacts, Expected Output, Constraints (Must/Must NOT), and Success Criteria.

---

## 2. Execution Directives & Constraints
- **Rewrite Only**: Do NOT execute the prompt. Do NOT answer the prompt. Only rewrite it.
- **Protected Mentions Preservation**: If the prompt contains tokens of the form `⟦PLH:N⟧` (protected @-mentions), copy each token unchanged into the rewritten prompt at the same relative position. Do not delete, translate, or reformat them.

---

## 3. Strict User Language Preservation in Mode B

- **100% Language Mirroring**: The entire generated prompt in Mode B (title, task narrative, input descriptions, deliverables, constraints, success criteria, and assumption notes) **MUST strictly match the language of the user's input**.
  - **Vietnamese input &rarr; 100% Vietnamese prompt narrative**.
  - **English input &rarr; 100% English prompt narrative**.
  - **Other languages (Japanese, French, etc.) &rarr; Output in matching language**.
- Technical identifiers (frameworks, library names, functions, CLI commands, file extensions, error codes) remain uncorrupted in standard English across all languages.
- Section headings can be formatted in the user's language or with bilingual standard tags (e.g., for Vietnamese: `### 🎯 Vai trò & Bối cảnh (Role & Context)`, `### 📋 Nhiệm vụ (Task)`, `### 📥 Đầu vào (Input)`, `### 📤 Đầu ra kỳ vọng (Expected Output)`, `### ⚙️ Ràng buộc & Quy tắc (Constraints & Rules)`, `### ✅ Tiêu chí nghiệm thu (Success Criteria)`).

---

## 3. The 7 Core Dimensions

Analyze and evaluate each dimension across 3 clarity tiers: ✅ Clear / ⚠️ Inferable / ❌ Missing:

```
[1] ROLE        — Is there an appropriate domain expert persona specified? (e.g., Senior Backend Architect, AI Researcher)
[2] TASK        — Is the requested action clear, atomic, and unambiguous?
[3] CONTEXT     — Is the system background, business context, or rationale adequately established?
[4] INPUT       — Are input artifacts clearly described? (codebase, schemas, API specs, logs, configs)
[5] OUTPUT      — Is the expected deliverable format specified? (Markdown, JSON, code diffs, tables)
[6] CONSTRAINTS — Are explicit requirements (Must do) and anti-patterns (Must NOT do) defined?
[7] GOAL        — Are concrete, measurable success criteria or verification targets provided?
```

---

## 4. Programming & AI/ML Criteria (P1–P7)

For engineering and machine learning tasks, systematically audit 7 auxiliary factors:

- **[P1] Language & Version**: Python 3.11? TypeScript 5.4? Node.js 20 LTS? Go 1.22?
- **[P2] Framework & Libraries**: FastAPI, React 18, PyTorch 2.3, LangChain, Docker?
- **[P3] Runtime Environment**: OS, containerized setups, cloud provider, hardware/GPU (CUDA, VRAM)?
- **[P4] Symptoms & Error Signatures**: Exact tracebacks, runtime error codes, divergence between expected vs actual behavior?
- **[P5] Codebase Scope**: A single helper function, a specific module, or a multi-service repository?
- **[P6] Performance Budgets**: Maximum latency (p99), minimum throughput (RPS), memory/compute limits?
- **[P7] Integration Points**: Databases (PostgreSQL, MongoDB), message brokers (Kafka, Redis), Auth (OAuth2, JWT)?

---

## 5. Decision Matrix: Infer vs Ask

- **Principle**: Maximize intelligent inference to minimize unnecessary friction and turns for the user.
- **When gap is ⚠️ Inferable**: Automatically populate the most appropriate default and document it in the inline assumptions footer.
- **When gap is ❌ Missing but low-risk**: Apply the Smart Defaults Library below silently.
- **When gap is ❌ Missing AND high-risk** (e.g., conflicting tech stack choices, breaking architecture migrations): Present at most 1–2 focused multiple-choice questions (A/B/C/D) in the user's language before outputting the enriched prompt.

### Smart Defaults Library (Auto-Applied)

| Gap | Default Applied |
|---|---|
| Unspecified Output Format | Structured Markdown with syntax-highlighted code blocks |
| Unspecified Code Quality | Balanced (Clean code, idiomatic style, complete error handling, maintainable) |
| Target Audience | Senior software engineer peer |
| Testing Scope | Provide reproduction instructions / testing examples; do not enforce full test suites unless requested |
| Response Density | Concise and high-signal; avoid redundant generic introductions or conversational padding |

---

## 6. Standard Mode B Output Template

```markdown
### 🎯 Enriched Prompt (Mode B: Structured)

## [Descriptive Task Title in User Language]

### 🎯 Role & Context
- **Role**: [Target expert role]
- **Context**: [System background, operational environment, and problem statement in User Language]

### 📋 Task
[Concrete, atomic action description in User Language]

### 📥 Input
- **Artifacts / Scope**: [Target files, API contracts, database schemas]
- **Tech Stack**: [Languages, frameworks, runtime versions]

### 📤 Expected Output
- **Format**: [Structured Markdown / Self-contained Code Snippets / Architectural Diagram]
- **Deliverables**: [Explicit list of concrete artifacts to be delivered in User Language]

### ⚙️ Constraints & Rules
**Must do:**
- [Mandatory technical requirement in User Language]

**Must NOT do:**
- [Prohibited anti-pattern / Constraint boundary in User Language]

### ✅ Success Criteria
- [Verifiable targets and acceptance conditions in User Language]

---
> 💡 *Assumptions made / Ghi chú giả định: [Explicitly state inferred technical defaults in User Language]*
```

---

## 7. Real-World Transformation Examples

### Example 1: Vietnamese Input &rarr; Vietnamese Mode B Prompt
- **Raw Input**: `Tạo chức năng rate limit cho API NestJS bằng Redis --mode-b`
- **Enriched Output**:

### 🎯 Enriched Prompt (Mode B: Structured)

## Triển Khai Cơ Chế Rate Limiting Phân Tán Với NestJS và Redis

### 🎯 Role & Context
- **Role**: Senior Node.js / NestJS Backend Architect.
- **Context**: Bảo vệ hệ thống API công khai khỏi nguy cơ bị brute-force và DDoS bằng cơ chế giới hạn tần suất gọi API (Rate Limiting) dựa trên bộ nhớ chia sẻ phân tán.

### 📋 Task
Thiết kế và triển khai một Throttler Guard tùy chỉnh hoặc tích hợp thư viện `@nestjs/throttler` kết hợp `ioredis` để quản lý quota truy cập của từng client theo IP và User ID.

### 📥 Input
- **Framework**: NestJS v10.x, Node.js 20 LTS.
- **Cache Store**: Redis 7.x (kết nối cluster/standalone qua `ioredis`).
- **Target Endpoints**: Áp dụng mặc định cho toàn bộ router, đồng thời hỗ trợ override rate limit qua Custom Decorator cho các endpoint nhạy cảm (như `/auth/login`).

### 📤 Expected Output
- **Deliverables**:
  1. File cấu hình module Redis Throttler (`throttler.module.ts`).
  2. Custom Throttler Guard (`custom-throttler.guard.ts`) xử lý logic lấy IP qua header `X-Forwarded-For`.
  3. Custom Decorator cấu hình giới hạn riêng biệt (`@RateLimit(limit, ttl)`).
  4. Ví dụ áp dụng trực tiếp trên Controller và hướng dẫn kiểm thử bằng Apache Bench hoặc cURL.

### ⚙️ Constraints & Rules
**Must do:**
- Bắt buộc trả về HTTP Header chuẩn: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
- Trả về mã lỗi chuẩn `429 Too Many Requests` kèm payload JSON thân thiện khi vượt ngưỡng.
- Xử lý lỗi kết nối Redis an toàn (graceful fallback: nếu Redis sập thì ghi log cảnh báo và không làm gián đoạn request của người dùng).

**Must NOT do:**
- Không lưu trạng thái rate limit trong in-memory bộ nhớ process (tránh mất đồng bộ khi scale nhiều instance).
- Không chặn toàn bộ request khi Redis gặp sự cố gián đoạn mạng tạm thời.

### ✅ Success Criteria
- Gửi 100 request liên tiếp vượt ngưỡng cấu hình, hệ thống trả về đúng HTTP 429 sau khi chạm hạn mức.
- Header phản hồi hiển thị chính xác số lượt gọi còn lại và thời gian reset quota.

---
> 💡 *Assumptions made: NestJS 10, ioredis 5.x, reverse proxy Nginx.*

---

### Example 2: English Input &rarr; English Mode B Prompt
- **Raw Input**: `Create rate limiting for NestJS API with Redis --mode-b`
- **Enriched Output**:

### 🎯 Enriched Prompt (Mode B: Structured)

## Distributed Rate Limiting Implementation with NestJS and Redis

### 🎯 Role & Context
- **Role**: Senior Node.js / NestJS Backend Architect.
- **Context**: Protect public-facing API endpoints against brute-force abuse and volumetric DDoS traffic by implementing a distributed rate limiting layer backed by shared memory cache.

### 📋 Task
Design and implement a custom Throttler Guard or configure `@nestjs/throttler` with `ioredis` to manage client quota by IP address and authenticated User ID across horizontal instances.

### 📥 Input
- **Framework**: NestJS v10.x on Node.js 20 LTS.
- **Cache Store**: Redis 7.x (standalone or cluster setup accessed via `ioredis`).
- **Target Endpoints**: Global default limit for all incoming routes, with custom decorator overrides for sensitive endpoints (e.g., `/auth/login`).

### 📤 Expected Output
- **Deliverables**:
  1. Configured Redis Throttler storage provider module (`throttler.module.ts`).
  2. Custom Throttler Guard (`custom-throttler.guard.ts`) with robust IP resolution handling `X-Forwarded-For` reverse proxy headers.
  3. Reusable parameter decorator for endpoint-specific limits (`@RateLimit(limit, ttl)`).
  4. Controller usage examples and benchmark verification commands using cURL or Apache Bench.

### ⚙️ Constraints & Rules
**Must do:**
- Return standard rate-limiting headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.
- Return HTTP `429 Too Many Requests` with a structured JSON error response when quota is exceeded.
- Implement graceful degradation: if Redis becomes temporarily unreachable, log an alert and fall back to open pass-through without failing active user requests.

**Must NOT do:**
- Do not store rate limit state in single-process local memory (prevents quota desynchronization across scaled replicas).
- Do not block client request pipelines on transient Redis network timeouts.

### ✅ Success Criteria
- Sending 100 consecutive requests exceeding the threshold consistently returns HTTP 429 once the quota is exhausted.
- Response headers accurately reflect remaining allowances and TTL reset timestamps.

---
> 💡 *Assumptions made: NestJS 10, ioredis 5.x, Nginx reverse proxy architecture.*
