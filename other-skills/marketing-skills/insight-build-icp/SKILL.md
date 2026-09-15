---
name: insight-build-icp
description: "Xây dựng chân dung khách hàng mục tiêu đa chiều (Ideal Customer Profile - ICP) và 2-4 persona cards chuyên sâu (nhân khẩu học, tâm lý học, Jobs-to-be-Done, rào cản mua hàng, tiêu chí ra quyết định). Kích hoạt khi nhận brief khách hàng mới hoặc yêu cầu xây dựng/chuẩn hóa ICP. Đầu ra lưu tại docs/marketing-projects/<client-slug>/insight/icp.md."
---

# insight-build-icp: Xây Dựng Chân Dung Khách Hàng Mục Tiêu Đa Chiều

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Kích hoạt khi người dùng cung cấp brief khách hàng mới, yêu cầu "xây ICP", "phác thảo chân dung khách hàng", "nghiên cứu đối tượng mục tiêu", hoặc khi bắt đầu phân kỳ Insight trong chiến dịch mới.

## Workflow

### Giai đoạn 1: Khai thác Dữ liệu Khách hàng & Ngữ cảnh Doanh nghiệp
**Mục tiêu**: Thu thập các nguồn dữ liệu đầu vào theo `client_context` từ `config.md`.
- Trích xuất thông tin sản phẩm, ngành hàng, mô hình kinh doanh (B2B/B2C/D2C), phân khúc giá từ `campaign-plan.md` hoặc brief của người dùng.
- Thu thập dữ liệu thứ cấp sẵn có: lịch sử bán hàng, phản hồi của đội ngũ sales/CSKH, review của khách hàng trên sàn/social, và phỏng vấn người dùng nếu có.
- Xác định số lượng persona cần lập: từ 2 đến 4 persona theo ngưỡng `persona_count_range` trong Validation Policy của `config.md`.

### Giai đoạn 2: Phân tích Đa chiều & Mô hình Hóa JTBD
**Mục tiêu**: Bóc tách tâm lý, động lực và hành vi mua hàng của từng phân khúc.
- Phân tích nhân khẩu học & đặc điểm nhận diện: độ tuổi, giới tính, khu vực địa lý, thu nhập, chức danh/quy mô công ty (nếu B2B).
- Phân tích tâm lý học (Psychographics): giá trị sống, nỗi sợ tiềm ẩn, khát vọng, niềm tin và lối sống.
- Áp dụng khung Jobs-to-be-Done (JTBD):
  - Việc cốt lõi cần hoàn thành (Functional Job).
  - Cảm xúc mong muốn đạt được (Emotional Job).
  - Vị thế xã hội mong muốn khẳng định (Social Job).
- Xác định rào cản mua hàng (Purchasing Friction) và tiêu chí ra quyết định (Decision Criteria).

### Giai đoạn 3: Tổng hợp Deliverable & Trình duyệt Insight Gate
**Mục tiêu**: Xuất tài liệu ICP chuẩn hóa và lưu trữ theo Naming Policy trong `config.md`.
- Định dạng toàn bộ nội dung thành file `docs/marketing-projects/<client-slug>/insight/icp.md`.
- Trình bày tóm tắt các phát hiện quan trọng và yêu cầu người dùng xác nhận thông qua Insight Gate trước khi chuyển tiếp dữ liệu sang nhóm Content và Ads.

## Output Format
Tệp deliverable được ghi tại `docs/marketing-projects/<client-slug>/insight/icp.md`:

```markdown
# Hồ Sơ Chân Dung Khách Hàng Mục Tiêu (ICP) — <client_name>
- Client Slug: `<client-slug>`
- Ngành hàng: <industry>
- Ngày lập: <YYYY-MM-DD>

## 1. Tổng Quan ICP & Phân Khúc Cốt Lõi
- Định nghĩa tệp khách hàng lý tưởng mang lại LTV cao nhất và chi phí chuyển đổi tối ưu.

## 2. Danh Sách Persona Cards (2 - 4 Persona)

### Persona 1: <Tên đại diện> — <Đặc trưng cốt lõi>
- **Nhân khẩu học**: Độ tuổi, giới tính, nghề nghiệp/chức vụ, thu nhập, địa lý.
- **Tâm lý & Lối sống**: Giá trị theo đuổi, sở thích, kênh truyền thông tin cậy.
- **Khung Jobs-to-be-Done (JTBD)**:
  - Functional Job: <Công việc chức năng cần giải quyết>
  - Emotional Job: <Cảm giác mong muốn đạt được>
  - Social Job: <Cách họ muốn người khác nhìn nhận>
- **Pain Points & Trăn trở lớn nhất**: <Vấn đề nhức nhối chưa được giải quyết tốt>
- **Rào cản & Lý do từ chối mua hàng**: <Nghi ngại về giá, uy tín, độ phức tạp>
- **Trigger mua hàng & Điểm chạm chuyển đổi**: <Sự kiện kích hoạt hành vi tìm kiếm giải pháp>
- **Thông điệp truyền thông then chốt (Key Value Proposition)**: <Thông điệp đánh trúng tâm lý>

(Lặp lại cấu trúc cho Persona 2, 3...)

## 3. Khuyến Nghị Ứng Dụng Vào Content & Performance Ads
- Hướng dẫn angle nội dung và targeting cho từng persona.
```

## Don'ts
- Không tạo persona chung chung, sáo rỗng thiếu dữ liệu hành vi thực tế (tránh mô tả kiểu "người thích mua sắm online").
- Không vượt quá 4 persona để tránh gây phân mảnh nguồn lực ngân sách và nội dung.
- Không tự suy đoán giá trị nhân khẩu học mà không gắn liền với mô hình kinh doanh và mức giá của client.
- Không đóng persona trước khi người dùng xác nhận đạt Insight Gate.

## Quality Checklist
- [ ] Số lượng persona nằm trong khoảng 2 đến 4 theo đúng Validation Policy trong `config.md`.
- [ ] Mỗi persona có đầy đủ 3 thành phần JTBD (Functional, Emotional, Social).
- [ ] Có danh sách cụ thể về pain points, rào cản mua hàng và trigger chuyển đổi.
- [ ] File deliverable được lưu đúng đường dẫn `docs/marketing-projects/<client-slug>/insight/icp.md`.
