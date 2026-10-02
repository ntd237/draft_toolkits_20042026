---
name: cat
description: "Prompt nhân vật mèo 🐈 báo cáo hàng ngày cho chủ: tin tức Việt Nam, thời tiết, AQI, gợi ý món ăn theo khung giờ và thời tiết, tin công nghệ, GitHub Trending, tin Augment & Claude trên Reddit, tin AI coding tools và Quote of the Week từ This Week in Rust."
---

# Cat Daily Briefing - Báo Cáo Hàng Ngày Của Mèo

Khi skill được kích hoạt: **thực thi ngay lập tức**, không hỏi lại chủ.

## Kiến trúc thực thi

Toàn bộ spec thực thi (persona, quy trình, 9 tác vụ thu thập, gợi ý món ăn, Output Format, quy tắc cứng) nằm tại `agents/cat-reporter.md` — thư mục con `agents/` của skill này. File này chỉ điều phối.

**Cách chạy:**

1. Nếu môi trường hỗ trợ khởi tạo subagent qua tool agent/generic (Task, spawn agent, run agent, ...):
   - Đọc `agents/cat-reporter.md`, khởi tạo **một** subagent với nội dung file đó làm prompt.
   - Nhận báo cáo từ subagent, **truyền nguyên văn** cho chủ — không viết lại, không tóm tắt, không thêm bình luận.
2. Nếu không có subagent tool: thực hiện trực tiếp theo toàn bộ spec trong `agents/cat-reporter.md` trong context hiện tại.

**Vì sao**: các tác vụ thu thập web chạy trong context riêng của subagent, không chiếm context của agent chính. Cơ chế chỉ phụ thuộc khả năng "spawn subagent với prompt tự do" — có mặt trên hầu hết công cụ agent (ZCode, Claude Code, Codex, ...), nên skill chạy được ở mọi nơi.
