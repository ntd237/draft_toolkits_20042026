---
name: lifecycle-design-automation-flow
description: "Thiết kế kiến trúc luồng tự động hóa tiếp thị vòng đời khách hàng (Automation Flows: Welcome Series, Abandoned Cart, Browse Abandonment, Post-Purchase Onboarding, Win-Back). Định nghĩa chính xác Trigger, bộ lọc điều kiện (Conditions/Splits), độ trễ thời gian (Delays) và mục tiêu chuyển đổi từng bước. Kích hoạt khi có yêu cầu 'thiết kế email flow', 'automation lifecycle', 'luồng bỏ giỏ hàng'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/crm/automation-flows/<flow-slug>.md."
---

# lifecycle-design-automation-flow: Thiết Kế Luồng Tự Động Hóa Vòng Đời Tiếp Thị

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "thiết kế luồng automation", "lập flow email tự động", "xây chuỗi chăm sóc khách hàng tự động", "flow bỏ giỏ hàng", "welcome series flow", hoặc sau khi đã hoàn thành phân khúc khách hàng với `crm-segment-customer-list`.

## Workflow

### Giai đoạn 1: Xác định Loại Luồng & Mục Tiêu Chuyển Đổi
**Mục tiêu**: Lựa chọn kịch bản tự động hóa phù hợp với giai đoạn trong vòng đời khách hàng.
- Lựa chọn một trong các luồng automation tiêu chuẩn:
  1. **Welcome Series (Chuỗi chào mừng)**: Dành cho lead mới đăng ký nhận tin hoặc tạo tài khoản.
  2. **Abandoned Cart Flow (Luồng cứu giỏ hàng bỏ rơi)**: Dành cho khách hàng đã thêm sản phẩm vào giỏ nhưng chưa thanh toán.
  3. **Browse Abandonment Flow (Luồng xem dở trang sản phẩm)**: Dành cho khách hàng đã xem trang sản phẩm nhưng chưa bấm thêm vào giỏ.
  4. **Post-Purchase & Onboarding Flow (Luồng sau mua & hướng dẫn)**: Dành cho khách hàng vừa hoàn tất đơn hàng đầu tiên.
  5. **Win-back / Re-engagement Flow (Luồng tái kích hoạt khách hàng cũ)**: Dành cho tệp khách hàng nguy cơ rời bỏ (At-risk) từ `crm/customer-segments.md`.
- Xác định mục tiêu chuyển đổi (Conversion Goal): Đơn hàng đầu tiên, đơn hàng mua lại (Repeat order), hoặc hoàn thành hồ sơ cá nhân.

### Giai đoạn 2: Thiết kế Kiến trúc Luồng Logic (Trigger -> Filter -> Delay -> Action)
**Mục tiêu**: Lập sơ đồ phân nhánh điều kiện chi tiết đảm bảo không gửi email trùng lặp hay gây phiền nhiễu.
- **Trigger Sự kiện (Event Trigger)**: Định nghĩa sự kiện kích hoạt chính xác (ví dụ: `Added to Cart`, `Subscribed to List`, `Placed Order`).
- **Bộ lọc Dòng chảy (Flow Filters / Exclusion Rules)**: Điều kiện loại trừ ngay lập tức (ví dụ: loại trừ người đã đặt hàng thành công kể từ khi bắt đầu luồng).
- **Phân nhánh Điều kiện (Conditional Splits)**:
  - Phân nhánh theo giá trị đơn hàng (Ví dụ: Giỏ hàng > 1.000.000đ vs Giỏ hàng < 1.000.000đ).
  - Phân nhánh theo khách hàng VIP vs Khách hàng mới.
  - Phân nhánh theo hành vi mở email / click link ở bước trước.
- **Khoảng trễ Thời gian (Time Delays)**: Cài đặt thời gian chờ tối ưu (ví dụ: Email 1 sau 1-2 giờ; Email 2 sau 24 giờ; Email 3 sau 48-72 giờ).

### Giai đoạn 3: Phác thảo Sơ đồ Luồng & Chuẩn hóa Deliverable
**Mục tiêu**: Xuất tài liệu kỹ thuật hoàn chỉnh cho đội ngũ cài đặt kỹ thuật (Klaviyo, HubSpot, Mailchimp) và lưu file theo Naming Policy trong `config.md`.
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/crm/automation-flows/<flow-slug>.md`.
- Handoff cấu trúc các bước sang `email-write-sequence-copy` để chấp bút nội dung chi tiết cho từng email trong chuỗi.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/crm/automation-flows/<flow-slug>.md`:

```markdown
# Thiết Kế Luồng Tự Động Hóa (Automation Flow) — <client_name>
- Client Slug: `<client-slug>`
- Tên luồng: <Tên luồng, ví dụ: Abandoned Cart Flow / Welcome Series>
- Mã luồng: `<flow-slug>` (ví dụ: `abandoned-cart-flow`)
- Nền tảng áp dụng: <Klaviyo / HubSpot / ActiveCampaign / Mailchimp>
- Ngày ban hành: <YYYY-MM-DD>

## 1. Tổng Quan Kiến Trúc Luồng
- **Sự kiện kích hoạt (Event Trigger)**: Người dùng thực hiện hành động `<Tên sự kiện>`
- **Bộ lọc loại trừ toàn luồng (Flow Filter)**: Đã mua hàng = 0 lần kể từ khi vào luồng.
- **Mục tiêu chuyển đổi cốt lõi**: Khách hàng hoàn tất thanh toán giỏ hàng dang dở.

## 2. Sơ Đồ Quy Trình Logic Chi Tiết (Logic Flowchart)

```
[Trigger: Thêm sản phẩm vào giỏ hàng]
       │
       ▼
[Chờ 1 giờ]
       │
       ▼
[Kiểm tra: Khách đã thanh toán chưa?] ──(Có)──> [Thoát luồng]
       │ (Chưa)
       ▼
[Bước 1: Gửi Email 1 - Nhắc nhở giỏ hàng & Hỗ trợ kỹ thuật]
       │
       ▼
[Chờ 24 giờ]
       │
       ▼
[Kiểm tra: Khách đã thanh toán chưa?] ──(Có)──> [Thoát luồng]
       │ (Chưa)
       ▼
[Bước 2: Phân nhánh điều kiện theo Giá trị giỏ hàng (AOV)]
       ├── (Giỏ hàng >= 1.000.000đ) ──> [Gửi Email 2A - Tặng mã FreeShip + Quà độc quyền]
       └── (Giỏ hàng < 1.000.000đ)  ──> [Gửi Email 2B - Đánh giá 5 sao & Bằng chứng uy tín]
       │
       ▼
[Chờ 48 giờ]
       │
       ▼
[Bước 3: Gửi Email 3 - Thông báo ưu đãi sắp hết hạn & Cảnh báo hết hàng]
       │
       ▼
[Kết thúc luồng / Gắn tag #cart_abandoned_unconverted]
```

## 3. Đặc Tả Từng Bước Gửi Thư (Step Specifications)
| Bước | Thời gian chờ (Delay) | Mục đích chính | Thông điệp cốt lõi | Trigger chuyển tiếp / Dừng |
|---|---|---|---|---|
| Email 1 | Sau 1 giờ | Nhắc nhở thân thiện | "Bạn có quên điều gì trong giỏ hàng?" | Dừng nếu đã mua |
| Email 2 | Sau 24 giờ | Xử lý rào cản mua hàng | Social proof + Ưu đãi FreeShip | Dừng nếu đã mua |
| Email 3 | Sau 48 giờ | Tạo độ gấp (Urgency) | "Mã giảm giá và giỏ hàng của bạn sắp hết hạn" | Dừng nếu đã mua |

## 4. Handoff Sản Xuất Nội Dung
- Chuyển tiếp sơ đồ này sang skill `email-write-sequence-copy` để viết nội dung chi tiết cho từng email (Subject, Preview text, Body copy, CTA button).
```

## Don'ts
- Không thiết kế luồng thiếu bộ lọc dừng (Exit Condition) dẫn đến tình trạng khách đã thanh toán xong vẫn tiếp tục nhận email nhắc mua hàng.
- Không spam dồn dập các email quá sát nhau (ví dụ gửi 3 email trong vòng 4 tiếng) gây ức chế và làm hỏng điểm uy tín người gửi.
- Không lạm dụng việc giảm giá ngay ở Email 1 khiến khách hàng hình thành thói quen cố tình bỏ giỏ hàng để đợi mã giảm giá.
- Không bỏ qua việc kiểm tra hành vi xem email trên thiết bị di động khi thiết kế cấu trúc luồng.

## Quality Checklist
- [ ] Luồng có đầy đủ Trigger, Exclusion Filters, Delays và Exit Criteria rõ ràng.
- [ ] Có sơ đồ logic trực quan mô tả sự phân nhánh điều kiện (Conditional Split).
- [ ] Bảng đặc tả từng bước nêu rõ thời gian chờ, thông điệp và mục đích hành động.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/crm/automation-flows/<flow-slug>.md`.
