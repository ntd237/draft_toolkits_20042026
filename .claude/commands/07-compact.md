---
description: "Tạo một bản tóm tắt chi tiết về cuộc hội thoại cho đến nay, chú ý kỹ đến các yêu cầu rõ ràng của người dùng và các hành động trước đó của bạn."
---

Nhiệm vụ của bạn là tạo một bản tóm tắt chi tiết về cuộc hội thoại cho đến nay, chú ý kỹ đến các yêu cầu rõ ràng của người dùng và các hành động trước đó của bạn.
Bản tóm tắt của bạn phải bao gồm toàn bộ mốc thời gian từ yêu cầu đầu tiên của người dùng trong cuộc hội thoại cho đến thời điểm hiện tại.
Bạn phải luôn viết bản tóm tắt bằng tiếng Việt.
Bản tóm tắt này cần phải thấu đáo trong việc nắm bắt các chi tiết kỹ thuật, các mẫu mã nguồn (code patterns) và các quyết định về kiến trúc vốn sẽ rất cần thiết để tiếp tục công việc phát triển mà không làm mất đi ngữ cảnh.

**Thời gian ước tính**: 3-5 phút (tùy thuộc vào độ dài của cuộc hội thoại)

---

## Khi nào nên sử dụng lệnh này

**Nên sử dụng khi:**
- **Cuộc hội thoại dài** và phức tạp (>10 lượt trao đổi)
- **Cần lưu trữ ngữ cảnh** cho công việc trong tương lai
- **Chuyển đổi tác vụ** hoặc tạm nghỉ
- **Người dùng yêu cầu cụ thể** bản tóm tắt

**Không sử dụng cho:**
- Các cuộc hội thoại ngắn (<5 lượt trao đổi)
- Các câu hỏi đáp đơn giản không có thay đổi về mã nguồn

---

## Các cấp độ tóm tắt

Chọn mức độ chi tiết phù hợp dựa trên độ phức tạp của cuộc hội thoại:
1. **Quick Compact (Tối giản nhanh - 5-10 lượt trao đổi):** Tập trung vào Bảng Trạng thái Tệp tin và Các Tác vụ Đang chờ. Bỏ qua các mô tả dài.
2. **Deep Compact (Tối giản sâu - >10 lượt trao đổi hoặc có các thay đổi kiến trúc phức tạp):** Bản tóm tắt đầy đủ 8 phần bao gồm phân tích kỹ thuật và các sơ đồ tùy chọn.

---

Trước khi đưa ra bản tóm tắt cuối cùng của bạn, hãy viết một phần **Phân tích (Analysis)** để sắp xếp các suy nghĩ của bạn và đảm bảo bạn đã bao quát hết các điểm cần thiết. Trong quá trình phân tích của bạn:

1. Phân tích theo trình tự thời gian từng tin nhắn và từng phần của cuộc hội thoại. Đối với mỗi phần, hãy xác định kỹ:
   - Các yêu cầu và ý định rõ ràng của người dùng
   - Cách tiếp cận của bạn để xử lý các yêu cầu của người dùng
   - Các quyết định chính, các khái niệm kỹ thuật và các mẫu mã nguồn (code patterns)
   - Các chi tiết cụ thể như tên tệp, chữ ký hàm, các chỉnh sửa tệp, v.v.
   - **Lưu ý về hiệu suất:** Tránh đưa vào "các đoạn mã đầy đủ" trừ khi thực sự quan trọng. Sử dụng các bản so sánh (diff) ngắn gọn hoặc dẫn chiếu số dòng/tên hàm để tiết kiệm token ngữ cảnh.
2. Kiểm tra lại độ chính xác về kỹ thuật và tính đầy đủ, giải quyết triệt để từng thành phần bắt buộc.

Bản tóm tắt của bạn nên bao gồm các phần sau:

1. **Yêu cầu và Ý định Chính:** Ghi lại chi tiết tất cả các yêu cầu và ý định rõ ràng của người dùng.
2. **Các Khái niệm Kỹ thuật then chốt:** Liệt kê tất cả các khái niệm kỹ thuật, công nghệ và framework quan trọng đã thảo luận.
3. **Bảng Trạng thái Tệp tin:** Một bảng ngắn gọn hiển thị các tệp đã được tạo, sửa đổi hoặc xóa.
   | Tên tệp | Trạng thái | Các thay đổi chính |
   | :--- | :--- | :--- |
   | [Tên] | [Đã tạo/Đã sửa/Đã xóa] | [Tóm tắt ngắn gọn] |
4. **Kiến trúc Dự án (Tùy chọn):** Sử dụng cú pháp **Mermaid** nếu cuộc hội thoại liên quan đến các luồng dữ liệu hoặc thay đổi cấu trúc phức tạp.
5. **Các thay đổi chi tiết:** Liệt kê các tệp và đoạn mã cụ thể đã được xem xét hoặc sửa đổi. Sử dụng các bản diff ngắn gọn hoặc các đoạn mã tập trung. Bao gồm một bản tóm tắt tại sao mỗi thay đổi lại quan trọng.
6. **Giải quyết Vấn đề:** Tài liệu hóa các vấn đề đã giải quyết và bất kỳ nỗ lực xử lý sự cố nào đang thực hiện.
7. **Tác vụ Đang chờ & Bước tiếp theo:** Phác thảo các tác vụ đang chờ và bước tiếp theo ngay lập tức (kèm theo các trích dẫn trực tiếp từ cuộc hội thoại để đảm bảo tính nhất quán trong diễn giải).
8. **Tóm tắt Bàn giao (Handover):** Một đoạn văn duy nhất tóm tắt "Trạng thái của Dự án" cho một khởi đầu mới.

---

Vui lòng cung cấp bản tóm tắt dựa trên cuộc hội thoại cho đến nay, tuân theo cấu trúc này và đảm bảo tính chính xác cũng như sự thấu đáo trong phản hồi của bạn.