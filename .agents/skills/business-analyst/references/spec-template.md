# BA Spec Template

## Full Mode (all 13 sections)

````markdown
# [Project / Module]: Đặc Tả Nghiệp Vụ & Kiến Trúc Giải Pháp
> Mode: [Lite/Full] — [reason].

## 1. Tổng Quan & Mục Tiêu Nghiệp Vụ
- **Bối cảnh & Vấn đề**: [Core problem statement]
- **Mục tiêu chính**: [Measurable business/operational objectives]
- **Phạm vi**: [In-Scope / Out-of-Scope]

## 2. Danh Sách Tác Nhân & Phân Quyền
| Actor / Role | Quyền hạn & Trách nhiệm | Ghi chú bảo mật |
| :--- | :--- | :--- |
| [End User / Admin] | [Role description] | [RBAC scope / Token policy] |

## 3. Luồng Nghiệp Vụ Cốt Lõi
- **Happy Path**: [Step-by-step from initiation to success]
- **Alternative / Edge Paths**: [Branching logic for invalid inputs or unmet conditions]

## 4. User Stories
- **US-01**: As a [actor], I want [capability], so that [business value].
  - Acceptance highlights: [1–3 bullets; full Gherkin in Section 9]

## 5. Sơ Đồ Quy Trình (Mermaid)
```mermaid
flowchart TD
    %% User -> Frontend -> Backend/AI Worker -> DB
```

## 6. Quy Tắc Nghiệp Vụ & Bảng Trạng Thái
- **Validation Rules**: [Format, time window, thresholds, constraints]
- **State Machine**: `DRAFT` -> `PROCESSING` -> `COMPLETED` / `FAILED` [transition triggers]

## 7. Góc Nhìn Kỹ Thuật Theo Domain
[Deep analysis for detected domain. Primary lens main sub-section; each secondary lens own sub-section.]

## 8. Xử Lý Trường Hợp Biên & Ngoại Lệ
| Kịch bản lỗi | Tác động | Cách xử lý (Fallback / Retry / Thông báo) |
| :--- | :--- | :--- |
| [Scenario] | [Impact] | [Concrete mechanism] |

## 9. Tiêu Chí Nghiệm Thu (Gherkin)
- **Scenario 1: [Happy Path]** — Given / When / Then
- **Scenario 2: [Exception]** — Given / When / Then

## 10. Yêu Cầu Phi Chức Năng & Quyền Riêng Tư
- **Performance**: [e.g. p95 API latency < 300ms]
- **Availability & Scalability**: [e.g. uptime 99.9%, concurrent users]
- **Privacy & Compliance**: [PII fields, retention, consent, data residency]
- **Security**: [AuthN/AuthZ, encryption, audit logging]

## 11. Ưu Tiên Hóa & Phạm Vi MVP (MoSCoW)
| Feature / US | Must | Should | Could | Won't |
| :--- | :---: | :---: | :---: | :---: |
| [US-01] | ✓ | | | |
- **MVP Slice**: [Minimal Must-Have set delivering end-to-end value]

## 12. Đề Xuất Thực Thể Dữ Liệu & Kiến Trúc
- **Data Model**: [User, Session, DetectionEvent, AuditLog, etc.]
- **API Contracts / Event Topics**: [REST, WebSocket, message broker]
- **Recommended Stack**: [Language, Framework, Database, AI Runtime]

## 13. Điểm Cần Xác Nhận & Bước Tiếp Theo
- [Open assumptions requiring alignment — including ALL autonomous-mode assumptions]
````

## Lite Mode (sections 1, 3, 8, 9 only)

````markdown
# [Project / Module]: Đặc Tả Nghiệp Vụ & Kiến Trúc Giải Pháp
> Mode: Lite — [reason].

## 1. Tổng Quan & Mục Tiêu Nghiệp Vụ
- **Bối cảnh & Vấn đề**: [Core problem statement]
- **Mục tiêu chính**: [Measurable business/operational objectives]
- **Phạm vi**: [In-Scope / Out-of-Scope]

## 3. Luồng Nghiệp Vụ Cốt Lõi
- **Happy Path**: [Step-by-step from initiation to success]
- **Alternative / Edge Paths**: [Branching logic for invalid inputs or unmet conditions]

## 8. Xử Lý Trường Hợp Biên & Ngoại Lệ
| Kịch bản lỗi | Tác động | Cách xử lý (Fallback / Retry / Thông báo) |
| :--- | :--- | :--- |
| [Scenario] | [Impact] | [Concrete mechanism] |

## 9. Tiêu Chí Nghiệm Thu (Gherkin)
- **Scenario 1: [Happy Path]** — Given / When / Then
- **Scenario 2: [Exception]** — Given / When / Then
````
