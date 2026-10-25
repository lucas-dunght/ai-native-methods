# Tham Chiếu Kỹ Thuật · Hệ Sinh Thái `tools/` & Cấu Hình API (`2026.10`)

Tài liệu tham chiếu này mô tả đầy đủ bề mặt kỹ thuật của thư mục [`tools/`](../tools/README.md), bao gồm các biến môi trường API Key, chữ ký hàm của máy chủ MCP `unified-search` (`search_pool.py`), danh mục 58 kỹ năng phụ trợ (`Companion Skills`), 21 tiện ích dòng lệnh `gstack-bin` và 13 mô-đun kiểm định `hooks`.

---

## 1. Biến Môi Trường & Cấu Hình API Key (`~/.mcp_env`)

Máy chủ MCP [`tools/unified-search-mcp/scripts/search_pool.py`](../tools/unified-search-mcp/scripts/search_pool.py) tự động đọc file `~/.mcp_env` (trên macOS/Linux) hoặc `%USERPROFILE%\.mcp_env` (trên Windows) và tự động nạp lại (`hot-reload`) mỗi khi thời gian sửa đổi (`mtime`) của file thay đổi mà không cần khởi động lại tiến trình MCP.

### 1.1. Bảng Biến Môi Trường

| Tên biến | Kiểu dữ liệu | Định dạng chuẩn | Mặc định | Tác dụng & Ràng buộc |
|---|---|---|---|---|
| `TAVILY_KEY_POOL` | `string` (CSV) | `tvly-xxx,tvly-yyy` | `""` | Danh sách API Key của Tavily ngăn cách bằng dấu phẩy `,`. Tự động loại bỏ khoảng trắng thừa và các khóa trùng lặp. |
| `TAVILY_API_KEY` | `string` | `tvly-xxx` | `""` | Khóa đơn lẻ dự phòng khi `TAVILY_KEY_POOL` để trống. Cũng được sử dụng bởi CLI `tvly` trong `tools/skills/tavily/`. |
| `EXA_KEY_POOL` | `string` (CSV) | `uuid-1,uuid-2` | `""` | Danh sách API Key của Exa (định dạng UUID 36 ký tự hoặc chuỗi khóa Exa) ngăn cách bằng dấu phẩy `,`. |
| `EXA_API_KEY` | `string` | `uuid-1` | `""` | Khóa đơn lẻ dự phòng khi `EXA_KEY_POOL` để trống. |
| `LINKUP_KEY_POOL` | `string` (CSV) | `lkp_xxx,lkp_yyy` | `""` | Danh sách API Key của Linkup ngăn cách bằng dấu phẩy `,`. |
| `LINKUP_API_KEY` | `string` | `lkp_xxx` | `""` | Khóa đơn lẻ dự phòng khi `LINKUP_KEY_POOL` để trống. |

### 1.2. Hằng Số Vận Hành Trong `search_pool.py`

| Hằng số | Giá trị mặc định | Vị trí dòng mã | Ý nghĩa kỹ thuật |
|---|---|---|---|
| `COOLDOWN_QUOTA_SECONDS` | `3600` (1 giờ) | `search_pool.py:83` | Thời gian cách ly khóa khi gặp mã lỗi hết hạn mức hoặc sai xác thực (`HTTP 401, 402, 403, 432, 433`). |
| `COOLDOWN_RATELIMIT_SECONDS` | `60` (1 phút) | `search_pool.py:84` | Thời gian cách ly khóa khi vượt ngưỡng gọi ngắn hạn (`HTTP 429`). |
| `COOLDOWN_TRANSIENT_SECONDS` | `30` (30 giây) | `search_pool.py:85` | Thời gian cách ly khóa khi gặp lỗi máy chủ hoặc đứt kết nối tạm thời (`HTTP 5xx`, `504`). |
| `CACHE_TTL_SECONDS` | `300` (5 phút) | `search_pool.py:86` | Thời gian sống của bộ nhớ đệm trong RAM (`TTLCache`, tối đa `128` mục) cho các truy vấn trùng lặp. |
| `STATE_FILE` | `$TMPDIR/unified_search_pool_state.json` | `search_pool.py:88` | File lưu trạng thái con trỏ Round-Robin (`rr_cursor`), thống kê (`stats`) và danh sách khóa đang cách ly (`cooldowns`) với quyền `0600`. Mọi khóa trong `cooldowns` đều được băm một chiều qua `sha256(key)[:16]`. |

---

## 2. Giao Diện Công Cụ MCP (`unified-search`)

Máy chủ `Unified Search Pool` cung cấp 3 công cụ qua giao thức `stdio` của `FastMCP`.

### 2.1. `web_search(query, num_results=5, provider="auto", mode="auto")`

Thực hiện tìm kiếm đa tín hiệu với cơ chế xoay vòng khóa nội bộ (`Round-Robin`) và tự động chuyển đổi dự phòng (`Failover`) giữa `Tavily`, `Exa` và `Linkup`.

- **Tham số đầu vào:**
  - `query` (`str`, bắt buộc): Câu hỏi hoặc cụm từ khóa cần tra cứu.
  - `num_results` (`int`, tùy chọn, mặc định `5`, giới hạn `[1..15]`): Số lượng kết quả trả về tối đa.
  - `provider` (`Optional[str]`, mặc định `"auto"`): Nhận một trong các giá trị `"auto"`, `"tavily"`, `"exa"`, `"linkup"`. Khi khác `"auto"`, hệ thống ép công cụ được chọn lên vị trí ưu tiên số 1.
  - `mode` (`Optional[str]`, mặc định `"auto"`): Nhận một trong 8 chế độ định tuyến:
    - `"auto"`: Chấm điểm trọng số tự động dựa trên biểu thức chính quy đa tín hiệu (`QueryRouter.route`).
    - `"legal"` (hoặc `"law"`): Ưu tiên `Tavily -> Linkup -> Exa` với `search_depth="advanced"` và `include_answer=True`.
    - `"news"` (hoặc `"realtime"`): Ưu tiên `Tavily -> Linkup -> Exa` cho tin tức thời sự và giá cả thời gian thực.
    - `"academic"` (hoặc `"paper"`): Ưu tiên `Exa (category="research paper") -> Linkup -> Tavily`.
    - `"code"` (hoặc `"tech"`): Ưu tiên `Exa (category="github" nếu có từ khóa github, ngược lại None) -> Tavily -> Linkup`.
    - `"company"`: Ưu tiên `Exa (category="company" cho tiếng Anh, None cho tiếng Việt) -> Linkup -> Tavily`.
    - `"deep"` (hoặc `"analysis"`, `"synthesis"`): Ưu tiên `Linkup (output_type="sourcedAnswer") -> Exa -> Tavily`.
    - `"hybrid"`: Chạy song song (`asyncio.gather`) 2 nhà cung cấp đứng đầu, khử trùng lặp URL qua `_deduplicate_markdown_blocks` và hợp nhất kết quả.
- **Giá trị trả về (`str`):** Chuỗi Markdown có tiêu đề ghi rõ nguồn thực thi, nhãn định tuyến và số thứ tự khóa đã dùng (ví dụ `### [Nguồn: TAVILY | Định tuyến: Pháp lý & Quy định (Tavily #1 - Legal RAG) | Key #2]`).

### 2.2. `web_extract(url)`

Trích xuất toàn bộ văn bản sạch từ một đường dẫn URL cụ thể.

- **Tham số đầu vào:**
  - `url` (`str`, bắt buộc): Đường dẫn `http://` hoặc `https://` cần bóc tách nội dung.
- **Cơ chế thực thi:** Thử lần lượt các khóa khả dụng trong `TAVILY_KEY_POOL` qua điểm cuối `https://api.tavily.com/extract` (timeout `15.0s`). Nếu toàn bộ khóa Tavily đều thất bại, tự động chuyển sang `EXA_KEY_POOL` qua điểm cuối `https://api.exa.ai/contents`. Văn bản dài trên `25.000` ký tự được cắt gọn tự động để bảo vệ cửa sổ ngữ cảnh.

### 2.3. `pool_status()`

Trả về báo cáo Markdown thời gian thực về tổng số khóa của từng nhà cung cấp, số khóa đang sẵn sàng, số khóa đang trong thời gian cách ly (`cooldown`), vị trí con trỏ `Key #N` kế tiếp và thống kê số lượt gọi thành công/thất bại của từng khóa đã che (`tvly...xxxx`).

---

## 3. Giao Diện Trình Cài Đặt & Tiện Ích CLI (`tools/gstack-bin/` & `tools/hooks/`)

### 3.1. Script Khởi Tạo Hệ Thống

| Lệnh thực thi | Nền tảng | Chức năng chính |
|---|---|---|
| `./tools/install-all.sh` | macOS / Linux | Cài đặt 3 Bộ Phương Pháp cốt lõi, 58 Companion Skills, 21 `gstack-bin`, 13 `hooks` và gọi `setup_env.sh`. |
| `./tools/unified-search-mcp/scripts/setup_env.sh` | macOS / Linux | Tạo `.venv`, cài `fastmcp>=0.1.0` và `httpx>=0.27.0`, tạo `~/.mcp_env` mẫu (quyền `0600`) và in đoạn cấu hình JSON/YAML cho các AI Client. |
| `.\tools\unified-search-mcp\scripts\setup_env.ps1` | Windows PowerShell | Khởi tạo `.venv` trên Windows, tạo `%USERPROFILE%\.mcp_env` và in cấu hình JSON đã escape dấu `\\`. |

### 3.2. Các Tiện Ích `gstack-bin` Quan Trọng

| Tiện ích | Tham số tiêu biểu | Tác dụng trong Bộ 02 & Bộ 03 |
|---|---|---|
| `gstack-wtree` | `fingerprint` | Tính dấu vân tay SHA-256 (`16 hex`) của `HEAD` + `git status --porcelain` + `git diff` để gắn vào bằng chứng kiểm thử (`WTREE_FINGERPRINT`). |
| `gstack-evidence` | `log`, `verify` | Ghi nhận và đối chiếu sổ cái bằng chứng kiểm thử tại Bước 7 (`VERIFY`) của Bộ 03. |
| `gstack-verify-gate` | `--branch <name>` | Kiểm tra xem nhánh hiện tại đã có đủ bằng chứng chạy test khớp với dấu vân tay cây thư mục trước khi cho phép phát hành hay chưa. |
| `gstack-diff-scope` | `<base-branch>` | Phân tích phạm vi các file thay đổi so với nhánh gốc để phát hiện thay đổi vượt rào (`Scope Creep`). |
| `gstack-redact` | `--repo-visibility <vis> --json` | Quét luồng văn bản hoặc `git diff --cached` để chặn rò rỉ khóa bí mật (trả về mã thoát `3` nếu phát hiện khóa mức `HIGH`). |

### 3.3. Các Mô-đun Kiểm Định Trong `tools/hooks/`

| Mô-đun | Cách gọi kiểm tra | Đầu ra / Quy tắc |
|---|---|---|
| `pr-body-contract.cjs` | `node tools/hooks/pr-body-contract.cjs < pr-body.md` | Trả về JSON `{"ok": true, "missingRequired": [], "missingTraceability": [], "findings": []}`. Trả về mã thoát `1` nếu thiếu mục bắt buộc trong thân PR. |
| `writing-language.cjs` | `node tools/hooks/writing-language.cjs --json` | Trả về ngôn ngữ viết tài liệu/PR mặc định của dự án (`en` hoặc `vi`). |
| `privacy-checker.cjs` | Được nạp bởi các hook bảo mật | Ngăn chặn đọc hoặc xuất các file nhạy cảm (`.env`, `.mcp_env`, khóa SSH, chứng chỉ cá nhân). |

---

## 4. Danh Mục 58 Companion Skills Trong `tools/skills/`

- **Nhóm `tools/skills/tavily/` (8 kỹ năng):** `tavily-search`, `tavily-extract`, `tavily-crawl`, `tavily-map`, `tavily-research`, `tavily-dynamic-search`, `tavily-best-practices`, `tavily-cli`.
- **Nhóm `tools/skills/akkit/` (19 kỹ năng):** `ak-fable-thinking`, `ak-graphify`, `ak-scout`, `ak-brainstorm`, `ak-plan`, `ak-cook`, `ak-fix`, `ak-debug`, `ak-test`, `ak-code-review`, `ak-security`, `ak-worktree`, `ak-orchestrate`, `ak-handoff`, `ak-vibe`, `ak-ship`, `ak-review-pr`, `ak-git`, `ak-watzup`.
- **Nhóm `tools/skills/gstack/` (31 kỹ năng):** `scrape`, `skillify`, `browse`, `setup-browser-cookies`, `setup-gbrain`, `sync-gbrain`, `freeze`, `unfreeze`, `spec`, `autoplan`, `plan-ceo-review`, `plan-eng-review`, `plan-design-review`, `plan-devex-review`, `cso`, `investigate`, `qa`, `qa-only`, `test-audit`, `review`, `ship`, `land-and-deploy`, `canary`, `retro`, `learn`, `guard`, `careful`, `context-save`, `context-restore`, `gstack`, `gstack-upgrade`.

---

## 5. Tài Liệu Liên Quan

- **Hướng dẫn thực hành (How-To):** [Cách cấu hình API Key Pool & Mở rộng thêm nhà cung cấp API mới](./how-to-configure-and-extend-api-tools.md)
- **Bài học từng bước (Tutorial):** [15 phút đầu tiên cài đặt `tools/` và chạy truy vấn đa tín hiệu](./tutorial-first-15-minutes-with-tools.md)
- **Giải thích kiến trúc (Explanation):** [Tại sao thiết kế Bộ định tuyến Đa tín hiệu & Xoay vòng khóa hai tầng](./explanation-multi-signal-router-and-key-pool.md)
