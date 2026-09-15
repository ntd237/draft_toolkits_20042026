---
name: cro-design-ab-test
description: "Thiết kế kế hoạch thử nghiệm A/B Testing chuẩn phương pháp khoa học cho Landing Page/Website. Xây dựng giả thuyết thử nghiệm (Hypothesis), thiết lập biến thể thử nghiệm (Control vs Variant), tính toán kích thước mẫu tối thiểu (cro_minimum_sample_size >= 300 conversions/variant) và thời gian chạy đảm bảo độ tin cậy thống kê (cro_ab_test_confidence >= 95%). Kích hoạt khi có yêu cầu 'thiết kế A/B test', 'lên kế hoạch test landing page', 'thử nghiệm chuyển đổi'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/analytics/ab-test-plan.md."
---

# cro-design-ab-test: Thiết Kế Kế Hoạch Thử Nghiệm A/B Test Khoa Học

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "thiết kế A/B test", "lên kế hoạch test landing page", "thử nghiệm 2 phiên bản trang đích", "xác định cỡ mẫu A/B testing", hoặc sau khi đã xác định được các giả thuyết cải tiến từ `cro-audit-landing-page`.

## Workflow

### Giai đoạn 1: Xây Dựng Giả Thuyết Thử Nghiệm (Scientific Hypothesis)
**Mục tiêu**: Định hình giả thuyết rõ ràng theo cấu trúc logic chuẩn mực.
- Đọc các khuyến nghị ưu tiên từ `analytics/landing-page-cro.md`.
- Xây dựng giả thuyết theo công thức bắt buộc:
  *"NẾU chúng ta [thay đổi cụ thể một yếu tố X] TRÊN [trang/vị trí cụ thể], THÌ [chỉ số chuyển đổi Y] sẽ [tăng Z%], BỞI VÌ [lý do tâm lý/hành vi của người dùng]."*
- Đảm bảo chỉ kiểm tra MỘT biến số duy nhất trong mỗi thử nghiệm A/B test (Single-variable test: chỉ đổi Headline HOẶC Form HOẶC Nút bấm; không đổi hỗn hợp nhiều thứ cùng lúc trừ khi làm Multivariate test).

### Giai đoạn 2: Thiết Kế Biến Thể & Định Nghĩa Chỉ Số Thành Công
**Mục tiêu**: Xác định chi tiết bản gốc (Control - Phiên bản A) và bản thử nghiệm (Variant - Phiên bản B).
- **Bản gốc (Control - A)**: Giữ nguyên hiện trạng trang đích đang chạy.
- **Bản thử nghiệm (Variant - B)**: Áp dụng thay đổi đã nêu trong giả thuyết.
- **Xác định chỉ số đo lường chính (Primary Metric)**:
  - Tỷ lệ gửi form thành công (Form Submission Conversion Rate) hoặc Lượt hoàn tất mua hàng (Purchase Rate).
- **Xác định chỉ số phụ / Chỉ số bảo vệ (Guardrail Metrics)**:
  - Tỷ lệ thoát trang (Bounce Rate), Thời gian trung bình trên trang, Tỷ lệ lead rác (Lead quality rate) — để đảm bảo tỷ lệ chuyển đổi tăng không làm suy giảm chất lượng khách hàng.

### Giai đoạn 3: Tính Toán Kích Thước Mẫu & Thời Lượng Thử Nghiệm theo `config.md`
**Mục tiêu**: Áp dụng các quy tắc thống kê nghiêm ngặt theo Validation Policy trong `config.md`.
- Đối chiếu các ngưỡng thống kê bắt buộc:
  - `cro_ab_test_confidence`: Ngưỡng độ tin cậy thống kê tối thiểu >= 95% ($p < 0.05$).
  - `cro_minimum_sample_size`: Tối thiểu >= 300 conversions / variant trước khi đưa ra kết luận.
  - Sức mạnh kiểm định (Statistical Power): Đạt chuẩn 80% ($\beta = 0.2$).
- Tính toán thời gian chạy thử nghiệm tối thiểu: Phải chạy đủ tối thiểu 2 chu kỳ tuần hoàn chỉnh (14 ngày) để triệt tiêu hiệu ứng chênh lệch giữa ngày trong tuần và cuối tuần (Day-of-week effect).
- Xuất tài liệu kế hoạch thử nghiệm và lưu tại `docs/marketing-projects/<client-slug>/analytics/ab-test-plan.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/analytics/ab-test-plan.md`:

```markdown
# Kế Hoạch Thử Nghiệm A/B Test (Experiment Plan) — <client_name>
- Client Slug: `<client-slug>`
- Mã thử nghiệm: `<test-id>` (ví dụ: `EXP_LP_01_Headline_Form`)
- Trang thử nghiệm: <URL trang đích>
- Công cụ điều phối thử nghiệm: <Google Optimize / VWO / AB Tasty / Meta Split Test>
- Ngày thiết lập: <YYYY-MM-DD>

## 1. Giả Thuyết Thử Nghiệm (The Hypothesis)
- **Giả thuyết cốt lõi**:
  > "NẾU chúng ta **rút ngắn form đăng ký từ 8 trường xuống còn 2 trường (Tên + SĐT)** và **thêm thanh CTA dính đáy màn hình (Sticky Bottom CTA)** trên trang đích di động, THÌ **tỷ lệ gửi form thành công sẽ tăng ít nhất 35%**, BỞI VÌ **người dùng di động không còn cảm thấy bị quá tải thông tin và có thể bấm đăng ký ngay ở bất kỳ vị trí cuộn nào**."

## 2. Đặc Tả Hai Phiên Bản Thử Nghiệm (Control vs Variant)
| Yếu tố | Phiên bản A (Control - Hiện tại) | Phiên bản B (Variant - Thử nghiệm) |
|---|---|---|
| **Tiêu đề Form** | "Đăng ký tư vấn chi tiết" | "Nhận tư vấn miễn phí trong 5 phút" |
| **Số trường form** | 8 trường (Họ tên, Email, SĐT, Địa chỉ, Tỉnh thành, Tuổi, Sản phẩm quan tâm, Ghi chú) | 2 trường (Họ và tên, Số điện thoại) |
| **Nút bấm CTA** | "Gửi thông tin" (Màu xám) | "Gửi cho tôi ngay" (Màu cam nổi bật) |
| **Thanh điều hướng** | Không có | Bổ sung thanh Sticky Bar dính đáy màn hình điện thoại |

## 3. Khung Đo Lường & Tiêu Chuẩn Thống Kê (Statistical Rigor)
- **Chỉ số đo lường chính (Primary KPI)**: Tỷ lệ chuyển đổi Form (Submissions / Total Visitors).
- **Chỉ số bảo vệ (Guardrail Metric)**: Tỷ lệ số điện thoại sai/rác (Không được tăng quá 5%).
- **Ngưỡng tin cậy thống kê bắt buộc**: >= 95% (Confidence Level $p < 0.05$).
- **Số chuyển đổi tối thiểu mỗi biến thể**: >= 300 chuyển đổi / biến thể (Tổng cộng >= 600 chuyển đổi).
- **Lưu lượng truy cập dự kiến**: 500 khách / ngày.
- **Thời lượng chạy dự kiến**: Tối thiểu 14 ngày liên tục (Bắt buộc chạy đủ 2 chu kỳ tuần).

## 4. Quy Trình Ra Quyết Định Khi Kết Thúc Thử Nghiệm (Decision Matrix)
- **Kịch bản 1 (Variant B thắng với độ tin cậy >= 95% & Lead rác ổn định)**: Triển khai 100% biến thể B cho toàn bộ lưu lượng; cập nhật lại trang chính thức.
- **Kịch bản 2 (Không có sự khác biệt có ý nghĩa thống kê - Inconclusive)**: Dừng test, giữ nguyên bản A, đúc rút bài học và lập giả thuyết mới.
- **Kịch bản 3 (Variant B thua hoặc Lead rác tăng vọt)**: Tắt biến thể B ngay lập tức, phân tích nguyên nhân tại sao giảm chất lượng.
```

## Don'ts
- Không tuyên bố biến thể chiến thắng chỉ sau 2-3 ngày đầu khi mẫu thử còn quá nhỏ và kết quả chưa đạt độ tin cậy thống kê 95% (Bẫy Peeking Problem).
- Không thay đổi cùng lúc quá nhiều yếu tố khác nhau mà không thể giải thích được yếu tố nào thực sự tạo ra sự tăng trưởng.
- Không dừng thử nghiệm giữa chừng vào ngày trong tuần mà không chạy trọn vẹn chu kỳ tuần (14 ngày).
- Không bỏ qua chỉ số bảo vệ (Guardrail Metrics); một biến thể tăng x2 số lượng lead nhưng toàn bộ là lead rác hoặc số ảo thì vẫn là một thất bại kinh doanh.

## Quality Checklist
- [ ] Giả thuyết được phát biểu đúng cấu trúc chuẩn (Nếu... Thì... Bởi vì...).
- [ ] Xác định rõ biến thể A (Control) và biến thể B (Variant) với các điểm thay đổi cụ thể.
- [ ] Tuân thủ các ngưỡng thống kê trong `config.md` (Confidence >= 95%, tối thiểu 300 conversions/variant, chạy tối thiểu 14 ngày).
- [ ] Có chỉ số bảo vệ (Guardrail Metrics) và ma trận ra quyết định khi kết thúc thử nghiệm.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/analytics/ab-test-plan.md`.
