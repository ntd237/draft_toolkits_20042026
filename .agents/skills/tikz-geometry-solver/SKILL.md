---
name: tikz-geometry-solver
description: Giải bài toán hình học phẳng kèm vẽ hình TikZ chuẩn xác 100%. Kích hoạt khi người dùng đưa đề toán hình học (tam giác, đường tròn, tứ giác, hình học giải tích 2D) yêu cầu vẽ hình bằng TikZ/LaTeX và/hoặc giải bài. Từ khoá: "vẽ hình tikz", "giải hình", "đề hình", "TikZ figure", "geometry problem draw and solve". Sinh hình TikZ compile-pass + lời giải đầy đủ có kiểm chứng chéo.
---

# Skill: tikz-geometry-solver

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first. Internal analysis in English.

## Trigger
Kích hoạt khi đầu vào là một đề bài hình học phẳng (văn bản, hoặc ảnh đề kèm hình) và người dùng cần (a) hình vẽ TikZ chuẩn xác theo dữ kiện, (b) lời giải, hoặc cả hai. Không kích hoạt với hình học không gian 3D (báo giới hạn 1 câu và vẫn xử lý phần 2D nếu tách được).

## Workflow

### Phase 1 — Phân tích đề
**Objective**: Trích xuất toàn bộ dữ kiện hình học thành danh sách ràng buộc có thể kiểm tra được.

- Restate đề bài in English internally; giữ nguyên ký hiệu điểm của đề (A, B, C, O, ...).
- Liệt kê 3 nhóm: **đối tượng** (điểm, đoạn, đường thẳng, đường tròn, tam giác...), **dữ kiện cho trước** (số đo cạnh/góc, vuông, song song, tiếp xúc, qua điểm...), **yêu cầu** (tính gì, chứng minh gì).
- Mỗi dữ kiện viết thành 1 mệnh đề kiểm tra được, ví dụ: "AB = 5 → |AB| = 5", "OI ⊥ AB → (O−I)·(B−A) = 0". Bảng này là nguồn sự thật duy nhất cho các phase sau.
- Nếu đề thiếu dữ kiện hoặc mâu thuẫn: nêu rõ dữ kiện nào thiếu/mâu thuẫn, hỏi hoặc đánh dấu ẩn số — không tự bịa số.

### Phase 2 — Dựng toạ độ
**Objective**: Tính toạ độ chính xác của mọi điểm từ ràng buộc, không ước lượng cảm tính.

- Chọn hệ toạ độ thuận lợi: cạnh chính nằm trên trục Ox, gốc tại đỉnh góc vuông, hoặc trục đối xứng là Oy. Nêu lý do chọn trong 1 câu.
- Tính toạ độ **chính xác** (phân số, căn thức) khi được; nếu hệ phương trình không giải được chính xác thì giải số với sai số ≤ 1e-6 và ghi rõ phương pháp. Công thức chuẩn xem `references/coordinate-method.md`.
- **Bắt buộc**: lập bảng kiểm tra — mỗi ràng buộc ở Phase 1 phải được thay số kiểm chứng (ví dụ tính lại |AB|, tích vô hướng, khoảng cách tâm-bán kính). Ràng buộc nào chưa pass thì chưa được sang Phase 3. Với bài có đường tròn: mỗi quan hệ tiếp xúc (đường tròn–đường tròn, đường tròn–cạnh) là một dòng kiểm tra riêng — xem `references/tikz-techniques.md`, mục "Quy tắc đường tròn & tiếp xúc".
- Nếu hệ vô nghiệm/đa nghiệm: dừng, báo lại người dùng thay vì chọn bừa nghiệm.

### Phase 3 — Sinh TikZ
**Objective**: Sinh hình TikZ thuần, dùng đúng toạ độ Phase 2, thể hiện đúng mọi dữ kiện.

- Chỉ dùng TikZ thuần + các library chuẩn: `calc`, `angles`, `quotes`, `intersections`, `arrows.meta`, `decorations.markings`, `patterns`. Không dùng tkz-euclide, GeoGebra export, pstricks.
- Preamble và các snippet chuẩn (dấu góc vuông, dấu bằng đoạn, hình tròn, label) xem `references/tikz-techniques.md`.
- Tuân thủ nghiêm **Quy tắc nét vẽ** và **Quy tắc label điểm** trong `references/tikz-techniques.md`: nét đứt chỉ dành cho đường phụ (đường cao, hình chiếu, kéo dài) — mọi đối tượng dữ kiện là nét liền; label không được bị bất kỳ đường nào cắt qua, hai điểm gần nhau thì label đặt theo hai hướng đối nhau.
- Toạ độ các điểm chép nguyên văn từ Phase 2 — không làm tròn khi vẽ (nếu phải làm tròn, giữ ≥ 4 chữ số thập phân).
- Thứ tự vẽ: fill/màu nền → đường → điểm → label → dấu ký hiệu (góc vuông, dấu bằng, mũi tên song song).
- Mọi dữ kiện hình ảnh (vuông, tiếp xúc, song song, trung điểm) phải có ký hiệu tương ứng trên hình.

### Phase 4 — Compile & verify
**Objective**: Compile-pass tuyệt đối và đối chiếu hình với dữ kiện đề.

- Compile bằng `scripts/compile_tikz.js` (Node.js, không cần package ngoài; tự dò `pdflatex`/`tectonic`, xuất PDF + PNG). Sửa lỗi và lặp cho đến khi exit code = 0.
- Trong môi trường web có runtime LaTeX: dùng runtime đó thay script, cùng tiêu chí compile-pass.
- Mở PNG và đối chiếu lần cuối với bảng ràng buộc Phase 1: góc vuông có vuông, đường tiếp tuyến chạm đúng điểm, tỉ lệ cạnh đúng dữ kiện, **các đường tròn nhìn thấy là tiếp xúc nhau và tiếp xúc cạnh**. Hình lệch dữ kiện → quay lại Phase 2 sửa toạ độ (không "nắn" hình tay).
- Kiểm tra trình bày hình trên PNG: nét đứt chỉ xuất hiện ở đường phụ, không label nào bị đường cắt qua, không hai label chồng nhau, **cung góc là cung nhỏ đúng số đo (không bị góc phản xạ vẽ thành vòng tròn)**. Vi phạm → quay lại Phase 3 sửa style/vị trí label (toạ độ đã đúng nên không đụng Phase 2).
- Nếu máy/web không có engine nào: giao `.tex` kèm 1 câu "chưa compile được vì thiếu LaTeX" và đánh dấu `<!-- UNVERIFIED-COMPILE -->` trên đầu file.

### Phase 5 — Giải & trình bày
**Objective**: Lời giải đầy đủ, đáp số được kiểm chứng bằng ≥ 2 cách.

- Giải từng bước, mỗi bước nêu định lý/định nghĩa dùng (Pythagoras, định lý cosin, tính chất tiếp tuyến...), dẫn từ dữ kiện đã liệt kê ở Phase 1.
- **Kiểm chứng chéo**: đáp số phải xác nhận được bằng cách thứ hai độc lập (ví dụ: tính bằng toạ độ so với lập luận tổng hợp, hoặc thay số ngược vào ràng buộc). Không khớp → giải lại trước khi trình bày.
- Ghi lời giải vào `solution.tex` (hình + lời giải), tóm tắt đáp số trong hội thoại.

## Output Format

```
<workdir>/tikz-solution/
├── hinh.tex        # standalone tikzpicture (nếu chỉ cần hình)
├── solution.tex    # hình + lời giải đầy đủ
├── solution.pdf    # kết quả compile
└── hinh.png        # ảnh render để xem nhanh
```

Trong hội thoại tóm tắt: (1) bảng ràng buộc → kết quả kiểm tra, (2) bảng toạ độ điểm, (3) đáp số + cách kiểm chứng chéo, (4) link file.

## Don'ts
- Không tự suy diễn/bịa dữ kiện khi đề thiếu — báo thiếu và hỏi.
- Không dùng toạ độ "nhìn là giống" — mọi điểm phải đi qua bảng kiểm Phase 2.
- Không dùng thư viện vẽ hình tự động (tkz-euclide, GeoGebra, Sage) — chỉ TikZ thuần.
- Không giao file chưa compile-pass khi môi trường có sẵn LaTeX engine.
- Không xử lý hình học 3D/không gian (ngoài scope — nêu 1 câu và xử lý phần 2D được tách ra).

## Quality Checklist
- [ ] Mỗi dữ kiện đề xuất hiện ở đúng 1 dòng bảng Phase 1 và có 1 phép kiểm tra pass.
- [ ] Bảng toạ độ Phase 2 có đầy đủ mọi điểm xuất hiện trên hình.
- [ ] `compile_tikz.js` (hoặc runtime web) exit code 0.
- [ ] PNG đối chiếu: mọi thuộc tính given (vuông/tiếp xúc/song song/tỉ lệ) hiển thị đúng.
- [ ] Nét đứt chỉ dùng cho đường phụ; mọi đối tượng dữ kiện vẽ nét liền.
- [ ] Cung góc vẽ là cung nhỏ đúng số đo — thứ tự chân góc đã được kiểm tra theo chiều quét ngược kim đồng hồ của `pic {angle}`.
- [ ] Mọi đường tròn: tâm + bán kính chép ≥ 6 chữ số từ bảng Phase 2; mỗi quan hệ tiếp xúc có dòng kiểm tra |C₁C₂| = r₁±r₂ hoặc d(tâm, cạnh) = r pass với sai số ≤ 1e-6.
- [ ] Không label nào bị đường cắt ngang; không có hai label chồng nhau (điểm gần nhau đặt label hướng đối nhau).
- [ ] Đáp số khớp giữa ≥ 2 phương pháp độc lập.
- [ ] File `.tex` không chứa toạ độ hoặc nhãn không có trong bảng Phase 2.
