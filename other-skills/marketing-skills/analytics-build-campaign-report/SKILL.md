---
name: analytics-build-campaign-report
description: "Tổng hợp báo cáo hiệu quả chiến dịch marketing đa kênh (Cross-Channel Performance Report: Meta Ads, Google Ads, TikTok, SEO, Email) chuẩn hóa theo mục tiêu KPI của client (Chi phí, Doanh thu, Blended ROAS, CPA, LTV). Bóc tách insight cốt lõi và đề xuất tái phân bổ ngân sách cho chu kỳ tiếp theo. Kích hoạt khi có yêu cầu 'báo cáo campaign', 'tổng kết chiến dịch marketing', 'report tháng/quý cho client'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/analytics/campaign-report.md."
---

# analytics-build-campaign-report: Tổng Hợp Báo Cáo Chiến Dịch Tiếp Thị Đa Kênh

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng cung cấp số liệu đa kênh và yêu cầu "lập báo cáo campaign", "report marketing tháng/quý", "tổng kết hiệu quả chiến dịch", "báo cáo gửi client", hoặc vào Tuần 6 (Measure & Optimize) trong quy trình vận hành chiến dịch chuẩn.

## Workflow

### Giai đoạn 1: Hợp nhất Dữ liệu Đa kênh & Đối chiếu Mục tiêu (KPI)
**Mục tiêu**: Thu thập số liệu thô từ các nền tảng quảng cáo, website analytics (GA4) và hệ thống CRM/Bán hàng.
- Thu thập dữ liệu từ các nguồn:
  - Nền tảng trả phí (Paid Ads): Chi tiêu (Spend), Lượt click, Lượt hiển thị, CPC, CTR từ Meta Ads, Google Ads, TikTok Ads.
  - Công cụ đo lường trang web (GA4): Phiên truy cập (Sessions), Tỷ lệ tương tác (Engagement Rate), Lượt chuyển đổi (Key Events / Conversions).
  - Hệ thống bán hàng/CRM: Doanh thu thực tế (Gross Revenue), Giá trị đơn trung bình (AOV), Doanh thu thuần từ khách cũ vs khách mới.
- Đối chiếu số liệu đạt được so với mục tiêu KPI đã cam kết trong `campaign-plan.md` (Doanh thu mục tiêu, Ngân sách trần, CPA tối đa, ROAS kỳ vọng).

### Giai đoạn 2: Phân tích Hiệu suất Phối thức Kênh & Các Chỉ số Hợp nhất (Blended Metrics)
**Mục tiêu**: Đánh giá bức tranh toàn cảnh sức khỏe tài chính của chiến dịch, tránh bẫy tính trùng số liệu giữa các nền tảng.
- Tính toán các chỉ số hợp nhất (Blended Metrics):
  - **Blended ROAS (Doanh thu tổng / Tổng chi tiêu quảng cáo)**: Thước đo chính xác nhất về tính sinh lời của marketing.
  - **MER (Marketing Efficiency Ratio)**: Tỷ lệ hiệu quả tiếp thị tổng thể.
  - **Blended CPA (Chi phí quảng cáo tổng / Tổng số khách hàng mới)**: Giá mua khách hàng thực tế không bị thổi phồng.
- Đánh giá đóng góp từng kênh: Kênh nào tạo ra nhận thức tốt nhất (First-touch), kênh nào chốt đơn hiệu quả nhất (Last-touch), và kênh nào có chi phí tối ưu nhất.

### Giai đoạn 3: Rút ra Bài học Kinh nghiệm & Đề xuất Tối ưu Chu kỳ Mới
**Mục tiêu**: Đưa ra nhận định chiến lược sâu sắc và hành động thực tiễn, lưu file theo Naming Policy trong `config.md`.
- Chỉ rõ 3 điểm thành công lớn nhất (Wins) và 3 điểm nghẽn cần khắc phục (Losses / Bottlenecks).
- Đề xuất tái cơ cấu ngân sách cho tháng tiếp theo (Ví dụ: Cắt giảm 20% budget kênh kém hiệu quả để dồn sang kênh có ROAS cao).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/analytics/campaign-report.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/analytics/campaign-report.md`:

```markdown
# Báo Cáo Hiệu Quả Chiến Dịch Tiếp Thị Đa Kênh — <client_name>
- Client Slug: `<client-slug>`
- Tên chiến dịch: <Tên chiến dịch>
- Khung thời gian báo cáo: <Từ ngày ... đến ngày ...>
- Ngày phát hành: <YYYY-MM-DD>

## 1. Tóm Tắt Kết Quả Cốt Lõi (Executive Summary)
- **Tổng ngân sách tiếp thị đã chi**: ... VNĐ (Đạt ...% kế hoạch)
- **Tổng doanh thu ghi nhận**: ... VNĐ (Đạt ...% mục tiêu)
- **Blended ROAS**: <Doanh thu / Chi tiêu, ví dụ: 4.2x>
- **Chi phí bình quân / Đơn hàng (Blended CPA)**: ... VNĐ

## 2. Bảng So Sánh Hiệu Suất Theo Từng Kênh Phân Phối
| Kênh tiếp thị | Chi tiêu (VNĐ) | Doanh thu (VNĐ) | ROAS kênh | CPA (VNĐ) | Số chuyển đổi | Đánh giá hiệu quả |
|---|---|---|---|---|---|---|
| **Meta Ads** | 30.000.000 | 125.000.000 | 4.16x | 120.000 | 250 | 🟢 Đạt mục tiêu ROAS |
| **Google Ads (Search)**| 15.000.000 | 78.000.000 | 5.20x | 95.000 | 158 | 🟢 Hiệu suất rất cao |
| **TikTok Ads** | 10.000.000 | 22.000.000 | 2.20x | 210.000 | 48 | 🔴 CPA cao, cần đổi creative |
| **Email Marketing** | 1.500.000 | 35.000.000 | 23.3x | 15.000 | 100 | 🟢 Kênh nuôi dưỡng cực tốt |
| **Organic Search (SEO)**| Chi phí cố định | 45.000.000 | - | - | 120 | 🟢 Tăng trưởng tự nhiên bền vững |
| **TỔNG HỢP (BLENDED)** | **56.500.000** | **305.000.000** | **5.40x** | **83.500** | **676** | **XUẤT SẮC** |

## 3. Phân Tích Chuyên Sâu & Phát Hiện Then Chốt (Key Insights)
- **Creative chiến thắng**: Mẫu video UGC số 01 trên Meta đem lại 60% doanh số toàn kênh.
- **Điểm nghẽn**: Kênh TikTok CPA cao do đối tượng xem video thoát trang nhiều ở bước điền form (Cần chuyển giao cho `cro-audit-landing-page`).
- **Giá trị khách cũ (Retention)**: Doanh thu từ chuỗi email tự động chiếm 11.5% tổng doanh thu với chi phí cực thấp.

## 4. Khuyến Nghị Chiến Lược Cho Chu Kỳ Kế Tiếp
- [ ] Dịch chuyển 30% ngân sách từ TikTok sang Google Ads Search để mở rộng cụm từ khóa có ý định mua cao từ `seo-research-keyword-cluster`.
- [ ] Phối hợp với nhóm Creative sản xuất thêm 3 biến thể dựa trên concept video UGC chiến thắng.
```

## Don'ts
- Không cộng dồn doanh thu của từng nền tảng quảng cáo (Meta + Google + TikTok) rồi coi đó là doanh thu tổng vì các nền tảng thường nhận vơ công trạng (Attribution Overlap), dẫn đến số liệu ảo.
- Không báo cáo chỉ số vanity metrics (Lượt view, lượt like, reach) mà không gắn với chỉ số tài chính (Doanh thu, CPA, ROAS).
- Không viết báo cáo khô khan chỉ toàn số liệu mà thiếu phần phân tích bối cảnh và đề xuất hành động cho client.
- Không che giấu các kênh hoạt động kém hiệu quả; cần trung thực chỉ ra nguyên nhân và đề xuất phương án xử lý dứt khoát.

## Quality Checklist
- [ ] Báo cáo có đầy đủ các chỉ số tài chính cốt lõi (Chi tiêu, Doanh thu, Blended ROAS, Blended CPA).
- [ ] Bảng so sánh đa kênh bóc tách chi tiết từng kênh tiếp thị.
- [ ] Xác định rõ điểm thắng (Wins), điểm nghẽn (Bottlenecks) và bài học rút ra.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/analytics/campaign-report.md`.
