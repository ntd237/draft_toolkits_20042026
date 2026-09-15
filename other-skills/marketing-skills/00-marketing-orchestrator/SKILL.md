---
name: 00-marketing-orchestrator
description: "Orchestrator tổng điều phối toàn bộ bộ 22 skill marketing theo mô hình agency đa ngành. Điều phối chiến dịch marketing end-to-end qua 5 nhóm (A-Insight, B-Content, C-SEO/Ads, D-CRM, E-Analytics/CRO), quản lý approval gates, handoff dữ liệu khép kín và khởi tạo file campaign plan."
---

# 00-marketing-orchestrator: Tổng Điều Phối Chiến Dịch Marketing Agency

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu lập kế hoạch chiến dịch marketing tổng thể, onboard khách hàng mới, triển khai chiến dịch end-to-end đa kênh, hoặc điều phối luồng công việc giữa các bộ phận marketing (Insight -> Strategy -> Production -> Launch -> Optimize).

## Workflow

### Giai đoạn 1: Khởi tạo Hồ sơ Client & Xác định Chế độ Thực thi
**Mục tiêu**: Thu thập `client_context` và xác định phạm vi chạy theo đúng quy định tại `config.md`.
- Trích xuất hoặc truy vấn người dùng các trường trong `client_context`: `client_name`, `industry`, `business_model`, `target_market`, `brand_voice_guidelines`, `key_competitors`, `budget_tier`.
- Xác định `<client-slug>` chuẩn hóa (kebab-case, không dấu, tối đa 40 ký tự) theo File System Policy trong `config.md`.
- Xác định chế độ thực thi: `full_campaign` (6 tuần), `phase_only` (theo nhóm A/B/C/D/E), hoặc `single_skill`.
- Khởi tạo file điều phối tại `docs/marketing-projects/<client-slug>/campaign-plan.md`.

### Giai đoạn 2: Điều phối Phân kỳ Theo Lộ trình
**Mục tiêu**: Kích hoạt tuần tự các skill tương ứng với từng giai đoạn và thực thi handoff dữ liệu khép kín.
- **Phân kỳ 1 — Insight & Nền tảng (Tuần 1)**:
  1. Kích hoạt `insight-build-icp` để tạo `insight/icp.md`.
  2. Kích hoạt `insight-analyze-competitor` để tạo `insight/competitor-audit.md`.
  3. Kích hoạt `insight-map-customer-journey` để tạo `insight/customer-journey.md`.
  4. (Tùy chọn) Kích hoạt `insight-scan-market-trend` để tạo `insight/trend-report.md`.
- **Cổng Phê duyệt 1 (Insight Gate)**: Dừng lại lấy xác nhận của người dùng về chân dung ICP và hành trình khách hàng trước khi chuyển tiếp.
- **Phân kỳ 2 — Chiến lược & Lập Kế hoạch (Tuần 2)**:
  1. Chuyển giao ICP và Journey sang `seo-research-keyword-cluster` để tạo `seo-ads/keyword-clusters.md`.
  2. Kích hoạt `content-plan-editorial-calendar` để xây dựng `content/editorial-calendar.md`.
  3. Kích hoạt `ads-structure-campaign` để thiết kế `seo-ads/campaign-structure.md`.
- **Cổng Phê duyệt 2 (Strategy Gate)**: Trình duyệt kế hoạch nội dung và cấu trúc quảng cáo.
- **Phân kỳ 3 — Sản xuất Nội dung & Creative (Tuần 3-4)**:
  1. Kích hoạt `content-write-longform-seo` cho các bài viết pillar/cluster.
  2. Kích hoạt `content-write-short-copy` và `ads-generate-creative-brief` cho creative quảng cáo.
  3. Kích hoạt `content-adapt-multichannel` để nhân bản nội dung sang các kênh social.
  4. Kích hoạt `lifecycle-design-automation-flow` và `email-write-sequence-copy` cho email marketing.
  5. Kích hoạt `content-audit-brand-voice` kiểm tra điểm số nhất quán tone giọng.
- **Phân kỳ 4 — Triển khai Chiến dịch (Tuần 5)**:
  1. Kích hoạt `crm-segment-customer-list` để phân tệp danh sách chạy campaign.
  2. Kiểm tra Pre-Launch QA Gate trên toàn bộ assets.
- **Phân kỳ 5 — Đo lường, Phân tích & Tối ưu (Tuần 6)**:
  1. Kích hoạt `analytics-build-campaign-report` để tổng hợp số liệu đa kênh.
  2. Khi có cảnh báo hiệu suất: Kích hoạt `ads-diagnose-underperformance` nếu CPA tăng hoặc CTR giảm theo ngưỡng tại `config.md`.
  3. Kích hoạt `cro-audit-landing-page` và `cro-design-ab-test` để nâng cao tỷ lệ chuyển đổi.

### Giai đoạn 3: Cập nhật Tiến độ & Bàn giao Dự án
**Mục tiêu**: Đồng bộ kết quả thực thi vào `campaign-plan.md` và trình bày tổng kết cho người dùng.
- Ghi nhận trạng thái hoàn thành của từng deliverable theo Naming Policy trong `config.md`.
- Liệt kê các hành động tối ưu tiếp theo cho chu kỳ sau.

## Output Format
Deliverable chính được lưu tại `docs/marketing-projects/<client-slug>/campaign-plan.md`:

```markdown
# Kế Hoạch Chiến Dịch Marketing: <client_name>
- Client Slug: `<client-slug>`
- Ngành hàng: <industry> | Mô hình: <business_model>
- Chế độ thực thi: <full_campaign | phase_only | single_skill>
- Ngân sách: <budget_tier>

## Trạng Thái Deliverables & Approval Gates
- [ ] Insight Gate: ICP (`insight/icp.md`) & Journey (`insight/customer-journey.md`)
- [ ] Strategy Gate: Content Calendar & Campaign Structure
- [ ] Production Gate: Content Pack, Creative Briefs & Email Sequences
- [ ] Pre-Launch QA Gate: Brand Voice Score >= 80 & Tracking Setup
- [ ] Optimization Gate: Report & Actionable Recommendations

## Nhật Ký Điều Phối & Lộ Trình Triển Khai
| Giai đoạn | Skill Thực thi | Tệp Deliverable | Trạng thái | Ghi chú Handoff |
|---|---|---|---|---|
| Tuần 1 | `insight-build-icp` | `insight/icp.md` | Đã duyệt | Truyền sang Content & Ads |
...
```

## Don'ts
- Không bỏ qua Insight Gate để chuyển thẳng sang sản xuất bài viết hay setup ads khi chưa chốt chân dung khách hàng.
- Không tự ý sinh deliverables ngoài danh mục Naming Policy quy định tại `config.md`.
- Không hardcode thông tin đặc thù ngành vào quy trình vận hành; mọi dữ liệu phải lấy động từ `client_context`.
- Không tiến hành A/B test hoặc thay đổi ngân sách ads mà không có dữ liệu chẩn đoán đạt ngưỡng tin cậy thống kê.

## Quality Checklist
- [ ] `campaign-plan.md` được tạo tại đúng thư mục quy định tại File System Policy.
- [ ] Toàn bộ thông tin `client_context` được xác thực đầy đủ trước khi kích hoạt các skill thành phần.
- [ ] Các cổng phê duyệt (Insight Gate, Strategy Gate, Pre-Launch Gate) được tuân thủ đúng trình tự.
- [ ] Handoff dữ liệu giữa các nhóm A -> B/C/D -> E được kết nối liền mạch.
