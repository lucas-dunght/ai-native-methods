# Gap Checklist Template · Danh sách Lỗ hổng & Truy vấn Bù đắp (v2.0)

Danh sách các điểm mù dữ liệu phát hiện ở Giai đoạn 5. Mỗi lỗ hổng đều phải đi kèm cấu hình truy vấn đa tín hiệu (`search_mode` + `suggested_query`) để có thể chạy thu thập bù đắp tức thì.

## Bản mẫu Mục Lỗ hổng

### Gap G-001 · Thiếu nguồn độc lập thứ hai cho quy mô GMV năm 2024

- **Thẻ liên quan.** `F-2026-001` (`trust_tier: probable`, `independent_origin_count: 1`).
- **Mô tả lỗ hổng.** Con số `114 tỷ USD` hiện có 3 bài báo đề cập nhưng cả 3 đều dẫn lại cùng một báo cáo gốc `S001`. Cần thêm ít nhất 1 nguồn thống kê độc lập từ ngân hàng trung ương hoặc tổ chức tài chính quốc tế để nâng lên `verified`.
- **Mức độ ưu tiên.** `high` (`high` | `medium` | `low`).
- **Kế hoạch thu thập bù đắp.**
  - **Công cụ & Chế độ (`search_mode`).** `unified-search` · `mode: academic` và `mode: legal`.
  - **Câu truy vấn gợi ý (`suggested_query`).** `"Southeast Asia digital payments" "2024" ("BIS" OR "World Bank" OR "ADB" OR "central bank")`
  - **Hạng nguồn mục tiêu (`target_authority_tier`).** `tier-1`
- **Trạng thái.** `open` (`open` | `resolved` | `disclosed-in-report`).

---

### Gap G-002 · Giả định chưa kiểm chứng về tỷ lệ phí giao dịch xuyên biên giới

- **Thẻ liên quan.** `F-2026-009` (`claim_label: ASSUMED`).
- **Mô tả lỗ hổng.** Đang giả định phí chuyển đổi ngoại tệ qua mã QR liên thông ASEAN thấp hơn thẻ quốc tế 1.5%, nhưng chưa có bảng biểu phí chính thức từ cổng thanh toán quốc gia.
- **Mức độ ưu tiên.** `medium`.
- **Kế hoạch thu thập bù đắp.**
  - **Công cụ & Chế độ (`search_mode`).** `unified-search` · `mode: legal` hoặc `gstack /scrape` trên cổng thông tin NAPAS / PayNow.
  - **Câu truy vấn gợi ý (`suggested_query`).** `"cross-border QR payment" fee schedule ASEAN NAPAS PayNow 2024 2025`
  - **Hạng nguồn mục tiêu (`target_authority_tier`).** `tier-1` hoặc `tier-2`.
- **Trạng thái.** `open`.
