# CC-NNN · [Tên task]

**Date deployed.** YYYY-MM-DD
**Date calibrated.** YYYY-MM-DD
**Linked TIP.** TIP-NNN
**Linked Completion Report.** CR-NNN

## 1. Prediction

Lấy từ Success Criteria của TIP.

- Criterion 1. [Prediction]
- Criterion 2. [Prediction]
- Criterion 3. [Prediction]

## 2. Actual

Quan sát sau khi deploy.

- Criterion 1. [Actual observation]
- Criterion 2. [Actual observation]
- Criterion 3. [Actual observation]

## 3. Delta

[Mô tả khoảng cách giữa prediction và actual. Nếu có pattern,
 ghi rõ. Ví dụ "actual chậm hơn prediction 30%" hoặc
 "actual có bug ở module X không lường trước".]

## 4. Error allocation (tổng = 100 điểm)

Phân bổ 100 điểm cho 4 loại lỗi.

- **Modeling**. [N điểm]
  Hiểu sai bài toán. TIP hoặc Blueprint không đúng intent thật.

- **Timing**. [N điểm]
  Deploy sai thời điểm. Ship lúc user chưa ready hoặc bị conflict
  với deploy khác.

- **World-change**. [N điểm]
  Thế giới thay đổi giữa lúc plan và lúc deploy. Ví dụ requirement
  thay đổi hoặc dependency upgrade.

- **Execution**. [N điểm]
  Thi công kém. Code có bug, performance chậm, UX không tốt.

Tổng phải = 100.

## 5. Root cause analysis (cho điểm cao nhất)

[Nếu một loại lỗi chiếm > 40 điểm, phân tích sâu root cause.
 Tại sao loại đó cao? Pattern gì gây ra?]

## 6. Lesson learned

[Điều rút ra cụ thể cho các cycle vibecode tương lai. Tránh
 lesson chung chung. Cụ thể đến mức actionable.]

- Lesson 1. [...]
- Lesson 2. [...]

## 7. Action items cho cycle sau

Liệt kê hành động cụ thể.

- [ ] Action 1
- [ ] Action 2
- [ ] Action 3

## 8. Confidence trend

[Xem qua các Calibration Card trước, confidence của Chủ thầu
 trong predictions có tăng hay giảm? Pattern gì?]

[Optional. Bỏ qua nếu là CC-001.]
