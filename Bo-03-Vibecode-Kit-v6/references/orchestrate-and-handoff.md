# Giao thức Điều phối Đa Thợ, Cố vấn Kongming, Trọng tài Độc lập và Handoff An toàn

Tài liệu này hướng dẫn cách tổ chức thi công khi dự án có nhiều gói công việc (`TIP`), kéo dài qua nhiều phiên làm việc hoặc phối hợp nhiều công cụ AI khác nhau (Claude, Antigravity, Codex, Cursor), được chắt lọc từ **`ak-orchestrate` v2.0**, **`ak-vibe` v1.5** và **`ak-handoff` v2.1**.

## 1. Điều phối Đa Thợ Song song (Multi-Builder Orchestration)

Khi Đồ thị Gói Công việc (`Task Graph` ở Bước 5) có từ hai gói `TIP` trở lên không phụ thuộc lẫn nhau và có thể giao cho nhiều phiên Thợ chạy cùng lúc, Chủ thầu bắt buộc áp dụng ba quy tắc bảo vệ.

### Quy tắc 1 · Đóng băng Hợp đồng Chung trước khi Phân luồng (Contracts Up Front)
Mọi cấu trúc dữ liệu, giao diện hàm (interface), bảng cơ sở dữ liệu hoặc file cấu hình mà nhiều Thợ cùng cần sử dụng phải được hoàn thành và đóng băng ở một gói `TIP` nền tảng chạy trước. Các Thợ chạy song song ở giai đoạn sau chỉ được phép đọc (`Read-only`) các file hợp đồng này.

### Quy tắc 2 · Sở hữu File Rời nhau Tuyệt đối (Disjoint File Ownership)
Hai Thợ chạy đồng thời không bao giờ được phép có quyền ghi vào cùng một file. Chủ thầu phải liệt kê tường minh danh sách đường dẫn được phép ghi (`Allowed write paths`) trong từng `TIP` và kiểm tra giao thoa bằng không trước khi phát lệnh thi công.

### Quy tắc 3 · Cô lập bằng Không gian Git Worktree (Worktree Isolation)
Ngay cả khi hai Thợ sửa hai thư mục khác nhau, việc chạy chung trên một cây thư mục vẫn gây xung đột bộ nhớ đệm biên dịch, file tạm hoặc làm nhiễu lệnh `git status`. Do đó, mỗi Thợ chạy song song phải được cấp một nhánh và một thư mục `git worktree` riêng biệt.

```bash
# Tạo worktree riêng cho từng gói TIP từ commit nền đã đóng băng hợp đồng
git worktree add -b feat/tip-002 .worktrees/tip-002 HEAD
git worktree add -b feat/tip-003 .worktrees/tip-003 HEAD
```

Khi một Thợ gặp lỗi thất bại, giữ nguyên worktree đó để Chủ thầu khám nghiệm hiện trường, tuyệt đối không xóa dấu vết lỗi.

## 2. Giám sát Cố vấn Kongming (`--advice`) và Giao thức Dừng 3-Strike

Trong các dự án mức **R2** và **R3**, hoặc khi sử dụng các mô hình Thợ chuyên tốc độ cao, việc để Thợ tự xoay xở khi gặp lỗi phức tạp thường dẫn đến hiện tượng "xoắn ốc suy thoái" (sửa mò làm hỏng các tính năng khác hoặc xóa bớt bài kiểm thử để vượt qua cổng).

Lớp **Cố vấn Kongming (Quân sư độc lập chạy trên mô hình có năng lực suy luận cao nhất)** tham gia tại 5 điểm chốt.
1. **Sau khi hoàn thành khảo sát và chẩn đoán (Bước 1 & 2).** Xác nhận nguyên nhân gốc rễ và phạm vi trước khi lập kế hoạch.
2. **Sau khi hoàn thành dự thảo Blueprint (Bước 4).** Đánh giá tính khả thi, điểm mù kiến trúc và rủi ro lớn nhất cần canh chừng.
3. **Khi Thợ chạm ngưỡng dừng 3-Strike hoặc gặp lỗi kiểm chứng (Bước 6).** Khi bất kỳ lệnh kiểm chứng nào thất bại mà nguyên nhân không hiển nhiên, hoặc sau 3 lần thử sửa liên tiếp vẫn đỏ, Thợ phải dừng ngay lập tức. Chủ thầu chuyển nguyên văn câu lệnh, log lỗi và các phương án đã thử sang Quân sư Kongming để lấy phán xét trước khi cho phép chạm lại vào code.
4. **Trước các quyết định cửa một chiều.** Thay đổi cấu trúc cơ sở dữ liệu, chính sách bảo mật hoặc hợp nhất nhánh lớn.
5. **Sau khi qua cổng Verify và trước khi nâng lên nhánh Stable (Bước 7 & 8).** Đánh giá tổng thể lần cuối và đề xuất các bước theo dõi sau phát hành.

Nguyên tắc cốt lõi là Quân sư Kongming chỉ đưa ra phán xét chiến lược và chỉ dẫn gỡ rối, tuyệt đối không trực tiếp sửa code thay Thợ.

## 3. Trọng tài Độc lập Chấm chéo (Independent Arbiter Pass · C3 Route)

Một phiên AI vừa bỏ công viết 500 dòng code sẽ luôn có xu hướng nhìn nhận sản phẩm của mình một cách lạc quan khi tự kiểm tra. Vì vậy, ở Bước 7 (`VERIFY`) của các tác vụ quan trọng, Chủ thầu khởi tạo một phiên **Trọng tài Độc lập (Arbiter)** theo các tiêu chuẩn sau.

- **Ngữ cảnh mới tinh (Fresh Context).** Phiên Trọng tài chỉ nhận vào bản vẽ `Blueprint`, gói yêu cầu `TIP`, báo cáo `Completion Report` và quyền truy cập kho mã nguồn hiện tại. Không nạp lịch sử hội thoại nháp của Thợ để tránh lây nhiễm định kiến.
- **Độc lập Họ Mô hình khi có thể (Cross-Model Independence).** Nếu Thợ thi công là họ mô hình A (ví dụ Claude), ưu tiên chọn Trọng tài hoặc công cụ phản biện từ họ mô hình B (ví dụ GPT/Codex) hoặc một phiên độc lập hoàn toàn.
- **Bảng kiểm của Trọng tài (Arbiter Checklist).**
  1. Mã `WTREE_FINGERPRINT` trong báo cáo có khớp tuyệt đối với trạng thái thực tế của cây thư mục hiện tại không?
  2. Các file bị thay đổi có nằm gọn trong `Scope Freeze` của TIP không?
  3. Chạy lại các lệnh `Verify command` trong TIP có thực sự trả về mã thoát `0` với cấp độ bằng chứng đạt chuẩn không?
  4. Có bài kiểm thử nào bị làm yếu đi, bị bỏ qua (`skip`) hoặc chỉ kiểm tra giả tạo không?
  5. Mọi yêu cầu `REQ-ID` được giao cho TIP này đã được giải quyết trọn vẹn chưa?

Chỉ khi Trọng tài kết luận **`PASS`** trên cả 5 câu hỏi, nhánh của Thợ mới được phép hợp nhất vào nhánh chính.

## 4. Hợp đồng Bàn giao Chuyển tiếp có Che mật khẩu (Redacted Handoff Contract)

Khi cần chuyển giao công việc giữa hai phiên làm việc (do hết giới hạn ngữ cảnh, hết ca làm việc hoặc chuyển từ môi trường lập kế hoạch sang môi trường thi công), tuyệt đối không dán toàn bộ lịch sử trò chuyện dài dòng. Hãy xuất một file **Handoff Contract** theo đúng bản mẫu `templates/Handoff-Contract.md`.

### Quy tắc Che mật khẩu Bắt buộc (Mandatory Redaction)
Trước khi ghi file Handoff hoặc chia sẻ nhật ký kiểm thử, phải quét và thay thế mọi chuỗi nhạy cảm bằng nhãn `[REDACTED:loại-khóa]`.
- Các khóa API, chuỗi Bearer Token, JWT, cookie phiên đăng nhập → `[REDACTED:token]`
- Khóa riêng tư PEM, SSH private key → `[REDACTED:private-key]`
- Giá trị biến môi trường nhạy cảm trong `.env` (`PASSWORD`, `SECRET`, `KEY`, `DATABASE_URL`) → `[REDACTED:env-secret]`
- Đường dẫn máy chủ nội bộ hoặc URL có gắn chữ ký truy cập tạm thời → `[REDACTED:signed-url]`

### Nguyên tắc Bước An toàn Đầu tiên (`First safe step`)
Mục số 8 (`Exact next actions`) của mọi bản Handoff phải mở đầu bằng một bước kiểm tra an toàn, chỉ đọc (`**First safe step.**`), giúp phiên AI tiếp nhận tự đối chiếu trạng thái nhánh, mã commit và kết quả chạy test hiện tại trước khi viết dòng code tiếp theo.
