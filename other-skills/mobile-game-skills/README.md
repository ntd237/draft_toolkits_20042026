# Mobile Game Skills (00–07) — AI Agent Toolkit for 2D/3D Mobile Game Development

Bộ 8 AI Agent Skills chuyên biệt cho quy trình phát triển Game Mobile 2D/3D đa nền tảng (iOS & Android), tối ưu hóa cho Unity (C#), Godot (C#/GDScript) hoặc các Game Engine C++ hiện đại.

---

## 1. Kiến Trúc & Triết Lý Cốt Lõi (Core Architecture)

Phát triển game di động đòi hỏi sự cân bằng nghiêm ngặt giữa độ mượt mà gameplay, giới hạn phần cứng di động (pin, nhiệt độ, GPU TBDR) và tính ổn định trên hàng ngàn cấu hình thiết bị. Bộ toolkit này thiết lập:

1. **Closed-Loop Orchestration**: Điều phối khép kín qua `00-mobile-game-orchestrator`, kiểm soát 6 pipelines tiêu chuẩn và cổng kiểm duyệt người dùng.
2. **Architecture Decoupling**: Tách biệt logic mô phỏng game thuần (Combat, Inventory, State Machine, Game Rules) khỏi vòng lặp phụ thuộc engine (`MonoBehaviour`, `Node`, frame loop), cho phép chạy unit test cực nhanh mà không cần khởi động engine.
3. **Strict Mobile TDD & Exception Engine**: Kỷ luật Test-Driven Development (Red → Green → Refactor) mặc định, tích hợp 3 tiêu chí bỏ qua TDD (Skip criteria) và luồng kiểm thử đảo chiều (Inverted TDD) cho spikes/game feel.
4. **Zero-GC per Frame & Mobile Rendering Discipline**: Kiểm soát rác bộ nhớ (GC allocation) trong các hàm tick (`Update`, `FixedUpdate`), tối ưu hóa Draw Call batching, Sub-Canvas và bộ đệm an toàn tai thỏ (Safe Area).
5. **Post-Review Bug Loop**: Tự động chuyển giao sang luồng sửa lỗi chuyên biệt (`05-mobile-game-fix`) khi khâu review phát hiện lỗi nghiêm trọng.

---

## 2. Ma Trận 8 Kỹ Năng & Quyền Hạn Tệp (Skill Map & Access Scopes)

| STT | Tên Kỹ Năng (Skill Name) | Vai Trò Chuyên Biệt | Phạm Vi Truy Cập Tệp (Scope) |
|---|---|---|---|
| `00` | `00-mobile-game-orchestrator` | Master orchestrator, domain gatekeeper, phân loại yêu cầu, điều phối 6 pipelines và bug loop | Read-only |
| `01` | `01-mobile-game-brainstorm` | Khảo sát GDD, cơ chế cảm ứng, phân tích đánh đổi hiệu năng (Draw Calls, GC, nhiệt), tạm dừng duyệt spec | Read-write docs (`docs/specs/`) |
| `02` | `02-mobile-game-plan` | Tách biệt kiến trúc logic/engine, lập kế hoạch rủi ro đa nền tảng (iOS/Android), chia wave, tạm dừng duyệt plan | Read-write docs (`docs/plans/`) |
| `03` | `03-mobile-game-implement` | Triển khai code tính năng mới, zero-GC, object pooling, math/physics (TDD Green + Refactor). Cấm sửa bug | Read-write production code |
| `04` | `04-mobile-game-bugfinder` | Điều tra crash, freeze/ANR, tụt FPS, leak bộ nhớ, cắm probe tạm thời `// [DEBUG-PROBE]` và dọn sạch | Read-only (chỉ cắm probe tạm) |
| `05` | `05-mobile-game-fix` | Kỹ năng duy nhất sửa lỗi triệt để theo RCA hoặc review, cấm sửa test né lỗi | Read-write production code |
| `06` | `06-mobile-game-test` | Viết test Red trước khi code, kiểm chứng sau code khi skip/invert TDD, quản lý thư mục test chuẩn | Read-write test files (`tests/` hoặc `test/`) |
| `07` | `07-mobile-game-review` | Rà soát chuyên sâu: GC trong Update, Draw Call, overdraw, Safe Area, mã `#if`, gian lận TDD, trả PASS/FAIL | Read-only |

---

## 3. Sơ Đồ 6 Canonical Pipelines

```
[Request] → 00-mobile-game-orchestrator (Domain Gate & Classification)
  │
  ├── Pipeline 1: Cơ chế đơn giản, cục bộ
  │   └── 06-mobile-game-test (Red) → 03-mobile-game-implement (Green+Refactor)* → 07-mobile-game-review
  │
  ├── Pipeline 2: Yêu cầu gameplay mơ hồ
  │   └── 01-mobile-game-brainstorm → [Duyệt Spec] → 06-mobile-game-test (Red) → 03-mobile-game-implement (Green+Refactor)* → 07-mobile-game-review
  │
  ├── Pipeline 3: Hệ thống phức tạp / Rủi ro đa nền tảng
  │   └── 01-mobile-game-brainstorm → [Duyệt Spec] → 02-mobile-game-plan → [Duyệt Plan] → [Waves TDD]* → 07-mobile-game-review
  │
  ├── Pipeline 4: Bug chưa rõ nguyên nhân (Crash, ANR, tụt FPS, Leak)
  │   └── 04-mobile-game-bugfinder
  │         ├── 4a (Đơn giản): 06-mobile-game-test (Red) → 05-mobile-game-fix (Green+Refactor)* → 07-mobile-game-review
  │         └── 4b (Phức tạp): 02-mobile-game-plan → [Duyệt Plan] → [Waves Bug-Fix]* → 07-mobile-game-review
  │
  ├── Pipeline 5: Bug đã rõ nguyên nhân (Đơn giản)
  │   └── 06-mobile-game-test (Red) → 05-mobile-game-fix (Green+Refactor)* → 07-mobile-game-review
  │
  └── Pipeline 6: Bug đã rõ nguyên nhân (Phức tạp / Toàn cục)
      └── 02-mobile-game-plan → [Duyệt Plan] → [Waves Bug-Fix]* → 07-mobile-game-review
```

---

## 4. Kỷ Luật TDD, Cơ Chế Bỏ Qua (Skip) & Đảo Chiều (Inverted)

### 4.1. TDD Chuẩn (Red → Green → Refactor)
Mặc định bắt buộc cho toàn bộ logic game thuần: tính toán sát thương, kinh tế game, trạng thái nhân vật, logic nhiệm vụ, điều kiện thắng thua.
- `06-mobile-game-test` viết test Red trước, xác nhận test fail vì thiếu code.
- `03-mobile-game-implement` (tính năng) hoặc `05-mobile-game-fix` (sửa lỗi) làm xanh test và refactor.

### 4.2. Điều Kiện Bỏ Qua TDD (Skip Criteria)
Chỉ được bỏ qua bước viết test Red trước nếu thỏa mãn 1 trong 3 lý do:
1. `user-request`: Người dùng chỉ định rõ không dùng TDD.
2. `no-test-framework`: Dự án chưa có test framework và người dùng từ chối cài đặt.
3. `config-only`: Thay đổi thuần về metadata, config Gradle/Xcode, asset, layout UI tĩnh.

**Trình tự Fallback khi Skip TDD**:
- Tính năng: `03-mobile-game-implement` → `06-mobile-game-test` (Scenario B - Post-Implementation Validation) → `07-mobile-game-review`.
- Sửa lỗi: `05-mobile-game-fix` → `06-mobile-game-test` (Scenario A - Bug Fix Confirmation) → `07-mobile-game-review`.
*(Ngoại trừ trường hợp `no-test-framework`, không bao giờ được bỏ qua bước test sau code).*

### 4.3. Kiểm Thử Đảo Chiều (Inverted TDD)
Áp dụng cho:
- **Spike kỹ thuật**: Thử nghiệm shader HLSL mới, test API render engine.
- **Game Feel & Visual Juice**: Tinh chỉnh rung màn hình (camera shake), hiệu ứng hạt (particles), cảm giác nảy/easing.
- Code trước, nhưng bắt buộc `06-mobile-game-test` phải viết test chốt chặn ngay sau đó để chống hồi quy.

---

## 5. Cơ Chế Sửa Bug Sau Review (Post-Review Bug Loop)

Khi `07-mobile-game-review` trả về **FAIL** (do có ≥1 lỗi `[BLOCKING]` như memory leak trong tick, crash native, lỗi Safe Area, hoặc gian lận TDD):
1. `00-mobile-game-orchestrator` nhận YAML handoff và tự động chuyển nhánh sang bug-fix (4a/4b/5/6).
2. Lấy root cause trực tiếp từ báo cáo review.
3. Mã nguồn sửa đổi **bắt buộc thuộc quyền của `05-mobile-game-fix`** (tuyệt đối không dùng `03-mobile-game-implement`).
4. Giới hạn tối đa **3 vòng lặp review-fail** liên tiếp; nếu vẫn fail thì dừng lại báo cáo người dùng.

---

## 6. Chính Sách Thư Mục Lưu Test (Test Directory Location Policy)

Thứ tự ưu tiên vị trí thư mục test dưới root dự án:
1. `tests/` — Nếu đã tồn tại trực tiếp dưới thư mục gốc.
2. `test/` — Nếu `tests/` chưa có, nhưng `test/` đã tồn tại.
3. Tạo mới `tests/` trực tiếp dưới thư mục gốc nếu cả hai chưa có.
*(Nghiêm cấm lưu file test rải rác ngoài thư mục quy chuẩn).*

---

## 7. Quy Chuẩn Ngôn Ngữ & Artifacts

- **Tài liệu hướng dẫn & Skill definition**: Tiếng Anh chuyên ngành chuẩn (`SKILL.md`, `references/`).
- **Nội dung Artifact**: `docs/specs/spec-<name>.md` và `docs/plans/plan-<name>.md` viết 100% bằng **Tiếng Việt Markdown**.
- **Cổng phê duyệt (Approval Gates)**:
  - `01-mobile-game-brainstorm`: Khảo sát luôn có lựa chọn write-in; tóm tắt và dừng chờ duyệt trước khi tạo spec.
  - `02-mobile-game-plan`: Tách biệt logic và engine loop; dừng chờ duyệt trước khi thực thi bất kỳ wave code nào.
