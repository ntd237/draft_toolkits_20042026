# Engine Reference — Runway Gen-4

## Đặc điểm chính
- Đầu vào chính là **image-to-video**: cần ảnh keyframe (ảnh tĩnh của khung cảnh/nhân vật) làm điểm xuất phát; prompt chỉ mô tả CHUYỂN ĐỘNG từ ảnh đó.
- Prompt ngắn, tập trung motion — viết dài mô tả hình ảnh là lãng phí vì hình đã có từ keyframe.
- Nhất quán nhân vật tốt nhất khi dùng chung ảnh tham chiếu qua các shot.

## Cấu trúc prompt khuyến nghị
1. Câu 1: chuyển động chính của chủ thể (động từ + hướng + tốc độ).
2. Câu 2: chuyển động camera.
3. (Tuỳ chọn) câu 3: hiệu ứng môi trường (tóc bay, khói lan, ánh sáng đổi).
- Giữ 1–3 câu, không mô tả lại hình dạng nhân vật/bối cảnh (đã nằm trong keyframe).

## Ví dụ khung
```
She lifts the glass and turns toward the window, unhurried.
Camera slowly dollies in, slight handheld drift.
Steam rises from the cup as morning light shifts across the counter.
```

## Negative prompt gợi ý mặc định
`warped face, morphing objects, jitter, flicker, text artifacts, watermark`

## Lưu ý riêng
- Trong `prompts.json`, mục `notes` PHẢI ghi rõ keyframe cần dùng: `"keyframe: ảnh CHAR-01 tại LOC-01"`.
- Nếu shot bắt đầu từ hành động giữa chừng (không hợp lý từ keyframe) → báo lại 04-storyboard-shotlist điều chỉnh mô tả shot thay vì bịa motion vô lý.
