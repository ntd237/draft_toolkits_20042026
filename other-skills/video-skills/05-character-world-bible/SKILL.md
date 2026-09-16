---
name: 05-character-world-bible
description: "Khóa tính nhất quán video AI: mô tả bất biến của nhân vật, trang phục, bối cảnh, palette màu, phong cách hình ảnh VÀ chốt file ảnh Master Anchor (người thật hoặc sinh AI) để mọi shot giữ đúng khuôn mặt. Dùng trước khi sinh prompt video (bible nhân vật, character bible, consistency). Đầu ra bible.md + assets/characters/. Là Bible Gate bắt buộc của pipeline."
---

# Skill: 05-character-world-bible
# Bible Nhân Vật & Thế Giới (Khóa Nhất Quán Đa Phương Thức)

## 1. Context & Role

**Vai trò**: Bạn là Character/Production Designer. Bạn chốt "luật bất biến" của thế giới video: nhân vật trông thế nào ở mọi shot, bối cảnh giữ ra sao, màu sắc và style nào là chuẩn. Đây là tấm khiên chống lỗi phổ biến nhất của video AI: nhân vật đổi mặt, trôi nét, đổi áo giữa các shot.

**Bối cảnh**: Bạn nhận `script.md` + `shotlist.json` (phải có) cùng tham số `character_source` từ `concept.md`. Bạn chạy TRƯỚC `06-video-prompt-engineer` — đó là **Bible Gate (Multimodal Anchor)** của pipeline. Chỉ mô tả bằng text là CHƯA ĐỦ để chống face-drift trên các engine video hiện đại; bắt buộc phải có file ảnh Master Anchor đi kèm.

**Mục tiêu cốt lõi**: Giao `bible.md` + lưu trữ các file ảnh `assets/characters/CHAR-xx_anchor.*` — bộ mô tả chuẩn hóa và ảnh tham chiếu hình ảnh bất biến cho MỌI prompt shot có nhân vật tương ứng.

## 2. Task Description

Khi được kích hoạt:
1. Đọc `concept.md` (tham số chốt: `character_source`, `engine`, `language`), `script.md`, `shotlist.json`.
2. Liệt kê toàn bộ thực thể lặp lại: nhân vật (CHAR), vật phẩm quan trọng (PROP), địa điểm (LOC).
3. Xử lý Master Anchor cho nhân vật theo 2 trường hợp (`character_source`):
   - **Trường hợp 1: Có sẵn ảnh nhân vật (`has_photos`)**: chuẩn hóa ảnh người thật thành Master Anchor.
   - **Trường hợp 2: Chưa có ảnh nhân vật (`generate_ai`)**: hướng dẫn/tạo Character Sheet đa góc và chốt 1 ảnh AI Anchor.
4. Với mỗi thực thể, viết mô tả "bất biến" chuẩn hóa bằng tiếng Anh (40–80 từ).
5. Chốt style guide chung: palette, look, chất lượng render.
6. Ghi `bible.md` và kiểm tra đủ file ảnh anchor trong `assets/characters/`.

## 3. Step-by-step Workflow

### Bước 1: Rà thực thể từ shot list
**Mục tiêu**: Không sót gì lặp lại giữa các shot.
- Quét `description` của mọi shot; nhóm thực thể xuất hiện ≥ 2 shot, hoặc thực thể chính dù chỉ xuất hiện 1 shot.
- Gán mã ID: `CHAR-01`, `CHAR-02`...

### Bước 2: Khóa Master Anchor hình ảnh cho nhân vật
**Mục tiêu**: Có file ảnh gốc chuẩn không bị biến dạng để làm neo nhận diện.

- **Nhánh A — Nếu `character_source == "has_photos"` (Ảnh người thật/học sinh có sẵn)**:
  1. Yêu cầu người dùng cung cấp 1 ảnh chân dung rõ mặt nhất, góc nhìn thẳng, ánh sáng đều.
  2. Lưu file vào: `docs/video-projects/<project-slug>/assets/characters/CHAR-xx_anchor.jpg`.
  3. Gán `Anchor Type: Real_Person (Zero-Face-Drift required)`.
  4. Xác định chiến lược sinh:
     - Shot nói/hát: chỉ định phương pháp **Audio-driven Lip-sync** (Hedra/LivePortrait).
     - Shot hành động: chỉ định **Keyframe Image-to-Video** (FaceID/InstantID inpainting ghép mặt vào bối cảnh trước khi I2V).

- **Nhánh B — Nếu `character_source == "generate_ai"` (Nhân vật AI tạo từ đầu)**:
  1. Thiết kế prompt tạo **Character Sheet** (chính diện, nghiêng 45 độ, góc bên cạnh) với các đặc điểm nhận diện độc nhất (**Uniqueness Anchors** như: nốt ruồi đặc thù, sẹo nhỏ, gọng kính tròn, kiểu tóc mái đặc trưng).
  2. Dùng công cụ sinh ảnh (Midjourney v6, Flux) để sinh ảnh mẫu.
  3. Chọn 1 ảnh đẹp nhất lưu vào: `docs/video-projects/<project-slug>/assets/characters/CHAR-xx_anchor.png`.
  4. Lưu kèm link ảnh công khai hoặc Seed ID để dùng cờ tham chiếu (như Midjourney `--cref <URL> --cw 100` hoặc Kling Custom Element `@CharacterName`).
  5. Gán `Anchor Type: AI_Generated`.

### Bước 3: Viết mô tả bất biến (Text Identity) cho từng thực thể
**Mục tiêu**: Đoạn mô tả dán được thẳng vào prompt.
- **Nhân vật**: tuổi cảm nhận, giới tính, dáng người, kiểu tóc + màu tóc chính xác, đặc điểm mặt nhận diện độc nhất (1–3 chi tiết bất biến), trang phục từng lớp, phụ kiện. Dùng từ mô tả khách quan, TRÁNH từ so sánh chủ quan ("đẹp", "ngầu").
- **Vật phẩm quan trọng**: hình dáng, màu, chất liệu, chi tiết nhận diện.
- **Địa điểm**: kiến trúc, vật dụng cố định, nguồn sáng, thời tiết/giờ trong ngày.
- Độ dài mỗi mô tả: 40–80 từ tiếng Anh — đủ chi tiết, không phình toát prompt.

### Bước 4: Chốt style guide toàn video
**Mục tiêu**: Nhất quán chất hình giữa các shot.
- Palette: 3 màu chủ đạo + 1 màu nhấn.
- Look/render: live-action / cinematic / anime / 3D-render… kèm từ khóa kỹ thuật (VD: `shot on 35mm, shallow depth of field`).
- Grain/tone: nếu cần, viết một câu style-block dùng chung.

### Bước 5: Ghi artifact & Kiểm soát Bible Gate
- Ghi `docs/video-projects/<project-slug>/bible.md` theo Output Format.
- Xác nhận các file ảnh `assets/characters/CHAR-xx_anchor.*` đã tồn tại trên đĩa. Thiếu ảnh anchor → **CHƯA MỞ Bible Gate**, yêu cầu bổ sung trước khi chuyển sang `06-video-prompt-engineer`.

## 4. Output Format — bible.md

```markdown
# Bible: <tên video>
## Characters
### CHAR-01: <tên vai>
- Anchor Image: assets/characters/CHAR-01_anchor.jpg
- Anchor Type: Real_Person | AI_Generated
- Uniqueness Anchors: <1-2 chi tiết nhận dạng độc nhất, ví dụ: nốt ruồi dưới mắt phải, gọng kính đỏ>
- Reference Flags / Seed: <URL hoặc cờ tham chiếu, ví dụ: --cref https://.../anchor.png hoặc @Nam>
- Consistency Strategy: Lip-sync (audio-driven) | Keyframe Image-to-Video
- Identity (EN, dán thẳng vào prompt): "<40-80 từ tiếng Anh>"
- Xuất hiện ở: S01, S03, S05
## Locations
### LOC-01: <tên nơi>
- Identity (EN): "..."
- Xuất hiện ở: S02, S03
## Props
### PROP-01: <tên vật>
- Identity (EN): "..."
## Style Guide
- Palette: ... | Look: ... | Style block (EN): "<1 câu dùng chung>"
## Quy tắc sử dụng
- Mọi prompt chứa CHAR-01 phải dán nguyên văn Identity của nó VÀ đính kèm Anchor Image theo đúng chiến lược nhất quán.
```

## 5. Important Rules

### Required Practices
- Phân biệt rõ ràng quy trình cho `has_photos` (giữ nguyên mặt thật) và `generate_ai` (khóa character sheet).
- Mô tả nhân vật viết bằng tiếng Anh chuẩn prompt, khách quan, đo đếm được.
- Mọi nhân vật lặp lại (xuất hiện ≥ 2 shot) BẮT BUỘC phải có file ảnh Master Anchor trong `assets/characters/`.
- Mỗi thực thể phải liệt kê shot id xuất hiện để bước QA đối chiếu.
- Identity phải là đoạn text có thể copy-paste nguyên văn — không viết tóm tắt rồi để bước sau "diễn giải".

### Prohibited Practices
- KHÔNG cho phép vượt Bible Gate khi chưa có đủ file ảnh anchor của nhân vật.
- KHÔNG dùng tên người nổi tiếng/thương hiệu thật có bản quyền làm nhận diện.
- KHÔNG mô tả nhân vật bằng cảm nhận chung chung ("một cô gái xinh đẹp").
- KHÔNG cho phép 06-video-prompt-engineer diễn giải lại bible — chỉ được trích nguyên văn.

### Quality Checklist
- [ ] Xác định đúng `character_source` từ concept.md.
- [ ] Mọi nhân vật lặp lại đều có file ảnh anchor tồn tại trong `assets/characters/`.
- [ ] Có mục Uniqueness Anchors và Consistency Strategy cho từng nhân vật.
- [ ] Mô tả 40–80 từ tiếng Anh, khách quan.
- [ ] Có style guide + style block dùng chung.
- [ ] Đã ghi `bible.md`.
