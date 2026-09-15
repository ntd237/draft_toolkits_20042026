---
name: ads-diagnose-underperformance
description: "Chẩn đoán nguyên nhân gốc rễ (RCA) khiến chiến dịch quảng cáo kém hiệu quả (CPA tăng vọt, CTR suy giảm, ROAS sụt giảm, tần suất frequency quá cao gây Ad Fatigue, hoặc tỷ lệ chuyển đổi Landing Page thấp). Đối chiếu ngưỡng cảnh báo tại config.md và đưa ra lộ trình tối ưu khẩn cấp. Kích hoạt khi có yêu cầu 'chẩn đoán ads', 'campaign chạy kém', 'tại sao CPA tăng cao'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/seo-ads/ads-diagnosis.md."
---

# ads-diagnose-underperformance: Chẩn Đoán Nguyên Nhân Quảng Cáo Kém Hiệu Quả

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng cung cấp số liệu quảng cáo và yêu cầu "chẩn đoán ads", "tại sao chiến dịch chạy kém", "CPA tuần này tăng gấp đôi", "quảng cáo bị bão hòa (ad fatigue)", hoặc khi số liệu vi phạm các ngưỡng cảnh báo quy định tại Validation Policy trong `config.md`.

## Workflow

### Giai đoạn 1: Tiếp nhận Số liệu Thực tế & Đối chiếu Ngưỡng Cảnh báo
**Mục tiêu**: Thu thập các chỉ số đo lường hiệu suất và so sánh với chỉ số cơ sở (Benchmark).
- Thu thập bộ chỉ số từ báo cáo của Ads Manager: Chi tiêu (Spend), Lượt hiển thị (Impressions), Tần suất (Frequency), Lượt click (Clicks), CTR, CPC, Tỷ lệ click vào link (Outbound CTR), Tỷ lệ chuyển đổi trang (LP Conversion Rate), Chi phí trên mỗi chuyển đổi (CPA), và ROAS.
- Đối chiếu với các ngưỡng cảnh báo bất thường trong `config.md`:
  - `ads_diagnosis_cpa_spike`: CPA tăng >= +20% so với benchmark 14 ngày trước.
  - `ads_diagnosis_ctr_drop`: CTR giảm >= -30% so với benchmark 14 ngày trước.
  - Tần suất (Frequency) hiển thị: > 3.5 lần trên tệp đối tượng lạnh (Cold).

### Giai đoạn 2: Cây Chẩn đoán Nguyên nhân Gốc rễ (Root Cause Analysis Tree)
**Mục tiêu**: Cô lập chính xác điểm nghẽn nằm ở đâu trong phễu: Creative, Targeting, Đấu thầu (Bidding), hay Landing Page / Sản phẩm.
- **Nhánh 1: CTR thấp & CPC cao**:
  - Nguyên nhân: Hook creative không đủ thu hút, hình ảnh nhàm chán, hoặc tệp đối tượng nhắm mục tiêu (Targeting) bị lệch so với thông điệp.
  - Giải pháp: Đổi hook 3 giây đầu, thay hình ảnh mới hoặc mở rộng tệp sang Broad targeting.
- **Nhánh 2: CTR cao, CPC rẻ nhưng CPA rất cao hoặc không có chuyển đổi**:
  - Nguyên nhân: Lỗi không nằm ở quảng cáo mà nằm ở **Landing Page** (Tốc độ tải chậm, nội dung LP không khớp với hứa hẹn trên ads - Message Mismatch, form đăng ký quá dài hoặc giá sản phẩm không cạnh tranh).
  - Giải pháp: Chuyển giao sang `cro-audit-landing-page` để tối ưu trang đích.
- **Nhánh 3: Tần suất (Frequency) cao, CPA tăng dần theo thời gian (Ad Fatigue)**:
  - Nguyên nhân: Tệp đối tượng quá nhỏ hoặc quảng cáo đã chạy quá lâu khiến người dùng bị "bội thực" quảng cáo (Creative Burnout).
  - Giải pháp: Thay bộ creative mới (Creative Refresh) hoặc mở rộng tệp Lookalike lớn hơn.
- **Nhánh 4: Bị kẹt trong giai đoạn máy học (Learning Limited)**:
  - Nguyên nhân: Ngân sách quá mỏng không đạt được tối thiểu 50 chuyển đổi/tuần/adset để thuật toán tối ưu.
  - Giải pháp: Gom nhóm các Ad Set nhỏ lại hoặc đổi sự kiện tối ưu sang bước nông hơn trong phễu (ví dụ: tối ưu Thêm vào giỏ hàng thay vì Mua hàng).

### Giai đoạn 3: Lập Báo cáo Chẩn đoán & Kế hoạch Khắc phục Ưu tiên
**Mục tiêu**: Xếp hạng các hành động sửa chữa cần thực hiện ngay lập tức và lưu file theo Naming Policy trong `config.md`.
- Đưa ra danh sách hành động theo quy tắc: Hành động khẩn cấp (Làm trong 24h) -> Hành động trung hạn (Làm trong tuần).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/seo-ads/ads-diagnosis.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/seo-ads/ads-diagnosis.md`:

```markdown
# Báo Cáo Chẩn Đoán Hiệu Quả Quảng Cáo (Ads RCA Report) — <client_name>
- Client Slug: `<client-slug>`
- Chiến dịch được chẩn đoán: <Tên Campaign / Ad Set>
- Khoảng thời gian phân tích: <Từ ngày ... đến ngày ...>
- Ngày lập báo cáo: <YYYY-MM-DD>

## 1. Bảng So Sánh Chỉ Số Thực Tế & Ngưỡng Benchmark
| Chỉ số | Benchmark (14 ngày trước) | Hiện tại | Biến động (%) | Đánh giá trạng thái |
|---|---|---|---|---|
| Chi phí / Chuyển đổi (CPA) | 120.000 đ | 185.000 đ | +54.2% | 🔴 Báo động (Vượt ngưỡng +20%) |
| Tỷ lệ click (CTR) | 2.1% | 1.1% | -47.6% | 🔴 Báo động (Tụt sâu quá -30%) |
| Tần suất hiển thị (Frequency) | 1.4 | 4.1 | +192% | 🟡 Cảnh báo (Bão hòa đối tượng) |
| Chi phí mỗi click (CPC) | 3.500 đ | 6.800 đ | +94.3% | 🟡 Cảnh báo chi phí cạnh tranh cao |
| Tỷ lệ chuyển đổi trang (CR) | 3.5% | 3.2% | -8.5% | 🟢 Bình thường (Landing Page ổn định) |

## 2. Kết Luận Nguyên Nhân Gốc Rễ (Root Causes)
1. **Nguyên nhân chính (Primary Driver)**: Quảng cáo rơi vào trạng thái bão hòa nặng (Ad Fatigue) — Tần suất 4.1 khiến tệp đối tượng nhìn thấy quảng cáo quá nhiều lần mà không có biến thể mới, dẫn tới CTR sụt giảm 47% và kéo CPA tăng vọt.
2. **Nguyên nhân thứ cấp**: Ad Set bị phân mảnh ngân sách, không đủ 50 chuyển đổi/tuần để máy học thoát Learning Limited.

## 3. Lộ Trình Hành Động Khắc Phục (Action Plan)

### Khẩn cấp (Thực hiện trong 24 Giờ tới):
- [ ] Tắt tạm thời 2 mẫu quảng cáo có Frequency > 4.5 và CPA vượt trần cho phép.
- [ ] Đẩy ngay 2 creative mới từ `ads-generate-creative-brief` với góc tiếp cận hook hoàn toàn mới.
- [ ] Mở rộng tệp đối tượng từ 1% Lookalike lên 3% Lookalike để hạ nhiệt tần suất hiển thị.

### Kế hoạch Tuần (Trung hạn):
- [ ] Gom 3 Ad Set nhỏ thành 1 Ad Set lớn với ngân sách tập trung để thoát khỏi Learning Limited.
- [ ] Phối hợp với nhóm Content để bổ sung biến thể copy PAS và FAB từ `content-write-short-copy`.
```

## Don'ts
- Không vội vàng kết luận do lỗi thuật toán hoặc vội vàng tăng/giảm ngân sách đột ngột khi chưa phân tích chuỗi chỉ số từ Impression -> Click -> Conversion.
- Không chỉnh sửa ngân sách quá 20% mỗi lần trên các Ad Set đang chạy ổn định (tránh làm reset máy học).
- Không đổ lỗi cho quảng cáo nếu CTR rất cao nhưng người dùng thoát trang ngay lập tức (đây là vấn đề của Landing Page hoặc Offer).
- Không tắt hết toàn bộ chiến dịch khi chỉ có 1 vài creative bị bão hòa.

## Quality Checklist
- [ ] Có bảng so sánh số liệu hiện tại với benchmark và tỷ lệ % biến động.
- [ ] Xác định chính xác nguyên nhân gốc rễ (Creative, Targeting, Bidding, hay Landing page).
- [ ] Có danh mục hành động phân loại theo mức độ khẩn cấp (trong 24h và trong tuần).
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/seo-ads/ads-diagnosis.md`.
