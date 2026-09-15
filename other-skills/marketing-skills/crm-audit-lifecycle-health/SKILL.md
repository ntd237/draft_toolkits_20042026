---
name: crm-audit-lifecycle-health
description: "Đánh giá sức khỏe tổng thể hệ thống CRM và hiệu suất vòng đời khách hàng (Tỷ lệ mở thư Open Rate, Click Rate, Bounce Rate, Unsubscribe Rate, Churn Rate, LTV Trend). So sánh số liệu với benchmark ngành hàng, chẩn đoán nguyên nhân suy giảm tương tác và đưa ra khuyến nghị cải thiện kỹ thuật khả năng gửi thư (Deliverability). Kích hoạt khi có yêu cầu 'đánh giá hiệu quả CRM', 'email marketing kém hiệu quả', 'audit email metrics'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/crm/lifecycle-health-report.md."
---

# crm-audit-lifecycle-health: Đánh Giá Sức Khỏe Vòng Đời Khách Hàng & Hệ Thống CRM

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "đánh giá hiệu quả CRM", "audit hệ thống email", "open rate giảm sút", "tỷ lệ hủy đăng ký tăng cao", "kiểm tra sức khỏe danh sách khách hàng", hoặc cần chẩn đoán nguyên nhân email rơi vào hòm thư rác.

## Workflow

### Giai đoạn 1: Tiếp nhận Báo cáo Số liệu CRM & Cấu hình Kỹ thuật Tên miền
**Mục tiêu**: Thu thập các chỉ số vận hành email trong 30 – 90 ngày qua từ nền tảng CRM của client.
- Tiếp nhận các chỉ số hiệu suất:
  - Tỷ lệ gửi thư thành công (Deliverability / Delivery Rate).
  - Tỷ lệ mở thư (Open Rate) và Tỷ lệ nhấp trên mở (Click-to-Open Rate - CTOR).
  - Tỷ lệ thoát email (Bounce Rate: Hard bounce & Soft bounce).
  - Tỷ lệ hủy đăng ký (Unsubscribe Rate) và Báo cáo spam (Spam Complaint Rate).
  - Tỷ lệ khách hàng mua lại (Repeat Purchase Rate) và tỷ lệ rời bỏ (Churn Rate).
- Kiểm tra các bản ghi xác thực tên miền bắt buộc: SPF, DKIM, DMARC và Google Postmaster Tools.

### Giai đoạn 2: Đối chiếu Benchmark Ngành & Chẩn đoán Điểm Nghẽn
**Mục tiêu**: So sánh số liệu thực tế với ngưỡng chuẩn của ngành theo `config.md` để khoanh vùng bất thường.
- Đối chiếu với Benchmark tiêu chuẩn:
  - Open Rate: Benchmark 20% – 25% (Nếu < 15% là mức báo động).
  - Click Rate (CTR): Benchmark 2% – 3% (Nếu < 1% là nội dung kém hấp dẫn).
  - Bounce Rate: Phải < 2% (Nếu > 2% có nguy cơ bị nhà mạng khóa tài khoản).
  - Spam Complaint Rate: Phải < 0.1% (Ngưỡng khắt khe mới của Google & Yahoo).
  - Unsubscribe Rate: Chuẩn < 0.5% mỗi chiến dịch.
- Chẩn đoán nguyên nhân gốc:
  - Lỗi suy giảm Open Rate: Tên miền bị đánh dấu blacklist, thiếu bản ghi DMARC, dòng tiêu đề nhàm chán, hoặc tệp subscriber quá cũ không được làm sạch.
  - Lỗi suy giảm Click Rate: Lời kêu gọi hành động (CTA) mờ nhạt, nội dung không đúng kỳ vọng của tiêu đề, hoặc giao diện email vỡ khung trên thiết bị di động.

### Giai đoạn 3: Lập Báo cáo Chẩn đoán & Lộ trình Khắc phục (Recovery Plan)
**Mục tiêu**: Đưa ra hướng xử lý kỹ thuật và chiến lược tái kích hoạt, lưu file theo Naming Policy trong `config.md`.
- Xây dựng kế hoạch làm sạch danh sách (List Cleaning / Scrubbing) và kế hoạch hâm nóng lại tên miền (Domain Warm-up nếu cần).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/crm/lifecycle-health-report.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/crm/lifecycle-health-report.md`:

```markdown
# Báo Cáo Sức Khỏe Hệ Thống CRM & Vòng Đời Khách Hàng — <client_name>
- Client Slug: `<client-slug>`
- Nền tảng CRM: <Klaviyo / HubSpot / Mailchimp>
- Giai đoạn phân tích: <30 / 60 / 90 ngày qua>
- Ngày thẩm định: <YYYY-MM-DD>

## 1. Bảng So Sánh Chỉ Số Thực Tế & Benchmark Ngành
| Chỉ số Vận hành CRM | Số liệu thực tế | Benchmark ngành | Độ lệch (%) | Trạng thái đánh giá |
|---|---|---|---|---|
| **Tỷ lệ mở thư (Open Rate)** | 14.2% | 22.0% | -35.4% | 🔴 Kém (Cần khắc phục khẩn cấp) |
| **Tỷ lệ Click / Mở (CTOR)** | 8.5% | 12.0% | -29.1% | 🟡 Cảnh báo (Nội dung chưa đủ hút) |
| **Tỷ lệ thư hỏng (Bounce Rate)** | 3.8% | < 2.0% | +90.0% | 🔴 Nguy hiểm (Rủi ro khóa IP gửi) |
| **Báo cáo Spam (Spam Rate)** | 0.15% | < 0.10% | +50.0% | 🔴 Vượt trần cho phép của Google |
| **Tỷ lệ Hủy đăng ký (Unsub)** | 0.8% | < 0.5% | +60.0% | 🟡 Tần suất gửi đang quá dày |
| **Khách mua lại (Repeat Rate)**| 18.0% | 25.0% | -28.0% | 🟡 Tiềm năng khai thác thêm |

## 2. Kết Luận Chẩn Đoán Nguyên Nhân Gốc Rễ
1. **Suy giảm khả năng gửi thư (Deliverability Drop)**: Hệ thống chưa cấu hình bản ghi DMARC nghiêm ngặt và Bounce rate ở mức 3.8% do danh sách khách hàng tích tụ lâu năm chưa từng qua bộ lọc làm sạch.
2. **Hiện tượng mệt mỏi vì bị spam (Subscriber Fatigue)**: Tần suất gửi thư tăng gấp đôi nhưng không phân khúc đối tượng, dẫn đến tỷ lệ Unsubscribe và Spam complaint tăng vọt.

## 3. Kế Hoạch Phục Hồi Hiệu Suất CRM (Actionable Roadmap)

### Bước 1: Vệ sinh Kỹ thuật Tên miền (Tuần 1)
- [ ] Cấu hình đầy đủ bản ghi SPF, DKIM và chính sách DMARC (`p=quarantine` hoặc `p=reject`).
- [ ] Chạy công cụ lọc sạch danh sách: Xóa vĩnh viễn các email Hard Bounce và email không tương tác > 180 ngày.

### Bước 2: Tối ưu Nội dung & Phân đoạn (Tuần 2-3)
- [ ] Tạm dừng gửi email toàn tệp (All-subscribers blast). Chỉ gửi thư cho tệp Engaged 30/60 ngày.
- [ ] Ứng dụng phân khúc từ `crm-segment-customer-list` để gửi thông điệp cá nhân hóa theo từng nhóm.
```

## Don'ts
- Không gửi email ồ ạt tới toàn bộ danh sách khi tỷ lệ Spam Complaint đang vượt ngưỡng 0.1% (nguy cơ tên miền bị vào Blacklist vĩnh viễn).
- Không giữ lại các địa chỉ email đã Hard Bounce vì tiếc số lượng danh bạ.
- Không đưa ra kết luận về chất lượng nội dung email nếu chưa kiểm tra xem email có thực sự vào được Inbox của người dùng hay bị rớt vào hòm thư Spam/Junk.
- Không đánh giá hiệu quả CRM chỉ dựa trên doanh số ngắn hạn mà bỏ qua các chỉ số bền vững về độ tương tác (Engagement).

## Quality Checklist
- [ ] Báo cáo có bảng đối chiếu đầy đủ các chỉ số: Open Rate, CTOR, Bounce Rate, Spam Rate, Unsubscribe Rate.
- [ ] So sánh trực quan với benchmark ngành và phân loại trạng thái rủi ro.
- [ ] Kiểm tra các yếu tố kỹ thuật tên miền (SPF, DKIM, DMARC).
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/crm/lifecycle-health-report.md`.
