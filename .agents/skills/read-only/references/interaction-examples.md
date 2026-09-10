# Read-Only Interaction Examples

Few-shot examples showing how the read-only skill handles common requests.

## Example 1: Bug Fix Request

**User**: "Sửa lỗi crash ở hàm `calculateDiscount` trong `src/utils/pricing.ts`."

**AI Action**: Reads `src/utils/pricing.ts`, identifies division by zero, checks tests using read tools.

**AI Response**:

> Theo chính sách **Read-Only**, tôi không can thiệp trực tiếp vào file `src/utils/pricing.ts`. Dưới đây là nguyên nhân và đoạn mã đã khắc phục để bạn copy vào dự án:
>
> **Tệp:** `src/utils/pricing.ts` (Dòng 24-32)
> ```typescript
> export function calculateDiscount(price: number, discountRate: number): number {
>   if (discountRate <= 0 || price <= 0) {
>     return 0;
>   }
>   return Math.min(price, price * (discountRate / 100));
> }
> ```
> **Hướng dẫn:** Thay thế hàm `calculateDiscount` cũ bằng hàm trên để ngăn ngừa lỗi chia cho 0 và giá trị âm.

## Example 2: Architecture & Shell Diagnostic

**User**: "Kiểm tra xem project hiện tại dùng phiên bản Node nào và gợi ý cấu trúc thư mục cho module auth mới."

**AI Action**: Executes `node -v` via inspect command, reads `package.json`, searches existing folders.

**AI Response**: Cites Node version from command output and presents recommended directory structure in markdown tree format without creating folders.
