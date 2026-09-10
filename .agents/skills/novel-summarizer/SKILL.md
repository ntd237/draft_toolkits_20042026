---
name: novel-summarizer
description: "Đọc và tóm tắt chi tiết, chính xác nội dung từng chương và dải chương tiểu thuyết (web novel, kiếm hiệp, tiên hiệp, huyền huyễn, light novel) từ đường link hoặc dải URL yêu cầu. Kích hoạt khi người dùng cung cấp link truyện hoặc quy luật URL kèm dải chương (ví dụ: từ chương 5 đến chương 8) và muốn có bản tóm tắt chi tiết, có cấu trúc, độ chính xác cao cho toàn bộ dải chương mà không bỏ sót sự kiện chính."
---

# Skill: novel-summarizer

## Điều kiện kích hoạt
Người dùng cung cấp liên kết truyện (hoặc quy luật URL và dải chương, ví dụ từ chương `05` đến chương `08`) của một bộ tiểu thuyết — tiên hiệp, huyền huyễn, ngôn tình, kiếm hiệp, đô thị, light novel, v.v. — và yêu cầu tóm tắt toàn bộ dải chương với đầy đủ chi tiết từng chương.

## Quy trình thực hiện

### Giai đoạn 1: Xác định quy luật URL & Lập danh sách chương
**Mục tiêu**: Xác định quy luật tạo URL cho dải chương được yêu cầu.

- Phân tích liên kết mẫu để tìm vị trí số chương:
  - Dạng số nguyên: `.../chuong-5.html` → `.../chuong-6.html`, `.../chuong-7.html`
  - Dạng đệm số không (zero-padded): `.../c05` → `.../c06`, `.../c07`
  - Dạng slug kèm tiêu đề: nếu URL có chứa tiêu đề chương (ví dụ: `chuong-5-khoi-dau`), thử tải chương đầu tiên hoặc tìm liên kết chương tiếp theo từ HTML của chương hiện tại.
- Lập danh sách các URL cần truy cập từ $N_{start}$ đến $N_{end}$.

### Giai đoạn 2: Lấy nội dung từng chương
**Mục tiêu**: Lấy nội dung văn bản thô cho từng chương trong dải.

- Sử dụng `read_url_content` để lấy nội dung văn bản thô của từng liên kết trong dải.
- Kiểm tra và xử lý dữ liệu trả về:
  - **Thành công**: Trích xuất tiêu đề chương và toàn bộ nội dung văn bản thân chương.
  - **Lỗi** (404, 403, Cloudflare, tường phí/paywall hoặc nội dung rỗng): Ghi nhận lỗi cho chương đó. Nếu không thể vượt qua rào cản, báo cáo rõ ràng cho người dùng biết chương nào bị lỗi và đề xuất họ dán trực tiếp nội dung thô của chương đó vào cuộc hội thoại.

### Giai đoạn 3: Tiền xử lý & Trích xuất sự kiện cốt lõi
**Mục tiêu**: Tách nội dung truyện khỏi tạp âm và ghi nhận các thực thể quan trọng.

- Loại bỏ mọi tạp âm: Lời nhắn của converter/dịch giả, quảng cáo website, liên kết chương trước/sau, bình luận.
- Nhận diện và ghi chú các thực thể chính:
  - **Nhân vật**: Nhân vật chính, nhân vật phụ, phản diện xuất hiện hoặc được nhắc tới.
  - **Bối cảnh & Địa điểm**: Nơi diễn ra sự kiện, thời gian, các thế lực/môn phái liên quan.
  - **Bảo toàn danh từ riêng**: Giữ nguyên tên nhân vật, địa danh, công pháp, chiêu thức, cảnh giới tu luyện, pháp bảo/vật phẩm theo dạng gốc (Hán-Việt hoặc phiên âm gốc), đảm bảo tính nhất quán xuyên suốt các chương.

### Giai đoạn 4: Tóm tắt có cấu trúc
**Mục tiêu**: Xây dựng bản tóm tắt từng chương gồm 4 thành phần cùng phần tổng quan diễn biến.

Với mỗi chương, xuất bản tóm tắt gồm:
1. **Tiêu đề & Thông tin chương**: Số thứ tự chương và tên chương (nếu có).
2. **Nhân vật & Địa điểm**: Các thực thể then chốt xuất hiện trong chương.
3. **Diễn biến chính**: Dòng thời gian tuần tự (3–6 gạch đầu dòng súc tích nắm bắt các sự kiện quan trọng).
4. **Điểm nhấn & Tình huống kết (Cliffhanger)**: Kỹ thuật dẫn dắt (cài cắm/plot twist), biến cố bất ngờ hoặc câu hỏi mở ở cuối chương.

Sau đó xây dựng **Tổng quan dải chương (Arc Overview)**: Tóm tắt ngắn gọn 1–2 đoạn văn về tiến trình cốt truyện xuyên suốt từ chương đầu đến chương cuối của dải.

### Giai đoạn 5: Kiểm tra độ chuẩn xác & Xuất kết quả
**Mục tiêu**: Đối chiếu bản tóm tắt với nguồn truyện trước khi bàn giao.

- Chạy Danh sách kiểm tra chất lượng (Quality Checklist). Xác nhận không có chi tiết bịa đặt, không nhầm lẫn tên gọi, không bỏ sót sự kiện mấu chốt.
- Xuất kết quả hoàn chỉnh theo định dạng Markdown (xem Định dạng đầu ra bên dưới).

## Định dạng đầu ra

```markdown
# 📖 TÓM TẮT TIỂU THUYẾT: [TÊN TRUYỆN] (NẾU XÁC ĐỊNH ĐƯỢC)
> **Dải chương**: Từ Chương [X] đến Chương [Y] | **Tổng số chương**: [Z] chương

---

## 🌟 TỔNG QUAN DẢI CHƯƠNG [X] - [Y]
*(Tóm tắt cô đọng 1–2 đoạn văn về diễn biến cốt truyện chính, bước ngoặt lớn và tiến trình phát triển của dải chương này).*

---

## 📜 CHI TIẾT TỪNG CHƯƠNG

### 🔹 Chương [X]: [Tên Chương]
- **📍 Bối cảnh & Nhân vật**: [Địa điểm diễn ra] | [Các nhân vật xuất hiện chính]
- **⚡ Diễn biến chính**:
  - [Sự kiện 1: Khởi đầu chương hoặc tiếp nối diễn biến trước...]
  - [Sự kiện 2: Biến cố/xung đột/cuộc đối thoại quan trọng...]
  - [Sự kiện 3: Hành động quyết định hoặc kết quả giải quyết...]
- **🎯 Điểm nhấn / Kết chương**: [Tình huống kết thúc, cú twist hoặc câu hỏi mở ở cuối chương].

*(Lặp lại cấu trúc trên cho các chương tiếp theo trong dải)*

---

## 🔑 ĐIỂM NHẤN CỐT TRUYỆN & TIẾN TRIỂN NHÂN VẬT
- **Chuyển biến nhân vật**: [Sự thay đổi về tâm lý, cảnh giới, sức mạnh hoặc quan hệ giữa các nhân vật].
- **Thế lực & Mối quan hệ**: [Liên minh mới, kẻ thù xuất hiện hoặc mâu thuẫn mới nảy sinh].
- **Manh mối / Hố chưa lấp (Foreshadowing)**: [Các chi tiết bí ẩn được tác giả cài cắm cho các chương sau].
```

## Những điều cần tránh
- Không tự bịa đặt nội dung cốt truyện cho những chương tải lỗi hoặc chưa đọc — phải báo cáo rõ ràng việc thiếu dữ liệu.
- Không viết tóm tắt hời hợt một dòng như "Chương này nhân vật A đánh nhau với nhân vật B rồi thắng" mà thiếu bối cảnh hoặc nguyên nhân.
- Không trộn lẫn suy đoán/phân tích cài cắm vào phần diễn biến chính — đặt các ghi chú diễn giải vào đúng mục Manh mối / Foreshadowing chuyên biệt.
- Không tự ý dịch hoặc làm biến đổi danh từ riêng (tên gọi, công pháp, cảnh giới tu luyện, pháp bảo/vật phẩm) làm sai lệch nghĩa gốc.
- Không đưa tạp âm website (watermark, lời nhắn dịch giả, quảng cáo) vào bản tóm tắt.
- Không đảo lộn thứ tự sự kiện trái với dòng thời gian gốc của chương truyện.

## Danh sách kiểm tra chất lượng
- [ ] Đã đọc đầy đủ toàn bộ các chương trong dải yêu cầu ($N_{start}$ đến $N_{end}$)?
- [ ] Danh từ riêng, cách xưng hô và thuật ngữ có chuẩn xác và nhất quán xuyên suốt các chương không?
- [ ] Diễn biến chính của từng chương có bao quát được các điểm nút cốt truyện quan trọng không?
- [ ] Các sự kiện tóm tắt đã được tách biệt rõ ràng với phần phân tích/tiến triển nhân vật chưa?
- [ ] Có báo cáo rõ các chương bị lỗi cho người dùng thay vì tự bịa nội dung thay thế không?
