---
name: content-audit-brand-voice
description: "Kiểm định và chấm điểm tính nhất quán giọng điệu thương hiệu (Brand Voice Audit) trên tập nội dung chuẩn bị hoặc đã xuất bản so với Brand Voice Guidelines. Chấm điểm trên thang 100 theo ngưỡng brand_voice_pass_score, chỉ ra các lỗi lệch tone và cung cấp bản viết lại chuẩn hóa. Đầu ra lưu tại docs/marketing-projects/<client-slug>/content/brand-voice-audit.md."
---

# content-audit-brand-voice: Kiểm Định & Hiệu Đính Giọng Điệu Thương Hiệu

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "audit brand voice", "kiểm tra giọng điệu bài viết", "đánh giá xem content có đúng tone không", hoặc trước khi phê duyệt xuất bản hàng loạt bài viết từ nhiều copywriter khác nhau.

## Workflow

### Giai đoạn 1: Tiếp nhận Guideline & Tập Nội dung Cần Kiểm
**Mục tiêu**: Thu thập tiêu chuẩn giọng điệu thương hiệu và danh sách bài viết cần rà soát.
- Trích xuất `brand_voice_guidelines` từ `client_context` trong `config.md` hoặc tài liệu hướng dẫn thương hiệu do người dùng cung cấp:
  - Các tính từ nhận diện thương hiệu (ví dụ: Chuyên gia, Điềm đạm, Gần gũi, Hài hước, Táo bạo).
  - Danh sách từ vựng khuyến khích sử dụng (Do's) và từ cấm kỵ/nhạy cảm (Don'ts / Blacklist).
  - Ngôi xưng hô quy chuẩn với khách hàng (Tôi - Bạn, Chúng tôi - Quý khách, Em - Anh/Chị).
- Tiếp nhận các văn bản nội dung cần kiểm định (bài blog, caption ads, chuỗi email).

### Giai đoạn 2: Chấm điểm & Bóc tách Lỗi Lệch chuẩn (Divergence Analysis)
**Mục tiêu**: Đánh giá trên thang điểm 100 và so sánh với ngưỡng `brand_voice_pass_score` (mặc định 80/100) theo Validation Policy trong `config.md`.
- Đánh giá theo 4 tiêu chí thành phần (mỗi tiêu chí 25 điểm):
  1. **Tính nhất quán về Ngôi xưng & Xưng hô**: Đúng quy chuẩn đã định, không lúc xưng "mình", lúc xưng "tôi", lúc xưng "chúng tôi".
  2. **Mức độ thể hiện Bản sắc (Persona Consistency)**: Giữ đúng phong thái định vị (ví dụ: thương hiệu y tế không dùng tiếng lóng tuổi teen; thương hiệu streetwear không hành văn hành chính).
  3. **Ngữ cảnh & Cảm xúc truyền tải (Emotional Tone)**: Phù hợp với tâm trạng của persona ở từng giai đoạn hành trình.
  4. **Kiểm soát Từ ngữ Cấm & Quy ước Ngành**: Không phạm từ ngữ quảng cáo bị cấm hoặc trái quy tắc đạo đức nghề nghiệp.
- Tính tổng điểm. Nếu tổng điểm < 80, đánh dấu trạng thái CẦN SỬA ĐỔI (REVISION REQUIRED).

### Giai đoạn 3: Đưa ra Báo cáo Hiệu đính & Bản Viết lại Chuẩn mực
**Mục tiêu**: Cung cấp phiên bản chỉnh sửa trực tiếp (Before vs After) và lưu file theo Naming Policy trong `config.md`.
- Trích dẫn chính xác từng đoạn văn bị lệch chuẩn, giải thích nguyên nhân và đưa ra phương án viết lại chuẩn tone.
- Ghi toàn bộ báo cáo vào `docs/marketing-projects/<client-slug>/content/brand-voice-audit.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/content/brand-voice-audit.md`:

```markdown
# Báo Cáo Kiểm Định Giọng Điệu Thương Hiệu (Brand Voice Audit) — <client_name>
- Client Slug: `<client-slug>`
- Ngày thẩm định: <YYYY-MM-DD>
- Điểm đánh giá tổng thể: <Số điểm> / 100
- Trạng thái kiểm định: <ĐẠT CHUẨN (PASS) | CẦN HIỆU ĐÍNH (REVISION REQUIRED)> (Ngưỡng đạt: >= 80 điểm)

## 1. Bảng Điểm Thành Phần
| Tiêu chí thẩm định | Điểm đạt được | Điểm tối đa | Nhận xét nhanh |
|---|---|---|---|
| 1. Quy chuẩn xưng hô & đại từ | ... | 25 | ... |
| 2. Nhất quán phong cách & bản sắc | ... | 25 | ... |
| 3. Cảm xúc & Ngữ điệu tiếp cận | ... | 25 | ... |
| 4. Tuân thủ từ vựng & Không dùng từ cấm | ... | 25 | ... |
| **Tổng điểm** | **...** | **100** | **...** |

## 2. Chi Tiết Lỗi Lệch Chuẩn & Bảng Hiệu Đính (Before / After)

### Điểm lệch 1: <Tên lỗi, ví dụ: Sai ngôi xưng và dùng từ ngữ suồng sã>
- **Đoạn gốc (Before)**:
  > "...<Trích dẫn đoạn văn gốc>..."
- **Nguyên nhân lệch tone**: <Giải thích tại sao cách hành văn này mâu thuẫn với guideline>
- **Bản hiệu đính đề xuất (After)**:
  > "...<Đoạn văn viết lại đúng chuẩn brand voice>..."

### Điểm lệch 2: <Tên lỗi>
...

## 3. Khuyến Nghị Cho Đội Ngũ Sáng Tạo Nội Dung
- Hướng dẫn thực hành ngắn gọn để tránh lặp lại lỗi trên các bài viết tiếp theo.
```

## Don'ts
- Không nhận xét cảm tính mơ hồ như "nghe chưa hay", "hơi kỳ"; mọi nhận xét phải đối chiếu trực tiếp với quy chuẩn trong `brand_voice_guidelines`.
- Không tự ý thay đổi ý nghĩa hay thông điệp cốt lõi của nội dung trong quá trình viết lại; chỉ hiệu đính ngữ điệu và câu từ.
- Không cho phép nội dung có điểm dưới 80 vượt qua Pre-Launch QA Gate.
- Không áp đặt tone giọng cá nhân của reviewer lên thương hiệu của client.

## Quality Checklist
- [ ] Báo cáo có bảng điểm thành phần minh bạch trên thang 100 điểm.
- [ ] Đối chiếu rõ ràng với ngưỡng `brand_voice_pass_score` (80/100) theo Validation Policy trong `config.md`.
- [ ] Mọi điểm trừ đều có trích dẫn đoạn gốc kèm bản viết lại (Before / After).
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/content/brand-voice-audit.md`.
