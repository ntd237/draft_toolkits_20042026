# Engine Reference — Veo 3 (Google)

## Đặc điểm chính
- Hỗ trợ **audio native**: dialogue, SFX, ambient có thể viết thẳng trong prompt.
- Ngoài ra hiểu mô tả cinematic chi tiết (lens, ánh sáng, pacing).
- Thường giới hạn ~8s mỗi clip — luôn xác nhận với config `duration_per_shot`.

## Cấu trúc prompt khuyến nghị
1. Câu mở: mô tả cảnh + chủ thể đang làm gì (hiện tại tiếp diễn).
2. Dialogue: viết trong ngoặc kép kèm only speaks / says — nêu rõ ngôn ngữ nếu không phải tiếng Anh (VD: `speaking Vietnamese`).
3. Camera & ánh sáng: một câu.
4. Audio: `Audio: <ambient/SFX/mood nhạc>`.
5. Style keywords cuối câu (35mm, cinematic, ...).

## Ví dụ khung
```
In a cozy Saigon café at dawn, <CHAR-01 identity>, <action>.
She says in Vietnamese: "Chào buổi sáng!" — warm, unhurried tone.
Camera: eye-level medium shot, slow dolly-in. Soft morning light through
blinds. Audio: coffee machine hiss, lo-fi ambience. Shot on 35mm, cinematic.
```

## Negative prompt gợi ý mặc định
`subtitles, captions, watermark, distorted face, extra fingers, morphing, text overlay`

## Lưu ý riêng
- Nếu không muốn engine tự sinh chữ trên màn hình → luôn đưa `subtitles/captions` vào negative.
- Dialogue dài quá 2 câu → tách shot.
