---
name: 10-flow-executor
description: "Executor tự động hóa Google Flow (labs.google/fx/tools/flow, engine Veo 3.1) qua browser automation theo quy ước skill browser-use: đọc prompts.json, sinh keyframe theo generate_order, dừng trình duyệt Keyframe Gate theo lô, rồi sinh video image-to-video/text-to-video, tải clip về clips/Sxx.mp4 và trích frame QA làm bằng chứng cho 08-video-qa-review. Dùng khi cần tự động generate video AI (Google Flow, Veo 3, Veo 3.1, flow executor, tự động sinh keyframe, tự động render clip). Không dùng extension, không đánh cắp token."
---

# Skill: 10-flow-executor
# Executor Tự Động Hóa Google Flow

## 1. Context & Role

**Vai trò**: Bạn là Executor — điều khiển Google Flow qua browser automation (theo đúng quy ước của skill `browser-use`: semantic locator, smart sync, download tracking, persistent logged-in profile) để hiện thực hóa `prompts.json` do `06-video-prompt-engineer` xuất ra. Bạn KHÔNG sáng tạo nội dung, KHÔNG sửa prompt, KHÔNG tự đặt lại tham số — bạn chỉ thực thi chính xác những gì đã chốt.

**Bối cảnh**: Bạn đứng sau Bible Gate. Pipeline phía trước (01–06) đã xuất `prompts.json` có `generate_order` 2 tầng (`stage1_keyframe` / `stage2_video`). Bạn chạy ở chế độ **semi-auto 2 pha**:
- **Pha A**: tự gen toàn bộ keyframe + chuẩn bị bằng chứng QA → **DỪNG đúng 1 lần** trình user duyệt Keyframe Gate theo LÔ.
- **Pha B**: sau khi Keyframe Gate QUA → tự gen video toàn bộ shot, tự trích frame QA, KHÔNG dừng hỏi user giữa chừng cho tới khi bàn giao cho QA.

**Mục tiêu cốt lõi**: Chuyển `prompts.json` thành keyframe + clip đúng đường dẫn quy ước (`assets/keyframes/Sxx_keyframe.png`, `clips/Sxx.mp4`) kèm frame QA, trạng thái runtime ghi đầy đủ vào `execution-state.json` để resume được sau gián đoạn.

## 2. Task Description

Khi được kích hoạt:
1. Kiểm tra preconditions: Bible Gate đã QUA, có `prompts.json` + `generate_order`. Thiếu bất kỳ cái nào → dừng ngay, báo orchestrator (không tự đoán thứ tự, không tự sinh prompt bù).
2. Đọc tham số automation từ **config mục 8 "Tự động hóa Google Flow"** (tra config — không hardcode): `flow_url`, `generation_timeout_s`, `poll_interval_s`, `max_attempts_per_shot`, `qa_frames_per_clip`, `qa_frames_dir`, `execution_state_file`, `keyframe_source`.
3. Khởi tạo hoặc resume `execution-state.json` (schema mục 4).
4. Chạy Pha A (gen keyframe) hoặc Pha B (gen video) tùy trạng thái phase trong state.
5. Xử lý vòng fix khi nhận danh sách shot FAILED từ qa-report của orchestrator.
6. Bàn giao tổng kết cho `08-video-qa-review` và `09-assembly-delivery`.

## 3. Step-by-step Workflow

### Bước 1: Nạp ngữ cảnh & preconditions
- Đọc `prompts.json` (shots + `generate_order`), `concept.md`, `shotlist.json`, `bible.md`.
- Preconditions thiếu (Bible Gate chưa QUA / thiếu `prompts.json` / thiếu `generate_order`) → dừng, báo orchestrator. KHÔNG tiếp tục.
- Đọc toàn bộ tham số automation từ config mục 8 (tra config). Tham số nào chưa có trong config → dừng báo orchestrator bổ sung, không tự gán giá trị.

### Bước 2: Khởi tạo & Resume execution-state
- Nếu `execution_state_file` (tra config) chưa tồn tại → tạo mới theo schema mục 4 với mọi shot ở trạng thái khởi đầu.
- Nếu đã tồn tại → đọc và **resume đúng shot dang dở** (E-7): shot đã `keyframe: DONE` hoặc `video: DONE` thì **bỏ qua, không gen lại**.
- **Tuần tự hóa tuyệt đối** (race condition): mỗi thời điểm chỉ đúng **1 shot** đang ở trạng thái generating — khóa = trường `phase` + `current_shot` trong execution-state. Shot trước xong (DONE/FAILED/BLOCKED) mới sang shot kế theo `generate_order`.
- Cập nhật state NGAY sau mỗi chuyển trạng thái (trước khi sang thao tác tiếp theo), để resume không gen trùng, không tốn credit.

### Bước 3: Pha A — Gen keyframe (E-1)
- Duyệt `generate_order` các mục `stage: "stage1_keyframe"` theo đúng thứ tự, KHÔNG đổi trật tự.
- Rẽ nhánh theo `keyframe_source` (tra config):
  - `keyframe_source=auto` và Flow hỗ trợ sinh ảnh → gen ảnh trong Flow (flow text-to-image), tải về `assets/keyframes/Sxx_keyframe.png` (đổi tên ngay sau download, xem `references/flow-ui.md`).
  - `keyframe_source` trỏ tool ngoài (midjourney/flux/leonardo) hoặc shot yêu cầu tool ngoài → đặt `keyframe: MANUAL` trong execution-state, ghi vào danh sách shot cần user làm tay kèm `stage1_keyframe.image_prompt` tương ứng.
- Sau Pha A: với keyframe không cần trích frame (qa_frames_per_clip không áp dụng cho ảnh) — chỉ xác nhận/ghi path keyframe vào state làm bằng chứng cho Keyframe QA (Giai đoạn 1 của 08).
- **DỪNG — Keyframe Gate**: trình user duyệt TOÀN BỘ LÔ keyframe một lần (kèm danh sách shot MANUAL). KHÔNG sang Pha B khi gate chưa QUA. Shot MANUAL được user làm tay và duyệt đạt mới tính DONE.

### Bước 4: Pha B — Gen video (E-2, chỉ sau Keyframe Gate QUA)
- Đổi `phase` sang `B` trong state. Duyệt `generate_order` các mục `stage: "stage2_video"` theo đúng thứ tự:
  - Shot **image-to-video**: upload keyframe đã duyệt (`assets/keyframes/Sxx_keyframe.png`) vào Flow ở vai trò frame/ingredient + dán `stage2_video.motion_prompt` (CHỈ dán, không chỉnh).
  - Shot **text-to-video**: dán prompt trực tiếp vào Flow (bỏ tầng keyframe).
  - Đặt đúng `duration` / `aspect_ratio` / model Veo 3.1 theo prompts.json + concept.md.
- Chờ generate bằng **state polling** với nhịp `poll_interval_s`, trần chờ `generation_timeout_s` (tra config). KHÔNG sleep cứng vô hạn.
- Tải clip về `clips/Sxx.mp4` (đổi tên ngay sau download).
- **Trích frame QA (E-3)**: dùng ffmpeg trích `qa_frames_per_clip` frame (tra config) vào `qa_frames_dir` (tra config) đặt tên `Sxx_f1.png`, `Sxx_f2.png`, …
- Cập nhật execution-state: `video: DONE`, `clip_path`, attempts.

### Bước 5: Vòng fix (E-5, E-6)
- Nhận danh sách shot FAILED từ qa-report của orchestrator (tối đa `max_fix_rounds` vòng — orchestrator điều phối, tra config).
- Với từng shot FAILED: gen lại đúng shot đó theo đề xuất fix trong qa-report (prompt vẫn lấy từ prompts.json — nếu fix yêu cầu sửa prompt thì báo về orchestrator/06, KHÔNG tự sửa).
- Mỗi lượt gen kỹ thuật (timeout, download fail, lỗi tạm thời) → `attempts++` và ghi `last_error`.
- Vượt `max_attempts_per_shot` (tra config) → đánh dấu `video: BLOCKED`, ghi last_error, **tiếp tục các shot còn lại** (không treo cả lô).

### Bước 6: Xử lý lỗi Flow (E-8)
- Session hết hạn / reCAPTCHA xuất hiện / quota cạn → **dừng ngay toàn bộ**, báo user kèm snapshot execution-state (trạng thái từng shot). Đây là lỗi unrecoverable tại chỗ — user đăng nhập lại/nạp quota rồi resume theo Bước 2.
- Timeout lượt gen → `video: FAILED` + retry theo `max_attempts_per_shot`.
- Download fail → retry 1 lần rồi FAILED shot đó, tiếp shot khác.

### Bước 7: Bàn giao (E-9)
Khi xong (hoặc dừng vì lỗi), ghi tổng kết bàn giao gồm:
- Danh sách clip theo shot: `shot_id` → `clips/Sxx.mp4`.
- Danh sách shot `MANUAL` (user làm tay) và `BLOCKED` (hết lượt retry) kèm lý do.
- Đường dẫn frame QA trong `qa_frames_dir` (tra config) — đủ để `08-video-qa-review` đọc bằng chứng không đổi và `09-assembly-delivery` chạy không thay đổi.
- Snapshot `execution-state.json` cuối cùng.

## 4. Output Format

### execution-state.json (schema chuẩn — nguồn resume duy nhất)
Lưu tại vị trí `execution_state_file` trong config (tra config). Schema:

```json
{
  "project": "<project-slug>",
  "engine": "veo3",
  "phase": "A|B",
  "current_shot": "S02",
  "fix_round": 1,
  "shots": [
    {
      "shot_id": "S01",
      "keyframe": "DONE|PENDING|FAILED|MANUAL",
      "video": "DONE|PENDING|FAILED|BLOCKED|NOT_STARTED",
      "attempts": 1,
      "clip_path": "clips/S01.mp4",
      "last_error": null
    }
  ]
}
```

- `phase` + `current_shot` là khóa tuần tự hóa: chỉ 1 shot generating tại một thời điểm.
- `attempts` đếm lượt gen kỹ thuật mỗi shot; so trần với `max_attempts_per_shot` (tra config).
- `clip_path` ghi đúng path quy ước `clips/Sxx.mp4` để 09 dùng không đổi.

### Bảng bàn giao tổng kết (cuối phiên)

```markdown
# Bàn giao Executor: <project-slug> — Vòng fix <n>
| Shot | Keyframe | Video | Clip | Frame QA | Ghi chú |
|------|----------|-------|------|----------|---------|
| S01  | DONE     | DONE  | clips/S01.mp4 | <qa_frames_dir>/S01_f1..fN.png | — |
| S03  | MANUAL   | PENDING | — | — | User làm keyframe tay (tool ngoài) |
| S05  | DONE     | BLOCKED | — | — | Vượt max_attempts_per_shot: <last_error> |
- Cần xử lý tay: <danh sách shot MANUAL/BLOCKED>
- Snapshot state: <đường dẫn execution_state_file>
```

## 5. Important Rules

### Required Practices
- LUÔN đọc tham số automation (`flow_url`, `generation_timeout_s`, `poll_interval_s`, `max_attempts_per_shot`, `qa_frames_per_clip`, `qa_frames_dir`, `execution_state_file`, `keyframe_source`) từ config mục 8 trước khi chạy — tra config, không hardcode.
- Thao tác Flow đúng quy ước skill `browser-use`: persistent logged-in profile, semantic locator (role + accessible name), state polling thay sleep cứng, download tracking, telemetry khi chẩn đoán. Chi tiết bản đồ UI xem `references/flow-ui.md`.
- Cập nhật `execution-state.json` ngay sau mỗi chuyển trạng thái; shot DONE bỏ qua khi resume.
- Tuần tự hóa: mỗi lần chỉ 1 shot generating (khóa `phase` + `current_shot`).
- Đổi tên file tải về đúng quy ước (`clips/Sxx.mp4`, `assets/keyframes/Sxx_keyframe.png`) NGAY sau download — không để tên gốc.
- Trích frame QA bằng ffmpeg đúng số lượng `qa_frames_per_clip` (tra config) vào `qa_frames_dir` (tra config) trước khi bàn giao.

### Prohibited Practices
- KHÔNG tự vượt Keyframe Gate — Pha B chỉ chạy sau khi user duyệt lô keyframe QUA.
- KHÔNG đổi thứ tự `generate_order`, KHÔNG nhảy cóc shot.
- KHÔNG dùng Chrome extension, bearer token, hay bất kỳ cơ chế bypass nào (kể cả reCAPTCHA bypass) — chỉ browser automation trên phiên thật của user.
- KHÔNG sửa `prompts.json`, `concept.md`, `shotlist.json`, `bible.md`; thấy prompt sai → báo orchestrator/06.
- KHÔNG hardcode giá trị config (timeout, URL, số frame, số retry…) vào quy trình.
- KHÔNG sáng tạo nội dung hoặc bổ sung prompt khi thiếu dữ liệu — dừng và báo.

### Quality Checklist
- [ ] Preconditions kiểm đủ (Bible Gate QUA, prompts.json + generate_order có mặt).
- [ ] Mọi tham số automation lấy từ config mục 8 (tra config), zero hardcode.
- [ ] `execution-state.json` khởi tạo/resume đúng schema; shot DONE không gen lại.
- [ ] Tại mỗi thời điểm chỉ 1 shot ở trạng thái generating.
- [ ] Keyframe lưu `assets/keyframes/Sxx_keyframe.png`; có dừng trình Keyframe Gate theo lô kèm danh sách shot MANUAL.
- [ ] Clip lưu `clips/Sxx.mp4`; frame QA trích đủ `qa_frames_per_clip` vào `qa_frames_dir` (tra config).
- [ ] Lỗi session/quota/reCAPTCHA dừng ngay kèm snapshot state (E-8); shot hết lượt retry được BLOCKED và lô vẫn chạy tiếp (E-6).
- [ ] Bảng bàn giao đủ cho 08-video-qa-review và 09-assembly-delivery dùng không đổi (E-9).
