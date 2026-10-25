# Giao thức Phỏng vấn RRI, Thẻ Quyết định `D<N>` và Cổng Duyệt Kế hoạch Đa Lăng kính

Tài liệu này hướng dẫn chi tiết cho Chủ thầu ở **Bước 2 (RRI)**, **Bước 3 (VISION)** và **Bước 4 (BLUEPRINT)**, kết hợp phương pháp phỏng vấn ngược 5 góc nhìn của Vibecode v6.0 với cơ chế **Decision Briefs / Completeness Score (`gstack`)**, **Autoplan 4-Lens Gate (`gstack /autoplan`)**, **4-Persona Red-Team (`ak-plan`)** và **Ultra Verifier Best-of-5 (`ak-brainstorm`)**.

## 1. Phỏng vấn Ngược RRI có Chọn lọc và Ngân hàng Câu hỏi 5 Góc nhìn

Sai lầm thường gặp khi áp dụng RRI máy móc là hỏi Con người hàng chục câu hỏi kỹ thuật mà lẽ ra chỉ cần đọc mã nguồn trong 2 phút là biết. Trong Vibecode Kit v6.1, Chủ thầu thực hiện RRI theo 3 bước lọc.

1. **Bước lọc 1 · Tự giải từ `SCAN REPORT`.** Đọc kỹ cấu trúc dự án, `package.json`, schema cơ sở dữ liệu và các bài test hiện có để tự điền tối đa các câu trả lời thuộc góc nhìn Developer, QA và Operator.
2. **Bước lọc 2 · Phân loại Quyết định 3 tầng.**
   - **Mechanical (Cơ học).** Tự quyết theo tiêu chuẩn kỹ thuật tốt nhất và ghi vào bảng Decisions Log.
   - **Taste (Đánh đổi cân bằng).** Đề xuất sẵn phương án khuyến nghị `(recommended)` và gom thành một danh sách gọn để Chủ nhà duyệt nhanh.
   - **User Challenge (Chiến lược / Cửa một chiều).** Trình bày thành từng thẻ quyết định **Decision Brief `D<N>`** theo đúng bản mẫu `templates/RRI-template.md`.
3. **Bước lọc 3 · Chấm điểm Độ hoàn thiện (`Completeness X/10`) và Ghi sổ Nợ Làm tắt (`Shortcut Debt`).**
   - Điểm `10/10` nghĩa là xử lý trọn vẹn cả luồng chính, các trường hợp biên, xử lý lỗi và khả năng mở rộng hợp lý.
   - Điểm `7/10` nghĩa là giải quyết tốt luồng chính (happy path) nhưng tạm gác lại một số trường hợp biên hiếm gặp.
   - Điểm `3/10` đến `5/10` là giải pháp tình thế để kiểm chứng nhanh giả thuyết.
   - Với sự hỗ trợ của AI Builder, khoảng cách thời gian giữa phương án `7/10` và `10/10` thường chỉ chênh nhau vài chục phút máy chạy. Vì vậy, Chủ thầu luôn ưu tiên khuyến nghị phương án có độ hoàn thiện cao, trừ khi Chủ nhà chủ động chọn phương án rút gọn kèm điều kiện nâng cấp rõ ràng trong `shortcut-ledger.csv`.

### Ngân hàng Câu hỏi Cốt lõi theo 5 Góc nhìn (Chỉ hỏi những điểm chưa rõ sau khi Scan)
- **End User (Người dùng cuối).** Ai là người trực tiếp thao tác? Hành động quan trọng nhất họ cần hoàn thành trong dưới 10 giây là gì? Khi mạng chậm hoặc thao tác sai thì màn hình hiển thị gì?
- **Business Analyst (Nghiệp vụ).** Quy tắc bất biến nào về tiền bạc, số lượng, trạng thái không bao giờ được phép vi phạm? Trường hợp ngoại lệ nào hay xảy ra nhất trong thực tế vận hành?
- **QA / Tester (Kiểm thử).** Làm sao biết chắc chắn tính năng này đã chạy đúng? Dữ liệu đầu vào lớn nhất, nhỏ nhất, rỗng hoặc sai định dạng sẽ trông như thế nào?
- **Developer (Kỹ thuật).** Thành phần nào trong dự án hiện tại có thể tái sử dụng ngay? Ranh giới giao tiếp với hệ thống bên ngoài nằm ở đâu và nếu hệ thống đó ngừng phản hồi thì xử lý thế nào?
- **Operator (Vận hành).** Cần thêm biến môi trường hay cấu hình mới nào không? Khi lên môi trường thật làm sao biết tính năng đang hoạt động khỏe mạnh và nếu cần quay lui (rollback) thì mất bao lâu?

## 2. Chuỗi Duyệt Kế hoạch 4 Lăng kính Tuần tự (Autoplan 4-Lens Sequential Gate)

Ở Bước 3 (`VISION`) và Bước 4 (`BLUEPRINT`) cho các tác vụ mức **R2** và **R3**, Chủ thầu rà soát bản thiết kế qua 4 lăng kính theo đúng thứ tự cố định. Lăng kính Kỹ thuật (**Eng**) luôn chạy cuối cùng để khóa toàn bộ các điều chỉnh từ ba lăng kính trước.

### Lăng kính 1 · CEO / Product Lens (Tầm nhìn & Chế độ Phạm vi)
- Đặt câu hỏi xem yêu cầu hiện tại đã chạm đúng nỗi đau gốc rễ của người dùng chưa, hay chỉ đang giải quyết phần ngọn.
- Chọn rõ một trong bốn chế độ phạm vi gồm **Expansion** (Mở rộng để đạt chất lượng 10 sao nếu chi phí tăng thêm bằng AI là rất nhỏ), **Selective Expansion** (Giữ lõi và chỉ mở rộng 1 đến 2 điểm đắt giá nhất), **Hold Scope** (Giữ nguyên phạm vi đã chốt) hoặc **Reduction** (Cắt giảm tối đa để ra mắt bản thử nghiệm ngay lập tức).

### Lăng kính 2 · Design Lens (Chỉ kích hoạt khi có Giao diện Người dùng)
- Kiểm tra phân cấp thị giác, tính nhất quán với hệ thống thiết kế hiện có và khả năng truy cập (Accessibility).
- Bắt buộc thiết kế đủ 4 trạng thái cho mọi màn hình gồm **Trạng thái Rỗng (Empty state)**, **Trạng thái Đang tải (Loading state)**, **Trạng thái Lỗi (Error state)** và **Trạng thái Đầy dữ liệu (Populated state)**.
- Loại bỏ các dấu hiệu giao diện rập khuôn vô hồn kiểu AI (AI Slop như lạm dụng dải màu tím xanh lòe loẹt, thẻ bo góc vô nghĩa, văn bản giữ chỗ chung chung).

### Lăng kính 3 · DX Lens (Chỉ kích hoạt khi có API, CLI, SDK hoặc Công cụ cho Lập trình viên)
- Tối ưu hóa thời gian từ lúc mở tài liệu đến lúc chạy thành công lệnh đầu tiên (Time-To-Hello-World).
- Thiết kế **Thông báo lỗi thân thiện cho cả Người và Agent (Agent-Ready Errors)** gồm cái gì vừa sai, tại sao nó sai và câu lệnh hoặc thao tác cụ thể để sửa ngay.

### Lăng kính 4 · Eng Manager Lens (Luôn chạy cuối cùng)
- Vẽ rõ sơ đồ luồng dữ liệu, các trạng thái chuyển đổi và ranh giới giao dịch (transaction boundaries).
- Kiểm tra an toàn đồng thời (race conditions), giới hạn thời gian chờ (timeouts), thử lại có kiểm soát (idempotent retries) và khóa chặt ma trận kiểm thử cho từng `REQ-ID`.

## 3. Phản biện Red-Team 4 Góc nhìn và Chế độ Ultra Best-of-5

Trước khi trình Blueprint cho Chủ nhà ký duyệt ở các dự án quan trọng, Chủ thầu thực hiện vòng phản biện nghịch cảnh (**Red-Team Gate**) qua 4 vai đối kháng.

1. **Kẻ Tấn công Giả định (Assumptions Challenger).** Chỉ ra 3 giả định ngầm trong Blueprint mà nếu sai sẽ làm sập toàn bộ thiết kế, từ đó bổ sung bước kiểm tra sớm.
2. **Kỹ sư Gây sập Hệ thống (Failure Mode Injector).** Giả lập tình huống mất kết nối mạng, đĩa đầy, dữ liệu trùng lặp gấp đôi hoặc người dùng bấm nút liên tục 10 lần trong 1 giây xem Blueprint đã có cơ chế đỡ chưa.
3. **Người Gác cổng Phạm vi (YAGNI / Scope Auditor).** Tìm các lớp trừu tượng hóa thừa thãi, các bảng dữ liệu hoặc cấu hình được vẽ ra chỉ để "dự phòng tương lai xa" mà không phục vụ trực tiếp cho yêu cầu hiện tại.
4. **Kiểm toán viên Bảo mật (Security & Privacy Reviewer).** Rà soát phân quyền truy cập, nguy cơ tiêm nhiễm câu lệnh (injection), lộ dữ liệu nhạy cảm trong log và an toàn chuỗi cung ứng thư viện.

### Khi nào bật Chế độ Ultra Verifier (Best-of-5)?
Khi bài toán ở mức **R3** có độ khó kỹ thuật đặc biệt cao (ví dụ thiết kế bộ máy đồng bộ dữ liệu phân tán hoặc thuật toán cốt lõi có nhiều hướng tiếp cận xung đột), Chủ thầu đóng gói toàn bộ kết quả `SCAN` và `RRI` thành một **Gói Bằng chứng Bất biến (Immutable Evidence Packet)**, phát cho **5 luồng phân tích độc lập (chỉ đọc)** cùng thiết kế phương án. Sau đó, một phiên Trọng tài trên mô hình mạnh nhất sẽ chấm điểm theo tiêu chí rõ ràng để chọn ra bản thiết kế chiến thắng đưa vào Blueprint.
