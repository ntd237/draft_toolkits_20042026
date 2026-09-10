---
name: english-exam-solver
description: "Giải đề tiếng Anh, TOEIC, IELTS với quy trình phân tích đề, kiểm chứng đáp án nhiều lớp, giải thích rõ ràng, ưu tiên độ chính xác tối đa và trung thực về mức độ chắc chắn. Triggers when the user asks to solve, answer, or grade English exam questions — grammar, vocabulary, reading comprehension, listening, TOEIC Parts 5/6/7, IELTS Reading/Writing, or general English exercises."
---

# Skill: english-exam-solver

## Language Protocol
- Respond in Vietnamese by default unless the user requests English output.
- Restate non-English requests in English before proceeding.
- Internal analysis in English; final response in Vietnamese with English technical terms where appropriate.

## Trigger
User submits an English exercise, test, or exam — grammar, vocabulary, collocation, pronunciation, stress, reading comprehension, cloze, error correction, sentence rewriting, TOEIC Part 5/6/7, IELTS Reading, IELTS Writing, listening-by-transcript, or mixed format — and needs accurate answers with explanations.

## Workflow

### Phase 1: Classify & Verify Input Completeness
**Objective**: Identify the question type and confirm enough context to solve it confidently.

- Determine the question type: grammar, vocabulary, collocation, pronunciation, stress, reading comprehension, cloze, error correction, sentence rewriting, TOEIC Part 5/6/7, IELTS Reading, IELTS Writing, listening-by-transcript, or mixed.
- Check whether the input has enough data: question text, passage, answer choices A/B/C/D, specific requirements, output constraints.
- If the question is missing context, blurry, cut off, or ambiguous, state what is missing before committing to a strong conclusion.

### Phase 2: Extract Linguistic Signals
**Objective**: Identify the decision-relevant language features before attempting an answer.

- Mark key clues: tense, word form, sentence structure, relative clauses, subject-verb agreement, prepositions, fixed collocations, nuance, connecting logic, register (formal/informal).
- For vocabulary and collocation, prioritize natural native-speaker usage over isolated dictionary definitions.
- For reading comprehension, classify the question type: main idea, detail, inference, reference, paraphrase, tone.
- For IELTS Writing or essay correction, separate analysis into 4 bands: Task Response, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy.

### Phase 3: Solve by Elimination
**Objective**: Derive the answer through principled elimination, not guesswork.

- Propose a candidate answer based on the best-fitting grammar rule or semantic match.
- Compare each option against the context to eliminate wrong answers: wrong word form, wrong collocation, wrong temporal logic, wrong register, wrong reference, wrong nuance, or unnatural.
- If two options are close, pinpoint the smallest distinguishing factor that decides the answer.
- For reading, use only information validly inferable from the text; do not add outside knowledge unless the question requires it.

### Phase 4: Multi-Layer Verification
**Objective**: Confirm the answer from at least two angles before finalizing.

- Cross-check via at least 2 lenses when possible: grammar rule + naturalness; literal meaning + context; elimination of wrong + proof of correct.
- For TOEIC/IELTS, ask: does this match real exam logic, or is it a "looks right" answer that is less natural?
- For sentence rewriting or error correction, verify the corrected sentence preserves the original meaning.
- For IELTS Writing grading, do not assign a band casually. Only give an estimated band when there is enough content, and state it is estimated.

### Phase 5: Output Per User Need
**Objective**: Match the response depth to what the user asked for.

- **Answer only**: short, accurate, consistent numbering.
- **Answer + brief explanation**: answer + the deciding signal.
- **Deep analysis**: why the answer is correct, why others are wrong, and a tip for recognizing this question type.
- **IELTS Writing grading/correction**: estimated band + 4-criteria feedback + errors to fix + suggested rewrite.
- If data is insufficient for high confidence, state the confidence level and what additional input is needed.

## Output Format

Choose the format matching the user's need:

- **Format 1 — Answer only**: `1. B | 2. D | 3. A`
- **Format 2 — Answer + brief explanation**:
  - `Câu 1: B`
  - `Lý do: ...`
- **Format 3 — Full analysis**:
  - `Đáp án đúng: ...`
  - `Dấu hiệu quyết định: ...`
  - `Vì sao các đáp án khác sai: ...`
  - `Mẹo nhận diện: ...`
- **Format 4 — IELTS Writing grading/correction**:
  - `Estimated band: ...`
  - `Nhận xét theo 4 tiêu chí: ...`
  - `Các lỗi cần sửa: ...`
  - `Bản sửa đề xuất: ...`

## Specialized Playbooks

### TOEIC Part 5 — Incomplete Sentences
**Mục tiêu**: Chọn đúng đáp án cho câu đơn hoặc câu ghép ngắn bằng cách nhận diện điểm kiểm tra chính của đề.

**Cách làm bắt buộc**:
- Xác định câu đang kiểm tra gì trước khi nhìn đáp án: từ loại, thì, bị động/chủ động, hòa hợp chủ vị, liên từ, giới từ, đại từ, mệnh đề quan hệ, hay collocation.
- Nhìn vào vị trí chỗ trống để dự đoán loại từ cần điền.
- Nếu các đáp án cùng từ gốc nhưng khác dạng, ưu tiên phân tích chức năng ngữ pháp của khoảng trống.
- Nếu các đáp án khác nghĩa, phải kiểm tra collocation, register công sở và logic ngữ cảnh.

**Bẫy thường gặp**:
- Chọn từ "nghe quen" nhưng sai từ loại.
- Chọn đáp án đúng ngữ pháp nhưng collocation không tự nhiên.
- Bỏ qua dấu hiệu thời gian hoặc chủ ngữ ở xa dẫn tới sai thì hoặc sai hòa hợp chủ vị.

**Checklist Part 5**:
- [ ] Đã xác định loại điểm ngữ pháp/từ vựng đang bị test
- [ ] Đã xác định loại từ cần điền
- [ ] Đã loại trừ từng đáp án sai bằng lý do cụ thể
- [ ] Đáp án cuối vừa đúng ngữ pháp vừa tự nhiên trong business English

### TOEIC Part 6 — Text Completion
**Mục tiêu**: Điền đúng từ/câu vào đoạn văn ngắn bằng cách kết hợp ngữ pháp câu và mạch logic toàn đoạn.

**Cách làm bắt buộc**:
- Đọc nhanh toàn đoạn trước để nắm chủ đề: email, memo, notice, article, instruction.
- Với câu hỏi điền từ, xử lý giống Part 5 nhưng phải kiểm tra thêm mạch ý trước và sau câu.
- Với câu hỏi điền câu, đánh giá chức năng câu cần thêm: mở thông tin mới, giải thích, chuyển ý, nhắc lại lịch trình, hay kết luận.
- Kiểm tra cohesion markers như `however`, `therefore`, `for example`, `in addition`, `as a result`.

**Bẫy thường gặp**:
- Chọn đáp án đúng ở mức câu nhưng phá vỡ mạch logic của đoạn.
- Chỉ nhìn một câu chứa chỗ trống mà bỏ qua câu trước/sau.
- Với điền câu, chọn câu có từ khóa giống đoạn nhưng không khớp chức năng diễn ngôn.

**Checklist Part 6**:
- [ ] Đã đọc toàn đoạn trước khi trả lời
- [ ] Đã kiểm tra logic trước, trong và sau chỗ trống
- [ ] Nếu là điền câu, đã xác định đúng chức năng của câu cần chèn
- [ ] Đáp án cuối giữ được độ mượt và mạch văn của cả đoạn

### TOEIC Part 7 — Reading Comprehension
**Mục tiêu**: Trả lời đúng câu hỏi đọc hiểu bằng chứng cứ trong văn bản, không suy diễn quá đà.

**Cách làm bắt buộc**:
- Xác định loại câu hỏi: detail, purpose, inference, vocabulary in context, reference, intent, main idea, information insertion, NOT/EXCEPT.
- Với single passage, xác định vị trí bằng chứng trước khi chọn đáp án.
- Với double/triple passage, phải map nguồn thông tin theo từng văn bản rồi mới tổng hợp.
- Nếu câu hỏi hỏi suy luận, chỉ chọn điều được hỗ trợ mạnh bởi văn bản, không chọn suy luận "có thể đúng ngoài đời".

**Bẫy thường gặp**:
- Chọn đáp án chứa từ giống bài nhưng đảo nghĩa hoặc thiếu điều kiện.
- Nhầm thông tin giữa 2-3 văn bản trong bộ câu hỏi.
- Với câu hỏi `What is suggested/implied`, suy luận quá xa khỏi dữ kiện.

**Checklist Part 7**:
- [ ] Đã xác định đúng loại câu hỏi
- [ ] Đã tìm được câu/đoạn làm bằng chứng
- [ ] Nếu là multi-passage, đã đối chiếu đúng văn bản nguồn
- [ ] Suy luận, nếu có, vẫn bám sát bằng chứng văn bản

### IELTS Reading
**Mục tiêu**: Giải câu hỏi học thuật bằng kỹ năng paraphrase, scanning, và phân biệt rõ giữa thông tin có, thông tin trái ngược, và thông tin không được nêu.

**Cách làm bắt buộc**:
- Xác định dạng câu hỏi: True/False/Not Given, Yes/No/Not Given, Matching Headings, Matching Information, Summary Completion, Sentence Completion, Multiple Choice, Matching Sentence Endings.
- Với TFNG/YNNG, áp dụng chuẩn:
  - `True/Yes`: Ý nghĩa khớp với bài.
  - `False/No`: Bài nói điều ngược lại.
  - `Not Given`: Bài không cung cấp đủ căn cứ để kết luận.
- Luôn tìm paraphrase thay vì chờ trùng từ.
- Với heading, tìm ý chính của đoạn chứ không chọn theo chi tiết nổi bật đơn lẻ.

**Bẫy thường gặp**:
- Nhầm `False` với `Not Given`.
- Bị đánh lừa bởi từ khóa bề mặt mà không đối chiếu nghĩa.
- Chọn heading theo một câu đầu/cuối thay vì toàn đoạn.

**Checklist IELTS Reading**:
- [ ] Đã xác định đúng dạng câu hỏi
- [ ] Đã map được keyword sang paraphrase trong bài
- [ ] Với TFNG/YNNG, đã phân biệt rõ "trái ngược" và "không được nêu"
- [ ] Không sử dụng kiến thức ngoài passage để trả lời

### IELTS Writing
**Mục tiêu**: Đánh giá hoặc hỗ trợ viết bài theo tiêu chí chấm thực tế, không chỉ sửa ngữ pháp bề mặt.

**Cách làm bắt buộc**:
- Xác định đúng task:
  - `Task 1 Academic`: mô tả biểu đồ/quy trình/bản đồ.
  - `Task 1 General`: letter.
  - `Task 2`: opinion, discussion, advantages-disadvantages, problem-solution, two-part question.
- Phân tích bài theo 4 tiêu chí: Task Response, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy.
- Nếu chấm band, phải nêu đây là `estimated band` và giải thích ngắn theo từng tiêu chí.
- Nếu sửa bài, tách rõ:
  - lỗi làm mất điểm
  - câu sửa mẫu
  - hướng viết lại tốt hơn

**Khung xử lý theo task**:
- `Task 1 Academic`: kiểm tra overview có nêu xu hướng chính không, có chọn số liệu nổi bật không, có tránh liệt kê máy móc không.
- `Task 1 General`: kiểm tra purpose, tone, bullet coverage, format letter phù hợp.
- `Task 2`: kiểm tra thesis rõ chưa, từng body paragraph có một ý trung tâm chưa, ví dụ có phục vụ lập luận không, kết luận có nhất quán không.

**Bẫy thường gặp**:
- Chấm điểm dựa chủ yếu vào grammar mà bỏ qua task achievement.
- Khen từ vựng "cao cấp" dù dùng sai collocation hoặc sai register.
- Sửa câu đẹp hơn nhưng làm đổi lập trường hoặc đổi dữ kiện gốc của người viết.

**Checklist IELTS Writing**:
- [ ] Đã xác định đúng loại task
- [ ] Đã đánh giá đủ 4 tiêu chí thay vì chỉ grammar
- [ ] Nếu chấm band, đã nêu rõ là estimated band
- [ ] Nếu sửa bài, đã giữ nguyên ý định giao tiếp và nghĩa gốc của người viết

### General English Exercises (phổ thông / đại học)
- Ưu tiên giải thích rõ dạng từ, mệnh đề, biến đổi câu, câu bị động, câu tường thuật, câu điều kiện, đảo ngữ, so sánh, liên từ.
- Khi phù hợp, rút ra quy tắc ngắn gọn để người học áp dụng cho câu tương tự.

## Format-Specific Output Add-ons

### Khi trả lời TOEIC Part 5/6/7
- `Câu X: [Đáp án]`
- `Dạng bẫy: [ngữ pháp / từ vựng / logic đoạn / inference ...]`
- `Dấu hiệu quyết định: ...`

### Khi trả lời IELTS Reading
- `Câu X: [Đáp án]`
- `Dạng câu hỏi: ...`
- `Bằng chứng / paraphrase then chốt: ...`

### Khi chấm hoặc sửa IELTS Writing
- `Task type: ...`
- `Estimated band: ...`
- `Nhận xét 4 tiêu chí: ...`
- `3 lỗi ưu tiên cần sửa: ...`
- `Bản sửa mẫu / outline đề xuất: ...`

## Don'ts
- Do not fabricate grammar rules or cite non-existent rules to force an answer.
- Do not guess blindly — if input is incomplete or audio is unclear, state the limitation instead of asserting confidently.
- Do not use absolute claims like "100% correct" when the evidence does not support it.
- Do not give vague explanations like "because it sounds more natural" without pointing to the specific structure, collocation, or contextual logic.
- Do not change the output style against the user's request — short when they need short, detailed when they need depth.
- Do not assign an IELTS band without reading enough content and comparing against the official criteria.
- Do not alter the original meaning when rewriting or correcting sentences.

## Quality Checklist
- [ ] Question type and output requirement correctly identified?
- [ ] Input completeness checked before concluding?
- [ ] Correct answer supported by at least one clear linguistic signal?
- [ ] Wrong options eliminated with specific reasons?
- [ ] No skipped steps or guesswork in the reasoning chain?
- [ ] Answer aligned with real TOEIC/IELTS exam logic or natural English usage?
- [ ] If uncertain, confidence level and missing data stated explicitly?
