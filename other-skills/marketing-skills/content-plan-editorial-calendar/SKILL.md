---
name: content-plan-editorial-calendar
description: "Lập kế hoạch biên tập nội dung (Editorial Calendar) đa kênh gắn với tầng phễu (TOFU/MOFU/BOFU), chủ đề trụ cột, định dạng bài và KPI chuyển đổi. Kích hoạt khi có yêu cầu 'content calendar', 'lên lịch nội dung', 'kế hoạch bài đăng tháng/quý'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/content/editorial-calendar.md."
---

# content-plan-editorial-calendar: Lập Kế Hoạch Lịch Biên Tập Nội Dung Đa Kênh

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "lập lịch nội dung", "content calendar", "lên kế hoạch biên tập tháng", "phân bổ lịch đăng đa kênh", hoặc sau khi đã hoàn thành các bước khảo sát ICP và hành trình khách hàng.

## Workflow

### Giai đoạn 1: Tiếp nhận Đầu vào & Xác định Trụ cột Nội dung (Content Pillars)
**Mục tiêu**: Đồng bộ dữ liệu từ `insight/icp.md` và `insight/customer-journey.md` để thiết lập chủ đề.
- Đọc thông tin persona mục tiêu và các pain points tương ứng.
- Xác định 3-5 trụ cột nội dung cốt lõi (Content Pillars) phản ánh năng lực cạnh tranh của client:
  - Pillar Giáo dục / Nhận thức vấn đề (Educational).
  - Pillar Bằng chứng xã hội / Case study / Thẩm định (Authority & Social Proof).
  - Pillar Trải nghiệm sản phẩm / Xử lý từ chối (Product & Friction Removal).
  - Pillar Văn hóa thương hiệu & Lối sống cộng đồng (Brand Culture & Lifestyle).
- Thu thập danh sách kênh phân phối mục tiêu (Facebook, TikTok, LinkedIn, Blog, Instagram).

### Giai đoạn 2: Thiết kế Lịch Phân bổ theo Tầng Phễu & Tần suất Xuất bản
**Mục tiêu**: Cân bằng tỷ lệ nội dung giữa nhận thức (TOFU), cân nhắc (MOFU) và bán hàng trực tiếp (BOFU).
- Thiết lập tỷ lệ xuất bản chuẩn mực (khuyến nghị 60% TOFU, 30% MOFU, 10% BOFU để duy trì tương tác tự nhiên).
- Lên lịch theo ma trận 4 tuần (hoặc khung thời gian chiến dịch quy định tại `config.md`):
  - Ngày đăng dự kiến (Date).
  - Kênh phân phối (Channel).
  - Tầng phễu (Funnel Stage: TOFU / MOFU / BOFU).
  - Trụ cột nội dung (Content Pillar).
  - Tiêu đề / Góc khai thác đề xuất (Working Title / Angle).
  - Định dạng (Format: Video ngắn, Ảnh đơn, Carousel, Bài dài, Infographic).
  - Kêu gọi hành động (Call-to-Action - CTA) và chỉ số đo lường (KPI).

### Giai đoạn 3: Rà soát Tính Thực thi & Trình duyệt Strategy Gate
**Mục tiêu**: Kiểm tra khối lượng công việc, tính khả thi sản xuất và lưu file theo Naming Policy trong `config.md`.
- Rà soát lịch đăng để đảm bảo không bị trùng lặp chủ đề trong tuần hoặc dồn quá nhiều bài bán hàng BOFU liên tiếp.
- Xuất dữ liệu ra file `docs/marketing-projects/<client-slug>/content/editorial-calendar.md`.
- Trình bày Strategy Gate cho người dùng xác nhận trước khi phân phối cho các writer/creator.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/content/editorial-calendar.md`:

```markdown
# Lịch Biên Tập Nội Dung (Editorial Calendar) — <client_name>
- Client Slug: `<client-slug>`
- Khung thời gian: <Tháng / Quý / Tuần>
- Ngày ban hành: <YYYY-MM-DD>

## 1. Hệ Thống Trụ Cột Nội Dung (Content Pillars)
- **Pillar 1: <Tên Pillar>**: <Mục đích và thông điệp truyền tải>
- **Pillar 2: <Tên Pillar>**: <Mục đích và thông điệp truyền tải>
- **Pillar 3: <Tên Pillar>**: <Mục đích và thông điệp truyền tải>

## 2. Bảng Kế Hoạch Đăng Bài Chi Tiết
| Ngày | Kênh | Funnel | Pillar | Tiêu đề / Angle dự kiến | Format | Mục tiêu CTA | KPI chính |
|---|---|---|---|---|---|---|---|
| T2 (W1) | TikTok | TOFU | Pillar 1 | 3 sai lầm khiến da khô vào mùa đông | Video 45s | Xem thêm ở bio | View & Share |
| T4 (W1) | Blog | TOFU | Pillar 1 | Hướng dẫn cấp ẩm chuyên sâu | Longform | Đọc bài liên quan | Organic Search |
| T6 (W1) | FB/IG | MOFU | Pillar 2 | Review khách hàng sau 14 ngày | Carousel | Inbox nhận mẫu thử | Comment/Inbox |
| CN (W1) | FB Ads | BOFU | Pillar 3 | Ưu đãi combo độc quyền cuối tuần | Single Image | Mua ngay | Conversion Rate |

## 3. Hướng Dẫn Phối Hợp & Sản Xuất (Production Notes)
- Phân công: Bài viết dài chuyển giao cho `content-write-longform-seo`.
- Copy quảng cáo ngắn và caption chuyển giao cho `content-write-short-copy`.
- Nội dung gốc cần nhân bản chuyển giao cho `content-adapt-multichannel`.
```

## Don'ts
- Không lên lịch chỉ toàn bài bán hàng trực tiếp (BOFU) gây nhàm chán và giảm tương tác hữu cơ của kênh.
- Không đưa ra các tiêu đề mơ hồ thiếu góc tiếp cận (tránh viết kiểu "bài viết thứ Hai").
- Không bỏ qua bước liên kết giữa bài đăng với persona và hành trình khách hàng đã duyệt tại `insight/icp.md`.
- Không phân bổ lịch đăng vượt quá nguồn lực sản xuất thực tế của agency hoặc client.

## Quality Checklist
- [ ] Xác định rõ tối thiểu 3 trụ cột nội dung (Content Pillars).
- [ ] Bảng lịch có đủ các trường: Ngày, Kênh, Funnel Stage, Pillar, Angle, Format, CTA, KPI.
- [ ] Tỷ lệ phân bổ giữa các tầng phễu TOFU/MOFU/BOFU cân đối và hợp lý.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/content/editorial-calendar.md`.
