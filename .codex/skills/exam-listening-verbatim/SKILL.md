---
name: exam-listening-verbatim
description: Exact verbatim transcription for IELTS, TOEIC, TOEFL, and similar listening-exam audio. Use when the user provides an audio file or asks to write out the full spoken content with maximum fidelity, preserving original wording, repetitions, fillers, numbers, spelled letters, and speaker turns without summarizing, translating, correcting, or inventing missing words.
---

# Exact Exam Listening Transcript

## Tổng quan

Dùng skill này khi người dùng gửi file audio của phần listening như IELTS, TOEIC, TOEFL hoặc bài nghe tương tự và muốn chép lại nguyên văn nội dung nghe được. Mục tiêu là trung thực tối đa với file gốc: không thêm, không bớt, không diễn giải, không dịch, không sửa ngữ pháp, không đoán bừa các đoạn không chắc.

## Ngôn ngữ và phong cách trả lời

- Dùng tiếng Việt khi trao đổi với người dùng.
- Giữ nguyên ngôn ngữ gốc trong phần transcript.
- Mặc định trả lời ngắn, đưa transcript trước, giải thích sau nếu thật sự cần.
- Nếu người dùng chỉ yêu cầu "chép lại", mặc định hiểu là transcript nguyên văn, không kèm đáp án hay giải nghĩa.

## Mục tiêu chính

- Chép lại toàn bộ lời nói trong file từ đầu đến cuối đầy đủ nhất có thể.
- Giữ nguyên từ ngữ, lặp lại, ngập ngừng, filler words, số, chữ cái đánh vần, thời gian, ngày tháng, địa chỉ, tên riêng và các chi tiết dễ sai.
- Ưu tiên độ chính xác hơn độ đẹp.
- Minh bạch mọi chỗ không thể xác minh thay vì đoán theo ngữ cảnh bài thi.

## Thông tin đầu vào cần có

Thu thập hoặc xác nhận các thông tin sau nếu có:

- File audio hoặc video có tiếng mà hệ thống thực sự truy cập được
- Yêu cầu định dạng đầu ra nếu người dùng có nêu: chỉ transcript, có timestamp, tách speaker, chia theo đoạn
- Chất lượng audio nếu người dùng đã biết trước có vấn đề

Nếu người dùng không nêu rõ format, mặc định dùng:

- Transcript nguyên văn
- Không dịch
- Không tóm tắt
- Không sửa câu chữ
- Không thêm nhãn speaker nếu audio không tự nêu danh tính và người dùng không yêu cầu

## Quy trình

### Giai đoạn 1: Xác nhận nguồn audio và khóa phạm vi đầu ra

**Objective**: Bảo đảm chỉ xử lý trên file audio thật sự có thể nghe được và chốt ngay từ đầu rằng đầu ra phải là transcript nguyên văn.

**Execution**:

**Step 1.1 - Xác nhận quyền truy cập audio**:
Kiểm tra xem file audio có thực sự khả dụng trong ngữ cảnh hiện tại hay không. Nếu không truy cập được file, định dạng không hỗ trợ hoặc không có âm thanh, nói rõ giới hạn đó và yêu cầu người dùng gửi lại file phù hợp. Không bao giờ giả vờ đã nghe được nội dung khi chưa truy cập được audio.

**Step 1.2 - Khóa chế độ transcript nguyên văn**:
Hiểu yêu cầu mặc định là chép nguyên văn. Không tự chuyển sang tóm tắt, dịch, giải thích, sửa ngữ pháp hoặc rút gọn cho "mượt" hơn nếu người dùng chưa yêu cầu riêng.

**Step 1.3 - Chốt chính sách xử lý chỗ không chắc**:
Đặt quy tắc rằng mọi chỗ không thể xác minh sau khi nghe lại phải được đánh dấu minh bạch ngay đúng vị trí, thay vì đoán theo ngữ cảnh bài thi, mẫu đề, đáp án hoặc xác suất ngôn ngữ.

**Deliverables must include**:
- Xác nhận đã có audio khả dụng hoặc nêu rõ vì sao chưa xử lý được
- Mặc định đầu ra được khóa là transcript nguyên văn
- Chính sách "không đoán bừa" được áp dụng ngay từ đầu

### Giai đoạn 2: Chép thô nguyên văn từ đầu đến cuối

**Objective**: Tạo bản chép thô đầy đủ, bao phủ toàn bộ file trước khi tinh chỉnh các đoạn khó nghe.

**Execution**:

**Step 2.1 - Nghe trọn file để lấy toàn cảnh**:
Đi qua toàn bộ audio một lượt để nắm cấu trúc, số speaker, vùng nhanh/chậm, đoạn nhiễu, chỗ có spelling, number dictation, địa chỉ, tên riêng hoặc chỉ dẫn bài thi.

**Step 2.2 - Chép nguyên văn theo đúng lời nói**:
Viết lại lời nói đúng như nghe thấy, giữ nguyên sự lặp lại, tự sửa câu của người nói, filler words như "uh", "um", "well", các đoạn đánh vần từng chữ, đọc số điện thoại, ngày tháng, giờ giấc và các dữ kiện ngắn dễ sai. Không tự làm sạch văn phong.

**Step 2.3 - Dùng dấu câu tối thiểu và thận trọng**:
Chỉ thêm dấu câu ở mức cần thiết để transcript đọc được. Dấu câu không được làm thay đổi ý nghĩa, thứ tự hoặc từ ngữ gốc.

**Deliverables must include**:
- Bản transcript thô bao phủ từ đầu đến cuối file
- Tất cả token dễ sai đã được giữ nguyên thay vì chuẩn hóa
- Không có đoạn nào bị lược bỏ chỉ vì nghe có vẻ không quan trọng

### Giai đoạn 3: Nghe lại có mục tiêu để xác minh

**Objective**: Giảm tối đa sai sót ở các vùng khó nghe và bảo đảm không có phần nào bị thêm hoặc thiếu.

**Execution**:

**Step 3.1 - Nghe lại các đoạn rủi ro cao**:
Replay kỹ các đoạn có nhiễu, tốc độ nhanh, accent nặng, speaker chồng tiếng hoặc chứa số, chữ cái, tên riêng, email, địa chỉ, giá tiền, ngày tháng, giờ giấc. Đây là các vùng có xác suất sai cao nhất trong bài nghe IELTS, TOEIC và các đề tương tự.

**Step 3.2 - Kiểm tra biên đầu và cuối cùng các chỗ chuyển speaker**:
Đối chiếu đầu file, cuối file và các đoạn chuyển người nói để tránh mất câu mở đầu, câu kết hoặc bỏ sót một lượt thoại ngắn. Nếu cần thể hiện đổi speaker, ưu tiên xuống dòng; chỉ gắn nhãn như `Speaker 1` hoặc `Speaker 2` khi người dùng yêu cầu hoặc audio tự xác định rõ.

**Step 3.3 - Xử lý bất định một cách trung thực**:
Nếu sau nhiều lượt nghe vẫn không xác minh được một đoạn, chèn đúng tại vị trí đó nhãn tối thiểu như `[không nghe rõ]` hoặc `[không chắc]`. Không tự bù từ còn thiếu bằng suy luận ngữ cảnh, mẫu đề, từ collocation quen thuộc hoặc đáp án có vẻ hợp lý.

**Deliverables must include**:
- Các đoạn rủi ro cao đã được nghe lại có mục tiêu
- Các vùng speaker-turn và biên file đã được rà soát
- Mọi bất định còn lại được đánh dấu minh bạch thay vì bị đoán bừa

### Giai đoạn 4: Xuất transcript cuối cùng

**Objective**: Trả ra bản transcript cuối cùng ở định dạng tối giản, đúng yêu cầu và không trộn thêm nội dung ngoài transcript.

**Execution**:

**Step 4.1 - Nếu audio rõ và xác minh được**:
Chỉ trả ra transcript nguyên văn. Không thêm phần mở đầu dài, không giải thích cách làm, không tóm tắt nội dung.

**Step 4.2 - Nếu còn vùng chưa xác minh được hoàn toàn**:
Vẫn trả transcript nguyên văn, giữ các nhãn bất định đúng chỗ. Sau transcript, chỉ thêm một ghi chú rất ngắn nêu rằng có một số đoạn không thể xác minh 100% và đề nghị người dùng gửi bản rõ hơn hoặc cắt clip ngắn hơn nếu muốn nghe lại chính xác tuyệt đối.

**Step 4.3 - Nếu người dùng yêu cầu thêm tác vụ khác**:
Nếu người dùng còn muốn dịch, tóm tắt, giải đề hoặc rút đáp án, luôn hoàn thành transcript nguyên văn trước hoặc tách phần đó thành mục riêng, không được làm lẫn với transcript gốc.

**Deliverables must include**:
- Một transcript cuối cùng đúng ngôn ngữ gốc của audio
- Không trộn lẫn transcript với tóm tắt hoặc diễn giải
- Ghi chú bổ sung chỉ xuất hiện khi thật sự cần vì còn vùng bất định

## Định dạng đầu ra

Mặc định, đầu ra phải theo thứ tự sau:

1. Transcript nguyên văn
2. Ghi chú ngắn về đoạn chưa xác minh, chỉ khi thực sự còn tồn tại

Template mặc định:

```text
[Transcript nguyên văn từ đầu đến cuối]

[Chỉ khi cần]
Ghi chú: Một số đoạn còn chưa thể xác minh 100%. Nếu bạn muốn, hãy gửi bản audio rõ hơn hoặc cắt riêng đoạn đó để mình chép lại chính xác hơn.
```

Nếu người dùng yêu cầu timestamp hoặc tách speaker, áp dụng đúng yêu cầu đó nhưng vẫn phải giữ nguyên văn nội dung lời nói.

## Quality Checklist

- [ ] Đã xác nhận audio thực sự khả dụng trước khi chép
- [ ] Transcript bao phủ toàn bộ file từ đầu đến cuối
- [ ] Không có tóm tắt, dịch, diễn giải hoặc làm sạch câu chữ lẫn vào transcript
- [ ] Các chi tiết dễ sai như số, chữ cái đánh vần, tên riêng, ngày giờ đã được rà lại
- [ ] Các chỗ lặp lại, filler words, false starts không bị tự ý xóa
- [ ] Không có từ nào được đoán bừa để lấp chỗ trống
- [ ] Mọi vùng chưa xác minh được đều được đánh dấu minh bạch

## Expected Results

- Người dùng nhận được transcript gần nhất với nội dung gốc của file audio
- Không có nội dung bịa thêm từ suy luận ngữ cảnh
- Các giới hạn về chất lượng audio được nêu rõ khi ảnh hưởng đến độ chính xác

## Important Rules

### Required Practices

- Luôn ưu tiên độ trung thực với audio gốc hơn độ đẹp của transcript.
- Luôn giữ nguyên ngôn ngữ gốc của file trong phần transcript.
- Luôn rà lại kỹ các đoạn có số, spelling, tên riêng, địa chỉ, ngày tháng và thời gian.
- Luôn minh bạch bất định bằng nhãn ngắn đúng vị trí nếu không thể xác minh.
- Luôn tách transcript nguyên văn khỏi mọi tác vụ phụ như dịch, giải thích, tóm tắt hoặc đáp án.
- Luôn nói rõ khi môi trường hiện tại không thật sự truy cập hoặc xử lý được audio.

### Prohibited Practices

- Không được tóm tắt thay cho transcript.
- Không được dịch hoặc diễn giải khi người dùng chỉ yêu cầu chép lại.
- Không được sửa ngữ pháp, làm sạch spoken English hoặc bỏ bớt phần lặp lại cho "đẹp".
- Không được suy đoán từ còn thiếu dựa trên mẫu đề, ngữ cảnh câu hỏi hoặc đáp án nghe có vẻ hợp lý.
- Không được thêm tên speaker, tiêu đề, chú giải dài hoặc metadata không được yêu cầu.
- Không được giả vờ đã nghe được file khi thực tế chưa truy cập hoặc chưa xử lý được audio.

## Best Practices Summary

**Verbatim first**: transcript phải trung thành với lời nói gốc trước khi nghĩ đến bất kỳ tác vụ phụ nào.
**No guessing**: chỗ nào không chắc thì đánh dấu minh bạch, không được lấp bằng suy luận.
**High-risk tokens**: số, spelling, tên riêng và thời gian phải được nghe lại kỹ vì đây là nhóm sai nhiều nhất trong audio bài thi.
