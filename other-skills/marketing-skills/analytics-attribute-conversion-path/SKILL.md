---
name: analytics-attribute-conversion-path
description: "Phân tích quy kết chuyển đổi đa điểm chạm (Multi-Touch Attribution - MTA) giúp xác định chính xác đóng góp thực tế của từng kênh tiếp thị (First-touch, Last-touch, Linear, Time-decay, Data-driven). Giải quyết xung đột ghi nhận chuyển đổi giữa Meta Ads, Google Ads và TikTok Ads, đưa ra khuyến nghị phân bổ ngân sách khách quan. Kích hoạt khi có yêu cầu 'phân tích attribution', 'kênh nào thực sự hiệu quả', 'nên tăng ngân sách kênh nào'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/analytics/attribution-model.md."
---

# analytics-attribute-conversion-path: Phân Tích Quy Kết Chuyển Đổi Đa Điểm Chạm

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "phân tích attribution", "đánh giá xem kênh nào đóng góp nhiều nhất", "giải quyết xung đột số liệu giữa Facebook và Google Ads", "phân bổ lại ngân sách tiếp thị giữa các kênh", hoặc khi client đặt câu hỏi: "Nên tăng tiền chạy kênh Meta hay TikTok?".

## Workflow

### Giai đoạn 1: Tiếp nhận Dữ liệu Hành trình Đa điểm chạm (Multi-Touch Data)
**Mục tiêu**: Thu thập dữ liệu đường dẫn chuyển đổi (Conversion Paths) từ GA4 và các nền tảng quảng cáo.
- Thu thập dữ liệu đường dẫn chuyển đổi: Chuỗi các điểm chạm mà khách hàng đã tương tác trước khi mua (ví dụ: `TikTok Video (View) -> Facebook Ad (Click) -> Organic Search Blog (Read) -> Google Brand Search (Purchase)`).
- Thu thập số liệu tự báo cáo (Self-reported attribution) của từng ad platform (Meta báo cáo 300 đơn, Google báo cáo 250 đơn, trong khi thực tế trên hệ thống nội bộ chỉ có 400 đơn).
- Xác định độ dài hành trình chuyển đổi (Path length: số điểm chạm trung bình) và thời gian trễ từ điểm chạm đầu tới khi mua (Time lag: số ngày trung bình).

### Giai đoạn 2: So sánh Các Mô hình Quy kết (Attribution Modeling Comparison)
**Mục tiêu**: Áp dụng nhiều lăng kính quy kết để đánh giá toàn diện giá trị của từng kênh.
- **Mô hình Điểm chạm Cuối (Last-Touch Attribution)**:
  - Ghi nhận 100% công trạng cho kênh cuối cùng (thường là Google Brand Search hoặc Direct).
  - Nhược điểm: Đánh giá thấp các kênh tạo nhận thức ban đầu (Meta, TikTok).
- **Mô hình Điểm chạm Đầu (First-Touch Attribution)**:
  - Ghi nhận 100% công trạng cho kênh mở đầu phễu.
  - Nhược điểm: Bỏ qua nỗ lực thuyết phục và bám đuổi ở giai đoạn sau.
- **Mô hình Dựa trên Vị trí (Position-Based / U-Shaped)**:
  - Phân bổ 40% cho First-Touch, 40% cho Last-Touch, và 20% chia đều cho các điểm chạm ở giữa (Middle-touches).
- **Mô hình Suy giảm theo Thời gian (Time-Decay)**:
  - Các điểm chạm càng gần thời điểm mua hàng càng nhận được tỷ trọng ghi nhận cao hơn.
- **Mô hình Dựa trên Dữ liệu (Data-Driven Attribution - DDA)**:
  - Sử dụng thuật toán học máy (Machine Learning) để tính toán xác suất đóng góp gia tăng (Incremental value) của từng kênh.

### Giai đoạn 3: Phân tích Đóng góp Gia tăng & Đề xuất Phân bổ Ngân sách
**Mục tiêu**: Xóa bỏ tình trạng tranh chấp công trạng và đưa ra tỷ lệ phân bổ ngân sách tối ưu, lưu file theo Naming Policy trong `config.md`.
- Xác định rõ vai trò thực sự của từng kênh trong hệ sinh thái (Kênh mở phễu - Introducer, Kênh xúc tác - Influencer, Kênh chốt hạ - Closer).
- Đưa ra đề xuất điều chuyển ngân sách có căn cứ số liệu.
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/analytics/attribution-model.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/analytics/attribution-model.md`:

```markdown
# Báo Cáo Phân Tích Quy Kết Chuyển Đổi (Attribution Model Report) — <client_name>
- Client Slug: `<client-slug>`
- Giai đoạn phân tích: <Từ ngày ... đến ngày ...>
- Tổng số chuyển đổi thực tế: <Số đơn hàng thực nhận trên CRM>
- Ngày phát hành: <YYYY-MM-DD>

## 1. Ma Trận So Sánh Đóng Góp Theo Các Mô Hình Quy Kết
| Kênh tiếp thị | Last-Touch (Đơn) | First-Touch (Đơn) | U-Shaped (Đơn) | Data-Driven (Đơn) | Vai trò chủ đạo trong phễu |
|---|---|---|---|---|---|
| **TikTok Ads** | 45 | 185 | 110 | 125 | **Mở phễu (Introducer)**: Kích thích nhu cầu ban đầu cực mạnh |
| **Meta Ads** | 120 | 140 | 150 | 145 | **Xúc tác (Influencer)**: Duy trì nhận thức & nuôi dưỡng |
| **Google Search** | 180 | 45 | 105 | 95 | **Chốt hạ (Closer)**: Thu hoạch khách hàng đã có ý định mua |
| **SEO Blog** | 35 | 50 | 45 | 40 | **Giáo dục**: Tạo niềm tin và giải quyết băn khoăn |
| **Email CRM** | 20 | 0 | 10 | 15 | **Bám đuổi**: Tái kích hoạt giỏ hàng bỏ quên |

## 2. Giải Mã Xung Đột Dữ Liệu Nền Tảng (Overlap De-duplication)
- **Hiện tượng**: Meta tự nhận 265 đơn, Google tự nhận 225 đơn (Tổng = 490 đơn), nhưng thực tế chỉ có 400 đơn thành công.
- **Giải thích**: Có tới 90 đơn hàng khách hàng vừa xem/click quảng cáo Meta, sau đó lên Google tìm kiếm tên thương hiệu để mua hàng. Cả hai nền tảng đều tự tính công 100%.
- **Kết luận**: Google đóng vai trò hoàn tất giao dịch (Harvesting), nhưng nguồn tạo ra nhu cầu gốc (Demand Generation) chính là Meta & TikTok. Nếu cắt giảm ngân sách Meta/TikTok, doanh số từ Google Search sẽ tụt dốc theo sau 7-14 ngày.

## 3. Khuyến Nghị Tái Phân Bổ Ngân Sách Tối Ưu
- [ ] **Giữ vững hoặc tăng 15% ngân sách TikTok Ads**: Tiếp tục nuôi dưỡng nguồn khách hàng mới (Top-of-Funnel) để duy trì dòng traffic tiềm năng.
- [ ] **Tối ưu chiến dịch Google Search**: Thiết lập chiến dịch bảo vệ từ khóa thương hiệu (Brand Protection) với chi phí thấp để thu hoạch trọn vẹn lưu lượng được tạo ra từ social ads.
```

## Don'ts
- Không vội vàng cắt ngân sách của các kênh mở phễu (TikTok, Meta) chỉ vì báo cáo Last-Touch ghi nhận số lượng chuyển đổi thấp.
- Không tin tưởng mù quáng vào số liệu tự báo cáo trên từng trình quản lý quảng cáo của các nền tảng (Meta Ads Manager / TikTok Ads Manager) mà không đối chiếu với GA4 và CRM.
- Không áp dụng duy nhất một mô hình Last-Touch cho những sản phẩm có giá trị cao hoặc chu kỳ cân nhắc mua hàng dài (>14 ngày).
- Không đề xuất chuyển đổi 100% ngân sách đột ngột sang một kênh duy nhất làm đứt gãy hành trình khách hàng.

## Quality Checklist
- [ ] Báo cáo có bảng so sánh đa chiều giữa ít nhất 3 mô hình quy kết (Last-Touch, First-Touch, U-Shaped hoặc Data-Driven).
- [ ] Bóc tách và giải thích rõ ràng nguyên nhân xung đột số liệu tính trùng (Attribution Overlap) giữa các ad platforms.
- [ ] Định danh rõ vai trò của từng kênh trong hệ sinh thái (Introducer, Influencer, Closer).
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/analytics/attribution-model.md`.
