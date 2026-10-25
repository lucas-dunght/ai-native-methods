# Giải Thích Kiến Trúc · Bộ Định Tuyến Đa Tín Hiệu & Cơ Chế Xoay Vòng Khóa An Toàn (`2026.10`)

Khi vận hành một hệ thống nghiên cứu và phát triển phần mềm có sự tham gia của nhiều AI Agent (như **Bộ 01 · Tinh Lọc Thông Tin Internet**), việc gọi trực tiếp một dịch vụ tìm kiếm đơn lẻ với một khóa API duy nhất nhanh chóng gặp ba điểm nghẽn lớn gồm cạn hạn mức miễn phí giữa chừng, định tuyến sai loại công cụ tìm kiếm và nguy cơ rò rỉ khóa API ra ổ cứng hoặc lên kho mã nguồn Git. Tài liệu này giải thích lý do thiết kế máy chủ proxy cục bộ `Unified Search Pool v2.0` (`search_pool.py`) cùng cơ chế bảo vệ khóa trong `tools/`.

---

## 1. Vấn Đề Cốt Lõi Khi Dùng Công Cụ Tìm Kiếm Đơn Lẻ

Trong thực tế triển khai các dự án nghiên cứu đa nguồn, ba chế độ lỗi sau đây thường xuyên xảy ra nếu không có lớp điều phối trung gian:

1. **Bẫy từ khóa đơn lẻ (`Keyword Hijacking`).** Một bộ phân loại ngây thơ dựa trên từ khóa đơn lẻ sẽ thấy chữ *"công ty"* hoặc *"doanh nghiệp"* trong câu hỏi *"Quy định mức đóng BHXH bắt buộc của công ty năm 2026"* và đẩy truy vấn sang kho hồ sơ Startup (`Exa category="company"`). Kết quả trả về toàn hồ sơ gọi vốn tiếng Anh thay vì văn bản pháp luật Việt Nam.
2. **Đốt cháy hạn mức (`Quota Exhaustion`) khi gặp truy vấn rỗng.** Khi một truy vấn chuyên ngành hẹp trả về `0` kết quả trên khóa số 1 của nhà cung cấp A, một vòng lặp thử lại đơn giản sẽ tiếp tục gọi khóa số 2, số 3... đến hết 6 khóa của cùng nhà cung cấp A (vẫn trả về `0` kết quả) và làm tốn 6 lượt gọi vô ích trước khi chịu chuyển sang nhà cung cấp B.
3. **Lộ khóa API thô trong file trạng thái dùng chung.** Khi nhiều tiến trình AI Agent chạy song song cần chia sẻ danh sách khóa đang bị giới hạn tốc độ (`HTTP 429`) qua một file JSON trong `/tmp/`, việc dùng chính chuỗi API Key làm khóa từ điển (`dict key`) trong file JSON sẽ làm lộ toàn bộ khóa bí mật dưới dạng văn bản thuần trên ổ đĩa.

---

## 2. Phương Án Thiết Kế Trong `Unified Search Pool v2.0`

### 2.1. Sơ Đồ Luồng Xử Lý Tổng Thể

```text
Truy vấn từ AI Agent -> web_search(query, mode, provider)
                             │
                             ▼
               ┌───────────────────────────┐
               │ 1. TTLCache (300s, 128)   │──(Trúng đích)──► Trả kết quả ngay (0 tốn credit)
               └─────────────┬─────────────┘
                             │ (Chưa có trong cache)
                             ▼
               ┌───────────────────────────┐
               │ 2. QueryRouter Đa Tín Hiệu│
               │ - Chấm điểm 6 nhóm Regex  │
               │ - Quy tắc Anti-Hijacking  │
               └─────────────┬─────────────┘
                             │ Xác định thứ tự: [Provider #1, Provider #2, Provider #3]
                             ▼
               ┌───────────────────────────┐
               │ 3. Vòng lặp Provider & Key│
               │ - Xoay con trỏ Round-Robin│
               │ - Bỏ qua key đang Cooldown│
               └─────────────┬─────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   [HTTP 200 có dữ liệu] [HTTP 204 Rỗng]   [HTTP 401/429/5xx]
   Ghi nhận OK, lưu      KHÔNG phạt key,   Phạt key theo tầng
   cache & trả về        nhảy ngay sang    (3600s / 60s / 30s),
                         Provider kế tiếp  thử key kế tiếp cùng Provider
```

### 2.2. Chấm Điểm Đa Tín Hiệu Có Trọng Số & Chống Bắt Nhầm (`Anti-Hijacking`)

Thay vì khớp lệnh `if/else` tuần tự, lớp `QueryRouter` (`search_pool.py:453-483`) đếm số lượng từ khóa khớp trên cả 6 nhóm tín hiệu và nhân với trọng số ưu tiên:
- `legal` (`× 4.0`): Văn bản luật, nghị định, thông tư, thuế, BHXH Việt Nam.
- `academic` (`× 3.5`): Bài báo khoa học, arXiv, luận án, hội thảo IEEE/ACM/NeurIPS.
- `deep` (`× 3.2`): Phân tích toàn diện, báo cáo tổng hợp chuyên sâu.
- `code` (`× 3.0`): Mã nguồn, GitHub, SDK, lỗi `traceback`.
- `news` (`× 2.5`) và `company` (`× 2.5`): Tin tức thời sự và hồ sơ doanh nghiệp.

Đặc biệt, hai quy tắc `Anti-Hijacking` (`search_pool.py:472-480`) triệt tiêu hoàn toàn hiện tượng bắt nhầm:
- Khi xuất hiện bất kỳ tín hiệu pháp lý nào (`legal_hits > 0`), hệ thống ép `scores["company"] = 0` và cộng thêm `+2.0` điểm cho nhánh `legal` nếu câu hỏi có kèm từ chỉ thời gian (*"mới nhất"*).
- Khi truy vấn hồ sơ doanh nghiệp bằng tiếng Việt (`has_vn_chars = True`), hệ thống tự động gỡ bỏ bộ lọc cứng `category="company"` của Exa để không làm rơi mất các trang báo cáo tài chính tiếng Việt trong nước.

### 2.3. Xoay Vòng Hai Tầng & Nhảy Nhanh Khi Kết Quả Rỗng (`HTTP 204 Fast-Jump`)

Hệ thống tách bạch rõ hai trạng thái thất bại:
- **Lỗi tại khóa (`HTTP 401/402/403/429/5xx`):** Khóa hiện tại bị lỗi hoặc hết hạn mức, nhưng bản thân công cụ tìm kiếm đó vẫn phù hợp. Hệ thống đưa khóa lỗi vào danh sách cách ly (`cooldown`) và thử ngay khóa tiếp theo trong **cùng một công cụ** theo con trỏ `Round-Robin`.
- **Kết quả rỗng (`HTTP 200` nhưng danh sách `results` trống, được chuẩn hóa thành mã nội bộ `204`):** Khóa hoàn toàn khỏe mạnh, nhưng cơ sở dữ liệu của công cụ đó không có tài liệu khớp với truy vấn. Hệ thống **không phạt khóa** và thoát vòng lặp nội bộ ngay lập tức (`break` tại `search_pool.py:802`) để chuyển sang công cụ tiếp theo.

### 2.4. Băm Một Chiều `key_id` & Nạp Nóng Biến Môi Trường (`Hot-Reload`)

- **Bảo vệ khóa trên đĩa:** Hàm `key_id(key)` (`search_pool.py:91-93`) tính `hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]`. File `/tmp/unified_search_pool_state.json` chỉ lưu chuỗi băm 16 ký tự hex cho bảng `cooldowns` và chuỗi đã che `tvly...xxxx` cho bảng `stats`. Ngay cả khi một tiến trình bên thứ ba đọc được file tạm, không một khóa API thật nào có thể bị khôi phục.
- **Tự động nạp lại (`mtime Hot-Reload`):** Hàm `load_mcp_env()` kiểm tra `env_file.stat().st_mtime` trước mỗi lần lấy khóa (`search_pool.py:58-61`). Người dùng chỉ cần mở `~/.mcp_env`, dán thêm khóa mới và lưu file, máy chủ MCP đang chạy sẽ nhận diện khóa mới ngay ở lượt tìm kiếm tiếp theo mà không cần khởi động lại IDE.

---

## 3. Các Đánh Đổi Kỹ Thuật (`Trade-offs`)

| Quyết định thiết kế | Lợi ích đạt được | Đánh đổi chấp nhận |
|---|---|---|
| **Gom 3 nhà cung cấp sau 1 cổng MCP (`web_search`)** | AI Agent chỉ cần nạp 1 định nghĩa công cụ duy nhất, tiết kiệm hàng nghìn token mô tả schema mỗi lượt hội thoại. | Khi một nhà cung cấp thêm tham số đặc thù rất sâu, người dùng cần cập nhật từ điển `provider_custom_params` trong `QueryRouter`. |
| **Lưu trạng thái chia sẻ qua file JSON cục bộ (`/tmp/`)** | Đồng bộ được con trỏ Round-Robin và trạng thái Cooldown giữa nhiều cửa sổ Claude Code / Antigravity mà không cần cài Redis hay SQLite. | Trong trường hợp cực hiếm khi 2 tiến trình ghi file cùng một phần nghìn giây, một lượt cộng thống kê `stats` có thể bị ghi đè nhẹ (không ảnh hưởng tới tính đúng đắn của kết quả tìm kiếm). |
| **Loại bỏ thư mục `dist/` (117MB) của `browse` khỏi Git** | Giữ kích thước toàn bộ kho lưu trữ nhẹ (`~8MB`), tải về trong vài giây. | Nếu người dùng muốn biên dịch lại trình duyệt headless GStack từ mã nguồn TypeScript, họ sẽ chạy lệnh build của `gstack` trên máy cục bộ. |

---

## 4. Các Phương Án Thay Thế Đã Cân Nhắc

1. **Dùng 3 MCP Server rời rạc (`tavily-mcp`, `exa-mcp-server`, `linkup-mcp`).** Phương án này đã bị loại bỏ làm mặc định vì:
   - Không hỗ trợ xoay vòng nhiều khóa (`Key Pool`) cho cùng một dịch vụ.
   - Khi khóa số 1 hết hạn mức (`HTTP 432`), tiến trình MCP đơn lẻ trả lỗi thẳng về cho AI Agent thay vì tự động chuyển sang khóa dự phòng.
2. **Đặt khóa API trực tiếp trong `mcp_config.json` của từng IDE.** Phương án này bị loại bỏ vì người dùng phải sửa tay ở 5 đến 7 file cấu hình khác nhau mỗi khi thay khóa, đồng thời rất dễ vô tình đính kèm file cấu hình chứa khóa thật khi chia sẻ môi trường. Việc gom toàn bộ khóa về một file `~/.mcp_env` duy nhất (quyền `0600`, nằm ngoài thư mục dự án) giải quyết triệt để rủi ro này.

---

## 5. Tài Liệu Liên Quan

- **Tham chiếu kỹ thuật (Reference):** [Bảng biến môi trường, chữ ký hàm MCP & danh mục `tools/`](./reference-tools-and-api-config.md)
- **Hướng dẫn thực hành (How-To):** [Cách thêm API Key Pool & Tích hợp nhà cung cấp tìm kiếm mới](./how-to-configure-and-extend-api-tools.md)
- **Bài học từng bước (Tutorial):** [15 phút đầu tiên cài đặt và chạy thử hệ thống](./tutorial-first-15-minutes-with-tools.md)
