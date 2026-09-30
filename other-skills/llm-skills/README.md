# LLM & GenAI Agent Skills (00–07) — AI Agent Toolkit for LLM & Generative AI Applications

Bộ 8 AI Agent Skills chuyên biệt cho quy trình kỹ thuật phát triển ứng dụng Mô hình Ngôn ngữ Lớn (LLM Applications) và AI Tạo sinh (Generative AI): Kiến trúc RAG (Retrieval-Augmented Generation), Hệ thống Đa tác tử (Multi-Agent Workflows), Gọi công cụ (Function Calling / Tool Use), Quản lý bộ nhớ & Context Window, Structured Outputs (Pydantic / JSON schemas), và Đánh giá chất lượng mô hình (LLM Evaluation & Guardrails).

---

## 1. Kiến Trúc & Triết Lý Cốt Lõi (Core Architecture)

Các ứng dụng LLM và GenAI có bản chất bất định (non-deterministic), nhạy cảm với context window, chi phí token và rủi ro an toàn (prompt injection, hallucination). Bộ toolkit này thiết lập các nguyên tắc chuẩn mực:

1. **Closed-Loop Orchestration**: Điều phối khép kín qua `00-llm-orchestrator`, kiểm soát 6 pipelines tiêu chuẩn, phân loại 3 nhóm yêu cầu và kiểm soát nghiêm ngặt các cổng phê duyệt (approval gates).
2. **Architecture Decoupling (Deterministic vs Probabilistic)**: Tách biệt triệt để logic nghiệp vụ xác định (text chunking, metadata normalization, Pydantic schema parsing, tool routing, guardrail filters) khỏi các lời gọi LLM xác suất. Các logic xác định có thể chạy unit test độc lập với tốc độ cao và chi phí token bằng 0.
3. **Strict LLM TDD & Exception Engine**: Kỷ luật Test-Driven Development (Red → Green → Refactor) mặc định cho mọi thành phần xác định. Tích hợp 3 tiêu chí bỏ qua TDD (Skip criteria) và luồng kiểm thử đảo chiều (Inverted TDD) cho Prompt Prototyping / Reasoning Spikes.
4. **Token Budget, Rate Limit & Resilience Discipline**: Kiểm soát cửa sổ ngữ cảnh (Context Window), bẫy lặp vô hạn gây cạn kiệt token, cơ chế retry với exponential backoff, circuit breaking và mô hình dự phòng (fallback models).
5. **Post-Review Bug Loop**: Tự động chuyển giao sang luồng sửa lỗi chuyên biệt (`05-llm-fix`) khi khâu review phát hiện lỗi nghiêm trọng (prompt injection, schema mismatch, token blowup, gian lận TDD).
6. **Harness Execution Log**: Mỗi pipeline run bắt buộc tạo log thực thi tại `docs/harness-logs/` (tạo trước khi skill đầu tiên chạy, append một section sau mỗi skill, một file cho mỗi pipeline run) — YAML handoff trong chat không thay thế được log file. Chi tiết trong `00-llm-orchestrator/references/execution-log.md`.
7. **Evaluation Regression Gate**: Thay đổi prompt/tham số retrieval/model config phải chạy golden eval set và so sánh điểm với baseline đã ghi nhận (cùng model version); tụt điểm dưới ngưỡng sẽ chặn nghiệm thu. Chi tiết trong `06-llm-test/references/evaluation-engineering.md`.

---

## 2. Ma Trận 8 Kỹ Năng & Quyền Hạn Tệp (Skill Map & Access Scopes)

| STT | Tên Kỹ Năng (Skill Name) | Vai Trò Chuyên Biệt | Phạm Vi Truy Cập Tệp (Scope) |
|---|---|---|---|
| `00` | `00-llm-orchestrator` | Master orchestrator, Domain Gatekeeper (LLM/GenAI), phân loại 3 nhóm request, điều phối 6 pipelines và bug loop | Read-only |
| `01` | `01-llm-brainstorm` | Làm rõ bài toán AI/LLM, phân tích đánh đổi (Closed vs Open-source, RAG vs Fine-tuning, Latency vs Cost), tạm dừng duyệt spec | Read-write docs (`docs/specs/`) |
| `02` | `02-llm-plan` | Tách biệt logic xác định với lời gọi LLM, lập kế hoạch rủi ro (fallback, rate limit, prompt injection), chia wave, tạm dừng duyệt plan | Read-write docs (`docs/plans/`) |
| `03` | `03-llm-implement` | Triển khai prompt templates, Pydantic schemas, vector retrieval, tool integration, chains/agents (TDD Green + Refactor). Cấm sửa bug | Read-write production code |
| `04` | `04-llm-bugfinder` | Điều tra lỗi đặc thù LLM (ảo giác, rớt ngữ cảnh, lỗi JSON schema, rò rỉ prompt injection, timeout/rate-limit), cắm probe `[DEBUG-PROBE]` và dọn sạch | Read-only (chỉ cắm probe tạm) |
| `05` | `05-llm-fix` | Kỹ năng duy nhất sửa lỗi triệt để theo RCA hoặc review report, cấm sửa test để né lỗi | Read-write production code |
| `06` | `06-llm-test` | Viết test Red trước khi code, kiểm chứng sau code khi skip/invert TDD, quản lý thư mục test chuẩn (`tests/` hoặc `test/`) | Read-write test files (`tests/` hoặc `test/`) |
| `07` | `07-llm-review` | Rà soát chuyên sâu: bảo mật prompt injection, rò rỉ API key, bẫy token vô hạn, retry backoff, gian lận TDD, trả PASS/FAIL | Read-only |

---

## 3. Sơ Đồ 6 Canonical Pipelines

```
[Request] → 00-llm-orchestrator (Domain Gate & Classification)
  │
  ├── Pipeline 1: Tính năng / Module cục bộ đơn giản
  │   └── 06-llm-test (Red) → 03-llm-implement (Green+Refactor)* → 07-llm-review
  │
  ├── Pipeline 2: Yêu cầu prompt / Kiến trúc LLM còn mơ hồ
  │   └── 01-llm-brainstorm → [Duyệt Spec] → 06-llm-test (Red) → 03-llm-implement (Green+Refactor)* → 07-llm-review
  │
  ├── Pipeline 3: Hệ thống RAG / Agent phức tạp / Rủi ro cao
  │   └── 01-llm-brainstorm → [Duyệt Spec] → 02-llm-plan → [Duyệt Plan] → [Waves TDD]* → 07-llm-review
  │
  ├── Pipeline 4: Bug chưa rõ nguyên nhân (Ảo giác, Context Drop, Lỗi Schema, Timeout)
  │   └── 04-llm-bugfinder
  │         ├── 4a (Đơn giản): 06-llm-test (Red) → 05-llm-fix (Green+Refactor)* → 07-llm-review
  │         └── 4b (Phức tạp): 02-llm-plan → [Duyệt Plan] → [Waves Bug-Fix]* → 07-llm-review
  │
  ├── Pipeline 5: Bug đã rõ nguyên nhân (Đơn giản, cục bộ)
  │   └── 06-llm-test (Red) → 05-llm-fix (Green+Refactor)* → 07-llm-review
  │
  └── Pipeline 6: Bug đã rõ nguyên nhân (Phức tạp / Toàn cục / Kiến trúc)
      └── 02-llm-plan → [Duyệt Plan] → [Waves Bug-Fix]* → 07-llm-review
```

---

## 4. Kỷ Luật TDD, Cơ Chế Bỏ Qua (Skip) & Đảo Chiều (Inverted)

### 4.1. TDD Chuẩn (Red → Green → Refactor)
Mặc định bắt buộc cho toàn bộ logic xác định trong ứng dụng LLM:
- **Parser & Schema Validation**: Pydantic models, JSON schema extraction, regex cleanup.
- **RAG Preprocessing**: Text chunking, token counting, metadata normalization, document filtering.
- **Agent & Tool Routing**: Schema đăng ký công cụ, router decision logic, tool parameter validation.
- `06-llm-test` viết test Red trước, xác nhận fail đúng lý do kỹ thuật; `03-llm-implement` / `05-llm-fix` code tối thiểu để Green rồi Refactor.

### 4.2. Điều Kiện Bỏ Qua TDD (Skip Criteria)
Chỉ được bỏ qua bước viết test Red trước nếu thỏa mãn 1 trong 3 lý do:
1. `user-request`: Người dùng yêu cầu rõ ràng không dùng TDD.
2. `no-test-framework`: Dự án chưa có test framework/eval runner và người dùng từ chối thiết lập.
3. `config-only`: Thay đổi thuần cấu hình (API keys, model parameters như `temperature`, `top_p`) hoặc chỉnh sửa câu chữ prompt tự do không có logic kiểm thử được.

**Trình tự Fallback khi Skip TDD**:
- Tính năng: `03-llm-implement` → `06-llm-test` (Scenario B - Post-Implementation Validation) → `07-llm-review`.
- Sửa lỗi: `05-llm-fix` → `06-llm-test` (Scenario A - Bug Fix Confirmation) → `07-llm-review`.
*(Ngoại trừ trường hợp `no-test-framework`, không bao giờ được bỏ qua bước test sau code).*

### 4.3. Kiểm Thử Đảo Chiều (Inverted TDD)
Áp dụng cho:
- **Prompt Prototyping & Reasoning Spikes**: Thử nghiệm khả năng suy luận của mô hình mới với zero-shot prompt hoặc chuỗi thought complex.
- **Khảo sát sinh câu trả lời tự do**: Thử nghiệm creative generation hoặc agent persona.
- Triển khai trước qua `03-llm-implement` / `05-llm-fix`, nhưng **bắt buộc `06-llm-test` phải viết test chốt chặn ngay sau đó** (deterministic assertions cho format/constraints hoặc LLM-eval benchmark assertions) để khóa hành vi, cấm bỏ qua kiểm thử.

---

## 5. Cơ Chế Sửa Bug Sau Review (Post-Review Bug Loop)

Khi `07-llm-review` trả về **FAIL** (do có ≥1 lỗi `[BLOCKING]` như rò rỉ prompt injection, lộ secret API key, nguy cơ cạn kiệt token do vòng lặp vô hạn, parser không an toàn, hoặc gian lận TDD):
1. `00-llm-orchestrator` nhận YAML handoff và tự động chuyển nhánh sang bug-fix (4a/4b/5/6).
2. Lấy root cause trực tiếp từ báo cáo review.
3. Mã nguồn sửa đổi **bắt buộc thuộc quyền của `05-llm-fix`** (tuyệt đối không dùng `03-llm-implement`).
4. Giới hạn tối đa **3 vòng lặp review-fail** liên tiếp; nếu vẫn fail thì dừng lại báo cáo người dùng.

---

## 6. Chính Sách Thư Mục Lưu Test (Test Directory Location Policy)

Thứ tự ưu tiên vị trí thư mục test:
1. **Quy ước dự án ưu tiên khi rõ ràng** — layout test hiện có (test colocated với code, cấu trúc monorepo package, hoặc đường dẫn test đã cấu hình trong runner) được tuân thủ nguyên trạng.
2. `tests/` — Nếu đã tồn tại trực tiếp dưới thư mục gốc.
3. `test/` — Nếu `tests/` chưa có, nhưng `test/` đã tồn tại.
4. Tạo mới `tests/` trực tiếp dưới thư mục gốc nếu không có quy ước nào và cả hai chưa có.
*(Nghiêm cấm lưu file test rải rác ngoài thư mục quy chuẩn; monorepo thì test nằm trong package bị thay đổi).*

---

## 7. Quy Chuẩn Ngôn Ngữ & Artifacts

- **Tài liệu hướng dẫn & Skill definition**: Tiếng Anh chuyên ngành chuẩn (`SKILL.md`, `references/`).
- **Nội dung Artifact**: `docs/specs/spec-<name>.md` và `docs/plans/plan-<name>.md` viết 100% bằng **Tiếng Việt Markdown**.
- **Cổng phê duyệt (Approval Gates)**:
  - `01-llm-brainstorm`: Khảo sát luôn có lựa chọn write-in; tóm tắt và dừng chờ duyệt trước khi tạo spec.
  - `02-llm-plan`: Tách biệt logic xác định và lời gọi mô hình; lập kế hoạch rủi ro LLM; dừng chờ duyệt trước khi thực thi bất kỳ wave code nào.
