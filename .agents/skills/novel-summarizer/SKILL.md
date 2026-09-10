---
name: novel-summarizer
description: "Đọc và tóm tắt chi tiết, chính xác nội dung từng chương và dải chương tiểu thuyết (web novel, kiếm hiệp, tiên hiệp, huyền huyễn, light novel) từ đường link hoặc dải URL yêu cầu. Triggers when the user provides a novel URL or a URL pattern with a chapter range (e.g. chương 5 đến chương 8) and wants a structured, high-fidelity summary covering the whole range without missing key events."
---

# Skill: novel-summarizer

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English before proceeding.
- Internal analysis in English; final summary in Vietnamese with original proper-noun terms preserved (Hán-Việt or original transliteration).

## Trigger
User provides a novel link (or a URL pattern and a chapter range, e.g. from chapter `05` to chapter `08`) for a novel — tiên hiệp, huyền huyễn, ngôn tình, kiếm hiệp, đô thị, light novel, etc. — and needs a summary that covers the entire range with per-chapter detail.

## Workflow

### Phase 1: Resolve URL Pattern & Build Chapter List
**Objective**: Determine the URL pattern for the requested chapter range.

- Parse the sample link to find the chapter-number position:
  - Integer form: `.../chuong-5.html` → `.../chuong-6.html`, `.../chuong-7.html`
  - Zero-padded form: `.../c05` → `.../c06`, `.../c07`
  - Slug form with title: if the URL includes the chapter title (e.g. `chuong-5-khoi-dau`), attempt to fetch the first chapter or find the next-chapter link from the current chapter's HTML.
- Build the list of URLs to visit from $N_{start}$ to $N_{end}$.

### Phase 2: Retrieve Content Per Chapter
**Objective**: Fetch the raw text content for each chapter in the range.

- Use `read_url_content` to retrieve the raw text content of each link in the range.
- Validate the returned data:
  - **Success**: extract the chapter title and full body text.
  - **Error** (404, 403, Cloudflare, paywall, or empty content): record the error for that chapter. If the obstacle cannot be bypassed, report clearly to the user which chapter failed and suggest they paste the raw text of that chapter directly.

### Phase 3: Pre-Process & Extract Facts
**Objective**: Separate story content from noise and capture key entities.

- Remove all noise: translator/converter notes, web ads, previous/next chapter links, comments.
- Identify and note key entities:
  - **Characters**: main characters, supporting characters, antagonists appearing or mentioned.
  - **Locations & Setting**: where events occur, time, related factions.
  - **Preserve proper nouns**: keep character names, place names, techniques, cultivation realms, items in their original form (Hán-Việt or original phonetic form), consistent across chapters.

### Phase 4: Structured Summarization
**Objective**: Build a per-chapter summary with 4 components and an arc overview.

For each chapter, produce:
1. **Chapter title & info**: chapter number and name (if available).
2. **Characters & Locations**: the key entities appearing in the chapter.
3. **Main events**: sequential timeline (3–6 concise bullets capturing key points).
4. **Highlights & Cliffhanger**: narrative technique (foreshadowing/plot twist), unexpected event, or open question at chapter end.

Then build the **Arc Overview**: a short 1-2 paragraph summary of the plot progression across the full range from first to last chapter.

### Phase 5: Fidelity Check & Output
**Objective**: Verify the summary against the source before delivery.

- Run the Quality Checklist. Confirm no fabrication, no name confusion, no missing key events.
- Output the complete result in Markdown format (see Output Format below).

## Output Format

```markdown
# 📖 TÓM TẮT TIỂU THUYẾT: [TÊN TRUYỆN] (NẾU XÁC ĐỊNH ĐƯỢC)
> **Dải chương**: Từ Chương [X] đến Chương [Y] | **Tổng số chương**: [Z] chương

---

## 🌟 TỔNG QUAN DẢI CHƯƠNG [X] - [Y]
*(Tóm tắt cô đọng 1–2 đoạn văn về diễn biến cốt truyện chính, bước ngoặt lớn và tiến trình phát triển của dải chương này).*

---

## 📜 CHI TIẾT TỪNG CHƯƠNG

### 🔹 Chương [X]: [Tên Chương]
- **📍 Bối cảnh & Nhân vật**: [Địa điểm diễn ra] | [Các nhân vật xuất hiện chính]
- **⚡ Diễn biến chính**:
  - [Sự kiện 1: Khởi đầu chương hoặc tiếp nối diễn biến trước...]
  - [Sự kiện 2: Biến cố/xung đột/cuộc đối thoại quan trọng...]
  - [Sự kiện 3: Hành động quyết định hoặc kết quả giải quyết...]
- **🎯 Điểm nhấn / Kết chương**: [Tình huống kết thúc, cú twist hoặc câu hỏi mở ở cuối chương].

*(Lặp lại cấu trúc trên cho các chương tiếp theo trong dải)*

---

## 🔑 ĐIỂM NHẤN CỐT TRUYỆN & TIẾN TRIỂN NHÂN VẬT
- **Chuyển biến nhân vật**: [Sự thay đổi về tâm lý, cảnh giới, sức mạnh hoặc quan hệ giữa các nhân vật].
- **Thế lực & Mối quan hệ**: [Liên minh mới, kẻ thù xuất hiện hoặc mâu thuẫn mới nảy sinh].
- **Manh mối / Hố chưa lấp (Foreshadowing)**: [Các chi tiết bí ẩn được tác giả cài cắm cho các chương sau].
```

## Don'ts
- Do not fabricate plot content for chapters that failed to load or were never read — report the gap instead.
- Do not write one-line shallow summaries like "Chương này nhân vật A đánh nhau với nhân vật B rồi thắng" without context or cause.
- Do not mix analysis/foreshadowing into the main event section — place interpretive notes in the dedicated Foreshadowing section.
- Do not translate or alter proper nouns (names, techniques, cultivation realms, items) in ways that shift their meaning.
- Do not include web noise (watermarks, translator credits, ads) in the summary.
- Do not reorder events against the chapter's original timeline.

## Quality Checklist
- [ ] All chapters in the requested range ($N_{start}$ to $N_{end}$) read?
- [ ] Proper nouns, forms of address, and terminology accurate and consistent across chapters?
- [ ] Each chapter's main events cover the key plot points?
- [ ] Summary events clearly separated from analysis/character progression notes?
- [ ] Any failed chapters reported to the user without fabricated replacement content?
