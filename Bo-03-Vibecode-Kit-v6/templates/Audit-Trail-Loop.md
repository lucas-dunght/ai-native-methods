# Nhật Ký Vòng Lặp Kiểm Toán & Ràng Buộc (`Audit Trail & Constraint Loop · v6.2 × pstack`)

- **Mã Dự án / Nhánh:** `[EPIC-YYYY-MM / feat/...]`
- **Người thực hiện:** `[Chủ thầu / Thợ / Trọng tài C3]`

---

## 1. Bảng Theo Dõi Vòng Lặp Ràng Buộc (`Constraint Loop Iterations`)

> **Quy tắc:** Khi có các ràng buộc cứng (văn phong, định dạng JSON, bảo mật `Zero-Secret`, không dùng `any`, cập nhật `Feature Map` không bị trôi), Agent không được dừng ở lần viết đầu tiên mà phải chạy kiểm tra cơ học -> sửa lỗi -> kiểm tra lại cho đến khi `0 violations`.

| Vòng lặp (`Iteration`) | Ràng buộc Kiểm tra (`Constraint`) | Câu lệnh Kiểm tra Cơ học (`Command`) | Số Vi phạm Phát hiện | Hành động Khắc phục | Kết quả Sau Sửa |
|---|---|---|---|---|---|
| `Loop #1` | `Zero Em-Dash & Zero Comma-Va` | `grep -rnP "\\x{2014}|,\\s+và" docs/` | `[3]` | Thay thế đúng ngữ cảnh | `0 matches (PASS)` |
| `Loop #2` | `Zero-Secret Policy` | `grep -rnE "sk-[a-zA-Z0-9]{20,}" .` | `0` | Không phát sinh | `0 matches (PASS)` |
| `Loop #3` | `Scrap-When-Wrong Type Audit` | `npm run typecheck && grep -rn ": any" src/` | `0` | Không dùng `any` / tham số vá víu | `0 errors (PASS)` |
| `Loop #4` | `Live Lever & Feature Map Sync` | `./bin/control-app doctor --json` | `0` | Đã đồng bộ `references/features/README.md` | `drift_detected: false (PASS)` |

---

## 2. Chuỗi Dấu Vân Tay Qua Các Cổng (`Fingerprint Chain of Custody`)

1. **Sau Bước 6 (`BUILD Complete`):**
   - `WTREE_FINGERPRINT: HEAD=[h1] TREE=[t1] WTREE=[w1] DIRTY_FILES=0`
2. **Sau Bước 7 (`VERIFY & ./bin/control-app Live Proof`):**
   - `WTREE_FINGERPRINT: HEAD=[h1] TREE=[t1] WTREE=[w1] DIRTY_FILES=0` (`Khớp 100% với bước BUILD`)
3. **Sau Bước 8 (`SHIP, Temporary Plan Cleanup & /maintain-verification-skill`):**
   - `WTREE_FINGERPRINT: HEAD=[h2] TREE=[t2] WTREE=[w2] DIRTY_FILES=0` (`Đã xóa/lưu trữ plan tạm và đồng bộ SHA-256 lên Kernel Registry`)
