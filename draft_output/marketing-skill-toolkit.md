# Bộ Skill Toolkit cho Nhân sự Marketing — Kiến trúc Agent Skill Đa ngành (Agency Model)

*(Thiết kế bởi vai trò AI Agent & Marketing Strategy Architect — tối ưu cho agency phục vụ nhiều client, nhiều vertical)*

---

## 1. Nguyên tắc thiết kế

Vì vận hành theo mô hình **agency đa ngành**, bộ skill phải:

- **Tách biệt "logic nghiệp vụ" khỏi "dữ liệu client"** — mỗi skill nhận `client_context` (ngành, ICP, brand voice, competitors) làm input động, không hard-code cho 1 ngành.
- **Chuẩn hóa naming theo format**: `[domain]-[action]-[object]` (snake_case, tiếng Anh) để dễ orchestrate và tránh trùng lặp chức năng.
- **Loại bỏ skill "chung chung"**: không có skill kiểu "viết content" mơ hồ — mỗi skill phải gắn với 1 deliverable cụ thể, đo lường được.
- **Phân cấp theo tần suất sử dụng thực tế trong agency**, không theo độ "hào nhoáng" công nghệ.

---

## 2. Bảng tổng hợp toàn bộ Skill Toolkit

### 🔵 Nhóm A — Market & Customer Insight

| Skill (chuẩn hóa tên) | Vai trò cốt lõi | Trigger | Input | Output | Use case ví dụ |
|---|---|---|---|---|---|
| `insight-build-icp` | Xây dựng chân dung khách hàng mục tiêu đa chiều (demographic, psychographic, JTBD) | User cung cấp brief khách hàng mới / yêu cầu "xây ICP" | Brand brief, dữ liệu bán hàng cũ, phỏng vấn sale, review sản phẩm | Tài liệu ICP + persona cards (2-4 persona) | Onboard client mới ngành F&B, cần ICP trước khi lên content calendar |
| `insight-analyze-competitor` | Phân tích đối thủ: positioning, pricing, content gap, channel mix | "phân tích đối thủ", "competitor audit" | Tên/URL đối thủ, ngành hàng | Ma trận so sánh + gap analysis + khuyến nghị khác biệt hóa | Client mỹ phẩm cần biết đối thủ đang chiếm ngách nào trên TikTok |
| `insight-scan-market-trend` | Quét xu hướng thị trường/ngành theo thời gian thực (social listening, search trend) | "xu hướng", "trend ngành X", đầu chiến dịch mới | Ngành hàng, khung thời gian, thị trường (VN/global) | Báo cáo trend + top chủ đề đang nổi + độ "nóng" | Lên ý tưởng campaign Tết cho 5 client cùng lúc |
| `insight-map-customer-journey` | Vẽ hành trình khách hàng theo từng funnel stage, xác định điểm chạm & pain point | "customer journey", trước khi thiết kế funnel | Persona (từ `insight-build-icp`), kênh hiện có của client | Sơ đồ journey map + pain point theo từng giai đoạn | Client B2B cần hiểu vì sao lead rớt ở giai đoạn demo |

### 🟢 Nhóm B — Content Marketing & Copywriting

| Skill | Vai trò cốt lõi | Trigger | Input | Output | Use case |
|---|---|---|---|---|---|
| `content-plan-editorial-calendar` | Lập kế hoạch nội dung theo chủ đề, kênh, tần suất, gắn với funnel stage | "content calendar", "kế hoạch nội dung tháng" | Persona, journey map, mục tiêu KPI, kênh (FB/IG/TikTok/Blog) | Bảng lịch content (chủ đề, format, CTA, ngày đăng) | Lập content calendar Q4 cho 3 client song song |
| `content-write-longform-seo` | Viết bài blog/article chuẩn SEO, có cấu trúc heading, semantic keyword | "viết bài blog", "content SEO" kèm keyword | Target keyword, search intent, outline (nếu có), brand voice | Bài viết hoàn chỉnh + meta title/description | Viết 10 bài pillar content cho website SaaS client |
| `content-write-short-copy` | Viết copy ngắn: caption, ad copy, headline, CTA theo AIDA/PAS | "viết caption", "viết ad copy" | Sản phẩm/offer, platform (FB Ads/Google Ads/IG), tone giọng | 3-5 biến thể copy A/B test | Viết 5 bộ ad copy test cho campaign chạy Facebook Ads |
| `content-adapt-multichannel` | Biến đổi 1 nội dung gốc thành nhiều format cho nhiều kênh (repurpose) | "chuyển bài này sang TikTok script", "repurpose content" | Nội dung gốc, kênh đích | Nội dung đã format lại theo đặc thù kênh đích | 1 bài blog → script Reels + carousel LinkedIn + email newsletter |
| `content-audit-brand-voice` | Kiểm tra tính nhất quán giọng điệu thương hiệu trên nội dung đã/sắp xuất bản | "audit brand voice", trước khi publish batch content | Brand voice guideline, nội dung cần kiểm | Báo cáo lệch chuẩn + bản chỉnh sửa | Đảm bảo 20 bài content của 1 client không bị lệch tone giữa các writer |

### 🟠 Nhóm C — SEO & Performance Ads

| Skill | Vai trò cốt lõi | Trigger | Input | Output | Use case |
|---|---|---|---|---|---|
| `seo-research-keyword-cluster` | Nghiên cứu & phân cụm từ khóa theo search intent, xây dựng topic cluster | "nghiên cứu từ khóa", "keyword research" | Ngành hàng, seed keyword, đối thủ | Bộ từ khóa phân cụm + volume/intent + đề xuất pillar-cluster | Xây content silo cho website mới của client |
| `seo-audit-technical-onpage` | Audit kỹ thuật SEO on-page (meta, heading, internal link, tốc độ, schema) | "audit SEO", "website bị tụt hạng" | URL website, Search Console data (nếu có) | Checklist lỗi + mức độ ưu tiên fix | Website client tụt traffic đột ngột, cần chẩn đoán nhanh |
| `ads-structure-campaign` | Thiết kế cấu trúc campaign (Google/Meta Ads): account → campaign → ad group/ad set → targeting | "lên cấu trúc chiến dịch quảng cáo" | Budget, mục tiêu (traffic/conversion/lead), platform | Sơ đồ cấu trúc campaign + targeting đề xuất | Setup campaign mới cho client thương mại điện tử, budget 50tr/tháng |
| `ads-generate-creative-brief` | Tạo creative brief cho designer/video editor từ mục tiêu ads | "brief creative", "brief cho designer" | Insight khách hàng, USP sản phẩm, platform | Brief chuẩn (hook, message, format, reference) | Brief 10 concept ảnh/video cho performance campaign |
| `ads-diagnose-underperformance` | Chẩn đoán nguyên nhân campaign kém hiệu quả (CTR thấp, CPA cao...) | "campaign chạy kém", có số liệu ads | Số liệu campaign (CTR, CPC, CPA, ROAS), creative đang dùng | Root cause + đề xuất khắc phục ưu tiên | CPA tăng gấp đôi tuần này, cần biết fix targeting hay creative trước |

### 🟣 Nhóm D — CRM & Lifecycle/Email Marketing

| Skill | Vai trò cốt lõi | Trigger | Input | Output | Use case |
|---|---|---|---|---|---|
| `crm-segment-customer-list` | Phân khúc danh sách khách hàng theo hành vi, giá trị, giai đoạn lifecycle (RFM...) | "phân khúc khách hàng", "segment list" | Dữ liệu khách hàng (mua hàng, tương tác) | Các segment + tiêu chí + đề xuất hành động theo segment | Chia 10.000 khách hàng thành nhóm VIP/at-risk/new để chạy email riêng |
| `lifecycle-design-automation-flow` | Thiết kế luồng automation (welcome, cart abandon, win-back, re-engagement) | "thiết kế email flow", "automation lifecycle" | Segment, điểm chạm hiện có, mục tiêu flow | Sơ đồ flow (trigger → điều kiện → nội dung → thời gian chờ) | Xây flow bỏ giỏ hàng 3 bước cho client e-commerce |
| `email-write-sequence-copy` | Viết nội dung chuỗi email theo từng bước trong flow đã thiết kế | "viết nội dung email flow", có flow sẵn | Flow structure (từ `lifecycle-design-automation-flow`), offer | Nội dung từng email trong chuỗi (subject, body, CTA) | Viết 5 email cho chuỗi nurture lead B2B |
| `crm-audit-lifecycle-health` | Đánh giá sức khỏe tổng thể vòng đời khách hàng (open rate, churn, LTV trend) | "đánh giá hiệu quả CRM", "email performance kém" | Báo cáo email/CRM hiện có | Chẩn đoán điểm nghẽn + benchmark ngành | Open rate giảm 30% 3 tháng liên tiếp, cần biết vì đâu |

### 🔴 Nhóm E — Marketing Analytics & CRO

| Skill | Vai trò cốt lõi | Trigger | Input | Output | Use case |
|---|---|---|---|---|---|
| `analytics-build-campaign-report` | Tổng hợp báo cáo hiệu quả chiến dịch đa kênh, chuẩn hóa theo KPI client | "báo cáo campaign", "report tháng" | Số liệu thô từ các kênh (Ads Manager, GA4, CRM) | Báo cáo trực quan (dashboard/slide) + insight + khuyến nghị | Báo cáo tổng kết campaign cuối tháng gửi 5 client |
| `analytics-attribute-conversion-path` | Phân tích attribution — kênh nào thực sự đóng góp vào chuyển đổi | "phân bổ ngân sách kênh nào hiệu quả" | Dữ liệu multi-touch (GA4, ads platforms) | Mô hình attribution + đề xuất phân bổ lại ngân sách | Client hỏi nên tăng budget Google Ads hay TikTok Ads |
| `cro-audit-landing-page` | Audit landing page/website theo checklist CRO (UX, tốc độ, form friction, trust signal) | "audit landing page", "conversion rate thấp" | URL landing page, dữ liệu heatmap/GA nếu có | Danh sách vấn đề + đề xuất theo mức độ tác động | LP có traffic tốt nhưng conversion rate chỉ 0.5% |
| `cro-design-ab-test` | Thiết kế thử nghiệm A/B test (hypothesis, biến thử, sample size, thời gian chạy) | "thiết kế A/B test", "test landing page" | Vấn đề CRO đã xác định, traffic hiện có | Test plan (hypothesis, variant, metric thành công, thời lượng) | Test 2 phiên bản headline trên LP trước khi scale ads |

---

## 3. Phân cấp mức độ ưu tiên triển khai

| Mức độ | Tiêu chí lựa chọn | Skills |
|---|---|---|
| 🥇 **Cốt lõi (Must-have)** | Dùng hàng ngày/tuần, là xương sống của mọi campaign, ROI triển khai cao nhất | `insight-build-icp`, `content-plan-editorial-calendar`, `content-write-short-copy`, `seo-research-keyword-cluster`, `ads-structure-campaign`, `ads-diagnose-underperformance`, `analytics-build-campaign-report`, `crm-segment-customer-list` |
| 🥈 **Mở rộng (Should-have)** | Nâng chất lượng & chiều sâu, dùng theo giai đoạn/dự án cụ thể | `insight-analyze-competitor`, `insight-map-customer-journey`, `content-write-longform-seo`, `content-adapt-multichannel`, `seo-audit-technical-onpage`, `ads-generate-creative-brief`, `lifecycle-design-automation-flow`, `email-write-sequence-copy`, `cro-audit-landing-page` |
| 🥉 **Nâng cao (Nice-to-have)** | Giá trị cao nhưng cần dữ liệu trưởng thành/công cụ tích hợp phức tạp hơn | `insight-scan-market-trend`, `content-audit-brand-voice`, `crm-audit-lifecycle-health`, `analytics-attribute-conversion-path`, `cro-design-ab-test` |

**Lý do phân cấp**: Nhóm Must-have là các skill mà thiếu chúng thì *không thể chạy một campaign cơ bản*. Nhóm Should-have giải quyết các điểm nghẽn phổ biến (đa kênh, kỹ thuật SEO, lifecycle). Nhóm Nice-to-have đòi hỏi dữ liệu lịch sử đủ lớn (attribution, A/B test) hoặc mang tính chiến lược dài hạn (trend scanning) — phù hợp khi agency đã vận hành ổn định.

---

## 4. Kịch bản Orchestration Workflow — Vận hành 1 Campaign End-to-End

**Bối cảnh**: Agency nhận client mới — thương hiệu D2C bán thực phẩm chức năng, mục tiêu launch sản phẩm mới trong 6 tuần.

```
Tuần 1 — INSIGHT & FOUNDATION
├─ insight-build-icp            → Xác định 2 persona chính (người tập gym, người trung niên chăm sóc sức khỏe)
├─ insight-analyze-competitor   → So sánh 3 đối thủ trực tiếp, tìm content gap
└─ insight-map-customer-journey → Xác định pain point ở giai đoạn "cân nhắc" (thiếu trust signal)

Tuần 2 — STRATEGY & PLANNING
├─ seo-research-keyword-cluster       → Xây cluster từ khóa "tăng cơ", "hỗ trợ tiêu hóa"...
├─ content-plan-editorial-calendar    → Lịch content 6 tuần theo funnel (TOFU blog → MOFU review → BOFU ads)
└─ ads-structure-campaign             → Cấu trúc campaign Meta Ads + Google Search theo giai đoạn

Tuần 3-4 — PRODUCTION
├─ content-write-longform-seo   → 4 bài blog pillar theo cluster từ khóa
├─ content-write-short-copy     → 5 bộ ad copy A/B test cho từng persona
├─ content-adapt-multichannel   → Repurpose blog → TikTok script + email
├─ ads-generate-creative-brief  → Brief cho team design 8 concept ảnh/video
└─ email-write-sequence-copy    ← (dùng output từ lifecycle-design-automation-flow)
   └─ lifecycle-design-automation-flow → Flow welcome series cho người đăng ký sớm

Tuần 5 — LAUNCH
├─ crm-segment-customer-list    → Phân khúc waitlist theo mức độ quan tâm
└─ (Campaign go-live: Ads + Content + Email đồng loạt)

Tuần 6 — MEASURE & OPTIMIZE
├─ ads-diagnose-underperformance  → Phát hiện CPA cao ở 1 ad set → điều chỉnh targeting
├─ cro-audit-landing-page         → LP conversion thấp → phát hiện form quá dài
├─ analytics-build-campaign-report → Tổng hợp báo cáo launch gửi client
└─ (Nếu có traffic đủ) cro-design-ab-test → Test rút gọn form trên LP
```

**Nguyên tắc phối hợp then chốt**: Output của skill nhóm Insight (A) luôn là input bắt buộc cho nhóm Content (B) và CRM (D); output của nhóm Ads/SEO (C) và CRM (D) đổ về nhóm Analytics (E) để đóng vòng lặp tối ưu — tạo thành **closed-loop system** thay vì các skill hoạt động rời rạc.

---

**Ghi chú triển khai**: Đây là bản đề xuất kiến trúc (chưa viết nội dung SKILL.md). Khi build thực tế, khuyến nghị bắt đầu với 8 skill Must-have trước, test luồng orchestration trên 1 client thật, rồi mới mở rộng dần — tránh over-engineering ngay từ đầu.
