---
name: ads-generate-creative-brief
description: "Tạo bản yêu cầu sáng tạo (Creative Brief) chuẩn hóa cho đội ngũ Designer, Video Editor, KOC từ mục tiêu quảng cáo, insight khách hàng và USP sản phẩm (Visual Hook, Audio Hook, Tỷ lệ khung hình, Bố cục, CTA, Moodboard tham khảo). Kích hoạt khi có yêu cầu 'brief creative', 'brief thiết kế quảng cáo', 'làm brief cho designer/video editor'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/seo-ads/creative-briefs/<brief-id>.md."
---

# ads-generate-creative-brief: Tạo Creative Brief Cho Designer & Video Editor

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "brief creative", "tạo brief thiết kế cho designer", "làm brief video quảng cáo cho editor", "viết mô tả concept hình ảnh/video ads", hoặc sau khi đã có cấu trúc chiến dịch từ `ads-structure-campaign`.

## Workflow

### Giai đoạn 1: Tiếp nhận Chiến lược Quảng cáo & Insight Khách hàng
**Mục tiêu**: Thu thập angle quảng cáo, thông điệp cần truyền tải và nền tảng đích.
- Đọc thông tin persona và pain point từ `insight/icp.md`.
- Trích xuất vị trí hiển thị (Placements) từ `seo-ads/campaign-structure.md`: Feed (1:1 hoặc 4:5), Reels/Stories/TikTok (9:16), Display Banner (16:9 hoặc các kích thước chuẩn IAB).
- Xác định định dạng creative cần sản xuất: Ảnh đơn (Static Image), Bộ ảnh xoay vòng (Carousel), Video ngắn UGC (User-Generated Content), hoặc Motion Graphic.

### Giai đoạn 2: Thiết kế Chi tiết Bản Brief Sáng tạo
**Mục tiêu**: Cung cấp đầy đủ hướng dẫn thị giác, văn bản hiển thị và tiêu chuẩn kỹ thuật để đội ngũ sản xuất thực thi không bị lệch hướng.
- **Phần Hook (3 giây đầu hoặc ấn tượng đầu tiên)**:
  - Video: Mô tả hành động giật gân, âm thanh kích thích, câu thoại mở đầu và chữ chạy to trên màn hình.
  - Ảnh: Bố cục điểm nhấn thị giác (Visual focal point), màu sắc tương phản cao, typography nổi bật.
- **Phần Thân (Core Body / Narrative)**:
  - Trình bày trực quan tính năng hoặc sự biến chuyển Before / After (tránh vi phạm chính sách hiển thị vết thương/da thịt nhạy cảm).
  - Đưa ra chứng thực uy tín (Social Proof: tem chứng nhận, số lượng người tin dùng, trích dẫn báo chí).
- **Phần Kêu gọi Hành động (CTA & Offer Placement)**:
  - Nút bấm đồ họa rõ ràng, thời hạn ưu đãi hoặc quà tặng đi kèm.
- **Quy cách kỹ thuật (Technical Specs)**:
  - Kích thước (Pixel), tỷ lệ (Aspect Ratio), thời lượng tối đa (nếu là video: 15s - 30s), vùng an toàn (Safe Zone) không bị icon và nút bấm của TikTok/Reels che khuất.

### Giai đoạn 3: Đóng gói Moodboard Tham khảo & Xuất Deliverable
**Mục tiêu**: Cung cấp phong cách tham chiếu và ghi file theo Naming Policy trong `config.md`.
- Gợi ý link hoặc mô tả phong cách tham chiếu (Visual Style / Mood & Tone: Tối giản công nghệ, Tươi sáng năng động, Sang trọng cao cấp).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/seo-ads/creative-briefs/<brief-id>.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/seo-ads/creative-briefs/<brief-id>.md`:

```markdown
# Bản Yêu Cầu Sáng Tạo Quảng Cáo (Creative Brief) — <client_name>
- Client Slug: `<client-slug>`
- Mã Brief: `<brief-id>` (ví dụ: `CR_FB_01_UGC_Video`)
- Chiến dịch / Ad Set liên quan: <Tên Ad Set từ campaign-structure.md>
- Nền tảng: <TikTok / Meta Feed & Reels / Google Display>
- Người nhận bàn giao: <Designer / Video Editor / Creator>
- Ngày tạo: <YYYY-MM-DD>

## 1. Mục Tiêu & Thông Điệp Cốt Lõi
- **Mục tiêu chuyển đổi**: Kích thích người dùng click vào Landing Page để đăng ký dùng thử.
- **Thông điệp duy nhất (Single-Minded Proposition)**: "Sản phẩm giúp giải quyết vấn đề X chỉ sau 7 ngày mà không gây tác dụng phụ Y."
- **Insight khách hàng khai thác**: Người tiêu dùng đã thử nhiều cách nhưng đều thất vọng vì tốn thời gian.

## 2. Quy Cách Kỹ Thuật (Production Specs)
- **Định dạng**: Video ngắn UGC / Ảnh đơn thiết kế đồ họa / Carousel
- **Tỷ lệ khung hình**: `9:16` (1080x1920) cho Reels/TikTok và `1:1` (1080x1080) cho Feed
- **Thời lượng video (nếu có)**: Tối ưu 25 - 35 giây (tối đa 45s)
- **Lưu ý Safe Zone**: Để trống 150px trên đỉnh và 250px dưới đáy để tránh icon ứng dụng che mất chữ.

## 3. Kịch Bản Khung Hình Chi Tiết (Storyboard / Visual Breakdown)

### Nếu là Video UGC / Motion Graphic:
| Thời gian | Hình ảnh & Hành động diễn viên | Chữ hiển thị trên màn hình (Text Overlay) | Lời thoại (Voice-over) / Âm thanh |
|---|---|---|---|
| `00 - 03s` (Hook) | Cận cảnh gương mặt ngỡ ngàng, cầm sản phẩm trên tay | "DỪNG LẠI! Nếu bạn vẫn đang..." | Âm thanh woosh mạnh, giọng nói hào hứng |
| `03 - 12s` (Problem) | Cảnh sinh hoạt thường ngày gặp khó khăn | "Tại sao 9/10 người đều mắc lỗi này?" | Nhạc nền dồn dập, đồng cảm |
| `12 - 25s` (Solution) | Thao tác mở hộp và sử dụng sản phẩm mượt mà | "Công nghệ mới giúp X nhanh gấp 3 lần" | Giọng giải thích tự tin, tiếng ASMR |
| `25 - 30s` (CTA) | Cầm điện thoại thao tác bấm mua kèm tem ưu đãi | "Nhận ưu đãi 30% ngay hôm nay" | Nhạc kết vui tươi, tiếng click chuột |

### Nếu là Ảnh đơn / Carousel:
- **Tiêu đề chính trên ảnh (Main Headline)**: Lớn, dễ đọc trên di động.
- **Hình ảnh chủ đạo**: Sản phẩm đặt ở góc 2/3, ánh sáng tự nhiên.
- **Badges / Trust Signals**: Icon chứng nhận, đánh giá 4.9/5 sao.
- **Màu sắc chủ đạo (Brand Palette)**: Theo quy chuẩn nhận diện thương hiệu.

## 4. Tham Chiếu Phong Cách (Moodboard & Reference Links)
- Tone cảm xúc: Đáng tin cậy, hiện đại, tràn đầy năng lượng tích cực.
```

## Don'ts
- Không viết brief mơ hồ không có chỉ dẫn hình ảnh (tránh mô tả kiểu "làm cái gì đó trông thật viral và chuyên nghiệp").
- Không nhồi nhét quá nhiều thông điệp hoặc quá nhiều chữ vào một khung hình quảng cáo.
- Không bỏ qua thông số tỷ lệ và Safe Zone khiến nút bấm của nền tảng che mất thông tin quan trọng.
- Không yêu cầu các hiệu ứng hình ảnh phức tạp vượt quá ngân sách hoặc thời hạn sản xuất của chiến dịch.

## Quality Checklist
- [ ] Xác định rõ tỷ lệ khung hình, định dạng tệp và quy cách Safe Zone kỹ thuật.
- [ ] Bảng kịch bản/visual breakdown phân chia rõ ràng giữa hình ảnh, text overlay và âm thanh.
- [ ] Có thông điệp cốt lõi duy nhất (Single-Minded Proposition) và CTA trực diện.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/seo-ads/creative-briefs/<brief-id>.md`.
