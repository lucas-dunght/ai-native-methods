# TIP-NNN · [Tên gói công việc ngắn gọn]

**Date.** YYYY-MM-DD
**Risk tier.** R[0|1|2|3]
**Priority.** P[0|1|2]
**Dependencies.** [Không có | Danh sách TIP phải hoàn thành trước]
**Linked Blueprint.** BP-NNN (Mục hoặc Module liên quan)
**Assigned Builder.** [Tên phiên Thợ thi công / Runtime / Model]
**Worktree / Branch.** [main | `.worktrees/tip-NNN` trên nhánh `feat/tip-NNN`]

## 1. Intent (Mục đích cốt lõi)

[Mô tả trong 1 đến 3 câu thật cụ thể về kết quả cần tạo ra sau khi hoàn thành gói công việc này. Không viết mơ hồ.]

## 2. Why & Context (Ngữ cảnh và Dẫn chiếu)

- **Lý do nghiệp vụ.** [Tại sao cần thực hiện gói công việc này và nó giải quyết yêu cầu `REQ-ID` nào]
- **Tài liệu & Kernel Registry tham chiếu.** [Mã ID sự thật L1/L2/L3 từ Bộ 02 hoặc Fact Card từ Bộ 01 nếu có]
- **Các file mẫu cần đọc trước.** [Danh sách các file có sẵn trong dự án để học quy ước đặt tên và cấu trúc]

## 3. Scope Freeze & Disjoint File Ownership (Khóa phạm vi sửa đổi)

Thợ thi công chỉ được phép tạo mới hoặc chỉnh sửa các đường dẫn nằm trong mục được phép ghi dưới đây.

- **Allowed write paths (Được phép ghi).**
  - `src/[đường-dẫn-file-1]`
  - `tests/[đường-dẫn-file-test-1]`
- **Read-only shared contracts (Hợp đồng dùng chung đã đóng băng, chỉ đọc).**
  - `src/types/[file-dùng-chung]`
- **Out of scope (Ngoài phạm vi).**
  - [Liệt kê rõ những tính năng hoặc thư mục tuyệt đối không chạm vào trong gói này để chống phình phạm vi]

## 4. Acceptance Criteria & Evidence Floor (Tiêu chí nghiệm thu cơ học)

Mỗi tiêu chí phải kiểm tra được bằng câu lệnh thực thi cụ thể, không đánh giá bằng cảm tính.

- **AC1 (Gherkin / Hành vi).** Khi `[điều kiện đầu vào]`, hệ thống thực hiện `[hành động]` và trả về `[kết quả quan sát được]`.
  - **Verify command.** `[Câu lệnh chạy test hoặc kiểm tra cơ học]`
- **AC2 (Trường hợp biên / Lỗi).** Khi `[dữ liệu rỗng, sai kiểu hoặc vượt ngưỡng]`, hệ thống trả về thông báo lỗi chuẩn và không làm hỏng trạng thái.
  - **Verify command.** `[Câu lệnh kiểm tra trường hợp biên]`
- **AC3 (Ràng buộc chất lượng).** Không lộ khóa bí mật trong mã nguồn, vượt qua kiểm tra kiểu tĩnh và linter.
  - **Verify command.** `[Câu lệnh kiểm tra kiểu / lint / secret scan]`

**Yêu cầu cấp độ bằng chứng tối thiểu (Evidence Floor).** `[unit-test | fixture-replay | live-run | production]` kèm dấu vân tay cây thư mục `WTREE_FINGERPRINT` ở trạng thái `FRESH`.

## 5. Reuse Ladder & Constraints (Bậc thang tái sử dụng và Ràng buộc)

- **Tái sử dụng.** [Chỉ rõ các hàm tiện ích, component hoặc thư viện có sẵn trong dự án phải tái sử dụng]
- **Ràng buộc thư viện ngoài.** [Không cài thêm gói mới | Chỉ được dùng các gói đã duyệt]
- **Shortcut được phép (nếu có).** [Ghi mã quyết định `D<N>` có `Completeness <= 7/10` đã được Chủ nhà chấp thuận kèm nhãn `vibecode-shortcut(D<N>)` cần gắn vào code]

## 6. Failure Protocol & 3-Strike Escalation (Giao thức dừng khi lỗi)

- Nếu bất kỳ lệnh kiểm chứng nào ở Mục 4 thất bại, Thợ phải đọc kỹ đầu ra lỗi để tìm nguyên nhân gốc rễ trước khi sửa.
- **Quy tắc 3-Strike.** Nếu cùng một lỗi kiểm chứng vẫn thất bại sau 3 lần thử sửa liên tiếp, hoặc phát hiện mâu thuẫn trong Blueprint/Contract dùng chung, Thợ phải **DỪNG NGAY LẬP TỨC**, giữ nguyên hiện trường và gửi nguyên văn câu lệnh cùng toàn bộ log lỗi về cho Chủ thầu / Quân sư Kongming. Tuyệt đối không tự ý sửa đổi bài kiểm thử hoặc hạ tiêu chuẩn nghiệm thu để làm xanh giả tạo.
