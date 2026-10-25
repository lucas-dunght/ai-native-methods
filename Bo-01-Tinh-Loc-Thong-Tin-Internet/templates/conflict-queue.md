# Conflict Queue Template · Hàng đợi Xung đột theo Thẻ Decision Brief D<N> (v2.0)

Hàng đợi chứa các cặp hoặc nhóm `Fact Cards` mâu thuẫn nhau về số liệu hoặc logic. AI Agent tuyệt đối không tự chọn sự thật chuẩn (`canonical`), mà bắt buộc đóng gói từng xung đột thành thẻ quyết định **Decision Brief `D<N>`** để con người phán xử.

## Bản mẫu Thẻ Quyết định Xung đột

### D1 · Conflict C-001 · Chênh lệch quy mô thị trường EdTech ĐNA năm 2023

- **Dự án / Chu kỳ nghiên cứu.** `research-cycle-2026-10-25` · Giai đoạn 4 (Xử lý xung đột).
- **Giải thích ELI10.** Chúng ta có hai báo cáo uy tín đưa ra hai con số khác nhau về tổng quy mô thị trường EdTech Đông Nam Á năm 2023 (`6.7 tỷ USD` so với `8.2 tỷ USD`). Nguyên nhân là báo cáo thứ nhất chỉ tính học phí trực tuyến K-12 và Upskilling, trong khi báo cáo thứ hai cộng thêm cả doanh thu bán phần cứng thiết bị trường học.
- **Rủi ro nếu chọn sai (Stakes).** Nếu chọn con số `8.2 tỷ USD` cho bài toán phần mềm thuần túy, dự phóng dung lượng thị trường (`TAM`) của dự án sẽ bị thổi phồng thêm `1.5 tỷ USD` không thuộc phân khúc mục tiêu.
- **Đối chiếu hai thẻ sự thật.**
  - **Card A (`F-2026-004`).** Quy mô đạt `6.7 tỷ USD` năm 2023 · Nguồn `S001` (`tier-1`, khảo sát 50 nền tảng phần mềm giáo dục, công bố tháng 03/2024).
  - **Card B (`F-2026-018`).** Quy mô đạt `8.2 tỷ USD` năm 2023 · Nguồn `S015` (`tier-2`, bài tổng hợp thị trường gộp cả thiết bị phần cứng, công bố tháng 06/2024).
- **Khuyến nghị (Recommendation).** Chọn phương án **A** vì phạm vi `brief.md` của chúng ta chỉ xét phần mềm K-12 và Upskilling, khớp hoàn toàn với phương pháp đo của `F-2026-004`.
- **Điểm độ phủ (Completeness).** `A = 10/10`, `B = 8/10`, `C = 5/10`.
- **Các phương án lựa chọn.**
  - **A) Giữ `F-2026-004` làm chuẩn cho mảng phần mềm và tách `F-2026-018` thành thẻ riêng ghi rõ bao gồm phần cứng (recommended)**
    - Ưu điểm. Bảo toàn tính chính xác của số liệu phần mềm và không làm mất thông tin tổng thể ngành.
    - Nhược điểm. Cần cập nhật lại trường `content` và `notes` của cả hai thẻ để nêu rõ ranh giới đo lường.
  - **B) Chỉ giữ `F-2026-004` (`6.7 tỷ USD`) và đánh dấu `F-2026-018` là `deprecated`**
    - Ưu điểm. Gọn kho thẻ sự thật, tập trung đúng phân khúc phần mềm.
    - Nhược điểm. Mất dữ liệu tham chiếu về quy mô chi tiêu thiết bị giáo dục.
  - **C) Từ chối cả hai và chạy vòng thu thập bổ sung từ nguồn thứ ba**
    - Ưu điểm. Độ an toàn cao nhất nếu nghi ngờ cả hai báo cáo.
    - Nhược điểm. Tốn thêm 1 vòng thu thập trong khi sự khác biệt đã giải thích được bằng phạm vi đo.
- **Tổng kết đánh đổi (Net).** Đánh đổi 2 phút cập nhật mô tả phạm vi đo để giữ được cả độ chính xác của phân khúc cốt lõi lẫn bức tranh toàn ngành.

**Quyết định của con người.** `[ ] Phương án A  |  [ ] Phương án B  |  [ ] Phương án C`
**Người phê duyệt.** `[Tên]` · **Ngày phê duyệt.** `[YYYY-MM-DD]`
