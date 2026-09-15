---
name: crm-segment-customer-list
description: "Phân khúc danh sách khách hàng (Customer Segmentation) theo hành vi, giá trị vòng đời và mô hình RFM (Recency, Frequency, Monetary). Phân loại tối thiểu 4 phân khúc (VIP, Khách hàng trung thành, Khách tiềm năng, Nguy cơ rời bỏ) theo crm_rfm_segments_min và đề xuất hành động tiếp thị cá nhân hóa. Kích hoạt khi có yêu cầu 'phân khúc khách hàng', 'chia tệp CRM', 'phân tích RFM'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/crm/customer-segments.md."
---

# crm-segment-customer-list: Phân Khúc Khách Hàng Chuyên Sâu & Mô Hình RFM

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "phân khúc khách hàng", "chia tệp dữ liệu CRM", "phân tích RFM", "phân loại tệp email theo hành vi", hoặc trước khi xây dựng các luồng automation và chiến dịch email marketing cá nhân hóa.

## Workflow

### Giai đoạn 1: Tiếp nhận Dữ liệu Giao dịch & Tương tác Khách hàng
**Mục tiêu**: Thu thập các biến số đo lường hành vi khách hàng từ hệ thống CRM/E-commerce của client.
- Tiếp nhận các trường dữ liệu: Thời điểm mua hàng gần nhất (Recency), Tần suất mua hàng trong kỳ (Frequency), Tổng giá trị chi tiêu (Monetary), Hành vi mở email / click link, Trạng thái tài khoản.
- Đảm bảo thiết lập tối thiểu 4 phân khúc theo quy định `crm_rfm_segments_min` trong Validation Policy của `config.md`:
  1. Phân khúc Khách hàng VIP / Tinh hoa (Champions / High-Value).
  2. Phân khúc Khách hàng Thường xuyên / Trung thành (Loyal Customers).
  3. Phân khúc Khách hàng Mới / Đầy tiềm năng (New & Promising).
  4. Phân khúc Khách hàng Nguy cơ rời bỏ / Ngủ đông (At-Risk / Hibernating / Churned).

### Giai đoạn 2: Thiết lập Bộ Quy tắc Phân loại (Segmentation Rules & Logic)
**Mục tiêu**: Định lượng tiêu chí phân nhóm rõ ràng để đội ngũ vận hành CRM cài đặt bộ lọc tự động.
- **Phân khúc 1: VIP / Champions**:
  - Tiêu chí: Recency <= 30 ngày, Frequency >= 3 lần, Monetary nằm trong top 10% chi tiêu cao nhất.
  - Mục tiêu tiếp thị: Tri ân đặc quyền, mời trải nghiệm sản phẩm mới trước công chúng, chăm sóc 1-1, không giảm giá đại trà.
- **Phân khúc 2: Khách hàng Trung thành (Loyal Customers)**:
  - Tiêu chí: Recency <= 60 ngày, Frequency >= 2 lần, tương tác đều đặn.
  - Mục tiêu tiếp thị: Upsell / Cross-sell các sản phẩm bổ trợ, tích điểm đổi quà, chương trình giới thiệu bạn bè (Referral).
- **Phân khúc 3: Khách hàng Mới (New Customers / Promising)**:
  - Tiêu chí: Mua lần đầu trong vòng 30 ngày qua hoặc đăng ký nhận tin chưa mua.
  - Mục tiêu tiếp thị: Chuỗi Onboarding hướng dẫn sử dụng, kích hoạt lần mua thứ hai bằng ưu đãi chào mừng.
- **Phân khúc 4: Khách hàng Nguy cơ rời bỏ (At-Risk / Inactive)**:
  - Tiêu chí: Recency từ 90 – 180 ngày không quay lại dù trước đó từng mua hàng.
  - Mục tiêu tiếp thị: Chuỗi Win-back / Tái kích hoạt kèm khảo sát lý do ngừng mua hoặc ưu đãi độc quyền.

### Giai đoạn 3: Tổng hợp Bản đồ Phân khúc & Xuất Deliverable
**Mục tiêu**: Mô tả đặc trưng từng nhóm và lưu file theo Naming Policy trong `config.md`.
- Ghi toàn bộ dữ liệu vào `docs/marketing-projects/<client-slug>/crm/customer-segments.md`.
- Handoff sang `lifecycle-design-automation-flow` để thiết kế kịch bản tự động tương ứng cho từng nhóm.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/crm/customer-segments.md`:

```markdown
# Bản Đồ Phân Khúc Khách Hàng (Customer Segmentation) — <client_name>
- Client Slug: `<client-slug>`
- Quy mô cơ sở dữ liệu phân tích: <Số lượng contacts / khách hàng>
- Ngày cập nhật: <YYYY-MM-DD>

## 1. Ma Trận Phân Khúc RFM Tổng Thể
| Phân khúc | Tỷ lệ tệp (%) | Đóng góp doanh thu (%) | Tiêu chuẩn lọc (Filter Rules) | Mục tiêu chiến lược cốt lõi |
|---|---|---|---|---|
| **1. VIP / Champions** | ~5% | ~35% | Mua gần đây, F >= 3 lần, Chi tiêu top 10% | Giữ chân tối đa & Chăm sóc đặc quyền |
| **2. Khách Trung Thành** | ~15% | ~30% | Mua trong 60 ngày, F >= 2 lần | Gia tăng giá trị đơn (AOV) & Cross-sell |
| **3. Khách Mới / Tiềm Năng** | ~40% | ~20% | Mua lần đầu < 30 ngày hoặc Lead mới | Kích hoạt mua lần 2 (Repeat purchase) |
| **4. Nguy Cơ Rời Bỏ (At-Risk)** | ~40% | ~15% | Không mua > 90 ngày | Chiến dịch Win-back & Khảo sát lý do |

## 2. Hướng Dẫn Kích Hoạt Từng Phân Khúc

### Phân khúc 1: VIP / Champions
- **Kênh tiếp cận tối ưu**: Email cá nhân từ người sáng lập, Zalo ZNS ưu tiên, Call trực tiếp từ CSKH riêng.
- **Thông điệp truyền thông**: "Tri ân đối tác đồng hành - Trải nghiệm trước bộ sưu tập mới".
- **Hành động kỹ thuật trên CRM**: Gắn thẻ tag `#segment_vip`, loại trừ khỏi các email giảm giá xả kho.

### Phân khúc 2: Khách Trung Thành
- **Kênh tiếp cận**: Email marketing tự động, SMS Brandname thông báo điểm thưởng.
- **Chiến dịch đề xuất**: Đổi điểm tích lũy lấy quà tặng giới hạn; mua combo kèm giá ưu đãi.

### Phân khúc 3: Khách Mới / Tiềm Năng
- **Luồng kích hoạt**: Đưa ngay vào chuỗi Welcome & Nurture Series thiết kế bởi `lifecycle-design-automation-flow`.

### Phân khúc 4: Nguy Cơ Rời Bỏ
- **Chiến dịch đề xuất**: Chuỗi Win-back 3 bước với voucher "Chúng tôi nhớ bạn" có thời hạn 48 giờ.

## 3. Đề Xuất Quy Trình Đồng Bộ & Vệ Sinh Dữ Liệu (List Hygiene)
- Tự động chuyển trạng thái phân khúc theo chu kỳ 14 ngày.
- Thanh lọc (Purge/Unsubscribe) các địa chỉ email không mở thư trong suốt 180 ngày để bảo vệ điểm uy tín tên miền (Domain Reputation).
```

## Don'ts
- Không gửi cùng một thông điệp hoặc cùng một mã giảm giá cho toàn bộ danh sách (Email Blast / Batch & Blast) gây hủy đăng ký hàng loạt.
- Không đặt tiêu chí phân khúc mơ hồ không thể cấu hình được bằng các trường điều kiện trên phần mềm CRM (HubSpot, Klaviyo, ActiveCampaign, v.v.).
- Không bỏ qua việc bảo vệ tệp khách hàng VIP khỏi các chương trình khuyến mãi đại trà làm xói mòn giá trị thương hiệu.
- Không để tệp khách hàng ngủ đông tích tụ quá 6 tháng mà không có chiến dịch thanh lọc.

## Quality Checklist
- [ ] Xác định tối thiểu 4 phân khúc khách hàng theo đúng Validation Policy trong `config.md`.
- [ ] Mỗi phân khúc đều có tiêu chí lọc định lượng cụ thể (Recency, Frequency, Monetary hoặc hành vi tương tác).
- [ ] Có chiến lược tiếp cận và thông điệp truyền thông riêng biệt cho từng nhóm.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/crm/customer-segments.md`.
