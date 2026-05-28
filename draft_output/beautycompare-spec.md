# BeautyCompare — Đặc tả Luồng & Chức năng

## 1. Tổng quan ứng dụng

| Thuộc tính | Giá trị |
|---|---|
| Tên app | BeautyCompare |
| Platform | iOS & Android (cross-platform — Flutter) |
| Người dùng mục tiêu | Người tiêu dùng Việt Nam, 18–35 tuổi, quan tâm skincare/makeup |
| Nguồn dữ liệu | Shopee VN, Lazada VN, Tiki VN |
| Ngôn ngữ giao diện | Tiếng Việt |
| Chiến lược dữ liệu | Cache TTL 6 giờ + refresh thủ công; fallback hiển thị dữ liệu cũ kèm banner cảnh báo |

---

## 2. Sơ đồ luồng màn hình (Screen Flow)

```
[Splash]
    → [Onboarding] (lần đầu)
    → [Home / Search]
        → [Search Results]
            → [Product Selection] (chọn 2–4 sản phẩm)
                → [Comparison View]
                    → [Product Detail] (drill-down tùy chọn)
                    → [Buy Redirect] (bottom sheet chọn sàn → deep-link / browser)
```

**Luồng chính (Happy Path):**
1. User mở app → Home
2. Gõ tên sản phẩm/thương hiệu → Search Results
3. Tick chọn 2–4 sản phẩm → nhấn "So sánh"
4. Xem bảng so sánh → nhấn "Mua ngay" trên sản phẩm muốn mua
5. Chọn sàn TMĐT → chuyển sang app/trình duyệt TMĐT

---

## 3. Đặc tả từng màn hình

### Màn hình 1: Splash / Onboarding
- **Mục đích:** Khởi động app, hiển thị brand, xin quyền cần thiết
- **Thành phần UI chính:**
  - Logo + tên app
  - Animation loading ngắn (≤2s)
  - Màn hình onboarding 3 slide (chỉ hiện lần đầu): giới thiệu tính năng so sánh, xem thành phần, mua ngay
  - Nút "Bắt đầu" ở slide cuối
- **Hành động người dùng:** Vuốt qua slides, nhấn "Bắt đầu" hoặc "Bỏ qua"
- **Điều hướng đến:** Home / Search
- **Edge cases:**
  - App đã cài trước → bỏ qua onboarding, vào thẳng Home
  - Splash timeout >3s → force navigate sang Home

---

### Màn hình 2: Home / Search
- **Mục đích:** Điểm vào chính — tìm kiếm sản phẩm và xem gợi ý
- **Thành phần UI chính:**
  - Search bar (placeholder: "Tìm tên sản phẩm, thương hiệu, thành phần...")
  - Section "Đang hot": top 5 sản phẩm được so sánh nhiều nhất (7 ngày)
  - Section "So sánh gần đây": lịch sử 3 phiên so sánh gần nhất (lưu local)
  - Bottom navigation: Home | Lịch sử | Cài đặt
- **Hành động người dùng:**
  - Tap search bar → focus, bàn phím hiện
  - Tap sản phẩm trong "Đang hot" → vào Search Results với keyword đó
  - Tap phiên so sánh gần đây → mở lại Comparison View đã lưu
- **Điều hướng đến:** Search Results
- **Edge cases:**
  - Lần đầu dùng, chưa có lịch sử → ẩn section "So sánh gần đây"
  - Không có internet → hiển thị banner "Đang offline — dữ liệu có thể chưa cập nhật", vẫn cho xem lịch sử local

---

### Màn hình 3: Search Results
- **Mục đích:** Hiển thị danh sách sản phẩm khớp với từ khóa tìm kiếm
- **Thành phần UI chính:**
  - Search bar (giữ keyword, có nút xóa)
  - Bộ lọc nhanh: Danh mục (Skincare / Makeup / Haircare), Thương hiệu, Khoảng giá
  - Danh sách kết quả: thumbnail | tên sản phẩm | thương hiệu | giá TB | rating trung bình
  - Chip hiển thị số sản phẩm đã chọn (ví dụ: "Đã chọn 2/4")
  - Nút "So sánh ngay" (disabled khi chọn <2, enabled khi chọn 2–4)
- **Hành động người dùng:**
  - Tick checkbox chọn sản phẩm
  - Áp dụng bộ lọc
  - Nhấn "So sánh ngay"
  - Scroll infinite load (20 items/page)
- **Điều hướng đến:** Comparison View
- **Edge cases:**
  - Không có kết quả → hiển thị "Không tìm thấy sản phẩm nào cho '[keyword]'" + gợi ý từ khóa khác
  - Chọn >4 sản phẩm → disable checkbox còn lại, toast "Tối đa 4 sản phẩm để so sánh"
  - Kết quả tải lỗi → hiển thị "Không tải được kết quả. Thử lại?" với nút retry

---

### Màn hình 4: Product Selection (tích hợp trong Search Results)
- **Mục đích:** Xác nhận danh sách sản phẩm trước khi so sánh
- **Thành phần UI chính:**
  - Bottom sheet hoặc floating bar hiển thị thumbnail các sản phẩm đã chọn
  - Nút xóa từng sản phẩm khỏi danh sách chọn
  - Nút "So sánh ngay" với badge số lượng
- **Hành động người dùng:** Xóa sản phẩm khỏi selection, xác nhận so sánh
- **Điều hướng đến:** Comparison View
- **Edge cases:**
  - Xóa hết → nút "So sánh ngay" disabled
  - Còn 1 sản phẩm → toast "Cần ít nhất 2 sản phẩm để so sánh"

---

### Màn hình 5: Comparison View
- **Mục đích:** Hiển thị bảng so sánh side-by-side các sản phẩm đã chọn
- **Thành phần UI chính:**
  - Header: tên các sản phẩm (sticky khi scroll dọc)
  - Cột đầu sticky: tên tiêu chí (Giá TB, Lượt mua, Đánh giá, Thành phần)
  - Cells dữ liệu: scroll ngang khi >2 sản phẩm
  - Highlight: giá thấp nhất (nền xanh lá), rating cao nhất (icon sao vàng)
  - Row "Thành phần": hiển thị số lượng thành phần + nút "Xem chi tiết"
  - Nút "Mua ngay" dưới mỗi cột sản phẩm
  - Nút "Lưu so sánh" (lưu local)
- **Hành động người dùng:**
  - Scroll ngang xem sản phẩm
  - Scroll dọc xem tiêu chí
  - Tap "Xem chi tiết" → Product Detail
  - Tap "Mua ngay" → Buy Redirect
  - Tap "Lưu so sánh" → lưu vào lịch sử
- **Điều hướng đến:** Product Detail, Buy Redirect
- **Edge cases:**
  - Một platform không có dữ liệu → hiển thị "—" trong cell đó
  - Tất cả platforms đều không có dữ liệu cho 1 tiêu chí → hiển thị "Chưa có dữ liệu" toàn row
  - Dữ liệu đang tải → skeleton loader cho từng cell

---

### Màn hình 6: Product Detail
- **Mục đích:** Xem chi tiết đầy đủ một sản phẩm — giá từng sàn, toàn bộ thành phần
- **Thành phần UI chính:**
  - Thumbnail lớn + tên + thương hiệu
  - Bảng giá theo từng sàn: Shopee | Lazada | Tiki (giá min–max, lượt mua, rating)
  - Danh sách thành phần đầy đủ (INCI): mỗi thành phần có icon cảnh báo nếu cần
  - Tooltip khi tap thành phần: tên tiếng Việt + công dụng
  - Nút "Mua ngay" (sticky bottom)
- **Hành động người dùng:**
  - Tap thành phần → tooltip
  - Tap "Mua ngay" → Buy Redirect
  - Tap nút back → Comparison View
- **Điều hướng đến:** Buy Redirect
- **Edge cases:**
  - Sản phẩm không có trên một sàn → ẩn hàng đó trong bảng giá
  - Danh sách thành phần rỗng → "Chưa có thông tin thành phần cho sản phẩm này"
  - Tooltip không có dữ liệu → "Chưa có mô tả cho thành phần này"

---

### Màn hình 7: Buy Redirect
- **Mục đích:** Cho user chọn sàn TMĐT và chuyển sang trang sản phẩm
- **Thành phần UI chính:**
  - Bottom sheet: tiêu đề "Chọn sàn để mua"
  - Danh sách sàn có sản phẩm: logo sàn | giá hiện tại | rating | nút "Đến [Shopee/Lazada/Tiki]"
  - Nút "Huỷ"
- **Hành động người dùng:**
  - Chọn sàn → app thực hiện deep-link
  - Nhấn "Huỷ" → đóng bottom sheet, quay lại Comparison View
- **Điều hướng đến:** App TMĐT (deep-link) hoặc trình duyệt (fallback)
- **Edge cases:**
  - Sản phẩm chỉ có trên 1 sàn → bỏ qua bottom sheet, redirect thẳng
  - App TMĐT chưa cài → fallback mở browser với `product_url`
  - Deep-link thất bại (timeout 2s) → tự động fallback browser, toast "Đang mở trình duyệt..."
  - Tất cả URLs đều không hợp lệ → toast "Không thể mở trang sản phẩm. Vui lòng thử lại sau."

---

## 4. Đặc tả chức năng (F1–F5)

### F1 — Product Search
- **Input:** Chuỗi keyword (tên sản phẩm, thương hiệu, tên thành phần INCI)
- **Output:** Danh sách sản phẩm có điểm match, sắp xếp theo relevance score giảm dần
- **Rules:**
  - Tối thiểu 2 ký tự mới trigger search
  - Debounce 300ms sau lần gõ cuối
  - Tìm kiếm không phân biệt hoa thường, có hỗ trợ không dấu (ví dụ: "duong am" → "dưỡng ẩm")
  - Kết quả rỗng → hiển thị "Không tìm thấy '[keyword]'" + gợi ý từ khóa liên quan
  - Lịch sử tìm kiếm: lưu 10 keyword gần nhất, hiển thị khi focus search bar

---

### F2 — Data Aggregation
- **Input:** `product_id` + danh sách platforms cần fetch
- **Output:** Object `PlatformData` cho từng platform
- **Rules:**
  - Fetch song song (parallel) từ Shopee/Lazada/Tiki, timeout mỗi request: 5s
  - `avg_price` = trung bình cộng `price_min` và `price_max` của listing đầu tiên
  - `purchase_volume` = tổng lượt bán 30 ngày nếu API cung cấp; fallback: tổng lượt bán all-time
  - `rating` = rating trung bình có trọng số theo `review_count`
  - `ingredients` = parse từ mô tả sản phẩm, ưu tiên INCI format; fallback: raw text
  - Cache kết quả TTL 6 giờ theo `product_id + platform`
  - Nếu platform trả lỗi hoặc timeout → field đó = `null`, UI hiển thị "—"

---

### F3 — Comparison Table
- **Input:** Danh sách 2–4 `Product` objects đã có `PlatformData`
- **Output:** Bảng so sánh render trên UI
- **Rules:**
  - Cột đầu (tên tiêu chí) sticky khi scroll ngang
  - Header hàng (tên sản phẩm) sticky khi scroll dọc
  - Highlight giá thấp nhất: nền `#E8F5E9` (xanh lá nhạt)
  - Highlight rating cao nhất: icon ⭐ màu vàng `#FFC107`
  - Thành phần chung giữa ≥2 sản phẩm: in đậm trong danh sách
  - Nếu tất cả giá trị trong 1 row đều `null` → hiển thị "Chưa có dữ liệu" full-width
  - Số thành phần hiển thị tóm tắt: "X thành phần" + nút "Xem tất cả"

---

### F4 — Buy Redirect
- **Input:** `product_id`, `platform` được chọn
- **Output:** Mở app TMĐT hoặc browser tại URL sản phẩm
- **Rules:**
  - Deep-link URI schemes:
    - Shopee: `shopee://product?itemid={item_id}&shopid={shop_id}`
    - Lazada: `lazada://product?itemId={item_id}`
    - Tiki: `tiki://product/{product_id}`
  - Timeout deep-link: 2s → nếu không mở được → fallback `https://` URL
  - Nếu sản phẩm chỉ có trên 1 platform → bỏ qua bottom sheet, redirect thẳng
  - Log analytics event: `buy_redirect_clicked { product_id, platform, source_screen, timestamp }`
  - Không lưu thông tin thanh toán hay tài khoản TMĐT của user

---

### F5 — Ingredient Analysis (Enhancement)
- **Input:** Danh sách thành phần INCI của sản phẩm
- **Output:** Danh sách thành phần có annotation (cảnh báo / công dụng)
- **Rules:**
  - Danh sách thành phần cần cảnh báo (cấu hình được, không hardcode): parabens, SLS/SLES, formaldehyde releasers, oxybenzone
  - Icon cảnh báo ⚠️ màu cam cho thành phần trong danh sách trên
  - Tooltip khi tap: tên tiếng Việt + công dụng + mức độ an toàn (Safe / Caution / Avoid)
  - Nếu thành phần không có trong database → không hiển thị tooltip, không hiển thị icon

---

## 5. Mô hình dữ liệu

```typescript
interface Product {
  id: string
  name: string
  brand: string
  category: "skincare" | "makeup" | "haircare" | "bodycare"
  thumbnail_url: string
  platforms: PlatformData[]
  ingredients: string[]        // INCI names, lowercase
  last_updated: number         // Unix timestamp
}

interface PlatformData {
  platform: "shopee" | "lazada" | "tiki"
  product_url: string          // https:// fallback URL
  deep_link: string            // URI scheme link
  price_min: number | null     // VND
  price_max: number | null     // VND
  avg_price: number | null     // VND, computed
  purchase_volume: number | null  // units sold
  rating: number | null        // 1.0–5.0, 1 decimal
  review_count: number | null
  fetched_at: number           // Unix timestamp
}

interface ComparisonSession {
  id: string
  product_ids: string[]        // 2–4 items
  created_at: number
  label: string                // auto-generated: "So sánh [brand1] vs [brand2]"
}

interface IngredientInfo {
  inci_name: string
  vi_name: string
  function: string
  safety_level: "safe" | "caution" | "avoid"
}
```

---

## 6. Xử lý lỗi & Edge Cases

| Scenario | Xử lý |
|---|---|
| Platform API timeout (>5s) | Skeleton loader → hiển thị "—" cho field đó, icon ⚠️ nhỏ với tooltip "Không tải được từ [platform]" |
| Sản phẩm không có trên một sàn | Hiển thị "—" trong cột platform đó |
| Deep-link app chưa cài | Tự động fallback mở browser với `product_url`, toast "Đang mở trình duyệt..." |
| Không có kết nối internet | Hiển thị dữ liệu cache (nếu có) + banner vàng "Đang offline — dữ liệu có thể chưa cập nhật"; nếu không có cache → màn hình lỗi với nút "Thử lại" |
| Danh sách thành phần không có | Hiển thị "Chưa có thông tin thành phần" trong row Thành phần |
| User chọn >4 sản phẩm | Disable checkbox còn lại, toast "Tối đa 4 sản phẩm để so sánh" |
| Tất cả platforms đều lỗi | Row hiển thị "Chưa có dữ liệu" full-width, nút "Tải lại" |
| Deep-link thất bại sau 2s | Fallback browser, log event `deep_link_failed { product_id, platform }` |
| URL sản phẩm không hợp lệ | Toast "Không thể mở trang sản phẩm. Vui lòng thử lại sau." |

---

## 7. Yêu cầu phi chức năng

### Performance
- Thời gian khởi động app (cold start): ≤3s trên thiết bị tầm trung (RAM 3GB)
- Thời gian tải kết quả tìm kiếm: ≤2s với kết nối 4G
- Thời gian render Comparison View: ≤1.5s sau khi có đủ dữ liệu
- Cache hit rate mục tiêu: ≥70% cho các sản phẩm phổ biến (top 1000)
- Kích thước app: ≤50MB (iOS), ≤40MB (Android)

### Security & Privacy
- Không lưu thông tin tài khoản TMĐT của user
- Analytics events không chứa PII (Personally Identifiable Information)
- Deep-link URLs phải được validate trước khi mở (whitelist domain: shopee.vn, lazada.vn, tiki.vn)
- HTTPS bắt buộc cho tất cả API calls; certificate pinning cho production

### Accessibility
- Font size tối thiểu: 14sp
- Contrast ratio: ≥4.5:1 (WCAG AA)
- Tất cả interactive elements có `contentDescription` cho screen reader
- Hỗ trợ Dynamic Type (iOS) / Font Scale (Android)

### Offline
- Lịch sử so sánh: lưu local (SQLite / Hive), truy cập được khi offline
- Dữ liệu sản phẩm cache: lưu local với TTL 6 giờ
- Tìm kiếm offline: chỉ tìm trong cache local, hiển thị banner offline

---

## 8. Checklist trước khi phát triển

### Product & Design
- [ ] Wireframe 7 màn hình đã được review và approve
- [ ] Design system (màu sắc, typography, spacing) đã được định nghĩa
- [ ] Prototype luồng chính (Home → Search → Compare → Buy) đã được user test

### Data & API
- [ ] Xác nhận khả năng truy cập API của Shopee/Lazada/Tiki (affiliate API, public API, hoặc backend aggregator)
- [ ] Xác định nguồn dữ liệu thành phần sản phẩm (INCI database, manual entry, hay OCR từ ảnh)
- [ ] Thiết kế backend aggregation service nếu dùng server-side caching
- [ ] Xác nhận deep-link URI schemes còn hoạt động với phiên bản app TMĐT hiện tại

### Technical
- [ ] Chọn framework: Flutter hay React Native (khuyến nghị Flutter cho performance)
- [ ] Thiết lập CI/CD pipeline (build, test, deploy)
- [ ] Định nghĩa API contract giữa mobile app và backend
- [ ] Thiết lập analytics (Firebase Analytics hoặc tương đương)
- [ ] Xác nhận App Store / Google Play guidelines cho deep-link và affiliate redirect

### Legal
- [ ] Kiểm tra Terms of Service của Shopee/Lazada/Tiki về việc hiển thị giá và dữ liệu sản phẩm
- [ ] Chính sách bảo mật (Privacy Policy) đã được soạn thảo
- [ ] Xác nhận không vi phạm quy định về so sánh giá thương mại tại Việt Nam

---
