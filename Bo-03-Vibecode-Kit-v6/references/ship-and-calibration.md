# Giao thức Phát hành Hai Chặng (Dual-Stage Ship) và Hiệu chỉnh Sau Phát hành (Calibration 100 điểm)

Tài liệu này hướng dẫn chi tiết cho **Bước 8 (REFINE, SHIP & CALIBRATION)** của Vibecode Kit v6.1, kết hợp quy trình phát hành hai chặng có hội tụ CI của **`ak-ship` v2.4 / `ak-vibe` v1.5** và quy trình kiểm toán tài liệu, theo dõi sau phát hành của **`gstack /ship`**, **`/land-and-deploy`**, **`/canary`** gắn thẳng vào **Thẻ Hiệu chỉnh 100 điểm (`Calibration Card`)** của Vibecode Kit.

## 1. Quy trình Phát hành Chuẩn và Phát hành Hai Chặng (`Beta -> Stable`)

Trước khi phát hành bất kỳ nhánh tính năng nào, Chủ thầu và Thợ phải đảm bảo 4 điều kiện tiên quyết.
1. Tất cả các gói `TIP` trong phạm vi đợt phát hành đều đã có `Completion Report` ở trạng thái `DONE`.
2. Bằng chứng kiểm thử trong sổ cái đạt trạng thái tươi mới (`FRESH`), khớp với dấu vân tay `WTREE_FINGERPRINT` hiện tại.
3. Cổng quét khóa bí mật (Gate G0) và cổng Trọng tài độc lập (ở mức R2/R3) đã thông qua với `0 lỗi nghiêm trọng`.
4. Tài liệu dự án (`README.md`, hướng dẫn cấu hình, nhật ký thay đổi `CHANGELOG.md`) đã được đồng bộ với hành vi mới của mã nguồn.

### Chế độ 1 · Phát hành Một Chặng (Single-Stage Ship · Cho dự án R0/R1 hoặc kho chỉ có 1 nhánh chính)
1. Đồng bộ nhánh chính (`git fetch` và hợp nhất nhánh gốc vào nhánh làm việc, chạy lại kiểm thử nếu có thay đổi).
2. Cập nhật phiên bản và `CHANGELOG.md` (nếu dự án có quản lý phiên bản).
3. Đóng gói commit theo chuẩn Conventional Commits (`feat`, `fix`, `docs`, `refactor`, `test`), đẩy nhánh lên kho từ xa và tạo Pull Request có đính kèm tóm tắt bằng chứng từ `Completion Report`.

### Chế độ 2 · Phát hành Hai Chặng (Dual-Stage Ship `Beta -> Stable` · Cho dự án R2/R3)
Đối với các dự án có tách biệt nhánh thử nghiệm (`beta`, `dev`, `staging`) và nhánh chính thức (`main`, `master`, `stable`), quy trình phát hành đi qua hai chặng tách biệt có cổng chặn cứng.

```
Nhánh Tính năng (feat/tip-NNN)
      │
      ▼  [Chặng 1 · Ship Beta]
Nhánh Thử nghiệm (beta / dev / staging)
      │
      ├──► Chạy CI/CD + Kiểm thử bề mặt thật (Canary / Staging QA)
      │    Nếu CI đỏ -> Tạo nhánh fix -> Duyệt & Hợp nhất lại vào beta cho tới khi XANH
      │
      ▼  [Cổng chặn Chặng 2 · Kiểm tra danh sách commit & Xác nhận ổn định]
Nhánh Chính thức (main / stable)
      │
      ▼  [Theo dõi sau phát hành & Lập Calibration Card 100 điểm]
Hoàn tất Chu kỳ
```

Các quy tắc an toàn tuyệt đối trong Phát hành Hai Chặng.
- **Không vượt rào khi Beta chưa xanh.** Tuyệt đối không mở hoặc hợp nhất nhánh lên `stable` khi hệ thống kiểm thử tự động (CI) hoặc môi trường `beta` đang báo lỗi hoặc đang chạy dở.
- **Kiểm tra chống cuốn theo commit lạ (Unrelated-Work Sweep Check).** Trước khi tạo Pull Request nâng cấp từ `beta` lên `stable`, phải liệt kê toàn bộ danh sách commit nằm giữa hai nhánh (`git log origin/main..origin/beta --oneline`). Nếu phát hiện có commit của tính năng khác chưa được nghiệm thu nằm lẫn trong nhánh `beta`, phải dừng lại báo cáo Con người để chọn phương án tách nhánh sạch thay vì hợp nhất mù quáng.
- **Không bao giờ đẩy cưỡng bức (`git push --force`)** lên nhánh dùng chung hoặc nhánh chính thức.

## 2. Giám sát Sau Phát hành (Canary Check) và Khép vòng Calibration Card 100 điểm

Phát hành code lên nhánh chính thức chưa phải là điểm kết thúc của chu kỳ Vibecode. Điểm tạo nên sự tiến hóa vượt bậc của đội ngũ là bước đối chiếu thực tế sau phát hành.

### Bước 8A · Quan sát Thực tế (Post-Deploy Observation)
Sau khi tính năng đi vào hoạt động (ngay lập tức đối với công cụ cục bộ R1, hoặc sau 1 đến 3 ngày vận hành thực tế đối với ứng dụng R2/R3), thu thập các dữ kiện thuộc nhóm **`OBSERVED`**.
- Hệ thống có phát sinh lỗi ngoại lệ nào trên nhật ký vận hành hay cửa sổ Console không?
- Các chỉ số thành công nêu trong `TIP` (tốc độ phản hồi, tỷ lệ hoàn thành thao tác, độ chính xác của dữ liệu) đạt bao nhiêu phần trăm so với dự đoán?
- Có điều kiện kích hoạt nâng cấp (`Upgrade Trigger`) nào trong sổ nợ làm tắt `shortcut-ledger.csv` đã chạm ngưỡng thực tế chưa?

### Bước 8B · Phân bổ 100 điểm Sai số trong Calibration Card
Chủ thầu mở bản mẫu `templates/Calibration-Card.md` và lập thẻ `CC-NNN.md`. Khi có bất kỳ sự khác biệt nào giữa **Dự đoán (`Prediction`)** và **Thực tế (`Actual`)**, Chủ thầu phân bổ tổng cộng **100 điểm** vào 4 nhóm nguyên nhân.

1. **Modeling (Mô hình hóa & Đặc tả).** Chấm điểm cao vào đây khi code chạy đúng như TIP yêu cầu, nhưng sản phẩm vẫn chưa giải quyết trọn vẹn vấn đề thực tế vì lúc viết TIP hoặc Blueprint đã hiểu thiếu góc khuất nghiệp vụ.
   - *Cách khắc phục ở vòng sau.* Nâng cấp bộ câu hỏi RRI ở góc nhìn Business Analyst và End User, hoặc bổ sung kiểm tra dữ liệu thật ở Bước 1 SCAN.
2. **Timing (Thời điểm & Phối hợp).** Chấm điểm cao vào đây khi tính năng tốt nhưng phát hành lệch nhịp với dữ liệu nền, phụ thuộc vào một bên khác chưa sẵn sàng hoặc gây gián đoạn người dùng đang thao tác.
   - *Cách khắc phục ở vòng sau.* Cải thiện đồ thị phụ thuộc ở Bước 5 Task Graph và quy trình phát hành ở Bước 8.
3. **World-change (Biến đổi từ Môi trường Bên ngoài).** Chấm điểm cao vào đây khi API bên thứ ba, dịch vụ đám mây, trình duyệt hoặc quy định pháp lý thay đổi ngoài tầm kiểm soát giữa lúc lập kế hoạch và lúc phát hành.
   - *Cách khắc phục ở vòng sau.* Bổ sung lớp cô lập biến thiên (`Isolated Seam` trong phần Extension Trace của Blueprint) để giảm chấn khi bên ngoài thay đổi.
4. **Execution (Thi công & Nghiệm thu Kỹ thuật).** Chấm điểm cao vào đây khi đặc tả đã rõ nhưng code vẫn có lỗi logic, rò rỉ tài nguyên, giao diện vỡ hoặc bước Verify ở Bước 7 chưa kiểm tra kỹ bề mặt thật.
   - *Cách khắc phục ở vòng sau.* Siết chặt `Evidence Floor` trong TIP, bổ sung bài kiểm thử tự động vào bộ Regression và bật Trọng tài độc lập (`Arbiter C3`).

Mỗi thẻ `Calibration Card` khép lại bằng tối đa 3 hành động cụ thể (`Action Items`) được đưa thẳng vào đầu vào của chu kỳ Vibecode kế tiếp, tạo thành một vòng lặp tự hoàn thiện liên tục.
