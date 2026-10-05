# Ví dụ mẫu — Tam giác với góc cho trước

Ví dụ này minh hoạ toàn bộ 5 phase của skill. Đây là chuẩn đối chiếu khi sinh kết quả mới.

## Đề bài

> Cho tam giác ABC có AB = 5, AC = 6, góc BAC = 60°. Tính độ dài BC, diện tích tam giác, và độ dài đường cao AH (H thuộc BC).

## Phase 1 — Bảng ràng buộc

| Dữ kiện | Ràng buộc kiểm tra |
|---|---|
| AB = 5 | \|AB\| = 5 |
| AC = 6 | \|AC\| = 6 |
| góc BAC = 60° | cos góc giữa (B−A) và (C−A) = 0.5 |
| H thuộc BC | H = B + t(C−B), 0 ≤ t ≤ 1 |
| AH ⊥ BC | (A−H)·(C−B) = 0 |

## Phase 2 — Toạ độ

Chọn A = (0,0), B = (5,0) (cạnh AB trên Ox), C = (6cos60°, 6sin60°) = (3, 3√3).

| Điểm | Toạ độ chính xác | Decimal (dùng trong TikZ) |
|---|---|---|
| A | (0, 0) | (0,0) |
| B | (5, 0) | (5,0) |
| C | (3, 3√3) | (3, 5.1962) |
| H | (135/31, 30√3/31) | (4.3548, 1.6762) |

Kiểm tra: |AB| = 5 ✓; |AC| = √(9+27) = 6 ✓; cos BAC = 3/6 = 0.5 → 60° ✓;
H = B + (10/31)(−2, 3√3), t = 10/31 ∈ [0,1] ✓; (A−H)·(C−B) = 0 ✓.

## Phase 3–4 — TikZ + compile

Xem `solution.tex`. Compile:
```bash
node ../../scripts/compile_tikz.js solution.tex --png
```
Kết quả mong đợi: `COMPILE_OK`, PNG cho thấy góc A = 60°, AH vuông BC.

## Phase 5 — Giải

- Định lý cosin: BC² = 5² + 6² − 2·5·6·cos60° = 25 + 36 − 30 = 31 → **BC = √31 ≈ 5.568**
- Diện tích: S = (1/2)·AB·AC·sin60° = 15·(√3/2) = **15√3/2 ≈ 12.99**
- Đường cao: AH = 2S/BC = 15√3/√31 = **15√93/31 ≈ 4.666**

## Kiểm chứng chéo (bắt buộc)

- BC bằng toạ độ: √((5−3)² + (0−3√3)²) = √(4+27) = √31 ✓ khớp
- AH bằng toạ độ: |AH| = √((135/31)² + (30√3/31)²) = √(675/31) = 15√3/√31 ✓ khớp
- Thay ngược: 2S/BC = 25.98/5.568 = 4.666 ✓ khớp
