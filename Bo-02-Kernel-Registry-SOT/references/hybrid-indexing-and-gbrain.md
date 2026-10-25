# Giao thức Chỉ mục Phụ thuộc Phân tầng (`CSV` · `ak-graphify` · `gstack /sync-gbrain`)

Tài liệu này hướng dẫn cách vận hành hệ thống chỉ mục phụ thuộc của Bộ 02 v2.0 theo nguyên tắc **Đơn giản trước, Mở rộng khi có bằng chứng quy mô (`Tiered Scaling`)**, tích hợp tinh hoa từ `ak-graphify` v1.0.1 và `gstack /setup-gbrain` + `/sync-gbrain`.

## 1. Bảng Quyết định Chọn Tầng Chỉ mục (`Tiered Indexing Matrix`)

| Quy mô kho tri thức | Tầng chỉ mục sử dụng | Công cụ vận hành | Lý do kỹ thuật |
|---|---|---|---|
| **Tầng 1 · Nhỏ và Vừa** (`< 500` thành phần trong `manifest.csv`) | Chỉ dùng `dependency-index.csv` thuần túy | `ripgrep` (`rg`), `git grep` hoặc script Python 20 dòng | Không tốn chi phí dựng đồ thị, dễ đọc bằng mắt thường, kiểm soát 100% qua Git diff |
| **Tầng 2 · Lớn hoặc Đa phương thức** (`>= 500` thành phần, hoặc kết hợp kho tài liệu với kho mã nguồn 20 ngôn ngữ) | `dependency-index.csv` + Đồ thị `ak-graphify` (`graphify-out/graph.json`) | `graphify .` (cập nhật gia tăng qua bộ đệm SHA-256) và MCP `query_graph`, `get_neighbors`, `shortest_path` | Tự động phát hiện các "nút thần" (`god nodes` được nhiều nơi phụ thuộc nhất) và truy vết chuỗi phụ thuộc nhiều bậc |
| **Tầng 3 · Đa dự án & Bộ nhớ Phiên làm việc** (Cần tìm kiếm ngữ nghĩa xuyên suốt tài liệu, code và lịch sử quyết định) | `dependency-index.csv` + `gstack /sync-gbrain` (PGLite nội bộ hoặc Supabase) | `/setup-gbrain` và `/sync-gbrain --incremental` kèm `--audit` | Tìm kiếm kết hợp ký hiệu mã nguồn và tri thức dự án trong ~50ms với cơ chế bảo vệ quyền riêng tư chặt chẽ |

## 2. Chuẩn hóa Nhãn Xuất xứ Quan hệ (`Provenance Tagging` từ `ak-graphify`)

Dù ở Tầng 1 (`dependency-index.csv`) hay Tầng 2 (`ak-graphify`), mọi cạnh liên kết `from_id -> to_id` đều phải gắn một trong ba nhãn xuất xứ (`provenance_tag`).

1. **`EXTRACTED` (Trích xuất cứng).** Quan hệ được khai báo tường minh trong trường `formula.inputs` của `L2`, mục con trỏ của `SKILL.md`, hoặc cây cú pháp `AST` của mã nguồn. Độ tin cậy 100%.
2. **`INFERRED` (Suy luận ngữ nghĩa).** Quan hệ do AI Agent phát hiện khi đọc nội dung tài liệu ở Phase 2 và Phase 3 (ví dụ một quy trình bán hàng nhắc tới tên một thông tư nhưng chưa gắn mã `OBL-*`). Cần được chuyển hóa dần thành `EXTRACTED` ở Phase 5.
3. **`AMBIGUOUS` (Mơ hồ / Cần xác nhận).** Quan hệ không chắc chắn, bắt buộc đẩy vào hàng đợi quyết định để con người xác nhận trước khi dùng làm căn cứ kiểm toán.

## 3. Quy tắc An toàn & Bảo mật khi Đồng bộ Bộ nhớ (`GBrain Trust & Privacy Gate`)

Khi dự án ở Tầng 3 kích hoạt `/sync-gbrain` để nạp `Kernel Registry` và mã nguồn vào bộ nhớ tìm kiếm của Agent, bắt buộc tuân thủ 3 hàng rào bảo mật.

1. **Cổng Chính sách Tin cậy (`Brain Trust Policy Gate`).**
   - Kiểm tra chính sách của kho (`gstack-gbrain-repo-policy get`). Nếu kho chứa dữ liệu mật được cấu hình `deny`, dừng ngay lập tức và không đồng bộ.
   - Phân biệt rõ chế độ máy trạm cá nhân (`personal` trên PGLite nội bộ) và chế độ dùng chung (`shared` qua máy chủ từ xa).
2. **Không Lưu Trùng lặp (`No Double-Store`) và Không Trộn `L4` vào Kiểm chứng `L1`.**
   - Khi nạp vào bộ nhớ tìm kiếm, giữ nguyên nhãn phân lớp `L1`, `L2`, `L3`, `L4` trong metadata của từng tài liệu để khi truy vấn, Agent vẫn phân biệt được đâu là số liệu cứng `L1` và đâu là văn phong `L4`.
3. **Kiểm toán Rò rỉ Dữ liệu Nhạy cảm (`/sync-gbrain --audit`).**
   - Chạy chế độ kiểm toán chỉ đọc (`--audit`) để rà soát danh sách các trang đã lập chỉ mục và đảm bảo không có khóa bí mật, mật khẩu hay thông tin cá nhân ngoài danh sách cho phép bị lưu vào bộ nhớ đệm.
