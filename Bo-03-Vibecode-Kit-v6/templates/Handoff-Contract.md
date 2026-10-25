# HO-NNN · Hợp đồng Bàn giao Chuyển tiếp Phiên làm việc (Redacted Handoff Contract)

**Handoff-version.** 1
**Date captured.** YYYY-MM-DD HH:mm
**Linked TIP / Blueprint.** TIP-NNN / BP-NNN
**From Agent / Session.** [Phiên bàn giao · Vai trò · Model]
**To Agent / Session.** [Phiên tiếp nhận · Vai trò · Model]

> **Hướng dẫn cho Agent tiếp nhận.** Đọc toàn bộ 9 mục dưới đây và đối chiếu mục `## 3. Current state` với kho mã nguồn thực tế trước khi thực hiện bất kỳ thao tác ghi nào. Bắt đầu chính xác từ dòng được đánh dấu `**First safe step.**` ở mục 8.

## 1. Mission and current status

- **Mục tiêu cuối cùng của tác vụ.** [Mô tả rõ kết quả cần đạt của gói công việc]
- **Phần việc đã hoàn thành.** [Những hạng mục đã làm xong và đã kiểm chứng]
- **Phần việc còn lại.** [Những hạng mục cần phiên tiếp nhận hoàn thành nốt]
- **Mức độ ưu tiên / Hạn chót.** [P0 / P1 / P2]

## 2. Scope and guardrails

- **Thư mục gốc làm việc (Workspace root).** `[Đường dẫn tuyệt đối hoặc tương đối trong repo]`
- **Các đường dẫn được phép sửa (Scope Freeze).**
  - `src/...`
  - `tests/...`
- **Các đường dẫn và hành động bị cấm.**
  - Không sửa các file hợp đồng dùng chung ngoài danh sách trên.
  - Không tự ý chạy lệnh triển khai (`deploy`) hoặc đẩy cưỡng bức (`git push --force`).
  - Không đưa khóa bí mật hoặc dữ liệu nhạy cảm vào mã nguồn và nhật ký.

## 3. Current state

Kết quả thu thập trực tiếp từ kho mã nguồn tại thời điểm tạo bản bàn giao (`OBSERVED`).

- **Git repository root.** `[Kết quả từ git rev-parse --show-toplevel]`
- **Current branch.** `[Kết quả từ git rev-parse --abbrev-ref HEAD]`
- **HEAD commit.** `[Kết quả từ git rev-parse HEAD]`
- **Working-tree fingerprint (`WTREE_FINGERPRINT`).** `[Mã băm 16 ký tự hiện tại]`
- **Trạng thái các file đang thay đổi (`git status --short`).**
```text
[Danh sách file đang sửa đổi hoặc chưa theo dõi, đã qua bộ lọc che mật khẩu]
```
- **Các thay đổi cục bộ trên đĩa có chủ đích hay không?** `[Có, đang làm dở phần X | Không, cây thư mục sạch]`

## 4. Decisions and rationale

- **Quyết định 1.** [Nội dung quyết định và lý do chọn, dẫn chiếu mã `D<N>` hoặc `BP-NNN`]
- **Phương án đã loại bỏ.** [Phương án nào đã thử hoặc đã cân nhắc nhưng loại bỏ để phiên sau không đi lại vào ngõ cụt]

## 5. Work performed

Tóm tắt các bước thực thi và câu lệnh quan trọng đã chạy (mọi thông tin nhạy cảm đã được thay bằng nhãn `[REDACTED:loại-khóa]`).

- Đã tạo/sửa `[tên file]` để xử lý `[mô tả ngắn]`.
- Đã chạy lệnh `[câu lệnh]` và thu được kết quả `[tóm tắt kết quả đã che secret]`.

## 6. Verification

- **Các bài kiểm tra đã chạy và đạt (`PASS`).**
  - `[Lệnh 1]` → Đạt (cấp bằng chứng `unit-test`).
- **Các bài kiểm tra đang lỗi hoặc chưa chạy (`FAIL` / `NOT RUN`).**
  - `[Lệnh 2]` → Chưa chạy vì `[lý do cụ thể]`.

## 7. Open risks and blockers

- **Rủi ro / Câu hỏi mở.** [Mô tả điểm nghẽn kỹ thuật hoặc câu hỏi cần Chủ thầu/Chủ nhà xác nhận nếu có, hoặc ghi `Not captured in this session`]

## 8. Exact next actions

Danh sách các bước hành động cụ thể theo đúng thứ tự thực hiện cho phiên tiếp nhận.

1. **First safe step.** Chạy lệnh `git status --short` và `[lệnh kiểm tra hiện trạng]` để xác nhận môi trường khớp với Mục 3 trước khi viết thêm code.
2. Hoàn thiện hàm/module `[tên cụ thể]` tại file `[đường dẫn:dòng]`.
3. Chạy lệnh kiểm chứng `[verify command]` cho tới khi toàn bộ tiêu chí AC trong `TIP-NNN` chuyển sang xanh.
4. Chụp lại mã `WTREE_FINGERPRINT` mới và xuất file `vibecode-artifacts/completion-reports/CR-NNN.md`.

## 9. Source pointers

- **Gói công việc hiện tại.** `vibecode-artifacts/TIP/TIP-NNN.md`
- **Bản vẽ kiến trúc.** `vibecode-artifacts/blueprints/BP-NNN.md`
- **Các file mã nguồn trọng tâm.**
  - `src/[file-1]`
  - `tests/[file-test-1]`
