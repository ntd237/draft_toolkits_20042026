# Marketing Toolkit Configuration

Tập tin cấu hình trung tâm (Single Source of Truth) định nghĩa toàn bộ quy định hệ thống, đường dẫn file, chính sách validation, runtime và workflow cho bộ Marketing Skill Toolkit.
Tất cả các skill trong bộ toolkit PHẢI tuân thủ các chính sách trong file này. Tuyệt đối không hardcode giá trị thuộc phạm vi runtime, validation, workflow, naming hoặc file system policy.

---

## 1. Chính sách Hệ thống Tệp (File System Policy)

- **Thư mục gốc của dự án marketing**: `docs/marketing-projects/<client-slug>/`
- **Quy tắc định danh `<client-slug>`**: chữ thường, kebab-case, không dấu, không khoảng trắng, tối đa 40 ký tự (ví dụ: `d2c-health-supplement`, `fnb-coffee-chain`).
- **Cấu trúc thư mục con theo nhóm chức năng**:
  - `insight/` — Lưu trữ kết quả nghiên cứu thị trường, ICP, đối thủ, hành trình khách hàng.
  - `content/` — Lưu trữ lịch biên tập, bài viết SEO, ad copy, nội dung đa kênh, báo cáo brand voice.
  - `seo-ads/` — Lưu trữ cụm từ khóa, audit SEO kỹ thuật, cấu trúc campaign, creative brief, chẩn đoán ads.
  - `crm/` — Lưu trữ phân khúc khách hàng, sơ đồ automation flow, chuỗi email, audit CRM.
  - `analytics/` — Lưu trữ báo cáo đa kênh, mô hình attribution, CRO audit, kế hoạch A/B test.

---

## 2. Chính sách Đặt tên Tệp & Định dạng Đầu ra (Naming Policy)

| Mã Skill | Đường dẫn Tệp Deliverable | Định dạng chính |
|---|---|---|
| `00-marketing-orchestrator` | `docs/marketing-projects/<client-slug>/campaign-plan.md` | Markdown |
| `insight-build-icp` | `docs/marketing-projects/<client-slug>/insight/icp.md` | Markdown + Persona Cards |
| `insight-analyze-competitor` | `docs/marketing-projects/<client-slug>/insight/competitor-audit.md` | Markdown + Matrix Table |
| `insight-scan-market-trend` | `docs/marketing-projects/<client-slug>/insight/trend-report.md` | Markdown + Heat Index |
| `insight-map-customer-journey` | `docs/marketing-projects/<client-slug>/insight/customer-journey.md` | Markdown + Journey Stages |
| `content-plan-editorial-calendar` | `docs/marketing-projects/<client-slug>/content/editorial-calendar.md` | Markdown Table |
| `content-write-longform-seo` | `docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md` | Markdown Article |
| `content-write-short-copy` | `docs/marketing-projects/<client-slug>/content/short-copy/<campaign-slug>.md` | Markdown Variants |
| `content-adapt-multichannel` | `docs/marketing-projects/<client-slug>/content/multichannel-pack/<topic-slug>.md` | Markdown Channel Pack |
| `content-audit-brand-voice` | `docs/marketing-projects/<client-slug>/content/brand-voice-audit.md` | Markdown Scorecard |
| `seo-research-keyword-cluster` | `docs/marketing-projects/<client-slug>/seo-ads/keyword-clusters.md` | Markdown Table / Clusters |
| `seo-audit-technical-onpage` | `docs/marketing-projects/<client-slug>/seo-ads/technical-seo-audit.md` | Markdown Audit Checklist |
| `ads-structure-campaign` | `docs/marketing-projects/<client-slug>/seo-ads/campaign-structure.md` | Markdown Hierarchy Tree |
| `ads-generate-creative-brief` | `docs/marketing-projects/<client-slug>/seo-ads/creative-briefs/<brief-id>.md` | Markdown Creative Spec |
| `ads-diagnose-underperformance` | `docs/marketing-projects/<client-slug>/seo-ads/ads-diagnosis.md` | Markdown RCA Report |
| `crm-segment-customer-list` | `docs/marketing-projects/<client-slug>/crm/customer-segments.md` | Markdown Segments + Rules |
| `lifecycle-design-automation-flow` | `docs/marketing-projects/<client-slug>/crm/automation-flows/<flow-slug>.md` | Markdown Flow Logic |
| `email-write-sequence-copy` | `docs/marketing-projects/<client-slug>/crm/email-sequences/<sequence-slug>.md` | Markdown Email Series |
| `crm-audit-lifecycle-health` | `docs/marketing-projects/<client-slug>/crm/lifecycle-health-report.md` | Markdown Metric Diagnostic |
| `analytics-build-campaign-report` | `docs/marketing-projects/<client-slug>/analytics/campaign-report.md` | Markdown Performance Summary |
| `analytics-attribute-conversion-path` | `docs/marketing-projects/<client-slug>/analytics/attribution-model.md` | Markdown Attribution Matrix |
| `cro-audit-landing-page` | `docs/marketing-projects/<client-slug>/analytics/landing-page-cro.md` | Markdown Heuristic Audit |
| `cro-design-ab-test` | `docs/marketing-projects/<client-slug>/analytics/ab-test-plan.md` | Markdown Experiment Plan |

---

## 3. Chính sách Runtime (Runtime Policy)

### 3.1. Chế độ vận hành (Execution Modes)
- `full_campaign`: Vận hành toàn diện theo lộ trình 6 tuần (Tuần 1 Insight -> Tuần 2 Strategy -> Tuần 3-4 Production -> Tuần 5 Launch -> Tuần 6 Measure & Optimize).
- `phase_only`: Vận hành theo một nhóm chức năng cụ thể (Nhóm A, B, C, D, hoặc E).
- `single_skill`: Chạy độc lập một skill deliverable theo yêu cầu trực tiếp từ user.

### 3.2. Cấu trúc Client Context bắt buộc (`client_context`)
Mỗi skill khi thực thi bắt buộc phải nhận hoặc trích xuất `client_context` từ `campaign-plan.md` hoặc input trực tiếp từ user:
- `client_name`: Tên thương hiệu/doanh nghiệp.
- `industry`: Ngành hàng hoạt động.
- `business_model`: B2B, B2C, D2C, E-commerce, Marketplace, SaaS.
- `target_market`: Thị trường mục tiêu (Việt Nam, Đông Nam Á, Toàn cầu, theo tỉnh thành).
- `target_audience_summary`: Tóm tắt tệp khách hàng mục tiêu hoặc tham chiếu `icp.md`.
- `brand_voice_guidelines`: Tone giọng (Chuyên gia, Thân thiện, Hài hước, Táo bạo, v.v.).
- `key_competitors`: Danh sách đối thủ chính.
- `budget_tier`: Ngân sách phân bổ (Thấp < 20tr/tháng, Vừa 20-100tr/tháng, Cao > 100tr/tháng).

### 3.3. Quy định Handoff & Vòng lặp Khép kín (Closed-Loop Data Flow)
- Dữ liệu đầu ra của Nhóm Insight (A) là đầu vào bắt buộc cho Nhóm Content (B), SEO/Ads (C) và CRM (D).
- Dữ liệu đầu ra của Nhóm Ads/SEO (C) và CRM (D) đổ về Nhóm Analytics (E).
- Kết quả chẩn đoán của Nhóm Analytics & CRO (E) phản hồi ngược về Nhóm Content (B), Ads (C) hoặc CRM (D) để tối ưu chu kỳ tiếp theo.

---

## 4. Chính sách Kiểm định & Ngưỡng Kỹ thuật (Validation Policy)

| Tham số / Chỉ số | Ngưỡng giá trị mặc định | Quy tắc kiểm định |
|---|---|---|
| `persona_count_range` | 2 – 4 persona | Tối thiểu 2 persona, tối đa 4 persona mỗi dự án để tránh phân mảnh |
| `competitor_analysis_count` | 3 – 5 đối thủ | Cần ít nhất 3 đối thủ trực tiếp/gián tiếp để lập ma trận gap |
| `short_copy_variants` | 3 – 5 biến thể / góc | Bắt buộc có các góc tiếp cận khác nhau (AIDA, PAS, BAB, FAB) |
| `longform_seo_word_count` | 1.500 – 3.500 từ | Bài pillar tối thiểu 2.000 từ, bài cluster tối thiểu 1.200 từ |
| `brand_voice_pass_score` | 80 / 100 điểm | Dưới 80 điểm bắt buộc chỉnh sửa trước khi publish |
| `ads_diagnosis_cpa_spike` | >= +20% so với benchmark 14 ngày | Kích hoạt cảnh báo bất thường CPA |
| `ads_diagnosis_ctr_drop` | >= -30% so với benchmark 14 ngày | Kích hoạt cảnh báo fatigue creative hoặc targeting lệch |
| `crm_rfm_segments_min` | 4 phân khúc | VIP, Khách trung thành, Khách tiềm năng, Nguy cơ rời bỏ |
| `email_sequence_length` | 3 – 7 email | Welcome (3-5 email), Nurture (4-7 email), Cart Abandon (3 email) |
| `cro_ab_test_confidence` | >= 95% (p < 0.05) | Ngưỡng tin cậy thống kê tối thiểu trước khi công nhận biến thể thắng |
| `cro_minimum_sample_size` | >= 300 conversions / variant | Ngăn chặn kết luận vội vàng khi mẫu chưa đủ lớn |

---

## 5. Chính sách Cổng Phê duyệt & Quy trình (Workflow Policy & Approval Gates)

1. **Insight Gate (Cổng Phê duyệt Chân dung & Insight)**:
   - File `insight/icp.md` và `insight/customer-journey.md` phải được người dùng phê duyệt trước khi lên kế hoạch lịch biên tập (`content/editorial-calendar.md`) hoặc cấu trúc chiến dịch quảng cáo (`seo-ads/campaign-structure.md`).
2. **Strategy Gate (Cổng Phê duyệt Chiến lược & Lịch trình)**:
   - Phê duyệt `content/editorial-calendar.md`, `seo-ads/keyword-clusters.md`, và `seo-ads/campaign-structure.md` trước khi tiến hành sản xuất hàng loạt nội dung hoặc setup ads.
3. **Pre-Launch QA Gate (Cổng Kiểm soát Trước Khi Chạy)**:
   - Bài viết SEO phải đạt checklist On-page; Ad copy phải có biến thể A/B; Creative brief phải có hook/CTA rõ ràng; Chuỗi email phải có UTM tracking và link test trước khi đưa vào hệ thống CRM/Ads.
4. **Optimization Gate (Cổng Quyết định Tối ưu & Thử nghiệm)**:
   - Các hành động tắt ad set, đổi cấu trúc budget hoặc áp dụng biến thể landing page mới từ A/B test phải có dữ liệu đo lường đạt ngưỡng tin cậy thống kê quy định tại Validation Policy.
