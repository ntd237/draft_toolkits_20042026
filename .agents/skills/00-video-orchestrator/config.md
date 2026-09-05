# Config — Video Production Toolkit

File tham chiếu trung tâm cho toàn bộ bộ skill.
Config là nguồn ĐỀ XUẤT và giới hạn validate — không phải giá trị dùng im lặng. 00-video-orchestrator PHẢI hỏi người dùng chốt tham số ở đầu mỗi lần chạy; kết quả chốt được ghi vào `concept.md` cho các skill sau đọc.

## 1. Thư mục dự án (File System Policy)

- Gốc: `docs/video-projects/<project-slug>/`
- `<project-slug>`: chữ thường, kebab-case, không dấu, tối đa 40 ký tự. Ví dụ: `quang-cao-ca-phe-30s`.
- Nếu chưa có slug do người dùng đặt, orchestrator tự đề xuất từ tên ý tưởng.

## 2. Danh mục artifact (Naming Policy)

| Thứ tự | File | Skill tạo ra |
|---|---|---|
| 01 | `concept.md` | 01-idea-brainstorm |
| 02 | `research.md` | 02-research-reference |
| 03 | `script.md` | 03-script-writer |
| 04 | `shotlist.json` (+ `shotlist.md` dạng đọc) | 04-storyboard-shotlist |
| 05 | `bible.md` | 05-character-world-bible |
| 06 | `prompts.json` | 06-video-prompt-engineer |
| 07 | `audio-plan.md` | 07-audio-designer |
| 08 | `qa-report.md` | 08-video-qa-review |
| 09 | `delivery-checklist.md` | 09-assembly-delivery |

- Clip đã generate (nếu có) lưu ở: `<project>/clips/S01.mp4`, … trùng shot id.

## 3. Engine video (Runtime Policy)

Danh mục `engine` hợp lệ — dùng làm CÁC LỰA CHỌN khi hỏi người dùng; giá trị được chọn ghi vào `concept.md` và dùng xuyên suốt:

- `veo3` — Google Veo 3 (hỗ trợ dialogue + audio trong prompt)
- `sora` — OpenAI Sora
- `kling` — Kuaishou Kling
- `runway` — Runway Gen-4 (image-to-video, cần keyframe)

Engine không có trong danh sách này phải được người dùng xác nhận trước khi dùng, và phải có file `references/<engine>.md` trong skill `06-video-prompt-engineer`.

## 4. Tham số mặc định (Validation Policy)

Cột "Mặc định" chỉ là ĐỀ XUẤT trình bày cho người dùng khi hỏi — KHÔNG được áp dụng im lặng. Giá trị người dùng chọn ghi vào `concept.md`; cột "Mặc định" đồng thời là giới hạn validate kỹ thuật (trần độ dài, duration limit).

| Tham số | Mặc định | Ghi chú |
|---|---|---|
| `mode` | `lite` | `lite` = đi tắt idea → script → bible → prompt; `full` = chạy đủ 9 bước |
| `aspect_ratio` | `16:9` | Cho phép `9:16`, `1:1` theo nền tảng đích |
| `duration_per_shot` | `5s` | Phải nằm trong giới hạn duration của engine đã chọn |
| `language` | `vi` | Ngôn ngữ kịch bản, VO, caption |
| `target_platform` | `youtube` | youtube / tiktok / facebook / ads |
| `shot_id_format` | `S01`, `S02`, … | Hai chữ số, tăng dần, không lặp |
| `max_prompt_chars` | `1500` | Trần độ dài mỗi prompt video |

## 5. Cổng (Gates) bắt buộc của pipeline

1. **Approval Gate**: `concept.md` phải được người dùng chọn hướng ý tưởng trước khi sang `03-script-writer` (bỏ qua trong `lite` nếu người dùng đưa sẵn ý tưởng chốt).
2. **Bible Gate**: không được sinh `prompts.json` khi chưa có `bible.md` hoàn chỉnh.
3. **QA Gate**: không được sang `09-assembly-delivery` khi `qa-report.md` còn clip ở trạng thái FAILED.

## 6. Vòng lặp QA

- Tối đa **3 vòng** fix → generate lại → QA.
- Vẫn FAILED sau 3 vòng: dừng, báo cáo người dùng kèm danh sách lỗi còn lại.

## 7. Thứ tự generate prompt (Runtime Policy)

`06-video-prompt-engineer` phải xuất thêm trường `generate_order` trong `prompts.json` — thứ tự dán prompt để kết quả tối ưu, theo quy tắc:
1. **Nhóm theo nhân vật**: mọi shot của cùng nhân vật lặp lại xếp liền nhau và dùng chung seed.
2. **Shot "thiết lập" chạy trước**: lần xuất hiện quan trọng nhất của nhân vật generate đầu tiên (2–3 lần thử, chọn bản đẹp nhất) để chốt mặt/seed; các shot còn lại của nhân vật tái dùng seed đó.
3. **Shot mở màn bối cảnh đầu nhóm phụ**: shot wide đủ đội hình/bối cảnh là chuẩn tham chiếu hình ảnh cho các shot nhóm sau.
4. **Nhân vật phụ xuất hiện 1 lần để sau cùng** — lỗi không ảnh hưởng chuỗi.
5. **Dừng kiểm giữa chừng**: sau mỗi shot "thiết lập", soi kết quả và sửa prompt trước khi generate phần còn lại — không chạy hàng loạt mù quáng.
