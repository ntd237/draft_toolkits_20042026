# Engine Reference — Kling (Kuaishou)

## Đặc điểm chính
- Mạnh về chuyển động tự nhiên (người đi, cử chỉ mặt); prompt hiệu quả khi **hành động rõ ràng và đo được**.
- Cấu trúc prompt dạng: subject + scene + motion + camera + aesthetic.
- Hỗ trợ text-to-video và image-to-video (dùng ảnh đầu làm keyframe → tăng nhất quán nhân vật).

## Cấu trúc prompt khuyến nghị
1. Subject: identity từ bible.
2. Scene: nơi chốn + thời điểm.
3. Motion: động từ cụ thể (walks toward, turns her head, lifts the cup) — tránh trạng thái tĩnh.
4. Camera: 1 cụm ngắn.
5. Aesthetic: style block.

## Ví dụ khung
```
<CHAR-01 identity> in a cozy Saigon café at dawn.
She walks slowly toward the window, then turns and smiles.
Camera: eye-level, slow dolly-in. Warm amber palette, soft morning light,
cinematic, 35mm.
```

## Negative prompt gợi ý mặc định
`deformed, blurry, distorted face, extra limbs, low quality, watermark, text`

## Lưu ý riêng
- Ưu tiên chế độ image-to-video khi cần giữ mặt/nhân vật khớp giữa các shot: ghi `notes` trong prompts.json là "dùng keyframe từ ảnh CHAR-01".
- Chuyển động camera mạnh quá dễ gây méo — mặc định dolly/pan chậm.
