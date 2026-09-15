---
name: seo-research-keyword-cluster
description: "Nghiên cứu và phân cụm từ khóa theo Search Intent (Informational, Navigational, Commercial, Transactional), xây dựng cấu trúc Topic Cluster và kiến trúc Silo nội dung cho website. Kích hoạt khi có yêu cầu 'nghiên cứu từ khóa', 'keyword research', 'phân cụm từ khóa', 'xây topic cluster'. Đầu ra lưu tại docs/marketing-projects/<client-slug>/seo-ads/keyword-clusters.md."
---

# seo-research-keyword-cluster: Nghiên Cứu & Phân Cụm Từ Khóa Topic Cluster

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu "nghiên cứu từ khóa", "phân cụm từ khóa", "keyword cluster", "lập danh sách từ khóa SEO", "thiết kế cấu trúc silo website", hoặc cần dữ liệu từ khóa trước khi viết bài với `content-write-longform-seo`.

## Workflow

### Giai đoạn 1: Mở rộng Từ khóa Hạt giống (Seed Keywords Expansion)
**Mục tiêu**: Khai thác toàn diện các truy vấn tìm kiếm xoay quanh sản phẩm và nhu cầu của khách hàng.
- Đọc thông tin ngành hàng, sản phẩm và persona từ `insight/icp.md`.
- Phát triển danh sách từ khóa hạt giống (Seed keywords) theo 3 nhánh chính:
  - Nhánh vấn đề/triệu chứng của người dùng (Problem-aware queries).
  - Nhánh tên giải pháp/chủng loại sản phẩm (Category queries).
  - Nhánh so sánh/đánh giá/thương hiệu (Brand & Comparison queries).
- Kết hợp các tiền tố và hậu tố tìm kiếm tự nhiên: "cách...", "tốt nhất", "ở đâu", "giá bao nhiêu", "đánh giá", "so sánh", "có nên...".

### Giai đoạn 2: Phân loại Ý định Tìm kiếm (Search Intent) & Phân cụm Ngữ nghĩa
**Mục tiêu**: Nhóm các từ khóa có cùng mục đích tìm kiếm vào một cụm duy nhất (Clustering) để tránh tự ăn thịt từ khóa (Keyword Cannibalization).
- Gắn nhãn Search Intent cho từng từ khóa:
  - **I (Informational)**: Tìm hiểu kiến thức, nguyên nhân, cách xử lý.
  - **C (Commercial Investigation)**: So sánh các thương hiệu, review, top list sản phẩm.
  - **T (Transactional)**: Có ý định mua ngay (kèm giá, địa chỉ, khuyến mãi, mua ở đâu).
- Gom nhóm theo nguyên tắc Topic Cluster:
  - 1 Từ khóa Trụ cột (Pillar Keyword): Volume lớn, độ bao quát cao, độ khó cao.
  - 4-8 Từ khóa Vệ tinh (Cluster Keywords): Từ khóa ngách (Long-tail keywords), search volume vừa/nhỏ, giải quyết các khía cạnh chuyên biệt.

### Giai đoạn 3: Thiết kế Kiến trúc Silo & Xuất Deliverable
**Mục tiêu**: Vẽ sơ đồ liên kết nội bộ (Internal Linking Matrix) giữa bài Pillar và các bài Cluster, lưu file theo Naming Policy trong `config.md`.
- Quy định đường dẫn URL slug dự kiến và cấu trúc liên kết 2 chiều (Pillar <-> Cluster).
- Ghi toàn bộ dữ liệu vào `docs/marketing-projects/<client-slug>/seo-ads/keyword-clusters.md`.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/seo-ads/keyword-clusters.md`:

```markdown
# Kế Hoạch Nghiên Cứu & Phân Cụm Từ Khóa (Keyword Clusters) — <client_name>
- Client Slug: `<client-slug>`
- Ngành hàng: <industry>
- Ngày lập: <YYYY-MM-DD>

## 1. Bản Đồ Kiến Trúc Topic Cluster (Silo Architecture)

### Cluster 1: <Tên Chủ Đề Cốt Lõi 1>
- **Từ khóa Pillar chính**: `<Từ khóa bao quát>` | Search Intent: Informational / Commercial | Ước tính Volume: Cao
- **URL Slug dự kiến**: `/kien-thuc/<slug-pillar>/`
- **Mục tiêu chuyển đổi**: Hướng dẫn toàn diện và dẫn dắt sang danh mục sản phẩm.

#### Bảng Danh Sách Từ Khóa Vệ Tinh (Sub-topics / Cluster Articles)
| STT | Từ khóa phụ / Long-tail | Search Intent | Định dạng bài viết | URL Slug con dự kiến | Quy tắc Internal Link |
|---|---|---|---|---|---|
| 1 | <Từ khóa ngách 1> | Informational | How-to Guide | `/kien-thuc/<slug-1>/` | Link trỏ về Pillar 1 |
| 2 | <Từ khóa ngách 2> | Commercial | So sánh / Review | `/kien-thuc/<slug-2>/` | Link trỏ về Pillar 1 & Product |
| 3 | <Từ khóa ngách 3> | Informational | Danh sách lỗi | `/kien-thuc/<slug-3>/` | Link trỏ về Pillar 1 |

---

### Cluster 2: <Tên Chủ Đề Cốt Lõi 2>
...

## 2. Hướng Dẫn Điều Phối Cho Đội Ngũ Viết Bài
- Thứ tự triển khai: Viết bài Pillar trước để định hình cấu trúc, sau đó triển khai các bài Cluster để bổ trợ sức mạnh SEO.
- Handoff sang skill: Sử dụng `content-write-longform-seo` để chấp bút từng bài viết theo các cụm từ khóa đã phê duyệt.
```

## Don'ts
- Không nhồi nhét nhiều từ khóa khác Search Intent vào chung một bài viết gây loãng trang.
- Không phân tách các từ khóa đồng nghĩa tuyệt đối thành các bài viết riêng biệt (gây lỗi tự ăn thịt từ khóa - Keyword Cannibalization).
- Không tự bịa đặt các con số search volume tuyệt đối khi không có công cụ đo lường chuyên dụng; chỉ nên phân cấp mức độ (Cao / Trung bình / Ngách dài).
- Không xây dựng cụm từ khóa rời rạc không liên kết được với danh mục sản phẩm/dịch vụ của client.

## Quality Checklist
- [ ] Xác định rõ tối thiểu 2 cụm Topic Cluster hoàn chỉnh.
- [ ] Mỗi cụm có 1 bài Pillar trung tâm và từ 4 đến 8 từ khóa vệ tinh (Cluster keywords).
- [ ] Mọi từ khóa đều được phân loại Search Intent (Informational, Commercial, Transactional).
- [ ] Có quy tắc định hướng liên kết nội bộ (Internal link) giữa Pillar và Sub-topics.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/seo-ads/keyword-clusters.md`.
