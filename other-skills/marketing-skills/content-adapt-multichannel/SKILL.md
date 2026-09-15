---
name: content-adapt-multichannel
description: "Tái sử dụng và biến đổi nội dung gốc (Repurpose Content: bài blog dài, case study, báo cáo nghiên cứu) thành bộ tài sản nội dung đa kênh (kịch bản video ngắn TikTok/Reels, bài Carousel LinkedIn/Facebook, Email Newsletter, Infographic concept). Kích hoạt khi có yêu cầu 'repurpose content', 'chuyển bài blog sang TikTok', 'phóng tác nội dung đa kênh'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/content/multichannel-pack/<topic-slug>.md."
---

# content-adapt-multichannel: Tái Khai Thác & Bản Địa Hóa Nội Dung Đa Kênh

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "repurpose nội dung này", "chuyển bài viết sang kịch bản video TikTok", "tạo slide carousel từ bài blog", "soạn bản tin email từ bài viết gốc", hoặc muốn tối đa hóa vòng đời của một tài sản nội dung lớn.

## Workflow

### Giai đoạn 1: Bóc tách Cốt lõi & Điểm Nhấn Giá trị từ Nội dung Gốc
**Mục tiêu**: Đọc nội dung nguồn và trích xuất các ý tưởng có khả năng viral hoặc giá trị thực hành cao.
- Tiếp nhận nội dung gốc (từ file `docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md` hoặc văn bản người dùng cung cấp).
- Trích xuất: 1 luận điểm trung tâm, 3-5 mẹo thực chiến (Tips/Tactics), các số liệu/biểu đồ ấn tượng, và câu trích dẫn đắt giá (Punchline/Quote).
- Xác định danh sách kênh đích cần chuyển đổi: TikTok/Reels (Video ngắn), Facebook/LinkedIn (Carousel hoặc bài phân tích), Email Newsletter (Bản tin cá nhân hóa).

### Giai đoạn 2: Định dạng Lại theo Đặc thù Từng Nền tảng
**Mục tiêu**: Viết lại nội dung phù hợp với thuật toán và thói quen tiêu thụ của người dùng từng kênh.
- **Kênh 1: Kịch bản Video Ngắn (TikTok / Instagram Reels / YouTube Shorts)**:
  - Thời lượng: 45 – 60 giây.
  - Cấu trúc: Hook thị giác/âm thanh 3 giây đầu -> 3 luận điểm dồn dập (mỗi ý 10s) -> CTA kêu gọi follow/comment.
  - Ghi chú khung hình (Visual cues): Mô tả hành động, chữ chạy trên màn hình (On-screen text), âm thanh nền.
- **Kênh 2: Kịch bản Slide Carousel (LinkedIn / Facebook / Instagram)**:
  - Số lượng slide: 6 – 10 slide.
  - Slide 1: Hook slide giật gân, hình ảnh gợi mở.
  - Slide 2-7: Mỗi slide 1 luận điểm súc tích (dưới 30 từ/slide).
  - Slide cuối: Tóm tắt bài học & CTA tương tác (Save bài viết, share).
- **Kênh 3: Bản tin Email Newsletter**:
  - Dòng tiêu đề thân mật (Subject line có tỷ lệ mở cao).
  - Giọng điệu trò chuyện trực tiếp (1-on-1), kể câu chuyện ngắn dẫn dắt đến bài học từ nội dung gốc.
  - Đường link trỏ về đọc bài viết đầy đủ trên website.

### Giai đoạn 3: Đóng gói Bộ Asset & Lưu Deliverable
**Mục tiêu**: Tập hợp tất cả các phiên bản chuyển đổi vào một tập tin duy nhất theo Naming Policy trong `config.md`.
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/content/multichannel-pack/<topic-slug>.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/content/multichannel-pack/<topic-slug>.md`:

```markdown
# Bộ Nội Dung Phân Phối Đa Kênh (Multichannel Content Pack) — <client_name>
- Client Slug: `<client-slug>`
- Chủ đề: <topic-slug>
- Nguồn gốc: <Link hoặc tên bài viết gốc>
- Ngày tạo: <YYYY-MM-DD>

## 1. Kịch Bản Video Ngắn (TikTok / Reels / Shorts - 60s)
- **Hook 3s đầu**: "[Câu mở đầu gây sốc hoặc thách thức quan niệm cũ]"
- **Text hiển thị trên màn hình (Text Overlay)**: ...
- **Phân cảnh chi tiết**:
  - `00-03s`: [Mô tả hình ảnh] - [Lời thoại]
  - `03-20s`: [Ý 1] - [Lời thoại]
  - `20-40s`: [Ý 2] - [Lời thoại]
  - `40-55s`: [Ý 3] - [Lời thoại]
  - `55-60s`: [CTA] - "Lưu ngay video này nếu bạn không muốn..."

## 2. Dàn Ý & Nội Dung Slide Carousel (LinkedIn / Instagram / Facebook)
- **Slide 1 (Bìa Hook)**: <Tiêu đề lớn giật mắt>
- **Slide 2 (Vấn đề)**: <Tại sao 90% người làm điều này thất bại>
- **Slide 3 - 6 (Giải pháp từng bước)**: <Mỗi slide 1 mẹo thực chiến>
- **Slide 7 (Tóm tắt)**: <Infographic thu nhỏ>
- **Slide 8 (CTA)**: "Nhấn Lưu để xem lại khi cần & Theo dõi để đón đọc bài sau."

## 3. Bản Tin Email Newsletter (Dành cho Tệp Subscriber)
- **Tiêu đề email (Subject Line)**: ...
- **Pre-header text**: ...
- **Thân email**:
  Chào bạn,
  <Câu chuyện mở đầu ngắn gọn dẫn tới bài học>
  ...
  <CTA link về bài viết gốc trên website>
```

## Don'ts
- Không sao chép nguyên si đoạn văn từ bài blog sang kịch bản video hoặc slide mà không biên tập lại ngữ điệu.
- Không làm slide carousel chứa quá nhiều chữ biến thành trang văn bản thu nhỏ.
- Không viết kịch bản video thiếu chỉ dẫn hình ảnh (Visual cues) cho người quay/dựng.
- Không phân phối cùng một câu chữ y hệt lên mọi kênh khiến khán giả bị nhàm chán khi theo dõi đa kênh.

## Quality Checklist
- [ ] Gói nội dung có đầy đủ ít nhất 3 định dạng: Video ngắn, Carousel slide, và Email newsletter.
- [ ] Kịch bản video có phân tách rõ ràng giữa lời thoại, hành động visual và text overlay.
- [ ] Slide Carousel có cấu trúc hook - thân - CTA tinh gọn, dễ đọc lướt trên màn hình điện thoại.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/content/multichannel-pack/<topic-slug>.md`.
