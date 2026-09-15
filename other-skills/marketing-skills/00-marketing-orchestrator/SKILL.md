---
name: 00-marketing-orchestrator
description: "Orchestrator tổng điều phối toàn bộ 22 skill marketing theo mô hình agency đa ngành. Điều phối chiến dịch marketing end-to-end qua 5 nhóm (A-Insight, B-Content, C-SEO/Ads, D-CRM, E-Analytics/CRO), quản lý approval gates, handoff dữ liệu khép kín và khởi tạo file campaign plan."
---

# 00-marketing-orchestrator: Tổng Điều Phối Toàn Diện 22 Skill Marketing Agency

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu lập kế hoạch chiến dịch marketing tổng thể, onboard khách hàng mới, triển khai chiến dịch end-to-end đa kênh, hoặc điều phối luồng công việc giữa các bộ phận marketing (Insight -> Strategy -> Production -> Launch -> Optimize).

## Bảng Ma Trận 22 Skill Marketing (Skill Map)

| Nhóm | Mã Skill | Vai trò Cốt lõi & Deliverable Chính | Tệp Deliverable Quy Chuẩn |
|---|---|---|---|
| **A. Insight** | `insight-build-icp` | Chân dung khách hàng mục tiêu & Persona cards | `docs/marketing-projects/<client-slug>/insight/icp.md` |
| **A. Insight** | `insight-analyze-competitor` | Phân tích đối thủ, positioning, pricing & gap | `docs/marketing-projects/<client-slug>/insight/competitor-audit.md` |
| **A. Insight** | `insight-scan-market-trend` | Quét xu hướng tìm kiếm, social trend & heat index | `docs/marketing-projects/<client-slug>/insight/trend-report.md` |
| **A. Insight** | `insight-map-customer-journey` | Bản đồ hành trình khách hàng 5 tầng phễu & pain points | `docs/marketing-projects/<client-slug>/insight/customer-journey.md` |
| **B. Content** | `content-plan-editorial-calendar` | Kế hoạch lịch biên tập đa kênh theo tầng phễu | `docs/marketing-projects/<client-slug>/content/editorial-calendar.md` |
| **B. Content** | `content-write-longform-seo` | Bài blog/article chuyên sâu chuẩn Semantic SEO | `docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md` |
| **B. Content** | `content-write-short-copy` | Copy ngắn, caption, ad copy A/B test (AIDA/PAS/BAB) | `docs/marketing-projects/<client-slug>/content/short-copy/<campaign-slug>.md` |
| **B. Content** | `content-adapt-multichannel` | Repurpose nội dung gốc sang video ngắn, carousel, email | `docs/marketing-projects/<client-slug>/content/multichannel-pack/<topic-slug>.md` |
| **B. Content** | `content-audit-brand-voice` | Kiểm định & chấm điểm nhất quán giọng điệu thương hiệu | `docs/marketing-projects/<client-slug>/content/brand-voice-audit.md` |
| **C. SEO/Ads** | `seo-research-keyword-cluster` | Nghiên cứu & phân cụm từ khóa Topic Cluster/Silo | `docs/marketing-projects/<client-slug>/seo-ads/keyword-clusters.md` |
| **C. SEO/Ads** | `seo-audit-technical-onpage` | Audit kỹ thuật On-page, schema, tốc độ & index | `docs/marketing-projects/<client-slug>/seo-ads/technical-seo-audit.md` |
| **C. SEO/Ads** | `ads-structure-campaign` | Kiến trúc chiến dịch quảng cáo đa tầng (Cold/Warm/Hot) | `docs/marketing-projects/<client-slug>/seo-ads/campaign-structure.md` |
| **C. SEO/Ads** | `ads-generate-creative-brief` | Bản mô tả sáng tạo cho Designer, Video Editor, KOC | `docs/marketing-projects/<client-slug>/seo-ads/creative-briefs/<brief-id>.md` |
| **C. SEO/Ads** | `ads-diagnose-underperformance` | Chẩn đoán nguyên nhân gốc rễ khi Ads kém hiệu quả (RCA)| `docs/marketing-projects/<client-slug>/seo-ads/ads-diagnosis.md` |
| **D. CRM** | `crm-segment-customer-list` | Phân khúc khách hàng RFM (VIP, Loyal, New, At-Risk) | `docs/marketing-projects/<client-slug>/crm/customer-segments.md` |
| **D. CRM** | `lifecycle-design-automation-flow` | Kiến trúc luồng automation (Welcome, Cart, Win-back) | `docs/marketing-projects/<client-slug>/crm/automation-flows/<flow-slug>.md` |
| **D. CRM** | `email-write-sequence-copy` | Soạn thảo nội dung chuỗi email theo từng bước luồng | `docs/marketing-projects/<client-slug>/crm/email-sequences/<sequence-slug>.md` |
| **D. CRM** | `crm-audit-lifecycle-health` | Đánh giá sức khỏe hệ thống CRM & khả năng gửi thư | `docs/marketing-projects/<client-slug>/crm/lifecycle-health-report.md` |
| **E. Analytics**| `analytics-build-campaign-report` | Báo cáo hiệu quả chiến dịch đa kênh & Blended ROAS | `docs/marketing-projects/<client-slug>/analytics/campaign-report.md` |
| **E. Analytics**| `analytics-attribute-conversion-path` | Phân tích quy kết đa điểm chạm & tái phân bổ ngân sách | `docs/marketing-projects/<client-slug>/analytics/attribution-model.md` |
| **E. Analytics**| `cro-audit-landing-page` | Heuristic audit tỷ lệ chuyển đổi trang đích | `docs/marketing-projects/<client-slug>/analytics/landing-page-cro.md` |
| **E. Analytics**| `cro-design-ab-test` | Kế hoạch thử nghiệm A/B test chuẩn phương pháp khoa học | `docs/marketing-projects/<client-slug>/analytics/ab-test-plan.md` |

## Workflow

### Giai đoạn 1: Khởi tạo Hồ sơ Client & Xác định Chế độ Thực thi
**Mục tiêu**: Thu thập `client_context` và xác định phạm vi chạy theo đúng quy định tại `config.md`.
- Trích xuất hoặc truy vấn người dùng các trường trong `client_context`: `client_name`, `industry`, `business_model`, `target_market`, `brand_voice_guidelines`, `key_competitors`, `budget_tier`.
- Xác định `<client-slug>` chuẩn hóa (kebab-case, không dấu, tối đa 40 ký tự) theo File System Policy trong `config.md`.
- Xác định chế độ thực thi: `full_campaign` (6 tuần), `phase_only` (theo nhóm A/B/C/D/E), hoặc `single_skill`.
- Khởi tạo file điều phối tại `docs/marketing-projects/<client-slug>/campaign-plan.md`.

### Giai đoạn 2: Điều phối Phân kỳ Theo Lộ trình Tích hợp Đủ 22 Skill
**Mục tiêu**: Kích hoạt tuần tự các skill tương ứng với từng giai đoạn và thực thi handoff dữ liệu khép kín.
- **Phân kỳ 1 — Insight & Khảo sát Nền tảng (Tuần 1)**:
  1. Kích hoạt `insight-build-icp` để tạo `insight/icp.md`.
  2. Kích hoạt `insight-analyze-competitor` để tạo `insight/competitor-audit.md`.
  3. Kích hoạt `insight-map-customer-journey` để tạo `insight/customer-journey.md`.
  4. Kích hoạt `insight-scan-market-trend` để nắm bắt xu hướng thị trường tại `insight/trend-report.md`.
  5. Kích hoạt `seo-audit-technical-onpage` để audit nền tảng website/landing page hiện có tại `seo-ads/technical-seo-audit.md`.
- **Cổng Phê duyệt 1 (Insight Gate)**: Lấy phê duyệt của người dùng về ICP, Journey và nền tảng trước khi sang bước chiến lược.
- **Phân kỳ 2 — Chiến lược & Lập Kế hoạch (Tuần 2)**:
  1. Kích hoạt `seo-research-keyword-cluster` để xây dựng topic cluster tại `seo-ads/keyword-clusters.md`.
  2. Kích hoạt `content-plan-editorial-calendar` để lập kế hoạch lịch đăng tại `content/editorial-calendar.md`.
  3. Kích hoạt `ads-structure-campaign` để thiết kế kiến trúc phân bổ ngân sách tại `seo-ads/campaign-structure.md`.
  4. Kích hoạt `crm-audit-lifecycle-health` để audit danh sách khách hàng và uy tín tên miền gửi email tại `crm/lifecycle-health-report.md`.
- **Cổng Phê duyệt 2 (Strategy Gate)**: Trình duyệt kế hoạch nội dung, kiến trúc quảng cáo và sức khỏe CRM.
- **Phân kỳ 3 — Sản xuất Nội dung, Creative & Automation (Tuần 3-4)**:
  1. Kích hoạt `content-write-longform-seo` cho các bài viết pillar và cluster.
  2. Kích hoạt `content-write-short-copy` và `ads-generate-creative-brief` cho hình ảnh/video ads.
  3. Kích hoạt `content-adapt-multichannel` để repurpose nội dung sang video ngắn và carousel.
  4. Kích hoạt `lifecycle-design-automation-flow` và `email-write-sequence-copy` cho các luồng email marketing.
  5. Kích hoạt `content-audit-brand-voice` kiểm tra điểm số nhất quán giọng điệu (ngưỡng >= 80 điểm).
- **Phân kỳ 4 — Triển khai Chiến dịch (Tuần 5)**:
  1. Kích hoạt `crm-segment-customer-list` để phân tệp danh sách RFM tại `crm/customer-segments.md`.
  2. Kiểm tra Pre-Launch QA Gate trên toàn bộ assets trước khi phát động chiến dịch.
- **Phân kỳ 5 — Đo lường, Quy kết & Tối ưu hóa (Tuần 6)**:
  1. Kích hoạt `analytics-build-campaign-report` để tổng hợp số liệu đa kênh và Blended ROAS tại `analytics/campaign-report.md`.
  2. Kích hoạt `analytics-attribute-conversion-path` để phân tích quy kết đa điểm chạm, giải quyết chồng chéo dữ liệu và tối ưu phân bổ ngân sách tại `analytics/attribution-model.md`.
  3. Khi có cảnh báo hiệu suất: Kích hoạt `ads-diagnose-underperformance` để tìm nguyên nhân gốc rễ (RCA) tại `seo-ads/ads-diagnosis.md`.
  4. Kích hoạt `cro-audit-landing-page` để bóc tách điểm nghẽn chuyển đổi tại `analytics/landing-page-cro.md`.
  5. Kích hoạt `cro-design-ab-test` để thiết lập thử nghiệm phân tách A/B chuẩn khoa học tại `analytics/ab-test-plan.md`.

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
- [ ] Insight Gate: ICP (`insight/icp.md`), Journey (`insight/customer-journey.md`), SEO Technical (`seo-ads/technical-seo-audit.md`)
- [ ] Strategy Gate: Content Calendar, Campaign Structure, CRM Health Report
- [ ] Production Gate: Content Pack, Creative Briefs, Email Sequences & Brand Voice Score >= 80
- [ ] Pre-Launch QA Gate: Segmentation Setup & Tracking Verification
- [ ] Optimization Gate: Attribution Model, RCA Report & A/B Test Plan

## Nhật Ký Điều Phối 22 Skill
| Giai đoạn | Skill Kích hoạt | Tệp Deliverable | Trạng thái | Ghi chú Handoff |
|---|---|---|---|---|
| Tuần 1 | `insight-build-icp` | `insight/icp.md` | Đã duyệt | Chuyển tiếp sang Content & Ads |
...
```

## Don'ts
- Không bỏ qua Insight Gate để chuyển thẳng sang sản xuất bài viết hay setup ads khi chưa chốt chân dung khách hàng.
- Không tự ý sinh deliverables ngoài danh mục Naming Policy quy định tại `config.md`.
- Không hardcode thông tin đặc thù ngành vào quy trình vận hành; mọi dữ liệu phải lấy động từ `client_context`.
- Không tiến hành A/B test hoặc thay đổi ngân sách ads mà không có dữ liệu chẩn đoán đạt ngưỡng tin cậy thống kê.

## Quality Checklist
- [ ] Toàn bộ 22 skill thành phần được liệt kê đầy đủ trong Bảng Ma Trận (Skill Map) và tích hợp vào Workflow.
- [ ] `campaign-plan.md` được tạo tại đúng thư mục quy định tại File System Policy.
- [ ] Toàn bộ thông tin `client_context` được xác thực đầy đủ trước khi kích hoạt các skill thành phần.
- [ ] Các cổng phê duyệt (Insight Gate, Strategy Gate, Pre-Launch Gate, Optimization Gate) được tuân thủ đúng trình tự.
- [ ] Handoff dữ liệu giữa các nhóm A -> B/C/D -> E được kết nối liền mạch.
