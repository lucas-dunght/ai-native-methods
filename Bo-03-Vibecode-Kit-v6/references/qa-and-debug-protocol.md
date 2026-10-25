# Giao thức Kiểm thử Bề mặt Thật (Surface-Aware QA) và Gỡ lỗi Nguyên nhân Gốc (Root-Cause Debug)

Tài liệu này định nghĩa quy trình kiểm soát chất lượng ở **Bước 6 (BUILD)**, **Bước 7 (VERIFY)** và quy trình xử lý khi gặp lỗi phức tạp trong Vibecode Kit v6.1, kết hợp từ **`gstack /qa`**, **`gstack /test-audit`**, **`gstack /investigate`** và **`ak-debug` v4.2**.

## 1. Giao thức Gỡ lỗi Nguyên nhân Gốc rễ (Systematic Root-Cause Debugging)

### Luật Sắt (The Iron Law of Debugging)
**KHÔNG BAO GIỜ SỬA CODE KHI CHƯA CHỨNG MINH ĐƯỢC NGUYÊN NHÂN GỐC RỄ.**

Khi gặp một bài kiểm thử thất bại, một lỗi biên dịch hoặc hành vi sai lệch, việc đoán mò và sửa thử từng dòng ("thử đổi chỗ này xem có chạy không") là con đường nhanh nhất làm nát kho mã nguồn. Thợ thi công bắt buộc đi qua 4 pha theo đúng thứ tự.

### Pha 1 · Tái hiện lỗi và Thu thập Bằng chứng (Reproduce & Evidence Capture)
- Chạy một câu lệnh cụ thể để tái hiện lỗi một cách nhất quán.
- Đọc toàn bộ thông báo lỗi và ngăn xếp lời gọi hàm (stack trace) từ đầu đến cuối, không đoán qua dòng cuối cùng.
- Khóa phạm vi chỉnh sửa (`Scope Freeze`) vào đúng module đang điều tra để không làm ảnh hưởng các vùng mã nguồn khác.

### Pha 2 · Truy ngược Dòng dữ liệu về Nguồn phát sinh (Backward Root-Cause Tracing)
- Bắt đầu từ nơi chương trình phát nổ hoặc trả về kết quả sai, lần ngược từng bước gọi hàm lên phía trên để tìm chính xác nơi dữ liệu hợp lệ bắt đầu biến thành dữ liệu hỏng.
- Nguyên tắc sửa lỗi ở đúng cao độ nguyên nhân là sửa tại nơi sinh ra dữ liệu sai hoặc tại hàm dùng chung mà các nhánh cùng đi qua, không đắp vá triệu chứng ở hàng chục nơi gọi hàm.

### Pha 3 · Kiểm định Giả thuyết Đơn biến (Single-Variable Hypothesis Testing)
- Đặt ra giả thuyết cụ thể theo cấu trúc "Lỗi xảy ra vì tại file X dòng Y, khi điều kiện Z xuất hiện thì giá trị trả về bị lệch".
- Kiểm chứng giả thuyết bằng cách in nhật ký chẩn đoán tạm thời hoặc viết một bài kiểm thử nhỏ chỉ nhắm vào đúng điều kiện đó. Mỗi lần chỉ thay đổi đúng một biến số.

### Pha 4 · Quy tắc Dừng 3-Strike và Sửa lỗi Có Phòng thủ Chiều sâu (3-Strike Stop & Fix)
- **Cổng chặn 3-Strike.** Nếu đã thử 3 giả thuyết hoặc 3 lần sửa liên tiếp mà lỗi vẫn còn hoặc làm phát sinh lỗi mới, Thợ phải **DỪNG NGAY LẬP TỨC**. Khôi phục lại trạng thái sạch trước khi sửa mò, ghi rõ 3 phương án đã thử cùng toàn bộ đầu ra lỗi và báo cáo lên Chủ thầu / Quân sư Kongming để xem xét lại kiến trúc.
- Khi đã chứng minh được nguyên nhân gốc rễ, viết một bài kiểm thử tái hiện lỗi chạy đỏ trước, áp dụng bản sửa lỗi gọn sạch để bài kiểm thử chuyển sang xanh, rồi xóa bỏ mọi đoạn mã chẩn đoán tạm thời.

## 2. Giao thức Kiểm thử Nhận diện Bề mặt (Surface-Aware QA · 3 Tiers)

Ở Bước 7 (`VERIFY`), hoạt động kiểm thử không dừng ở việc chạy lại bộ unit test sẵn có mà phải kiểm tra trực tiếp trên bề mặt hoạt động thực tế của sản phẩm theo 3 tầng.

### Tầng 1 · Kiểm chứng Tĩnh và Bảo mật Cơ bản (Static & Gate G0)
- Quét phát hiện lộ khóa bí mật, mật khẩu hoặc token trong toàn bộ các file mới và file thay đổi (Gate G0 · nếu phát hiện lộ khóa thì chặn đứng ngay lập tức).
- Chạy trình kiểm tra kiểu tĩnh (TypeScript/Mypy...), linter và kiểm tra định dạng.

### Tầng 2 · Kiểm thử Đơn vị, Biên và Tích hợp (Unit, Boundary & Integration)
- Kiểm tra toàn bộ các tiêu chí nghiệm thu `AC` trong `TIP`.
- Thử thách các trường hợp biên gồm đầu vào rỗng (`null`, `undefined`, chuỗi trống `""`, mảng rỗng `[]`), dữ liệu cực lớn, ký tự tiếng Việt có dấu / Unicode đặc biệt, gọi lặp hai lần liên tiếp và quyền truy cập không hợp lệ.

### Tầng 3 · Thăm dò Bề mặt Thật (Live Surface Exploration)
Tùy theo loại sản phẩm, chọn đúng công cụ kiểm chứng bề mặt thật thay vì chỉ nhìn mã nguồn.
- **Bề mặt Web / Giao diện (Browser Surface).** Mở ứng dụng trên trình duyệt thật, thực hiện thao tác bấm, điền biểu mẫu, kiểm tra bố cục trên màn hình máy tính và điện thoại, chụp ảnh màn hình bằng chứng và kiểm tra cửa sổ Console đảm bảo không có lỗi JavaScript ngầm.
- **Bề mặt API / Dịch vụ (API Surface).** Khởi chạy máy chủ cục bộ, gửi các yêu cầu HTTP/gRPC thật với đầy đủ trường hợp hợp lệ và không hợp lệ, kiểm tra mã trạng thái trả về, cấu trúc dữ liệu và độ trễ.
- **Bề mặt Công cụ Dòng lệnh (CLI Surface).** Chạy trực tiếp câu lệnh với các cờ tham số đúng, tham số sai, đường dẫn không tồn tại và kiểm tra cả `stdout`, `stderr` lẫn mã thoát (`exit code`).
- **Bề mặt Tiến trình Ngầm / Webhook (Worker & Webhook Surface).** Phát sự kiện mẫu vào hàng đợi hoặc endpoint, kiểm tra khả năng xử lý trùng lặp (idempotency) và khả năng phục hồi khi lỗi giữa chừng.

### Luật Bắt buộc Regression Đỏ trước Xanh sau (Red-Before-Green Rule)
Mọi lỗi phát hiện được trong quá trình thăm dò QA ở Bước 7 phải được chuyển hóa thành một bài kiểm thử tự động mới. Bài kiểm thử này bắt buộc phải **chạy đỏ (thất bại)** trên mã nguồn đang lỗi để chứng minh nó bắt đúng bệnh, sau đó mới sửa mã nguồn để bài kiểm thử **chuyển sang xanh (thành công)**.

## 3. Kiểm toán Bộ Kiểm thử (Test Audit · Chống Test Giả tạo)

Để ngăn chặn tình trạng AI viết các bài kiểm thử vô giá trị nhằm lấy số lượng ("test theatre"), Chủ thầu hoặc Trọng tài thực hiện rà soát nhanh bộ kiểm thử theo 4 tiêu chí.

1. **Cấm bài kiểm thử không có khẳng định (Assertion-free tests).** Mọi bài kiểm thử phải kiểm tra kết quả đầu ra hoặc trạng thái thay đổi cụ thể, không chấp nhận bài test chỉ gọi hàm rồi kết thúc hoặc chỉ kiểm tra `expect(true).toBe(true)`.
2. **Cấm bài kiểm thử tự chứng minh (Tautological mocks).** Không chấp nhận bài test giả lập (mock) chính hàm đang cần kiểm tra rồi khẳng định hàm giả lập trả về đúng giá trị vừa gán.
3. **Cấm kiểm thử hành vi bằng cách đếm chữ trong file mã nguồn (Source-grep tests).** Trừ khi đang kiểm tra quy tắc văn phong hoặc cấu trúc tài liệu, các bài kiểm thử phần mềm phải gọi và chạy hàm thật chứ không đọc file `.ts`/`.py` như văn bản để tìm chuỗi ký tự.
4. **Cấm làm yếu bài kiểm thử cũ để qua cổng (No Gate Weakening).** Thợ tuyệt đối không được tự ý xóa bài kiểm thử cũ, tăng thời gian chờ vô lý hoặc thêm cờ bỏ qua (`skip` / `todo`) để làm xanh báo cáo. Mọi thay đổi đối với bài kiểm thử hiện có phải được giải trình rõ trong mục `DEVIATIONS` của `Completion Report`.
