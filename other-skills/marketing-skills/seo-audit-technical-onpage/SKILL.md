---
name: seo-audit-technical-onpage
description: "Audit kỹ thuật SEO On-page và Technical SEO cho website hoặc URL cụ thể (thẻ meta, cấu trúc heading, internal link, schema markup, core web vitals, indexation, sitemap/robots). Kích hoạt khi có yêu cầu 'audit SEO', 'kiểm tra onpage', 'chẩn đoán website bị tụt hạng'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/seo-ads/technical-seo-audit.md."
---

# seo-audit-technical-onpage: Audit Kỹ Thuật SEO On-Page & Technical

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "audit SEO", "kiểm tra on-page website", "chẩn đoán lỗi kỹ thuật SEO", "website bị tụt traffic/thứ hạng", hoặc cần đánh giá hiện trạng SEO của client trước khi triển khai chiến dịch nội dung.

## Workflow

### Giai đoạn 1: Tiếp nhận URL & Rà soát Lập chỉ mục & Thu thập dữ liệu (Crawling & Indexing)
**Mục tiêu**: Kiểm tra khả năng bot tìm kiếm tiếp cận và lập chỉ mục nội dung trang web.
- Tiếp nhận URL trang web hoặc danh sách URL cần audit từ người dùng.
- Kiểm tra các tệp chỉ dẫn kỹ thuật:
  - Tệp `robots.txt`: Có vô tình chặn các thư mục quan trọng hay tài nguyên CSS/JS không.
  - Tệp `sitemap.xml`: Có đầy đủ, cập nhật và khai báo đúng trên Google Search Console không.
  - Thẻ `canonical`: Kiểm tra xem có bị trùng lặp nội dung hoặc trỏ sai địa chỉ không.
  - Thẻ `robots meta`: Kiểm tra cờ `noindex`, `nofollow` có bị cài đặt nhầm lẫn không.

### Giai đoạn 2: Rà soát On-Page & Tối ưu Trải nghiệm Trang (Page Experience)
**Mục tiêu**: Đánh giá chi tiết các yếu tố xếp hạng nội dung trên trang.
- **Thẻ Meta & URL**:
  - Độ dài Meta Title (<60 ký tự, chứa từ khóa) và Meta Description (<155 ký tự).
  - Cấu trúc URL thân thiện, ngắn gọn, không chứa tham số thừa hoặc ký tự đặc biệt.
- **Cấu trúc Heading**:
  - Chỉ duy nhất 1 thẻ H1 chứa từ khóa mục tiêu.
  - Phân cấp H2, H3 mạch lạc, không nhảy cóc cấp độ heading.
- **Hình ảnh & Đa phương tiện**:
  - Tối ưu thuộc tính `alt` mô tả chính xác nội dung ảnh.
  - Định dạng nén hiện đại (WebP) và dung lượng tệp (<150KB cho ảnh thông thường).
- **Liên kết Nội bộ (Internal Links) & Outbound Links**:
  - Kiểm tra liên kết gãy (Broken link 404).
  - Kiểm tra mật độ và tính liên quan của anchor text.
- **Dữ liệu có cấu trúc (Schema Markup)**:
  - Kiểm tra sự hiện diện của Schema phù hợp: `Article`, `Product`, `Organization`, `FAQPage`, `BreadcrumbList`.
- **Hiệu suất Tải trang & Core Web Vitals**:
  - Đánh giá LCP (Largest Contentful Paint), INP (Interaction to Next Paint), CLS (Cumulative Layout Shift).

### Giai đoạn 3: Phân loại Thứ tự Ưu tiên & Xuất Báo cáo Khắc phục
**Mục tiêu**: Lập danh sách lỗi theo mức độ nghiêm trọng và lưu file theo Naming Policy trong `config.md`.
- Phân loại lỗi theo 3 mức độ:
  - 🔴 **Nghiêm trọng (Critical / P0)**: Chặn index, lỗi 404 hàng loạt, thiếu H1/Title, website load > 5s.
  - 🟡 **Cảnh báo (Warning / P1)**: Thiếu alt text, Title quá dài, thiếu Schema, internal link yếu.
  - 🟢 **Cải thiện (Opportunity / P2)**: Tối ưu thêm từ khóa LSI, nén ảnh sâu hơn, bổ sung FAQ schema.
- Ghi toàn bộ nội dung vào `docs/marketing-projects/<client-slug>/seo-ads/technical-seo-audit.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/seo-ads/technical-seo-audit.md`:

```markdown
# Báo Cáo Audit Kỹ Thuật SEO On-Page (Technical SEO Audit) — <client_name>
- Client Slug: `<client-slug>`
- URL Kiểm tra: <URL>
- Ngày thực hiện: <YYYY-MM-DD>

## 1. Tóm Tắt Tình Trạng Kỹ Thuật (Executive Summary)
- Điểm đánh giá On-page tổng quan: <Tốt / Trung bình / Báo động>
- Số lỗi nghiêm trọng (Critical): <Số lượng> | Cảnh báo (Warning): <Số lượng>

## 2. Bảng Danh Mục Kiểm Tra Chi Tiết (Audit Matrix)
| Hạng mục kiểm tra | Tiêu chuẩn kỹ thuật | Hiện trạng phát hiện | Mức độ ưu tiên | Khuyến nghị khắc phục |
|---|---|---|---|---|
| **Robots.txt & Sitemap** | Hợp lệ, không chặn bot | Hoạt động bình thường | 🟢 P2 | Không cần sửa |
| **Thẻ Canonical** | Tự trỏ hoặc trỏ trang gốc | Thiếu canonical trên trang con | 🔴 P0 | Bổ sung thẻ `<link rel="canonical">` |
| **Thẻ Meta Title** | < 60 ký tự, chứa từ khóa | Dài 75 ký tự, bị cắt cụt | 🟡 P1 | Viết lại ngắn gọn dưới 60 ký tự |
| **Thẻ Meta Description** | 120 - 155 ký tự, có CTA | Bị để trống (trang tự lấy text) | 🟡 P1 | Bổ sung mô tả chứa từ khóa & CTA |
| **Thẻ Heading H1** | Duy nhất 1 thẻ H1/trang | Phát hiện 2 thẻ H1 | 🔴 P0 | Chuyển thẻ H1 thứ hai thành H2 |
| **Hình ảnh & Thẻ Alt** | Có alt text, dung lượng < 150KB | 5 ảnh thiếu alt, định dạng PNG nặng 2MB | 🟡 P1 | Chuyển sang WebP, bổ sung alt text |
| **Schema Markup** | Hợp lệ theo Schema.org | Chưa cài đặt Schema | 🟡 P1 | Tích hợp Schema Article/Product |
| **Core Web Vitals** | LCP < 2.5s, CLS < 0.1 | LCP 4.2s (Chậm do ảnh bìa) | 🔴 P0 | Tối ưu nén ảnh hero và bật Lazyload |

## 3. Lộ Trình Sửa Lỗi Từng Bước Cho Đội Ngũ Lập Trình & Content
1. **Tuần 1 (Sửa lỗi Critical)**: Khắc phục H1 kép, bổ sung canonical và tối ưu tốc độ LCP.
2. **Tuần 2 (Sửa lỗi Warning)**: Cập nhật meta title/description, bổ sung Schema và alt text hình ảnh.
```

## Don'ts
- Không đưa ra kết luận lỗi nếu không chỉ rõ URL cụ thể hoặc vị trí thẻ HTML bị vi phạm.
- Không liệt kê danh sách lỗi mà không có hướng dẫn kỹ thuật chi tiết để lập trình viên hoặc SEO content sửa chữa.
- Không bỏ qua yếu tố di động (Mobile responsiveness) vì Google áp dụng Mobile-first Indexing.
- Không nhầm lẫn giữa lỗi SEO on-page với lỗi chiến lược từ khóa hay nội dung mỏng (Thin content).

## Quality Checklist
- [ ] Báo cáo kiểm tra đầy đủ các trục: Indexing, Meta tags, Headings, Images, Schema, và Core Web Vitals.
- [ ] Mỗi vấn đề đều được gán mức độ ưu tiên rõ ràng (Critical, Warning, Opportunity).
- [ ] Có hướng dẫn khắc phục cụ thể theo từng bước hành động.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/seo-ads/technical-seo-audit.md`.
