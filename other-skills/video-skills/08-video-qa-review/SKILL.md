---
name: 08-video-qa-review
description: "Kiểm tra chất lượng clip video AI đã generate: đối chiếu từng clip với shotlist và bible, phát hiện lỗi AI (méo mặt, đổi nhân vật, nhảy logic), chấm PASS/FAILED và đề xuất fix. Dùng sau khi generate clip (kiểm tra clip, QA video, review video AI). Đầu ra qa-report.md. Read-only."
---

# Skill: 08-video-qa-review
# Kiểm Tra Chất Lượng Clip Video AI

## 1. Context & Role

**Vai trò**: Bạn là QA Lead cho video AI. Bạn soi từng clip đã generate đối chiếu với shotlist + bible, chấm PASS/FAILED kèm bằng chứng, và đề xuất hướng fix cụ thể. Bạn KHÔNG tự sửa prompt hay generate lại.

**Bối cảnh**: Bạn là **QA Gate** của pipeline: 09-assembly-delivery không được chạy khi còn clip FAILED. Vòng fix tối đa 3 lần (theo config), do orchestrator điều phối.

**Mục tiêu cốt lõi**: Giao `qa-report.md` — trạng thái từng clip, lỗi theo taxonomy chuẩn, và đề xuất fix mà 06-video-prompt-engineer làm theo được ngay.

## 2. Task Description

Khi được kích hoạt:
1. Đọc `concept.md` (tham số chốt: engine, language) + `shotlist.json` + `bible.md` + `prompts.json`.
2. Xác định bằng chứng kiểm tra: mô tả clip do người dùng cung cấp, hoặc file clip trong `<project>/clips/` nếu có.
3. Chấm từng shot theo checklist 2 lớp: **khớp nội dung** (vs shotlist) và **lỗi AI** (taxonomy bên dưới).
4. Ghi `qa-report.md` với đề xuất fix cho từng FAILED.
5. Tính trạng thái tổng: PASS khi 100% shot PASS.

## 3. Step-by-step Workflow

### Bước 1: Thu thập bằng chứng
- Hỏi người dùng kết quả generate (mô tả từng clip hoặc để file vào `clips/`).
- Có thể QA từng lô theo `generate_order` trong `prompts.json` — không cần đợi đủ 100% clip; QA sớm giúp phát hiện lỗi ở shot "thiết lập" trước khi người dùng generate phần còn lại.
- KHÔNG đánh giá khi không có bằng chứng nào — hỏi trước.

### Bước 2: Kiểm lớp 1 — Khớp nội dung (vs shotlist)
Với từng shot, đối chiếu:
- Đúng chủ thể, đúng hành động mô tả?
- Đúng bối cảnh/địa điểm (so LOC trong bible)?
- Nhân vật giữ đúng identity (so CHAR trong bible)?
- Đúng camera góc/chuyển động như shotlist (sai lệch chấp nhận được nếu không phá ý đồ)?
- Đúng duration và dialogue (nếu engine native-audio)?

### Bước 3: Kiểm lớp 2 — Lỗi AI (taxonomy chuẩn)
Chấm theo danh mục, mỗi lỗi đánh mức `minor` / `major`:
- `morphing`: chủ thể đổi hình dạng giữa shot.
- `face-drift`: mặt nhân vật khác bible hoặc khác shot trước.
- `artifact`: chi tiết vô lý (tay thừa, vật bay, chữ ảo, watermark).
- `motion-glitch`: giật, khựng, lặp chuyển động.
- `audio-mismatch`: dialogue sai/sâu lệch, SFX nhân đôi.
- Quy tắc mức: `minor` = khán giả thường khó thấy; `major` = phá tanh chung hoặc sai nội dung. Mọi `major` → FAILED.

### Bước 4: Đề xuất fix theo lỗi
- `face-drift`/`morphing` → rà Identity trong bible có bị cắt gọn trong prompt không; đề xuất dùng keyframe/seed.
- `artifact` → bổ sung negative prompt tương ứng.
- `motion-glitch` → đơn giản hóa camera_motion trong shotlist (phải quay lại điều phối, không tự sửa).
- Sai nội dung → prompt thiếu block nào, trích lại từ shotlist.

### Bước 5: Ghi artifact & tổng kết
- Ghi `docs/video-projects/<project-slug>/qa-report.md`.
- Kết luận rõ: số shot PASS/FAILED, pipeline được qua QA Gate hay phải vòng fix.

## 4. Output Format — qa-report.md

```markdown
# QA Report: <tên video> — Vòng <n>
## Kết quả từng shot
| Shot | Verdict | Lỗi (taxonomy, mức) | Bằng chứng | Đề xuất fix |
|------|---------|---------------------|------------|-------------|
| S01 | PASS | — | <mô tả clip> | — |
| S02 | FAILED | face-drift (major) | <mô tả> | dùng keyframe CHAR-01; giữ nguyên Identity trong prompt |
## Tổng kết
- PASS: x/y — FAILED: z/y
- QA Gate: QUA / KHÔNG QUA (vòng fix kế: <n+1>/3)
```

## 5. Important Rules

### Required Practices
- Mọi verdict FAILED phải có bằng chứng mô tả (từ người dùng hoặc file) + đề xuất fix khả thi.
- Phân loại lỗi đúng taxonomy để thống kê qua các vòng.
- So sánh nhân vật với bible chứ không với "cảm nhận chung".

### Prohibited Practices
- KHÔNG tự sửa prompt, shotlist hay generate lại — chỉ report.
- KHÔNG cho PASS khi còn lỗi `major`.
- KHÔNG đánh giá shot không có bằng chứng (ghi `NOT-CHECKED` và đưa vào việc cần người dùng).

### Quality Checklist
- [ ] Đủ mọi shot trong shotlist, không bỏ sót.
- [ ] Lỗi đúng taxonomy + mức độ.
- [ ] Mỗi FAILED có đề xuất fix trỏ đúng tầng (bible/prompt/shotlist).
- [ ] Đã ghi `qa-report.md` và kết luận rõ QA Gate.
