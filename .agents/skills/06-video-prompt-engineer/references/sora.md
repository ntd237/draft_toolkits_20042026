# Engine Reference — Sora (OpenAI)

## Đặc điểm chính
- Mạnh về tính trần thuật và vật lý cảnh; không có audio native đồng bộ như Veo 3 (tùy phiên bản) — âm thanh xử lý ở bước hậu kỳ, prompt tập trung hình ảnh.
- Ăn mô tả văn xuôi dày hơn là danh sách từ khóa rời.
- Hỗ trợ nhiều tỷ lệ/duration; bám config.

## Cấu trúc prompt khuyến nghị
1. Đoạn văn 3–5 câu, trần thuật theo thứ tự thời gian trong shot: bối cảnh → chủ thể → hành động → chi tiết chuyển động → khí chất hình ảnh.
2. Camera movement viết như một hành động của "người quay".
3. Kết bằng style block từ bible.

## Ví dụ khung
```
Dawn light fills a small Saigon café. <CHAR-01 identity> stands behind the
counter, pouring condensed milk into a glass. Steam curls upward as she
stirs. The camera drifts slowly from the doorway toward her hands.
Shallow depth of field, warm amber palette, shot on 35mm.
```

## Negative prompt gợi ý mặc định
`watermark, on-screen text, warped hands, inconsistent character, flickering`

## Lưu ý riêng
- Tránh viết dialogue trong prompt trừ khi xác nhận phiên bản hỗ trợ audio; dialogue để cho bước audio/hậu kỳ.
- Hành động phức tạp nhiều bước → ưu tiên diễn tả 1–2 hành động chính, bỏ chi tiết phụ.
