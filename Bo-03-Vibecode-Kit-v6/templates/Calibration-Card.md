# CC-NNN · [Tên gói công việc hoặc Đợt phát hành]

**Date deployed.** YYYY-MM-DD
**Date calibrated.** YYYY-MM-DD (sau khi có dữ liệu vận hành thực tế)
**Linked TIP.** TIP-NNN
**Linked Completion Report.** CR-NNN
**Ship Mode.** [Single-Stage | Dual-Stage Beta -> Stable]

## 1. Prediction (Dự đoán trước khi phát hành)

Trích xuất từ các tiêu chí thành công của `TIP-NNN` và `Blueprint`.

- **Criterion 1.** [Dự đoán định lượng hoặc định tính ban đầu]
- **Criterion 2.** [Dự đoán về hiệu năng, trải nghiệm hoặc thời gian hoàn thành]
- **Criterion 3.** [Dự đoán về độ ổn định và các góc khuất đã lường trước]

## 2. Actual (Thực tế quan sát được sau khi chạy thật)

Mọi nhận định ở mục này phải thuộc loại **OBSERVED** (có số liệu đo đạc, nhật ký hệ thống hoặc phản hồi thực tế).

- **Criterion 1.** [Kết quả thực tế quan sát được]
- **Criterion 2.** [Kết quả thực tế quan sát được]
- **Criterion 3.** [Các sự cố, điểm nghẽn hoặc hành vi ngoài dự kiến phát sinh]

## 3. Delta (Khoảng cách giữa Dự đoán và Thực tế)

[Mô tả cụ thể độ lệch giữa kỳ vọng và thực tế. Ví dụ tốc độ phản hồi chậm hơn dự kiến 35% khi dữ liệu vượt 10.000 dòng, hoặc người dùng hiểu nhầm nhãn nút bấm ở màn hình thanh toán.]

## 4. Error Allocation (Phân bổ 100 điểm sai số)

Nếu có bất kỳ độ lệch hay vấn đề nào phát sinh, bắt buộc phân bổ tổng cộng **đúng 100 điểm** vào 4 nhóm nguyên nhân gốc rễ dưới đây (nếu hoàn toàn trùng khớp không có sai số thì ghi 0 cho cả 4 mục và nêu rõ lý do).

- **Modeling.** [N điểm]
  Hiểu sai bài toán hoặc đặc tả thiếu. TIP hoặc Blueprint chưa phản ánh đúng nhu cầu thực tế hoặc bỏ sót trường hợp biên.
- **Timing.** [N điểm]
  Phát hành sai thời điểm hoặc lệch nhịp phối hợp. Đẩy lên khi dữ liệu nền chưa sẵn sàng hoặc xung đột với đợt cập nhật khác.
- **World-change.** [N điểm]
  Môi trường bên ngoài thay đổi giữa lúc lập kế hoạch và lúc vận hành. Ví dụ API bên thứ ba đổi cấu trúc, thư viện phụ thuộc cập nhật hoặc quy định nghiệp vụ thay đổi.
- **Execution.** [N điểm]
  Sai sót trong khâu thi công hoặc nghiệm thu. Code có lỗi logic, hiệu năng kém, hoặc bước Verify bỏ lọt lỗi bề mặt.

**Tổng cộng.** `100 điểm` (hoặc `0 điểm` nếu tuyệt đối không có độ lệch).

## 5. Root Cause Analysis (Phân tích sâu cho nhóm điểm cao nhất)

[Nếu bất kỳ nhóm lỗi nào ở Mục 4 chiếm từ 40 điểm trở lên, phân tích sâu nguyên nhân gốc rễ. Tại sao cổng RRI, 4-Lens Review, Red-Team hay Verify lại để lọt vấn đề này?]

## 6. Shortcut Debt Harvest (Thu hoạch và Rà soát Nợ Làm tắt)

Kiểm tra các mục trong `vibecode-artifacts/shortcut-ledger.csv` liên quan đến tính năng này.

| Mã Quyết định | Mô tả đường tắt đã chọn (`Completeness <= 7/10`) | Điều kiện kích hoạt nâng cấp (`Upgrade Trigger`) | Đã chạm ngưỡng kích hoạt chưa? | Quyết định ở chu kỳ tới |
|---|---|---|---|---|
| D01 | [Mô tả ngắn] | [Điều kiện cụ thể] | [Chưa | Đã chạm] | [Giữ nguyên | Mở TIP nâng cấp lên 10/10] |

## 7. Lesson Learned (Bài học đúc kết cho hệ thống)

[Rút ra quy tắc hoặc kinh nghiệm cụ thể để cập nhật vào `AGENTS.md` hoặc bộ câu hỏi RRI cho các chu kỳ sau. Tránh viết khẩu hiệu chung chung.]

- **Lesson 1.** [Bài học cụ thể, có thể kiểm tra được]
- **Lesson 2.** [Bài học cụ thể, có thể kiểm tra được]

## 8. Action Items cho Chu kỳ tiếp theo

- [ ] **Action 1.** [Hành động cụ thể, gắn với mã TIP dự kiến hoặc file cần cập nhật]
- [ ] **Action 2.** [Hành động cụ thể]

## 9. Confidence Trend (Xu hướng độ chính xác của Dự đoán)

[So với các thẻ Calibration Card trước đó, khoảng cách Delta giữa Dự đoán và Thực tế của đội ngũ đang thu hẹp hay mở rộng? Mảng nào đã kiểm soát tốt, mảng nào vẫn hay ước lượng sai?]
