---
name: insight-analyze-competitor
description: "Phân tích đối thủ cạnh tranh toàn diện theo ma trận positioning, pricing, content gap, channel mix và USP. Kích hoạt khi có yêu cầu 'phân tích đối thủ', 'competitor audit', 'so sánh đối thủ', hoặc cần tìm khoảng trống thị trường cho chiến dịch mới. Đầu ra lưu tại docs/marketing-projects/<client-slug>/insight/competitor-audit.md."
---

# insight-analyze-competitor: Phân Tích Đối Thủ & Tìm Khoảng Trống Thị Trường

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "phân tích đối thủ", "competitor audit", "đánh giá đối thủ cạnh tranh", "tìm content gap so với đối thủ", hoặc cung cấp danh sách URL/tên đối thủ của thương hiệu.

## Workflow

### Giai đoạn 1: Xác định Danh sách Đối thủ & Thu thập Dữ liệu
**Mục tiêu**: Lựa chọn 3 đến 5 đối thủ đại diện theo đúng quy định `competitor_analysis_count` trong `config.md`.
- Trích xuất danh sách đối thủ từ `key_competitors` trong `client_context` hoặc truy vấn người dùng.
- Phân loại đối thủ: Đối thủ trực tiếp (cùng sản phẩm, cùng phân khúc), Đối thủ gián tiếp (khác sản phẩm nhưng giải quyết cùng nhu cầu), Đối thủ tiềm năng (chiếm lĩnh thị phần truyền thông).
- Thu thập dữ liệu công khai: URL website, landing page, fanpage, kênh TikTok, thư viện quảng cáo (Meta Ads Library, Google Ads Transparency), và dải giá sản phẩm.

### Giai đoạn 2: Lập Ma trận So sánh & Bóc tách Chiến lược
**Mục tiêu**: Đánh giá đa chiều trên các trụ cột chiến lược tiếp thị.
- **Định vị & Thông điệp (Positioning & Messaging)**: Slogan, tuyên ngôn giá trị, góc định vị thương hiệu (chuyên gia, bình dân, cao cấp, đổi mới).
- **Chiến lược Giá & Phân khúc (Pricing Tier)**: Mức giá sàn, giá trần, chính sách bundle/khuyến mãi, định vị giá so với client.
- **Phối thức Kênh (Channel Mix)**: Kênh trọng tâm mang lại lượng tương tác và traffic lớn nhất (SEO, Facebook Ads, TikTok Shop, Email, KOLs).
- **Phân tích Khoảng trống Nội dung (Content Gap Analysis)**: Các chủ đề/angle đối thủ bỏ quên hoặc giải quyết hời hợt mà khách hàng mục tiêu đang bức xúc.
- **Điểm mạnh & Điểm yếu chí mạng**: Rào cản kỹ thuật, uy tín thương hiệu, chất lượng dịch vụ khách hàng từ phản hồi tiêu cực của người dùng.

### Giai đoạn 3: Tổng hợp Khuyến nghị Khác biệt hóa & Xuất File
**Mục tiêu**: Đề xuất chiến lược "đánh vào sườn" (Flanking Strategy) và ghi file theo Naming Policy trong `config.md`.
- Xây dựng ma trận so sánh trực quan và đề xuất 2-3 điểm khác biệt hóa sắc bén (USP) cho client.
- Ghi toàn bộ kết quả vào `docs/marketing-projects/<client-slug>/insight/competitor-audit.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/insight/competitor-audit.md`:

```markdown
# Báo Cáo Phân Tích Đối Thủ Cạnh Tranh (Competitor Audit) — <client_name>
- Client Slug: `<client-slug>`
- Ngày thực hiện: <YYYY-MM-DD>
- Số lượng đối thủ phân tích: <3 - 5 đối thủ>

## 1. Ma Trận So Sánh Năng Lực Cạnh Tranh
| Tiêu chí | Client: <client_name> | Đối thủ A: <Tên> | Đối thủ B: <Tên> | Đối thủ C: <Tên> |
|---|---|---|---|---|
| Phân khúc giá | ... | ... | ... | ... |
| Định vị cốt lõi | ... | ... | ... | ... |
| Kênh truyền thông chính | ... | ... | ... | ... |
| Chiến lược Ads chính | ... | ... | ... | ... |
| Điểm mạnh vượt trội | ... | ... | ... | ... |
| Điểm yếu bị phàn nàn | ... | ... | ... | ... |

## 2. Phân Tích Chi Tiết Từng Đối Thủ
### Đối thủ 1: <Tên đối thủ>
- URL / Kênh hoạt động: ...
- Chiến lược nội dung & Angle quảng cáo chủ đạo: ...
- Đánh giá Creative & Landing Page: ...

## 3. Bản Đồ Khoảng Trống Thị Trường (Content & Angle Gap)
- Khoảng trống nội dung chưa ai khai thác sâu: ...
- Nỗi đau của khách hàng mà đối thủ chưa đáp ứng: ...

## 4. Đề Xuất Chiến Lược Khác Biệt Hóa (Actionable Differentiation)
- Đề xuất USP truyền thông cho chiến dịch: ...
- Khuyến nghị kênh nên tập trung đối đầu hoặc né tránh: ...
```

## Don'ts
- Không liệt kê thông tin đối thủ chung chung dạng sao chép mô tả trang web mà thiếu phân tích đánh giá phản biện.
- Không phân tích dưới 3 đối thủ khiến góc nhìn bị phiến diện, hoặc vượt quá 5 đối thủ gây loãng thông tin chiến lược.
- Không bỏ qua thư viện quảng cáo của đối thủ khi phân tích các ngành hàng phụ thuộc vào performance ads.
- Không đưa ra kết luận khác biệt hóa nếu không dựa trên bằng chứng dữ liệu từ ma trận.

## Quality Checklist
- [ ] Số lượng đối thủ phân tích đạt từ 3 đến 5 theo Validation Policy trong `config.md`.
- [ ] Ma trận so sánh phản ánh đầy đủ: giá, định vị, kênh chính, điểm mạnh, điểm yếu.
- [ ] Xác định rõ ít nhất 2 khoảng trống nội dung hoặc khoảng trống thị trường (Gaps).
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/insight/competitor-audit.md`.
