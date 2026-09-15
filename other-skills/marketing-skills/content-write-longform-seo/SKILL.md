---
name: content-write-longform-seo
description: "Viết bài blog/article chuẩn SEO chuyên sâu, cấu trúc heading phân tầng (H1-H3), tích hợp từ khóa ngữ nghĩa LSI, tối ưu Search Intent và giữ vững brand voice. Kích hoạt khi có yêu cầu 'viết bài SEO', 'viết blog', 'viết pillar content'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md."
---

# content-write-longform-seo: Viết Bài Chuyên Sâu Chuẩn SEO & Semantic Search

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "viết bài SEO", "viết blog chuẩn SEO", "soạn bài pillar", "viết bài theo cụm từ khóa", hoặc nhận danh sách từ khóa từ skill `seo-research-keyword-cluster`.

## Workflow

### Giai đoạn 1: Xác định Intent, Từ khóa & Cấu trúc Dàn ý
**Mục tiêu**: Thu thập từ khóa mục tiêu, search intent và định hình cấu trúc bài viết theo quy định `longform_seo_word_count` trong `config.md`.
- Đọc từ khóa chính (Primary Keyword), từ khóa phụ (Secondary Keywords) và từ khóa ngữ nghĩa LSI từ `seo-ads/keyword-clusters.md` hoặc brief của người dùng.
- Phân tích Search Intent của người tìm kiếm: Informational (tìm kiến thức), Commercial Investigation (so sánh giải pháp), hay Transactional (mua ngay).
- Xây dựng dàn ý heading phân tầng (H1 duy nhất, các H2 bao quát luận điểm lớn, các H3 giải thích chi tiết).
- Đảm bảo mục tiêu dung lượng bài viết nằm trong dải 1.500 – 3.500 từ (bài pillar tối thiểu 2.000 từ, bài cluster tối thiểu 1.200 từ) theo Validation Policy trong `config.md`.

### Giai đoạn 2: Chấp bút Nội dung Chuyên sâu & Tích hợp Giá trị Thực
**Mục tiêu**: Viết nội dung giải quyết thấu đáo vấn đề của người đọc, tuân thủ `brand_voice_guidelines`.
- **Mở bài (Introduction)**: Hook người đọc trong 3 câu đầu (nêu rõ vấn đề nhức nhối hoặc thực trạng giật mình), nêu lý do bài viết này giải quyết triệt để vấn đề, và chèn từ khóa chính tự nhiên trong 100 từ đầu tiên.
- **Thân bài (Body Sections)**:
  - Cung cấp kiến thức sâu, số liệu kiểm chứng, ví dụ thực tế hoặc bảng biểu so sánh trực quan.
  - Phân bổ từ khóa phụ và thực thể ngữ nghĩa (Entities) một cách mượt mà, tránh nhồi nhét (keyword stuffing).
  - Tích hợp các điểm neo liên kết nội bộ (Internal link anchor suggestions) trỏ về các bài viết liên quan hoặc trang sản phẩm.
- **Kết bài & Kêu gọi Hành động (Conclusion & CTA)**:
  - Tóm lược các bước hành động quan trọng (Key Takeaways).
  - CTA tự nhiên dẫn dắt người đọc sang giai đoạn cân nhắc mua hàng hoặc để lại thông tin tư vấn.

### Giai đoạn 3: Tối ưu On-Page Snippet & Xuất Deliverable
**Mục tiêu**: Viết thẻ Meta Title, Meta Description, URL slug và lưu file theo Naming Policy trong `config.md`.
- Viết Meta Title (dưới 60 ký tự, chứa từ khóa chính ở đầu).
- Viết Meta Description (dưới 155 ký tự, có từ khóa và kích thích click-through rate).
- Đặt tên file theo `<article-slug>.md` và lưu tại `docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md`:

```markdown
---
title: "<Meta Title chuẩn SEO - dưới 60 ký tự>"
meta_description: "<Meta Description cuốn hút - dưới 155 ký tự>"
primary_keyword: "<Từ khóa chính>"
secondary_keywords: ["<Từ khóa phụ 1>", "<Từ khóa phụ 2>", "<Từ khóa LSI>"]
search_intent: "Informational / Commercial"
word_count: <Số lượng từ>
---

# <Tiêu Đề Bài Viết H1 - Chứa Từ Khóa Chính Tự Nhiên>

*Tóm tắt nhanh (TL;DR): <3 câu tóm tắt giá trị bài viết cho độc giả bận rộn>*

## 1. <Tiêu đề H2 - Bối cảnh & Nhận diện Vấn đề>
<Nội dung giải thích sâu sắc, dẫn chứng cụ thể>

### 1.1. <Tiêu đề H3 - Chi tiết chuyên môn>
<Phân tích kỹ thuật, bảng dữ liệu hoặc case study>

## 2. <Tiêu đề H2 - Giải pháp & Hướng Dẫn Từng Bước>
- **Bước 1**: ...
- **Bước 2**: ...
- **Bước 3**: ...

## 3. <Tiêu đề H2 - Những Sai Lầm Thường Gặp Cần Tránh>
<Cảnh báo các bẫy phổ biến và cách khắc phục>

## 4. Tổng Kết & Lời Khuyên Hành Động
<Tóm lược key takeaways>

> [!TIP]
> **Đề xuất bước tiếp theo**: <CTA hướng độc giả click xem sản phẩm/dịch vụ của client>

---
### Gợi ý Internal Linking
- Trỏ tới bài: `[Tên bài]` qua anchor text: `"[Anchor text phù hợp]"`
```

## Don'ts
- Không viết bài hời hợt, nhồi nhét từ khóa thiếu tự nhiên làm suy giảm trải nghiệm người đọc.
- Không đạo văn hoặc xào xáo nội dung cũ của đối thủ mà không bổ sung góc nhìn mới hay số liệu thực tế.
- Không viết vượt ra ngoài tone giọng thương hiệu (`brand_voice_guidelines`).
- Không tạo bài viết dưới ngưỡng tối thiểu (1.200 từ cho cluster, 2.000 từ cho pillar) trừ khi người dùng chỉ định rõ.

## Quality Checklist
- [ ] Dung lượng bài viết đạt ngưỡng quy định tại Validation Policy trong `config.md`.
- [ ] Đầy đủ Meta Title (<60 ký tự) và Meta Description (<155 ký tự).
- [ ] Cấu trúc heading phân tầng rõ ràng (chỉ duy nhất một H1, các H2 và H3 logic).
- [ ] Có gợi ý anchor text cho internal linking và CTA chuyển đổi.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/content/seo-articles/<article-slug>.md`.
