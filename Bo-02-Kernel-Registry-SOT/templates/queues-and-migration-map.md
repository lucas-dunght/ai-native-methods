# Queues and Migration Map Template · Hàng đợi Quyết định D<N> & Bản đồ Di trú (v2.0)

Tài liệu này gom ba bản mẫu điều phối giữa AI Agent và con người ở Phase 2, Phase 3, Phase 4 và Phase 5 của Bộ 02 v2.0.

---

## 1. Hàng đợi Xung đột Sự thật (`queues/conflict-queue.md`)

Mỗi xung đột giữa hai tài liệu nguồn ở Phase 3 bắt buộc trình bày theo cấu trúc thẻ quyết định **Decision Brief `D<N>`**.

### D1 · Conflict C-001 · Hai bảng giá khác nhau cho cùng mã sản phẩm SKU X-001 Quý 4/2026

- **Giải thích ELI10.** Trong thư mục tài liệu gốc có hai tệp PDF cùng ghi bảng giá Quý 4/2026 cho sản phẩm `SKU X-001`. Tệp của Phòng Kinh doanh ghi `12.500.000 VND`, trong khi tệp trong thư mục Tài chính ghi `13.000.000 VND`.
- **Rủi ro nếu chọn sai (Stakes).** Nếu chọn nhầm đơn giá chuẩn (`canonical`), toàn bộ báo giá gửi khách hàng và công thức tính tổng doanh thu `L2-total-revenue-Q4-2026` sẽ lệch `4%`.
- **Đối chiếu bằng chứng (`[OBSERVED]`).**
  - **Nguồn A.** `raw-docs/sales/pricing-2026-Q4-final.pdf` (`12.500.000 VND`, có chữ ký số ngày `2026-09-28`).
  - **Nguồn B.** `raw-docs/finance/pricing-2026-Q4-draft.pdf` (`13.000.000 VND`, bản dự thảo ngày `2026-09-10`, chưa có chữ ký).
- **Khuyến nghị (Recommendation).** Chọn phương án **A** vì tệp của Phòng Kinh doanh là bản ban hành sau và đã có chữ ký phê duyệt chính thức.
- **Điểm độ phủ (Completeness).** `A = 10/10`, `B = 3/10`.
- **Các phương án lựa chọn.**
  - **A) Chọn `12.500.000 VND` (Nguồn A) làm mục `L1-product-price-001` chính thức và ghi chú Nguồn B là bản nháp cũ đã hết hiệu lực (recommended)**
  - **B) Chọn `13.000.000 VND` (Nguồn B) làm mục `L1` chính thức**
  - **C) Tạm hoãn tạo mục `L1` này để xin xác nhận lại từ Giám đốc Tài chính**
- **Quyết định của con người.** `[ ] Phương án A  |  [ ] Phương án B  |  [ ] Phương án C`

---

## 2. Hàng đợi Chưa phân loại (`queues/unclassified-queue.md`)

Dùng cho các tệp hỗn hợp phát hiện ở Phase 2.

### D2 · Unclassified U-001 · Biên bản họp chiến lược Quý 3 (`board-notes-2026-09.md`)

- **Giải thích ELI10.** Tệp biên bản họp này chứa đồng thời 3 loại thông tin gồm định mức thưởng KPI mới (`L1`), yêu cầu bảo mật hồ sơ nhân sự (`L3`) và lời nhắn nhủ về văn hóa làm việc của CEO (`L4`).
- **Rủi ro nếu chọn sai (Stakes).** Nếu để nguyên một tệp hỗn hợp hoặc đẩy nhầm cả tệp vào `registry/`, AI Agent sẽ nhầm lời động viên của CEO thành quy định cứng.
- **Khuyến nghị (Recommendation).** Chọn **A** (Tách phần bảng định mức KPI thành `L1`, trích điều khoản bảo mật hồ sơ vào `L3` và giữ phần văn hóa làm việc ở `L4`).
- **Điểm độ phủ (Completeness).** `A = 10/10`, `B = 6/10`.
- **Quyết định của con người.** `[ ] Phương án A  |  [ ] Phương án B`

---

## 3. Bản đồ Di trú & Biên bản Khóa Phạm vi Sao chép (`queues/migration-map.md`)

Trình con người duyệt ở cuối Phase 4 và ghi nhận bằng chứng bảo toàn dữ liệu ở cuối Phase 5.

```markdown
# Migration Map & Copy-Only Scope Freeze Receipt

## 1. Dấu vân tay Bảo toàn Thư mục Gốc (`Zero Source Mutation Proof`)
- **Thư mục gốc được khảo sát.** `raw-docs/`
- **Mã băm trước khi chạy Phase 5 (`PRE_MIGRATION_FINGERPRINT`).** `sha256:e3b0c44298fc1c149afbf4c8996fb924`
- **Mã băm sau khi chạy Phase 5 (`POST_MIGRATION_FINGERPRINT`).** `sha256:e3b0c44298fc1c149afbf4c8996fb924`
- **Kết luận kiểm chứng (`[OBSERVED]`).** `MATCH 100%` (Không có tệp gốc nào bị xóa, di chuyển hay sửa đổi).

## 2. Bảng Ánh xạ Sao chép và Trích xuất (`Source -> Target`)

| Đường dẫn gốc (Giữ nguyên 100%) | Thao tác | Đường dẫn đích trong `kernel-registry/` | Xuất xứ |
|---|---|---|---|
| `raw-docs/sales/pricing-2026-Q4-final.pdf` | Trích xuất YAML | `registry/stored-facts/L1-product-price-001.yaml` | `L1` |
| `raw-docs/finance/budget-plan-2026-Q4.xlsx` | Trích xuất Công thức | `registry/derived-facts/L2-total-revenue-Q4-2026.yaml` | `L2` |
| `raw-docs/legal/decree-13-2023-nd-cp.pdf` | Sao chép + Trích xuất | `obligations/decree-13-2023-nd-cp/obligations.yaml` | `L3` |
| `raw-docs/brand/ceo-writing-style.md` | Sao chép nguyên bản | `style/voice-guide.md` + `style/L4-style.yaml` | `L4` |
```
