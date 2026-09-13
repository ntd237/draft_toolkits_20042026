---
name: vn-stock-weekend-news
description: "Tổng hợp tin tức tài chính cuối tuần (thứ 6, thứ 7, chủ nhật) bao gồm vĩ mô thế giới, vĩ mô & chính sách dòng tiền Việt Nam (SBV, OMO, tỷ giá, lãi suất) và tin doanh nghiệp; phân tích đánh giá tác động tới VN-Index và nhóm cổ phiếu/ngành trong tuần giao dịch kế tiếp."
---

# Weekend Financial News & Stock Impact Synthesizer

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng yêu cầu tổng hợp tin tức tài chính cuối tuần (thứ 6, thứ 7, chủ nhật), đánh giá biến động vĩ mô/chính sách dòng tiền gần nhất của Việt Nam & thế giới, hoặc phân tích tác động của tin tức cuối tuần tới thị trường chứng khoán Việt Nam (VN-Index) và các mã cổ phiếu trong tuần mới.

## Workflow

### Phase 1: Thu thập & Lọc Tin tức Theo Mốc Thời Gian
**Objective**: Thu thập và xác minh dữ liệu tin tức được công bố chính xác trong khung thời gian từ thứ 6 đến hết ngày chủ nhật của tuần gần nhất kèm đường dẫn URL gốc.
- Xác định mốc thời gian 3 ngày cuối tuần gần nhất (Thứ 6, Thứ 7, Chủ Nhật) dựa trên thời gian thực tế hiện tại.
- Truy vấn và đối chiếu dữ liệu từ các nguồn tài chính chính thống, lưu giữ đầy đủ đường link URL bài viết gốc:
  - Vĩ mô & chính sách Việt Nam: Cổng TTĐT Chính phủ, Ngân hàng Nhà nước (SBV), Bộ Tài chính, Tổng cục Thống kê (GSO).
  - Tin tức thị trường & doanh nghiệp: Báo Đầu tư, Vietstock, CafeF, VnEconomy, FiinPro, Sở GDCK (HOSE, HNX).
  - Vĩ mô & hàng hóa quốc tế: Bloomberg, Reuters, Investing.com, Trading Economics, U.S. Bureau of Labor Statistics.
- Loại bỏ các tin đồn vô căn cứ, bài viết lặp lại hoặc tin tức đã phản ánh hoàn toàn vào phiên giao dịch từ thứ 5 trở về trước.

### Phase 2: Phân Loại Dữ Liệu Theo 4 Trụ Cột Tài Chính
**Objective**: Phân loại các thông tin đã thu thập vào 4 nhóm trọng tâm để chuẩn bị cho bước đánh giá tác động.
- **Trụ cột 1 - Vĩ mô Quốc tế**: Quyết định lãi suất/biên bản họp FED, biến động chỉ số DXY, lợi suất trái phiếu Mỹ (US 10Y), giá hàng hóa chủ chốt (Dầu Brent/WTI, Thép HRC, Quặng sắt, Vàng XAU/USD, Phân bón), diễn biến các chỉ số chứng khoán lớn (Dow Jones, S&P 500, Nikkei 225, Shanghai).
- **Trụ cột 2 - Vĩ mô & Chính sách Tiền tệ/Tài khóa Việt Nam**: Động thái bơm/hút ròng qua OMO/Tín phiếu của SBV, biến động tỷ giá USD/VND (liên ngân hàng, chợ đen, NHTM), lãi suất liên ngân hàng, room tín dụng, chỉ đạo điều hành lãi suất huy động/cho vay, giải ngân vốn đầu tư công và các chính sách thuế.
- **Trụ cột 3 - Sự kiện & Tin tức Doanh nghiệp/Ngành**: Ước tính/công bố KQKD, kế hoạch chia cổ tức, phát hành tăng vốn/bán vốn ngoại, trúng thầu dự án lớn, thông tin biến động nhân sự cấp cao, kết luận thanh tra/pháp lý hoặc các vụ án kinh tế liên quan.
- **Trụ cột 4 - Trạng thái Dòng tiền & Tâm lý Thị trường**: Trạng thái mua/bán ròng của khối ngoại và tự doanh trong phiên thứ 6, thanh khoản tuần, mức độ đòn bẩy margin toàn thị trường và tâm lý nhà đầu tư cá nhân sau chuỗi tin cuối tuần.

### Phase 3: Đánh Giá Cơ Chế Truyền Dẫn & Ma Trận Tác Động
**Objective**: Phân tích định tính và định lượng tác động nhiều chiều của từng nhóm tin tức tới VN-Index, các nhóm ngành và mã cổ phiếu cụ thể theo logic kinh tế.
- Tra cứu cơ chế truyền dẫn chính sách và tỷ giá tại `references/macro_policy_framework.md` để đánh giá tác động vĩ mô.
- Tra cứu bảng liên kết ngành và cổ phiếu đại diện tại `references/stock_impact_matrix.md` để gắn mã chứng khoán (Ticker) tương ứng.
- Đánh giá mức độ tác động theo 3 cấp độ chuẩn:
  - 🟢 **Tích cực (Bullish Catalyst)**: Hỗ trợ tăng giá hoặc kích hoạt dòng tiền vào ngành/cổ phiếu.
  - 🔴 **Tiêu cực (Bearish Catalyst)**: Tạo áp lực điều chỉnh, rút vốn hoặc suy giảm biên lợi nhuận.
  - 🟡 **Trung tính / Cần theo dõi (Neutral / Watchlist)**: Tác động đa chiều, cần kiểm chứng phản ứng cung cầu phiên thứ 2.
- Làm rõ tính hai mặt của sự kiện (ví dụ: Tỷ giá tăng tích cực cho nhóm xuất khẩu như Thủy sản/Dệt may nhưng tiêu cực cho doanh nghiệp vay nợ USD lớn và kích hoạt khối ngoại bán ròng).

### Phase 4: Tổng Hợp Bản Tin Chiến Lược Đầu Tuần Kèm URL Trích Nguồn
**Objective**: Định dạng bản tin cô đọng dạng Bullet-points phân cấp rõ ràng, đính kèm link URL nguồn thực tế tại từng mục tin để người dùng kiểm chứng.
- Trình bày tóm tắt theo cấu trúc chuẩn trong phần Output Format.
- Đính kèm đường link nguồn bài viết dạng Markdown `([Tên nguồn / Tiêu đề](URL))` ngay tại mỗi đầu mục tin tức.
- Nêu rõ 2 kịch bản vận động khả dĩ của VN-Index trong tuần mới (Kịch bản cơ sở và Kịch bản thận trọng) kèm mốc kháng cự/hỗ trợ then chốt.
- Liệt kê danh mục cổ phiếu/nhóm ngành tâm điểm cần ưu tiên theo dõi hoặc phòng thủ.

## Output Format

Bản tin được xuất trực tiếp ra màn hình phản hồi theo cấu trúc Bullet-points phân cấp sau:

```markdown
# 📊 BẢN TIN TÀI CHÍNH CUỐI TUẦN & TÁC ĐỘNG TTCK TUẦN MỚI
*(Khung thời gian tin tức: [Ngày Thứ 6] đến [Ngày Chủ Nhật])*

---

### 1. 🌐 Vĩ Mô Toàn Cầu & Hàng Hóa
- **[Tên sự kiện / Chỉ số quốc tế]**: [Nội dung tóm tắt số liệu] — *(Nguồn: [Tên nguồn / Tiêu đề bài viết](URL))*
  - *Tác động*: [🟢 Tích cực / 🔴 Tiêu cực / 🟡 Trung tính] - [Phân tích ngắn gọn cơ chế ảnh hưởng tới tâm lý chung].
- **[Biến động giá hàng hóa (Dầu / Thép / Vàng...)]**: [Tỷ lệ tăng/giảm + Xu hướng] — *(Nguồn: [Tên nguồn](URL))*
  - *Nhóm ngành ảnh hưởng*: [Mã cổ phiếu hưởng lợi / chịu rủi ro].

---

### 2. 🏛️ Vĩ Mô, Chính Sách Dòng Tiền & Tỷ Giá Việt Nam
- **[Động thái NHNN / Thanh khoản hệ thống]**: [Hút/bơm ròng OMO, Tín phiếu, Lãi suất LNH] — *(Nguồn: [SBV / Báo chí](URL))*
  - *Tác động dòng tiền*: [Tác động lên thanh khoản và định giá thị trường chung].
- **[Diễn biến Tỷ giá & Dự trữ ngoại hối]**: [Biến động USD/VND, động thái mua/bán ngoại tệ] — *(Nguồn: [Tên nguồn](URL))*
  - *Tác động*: [Tác động tới dòng vốn khối ngoại và chi phí tài chính doanh nghiệp].
- **[Chính sách tài khóa / Đầu tư công / BĐS]**: [Nghị quyết, công điện, văn bản pháp lý mới] — *(Nguồn: [Báo Chính phủ / Cổng TTĐT](URL))*
  - *Nhóm hưởng lợi*: [Ngành / Mã cổ phiếu liên quan trực tiếp].

---

### 3. 🏢 Điểm Tin Doanh Nghiệp & Nhóm Ngành
- **[Nhóm Ngành A (Ngân hàng / BĐS / Thép...)]**:
  - `MÃ_CP`: [Tóm tắt tin tức: KQKD / Cổ tức / Tăng vốn / Hợp đồng / Pháp lý] — *(Nguồn: [CafeF / Vietstock / FiinPro](URL))*
    - *Đánh giá*: [🟢/🔴/🟡] [Tác động ngắn hạn tới giá cổ phiếu và điểm cần lưu ý].
- **[Nhóm Ngành B]**:
  - `MÃ_CP`: [Tóm tắt sự kiện doanh nghiệp] — *(Nguồn: [Tên nguồn](URL))*
    - *Đánh giá*: [🟢/🔴/🟡] [Tác động ngắn hạn].

---

### 4. 🧭 Kịch Bản VN-Index & Chiến Lược Hành Động Tuần Mới
- **Xu hướng dòng tiền & Tâm lý**: [Tóm tắt tương quan giữa tin tức tích cực vs tiêu cực].
- **Kịch bản thị trường**:
  - 📈 *Kịch bản cơ sở (Tỷ xác suất %)*: [Dự kiến vùng điểm số, phản ứng trước chuỗi tin tức].
  - 📉 *Kịch bản thận trọng (Tỷ xác suất %)*: [Vùng hỗ trợ cần quản trị rủi ro nếu áp lực bán xuất hiện].
- **Danh mục cổ phiếu tâm điểm**:
  - 🚀 *Tiềm năng thu hút dòng tiền*: `MÃ 1`, `MÃ 2` ([Lý do ngắn gọn]).
  - ⚠️ *Cần thận trọng / Quản trị rủi ro*: `MÃ 3`, `MÃ 4` ([Lý do ngắn gọn]).
```

## Don'ts
- Không bỏ sót đường dẫn URL trích nguồn hoặc bịa đặt đường link giả mạo (hallucinated URL).
- Không thu thập hoặc tổng hợp các tin tức phát hành ngoài khung thời gian Thứ 6 - Chủ Nhật gần nhất, trừ khi có mối liên kết nhân quả trực tiếp giải thích cho sự kiện cuối tuần.
- Không đưa tin đồn mạng xã hội, tin hành lang chưa được kiểm chứng từ các cơ quan quản lý hoặc báo chí chính thống.
- Không đưa ra lời khuyên đầu tư mang tính cam kết lợi nhuận, phím lệnh mua/bán tuyệt đối hoặc khẳng định chắc chắn 100% hướng đi của giá cổ phiếu.
- Không đưa ra nhận định chung chung, sáo rỗng mà thiếu mã cổ phiếu (Ticker) cụ thể hoặc thiếu cơ chế truyền dẫn kinh tế.
- Không tự ý ghi đè hay tạo các file mã nguồn/file dữ liệu trên ổ đĩa trừ khi người dùng có chỉ định rõ ràng (Chế độ Read-only mặc định).
- Không bịa đặt số liệu tài chính, tỷ lệ tăng trưởng hoặc nội dung văn bản điều hành của NHNN/Chính phủ.

## Quality Checklist
- [ ] Mọi tin tức vĩ mô, chính sách và sự kiện doanh nghiệp đều có đường dẫn URL trích nguồn thực tế để người dùng trực tiếp rà soát và kiểm chứng.
- [ ] Khung thời gian tin tức đã được xác định chính xác trong khoảng Thứ 6 - Thứ 7 - Chủ Nhật của tuần gần nhất.
- [ ] Phân loại đầy đủ 4 trụ cột: Vĩ mô quốc tế, Vĩ mô/Chính sách tiền tệ Việt Nam, Tin tức doanh nghiệp, và Kịch bản VN-Index.
- [ ] Động thái chính sách tiền tệ (SBV, OMO, Tín phiếu, Tỷ giá, Lãi suất) được phân tích rõ ràng theo `references/macro_policy_framework.md`.
- [ ] Mỗi sự kiện tin tức đều được gắn mã cổ phiếu (Ticker) cụ thể và xếp hạng tác động (🟢/🔴/🟡) theo `references/stock_impact_matrix.md`.
- [ ] Trình bày chuẩn định dạng Bullet-points phân cấp, súc tích, không lan man lý thuyết.
- [ ] Không chứa lời cam kết đầu tư tài chính hay phím lệnh tuyệt đối vi phạm nguyên tắc an toàn.
- [ ] File tham chiếu `references/macro_policy_framework.md` và `references/stock_impact_matrix.md` đều tồn tại và dưới 300 dòng.
