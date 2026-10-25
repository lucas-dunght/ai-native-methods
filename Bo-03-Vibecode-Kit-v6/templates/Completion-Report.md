# CR-NNN · Báo cáo Hoàn thành Gói Công việc (Completion Report)

**Date.** YYYY-MM-DD
**Linked TIP.** TIP-NNN
**Linked Blueprint.** BP-NNN
**Builder Session / Runtime.** [Tên phiên Thợ thi công & Model thực thi]
**Worktree / Branch.** [Tên nhánh và đường dẫn worktree]

## 1. Trạng thái Tổng quát và Dấu vân tay Bằng chứng (Status & Fingerprint Ledger)

- **STATUS.** `[DONE | DONE_WITH_CONCERNS | PARTIAL | BLOCKED | NEEDS_CONTEXT]`
- **WTREE_FINGERPRINT.** `[Mã băm 16 ký tự từ lệnh (git status --porcelain; git diff HEAD) | shasum -a 256 | cut -c1-16]`
- **COMMIT_HASH.** `[Mã commit git sau khi đã đóng gói thay đổi hoặc ghi UNCOMMITTED]`
- **EVIDENCE_KIND.** `[static-read | unit-test | fixture-replay | live-run | production]`
- **EVIDENCE_STATUS.** `[FRESH | STALE | MISSING]` (Chỉ ghi `FRESH` khi không sửa thêm bất kỳ file nào sau lần chạy kiểm thử cuối cùng)

## 2. Danh sách File đã Thay đổi và Kiểm tra Scope Freeze

- **Files created (Tạo mới).**
  - `src/...`
  - `tests/...`
- **Files modified (Chỉnh sửa).**
  - `src/...`
- **Xác nhận tuân thủ Scope Freeze.** `[PASS | VIOLATION]` (Tất cả các file trên đều nằm trong mục `Allowed write paths` của `TIP-NNN`, không chạm vào file ngoài phạm vi và không vi phạm `Disjoint File Ownership`).

## 3. Kết quả Kiểm chứng Từng Tiêu chí Nghiệm thu (Acceptance Criteria Results)

Mọi tuyên bố hoàn thành dưới đây đều thuộc mức **OBSERVED** (có câu lệnh thực thi và đầu ra thực tế trong phiên này).

| Mã AC | Mô tả tiêu chí trong TIP | Câu lệnh đã chạy | Kết quả thực tế (Observed Output) | Đánh giá |
|---|---|---|---|---|
| AC1 | [Mô tả ngắn] | `[Lệnh chạy test 1]` | `[Tóm tắt kết quả, số test pass, thời gian chạy]` | `PASS` |
| AC2 | [Mô tả ngắn] | `[Lệnh chạy test 2]` | `[Tóm tắt kết quả]` | `PASS` |
| AC3 | [Kiểm tra kiểu / lint / secret] | `[Lệnh kiểm tra]` | `[0 lỗi, 0 cảnh báo bảo mật]` | `PASS` |

## 4. Các Đường tắt đã Áp dụng theo Phê duyệt (Shortcuts Taken)

- [Ghi rõ mã quyết định `D<N>` có `Completeness <= 7/10` đã thực thi, vị trí dòng chú thích `vibecode-shortcut(D<N>)` trong mã nguồn và điều kiện nâng cấp. Ghi `Không có` nếu thi công trọn vẹn 10/10.]

## 5. Độ lệch so với Bản vẽ (Deviations from Blueprint / TIP)

- **Deviation 1.**
  - **Nội dung thay đổi (What).** [Đã làm khác chi tiết nhỏ nào so với mô tả ban đầu]
  - **Lý do (Why).** [Tại sao thực tế mã nguồn buộc phải điều chỉnh cục bộ ở Level 1]
  - **Tác động (Impact).** [Khẳng định không làm thay đổi kiến trúc tổng thể hay hợp đồng giao tiếp dùng chung]

## 6. Vấn đề Tồn đọng và Mức độ Tự tin (Known Issues & Confidence Level)

- **Issues phát hiện.**
  - `[Severity. Low | Medium | High]` · [Mô tả vấn đề hoặc giới hạn chưa được giải quyết trong phạm vi TIP này]
- **Độ tự tin theo từng thành phần (Confidence Level).**
  - Thành phần A. `[High | Medium | Low]` · [Lý do]
  - Tổng thể gói TIP-NNN. `[High | Medium | Low]`

## 7. Đề xuất Cải tiến cho Chủ thầu (Suggestions for Contractor)

Thợ thi công ghi lại những phát hiện hoặc cách tiếp cận tốt hơn cho các gói TIP tiếp theo mà không tự ý vượt ranh giới sửa code trong gói hiện tại.

- **Suggestion 1.** [Mô tả đề xuất cải tiến kiến trúc, hiệu năng hoặc dọn dẹp mã nguồn ở các module lân cận]
- **Suggestion 2.** [Mô tả bài kiểm thử hoặc kịch bản cần bổ sung ở vòng sau]
