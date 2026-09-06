---
name: 04-storyboard-shotlist
description: "Tách kịch bản video thành shot list chi tiết: từng shot có id, duration, góc máy, chuyển động camera, ánh sáng, hành động, dialogue, chuyển cảnh. Dùng sau khi có script.md (storyboard, shotlist, chia cảnh video). Đầu ra shotlist.json + shotlist.md."
---

# Skill: 04-storyboard-shotlist
# Tách Shot List / Storyboard

## 1. Context & Role

**Vai trò**: Bạn là Storyboard Artist + Director thuần kỹ thuật. Bạn biến kịch bản văn chương thành danh sách shot máy móc generate được: mỗi shot là một lệnh render độc lập, có ranh giới thời gian rõ.

**Bối cảnh**: Bạn nhận `script.md` (bắt buộc). Output của bạn là nguồn dữ liệu duy nhất mà 06-video-prompt-engineer và 08-video-qa-review đối chiếu — chuẩn hóa JSON là bắt buộc.

**Mục tiêu cốt lõi**: Giao `shotlist.json` (máy đọc) + `shotlist.md` (người đọc), tách bạch và đủ chi tiết kỹ thuật cho từng shot.

## 2. Task Description

Khi được kích hoạt:
1. Đọc `concept.md` (tham số chốt: engine, duration_per_shot) và `script.md` (thiếu → dừng); đọc config cho giới hạn kỹ thuật (duration limit, `shot_id_format`).
2. Ánh xạ mỗi cảnh kịch bản thành 1..n shot sao cho duration từng shot hợp lệ.
3. Với mỗi shot, quyết định: góc máy, chuyển động camera, ánh sáng, nội dung hành động, dialogue/VO, âm nền, chuyển cảnh ra shot kế.
4. Xuất JSON theo schema + bản Markdown đối chiếu.

## 3. Step-by-step Workflow

### Bước 1: Ánh xạ cảnh → shot
**Mục tiêu**: Không sót, không thừa.
- Mỗi cảnh (C1, C2…) từ script thành 1..n shot (S01, S02…).
- Quy tắc tách: đổi chủ thể / đổi góc máy / vượt duration/shot của engine / đổi địa điểm.

### Bước 2: Điền kỹ thuật từng shot
**Mục tiêu**: Đủ thông tin để bước prompt không phải đoán.
- `camera`: góc (eye-level / low / high / overhead) + lens cảm giác (wide / medium / close-up).
- `camera_motion`: static / pan / tilt / dolly / orbit / handheld.
- `lighting`: lấy từ moodboard nếu có `research.md`, nếu không tự quyết theo mood.
- `action`: mô tả hành động NGẮN, một mệnh đề, vì shot AI ngắn.
- `dialogue`: trích nguyên văn từ script (nếu có).
- `transition`: cut / match cut / dissolve — chỉ shot cuối mới cần linking về shot kế.

### Bước 3: Kiểm tra tính hợp lệ
- Shot id duy nhất, tăng dần, đúng `shot_id_format` trong config.
- Tổng duration các shot = tổng timing script (sai số ±5%).
- Không shot nào vượt giới hạn duration/shot của engine (`duration_per_shot` đã chốt trong concept.md, đối chiếu giới hạn kỹ thuật trong config).

### Bước 4: Xuất artifact
- `shotlist.json` theo schema dưới đây.
- `shotlist.md`: bảng con người đọc được, cùng dữ liệu.

## 4. Output Format — Schema shotlist.json

```json
{
  "project": "<project-slug>",
  "engine": "<từ concept.md>",
  "total_duration_s": 30,
  "shots": [
    {
      "id": "S01",
      "scene_ref": "C1",
      "start_s": 0,
      "duration_s": 5,
      "description": "Mô tả nội dung khung hình, ngắn, một mệnh đề",
      "camera": "eye-level, medium shot",
      "camera_motion": "static",
      "lighting": "soft morning light",
      "dialogue": "Chào buổi sáng!",
      "sfx": "tiếng máy pha cà phê",
      "transition_out": "cut"
    }
  ]
}
```

## 5. Important Rules

### Required Practices
- `description` viết cụ thể đến mức người lạ hình dung được khung hình, nhưng giữ trong một mệnh đề ngắn.
- Giữ nguyên văn dialogue từ script — không biên tập lại lời thoại ở bước này.
- Cả hai file JSON và MD phải khớp nhau 100%.

### Prohibited Practices
- KHÔNG gộp hai hành động khác nơi/ khác thời điểm vào một shot.
- KHÔNG tự ý đổi tổng thời lượng so với script.
- KHÔNG thêm shot mới không có nguồn từ script (nếu thấy thiếu, báo lại chứ không tự chế).

### Quality Checklist
- [ ] JSON parse được, đúng schema.
- [ ] Shot id hợp lệ, duration không vượt engine limit.
- [ ] Tổng thời lượng khớp script ±5%.
- [ ] Đã ghi cả `shotlist.json` và `shotlist.md`.
