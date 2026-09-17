# draft_toolkits_20042026

![Status](https://img.shields.io/badge/status-draft-orange)
![Content](https://img.shields.io/badge/content-AI%20skills%20%2B%20prompts-blue)
![Language](https://img.shields.io/badge/language-Vietnamese-green)
![Format](https://img.shields.io/badge/format-Markdown-informational)

Không gian nháp để tôi gom, nghịch, test, sáng tạo và thử nghiệm các `prompts` và `skills` cho AI assistants. Repo này đóng vai trò như một sandbox cá nhân để thử ý tưởng mới, tinh chỉnh workflow, lưu các phiên bản nháp và kiểm nghiệm prompt trước khi tái sử dụng ở nơi khác.

## Mục lục

- [Tổng quan](#tổng-quan)
- [Cài đặt](#cài-đặt)
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
- `other-skills/`: kho nhóm skill chuyên biệt theo pipeline (`marketing-skills/`, `video-skills/`, `apk-skills/`), copy sang `.agents/skills/` khi muốn dùng.
- `docs/`: tài liệu quy trình, hướng dẫn cài đặt và xử lý kỹ thuật.
- `draft_output/`: nơi lưu output, ghi chú, bản so sánh hoặc kết quả thử nghiệm.

## Cài đặt

Repo này là một sandbox tài liệu, không phải ứng dụng chạy trực tiếp. Không có `requirements.txt`, script cài đặt hay entrypoint thực thi ở root — chỉ cần clone về là dùng được.

```bash
git clone https://github.com/ntd237/draft_toolkits_20042026.git
cd draft_toolkits_20042026
```

## License

Repo này được phát hành theo giấy phép [MIT](LICENSE).

## Liên hệ

- Tác giả: `ntd237`
- Email: `ntd237.work@gmail.com`
- GitHub: `https://github.com/ntd237`
