---
name: yolo-dataset-bootstrap
description: Lập quy trình bootstrap dataset YOLO thực chiến cho bộ ảnh lớn, gồm cỡ seed set, auto-annotation, ngưỡng confidence, hàng đợi review, QA sampling và active learning với CVAT, Label Studio hoặc Roboflow.
---

# YOLO Dataset Bootstrap

## Tổng quan

Dùng skill này khi người dùng muốn có một kế hoạch nhanh, thực tế để gán nhãn hoặc làm sạch một bộ dữ liệu YOLO lớn với ít công sức thủ công nhất có thể. Trọng tâm là biến một seed set nhỏ nhưng chất lượng thành một dataset lớn hơn đã qua review bằng auto-annotation, chia luồng theo confidence, QA lấy mẫu và 2-3 vòng retrain.

## Ngôn ngữ và phong cách trả lời

- Dùng cùng ngôn ngữ với người dùng.
- Giữ tên tool và model bằng tiếng Anh khi như vậy rõ nghĩa hơn.
- Ưu tiên hướng dẫn thiên về hành động hơn là lý thuyết.
- Mặc định đưa ra khoảng giá trị, ngưỡng và bước tiếp theo thật cụ thể thay vì lời khuyên chung chung.

## Khi nào nên dùng skill này

Dùng skill này khi người dùng hỏi về một trong các tình huống sau:

- Quy trình gán nhãn nhanh cho 1k-100k ảnh YOLO
- Chiến lược bootstrapping hoặc pseudo-labeling cho detection dataset
- Cách setup auto-annotation bằng CVAT, Label Studio hoặc Roboflow
- Cách chia ngưỡng confidence cho các hàng đợi accept / review / reject
- Cách chọn cỡ seed set, chiến lược lấy mẫu hoặc giảm khối lượng review tay
- Vòng lặp active learning để cải thiện chất lượng dataset qua nhiều vòng
- Chiến lược QA để phát hiện lỗi auto-label có tính hệ thống

## Mục tiêu chính

Tạo ra một pipeline annotation thực tế, cân bằng giữa tốc độ, chất lượng nhãn và chi phí review. Câu trả lời cần giúp người dùng quyết định:

- nên gán nhãn trước bao nhiêu ảnh
- nên train baseline đầu tiên như thế nào
- nên auto-label phần ảnh còn lại ra sao
- nên chia prediction theo confidence thế nào
- nên review và QA sao cho hiệu quả
- khi nào nên retrain và khi nào nên dừng vòng lặp

## Thông tin đầu vào cần có

Thu thập các thông tin sau nếu có. Nếu thiếu một phần, hãy đưa ra giả định hợp lý và nêu rõ giả định đó.

- Kích thước dataset
- Loại bài toán: detection, segmentation hay pose
- Số lượng class
- Độ khó giữa các class và mức mất cân bằng class
- Kích thước object và mật độ object trên mỗi ảnh
- Mức đa dạng của domain: góc chụp, ánh sáng, nền, thời tiết, motion blur
- Có nhãn sẵn hay có baseline model sẵn hay không
- Quy mô team annotation và năng lực review
- Metric mục tiêu hoặc mức chấp nhận false positive / false negative
- Ràng buộc về tool: self-hosted, ít setup, trả phí hay miễn phí

Chỉ hỏi thêm những thông tin thật sự cần thiết để tránh đưa ra lời khuyên sai hướng. Nếu người dùng đang cần câu trả lời vận hành nhanh, hãy tiếp tục với các giả định hợp lý thay vì chặn lại để hỏi quá nhiều.

## Quy trình

### Giai đoạn 1: Xác định phạm vi và quyết định bootstrap

**Objective**: Xác định xem workflow bootstrap bằng seed set có phù hợp không và ước lượng cỡ batch gán nhãn đầu tiên một cách thực tế.

**Execution**:

**Step 1.1 - Phân tích dataset**:
Xác định loại bài toán, số lượng class, độ đa dạng dữ liệu và mức độ khó dự kiến. Chỉ rõ các yếu tố khiến auto-annotation dễ hoặc khó hơn, ví dụ detection một class, object rất nhỏ, cảnh đông hoặc bị che khuất nhiều.

**Step 1.2 - Ước lượng seed set**:
Đề xuất batch gán nhãn tay ban đầu. Dùng khoảng 300-800 ảnh làm mốc thực tế mặc định cho object detection. Chỉ nghiêng về đầu thấp nếu bài toán rất đơn giản, ít biến thiên và chỉ có một class. Nghiêng về đầu cao nếu có nhiều class, nhiều tình huống long-tail hoặc môi trường khó.

**Step 1.3 - Đặt tiêu chí đủ tốt cho vòng đầu**:
Xác định mức chất lượng chấp nhận được của model đầu tiên: precision đủ để auto-label các mẫu dễ, recall đủ để kéo ra các object có khả năng đúng cho hàng review. Nêu rõ đây là model bootstrap, chưa phải model cuối cùng.

**Deliverables must include**:
- Tóm tắt độ khó của dataset
- Kích thước seed set được đề xuất kèm giải thích
- Kết luận rõ ràng có nên dùng auto-annotation hay không

### Giai đoạn 2: Tạo seed set và train baseline

**Objective**: Tạo một batch gán nhãn đầu tiên đủ đa dạng và train baseline model đủ tốt để tăng tốc cho vòng tiếp theo.

**Execution**:

**Step 2.1 - Tạo seed set đa dạng**:
Hướng dẫn người dùng lấy mẫu phủ được nhiều góc chụp, điều kiện sáng, background, khoảng cách, kích thước object và các edge case hiếm. Cảnh báo rằng seed set quá hẹp sẽ tạo ra auto-label bị lệch và làm tốn thời gian review ở các vòng sau.

**Step 2.2 - Gán nhãn seed set cẩn thận**:
Ưu tiên tính nhất quán của annotation hơn là tốc độ trong vòng đầu. Nếu định nghĩa class còn mơ hồ, yêu cầu chốt rule gán nhãn trước khi scale lên số lượng lớn.

**Step 2.3 - Train baseline nhanh**:
Đề xuất một vòng train ngắn ban đầu, thường khoảng 30-80 epochs cho baseline YOLO, vừa đủ để sinh prediction hữu ích cho bước chia luồng. Nhắc rõ số epochs cụ thể còn phụ thuộc vào tốc độ hội tụ, số class và mức augmentation.

**Deliverables must include**:
- Kế hoạch lấy mẫu cho seed set
- Cảnh báo về rủi ro annotation không nhất quán
- Khuyến nghị train baseline với khoảng epochs thực tế

### Giai đoạn 3: Auto-annotation và chia luồng theo confidence

**Objective**: Dùng baseline model để gán nhãn cho phần dữ liệu còn lại và chia prediction vào các hàng đợi giúp giảm công review tay.

**Execution**:

**Step 3.1 - Auto-label phần dữ liệu chưa gán nhãn**:
Khuyến nghị chạy baseline model trên toàn bộ phần ảnh còn lại bằng tool stack mà người dùng chọn. Nếu người dùng cần tư vấn tool, ưu tiên CVAT khi cần review workflow tốt, Label Studio khi cần pipeline linh hoạt và Roboflow Auto Label khi cần tốc độ cùng ít công setup.

**Step 3.2 - Áp dụng chính sách confidence ban đầu**:
Dùng một chính sách chia luồng thực tế như sau:
- `> 0.6`: accept or fast-pass
- `0.3-0.6`: send to manual review queue
- `< 0.3`: ignore, defer, or review selectively

Nêu rõ đây chỉ là ngưỡng khởi điểm, không phải chân lý cố định cho mọi bài toán. Có thể siết chặt hoặc nới lỏng dựa trên độ rủi ro của class, mức chấp nhận false positive và kết quả quan sát bằng mắt.

**Step 3.3 - Chia theo mức rủi ro, không chỉ theo confidence**:
Với class quan trọng, lỗi dự đoán gây tốn kém hoặc object quá nhỏ, khuyến nghị ngưỡng chặt hơn và review tay nhiều hơn ngay cả khi confidence nhìn có vẻ cao.

**Deliverables must include**:
- Đề xuất hướng dùng tool cho auto-annotation
- Chính sách chia luồng theo confidence thật cụ thể
- Ghi chú về thời điểm cần override ngưỡng theo mức rủi ro của class

### Giai đoạn 4: Review, QA và chặn lỗi lan rộng

**Objective**: Ngăn lỗi nhãn có tính hệ thống lan ra toàn bộ dataset.

**Execution**:

**Step 4.1 - Review hàng đợi không chắc chắn trước**:
Ưu tiên các ảnh có confidence trung bình, cảnh đông và những class mà model đang yếu. Giải thích rằng các chỉnh sửa này thường đem lại mức cải thiện lớn nhất ở vòng retrain kế tiếp.

**Step 4.2 - QA một phần nhãn đã auto-accept**:
Khuyến nghị audit 5-10% phần dữ liệu đã auto-accept để phát hiện lỗi có tính hệ thống trước khi chúng lan rộng.

**Step 4.3 - Theo dõi mẫu lỗi lặp lại**:
Nếu model liên tục bỏ sót một class, vẽ box lỏng, gộp nhiều instance thành một hoặc hallucinate trên vài loại background nhất định, hướng dẫn tạo một nhóm review mục tiêu và đưa nhóm này vào vòng train tiếp theo.

**Deliverables must include**:
- Thứ tự ưu tiên review
- Khuyến nghị QA lấy mẫu
- Danh sách ngắn các lỗi có tính hệ thống cần theo dõi

### Giai đoạn 5: Retraining và vòng lặp active learning

**Objective**: Biến các nhãn đã review thành mức cải thiện đo được thông qua một số vòng retrain có trọng tâm.

**Execution**:

**Step 5.1 - Retrain trên dữ liệu đã làm sạch**:
Khuyến nghị retrain sau mỗi batch review có ý nghĩa thay vì chờ đến khi toàn bộ dataset hoàn hảo.

**Step 5.2 - Lặp lại 2-3 vòng**:
Dùng 2-3 vòng active learning làm khuyến nghị mặc định. Giải thích rằng sau vài vòng, mức cải thiện biên thường giảm dần và chi phí review sẽ trở thành yếu tố chi phối.

**Step 5.3 - Xác định điều kiện dừng**:
Dừng khi phần auto-accept ổn định và sạch, khối lượng review đã ở mức kiểm soát được, và các batch review mới chỉ mang lại cải thiện nhỏ.

**Deliverables must include**:
- Khuyến nghị nhịp retrain
- Số vòng active learning đề xuất
- Điều kiện dừng rõ ràng

## Hướng dẫn chọn tool

- **CVAT**: Lựa chọn mặc định tốt nhất khi người dùng cần auto-annotation đi kèm review workflow mạnh cho team.
- **Label Studio**: Phù hợp khi người dùng cần pipeline linh hoạt và dễ tùy biến.
- **Roboflow Auto Label**: Phù hợp khi người dùng cần triển khai nhanh, ít setup và chấp nhận phương án trả phí được quản lý sẵn.

Nếu người dùng không chỉ định tool, hãy đề xuất một tool và giải thích ngắn gọn vì sao nó hợp với tốc độ, chi phí setup và ngân sách của team.

## Tài liệu tham chiếu đi kèm

Load `references/thresholds-and-tooling.md` khi cần các heuristic dùng lại được cho cỡ seed set, khoảng epochs vòng đầu, ngưỡng confidence, tỷ lệ QA sampling hoặc trade-off giữa các tool.

## Định dạng đầu ra

Khi dùng skill này, hãy sắp xếp câu trả lời theo thứ tự sau:

1. Tóm tắt tình huống
2. Workflow đề xuất
3. Chính sách confidence-threshold
4. Khuyến nghị tool
5. QA và kiểm soát rủi ro
6. Các bước cần làm ngay

Nếu người dùng muốn câu trả lời thật ngắn, hãy nén cùng logic đó thành một action plan súc tích nhưng không được bỏ phần threshold, QA hoặc hướng dẫn retraining.

## Checklist chất lượng

- [ ] Khuyến nghị có cỡ seed set cụ thể hoặc một khoảng rõ ràng
- [ ] Vòng train đầu tiên được mô tả là baseline để bootstrap, không phải model cuối
- [ ] Câu trả lời có chính sách confidence-triage rõ ràng
- [ ] Câu trả lời có QA sampling cho phần prediction auto-accept
- [ ] Câu trả lời có 2-3 vòng retraining / active learning
- [ ] Phần tư vấn tool gắn với nhu cầu workflow, không liệt kê chung chung
- [ ] Có nêu rủi ro từ seed set thiếu đa dạng hoặc lỗi có tính hệ thống
- [ ] Giả định được nêu rõ khi đầu vào của người dùng còn thiếu

## Quy tắc quan trọng

### Điều bắt buộc

- Luôn đưa ra workflow khởi điểm cụ thể, không chỉ nói best practice chung chung.
- Luôn có khuyến nghị về seed set và giải thích yếu tố làm thay đổi con số đó.
- Luôn đưa ra hướng dẫn confidence-threshold như heuristic khởi điểm.
- Luôn có chính sách review tay và chính sách QA lấy mẫu.
- Luôn nhắc rằng threshold cần được hiệu chỉnh bằng quan sát thực tế và mức rủi ro của từng class.
- Luôn tối ưu đồng thời cho tốc độ và chất lượng nhãn, không chỉ nhìn vào metric train model.

### Điều cấm làm

- Không được mặc định khuyên gán nhãn tay toàn bộ dataset.
- Không được coi một ngưỡng confidence cố định là đúng cho mọi bài toán.
- Không được bỏ qua QA cho phần auto-accepted.
- Không được giả định seed set là đủ tốt nếu nó thiếu đa dạng bối cảnh.
- Không được khuyên dùng tool mà không giải thích trade-off của workflow.
- Không được chỉ tập trung vào mAP mà bỏ qua tính nhất quán của annotation và chi phí review.

## Tóm tắt best practices

Hãy bootstrap thật nhanh bằng một seed set nhỏ nhưng đa dạng, train baseline sớm, auto-label phần lớn mẫu dễ, review nhóm không chắc chắn, audit một phần dữ liệu đã accept và retrain theo các vòng ngắn cho đến khi khối lượng review không còn giảm thêm đáng kể.
