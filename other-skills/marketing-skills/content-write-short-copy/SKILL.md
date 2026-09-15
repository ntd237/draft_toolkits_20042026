---
name: content-write-short-copy
description: "Sáng tạo nội dung ngắn hiệu suất cao (caption social, ad copy Meta/Google/TikTok, headline, hook mở đầu, CTA) theo các công thức AIDA, PAS, BAB, FAB với 3-5 biến thể A/B testing. Kích hoạt khi có yêu cầu 'viết caption', 'viết ad copy', 'soạn nội dung chạy ads'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/content/short-copy/<campaign-slug>.md."
---

# content-write-short-copy: Sáng Tạo Copy Ngắn & Biến Thể Quảng Cáo Đa Kênh

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "viết ad copy", "viết caption Facebook/Instagram/TikTok", "tạo headline quảng cáo", "viết nội dung chạy ads", hoặc cần các biến thể copy cho chiến dịch test quảng cáo.

## Workflow

### Giai đoạn 1: Tiếp nhận Sản phẩm, Offer & Nền tảng Đích
**Mục tiêu**: Thu thập các yếu tố cốt lõi của ưu đãi và xác định ranh giới kỹ thuật của nền tảng.
- Trích xuất thông tin sản phẩm/dịch vụ, USP, ưu đãi chính (Offer: giảm giá, quà tặng, dùng thử, bảo hành).
- Đọc đặc tính persona từ `insight/icp.md` để chọn điểm chạm cảm xúc (Trigger).
- Xác định nền tảng đăng tải: Facebook Ads (feed/story), Google Search/Responsive Ads, TikTok Video Caption, Instagram Feed.
- Thiết lập số lượng biến thể cần tạo: 3 đến 5 biến thể theo ngưỡng `short_copy_variants` trong Validation Policy của `config.md`.

### Giai đoạn 2: Sáng tạo Biến thể Copy theo Khung Công thức
**Mục tiêu**: Viết 3-5 biến thể tiếp cận từ các góc tâm lý khác nhau để phục vụ A/B testing.
- **Biến thể 1: Công thức PAS (Problem - Agitate - Solve)**:
  - Nêu bật nỗi đau nhức nhối -> Xoáy sâu vào hậu quả nếu trì hoãn -> Đưa ra sản phẩm như liều thuốc giải.
- **Biến thể 2: Công thức AIDA (Attention - Interest - Desire - Action)**:
  - Hook giật mình -> Khơi gợi sự tò mò -> Kích thích khao khát sở hữu -> Kêu gọi hành động dứt khoát.
- **Biến thể 3: Công thức BAB (Before - After - Bridge)**:
  - Tình trạng bế tắc trước đây -> Viễn cảnh tươi đẹp sau khi dùng -> Chiếc cầu nối là sản phẩm.
- **Biến thể 4: Công thức FAB (Features - Advantages - Benefits)**:
  - Tính năng độc đáo -> Ưu điểm vượt trội -> Lợi ích thiết thực mà khách hàng thụ hưởng.
- **Biến thể 5 (Social Proof & Urgency)**:
  - Bằng chứng xã hội (Feedback, số lượng người tin dùng) kết hợp sự khan hiếm về thời gian/số lượng.

### Giai đoạn 3: Rà soát Kỹ thuật, Hashtag & Lưu Deliverable
**Mục tiêu**: Kiểm tra giới hạn ký tự từng kênh, tối ưu CTA và ghi file theo Naming Policy trong `config.md`.
- Rà soát giới hạn ký tự (Primary text, Headline 40 ký tự, Description 30 ký tự đối với Google/Meta Ads).
- Đề xuất bộ hashtag tối ưu và định dạng emoji phù hợp với `brand_voice_guidelines`.
- Lưu kết quả vào `docs/marketing-projects/<client-slug>/content/short-copy/<campaign-slug>.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/content/short-copy/<campaign-slug>.md`:

```markdown
# Bộ Biến Thể Copy Ngắn & Quảng Cáo (Short Copy Pack) — <client_name>
- Client Slug: `<client-slug>`
- Chiến dịch: <campaign-slug>
- Nền tảng: <Facebook Ads / TikTok / Google Ads>
- Ngày soạn: <YYYY-MM-DD>

## 1. Tóm Tắt Ưu Đãi & Thông Điệp Cốt Lõi
- **Sản phẩm / Dịch vụ**: ...
- **Offer chính**: ...
- **Target Persona**: ...

## 2. Danh Sách Biến Thể A/B Testing (3 - 5 Biến Thể)

### Biến Thể 1 (Góc Tiếp Cận: PAS — Đánh Vào Nỗi Đau)
- **Headline (Tiêu đề)**: <Tiêu đề sắc bén dưới 40 ký tự>
- **Hook 3 giây / Dòng mở đầu**: <Câu mở đầu giữ chân người đọc>
- **Body Copy**:
  <Nội dung triển khai xoáy sâu vào vấn đề và đưa ra giải pháp>
- **Call to Action (CTA)**: <Nút bấm & lời kêu gọi, ví dụ: Nhận tư vấn ngay>
- **Ghi chú Creative**: <Gợi ý hình ảnh/video phù hợp: hình ảnh người nhăn trán mệt mỏi>

### Biến Thể 2 (Góc Tiếp Cận: AIDA — Kích Thích Khao Khát)
- **Headline**: ...
- **Hook**: ...
- **Body Copy**: ...
- **CTA**: ...
- **Ghi chú Creative**: ...

### Biến Thể 3 (Góc Tiếp Cận: BAB — Trước & Sau Chuyển Hóa)
- **Headline**: ...
- **Hook**: ...
- **Body Copy**: ...
- **CTA**: ...
- **Ghi chú Creative**: ...

## 3. Khuyến Nghị Setup Test A/B
- Chạy phân bổ ngân sách đều giữa các biến thể trong 3-5 ngày đầu để tìm ra copy chiến thắng (Winning copy).
```

## Don'ts
- Không dùng từ ngữ vi phạm chính sách quảng cáo của Meta/Google (tuyên bố chữa dứt điểm 100%, so sánh trước/sau hở da thịt, body shaming, cam kết tài chính phi thực tế).
- Không viết các biến thể chỉ thay đổi vài từ đơn giản; mỗi biến thể phải mang một góc tiếp cận tâm lý (Angle) khác biệt.
- Không để copy trôi nổi thiếu lời kêu gọi hành động (CTA) rõ ràng.
- Không viết copy quá dài lê thê làm mất nhịp điệu đọc nhanh của người dùng di động.

## Quality Checklist
- [ ] Số lượng biến thể đạt từ 3 đến 5 theo đúng Validation Policy trong `config.md`.
- [ ] Mỗi biến thể sử dụng một mô hình copywriting riêng biệt (PAS, AIDA, BAB, FAB).
- [ ] Đầy đủ Headline, Hook, Body text, CTA và gợi ý creative cho designer.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/content/short-copy/<campaign-slug>.md`.
