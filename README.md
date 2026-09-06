# draft_toolkits_20042026

![Status](https://img.shields.io/badge/status-draft-orange)
![Content](https://img.shields.io/badge/content-AI%20skills%20%2B%20prompts-blue)
![Language](https://img.shields.io/badge/language-Vietnamese-green)
![Format](https://img.shields.io/badge/format-Markdown-informational)

Không gian nháp để tôi gom, nghịch, test, sáng tạo và thử nghiệm các `prompts`, `skills` và `commands` cho AI assistants, tập trung vào các `skills` theo định dạng `SKILL.md` — skill đang hoạt động đặt trong `.agents/skills`, các nhóm skill theo pipeline đặt trong `other-skills/`.

Repo này đóng vai trò như một sandbox cá nhân để thử ý tưởng mới, tinh chỉnh workflow, lưu các phiên bản nháp và kiểm nghiệm prompt trước khi tái sử dụng ở nơi khác.

## Mục lục

- [Tổng quan](#tổng-quan)
- [Tính năng nổi bật](#tính-năng-nổi-bật)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Ví dụ sử dụng](#ví-dụ-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Quy ước nội dung](#quy-ước-nội-dung)
- [License](#license)
- [Liên hệ](#liên-hệ)

## Tổng quan

### Bài toán

Khi nghịch với AI assistants, prompt và workflow thường xuất hiện rời rạc trong chat, note hoặc thư mục tạm. Điều đó dẫn tới:

- Ý tưởng hay bị thất lạc sau vài phiên thử nghiệm.
- Khó nhớ prompt nào đang là bản nháp, prompt nào đã dùng ổn.
- Mỗi lần muốn thử biến thể mới lại phải lục lại chat cũ hoặc viết lại từ đầu.
- Khó theo dõi các thử nghiệm theo từng nhóm như `skills` hay prompt rời.

### Cách repo này giải quyết

Repo này gom các thử nghiệm vào cấu trúc đủ gọn để dễ tìm lại và tiếp tục chỉnh sửa:

- `.agents/skills/`: nơi lưu các skill đang hoạt động dạng `SKILL.md`, có thể đi kèm `references/`.
- `other-skills/`: kho nhóm skill theo pipeline chưa kích hoạt (`apk-skills/`, `video-skills/`) và skill độc lập (`security-scan/`), copy sang `.agents/skills/` khi muốn dùng.
- `draft_output/`: nơi lưu output, ghi chú, bản so sánh hoặc kết quả thử nghiệm.

### Công nghệ và định dạng

- Nội dung chính: Markdown (`.md`) với front matter mô tả (`name`, `description`)
- Định dạng skill: `SKILL.md` kèm thư mục `references/` khi cần tài liệu tham chiếu
- Môi trường mục tiêu: Antigravity, Claude Code, opencode hoặc hệ thống tương tự có hỗ trợ nạp skill từ thư mục
- Ngôn ngữ giao tiếp mặc định trong nhiều prompt: tiếng Việt

## Tính năng nổi bật

- Có chỗ riêng để thử ý tưởng prompt mà không cần trộn với repo production.
- Tách `.agents/skills/`, `other-skills/` và `draft_output/` để vòng lặp thử nghiệm rõ ràng hơn.
- Các skill đã có cấu trúc hoàn chỉnh (`SKILL.md` + `references/`) nên dễ copy hoặc fork sang repo khác.
- Nhiều nội dung đã quy ước ngôn ngữ và workflow nên dễ so sánh giữa các phiên bản thử nghiệm.
- Cấu trúc thư mục gọn, hợp với cách làm việc kiểu viết nháp rồi tinh chỉnh dần.

## Cài đặt

Repo này là một sandbox tài liệu, không phải ứng dụng chạy trực tiếp. Không có `requirements.txt`, script cài đặt hay entrypoint thực thi ở root — chỉ cần clone về là dùng được.

### 1. Clone repo

```bash
git clone https://github.com/ntd237/draft_toolkits_20042026.git
cd draft_toolkits_20042026
```

### 2. Kiểm tra cài đặt

Xác nhận clone thành công bằng cách liệt kê các skill hiện có:

```bash
ls .agents/skills
ls other-skills/apk-skills other-skills/video-skills other-skills/security-scan
```

Kết quả mong đợi: `.agents/skills` gồm 9 skill đang hoạt động (`business-analyst`, `cat`, `code-search-expert`, `convert-model`, `dog`, `english-exam-solver`, `exam-listening-verbatim`, `novel-summarizer`, `read-only`); `other-skills` gồm 2 nhóm pipeline — `apk-skills` (5 skill `00-apk-convert` → `04-apk-verify-fix`) và `video-skills` (10 skill `00-video-orchestrator` → `09-assembly-delivery`) — cùng 1 skill độc lập `security-scan`.

## Sử dụng

### 1. Thử nghiệm trực tiếp trong repo

- Mở `.agents/skills/<skill>/SKILL.md` để đọc, chỉnh sửa hoặc viết lại một skill đang hoạt động.
- Dùng `other-skills/` để lưu trữ, tinh chỉnh các nhóm skill theo pipeline chưa đưa vào dùng hằng ngày.
- Dùng `draft_output/` để lưu kết quả test, note, nhận xét hoặc output muốn giữ lại.

### 2. Danh sách skill hiện có

**Skill đang hoạt động — `.agents/skills/`:**

| Vị trí | Skill | Vai trò |
| --- | --- | --- |
| `.agents/skills/business-analyst` | `business-analyst` | Phân tích nghiệp vụ và kiến trúc giải pháp cho Web, Mobile, Game, AI (CV, NLP/LLM, GenAI, ML): biến ý tưởng thô thành workflow nghiệp vụ, use case, sơ đồ Mermaid, business rules, edge cases, acceptance criteria và kiến trúc hệ thống |
| `.agents/skills/cat` | `cat` | Prompt nhân vật mèo 🐈 báo cáo tin tức hàng ngày: tin tức Việt Nam, thời tiết, AQI, món ăn theo khung giờ, GitHub Trending, tin AI coding tools |
| `.agents/skills/code-search-expert` | `code-search-expert` | Truy xuất và điều hướng code chuyên gia: kết hợp CodeGraph AST, ripgrep và tìm kiếm ngữ nghĩa vector, kèm mở rộng truy vấn tự động Việt→Anh để định vị logic, symbol và luồng kiến trúc |
| `.agents/skills/convert-model` | `convert-model` | Lập kế hoạch chuyển đổi model ML/DL giữa các runtime (ONNX, TensorRT, OpenVINO, TFLite, Core ML, RKNN...) và xếp hạng các đường chuyển đổi khả thi |
| `.agents/skills/dog` | `dog` | Prompt nhân vật cún/chó 🐕 báo cáo tin tức hàng ngày: tin tức Việt Nam, thời tiết, AQI, món ăn theo khung giờ, GitHub Trending, tin Augment & Claude trên Reddit, tin AI coding tools, Quote of the Week từ This Week in Rust |
| `.agents/skills/english-exam-solver` | `english-exam-solver` | Giải đề tiếng Anh, TOEIC, IELTS với quy trình phân tích kỹ, loại trừ đáp án sai và giữ độ chính xác cao |
| `.agents/skills/exam-listening-verbatim` | `exam-listening-verbatim` | Chép nguyên văn audio listening kiểu IELTS/TOEIC/TOEFL, không tóm tắt, không dịch, không sửa |
| `.agents/skills/novel-summarizer` | `novel-summarizer` | Đọc và tóm tắt chi tiết, chính xác nội dung từng chương và dải chương tiểu thuyết (web novel, kiếm hiệp, tiên hiệp, huyền huyễn, light novel) từ đường link hoặc dải URL yêu cầu |
| `.agents/skills/read-only` | `read-only` | Cố vấn AI đa năng và chuyên gia thao tác an toàn cho các AI coding agent: research kỹ thuật sâu, duyệt web, kiểm tra terminal và trả lời các câu hỏi phức tạp |

**Skill độc lập — `other-skills/security-scan/`:**

| Vị trí | Skill | Vai trò |
| --- | --- | --- |
| `other-skills/security-scan` | `security-scan` | Quét bảo mật read-only cho project: phát hiện OWASP Top 10, hardcoded secrets, dependency lỗ hổng, config không an toàn; xuất báo cáo xếp hạng severity kèm khuyến nghị khắc phục |

**Nhóm pipeline APK — `other-skills/apk-skills/`:**

| Vị trí | Skill | Vai trò |
| --- | --- | --- |
| `other-skills/apk-skills/00-apk-convert` | `00-apk-convert` | Orchestrator một lệnh cho pipeline chuyển đổi APK/XAPK free↔paid: điều phối analyzer → convert → verify & auto-fix, xuất bản build debug + release đã sign |
| `other-skills/apk-skills/01-apk-edition-analyzer` | `01-apk-edition-analyzer` | Phân tích read-only một APK/XAPK: map ad SDK, feature flags, obfuscation, native libs, tech stack, package info; xuất `analysis.json` cho các converter downstream |
| `other-skills/apk-skills/02-apk-free2paid` | `02-apk-free2paid` | Chuyển APK/XAPK bản FREE (có ads, giới hạn feature) thành bản PAID (no ads, unlock premium); xử lý obfuscation, XAPK splits, native libs, sign bằng keystore mới |
| `other-skills/apk-skills/03-apk-paid2free` | `03-apk-paid2free` | Chuyển APK/XAPK bản PAID (no ads, full premium) thành bản FREE (có ads, gate premium); inject ad SDK stubs, re-gate premium, xử lý obfuscation và XAPK splits |
| `other-skills/apk-skills/04-apk-verify-fix` | `04-apk-verify-fix` | Verify APK đã convert: cài lên device/emulator, smoke test, đọc logcat và tự động fix trong loop cho đến khi install + launch + edition check đều pass |

**Nhóm pipeline video AI — `other-skills/video-skills/`:**

| Vị trí | Skill | Vai trò |
| --- | --- | --- |
| `other-skills/video-skills/00-video-orchestrator` | `00-video-orchestrator` | Orchestrator điều phối pipeline sản xuất video AI từ A-Z: idea → research → script → storyboard → bible → video prompt → audio → QA → delivery |
| `other-skills/video-skills/01-idea-brainstorm` | `01-idea-brainstorm` | Lên ý tưởng video AI: concept, thông điệp, đối tượng khán giả, mood/tone, format; đầu ra `concept.md` với 3-5 hướng ý tưởng được chấm điểm |
| `other-skills/video-skills/02-research-reference` | `02-research-reference` | Nghiên cứu tham chiếu cho video AI: video/trend cùng chủ đề, visual style, moodboard, gợi ý âm nhạc, lưu ý bản quyền; đầu ra `research.md` |
| `other-skills/video-skills/03-script-writer` | `03-script-writer` | Viết kịch bản video: logline → treatment → kịch bản 2 cột (hình/tiếng) có timing từng cảnh, dialogue, voiceover; đầu ra `script.md` |
| `other-skills/video-skills/04-storyboard-shotlist` | `04-storyboard-shotlist` | Tách kịch bản thành shot list chi tiết: id, duration, góc máy, chuyển động camera, ánh sáng, hành động, dialogue, chuyển cảnh; đầu ra `shotlist.json` + `shotlist.md` |
| `other-skills/video-skills/05-character-world-bible` | `05-character-world-bible` | Khóa tính nhất quán video AI: mô tả bất biến của nhân vật, trang phục, bối cảnh, palette màu, phong cách hình ảnh; đầu ra `bible.md` |
| `other-skills/video-skills/06-video-prompt-engineer` | `06-video-prompt-engineer` | Chuyển từng shot trong shotlist thành prompt video hoàn chỉnh theo engine cụ thể (Veo 3, Sora, Kling, Runway), nhúng bible nhân vật/bối cảnh và style block vào mọi prompt |
| `other-skills/video-skills/07-audio-designer` | `07-audio-designer` | Thiết kế âm thanh video: nhạc nền theo mood, SFX khớp shot, kịch bản voiceover có timing, gợi ý nguồn nhạc an toàn bản quyền; đầu ra `audio-plan.md` |
| `other-skills/video-skills/08-video-qa-review` | `08-video-qa-review` | Kiểm tra chất lượng clip video AI đã generate: đối chiếu từng clip với shotlist và bible, phát hiện lỗi AI (méo mặt, đổi nhân vật, nhảy logic), chấm PASS/FAILED và đề xuất fix |
| `other-skills/video-skills/09-assembly-delivery` | `09-assembly-delivery` | Giai đoạn xuất bản: ghép clip (ffmpeg/CapCut/Premiere), chèn VO/nhạc/caption theo audio plan, tạo thumbnail, xuất file đúng spec nền tảng đích |

Skill nào có thư mục `references/` thì đó là tài liệu tham chiếu domain knowledge đi kèm, ví dụ `other-skills/security-scan/references/` gồm 8 file bao quát từng mảng kiểm định (recon, secrets, injection, auth/crypto, config/infra, dependencies, tooling, report template), `.agents/skills/convert-model/references/` gồm 2 file về quantization, tensor shapes và runtime matrix, hay `other-skills/video-skills/06-video-prompt-engineer/references/` gồm 4 file theo từng engine video (Veo 3, Sora, Kling, Runway).

### 3. Khi có bản ổn, đem đi dùng

Nếu môi trường AI assistant của bạn hỗ trợ nạp skill từ thư mục, bạn có thể lấy các phần đã thử ổn trong repo này để đồng bộ:

- `.agents/skills/<skill>/` — skill đang hoạt động
- `other-skills/<nhóm>/<skill>/` — nhóm skill theo pipeline

Chi tiết cơ chế nạp phụ thuộc vào runtime bạn đang dùng. Repo này trước hết là nơi thử nghiệm và lưu nháp, không phải bộ phân phối hoàn chỉnh.

## Ví dụ sử dụng

### Ví dụ 1: Thử một skill chuyên biệt

```text
1. Mở `.agents/skills/convert-model/SKILL.md`.
2. Chỉnh wording, heuristic chọn runtime hoặc yêu cầu đầu ra.
3. Test skill đó trên một tình huống thật, ví dụ convert một model `.pt` sang ONNX.
4. Ghi nhận phần nào hiệu quả, phần nào còn mơ hồ hoặc dư thừa.
```

### Ví dụ 2: Thử nghiệm skill mới rồi đưa vào dùng

```text
1. Tạo thư mục `other-skills/<nhóm>/<tên-skill>/` với `SKILL.md` kèm front matter `name` + `description`.
2. Test nhiều vòng, ghi output và nhận xét vào `draft_output/`.
3. Khi skill đã ổn và cần dùng hằng ngày, copy sang `.agents/skills/<tên-skill>/`.
```

## Cấu trúc dự án

```text
draft_toolkits_20042026/
├── .agents/
│   └── skills/
│       ├── business-analyst/
│       ├── cat/
│       ├── code-search-expert/
│       ├── convert-model/
│       ├── dog/
│       ├── english-exam-solver/
│       ├── exam-listening-verbatim/
│       ├── novel-summarizer/
│       └── read-only/
├── other-skills/
│   ├── apk-skills/        # 5 skill pipeline chuyển đổi APK free↔paid (00→04)
│   ├── video-skills/      # 10 skill pipeline sản xuất video AI (00→09)
│   └── security-scan/     # 1 skill audit bảo mật read-only (SKILL.md + 8 references)
├── draft_output/          # thư mục lưu output các vòng test
├── .gitignore
├── LICENSE
└── README.md
```

> Ghi chú: repo có thể chứa thêm một số thư mục khác ngoài working copy (ví dụ `docs/`, `collection/`) nhưng chúng nằm trong `.gitignore` hoặc chỉ tồn tại cục bộ, không thuộc phạm vi tài liệu này.

## Quy ước nội dung

- Nhiều skill quy định trả lời bằng tiếng Việt; một số yêu cầu restate yêu cầu bằng tiếng Anh trước khi trả lời tiếng Việt.
- File skill bắt buộc có front matter mô tả `name` và `description`.
- Skill chuyên biệt nên đi kèm `references/` khi cần heuristic hoặc domain knowledge tái sử dụng.
- Skill thử nghiệm mới đặt trong `other-skills/<tên-skill>/` hoặc `other-skills/<nhóm>/<tên-skill>/`; chỉ chuyển lên `.agents/skills/<tên-skill>/` khi đã test ổn và cần dùng thường xuyên.

## License

Repo này được phát hành theo giấy phép [MIT](LICENSE).

## Liên hệ

- Tác giả: `ntd237`
- Email: `ntd237.work@gmail.com`
- GitHub: `https://github.com/ntd237`
