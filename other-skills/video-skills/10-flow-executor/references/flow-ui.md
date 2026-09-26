# Reference — Bản đồ thao tác UI Google Flow & Xử lý sự cố

Tài liệu tham chiếu cho skill `10-flow-executor`. Mọi tham số runtime (`flow_url`, `generation_timeout_s`, `poll_interval_s`, `max_attempts_per_shot`, `qa_frames_per_clip`, `qa_frames_dir`, `execution_state_file`, `keyframe_source`) **tra config mục 8 "Tự động hóa Google Flow"** — không hardcode tại đây.

## 0. Quy tắc VERIFY-ON-SITE (bắt buộc)

Google Flow là web app thay đổi liên tục. Toàn bộ selector/label ghi trong tài liệu này là **dạng "cập nhật lúc triển khai thực tế"** — người thực thi PHẢI:

1. Xác minh lại từng bước trên UI thật trước khi chạy lô (mở `flow_url` bằng persistent logged-in profile, soi từng màn hình, chốt locator).
2. KHÔNG tự bịa locator cứng. Ưu tiên **semantic locator** theo skill `browser-use`: Tier 1 `getByRole` + accessible name → Tier 2 label/placeholder → Tier 3 text → Tier 4 test-id; CSS ngữ nghĩa/XPath tương đối chỉ làm fallback. Cấm XPath tuyệt đối (`/html/body/...`) và locator bám class/hash styling động.
3. Ghi lại locator đã xác minh vào phần "Ghi chú verify" của từng bước dưới đây khi chạy thực địa (buổi dry-run interactive với user sau implement — điều kiện kết thúc pipeline trước 07-review final).
4. Đồng bộ bằng state polling (`locator.waitFor({ state: 'visible' })`, `waitForResponse` trên endpoint generate) — KHÔNG dùng sleep cứng; nhịp poll và trần chờ lấy từ `poll_interval_s` / `generation_timeout_s` (tra config).

## 1. Quy trình tương tác chuẩn (Pha A — gen keyframe trong Flow)

> Áp dụng khi `keyframe_source=auto` và Flow hỗ trợ sinh ảnh. Nếu `keyframe_source` trỏ tool ngoài (midjourney/flux/leonardo) → KHÔNG vào Flow cho shot đó; đánh dấu `keyframe: MANUAL` trong execution-state và đưa vào danh sách user làm tay.

| Bước | Thao tác | Điểm xác minh | Ghi chú verify (điền khi thực địa) |
|---|---|---|---|
| A1 | Mở `flow_url` (tra config) bằng persistent logged-in profile | Đã đăng nhập, không bị văng ra trang login | |
| A2 | Vào project: **tạo project mới hoặc chọn project trùng `<project-slug>`** | Tên project khớp project-slug | |
| A3 | Chọn chế độ sinh ảnh (nếu Flow có) / mở khung nhập prompt | Ô nhập prompt visible | |
| A4 | Dán nguyên văn `stage1_keyframe.image_prompt` từ prompts.json | Nội dung ô nhập khớp prompt (không bị cắt theo `max_prompt_chars` — tra config) | |
| A5 | Submit generate | Request generate bắn ra (waitForResponse) | |
| A6 | Poll kết quả theo `poll_interval_s`, trần `generation_timeout_s` | Ảnh kết quả render xong trong khung kết quả | |
| A7 | Download ảnh | Sự kiện download kích hoạt (`waitForEvent('download')`) | |
| A8 | Đổi tên → `assets/keyframes/Sxx_keyframe.png`, cập nhật execution-state | File tồn tại đúng path | |

## 2. Quy trình tương tác chuẩn (Pha B — gen video)

| Bước | Thao tác | Điểm xác minh | Ghi chú verify (điền khi thực địa) |
|---|---|---|---|
| B1 | Mở `flow_url` (tra config), vào đúng project | Đã đăng nhập + đúng project | |
| B2 | **Shot image-to-video**: upload keyframe đã duyệt (`assets/keyframes/Sxx_keyframe.png`) vào Flow ở vai trò frame/ingredient (file upload qua `setInputFiles`) | Ảnh preview hiển thị trong khung soạn | |
| B3 | Dán prompt: image-to-video → dán `stage2_video.motion_prompt`; text-to-video → dán prompt trực tiếp (bỏ tầng keyframe) | Ô nhập chứa đúng prompt | |
| B4 | Đặt model **Veo 3.1** (engine ghi trong state là `veo3`) + `aspect_ratio` + `duration` đúng theo prompts.json/concept.md | Giá trị hiển thị khớp chốt | |
| B5 | Submit generate | Request generate bắn ra | |
| B6 | Poll trạng thái theo `poll_interval_s`, trần `generation_timeout_s` | Clip render xong (thumbnail/player sẵn sàng) | |
| B7 | Download clip | Sự kiện download kích hoạt | |
| B8 | Đổi tên → `clips/Sxx.mp4`; cập nhật execution-state (`video: DONE`, `clip_path`, attempts) | File tồn tại đúng path | |
| B9 | Trích `qa_frames_per_clip` frame bằng ffmpeg vào `qa_frames_dir` (tra config), tên `Sxx_f1.png`, `Sxx_f2.png`, … | Số frame khớp config | |
| B10 | Chuyển `current_shot` sang shot kế theo `generate_order` | State ghi nhận trước khi thao tác tiếp | |

## 3. Quy ước đặt tên file tải về

- Tên gốc do Flow sinh ra (thường là hash/uuid + đuôi mở rộng) **chỉ dùng tạm** — ĐỔI TÊN NGAY SAU DOWNLOAD, không để tên gốc trong thư mục artifact.
- Map đích:
  - Keyframe (Pha A): `<project>/assets/keyframes/Sxx_keyframe.png` — trùng shot id.
  - Clip (Pha B): `<project>/clips/Sxx.mp4` — trùng shot id.
  - Frame QA: `<qa_frames_dir>` (tra config) — `Sxx_f<N>.png` với N đánh thứ tự frame trích.
- Nếu download về thư mục tạm của trình duyệt → move/rename vào path đích trong cùng bước, rồi mới cập nhật execution-state (state chỉ ghi DONE sau khi file đã ở đúng path).

## 4. Bảng sự cố (triệu chứng → xử lý)

Khớp bảng Edge Cases / Xử lý ngoại lệ trong plan. Mọi lần retry kỹ thuật phải `attempts++` và ghi `last_error` vào execution-state; trần retry là `max_attempts_per_shot` (tra config).

| Triệu chứng | Chẩn đoán | Xử lý |
|---|---|---|
| Generate không ra kết quả sau `generation_timeout_s` (tra config) | Timeout lượt gen | Đánh dấu `FAILED` + `attempts++`; còn lượt → gen lại đúng shot; hết lượt → `BLOCKED`, chuyển shot kế (E-6) |
| Flow báo hết credit / thông điệp quota | Quota Google cạn (E-8) | **Dừng ngay toàn bộ**, báo user kèm snapshot execution-state; không gen tiếp để tránh dây chuyền lỗi |
| Bị văng ra trang đăng nhập / cookie hết hạn | Session hết hạn (E-8) | **Dừng ngay**, báo user đăng nhập lại; sau đó resume từ execution-state (E-7) — shot DONE không gen lại |
| Hiện challenge reCAPTCHA giữa thao tác | Google nghi hoạt động bất thường (E-8) | **Dừng ngay**, KHÔNG cố vượt/bypass; báo user tự xử lý rồi resume (E-7) |
| Click download nhưng không có file / sự kiện download không nổ | Download fail | Retry 1 lần (kiểm tra popup/permissions); vẫn fail → `FAILED` shot đó, tiếp shot khác (E-6) |
| File tải về hỏng / 0 byte / không mở được bằng ffmpeg | Kết quả không tải được | Xóa file hỏng, coi như download fail (retry 1 lần → FAILED) |
| Lỗi ffmpeg khi trích frame QA | Môi trường local | `FAILED` shot, QA ghi `NOT-CHECKED`; báo trong bàn giao |
| Mất mạng tạm thời / requestfailed | Network timeout | Retry theo `max_attempts_per_shot` (tra config) với backoff; ghi attempts vào state |
| Browser/tab bị đóng giữa chừng | Gián đoạn pipeline (E-7) | Chạy lại skill → đọc execution-state và resume đúng shot dang dở |
| Ô prompt từ chối nội dung (đếm ký tự vượt trần) | Prompt dài hơn giới hạn UI | Dừng shot đó, báo orchestrator/06 rút gọn — KHÔNG tự cắt prompt |

## 5. Nguyên tắc dừng & bàn giao

- Lỗi nhóm E-8 (session/reCAPTCHA/quota) → dừng toàn bộ + snapshot state; không tự thử lại vô hạn.
- Lỗi kỹ thuật từng shot → cô lập shot (FAILED/BLOCKED), lô vẫn chạy tiếp.
- Kết thúc (xong lô hoặc dừng): xuất bảng bàn giao theo Output Format của SKILL.md — danh sách clip per shot, shot MANUAL/BLOCKED, đường dẫn frame QA — đủ cho `08-video-qa-review` và `09-assembly-delivery` dùng không đổi (E-9).
