# BP-NNN · [Tên dự án hoặc Tính năng]

**Date.** YYYY-MM-DD
**Risk tier.** R[1|2|3]
**Linked Scan.** SCAN-NNN
**Linked RRI.** RRI-NNN

## 1. Tóm tắt Tầm nhìn và Phạm vi (Vision & Scope Boundary)

- **Kết quả đầu ra cho người dùng (Outcome).** [Mô tả trạng thái hoàn thành rõ ràng mà người dùng hoặc hệ thống vận hành nhìn thấy được]
- **Các giới hạn bất biến (Constraints).** [Ngôn ngữ, nền tảng, thời gian phản hồi, yêu cầu bảo mật và tương thích ngược]
- **Ngoài phạm vi (Non-goals).** [Những phần việc liên quan nhưng kiên quyết không làm trong bản vẽ này]

## 2. Sơ đồ Kiến trúc và Luồng Dữ liệu (Architecture & Data Flow)

```
[Vẽ sơ đồ ASCII hoặc Mermaid flowchart thể hiện rõ các thành phần,
 chiều đi của dữ liệu, ranh giới xác thực và nơi xử lý lỗi]
```

## 3. Bộ Công nghệ và Bậc thang Tái sử dụng (Tech Stack & Reuse Ladder)

- **Language & Runtime.** [Phiên bản cụ thể]
- **Framework & Core Libraries.** [Các thư viện chính]
- **Database & Storage.** [Hệ quản trị cơ sở dữ liệu và cơ chế lưu đệm]
- **Hosting & CI/CD.** [Môi trường chạy thử nghiệm Beta và môi trường chính thức Stable]
- **Thành phần tái sử dụng từ dự án.** [Liệt kê các module, hàm tiện ích, giao diện có sẵn phải dùng lại]

## 4. Thiết kế Module và Hợp đồng Giao tiếp (Modules & Frozen Contracts)

### Module A · `[Tên Module]`
- **Trách nhiệm.** [Module này làm đúng một việc gì]
- **Đường dẫn file dự kiến.** `src/...`
- **Giao diện đầu vào và đầu ra (Interface Contract).** [Chữ ký hàm, kiểu dữ liệu hoặc API endpoint cần đóng băng trước khi chia cho nhiều Thợ]
- **Phụ thuộc.** [Các module hoặc dịch vụ mà Module A gọi tới]
- **Xử lý lỗi.** [Các mã lỗi và hành vi dự phòng khi thất bại]

### Module B · `[Tên Module]`
- **Trách nhiệm.** [...]
- **Đường dẫn file dự kiến.** `src/...`
- **Giao diện đầu vào và đầu ra.** [...]

## 5. Mô hình Dữ liệu và Tham chiếu Nguồn Sự thật (Data Model & SOT)

- **Schema bảng / Cấu trúc dữ liệu.**
```sql
-- Hoặc định nghĩa TypeScript / JSON Schema rõ ràng
```
- **Liên kết Kernel Registry (Bộ 02).** [Liệt kê các mã định danh `L1`, `L2`, `L3`, `L4` được tham chiếu]

## 6. Vết Mở rộng Tiến hóa (Evolutionary Extension Trace)

- **Biến thể thực tế tiếp theo có khả năng xảy ra cao nhất.** [Ví dụ thêm nhà cung cấp thanh toán thứ hai hoặc hỗ trợ đa ngôn ngữ]
- **Hợp đồng giữ nguyên không đổi (Stable Contract).** [Những file và giao diện nào sẽ không phải sửa khi biến thể đó xuất hiện]
- **Điểm cô lập biến thiên (Isolated Seam).** [File hoặc lớp chuyển đổi nào sẽ đón nhận thay đổi đó]
- **Những phần suy đoán đã cắt bỏ (YAGNI).** [Những lớp trừu tượng phức tạp nào đã quyết định không xây dựng ngay lúc này]

## 7. Bảng Ánh xạ Yêu cầu và Ma trận Kiểm thử (REQ-ID Mapping & Test Matrix)

| Mã REQ-ID | Mô tả yêu cầu | Module phụ trách | Mã TIP dự kiến | Phương pháp & Lệnh kiểm chứng (Verify Command) | Cấp bằng chứng yêu cầu |
|---|---|---|---|---|---|
| REQ-01 | [Yêu cầu 1] | Module A | TIP-001 | `[Lệnh chạy test]` | `unit-test` |
| REQ-02 | [Yêu cầu 2] | Module A + B | TIP-002 | `[Lệnh chạy tích hợp / E2E]` | `live-run` |

## 8. Kết quả Duyệt 4 Lăng kính và Phản biện Red-Team (4-Lens & Red-Team Gate)

- **Lăng kính CEO (Tầm nhìn & Phạm vi).** [Đã chọn chế độ Mở rộng / Giữ nguyên / Thu gọn nào và tại sao]
- **Lăng kính Design (Giao diện & Chống AI Slop).** [Điểm thiết kế X/10, bố cục, trạng thái rỗng/đang tải/lỗi, hoặc ghi Không áp dụng nếu không có UI]
- **Lăng kính DX (Trải nghiệm Lập trình viên & Agent).** [Độ rõ ràng của thông báo lỗi và tài liệu CLI/API, hoặc ghi Không áp dụng]
- **Lăng kính Eng (Kiến trúc & An toàn vận hành).** [Đã khóa sơ đồ trạng thái, kiểm soát đồng thời và giới hạn tài nguyên chưa]
- **Phản biện Red-Team 4 góc nhìn (Assumptions, Failure Modes, Scope, Security).** [Tóm tắt các lỗ hổng đã phát hiện khi tự phản biện và cách đã sửa ngay vào Blueprint này]

## 9. Danh mục Nợ Làm tắt đã Chấp thuận (Approved Shortcuts)

[Liệt kê các quyết định `D<N>` có điểm `Completeness <= 7/10` mà Chủ nhà đã đồng ý để ưu tiên tốc độ, kèm điều kiện nâng cấp. Ghi Không có nếu mọi mục đều chọn 10/10.]

## 10. Ký duyệt Khế ước (Blueprint Approval)

Blueprint này là khế ước kỹ thuật. Mọi thay đổi kiến trúc sau khi ký duyệt đều phải quay lại cập nhật từ bước Vision.

- **Trạng thái.** `[DRAFT | APPROVED | REVISED]`
- **Người phê duyệt (Homeowner / Chủ nhà).** [Tên người duyệt]
- **Ngày phê duyệt.** YYYY-MM-DD
