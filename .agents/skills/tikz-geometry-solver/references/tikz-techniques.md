# TikZ Techniques — Plane Geometry Reference

## Minimal preamble (standalone)

```latex
\documentclass[tikz,border=3mm]{standalone}
\usetikzlibrary{calc,angles,quotes,intersections,arrows.meta,decorations.markings,patterns}
\begin{document}
\begin{tikzpicture}[scale=1,
    point/.style={circle,fill,inner sep=1.4pt},
    every node/.style={font=\small}]
  % fill/màu nền trước → đường → điểm → label → dấu ký hiệu
\end{tikzpicture}
\end{document}
```

Đối với `solution.tex` (hình + lời giải): dùng `\documentclass[a4paper]{article}`, `\usepackage{tikz}` + cùng `\usetikzlibrary`, hình đặt trong `center`.

## Điểm & toạ độ

```latex
\coordinate (A) at (0,0);
\coordinate (B) at (5,0);
\coordinate (C) at (1.5,2.598);   % chép nguyên văn từ bảng toạ độ Phase 2
```

- Toạ độ decimal giữ ≥ 4 chữ số thập phân.
- `[scale=...]` chỉ co giãn toạ độ, KHÔNG co giãn text/độ dày nét — ưu tiên dùng toạ độ thật, scale chỉ để chỉnh khổ.

## calc — điểm phụ, trung điểm, hình chiếu, xoay

```latex
\coordinate (M) at ($(A)!0.5!(B)$);              % trung điểm AB
\coordinate (D) at ($(A)!2.0!(B)$);              % điểm D sao cho B là trung điểm AD
\coordinate (H) at ($(A)!(C)!(B)$);              % hình chiếu của C lên đường AB
\coordinate (E) at ($(A)!1.5!30:(B)$);           % xoay B quanh A góc 30°, kéo dài 1.5 lần
\coordinate (F) at ($ (A) + (0,0.3)$);           % dịch điểm
```

## intersections — giao điểm hai đường

```latex
\draw[name path=AB] (A) -- (B);
\draw[name path=circ] (O) circle (2);
\path[name intersections={of=AB and circ, by=P,Q}];  % P, Q là giao điểm
```

Giao đường tròn–đường tròn: `name intersections={of=c1 and c2, by=T1,T2}`.

## angles — đánh dấu góc, góc vuông

```latex
\pic [draw, angle radius=7mm, angle eccentricity=1.4, "$60^\circ$"] {angle = B--A--C};
\pic [draw, angle radius=3mm] {right angle = B--A--C};
```

- Thứ tự `X--Y--Z`: **Y là đỉnh góc**. Sai thứ tự là lỗi compile/hình phổ biến nhất.
- **Cảnh giác góc phản xạ**: `\pic {angle = X--Y--Z}` quét cung **ngược chiều kim đồng hồ từ tia Y→X đến tia Y→Z**. Nếu phép quét đó > 180°, cung thành "vòng tròn lớn" bao quanh đỉnh. Luôn tính hướng (góc lượng giác) của hai tia trước:
  - Nếu (hướng tia Y→Z) − (hướng tia Y→X) theo chiều ngược kim đồng hồ ≤ 180° → giữ thứ tự.
  - Ngược lại → **đổi chân**: `angle = Z--Y--X`.
  Ví dụ: tại B có tia B→A hướng 180°, tia B→C hướng 120°: `angle = A--B--C` quét 300° (SAI, thành vòng tròn); `angle = C--B--A` quét 60° (ĐÚNG).
- Với góc vuông `right angle`, pic vẽ ô vuông giữa hai tia nên không bị lỗi quét — nhưng vẫn cần hai chân kề đỉnh.
- Dấu góc vuông thay thế (dùng khi pic right angle vẽ lệch):
  ```latex
  \draw ($(A)!3mm!(B)$) -- ($($(A)!3mm!(B)$)!3mm!90:($(A)!3mm!(C)$)$) -- ($(A)!3mm!(C)$);
  ```

## Đường tròn, cung, tiếp tuyến

```latex
\draw (O) circle[radius=2.5];                    % đường tròn tâm O bán kính 2.5
\draw (O) arc[start angle=0, end angle=60, radius=2.5];
```

- Bán kính đường tròn luôn tính ra số thực (không để `r` chưa khai báo).
- Điểm tiếp tuyến phải tính ở Phase 2 (foot of perpendicular từ tâm) — không "vẽ cho chạm".

### Quy tắc đường tròn & tiếp xúc (bắt buộc)

Đường tròn là đối tượng dễ vẽ lệch nhất vì sai bán kính 10–20% mắt vẫn thấy "có vẻ đúng".
Cấm cảm tính theo 3 quy tắc:

1. **Tâm và bán kính chép nguyên văn từ bảng Phase 2**, giữ ≥ 6 chữ số thập phân. Làm tròn bán kính hoặc tâm → mất tiếp xúc (lỗi 1e-4 cm là thấy được khi zoom, 1e-2 là thấy bằng mắt).
2. **Mỗi quan hệ tiếp xúc phải có 1 dòng kiểm tra bằng số trong bảng Phase 2**, pass trước khi vẽ:
   - Tiếp xúc ngoài 2 đường tròn: |C₁C₂| = r₁ + r₂ (sai số ≤ 1e-6).
   - Tiếp xúc trong: |C₁C₂| = |r₁ − r₂|.
   - Tiếp xúc đường thẳng: d(tâm, đường thẳng) = r, và chân vuông góc nằm TRÊN đoạn cạnh (không phải phần kéo dài).
3. **Cú pháp bán kính không đơn vị** (`circle[radius=2.5]`, không viết `2.5cm`): bán kính không đơn vị chịu tác động của `[scale=...]` giống hệt toạ độ; viết kèm đơn vị thì bán kính KHÔNG bị scale → hình toạ độ thu nhỏ nhưng đường tròn giữ nguyên cỡ → lệch hoàn toàn. Trong 1 hình chỉ dùng một kiểu nhất quán.

## Đánh dấu đoạn bằng nhau / song song

```latex
% dấu gạch ngang giữa đoạn (số đoạn bằng nhau)
\path[postaction={decorate,decoration={markings,
  mark=at position 0.5 with {\draw (0,-2pt)--(0,2pt);}}}] (A) -- (B);
% 2 dấu: thêm mark thứ hai position 0.45/0.55
% mũi tên chỉ song song: mark with {\draw[-{Stealth}] (0,0)--(0,4pt);}
```

## Quy tắc nét vẽ (bắt buộc)

Nét đứt KHÔNG phải lựa chọn thẩm mỹ tùy hứng — phân loại theo vai trò đường:

| Nét | Dành cho | Ví dụ |
|---|---|---|
| **Liền, thick** | Mọi đối tượng dữ kiện của đề | cạnh hình, đường chéo đề nêu, đường thẳng đề cho, đường tròn |
| **Đứt (dashed)** | CHỈ đường phụ dựng thêm để giải | đường cao, hình chiếu, bán kính tại điểm tiếp xúc, đoạn kéo dài ngoài đoạn cho trước, đường trung tuyến phụ |
| Liền mảnh (thin) | đường phụ cũng nằm trong dữ kiện gián tiếp (ví dụ đường tròn phụ dựng để tìm giao điểm) | hiếm khi cần |

- Một đường chọn nét gì thì **đứt toàn bộ đường** — không đứt đoạn đầu liền đoạn cuối.
- Không chuyển nét đứt ↔ liền chỉ để "tránh đường khác" — đường cắt nhau là bình thường trong hình hình học; tránh bằng **vị trí label**, không phải bằng kiểu nét.
- Trường hợp một đường vừa là dữ kiện vừa là đường phụ (ví dụ đường cao trùng cạnh) → vẽ **liền** (ưu tiên vai trò dữ kiện).

```latex
\draw[thick] (A) -- (B) -- (C) -- cycle;   % cạnh chính: liền
\draw[thick] (B) -- (D);                   % đường chéo đề nêu: liền
\draw[dashed] (A) -- (H);                  % đường cao dựng thêm: đứt
```

## Quy tắc label điểm (bắt buộc)

Mục tiêu: **không label nào bị bất kỳ đường nào cắt qua, không hai label nào chồng nhau.**

1. **Vẽ đúng thứ tự**: fill nền → đường → **chấm điểm (đè lên đường)** → label → dấu ký hiệu. Chấm điểm vẽ sau đường để che chỗ đường đi qua tâm.
2. **Hướng label**: chĩa ra **ngoài hình** — đỉnh trên → `above`, góc dưới trái → `below left`... Với điểm **nằm trong hình hoặc nằm trên đường** (giao điểm, chân đường cao, tâm): đặt label **vuông góc hướng ra khỏi đường gần nhất**, không đặt label trùng hướng với đường đi qua điểm đó (nếu đặt `right` mà đường đi ngang qua bên phải thì label nằm đè lên đường).
3. **Kiểm tra va chạm với mọi đường**: tại một điểm có k đường đi qua, label phải đặt vào **góc sector trống lớn nhất** giữa các đường đó — đo bằng góc thực từ toạ độ, ưu tiên **tia phân giác của sector** (cách đều hai biên), giữ khoảng cách từ mép label đến mọi đường ≥ 2mm. Ví dụ điểm H nằm trên BD, có HA và BD qua đó: 4 sector — chọn sector không chứa đường nào khác và chĩa ra ngoài vùng đặc.
4. **Hai điểm gần nhau** (khoảng cách vẽ < ~1.5cm): đặt 2 label theo **hai hướng đối nhau** (một `above left`, một `below right`...). Nếu vẫn chồng: tăng `label distance` hoặc dịch bằng `shift={(dx,dy)}`. Tuyệt đối không để 2 label chạm nhau.
5. **Cấm `fill=white` cho label điểm**: nền trắng tạo khoảng hở trên đường đi qua, nhìn như đường bị cắt gãy. Mọi điểm — kể cả điểm nằm trong hình (tâm đường tròn, tâm hình chữ nhật) — đều có ít nhất một sector trống, vì chỉ hữu hạn đường đi qua nó. Đặt label dọc theo **tia phân giác của sector trống** với offset đủ (mép text cách điểm ≥ 2mm):
   ```latex
   % O là tâm, nằm TRÊN đường chéo BD → sector trống hướng xuống-trái (phân giác ~225°):
   \fill[point] (O) node[below left=2pt] {$O$};   % ĐÚNG: nằm gọn trong sector trống
   \fill[point] (O) node[fill=white] {$O$};        % SAI: nền trắng đè lên, cắt đứt BD
   ```
   Lưu ý: hướng "dễ nhìn" như `below right` có thể chỉ cách biên sector vài độ (rơi gần đúng lên đường) — luôn đo góc theo toạ độ, không nhìn cảm tính. `fill=white` chỉ được dùng khi label PHẢI nằm trên đường theo quy ước (ghi số đo/tên trên chính đoạn thẳng) — không dùng cho label điểm.
6. Toán trong label luôn bọc `$...$`.

## Kiểu nét & màu thông dụng

```latex
\draw[thick] (A) -- (B);                  % cạnh chính
\draw[dashed] (C) -- (H);                 % ĐÚNG vai trò: đường phụ, đường cao
\draw[very thick, red] (A) -- (B);        % nhấn mạnh kết quả
\fill[blue!20, opacity=0.5] (A) -- (B) -- (C) -- cycle;
```

## Lỗi compile thường gặp

| Lỗi | Nguyên nhân |
|---|---|
| `Missing $ inserted` | label thiếu `$...$`, ký tự `_`/`^` ngoài math |
| `I do not know the key '/tikz/angle'` | thiếu library `angles` hoặc `quotes` |
| `Package pgf Error: No shape named P` | dùng `\coordinate` chưa định nghĩa (sai tên/hoá) |
| Hình trống/trắng | thiếu `\end{tikzpicture}` hoặc compile class không có tikz |
| `Undefined control sequence \pic` | TikZ quá cũ — thay pic bằng cách vẽ tay (mục angles) |
| Cung vẽ sai hướng | `arc` start angle ngược chiều kim đồng hồ mặc định |
