# Coordinate Method — dựng toạ độ từ dữ kiện

## 1. Chọn hệ toạ độ

| Dữ kiện đề | Chọn hệ |
|---|---|
| Tam giác với cạnh AB cho trước | A = (0,0), B = (c,0) trên Ox |
| Góc vuông tại A | A = (0,0), hai cạnh góc vuông = hai trục |
| Hình đối xứng (đều/cân) | Trục đối xứng = Oy, gốc tại đáy hoặc trọng tâm |
| Đường tròn tâm O bán kính R | O = (0,0), R giữ nguyên — không scale |

Mục tiêu: số ẩn toạ độ tự do ít nhất, phép tính ra số tròn khi được.

## 2. Công thức tính điểm chuẩn

Cho A(x₁,y₁), B(x₂,y₂), t = |AB|:

- **Trung điểm**: M = ((x₁+x₂)/2, (y₁+y₂)/2)
- **Chia đoạn tỉ lệ k**: P = ((1−k)x₁+kx₂, (1−k)y₁+ky₂)
- **Hình chiếu H của P lên đường AB**: 
  H = A + ((P−A)·(B−A)/t²)·(B−A)
- **Điểm C biết AC = b, góc BAC = α** (A=(0,0), B trên Ox):
  C = (b·cos α, b·sin α)
- **Điểm C biết AC = b, BC = a**: giao hai đường tròn — 
  d = (a² − b² + t²)/(2t) là hình chiếu của C lên AB;
  h = √(b² − d²); C = A + (d/t)(B−A) + h·(−(y_B−y_A)/t, (x_B−x_A)/t)
- **Trọng tâm G** tam giác ABC: ((x_A+x_B+x_C)/3, ...)
- **Tâm đường tròn ngoại tiếp**: nghiệm hệ |OA|² = |OB|² = |OC|² (2 phương trình tuyến tính sau khai triển)
- **Tâm nội tiếp**: (a·A + b·B + c·C)/(a+b+c) với a = |BC| (đối diện A)
- **Khoảng cách điểm–đường** (đường qua A, vector chỉ phương u): 
  d(P, Δ) = |(P−A) × u|/|u| với tích có hướng 2D: (p₁u₂ − p₂u₁)

## 3. Giải số khi không ra dạng chính xác

- Chọn ẩn (thường 1–2 toạ độ), lập hệ từ bảng ràng buộc Phase 1.
- Giải bằng phương pháp luận số học thủ công (thử, chia đôi, Newton) với dung sai 1e-6; ghi rõ phương pháp + giá trị gần đúng trong bảng.
- Kiểm tra số nghiệm: hệ 2 đường tròn có 0/1/2 nghiệm tùy vị trí — khi 2 nghiệm, chọn nghiệm phù hợp "hình nằm phía nào" và nêu rõ lựa chọn.

## 4. Bảng kiểm tra ràng buộc (bắt buộc)

Mỗi dòng = 1 dữ kiện Phase 1:

| Dữ kiện | Công thức kiểm tra | Thay số | Kết quả |
|---|---|---|---|
| AB = 5 | √((x_B−x_A)²+(y_B−y_A)²) | √(5²+0²) | = 5 ✓ |
| Â = 90° | (B−A)·(C−A) | (5,0)·(0,4) = 0 | = 0 ✓ |
| (O) tiếp AB | d(O, AB) = R | 3 = 3 | ✓ |

Quy tắc:
- Pass 100% dòng mới được sang Phase 3.
- Sai số cho phép: chính xác (phân số/căn) hoặc ≤ 1e-6 (giải số).
- Nếu một ràng buộc không thể kiểm tra bằng công thức (ví dụ "tứ giác nội tiếp") — chuyển thành ràng buộc tương đương (4 điểm cùng thuộc 1 đường tròn: kiểm tra tâm/bán kính).

## 5. Xử lý hình không tồn tại

Nếu bảng kiểm cho kết quả mâu thuẫn (ví dụ a + b < c), bài toán **vô hình**: dừng, báo người dùng kèm bằng chứng (dòng nào fail, chênh bao nhiêu). Đây là kết quả hợp lệ, không phải lỗi.
