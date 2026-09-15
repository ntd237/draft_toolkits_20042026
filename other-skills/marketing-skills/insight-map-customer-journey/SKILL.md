---
name: insight-map-customer-journey
description: "Thiết kế bản đồ hành trình khách hàng đa giai đoạn (Awareness -> Consideration -> Decision -> Retention -> Advocacy), xác định điểm chạm (touchpoints), cảm xúc, rào cản tâm lý và cơ hội chuyển đổi. Kích hoạt khi có yêu cầu 'vẽ customer journey', 'mapping hành trình khách hàng', 'tìm điểm rơi rớt lead'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/insight/customer-journey.md."
---

# insight-map-customer-journey: Thiết Kế Bản Đồ Hành Trình Khách Hàng

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "vẽ customer journey", "lập bản đồ hành trình khách hàng", "phân tích điểm rơi rớt chuyển đổi", hoặc trước khi thiết kế funnel chiến dịch và cấu trúc luồng tự động hóa CRM.

## Workflow

### Giai đoạn 1: Tiếp nhận ICP & Xác định Hệ thống Điểm chạm
**Mục tiêu**: Đọc dữ liệu chân dung khách hàng từ `insight/icp.md` và xác định các kênh hiện diện của client.
- Tiếp nhận persona mục tiêu đã duyệt tại Insight Gate từ file `docs/marketing-projects/<client-slug>/insight/icp.md`.
- Thu thập danh mục điểm chạm (Touchpoints) client đang có hoặc dự kiến triển khai: Website, Fanpage, TikTok Shop, Google Ads, Zalo OA, Email, Đội ngũ tư vấn trực tiếp.

### Giai đoạn 2: Bóc tách Hành trình theo 5 Tầng Phễu
**Mục tiêu**: Mô hình hóa suy nghĩ, hành động, cảm xúc và rào cản của khách hàng qua từng chặng.
- **1. Nhận thức (Awareness / TOFU)**:
  - Hành động: Khách hàng gặp vấn đề, bắt đầu tìm kiếm thông tin hoặc vô tình thấy quảng cáo/nội dung giáo dục.
  - Điểm chạm: Social posts, TikTok video, SEO bài viết thông tin, Top-of-Funnel ads.
  - Cảm xúc & Nỗi đau: Mơ hồ, bối rối, chưa hiểu rõ bản chất vấn đề.
- **2. Cân nhắc & Đánh giá (Consideration / MOFU)**:
  - Hành động: Khách hàng so sánh giải pháp của client với đối thủ hoặc phương pháp tự làm.
  - Điểm chạm: Bài so sánh sản phẩm, review KOL/KOC, case study, feedback khách cũ, webinar/demo.
  - Cảm xúc & Nỗi đau: Lo sợ lãng phí tiền, nghi ngờ chất lượng hoặc cam kết bảo hành.
- **3. Ra quyết định & Mua hàng (Decision / BOFU)**:
  - Hành động: Bỏ hàng vào giỏ, điền form đăng ký, chat với tư vấn viên, thanh toán.
  - Điểm chạm: Landing page, tin nhắn chốt đơn, giỏ hàng thương mại điện tử, nhân viên bán hàng.
  - Cảm xúc & Nỗi đau: Ngại quy trình thanh toán rườm rà, tiếc tiền phút chót, thiếu trust signal.
- **4. Duy trì & Gắn kết (Retention)**:
  - Hành động: Nhận hàng, sử dụng sản phẩm, liên hệ hỗ trợ hoặc nhận chuỗi onboarding email.
  - Điểm chạm: SMS/Email thông báo đơn, hướng dẫn sử dụng, dịch vụ CSKH, cộng đồng người dùng.
- **5. Trung thành & Giới thiệu (Advocacy)**:
  - Hành động: Đánh giá 5 sao, giới thiệu người thân bạn bè, mua lại (repeat purchase).
  - Điểm chạm: Chương trình loyalty, voucher khách hàng thân thiết, chương trình affiliate/referral.

### Giai đoạn 3: Xác định Điểm Rơi rớt & Đề xuất Giải pháp Kích hoạt
**Mục tiêu**: Định vị chính xác vị trí khách hàng dễ từ bỏ nhất và đề xuất giải pháp cho Content/Ads/CRM.
- Đánh dấu các điểm nghẽn nghiêm trọng (Friction points) và rò rỉ chuyển đổi (Conversion leaks).
- Tổng hợp thành file deliverable theo đúng Naming Policy trong `config.md` tại `docs/marketing-projects/<client-slug>/insight/customer-journey.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/insight/customer-journey.md`:

```markdown
# Bản Đồ Hành Trình Khách Hàng (Customer Journey Map) — <client_name>
- Client Slug: `<client-slug>`
- Persona Trọng Tâm: <Tên persona đại diện từ icp.md>
- Ngày hoàn thành: <YYYY-MM-DD>

## 1. Ma Trận Hành Trình Toàn Diện (5 Giai Đoạn)
| Tiêu chí | 1. Nhận thức (TOFU) | 2. Cân nhắc (MOFU) | 3. Quyết định (BOFU) | 4. Duy trì (Retention) | 5. Trung thành (Advocacy) |
|---|---|---|---|---|---|
| **Mục tiêu khách hàng** | Tìm hiểu nguyên nhân | So sánh giải pháp | Chọn phương án tối ưu | Giải quyết triệt để | Chia sẻ & nhận ưu đãi |
| **Điểm chạm (Touchpoints)** | Video TikTok, Bài blog SEO | Review, So sánh, Case study | Landing page, Sales chat | Email onboarding, CSKH | Cộng đồng, Referral |
| **Suy nghĩ nội tâm** | "Sao mình lại bị thế này?" | "Cái này có tốt hơn loại X?" | "Mua ở đây có uy tín không?" | "Dùng thế nào cho đúng?" | "Sản phẩm này rất đáng tiền" |
| **Cảm xúc chủ đạo** | Lo lắng, tò mò | Đắn đo, phân vân | Hồi hộp, hy vọng | An tâm hoặc thất vọng | Tự hào, tin tưởng |
| **Rào cản / Điểm nghẽn** | Chưa tin thương hiệu | Thiếu bằng chứng chứng thực | Form dài, phí ship cao | Hướng dẫn sơ sài | Không có lý do quay lại |
| **Cơ hội Marketing** | Nội dung hữu ích không bán hàng | Case study thực tế, bảo hành | Ưu đãi giới hạn, live chat | Email chăm sóc tự động | Tặng quà tri ân |

## 2. Phân Tích Điểm Nghẽn Trọng Yếu (Critical Drop-off Points)
- **Điểm nghẽn số 1**: <Mô tả điểm rơi rớt lớn nhất, ví dụ: khách xem demo xong không chuyển đổi>
- **Điểm nghẽn số 2**: <Ví dụ: tỷ lệ bỏ giỏ hàng cao ở bước nhập thông tin>

## 3. Khuyến Nghị Phối Hợp Đa Bộ Phận
- **Chuyển giao cho Nhóm Content**: Cần bổ sung các bài viết MOFU giải đáp nghi ngại.
- **Chuyển giao cho Nhóm SEO & Ads**: Retargeting khách hàng dừng ở giai đoạn BOFU bằng ưu đãi mạnh.
- **Chuyển giao cho Nhóm CRM**: Thiết lập luồng tự động cứu giỏ hàng và onboarding khách hàng mới.
```

## Don'ts
- Không vẽ hành trình một chiều lý tưởng mà bỏ qua các bước khách hàng thoát trang, nghi ngờ hoặc do dự.
- Không mô tả điểm chạm chung chung thiếu gắn kết với các kênh truyền thông thực tế của client.
- Không tự ý lập hành trình khi chưa có dữ liệu đầu vào từ `insight/icp.md`.
- Không bỏ qua giai đoạn sau mua hàng (Retention & Advocacy) trong mô hình kinh doanh có tính chu kỳ hoặc đòi hỏi LTV cao.

## Quality Checklist
- [ ] Phủ kín đủ 5 giai đoạn từ Nhận thức đến Trung thành.
- [ ] Mỗi giai đoạn xác định rõ điểm chạm, suy nghĩ, cảm xúc, rào cản và cơ hội.
- [ ] Định vị rõ ít nhất 2 điểm nghẽn chuyển đổi lớn và giải pháp tương ứng.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/insight/customer-journey.md`.
