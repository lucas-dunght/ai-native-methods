# RRI-NNN · Biên bản Phỏng vấn Ngược và Phân loại Quyết định

**Date.** YYYY-MM-DD
**Linked Scan.** SCAN-NNN
**Risk tier.** R[1|2|3]
**Contractor.** [Tên phiên Chủ thầu]
**Homeowner.** [Tên Chủ nhà / Người ra quyết định]

## 1. Các câu hỏi đã tự giải từ Bước SCAN (Auto-Answered from Codebase)

Chủ thầu đã đọc `SCAN-NNN` và tự trả lời các điểm sau mà không cần làm phiền Chủ nhà.

| STT | Góc nhìn (Persona) | Câu hỏi đặt ra | Câu trả lời rút từ mã nguồn / hiện trạng | Nhãn nhận định |
|---|---|---|---|---|
| 1 | Developer | Dự án dùng cơ chế xác thực và quản lý gói nào? | [Câu trả lời kèm đường dẫn file] | `OBSERVED` |
| 2 | QA / Tester | Đã có sẵn khung chạy kiểm thử tự động chưa? | [Câu trả lời kèm lệnh chạy] | `OBSERVED` |
| 3 | Operator | Cấu hình môi trường đang lưu ở đâu? | [Câu trả lời] | `DERIVED` |

## 2. Quyết định Tầng 1 · Mechanical (Chủ thầu tự quyết định ngầm)

Các quyết định kỹ thuật chỉ có một phương án đúng đắn hiển nhiên theo tiêu chuẩn ngành và quy ước sẵn có của kho mã nguồn.

| Mã số | Góc nhìn | Vấn đề kỹ thuật | Quyết định của Chủ thầu | Lý do |
|---|---|---|---|---|
| M01 | Developer | Kiểm tra đầu vào của hàm API | Bắt buộc xác thực schema đầu vào trước khi gọi tầng nghiệp vụ | Chống dữ liệu bẩn làm sập hệ thống |
| M02 | Operator | Lưu trữ khóa bí mật | Đọc qua biến môi trường, tuyệt đối không ghi cứng trong code | Nguyên tắc an toàn cơ bản |

## 3. Quyết định Tầng 2 · Taste (Đánh đổi cân bằng · Đề xuất gói mặc định)

Các quyết định có từ hai phương án khả thi trở lên với ưu nhược điểm tương đương. Chủ thầu chọn sẵn phương án khuyến nghị `(recommended)` để Chủ nhà duyệt nhanh hoặc đổi nếu muốn.

| Mã số | Góc nhìn | Chế độ hỏi | Câu hỏi và Phương án Khuyến nghị `(recommended)` | Điểm Completeness | Phản hồi của Chủ nhà |
|---|---|---|---|---|---|
| T01 | End User | CHALLENGE | Hiển thị thông báo lỗi ngay dưới từng ô nhập liệu thay vì hộp thoại bật lên `(recommended)` | 9/10 | `[Đồng ý / Đổi sang...]` |
| T02 | Business Analyst | GUIDED | Xuất báo cáo mặc định ở định dạng CSV UTF-8 có BOM để mở trực tiếp trên Excel tiếng Việt `(recommended)` | 10/10 | `[Đồng ý / Đổi sang...]` |

## 4. Quyết định Tầng 3 · User Challenge (Thẻ Quyết định Chiến lược `D<N>`)

Các quyết định cửa một chiều, ảnh hưởng trực tiếp tới phạm vi sản phẩm, chi phí, bảo mật hoặc kiến trúc cốt lõi. Chủ nhà bắt buộc chọn rõ từng thẻ.

### D01 · [Tiêu đề quyết định chiến lược số 1]
- **Góc nhìn đại diện.** [End User | Business Analyst | QA/Tester | Developer | Operator]
- **Chế độ hỏi.** [CHALLENGE | GUIDED | EXPLORE]
- **Giải thích nhanh (ELI10).** [2 đến 3 câu giải thích bản chất vấn đề bằng ngôn ngữ đời thường, không lạm dụng thuật ngữ]
- **Rủi ro nếu chọn sai (Stakes).** [Chuyện gì sẽ xảy ra cho người dùng hoặc doanh nghiệp nếu chọn sai hướng này]
- **Khuyến nghị của Chủ thầu.** Chọn Phương án A vì `[lý do ngắn gọn, thực tế]`.
- **Độ hoàn thiện (Completeness).** A = 10/10 · B = 7/10 · C = 4/10
- **Ước lượng công sức (Dual-scale effort).** A (Thủ công X ngày / AI Builder Y phút) · B (Thủ công X giờ / AI Builder Y phút)

**Phương án A · [Tên phương án đầy đủ] (recommended)**
- Ưu điểm 1. [Lợi ích cụ thể, quan sát được]
- Ưu điểm 2. [Lợi ích cụ thể, quan sát được]
- Nhược điểm. [Chi phí hoặc độ phức tạp phải chấp nhận]

**Phương án B · [Tên phương án rút gọn / làm tắt có kiểm soát]**
- Ưu điểm 1. [Ra mắt nhanh, ít thay đổi]
- Ưu điểm 2. [Đơn giản hóa việc triển khai bước đầu]
- Nhược điểm. [Giới hạn nào chưa được xử lý, khi nào sẽ bộc lộ hạn chế]

**Tổng kết đánh đổi (Net).** [Một câu tóm tắt bản chất cuộc đánh đổi này]
**Lựa chọn của Chủ nhà.** `[Phương án A | Phương án B | Ý kiến khác]`
**Điều kiện nâng cấp nếu chọn phương án `Completeness <= 7/10` (Shortcut Trigger).** `[Ghi rõ khi nào phải nâng cấp lên 10/10]`

---

## 5. Ma trận Yêu cầu Đầu ra (Requirements Matrix · REQ-IDs)

Tổng hợp toàn bộ yêu cầu đã chốt sau phiên phỏng vấn ngược để đưa vào Blueprint.

| Mã REQ-ID | Nhóm Persona | Mô tả yêu cầu cụ thể | Mức ưu tiên (P0/P1/P2) | Nguồn quyết định (`SCAN` / `M` / `T` / `D`) | Tiêu chí kiểm chứng sơ bộ |
|---|---|---|---|---|---|
| REQ-01 | End User | [Mô tả yêu cầu] | P0 | D01 | [Cách kiểm tra] |
| REQ-02 | Business Analyst | [Mô tả yêu cầu] | P0 | T02 | [Cách kiểm tra] |
| REQ-03 | QA / Tester | [Mô tả yêu cầu] | P1 | M01 | [Cách kiểm tra] |
| REQ-04 | Operator | [Mô tả yêu cầu] | P1 | SCAN | [Cách kiểm tra] |

## 6. Câu hỏi Mở còn Tồn đọng (Open Questions & Blockers)

[Liệt kê những điểm chưa thể chốt ngay và người chịu trách nhiệm phản hồi trước khi khóa Blueprint. Ghi Không còn câu hỏi mở nếu đã giải quyết 100%.]
