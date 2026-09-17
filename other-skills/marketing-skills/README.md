# Bộ Marketing Skill Toolkit (Agency Model)

Bộ công cụ 23 AI Agent Skills chuyên biệt cho phòng ban Tiếp thị / Agency đa ngành, được thiết kế theo kiến trúc module hóa khép kín (Closed-Loop System).

---

## 1. Cấu Trúc Thư Mục & Phân Nhóm Chức Năng

Toàn bộ các skill được lưu trữ tại `other-skills/marketing-skills/`:

```
marketing-skills/
├── config.md                              # Cấu hình trung tâm (Single Source of Truth)
├── 00-marketing-orchestrator/            # Master Orchestrator điều phối chiến dịch end-to-end
│   ├── SKILL.md
│   └── config.md
│
├── [Nhóm A: Market & Customer Insight]
│   ├── insight-build-icp/                 # Xây dựng chân dung ICP & Persona cards
│   ├── insight-analyze-competitor/        # Phân tích đối thủ & Ma trận khoảng trống thị trường
│   ├── insight-scan-market-trend/         # Quét xu hướng tìm kiếm & Social listening
│   └── insight-map-customer-journey/      # Thiết kế bản đồ hành trình khách hàng 5 giai đoạn
│
├── [Nhóm B: Content Marketing & Copywriting]
│   ├── content-plan-editorial-calendar/   # Lập kế hoạch lịch biên tập đa kênh theo phễu
│   ├── content-write-longform-seo/        # Viết bài blog/article chuyên sâu chuẩn SEO
│   ├── content-write-short-copy/          # Sáng tạo short copy (AIDA, PAS, BAB) với 3-5 biến thể test
│   ├── content-adapt-multichannel/        # Repurpose nội dung gốc sang TikTok, Carousel, Newsletter
│   └── content-audit-brand-voice/         # Audit và hiệu đính tính nhất quán của giọng điệu thương hiệu
│
├── [Nhóm C: SEO & Performance Ads]
│   ├── seo-research-keyword-cluster/      # Nghiên cứu & phân cụm từ khóa Topic Cluster / Silo
│   ├── seo-audit-technical-onpage/        # Audit kỹ thuật SEO On-page, Schema, Core Web Vitals
│   ├── ads-structure-campaign/            # Thiết kế kiến trúc chiến dịch Meta/Google Ads đa tầng
│   ├── ads-generate-creative-brief/       # Tạo brief sáng tạo chi tiết cho Designer & Video Editor
│   └── ads-diagnose-underperformance/     # Chẩn đoán nguyên nhân gốc rễ khi Ads kém hiệu quả (RCA)
│
├── [Nhóm D: CRM & Lifecycle/Email Marketing]
│   ├── crm-segment-customer-list/         # Phân khúc khách hàng đa chiều theo mô hình RFM
│   ├── lifecycle-design-automation-flow/  # Thiết kế sơ đồ luồng tự động hóa tiếp thị vòng đời
│   ├── email-write-sequence-copy/         # Soạn thảo nội dung hoàn chỉnh cho chuỗi email tiếp thị
│   └── crm-audit-lifecycle-health/        # Đánh giá sức khỏe hệ thống CRM và khả năng gửi thư
│
└── [Nhóm E: Marketing Analytics & CRO]
    ├── analytics-build-campaign-report/   # Báo cáo hiệu quả chiến dịch hợp nhất đa kênh
    ├── analytics-attribute-conversion-path/# Phân tích quy kết chuyển đổi đa điểm chạm (Attribution)
    ├── cro-audit-landing-page/            # Heuristic audit tối ưu hóa tỷ lệ chuyển đổi trang đích
    └── cro-design-ab-test/                # Thiết kế kế hoạch thử nghiệm A/B test chuẩn thống kê
```

---

## 2. Bảng Danh Mục Đầy Đủ 22 Skill + 1 Orchestrator

| Nhóm | Tên Skill | Mức độ ưu tiên | Tệp Deliverable Được Tạo Ra |
|---|---|---|---|
| **Điều phối** | `00-marketing-orchestrator` | Must-have | `docs/marketing-projects/<client-slug>/campaign-plan.md` |
| **A - Insight** | `insight-build-icp` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/insight/icp.md` |
| **A - Insight** | `insight-analyze-competitor` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/insight/competitor-audit.md` |
| **A - Insight** | `insight-scan-market-trend` | 🥉 Nice-to-have | `docs/marketing-projects/<client-slug>/insight/trend-report.md` |
| **A - Insight** | `insight-map-customer-journey` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/insight/customer-journey.md` |
| **B - Content** | `content-plan-editorial-calendar` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/content/editorial-calendar.md` |
| **B - Content** | `content-write-longform-seo` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md` |
| **B - Content** | `content-write-short-copy` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/content/short-copy/<campaign-slug>.md` |
| **B - Content** | `content-adapt-multichannel` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/content/multichannel-pack/<topic-slug>.md` |
| **B - Content** | `content-audit-brand-voice` | 🥉 Nice-to-have | `docs/marketing-projects/<client-slug>/content/brand-voice-audit.md` |
| **C - SEO/Ads** | `seo-research-keyword-cluster` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/seo-ads/keyword-clusters.md` |
| **C - SEO/Ads** | `seo-audit-technical-onpage` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/seo-ads/technical-seo-audit.md` |
| **C - SEO/Ads** | `ads-structure-campaign` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/seo-ads/campaign-structure.md` |
| **C - SEO/Ads** | `ads-generate-creative-brief` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/seo-ads/creative-briefs/<brief-id>.md` |
| **C - SEO/Ads** | `ads-diagnose-underperformance` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/seo-ads/ads-diagnosis.md` |
| **D - CRM** | `crm-segment-customer-list` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/crm/customer-segments.md` |
| **D - CRM** | `lifecycle-design-automation-flow` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/crm/automation-flows/<flow-slug>.md` |
| **D - CRM** | `email-write-sequence-copy` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/crm/email-sequences/<sequence-slug>.md` |
| **D - CRM** | `crm-audit-lifecycle-health` | 🥉 Nice-to-have | `docs/marketing-projects/<client-slug>/crm/lifecycle-health-report.md` |
| **E - Analytics**| `analytics-build-campaign-report` | 🥇 Must-have | `docs/marketing-projects/<client-slug>/analytics/campaign-report.md` |
| **E - Analytics**| `analytics-attribute-conversion-path` | 🥉 Nice-to-have | `docs/marketing-projects/<client-slug>/analytics/attribution-model.md` |
| **E - Analytics**| `cro-audit-landing-page` | 🥈 Should-have | `docs/marketing-projects/<client-slug>/analytics/landing-page-cro.md` |
| **E - Analytics**| `cro-design-ab-test` | 🥉 Nice-to-have | `docs/marketing-projects/<client-slug>/analytics/ab-test-plan.md` |

---

## 3. Quy Trình Vận Hành Khép Kín (Closed-Loop Workflow)

1. **Tuần 1 — Insight & Nền tảng**: Khảo sát ICP, đối thủ, hành trình khách hàng -> Qua **Insight Gate**.
2. **Tuần 2 — Chiến lược & Kế hoạch**: Nghiên cứu từ khóa, lập lịch content, thiết kế cấu trúc Ads -> Qua **Strategy Gate**.
3. **Tuần 3-4 — Sản xuất Đa kênh**: Viết bài SEO, sáng tạo short copy, brief creative, thiết kế email flow -> Qua **Pre-Launch QA Gate**.
4. **Tuần 5 — Triển khai Chiến dịch**: Phân tệp danh sách CRM, launch Ads, khởi chạy Email flow.
5. **Tuần 6 — Đo lường & Tối ưu hóa**: Lập báo cáo đa kênh, chẩn đoán nguyên nhân nếu CPA tăng vọt, audit landing page và thiết kế A/B testing -> Đóng vòng lặp phản hồi cho chiến dịch tiếp theo.

---

## 4. Tương Thích & Vận Hành Trên Antigravity IDE

Bộ skill được tối ưu hóa đặc biệt để vận hành mượt mà trên **Antigravity IDE**:

- **Tự động hóa trình duyệt (Playwright MCP)**:
  - Tích hợp sẵn với MCP server `playwright` để tự động mở, đọc dynamic DOM (`browser_snapshot`) và chụp ảnh màn hình (`browser_take_screenshot`) đối với các website/landing page render bằng JavaScript (React, Vue, SPA).
- **Lệnh tắt `/browser` (Slash Command)**:
  - Khi nghiên cứu đối thủ trên các nền tảng có cơ chế chống bot gắt gao (Meta Ads Library, TikTok, Cloudflare CAPTCHA), người dùng có thể gõ trực tiếp lệnh `/browser` trong Antigravity IDE để mở phiên duyệt web tương tác hoặc gắn vào session cá nhân để vượt captcha.
- **Xử lý Đa phương thức (Multimodal Vision)**:
  - Hỗ trợ dán (paste) trực tiếp ảnh chụp màn hình từ clipboard hoặc kéo thả file ảnh ads vào khung chat. AI sẽ tự động kích hoạt thị giác máy tính để phân tích bố cục, Hook 3s, thông điệp và Offer của đối thủ.
