---
name: cro-audit-landing-page
description: "Audit tối ưu hóa tỷ lệ chuyển đổi trang đích (Landing Page CRO Audit): phân tích trải nghiệm người dùng UX/UI trên di động, ma sát biểu mẫu điền thông tin (Form Friction), tín hiệu uy tín (Trust Signals), tính thuyết phục của CTA, và sự đồng nhất thông điệp với quảng cáo (Message Match). Phân loại lỗi theo ma trận Tác động vs Độ khó (Impact vs Effort Matrix). Kích hoạt khi có yêu cầu 'audit landing page', 'tỷ lệ chuyển đổi thấp', 'tối ưu trang đích'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/analytics/landing-page-cro.md."
---

# cro-audit-landing-page: Audit Tối Ưu Hóa Tỷ Lệ Chuyển Đổi Trang Đích

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng cung cấp URL landing page/website và yêu cầu "audit landing page", "tối ưu tỷ lệ chuyển đổi", "tại sao chạy ads nhiều click nhưng không ra đơn", "landing page conversion rate thấp", hoặc sau khi phát hiện điểm nghẽn chuyển đổi từ `ads-diagnose-underperformance`.

## Workflow

### Giai đoạn 1: Tiếp nhận URL Trang Đích & Thu Thập Chỉ Số Hiện Trạng
**Mục tiêu**: Nắm bắt lưu lượng truy cập, tỷ lệ chuyển đổi hiện tại và thông điệp quảng cáo nguồn dẫn về trang.
- Tiếp nhận URL trang đích cần audit, tỷ lệ chuyển đổi hiện tại (ví dụ: CR chỉ đạt 0.5% - 1.0%), và nguồn lưu lượng chủ đạo (Mobile hay Desktop, từ Facebook Ads hay Google Ads).
- Đọc thông điệp và hình ảnh quảng cáo đang chạy từ `content/short-copy/` hoặc `seo-ads/creative-briefs/` để kiểm tra độ khớp thông điệp (Message Match).

### Giai đoạn 2: Khảo sát Heuristic Đa Chiều theo 5 Trụ Cột CRO
**Mục tiêu**: Rà soát từng khu vực trên trang đích theo khung đánh giá chuyển đổi chuyên sâu.
- **1. Khu vực Đầu trang (Above-the-Fold & First Screen)**:
  - Tiêu đề (Headline): Có trả lời được 3 câu hỏi của khách hàng trong 5 giây đầu: "Đây là cái gì?", "Nó giúp gì cho tôi?", và "Làm sao để nhận nó?" không.
  - Hình ảnh minh họa (Hero Visual): Có thể hiện rõ sản phẩm đang hoạt động hay chỉ là hình ảnh minh họa stock vô hồn.
  - Nút bấm CTA chính: Có nổi bật, tương phản màu sắc và hiển thị ngay trên màn hình đầu tiên không.
- **2. Tính Đồng nhất Thông điệp (Message Match)**:
  - Khách hàng bấm vào quảng cáo "Giảm giá 40% kem chống nắng" thì khi vào trang đích có nhìn thấy ngay ưu đãi 40% kem chống nắng hay phải cuộn tìm kiếm.
- **3. Ma sát Biểu mẫu & Thao tác (Form & Checkout Friction)**:
  - Số lượng trường thông tin cần điền: Có đang bắt khách điền quá nhiều thông tin không cần thiết (địa chỉ chi tiết, ngày sinh, ghi chú) trước khi chốt đơn không.
  - Tự động điền (Autofill), hiển thị bàn phím số khi nhập số điện thoại, thông báo lỗi trực quan (Inline validation).
- **4. Tín hiệu Tạo Niềm tin & Giảm Thiểu Rủi ro (Trust Signals & Risk Reversal)**:
  - Có đánh giá thực tế của khách hàng (Reviews kèm ảnh thật/video), chứng nhận y tế/chất lượng, chính sách bảo hành, đổi trả hàng rõ ràng không.
- **5. Trải nghiệm Tốc độ & Giao diện Di động (Mobile UX & Speed)**:
  - Tốc độ hiển thị nội dung trên mạng 4G di động. Có bị pop-up che khuất màn hình hay nút bấm quá nhỏ khó chạm (Fat finger error) không.

### Giai đoạn 3: Phân Loại Thứ Tự Ưu Tiên (Impact vs Effort) & Xuất Deliverable
**Mục tiêu**: Xếp hạng các giải pháp cần khắc phục và lưu file theo Naming Policy trong `config.md`.
- Sắp xếp giải pháp theo ma trận: Quick Wins (Tác động cao - Tốn ít công sức làm ngay), Major Projects (Tác động cao - Cần code phức tạp), Fill-ins (Tác động thấp), và Time Wasters (Không nên làm).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/analytics/landing-page-cro.md`.
- Handoff các ý tưởng cải tiến sang `cro-design-ab-test` nếu lưu lượng truy cập đủ lớn để thiết lập thử nghiệm phân tách.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/analytics/landing-page-cro.md`:

```markdown
# Báo Cáo Audit Tỷ Lệ Chuyển Đổi Trang Đích (Landing Page CRO Audit) — <client_name>
- Client Slug: `<client-slug>`
- URL Trang Đích: <URL>
- Tỷ lệ chuyển đổi hiện tại: <CR hiện tại, ví dụ: 0.65%>
- Mục tiêu CR kỳ vọng: >= 2.50%
- Ngày thẩm định: <YYYY-MM-DD>

## 1. Tóm Tắt Đánh Giá Tổng Thể (Scorecard)
- **Điểm trải nghiệm Above-the-fold**: 5/10 (Tiêu đề mơ hồ, CTA chìm)
- **Điểm đồng nhất thông điệp (Message Match)**: 4/10 (Nội dung trên ads không thấy trên màn 1)
- **Điểm ma sát biểu mẫu (Friction)**: 3/10 (Form 8 trường thông tin quá dài)
- **Điểm tín hiệu uy tín (Trust)**: 6/10 (Thiếu feedback có hình ảnh thực tế)
- **Điểm tối ưu di động (Mobile UX)**: 7/10 (Giao diện chuẩn nhưng tải hơi chậm)

## 2. Bảng Danh Mục Điểm Nghẽn & Khuyến Nghị Khắc Phục (Impact vs Effort)
| STT | Vị trí / Yếu tố | Vấn đề phát hiện | Mức độ tác động (Impact) | Độ khó kỹ thuật (Effort) | Khuyến nghị cải tiến cụ thể |
|---|---|---|---|---|---|
| 1 | **Form Đăng Ký** | Yêu cầu 8 trường dữ liệu (gồm cả địa chỉ chi tiết) | 🔴 Cao (High) | 🟢 Dễ (Low) - Quick Win | Cắt giảm còn 2 trường: "Họ tên" và "Số điện thoại" |
| 2 | **Khu vực Màn 1** | Tiêu đề trừu tượng, nút CTA chìm vào nền trắng | 🔴 Cao (High) | 🟢 Dễ (Low) - Quick Win | Đổi sang headline PAS rõ lợi ích, nút màu cam nổi bật |
| 3 | **Message Match** | Ads nói "Tặng voucher 100k" nhưng vào trang không thấy | 🔴 Cao (High) | 🟢 Dễ (Low) - Quick Win | Treo thanh thông báo (Sticky bar) gắn mã voucher ở đỉnh |
| 4 | **Social Proof** | Đánh giá dạng chữ không có ảnh đại diện hay người thật | 🟡 Trung bình | 🟡 Trung bình | Bổ sung 3 video review thực tế của khách hàng |
| 5 | **Tốc độ tải ảnh** | Ảnh sản phẩm chưa nén nặng 4MB khiến LCP mất 4.8s | 🔴 Cao (High) | 🟢 Dễ (Low) | Nén sang WebP dưới 100KB, bật lazy-loading |

## 3. Bản Phác Thảo Giao Diện Mới Đề Xuất (Wireframe Concept)
- [Mô tả bố cục mới cho Màn hình 1 trên điện thoại: Headline + Sub-headline + 3 gạch đầu dòng cam kết + Nút CTA dính đáy màn hình (Sticky Bottom CTA)].
```

## Don'ts
- Không nhận xét giao diện dựa trên sở thích thẩm mỹ cá nhân ("màu này tôi không thích"); mọi khuyến nghị phải dựa trên nguyên lý tâm lý học hành vi và dữ liệu chuyển đổi.
- Không chỉ trích thiết kế mà không đưa ra giải pháp thay thế cụ thể (phải nêu rõ sửa chữ gì, đổi nút gì, bỏ trường nào).
- Không khuyến nghị đập đi xây lại toàn bộ trang đích nếu chỉ cần sửa các Quick Wins (Headline, Form, Sticky CTA) là đã có thể x2 chuyển đổi.
- Không bỏ qua bước kiểm tra trên màn hình điện thoại di động (Mobile Device chiếm 80-90% traffic ads hiện nay).

## Quality Checklist
- [ ] Báo cáo đánh giá đủ 5 trụ cột: Above-the-fold, Message Match, Form Friction, Trust Signals, Mobile UX.
- [ ] Bảng khuyến nghị được phân loại theo ma trận Tác động vs Độ khó (Impact vs Effort).
- [ ] Có đề xuất cắt giảm ma sát cụ thể cho form đăng ký và tiêu đề.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/analytics/landing-page-cro.md`.
