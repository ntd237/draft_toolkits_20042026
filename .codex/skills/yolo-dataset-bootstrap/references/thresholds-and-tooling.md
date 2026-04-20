# Thresholds và Tooling

## Heuristic khởi điểm

Dùng các giá trị sau như điểm xuất phát, sau đó hiệu chỉnh lại bằng review trực quan:

- Seed set: `300-800` ảnh gán nhãn tay cho các bài toán detection điển hình
- Baseline training: `30-80` epochs cho YOLO bootstrap model đầu tiên
- Confidence triage:
  - `> 0.6`: accept hoặc fast-pass
  - `0.3-0.6`: đưa vào hàng review tay
  - `< 0.3`: bỏ qua, để lại sau hoặc review có chọn lọc
- QA sample cho phần auto-accepted: `5-10%`
- Số vòng active learning: `2-3`

## Khi nào nên siết threshold

Dùng ngưỡng accept chặt hơn và tăng review tay khi:

- Class có tính quan trọng cao hoặc nhạy cảm
- False positive gây tốn kém
- Object quá nhỏ hoặc bị che khuất nhiều
- Cảnh đông
- Model có xu hướng over-detect trên các background nhiều chi tiết

## Khi nào nên tăng seed set

Tăng kích thước batch gán nhãn tay ban đầu khi:

- Có nhiều class
- Các class long-tail quan trọng
- Điều kiện camera biến thiên mạnh
- Ánh sáng và background thay đổi nhiều
- Các edge case hiếm có ảnh hưởng đáng kể trong môi trường thực tế

## Chọn tool

- **CVAT**: Lựa chọn toàn diện nhất khi cần auto-annotation đi kèm review có cấu trúc
- **Label Studio**: Phù hợp nhất khi cần ghép pipeline linh hoạt
- **Roboflow Auto Label**: Phù hợp nhất khi ưu tiên tốc độ và ít setup hơn độ nhạy cảm về chi phí
