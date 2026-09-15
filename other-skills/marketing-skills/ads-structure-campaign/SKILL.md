---
name: ads-structure-campaign
description: "Thiết kế kiến trúc chiến dịch quảng cáo đa tầng phân cấp (Account -> Campaign -> Ad Set / Ad Group -> Ads) cho Meta Ads và Google Ads. Phân bổ ngân sách, thiết lập mục tiêu chiến dịch và ma trận targeting đa tầng phễu (Cold, Warm, Hot). Kích hoạt khi có yêu cầu 'lên cấu trúc chiến dịch quảng cáo', 'setup ads', 'cấu trúc campaign Meta/Google'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/seo-ads/campaign-structure.md."
---

# ads-structure-campaign: Thiết Kế Cấu Trúc Chiến Dịch Quảng Cáo Đa Tầng

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "lên cấu trúc chiến dịch quảng cáo", "thiết kế campaign Meta Ads/Google Ads", "phân bổ ngân sách chạy ads", "lập kế hoạch setup tài khoản quảng cáo", hoặc sau khi đã hoàn tất bước nghiên cứu ICP và định vị sản phẩm.

## Workflow

### Giai đoạn 1: Tiếp nhận Mục tiêu, Ngân sách & Nền tảng Chạy Ads
**Mục tiêu**: Xác định các thông số ngân sách từ `client_context` và mục tiêu kinh doanh.
- Đọc thông tin ngân sách (`budget_tier`) từ `config.md` hoặc số liệu thực tế người dùng cung cấp (ví dụ: 50.000.000 VNĐ/tháng).
- Xác định mục tiêu chuyển đổi cốt lõi: Tạo khách hàng tiềm năng (Lead Gen), Doanh số thương mại điện tử (Purchase/ROAS), hay Lưu lượng truy cập (Traffic/Brand Awareness).
- Chọn nền tảng triển khai: Meta Ads (Facebook/Instagram), Google Ads (Search, Performance Max, Display), hoặc TikTok Ads.

### Giai đoạn 2: Thiết kế Phân tầng Chiến dịch theo Ma trận Phễu Khách hàng
**Mục tiêu**: Phân bổ cấu trúc tài khoản theo 3 tầng đối tượng: Cold (Lạnh), Warm (Ấm) và Hot (Nóng).
- **Quy tắc phân bổ ngân sách khuyến nghị**:
  - Tầng Cold (Tiếp cận đối tượng mới): 60% – 70% tổng ngân sách.
  - Tầng Warm (Tương tác & Nurturing): 15% – 20% tổng ngân sách.
  - Tầng Hot (Retargeting bám đuổi chốt đơn): 10% – 15% tổng ngân sách.
- **Cấu trúc chi tiết Meta Ads**:
  - Cấp Campaign: Đặt tên chuẩn hóa, chọn mục tiêu tối ưu (Objective: Sales / Leads / Engagement), bật CBO (Advantage Campaign Budget) hoặc ABO (Ad Set Budget).
  - Cấp Ad Set: Phân định đối tượng (Broad / Interest & Demographics / Lookalike / Custom Audience retargeting), vị trí hiển thị (Placements), tối ưu hóa lượt phân phối.
  - Cấp Ads: Ghép nối 2-3 creative formats (Video, Carousel, Single Image) kết hợp biến thể copy từ `content-write-short-copy`.
- **Cấu trúc chi tiết Google Ads (nếu áp dụng)**:
  - Chia tách Campaign: Brand Search (Bảo vệ thương hiệu), Non-brand High Intent Search (Từ khóa tìm kiếm có ý định mua), và Performance Max (PMax đa kênh).
  - Cấp Ad Group: Gom nhóm theo chủ đề từ khóa chặt chẽ (STAG - Single Theme Ad Groups).

### Giai đoạn 3: Chuẩn hóa Quy ước Đặt tên (Naming Taxonomy) & Xuất Deliverable
**Mục tiêu**: Xây dựng quy ước đặt tên chuyên nghiệp để dễ dàng theo dõi hiệu quả trên báo cáo, lưu file theo Naming Policy trong `config.md`.
- Quy chuẩn định danh: `[Platform]_[Funnel]_[Objective]_[Audience]_[Date]` (ví dụ: `FB_Cold_Conversions_Broad_2026Q1`).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/seo-ads/campaign-structure.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/seo-ads/campaign-structure.md`:

```markdown
# Cấu Trúc Chiến Dịch Quảng Cáo (Campaign Structure) — <client_name>
- Client Slug: `<client-slug>`
- Nền tảng chính: <Meta Ads / Google Ads / TikTok Ads>
- Tổng ngân sách phân bổ: <Số tiền> VNĐ / tháng
- Ngày lập: <YYYY-MM-DD>

## 1. Sơ Đồ Phân Bổ Ngân Sách Đa Tầng (Budget Allocation)
- **Tầng Cold (Khách hàng mới)**: 70% (~... VNĐ) -> Mở rộng tệp & tạo nhu cầu.
- **Tầng Warm (Gắn kết & Cân nhắc)**: 20% (~... VNĐ) -> Tương tác video, xem sản phẩm.
- **Tầng Hot (Retargeting chốt đơn)**: 10% (~... VNĐ) -> Bỏ giỏ hàng, điền form dang dở.

## 2. Kiến Trúc Chi Tiết Meta Ads (Campaign Hierarchy)

### Chiến Dịch 1 (Cold Traffic): `FB_Cold_Sales_BroadLookalike`
- **Mục tiêu (Objective)**: Lượt mua hàng (Purchase Conversions)
- **Cơ chế ngân sách**: CBO / ABO - Ngân sách: ... VNĐ / ngày
- **Cấu trúc Ad Sets**:
  - `AdSet 01 - Broad Targeting`: Độ tuổi 22-45, Vị trí Việt Nam, Không chọn sở thích (để AI tự học).
  - `AdSet 02 - Core Interests`: Nhắm vào sở thích theo ICP từ `insight/icp.md`.
  - `AdSet 03 - Lookalike 1-2%`: Tệp tương tự từ danh sách khách mua hàng cũ.
- **Phân bổ Ad Creatives**: Mỗi Ad Set gắn 3 creatives (1 Video ngắn demo + 1 Ảnh đơn infographic + 1 Carousel tính năng).

### Chiến Dịch 2 (Retargeting): `FB_Hot_Sales_CartAbandoners`
- **Mục tiêu (Objective)**: Lượt mua hàng
- **Cấu trúc Ad Sets**:
  - `AdSet 01 - Custom Audience`: Người đã thêm vào giỏ hàng trong 14 ngày qua (loại trừ người đã mua).
- **Ad Creatives**: Đánh mạnh vào bảo hành, voucher giảm giá đặc biệt và giải quyết nỗi sợ rủi ro.

## 3. Quy Ước Đặt Tên (Naming Taxonomy) & UTM Tracking
- **URL Parameter Template**:
  `utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`
- Handoff sang: `ads-generate-creative-brief` để tạo yêu cầu thiết kế hình ảnh/video cho từng Ad Set.
```

## Don'ts
- Không gom lẫn lộn khách hàng mới toanh (Cold) và khách hàng đã vào giỏ hàng (Hot) vào chung một nhóm quảng cáo.
- Không chia quá nhiều nhóm quảng cáo vi mô khi ngân sách nhỏ (ngân sách dưới 500k/ngày chia quá 3 nhóm sẽ khiến nhóm bị kẹt trong giai đoạn máy học - Learning Phase).
- Không đặt tên chiến dịch lộn xộn, vô nghĩa khiến việc tổng hợp báo cáo ở nhóm Analytics bị phân mảnh.
- Không bỏ qua thông số theo dõi UTM tracking khi thiết lập chiến dịch.

## Quality Checklist
- [ ] Phân bổ tỷ lệ ngân sách rõ ràng giữa các tầng Cold / Warm / Hot.
- [ ] Cấu trúc thể hiện đầy đủ 3 cấp: Campaign -> Ad Set / Ad Group -> Ads.
- [ ] Có quy tắc nhắm mục tiêu (Targeting criteria) gắn chặt với dữ liệu từ `insight/icp.md`.
- [ ] Có quy ước đặt tên chuẩn hóa (Naming Taxonomy) và chuỗi UTM tracking.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/seo-ads/campaign-structure.md`.
