---
name: email-write-sequence-copy
description: "Viết nội dung hoàn chỉnh cho chuỗi email tiếp thị tự động theo sơ đồ luồng (Subject line tối ưu tỷ lệ mở, Preview text, Thân bài cá nhân hóa 1-on-1, CTA trực diện). Đáp ứng tiêu chuẩn độ dài chuỗi email_sequence_length từ 3-7 email (Welcome 3-5 email, Nurture 4-7 email, Abandoned Cart 3 email). Kích hoạt khi có yêu cầu 'viết nội dung email flow', 'soạn chuỗi email nuôi dưỡng/chào mừng/cứu đơn'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/crm/email-sequences/<sequence-slug>.md."
---

# email-write-sequence-copy: Soạn Thảo Nội Dung Chuỗi Email Tiếp Thị Tự Động

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "viết nội dung email", "soạn chuỗi email chào mừng", "viết email bỏ giỏ hàng", "viết email nurture lead", hoặc sau khi đã có sơ đồ luồng từ `lifecycle-design-automation-flow`.

## Workflow

### Giai đoạn 1: Tiếp nhận Sơ đồ Luồng & Xác định Số lượng Email
**Mục tiêu**: Thu thập cấu trúc các bước từ `crm/automation-flows/<flow-slug>.md` và quy chuẩn độ dài theo `config.md`.
- Đọc mục tiêu từng email, thời gian trễ (Delay) và phân nhánh từ sơ đồ luồng automation.
- Xác định số lượng email cần viết theo ngưỡng `email_sequence_length` trong Validation Policy của `config.md`:
  - Chuỗi Welcome Series: 3 – 5 email.
  - Chuỗi Nurture / Giáo dục khách hàng: 4 – 7 email.
  - Chuỗi Abandoned Cart (Cứu giỏ hàng): 3 email.
  - Chuỗi Win-back (Tái kích hoạt): 3 email.
- Tiếp nhận các biến động (Dynamic Merge Tags) của hệ thống CRM (ví dụ: `{{first_name}}`, `{{cart_items}}`, `{{cart_url}}`).

### Giai đoạn 2: Chấp bút Nội dung Từng Email theo Nguyên tắc Đàm thoại (1-on-1)
**Mục tiêu**: Soạn thảo từng email mang phong cách trò chuyện chân thành, cá nhân hóa cao và thúc đẩy hành động.
- **Tiêu đề thư (Subject Line) & Đoạn xem trước (Preview Text)**:
  - Tạo 2 lựa chọn Subject Line cho mỗi email để phục vụ A/B testing (1 dòng đánh vào sự tò mò/thân mật, 1 dòng trực diện nêu rõ lợi ích).
  - Preview Text bổ trợ ý nghĩa cho Subject Line, không bị cắt cụt trên màn hình điện thoại (dưới 50 ký tự).
- **Mở đầu thư (The Hook)**:
  - Gọi tên khách hàng tự nhiên, vào thẳng vấn đề hoặc dẫn dắt bằng một tình huống quen thuộc.
- **Thân thư (The Value / Core Story)**:
  - Cung cấp giá trị hữu ích trước khi yêu cầu mua hàng.
  - Sử dụng các đoạn văn ngắn (1-3 câu mỗi đoạn), cách dòng thoáng đãng, dễ đọc lướt trên thiết bị di động.
- **Kêu gọi hành động (The Single CTA)**:
  - Mỗi email chỉ tập trung vào MỘT hành động duy nhất (bấm link xem giỏ hàng, đọc bài viết, đặt lịch tư vấn).
  - Đặt link ở cả dạng văn bản (Text link) và nút bấm nổi bật (Button).
- **Tái bút (P.S. Note)**:
  - Tận dụng dòng P.S. để nhắc lại ưu đãi chính hoặc nhấn mạnh tính cấp bách (đây là vị trí có tỷ lệ đọc cao thứ hai sau tiêu đề).

### Giai đoạn 3: Rà soát Kỹ thuật Spam Triggers & Xuất Deliverable
**Mục tiêu**: Loại bỏ các từ khóa dễ bị bộ lọc phân loại vào tab Spam/Promotions và lưu file theo Naming Policy trong `config.md`.
- Rà soát các từ ngữ nhạy cảm dễ rơi vào Spam: "MIỄN PHÍ 100%", "KIẾM TIỀN NGAY", viết hoa toàn bộ tiêu đề (ALL CAPS), lạm dụng dấu chấm than (!!!).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/crm/email-sequences/<sequence-slug>.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/crm/email-sequences/<sequence-slug>.md`:

```markdown
# Nội Dung Chuỗi Email Tiếp Thị (Email Sequence Copy) — <client_name>
- Client Slug: `<client-slug>`
- Tên chuỗi: <Tên chuỗi email>
- Mã chuỗi: `<sequence-slug>` (ví dụ: `welcome-nurture-series`)
- Số lượng email: <3 - 7 email>
- Ngày soạn: <YYYY-MM-DD>

---

## Email 1: <Tên bước trong flow, ví dụ: Chào mừng & Trao gửi quà tặng>
- **Thời điểm gửi**: Ngay sau khi đăng ký (Trigger: Subscribed)
- **Mục tiêu**: Tạo ấn tượng ban đầu và khuyến khích mở quà tặng/lead magnet.
- **Subject Line (A/B Test)**:
  - *Option A (Thân mật)*: Chào {{first_name}}, món quà đặc biệt của bạn đã sẵn sàng
  - *Option B (Trực diện)*: [Tải ngay] Bộ tài liệu hướng dẫn dành riêng cho bạn
- **Preview Text**: Mở thư để nhận đường link truy cập tài liệu độc quyền...
- **Nội dung thư**:

Chào {{first_name}},

Cảm ơn bạn đã tin tưởng và tham gia cộng đồng của chúng tôi!

Như đã hứa, đây là đường link tải toàn bộ tài liệu hướng dẫn mà bạn vừa đăng ký:
👉 **[BẤM VÀO ĐÂY ĐỂ TẢI BỘ TÀI LIỆU MIỄN PHÍ]**

Trong tài liệu này, bạn sẽ khám phá ra:
- Bí quyết 1...
- Sai lầm phổ biến mà 80% mọi người hay mắc...

Nếu bạn có bất kỳ thắc mắc nào trong quá trình áp dụng, chỉ cần nhấn **Trả lời (Reply)** trực tiếp email này. Đội ngũ chuyên gia luôn sẵn sàng hỗ trợ bạn.

Chúc bạn một ngày làm việc hiệu quả!

Thân mến,
<Tên người gửi / Founder>
<Chức danh & Tên thương hiệu>

**P.S.** Ngày mai, tôi sẽ gửi cho bạn một mẹo nhỏ nhưng cực kỳ lợi hại giúp bạn tiết kiệm 50% thời gian. Hãy nhớ kiểm tra hòm thư nhé!

---

## Email 2: <Tên bước tiếp theo>
...
```

## Don'ts
- Không nhồi nhét nhiều mục tiêu hoặc nhiều nút bấm CTA khác nhau trong cùng một email gây rối trí người đọc.
- Không viết tiêu đề giật gân lừa dối (Clickbait) không liên quan đến nội dung bên trong thư làm gia tăng tỷ lệ báo cáo thư rác (Spam Complaint).
- Không viết những bức thư dài đặc chữ không có khoảng trống dòng khiến người xem trên di động bị ngợp.
- Không quên để biến cá nhân hóa (Merge tags) hoặc quên kiểm tra giá trị dự phòng mặc định (Fallback text, ví dụ: `{{first_name|default:"bạn"}}`).

## Quality Checklist
- [ ] Số lượng email nằm trong khoảng 3 đến 7 email theo đúng Validation Policy trong `config.md`.
- [ ] Mỗi email có đủ 2 phương án Subject Line (A/B testing), Preview Text, Body text, và CTA rõ ràng.
- [ ] Đã kiểm tra và loại bỏ các bẫy kích hoạt bộ lọc thư rác (Spam triggers).
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/crm/email-sequences/<sequence-slug>.md`.
