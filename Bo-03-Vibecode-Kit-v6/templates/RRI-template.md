# Biên Bản Khử Mơ Hồ, `Indirect Prompting` & Bảng Quyết Định (`RRI & Decision Brief · v6.2 × pstack`)

- **Mã Tác vụ:** `[TASK-ID]`
- **Cấp độ Rủi ro (`Risk Tier`):** `[R0 / R1 / R2 / R3]`
- **Điểm RRI hiện tại:** `[X.X / 10.0]` (`Ngưỡng mở khóa: >= 8.5/10`)
- **Trạng thái:** `[PENDING_USER_APPROVAL / APPROVED]`

---

## 1. Bản Diễn Đạt Lại Bằng Lời Tự Nhiên (`Indirect Prompting Restate`)

> *"Restate in your own words and in plain English"* · Nén nguồn thông tin nhiễu thành bài toán có cấu trúc để Chủ nhà bắt lỗi hiểu sai ngay trước khi viết bất kỳ dòng code nào:

- **Hiện trạng đang chạy (`What is happening now`):** `[Mô tả ngắn gọn cơ chế hiện tại kèm nhãn OBSERVED: file:line]`.
- **Điểm gãy / Nhu cầu thật (`What is the real gap`):** `[Diễn đạt bản chất bài toán bằng ngôn ngữ tự nhiên, tách khỏi giải pháp gợi ý ban đầu]`.
- **Ranh giới bất biến (`What must stay intact`):** `[Các luồng dữ liệu và hợp đồng API không được phép làm gãy]`.

---

## 2. Mô Hình Nhận Thức Hai Chiều (`/teach = /how + /why + /recall`)

- **Tra cứu `Feature Map` (`references/features/README.md`):** `[Mã tính năng liên quan + lệnh ./bin/control-app chạm tới màn hình/API đó]`.
- **Cơ chế Runtime hiện tại (`/how`):** `[OBSERVED: path/to/file:line]` · `[Tóm tắt luồng gọi hàm thực tế tại runtime]`.
- **Nguyên nhân Lịch sử & Ý đồ Thiết kế (`/why`):** `[OBSERVED: git log / PR # / ticket]` · `[Tại sao đoạn code hiện tại lại được viết như vậy, có chốt chặn an toàn ẩn nào cần giữ không]`.
- **Chứng minh Thực nghiệm (`/teach`):** `[Giải thích trực quan vì sao hướng tiếp cận mới tốt hơn hiện trạng dựa trên dữ liệu/code thật]`.
- **Ngữ cảnh Phiên trước (`/recall`):** `[Tóm tắt quyết định từ lịch sử hội thoại cũ hoặc ghi N/A nếu là phiên mới]`.

---

## 3. Bảng Chấm Điểm Sẵn Sàng Yêu Cầu (`RRI Breakdown`)

| Trụ cột đánh giá | Điểm (`0.0 - 2.0`) | Hiện trạng & Bằng chứng |
|---|---|---|
| 1. Mục tiêu & Bản `Indirect Prompting Restate` | `[2.0 / 2.0]` | `[Đã rõ / Còn mơ hồ ở điểm X]` |
| 2. Ngữ cảnh Runtime (`/how`) & Lịch sử (`/why`) | `[2.0 / 2.0]` | `[Đã truy vết đủ git blame & luồng gọi hàm]` |
| 3. Trường hợp biên & Xử lý lỗi (`Edge Cases`) | `[1.5 / 2.0]` | `[Cần chốt câu hỏi D1]` |
| 4. Ràng buộc Bảo mật & Hiệu năng (`NFRs`) | `[2.0 / 2.0]` | `[Đã chốt ngưỡng độ trễ & phân quyền]` |
| 5. Đòn bẩy Kiểm chứng (`./bin/control-app Lever`) | `[2.0 / 2.0]` | `[Đã xác định lệnh ./bin/control-app kiểm chứng sống]` |
| **TỔNG ĐIỂM RRI** | **`[9.5 / 10.0]`** | **Đạt chuẩn mở khóa Bước 3 (`VISION`) khi `>= 8.5`** |

---

## 4. Bảng Quyết Định Chuẩn Hóa (`Decision Ledger & D<N> Briefs`)

| Mã Quyết định | Hạng mục & Bằng chứng (`file:line`) | Hiện trạng | Phương án Đề xuất | Trạng thái | Phê duyệt của Chủ nhà |
|---|---|---|---|---|---|
| `D1` | `[Tên hạng mục] (src/file.ts:20)` | `[Chưa có]` | `Phương án A (10/10)` | `approved / unresolved` | `[Chờ chọn A/B/C]` |

### Chi tiết Quyết định `D1`: `[Tiêu đề Quyết định]`
- **Giải thích đơn giản (`ELI10`):** `[Giải thích trong 2 câu bằng ngôn ngữ đời thường cho người không chuyên cũng hiểu ngay]`.
- **Rủi ro nếu chọn sai (`Stakes`):** `[Điều gì sẽ xảy ra trong thực tế nếu chọn phương án kém hơn]`.
- **Khuyến nghị (`Recommendation`):** Chọn **Phương án A** theo nguyên tắc *"Boil the Lake"* vì đạt độ hoàn thiện `10/10` mà chỉ tốn thêm vài phút thực thi của AI.

```text
Cam kết thực hiện                        | Hiện tại | A (Recommended) | B (Rút gọn) | C (Bỏ qua)
-----------------------------------------+----------+-----------------+-------------+-----------
Xử lý trọn vẹn luồng chính & trường hợp biên | Không    | Có (10/10)      | Một phần    | Không
Không để lại nợ kỹ thuật (Shortcut Debt) | Không    | Có (0 nợ)       | Nợ Type-2   | Nợ Type-1
```

- **A) `(Recommended)` `[Tên Phương án A · Completeness: 10/10 · Shortcut Debt: None]`**
  - Nỗ lực: `S (Con người: ~2 giờ / AI: ~5 phút)` · Rủi ro: `Thấp`
  - Ưu điểm: Giải quyết triệt để gốc rễ bài toán, không phát sinh nợ kỹ thuật.
  - Nhược điểm: Cần sửa thêm `[1-2]` tệp kiểm thử.
- **B) `[Tên Phương án B · Completeness: 7/10 · Shortcut Debt: Type-2 Deferred Edge Case]`**
  - Nỗ lực: `S (Con người: ~30 phút / AI: ~2 phút)` · Rủi ro: `Trung bình`
  - Ưu điểm: Chạy nhanh cho trường hợp phổ biến nhất.
  - Nhược điểm: Phải ghi nợ trường hợp biên vào `TODOS.md`.
- **C) `[Tên Phương án C · Không làm gì / Giữ nguyên]`**
  - Nỗ lực: `0` · Rủi ro: `Cao`
