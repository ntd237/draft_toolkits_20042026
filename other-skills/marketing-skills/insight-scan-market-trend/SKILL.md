---
name: insight-scan-market-trend
description: "Quét xu hướng thị trường, social listening và search trend theo thời gian thực. Xác định chủ đề thịnh hành, chỉ số độ nóng (Heat Index) và cơ hội đón sóng nội dung cho chiến dịch marketing. Kích hoạt khi có yêu cầu 'quét xu hướng', 'trend ngành', 'lên ý tưởng chiến dịch theo mùa/Tết/sự kiện'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/insight/trend-report.md."
---

# insight-scan-market-trend: Quét Xu Hướng Thị Trường & Dữ Liệu Thời Gian Thực

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "quét xu hướng", "trend ngành X", "tìm chủ đề thịnh hành", "chuẩn bị chiến dịch mùa vụ/Tết/Black Friday", hoặc cần dữ liệu search trend/social listening mới nhất cho ngành hàng.

## Workflow

### Giai đoạn 1: Xác định Phạm vi Quét & Nguồn Dữ liệu
**Mục tiêu**: Thiết lập bộ từ khóa hạt giống và khung thời gian khảo sát theo `client_context`.
- Thu thập ngành hàng (`industry`), thị trường đích (`target_market`: Việt Nam hoặc quốc tế) và khung thời gian (7 ngày, 30 ngày, hoặc xu hướng mùa vụ 3-6 tháng tới).
- Phân tách cụm chủ đề cần quét:
  - Xu hướng văn hóa / hành vi tiêu dùng đại chúng (Macro trends).
  - Xu hướng thảo luận trên mạng xã hội (TikTok, Facebook, Threads, YouTube).
  - Xu hướng tìm kiếm Google Trends liên quan đến nhu cầu giải quyết vấn đề của sản phẩm.

### Giai đoạn 2: Đánh giá Mức độ Nóng & Phân loại Xu hướng
**Mục tiêu**: Lọc nhiễu và chấm điểm tiềm năng ứng dụng của từng xu hướng theo Heat Index.
- Chấm điểm Heat Index từ 1 đến 5 sao dựa trên 3 tiêu chí:
  1. **Volume & Tốc độ tăng trưởng**: Lượng thảo luận/tìm kiếm có tăng đột biến không.
  2. **Độ tương thích thương hiệu**: Có phù hợp với `brand_voice_guidelines` và sản phẩm của client không.
  3. **Tuổi thọ xu hướng (Trend Shelf-life)**: Trend chớp nhoáng (Micro-trend vài ngày) hay xu hướng hành vi bền vững (Macro-trend nhiều quý).
- Xác định góc tiếp cận (Angle) khả thi: Hài hước giải trí, Giáo dục người dùng, Phản biện xu hướng sai lầm, hoặc Cung cấp giải pháp đột phá.

### Giai đoạn 3: Tổng hợp Báo cáo Xu hướng & Đề xuất Kích hoạt
**Mục tiêu**: Đưa ra hành động cụ thể cho đội ngũ Content và Ads, lưu file theo Naming Policy trong `config.md`.
- Lập bảng danh mục xu hướng kèm đề xuất format triển khai (Reels, TikTok, bài blog, hoặc hook quảng cáo).
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/insight/trend-report.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/insight/trend-report.md`:

```markdown
# Báo Cáo Xu Hướng Thị Trường (Market Trend Report) — <client_name>
- Client Slug: `<client-slug>`
- Ngành hàng: <industry> | Khung thời gian: <Thời gian quét>
- Ngày cập nhật: <YYYY-MM-DD>

## 1. Bản Đồ Xu Hướng & Chỉ Số Độ Nóng (Heat Index)
| Xu hướng / Chủ đề | Nền tảng nổi bật | Heat Index (1-5★) | Phân loại (Micro / Macro) | Mức độ phù hợp thương hiệu |
|---|---|---|---|---|
| Chủ đề 1 | TikTok / Threads | ★★★★★ | Macro | Cao — Sản phẩm giải quyết trực tiếp |
| Chủ đề 2 | Google Search | ★★★★☆ | Bền vững | Rất cao — Phù hợp làm SEO Pillar |
| Chủ đề 3 | Facebook Group | ★★★☆☆ | Micro (ngắn hạn) | Trung bình — Bắt trend social post |

## 2. Phân Tích Chuyên Sâu Từng Xu Hướng
### Xu hướng 1: <Tên xu hướng>
- **Bối cảnh & Động lực thúc đẩy**: <Tại sao người dùng lại quan tâm lúc này>
- **Từ khóa & Hashtag liên quan**: <Danh sách hashtag / query phổ biến>
- **Tâm lý khách hàng (Customer Sentiment)**: <Cảm xúc chủ đạo: hào hứng, lo lắng, tò mò>

## 3. Ý Tưởng Kích Hoạt Chiến Dịch (Activation Ideas)
- **Gợi ý cho Content Social**: <Format bài đăng, hook 3 giây cho short video>
- **Gợi ý cho Performance Ads**: <Hook quảng cáo đón đầu mối quan tâm>
- **Cảnh báo rủi ro (Brand Safety)**: <Những điều cần tránh để không gây phản cảm hoặc tranh cãi tiêu cực>
```

## Don'ts
- Không liệt kê các xu hướng vô thưởng vô phạt không liên quan đến ngành hàng hoặc giá trị cốt lõi của client.
- Không khuyến khích bắt các trào lưu độc hại, gây tranh cãi tiêu cực hoặc vi phạm thuần phong mỹ tục làm tổn hại uy tín thương hiệu.
- Không nhầm lẫn giữa trend ngắn hạn 48 giờ với xu hướng tiêu dùng mang tính cấu trúc của thị trường.
- Không đưa ra các nhận định về độ nóng nếu không có căn cứ từ dữ liệu tìm kiếm hoặc mạng xã hội.

## Quality Checklist
- [ ] Báo cáo có phân loại rõ ràng giữa xu hướng vi mô (ngắn hạn) và vĩ mô (dài hạn).
- [ ] Mỗi xu hướng đều có điểm đánh giá Heat Index và mức độ phù hợp với thương hiệu.
- [ ] Có đề xuất góc khai thác cụ thể cho Content và Ads kèm lưu ý về Brand Safety.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/insight/trend-report.md`.
