# Enrichment Pass Template · Bản mẫu Làm giàu 4 Chiều & Cầu nối Bộ 02 (v2.0)

Sử dụng ở Giai đoạn 6 sau khi đã khử trùng lặp, giải quyết xong hàng đợi xung đột và tính toán `independent_origin_count`.

## Danh mục Kiểm tra Làm giàu cho Từng Thẻ (`Fact Card`)

1. **Kiểm tra Phòng vang (`Echo-Chamber Audit`).**
   - Đếm số lượng `primary_origin_url` duy nhất của thẻ.
   - Cập nhật trường `independent_origin_count`.
   - Áp dụng quy tắc phân hạng cơ học để gán `trust_tier: verified | probable | unverified`.
2. **Chiều 1 · Đối chiếu chéo (`cross_references`).**
   - Tìm các thẻ bổ sung nguyên nhân, hệ quả hoặc số liệu thành phần cho thẻ hiện tại.
3. **Chiều 2 · Phân loại đa trục (`classification`).**
   - Gán nhãn theo bảng từ khóa chuẩn của dự án (ví dụ `market-size`, `regulation`, `unit-economics`, `competitor-pricing`).
4. **Chiều 3 · Độ tươi và Mức độ trọng yếu (`recency_status` & `importance_rank`).**
   - `current`. Dữ liệu trong vòng 24 tháng tính đến thời điểm nghiên cứu.
   - `historical`. Dữ liệu từ 2 đến 5 năm trước dùng để so sánh chuỗi thời gian.
   - `outdated`. Dữ liệu đã quá 5 năm hoặc đã bị thay thế bởi văn bản pháp lý mới.
5. **Chiều 4 · Lỗ hổng kéo theo (`gaps_implied`) & Cầu nối Bộ 02 (`bo02_bridge`).**
   - Liên kết mã `G-NNN` nếu thẻ cần làm rõ thêm chi tiết.
   - Nếu thẻ đạt `trust_tier: verified` và là dữ liệu định lượng hoặc quy định chuẩn, bật `bo02_bridge.export_ready: true` để xuất thẳng sang `L1-stored-fact.yaml` của Bộ 02.

## Mẫu Nhật ký Làm giàu (`enrichment-log.md`)

```markdown
# Nhật ký Làm giàu Chu kỳ Nghiên cứu · YYYY-MM-DD

- **Tổng số thẻ đầu vào sau khử trùng lặp.** 24 thẻ
- **Số thẻ bị hạ từ Verified xuống Probable do trùng nguồn gốc (Phòng vang).** 4 thẻ (`F-2026-003`, `F-2026-007`, `F-2026-011`, `F-2026-019`)
- **Phân bổ độ tin cậy cuối cùng.**
  - `verified`. 12 thẻ (`50.0%` · Đạt ngưỡng `>= 40%`)
  - `probable`. 9 thẻ (`37.5%`)
  - `unverified`. 3 thẻ (`12.5%`)
- **Số thẻ đủ chuẩn xuất thẳng sang Bộ 02 (`L1 Stored Facts`).** 10 thẻ
```
