# Giao thức Khảo sát Hiện trạng (SCAN) và Giải phẫu Dự án (X-Ray Protocol)

Tài liệu này hướng dẫn cách thực hiện **Bước 1 (SCAN)** cho dự án mới hoặc dự án đang phát triển, đồng thời cung cấp quy trình **Giải phẫu Toàn diện (X-Ray Protocol)** khi tiếp nhận bàn giao một kho mã nguồn cũ, kiểm toán kỹ thuật hoặc chuẩn bị tài liệu chuyển giao hệ thống.

## 1. Giao thức Bước 1 · SCAN (Khảo sát Nhanh và Khảo sát Đầy đủ)

Mục tiêu của Bước 1 là thu thập các sự thật đã kiểm chứng (**`OBSERVED`**) về kho mã nguồn và môi trường thực thi trong thời gian ngắn nhất để làm đầu vào vững chắc cho bước RRI và Vision.

### Chế độ 1A · Quét Khởi tạo cho Dự án Mới (Greenfield Scan · 2 đến 5 phút)
Khi thư mục dự án mới khởi tạo hoặc còn trống, Thợ thi công kiểm tra nhanh 4 yếu tố.
1. **Công cụ và Runtime trên máy trạm.** Phiên bản ngôn ngữ lập trình (`node -v`, `python3 --version`, `go version`...), trình quản lý gói và công cụ kiểm soát phiên bản Git.
2. **Tài nguyên Tri thức Đi kèm.** Dự án có sẵn tài liệu yêu cầu ban đầu, bộ thẻ sự thật từ **Bộ 01 (`Fact Cards`)** hay kho nguồn sự thật **Bộ 02 (`Kernel Registry L1–L4`)** nào cần kết nối không?
3. **Ràng buộc Hạ tầng Đích.** Dự kiến chạy trên máy cá nhân, máy chủ đám mây hay thiết bị di động?
4. **Đề xuất Risk Tier ban đầu.** Phân loại sơ bộ từ `R0` đến `R3` dựa trên mục tiêu của Chủ nhà.

### Chế độ 1B · Quét Hiện trạng cho Dự án Đang có (Existing Codebase Scan · 5 đến 15 phút)
Khi làm việc trên một kho mã nguồn đã có sẵn, Thợ thi công thu thập thông tin theo đúng cấu trúc `SCAN REPORT` dưới đây.

```markdown
# SCAN-NNN · Báo cáo Khảo sát Hiện trạng Kho Mã nguồn

**Date.** YYYY-MM-DD
**Repository / Branch.** [Tên kho và nhánh hiện tại]
**WTREE_FINGERPRINT.** [Mã băm 16 ký tự hiện tại]

## 1. Công nghệ và Cấu trúc Thư mục (OBSERVED)
- **Ngôn ngữ & Framework.** [Đọc từ package.json / pyproject.toml / go.mod...]
- **Cấu trúc thư mục chính.** [Liệt kê các thư mục cốt lõi và vai trò của từng thư mục]
- **Điểm vào ứng dụng (Entrypoints).** [Các file khởi chạy chính]

## 2. Quy ước Mã nguồn và Mẫu Thiết kế Đang dùng (OBSERVED & DERIVED)
- **Cách tổ chức module và đặt tên.** [Quy ước thực tế đang áp dụng trong code]
- **Cơ chế quản lý trạng thái, cơ sở dữ liệu và xác thực.** [Mô tả kèm đường dẫn file]
- **Các hàm tiện ích dùng chung có sẵn (Reuse Candidates).** [Liệt kê các file helper/utils để tái sử dụng ở Bước 6]

## 3. Sức khỏe Hệ thống Kiểm thử và Công cụ Kiểm tra (OBSERVED)
- **Lệnh chạy kiểm thử hiện có.** `[Lệnh test]` → Kết quả chạy thử hiện tại `[X pass / Y fail]`
- **Lệnh kiểm tra kiểu tĩnh và linter.** `[Lệnh typecheck/lint]` → Kết quả hiện tại

## 4. Điểm nghẽn, Lỗ hổng và Giả định Cần Làm rõ (Gaps & ASSUMED)
- **Điểm mù / Rủi ro phát hiện.** [Các vùng code thiếu test, phụ thuộc lỗi thời hoặc có cảnh báo bảo mật]
- **Các giả định cần xác nhận ở bước RRI (ASSUMED).** [Liệt kê 3 đến 5 điểm cần hỏi Chủ thầu/Chủ nhà]
```

## 2. Giao thức Giải phẫu Toàn diện (X-Ray Protocol · Dùng khi Tiếp nhận hoặc Bàn giao Lớn)

Khi bạn nhận lại một dự án từ nhóm khác, chuẩn bị bàn giao đồ án tốt nghiệp hoặc cần kiểm toán toàn bộ hệ thống sau nhiều vòng phát triển, hãy chạy **Giao thức X-Ray 6 Lớp**. Khác với bản `SCAN` ngắn gọn phục vụ từng tác vụ, bản báo cáo `X-RAY REPORT` là bức ảnh chụp cắt lớp toàn bộ dự án.

### Lớp 1 · Bản đồ Kiến trúc và Phụ thuộc (Architecture & Dependency Map)
- Vẽ sơ đồ toàn bộ các thành phần trong hệ thống, các dịch vụ bên ngoài mà hệ thống gọi tới và chiều di chuyển của dữ liệu từ giao diện người dùng xuống tới cơ sở dữ liệu.
- Liệt kê các thư viện bên thứ ba quan trọng nhất và đánh dấu những thư viện đã ngừng bảo trì hoặc có rủi ro khóa chặt nhà cung cấp (vendor lock-in).

### Lớp 2 · Giải phẫu Mô hình Dữ liệu và Nguồn Sự thật (Data & State Anatomy)
- Liệt kê toàn bộ các bảng dữ liệu, mối quan hệ khóa ngoại, các chỉ mục (indexes) và quy trình di trú dữ liệu (migrations).
- Đối chiếu với phương pháp **Bộ 02 (Kernel Registry)**. Chỉ ra những con số cấu hình, công thức tính toán hoặc quy tắc nghiệp vụ nào đang bị viết cứng (hardcode) rải rác trong code cần được gom về kho chuẩn.

### Lớp 3 · Đường đi của Các Luồng Nghiệp vụ Trọng tâm (Critical Execution Paths)
- Chọn ra 3 đến 5 luồng nghiệp vụ quan trọng nhất của sản phẩm (ví dụ luồng đăng ký và đăng nhập, luồng tạo đơn và thanh toán, luồng xuất báo cáo).
- Với mỗi luồng, ghi rõ chuỗi file và hàm đi qua theo thứ tự từ điểm đầu đến điểm cuối kèm số dòng (`file:line`) để bất kỳ kỹ sư hay AI agent mới nào cũng có thể tra cứu trong 1 phút.

### Lớp 4 · Kiểm toán Bảo mật và Ranh giới Tin cậy (Security & Trust Boundaries)
- Kiểm tra cách hệ thống quản lý khóa bí mật, xác thực người dùng, phân quyền theo vai trò và làm sạch dữ liệu đầu vào.
- Chỉ rõ các bề mặt tiếp xúc với internet công cộng và cơ chế bảo vệ hiện có.

### Lớp 5 · Đánh giá Độ phủ Kiểm thử và Sổ nợ Kỹ thuật (Test Health & Debt Inventory)
- Đo lường tỷ lệ các luồng nghiệp vụ trọng tâm ở Lớp 3 đã có bài kiểm thử tự động bảo vệ.
- Tổng hợp toàn bộ các mục trong `shortcut-ledger.csv`, các ghi chú `TODO` / `FIXME` trong mã nguồn và xếp hạng theo mức độ rủi ro.

### Lớp 6 · Cẩm nang Vận hành Khẩn cấp (15-Minute Runbook)
- Viết hướng dẫn từng bước để một người mới có thể kéo mã nguồn về, cài đặt môi trường, chạy bộ kiểm thử và khởi động ứng dụng thành công trong vòng dưới 15 phút.
- Nêu rõ cách kiểm tra sức khỏe hệ thống và cách khôi phục về phiên bản ổn định gần nhất khi xảy ra sự cố.
