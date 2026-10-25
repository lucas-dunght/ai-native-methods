# How to · Cách Thêm API Key Pool, Kết Nối AI Client & Tích Hợp Nhà Cung Cấp API Mới (`2026.10`)

Tài liệu hướng dẫn thực hành này chỉ dẫn từng bước cách đăng ký và nạp khóa API (`API Key Pool`) vào hệ thống `tools/`, cách kết nối máy chủ MCP `unified-search` vào các trình biên tập AI và cách viết thêm mã nguồn để tích hợp một nhà cung cấp API tìm kiếm mới vào `search_pool.py`.

---

## Điều Kiện Tiên Quyết (`Prerequisites`)

- Đã tải kho lưu trữ `ai-native-methods` về máy tính.
- Có sẵn **Python 3.10 trở lên** (khuyến nghị cài thêm `uv` để khởi tạo môi trường ảo nhanh gấp 10 lần `pip`).
- Đã chạy lệnh cài đặt tự động `./tools/install-all.sh` (trên macOS/Linux) hoặc `.\tools\unified-search-mcp\scripts\setup_env.ps1` (trên Windows).

---

## Phần 1 · How to Lấy & Thêm API Key Pool Vào `~/.mcp_env`

Máy chủ `Unified Search Pool v2.0` đọc danh sách khóa từ file `~/.mcp_env` (hoặc `%USERPROFILE%\.mcp_env` trên Windows). Bạn có thể nạp từ 1 đến 6+ khóa cho mỗi dịch vụ để nhân gấp nhiều lần hạn mức miễn phí hàng tháng.

### Bước 1. Đăng ký khóa API miễn phí từ 3 nhà cung cấp

1. **Tavily (`TAVILY_KEY_POOL`):**
   - Truy cập `https://app.tavily.com` và đăng nhập.
   - Mỗi tài khoản nhận **1.000 lượt tìm kiếm miễn phí/tháng**. Khóa có định dạng `tvly-dev-...` hoặc `tvly-...`.
2. **Exa (`EXA_KEY_POOL`):**
   - Truy cập `https://dashboard.exa.ai` và tạo tài khoản.
   - Mỗi tài khoản nhận **hạn mức dùng thử miễn phí** cho tìm kiếm ngữ nghĩa (`Neural Search`), bài báo khoa học và mã nguồn. Khóa có định dạng UUID (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).
3. **Linkup (`LINKUP_KEY_POOL`):**
   - Truy cập `https://app.linkup.so` và lấy khóa trong mục API Keys.
   - Mỗi tài khoản nhận **5 EUR hạn mức miễn phí/tháng** cho chế độ tổng hợp chuyên sâu (`sourcedAnswer`). Khóa có định dạng `lkp_...`.

### Bước 2. Mở file `~/.mcp_env` và điền danh sách khóa

Trên macOS hoặc Linux, chạy lệnh sau để mở (hoặc tạo từ bản mẫu `.mcp_env.example`):

```bash
cp -n tools/unified-search-mcp/.mcp_env.example ~/.mcp_env
chmod 600 ~/.mcp_env
nano ~/.mcp_env
```

Điền các khóa của bạn vào giữa cặp dấu ngoặc kép, ngăn cách nhiều khóa của cùng một dịch vụ bằng dấu phẩy `,` (không cần khoảng trắng):

```bash
# --- UNIFIED SEARCH KEY POOL ---
export TAVILY_KEY_POOL="<YOUR_TAVILY_KEY_1>,<YOUR_TAVILY_KEY_2>,<YOUR_TAVILY_KEY_3>"
export EXA_KEY_POOL="<YOUR_EXA_KEY_1>,<YOUR_EXA_KEY_2>"
export LINKUP_KEY_POOL="<YOUR_LINKUP_KEY_1>,<YOUR_LINKUP_KEY_2>"

# (Tùy chọn) Khóa đơn lẻ cho các công cụ CLI đọc trực tiếp TAVILY_API_KEY
export TAVILY_API_KEY="<YOUR_TAVILY_KEY_1>"
```

> **Lưu ý về cơ chế Hot-Reload:** Ngay sau khi bạn bấm lưu file `~/.mcp_env`, hàm `load_mcp_env()` trong `search_pool.py` sẽ tự động phát hiện thời gian sửa đổi file (`mtime`) mới và nạp danh sách khóa mới ngay ở câu lệnh tìm kiếm tiếp theo mà **không cần khởi động lại IDE**.

---

## Phần 2 · How to Cấu Hình API Cho Bộ Kỹ Năng CLI (`tavily-cli` & `gbrain`)

Ngoài máy chủ MCP `unified-search`, một số kỹ năng chuyên biệt trong `tools/skills/` có thể gọi qua giao diện dòng lệnh (`CLI`):

### 1. Cấu hình `tavily-cli` (`tvly`) cho kỹ năng `tavily-dynamic-search` (PTC)

Khi sử dụng các kỹ năng trong `tools/skills/tavily/` (như lọc ngữ cảnh cô lập bằng Python hoặc cào toàn bộ chuyên mục bằng `tavily-crawl`), hãy nạp biến môi trường từ `~/.mcp_env` vào shell của bạn:

```bash
# Thêm dòng tự động nạp ~/.mcp_env vào ~/.zshrc (macOS) hoặc ~/.bashrc (Linux)
grep -q "source ~/.mcp_env" ~/.zshrc 2>/dev/null || echo '[ -f ~/.mcp_env ] && source ~/.mcp_env' >> ~/.zshrc
source ~/.zshrc
```

Nếu bạn đã cài công cụ dòng lệnh `tvly`, bạn cũng có thể đăng nhập một lần bằng lệnh:

```bash
tvly login --api-key "$TAVILY_API_KEY"
```

### 2. Cấu hình API nhúng Vector cho `gstack /setup-gbrain` (Bộ 02 cấp độ 3)

Khi kho tri thức `Kernel Registry` của Bộ 02 vượt quá `500` mục và bạn kích hoạt `/setup-gbrain`:
- **Chế độ cục bộ miễn phí (`Local PGLite`):** Không cần khóa API bên ngoài.
- **Chế độ tìm kiếm ngữ nghĩa nâng cao (`Vector Embeddings`):** Thêm `OPENAI_API_KEY` hoặc `GEMINI_API_KEY` vào `~/.mcp_env`:

```bash
export GEMINI_API_KEY="<YOUR_GEMINI_API_KEY>"
export OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

---

## Phần 3 · How to Kết Nối Máy Chủ MCP `unified-search` Vào AI Client

Khi bạn chạy `./tools/install-all.sh`, màn hình Terminal đã in sẵn đường dẫn tuyệt đối của máy bạn. Dưới đây là cách gắn đoạn cấu hình đó vào từng công cụ:

### 1. Antigravity IDE / Antigravity 2.0 / Cursor / Claude Desktop

Mở file cấu hình MCP tương ứng:
- **Antigravity 2.0:** `~/.gemini/config/mcp_config.json` (hoặc `~/.gemini/antigravity/mcp_config.json`)
- **Antigravity IDE:** `~/.gemini/antigravity-ide/mcp_config.json`
- **Claude Desktop (macOS):** `~/Library/Application Support/Claude/claude_desktop_config.json`

Thêm mục `"unified-search"` vào trong khối `"mcpServers"` (thay `/ABS/PATH/TO/ai-native-methods` bằng đường dẫn thư mục repo trên máy bạn):

```json
{
  "mcpServers": {
    "unified-search": {
      "command": "/ABS/PATH/TO/ai-native-methods/tools/unified-search-mcp/.venv/bin/python",
      "args": [
        "-u",
        "/ABS/PATH/TO/ai-native-methods/tools/unified-search-mcp/scripts/search_pool.py"
      ]
    }
  }
}
```

### 2. Claude Code CLI (1 lệnh duy nhất)

```bash
REPO_DIR="$(pwd)"
claude mcp add unified-search \
  "${REPO_DIR}/tools/unified-search-mcp/.venv/bin/python" \
  "${REPO_DIR}/tools/unified-search-mcp/scripts/search_pool.py"
```

---

## Phần 4 · How to Tích Hợp Thêm Một Nhà Cung Cấp API Mới Vào `search_pool.py`

Giả sử bạn muốn thêm một dịch vụ tìm kiếm thứ tư (ví dụ **Brave Search API** hoặc **Serper.dev**) vào [`tools/unified-search-mcp/scripts/search_pool.py`](../tools/unified-search-mcp/scripts/search_pool.py) để tăng thêm tầng dự phòng. Bạn chỉ cần thực hiện **4 bước chỉnh sửa chuẩn hóa** sau đây:

### Bước 1. Khai báo biến Pool mới trong `~/.mcp_env` và `KeyPoolManager`

1. Thêm dòng biến môi trường vào `~/.mcp_env`:
   ```bash
   export BRAVE_KEY_POOL="<YOUR_BRAVE_KEY_1>,<YOUR_BRAVE_KEY_2>"
   ```
2. Trong file `tools/unified-search-mcp/scripts/search_pool.py`, mở lớp `KeyPoolManager`:
   - Tại dòng `101`, thêm `"brave": 0` vào từ điển con trỏ `self.rr_cursor`:
     ```python
     self.rr_cursor: Dict[str, int] = {"tavily": 0, "exa": 0, "linkup": 0, "brave": 0}
     ```
   - Tại dòng `120`, thêm `"brave"` vào danh sách khôi phục con trỏ:
     ```python
     for p in ("tavily", "exa", "linkup", "brave"):
     ```
   - Tại phương thức `get_keys(self, provider: str)` (dòng `165`), thêm nhánh đọc khóa `"brave"`:
     ```python
     elif provider == "brave":
         return self.parse_pool("BRAVE_KEY_POOL", "BRAVE_API_KEY")
     ```

### Bước 2. Viết hàm gọi API bất đồng bộ `search_<provider>()`

Tại Mục 5 (`Provider Search Clients`, khoảng dòng `745` của `search_pool.py`), thêm hàm bất đồng bộ trả về bộ ba `(success: bool, content: str, http_status: int)`. Lưu ý trả về mã `204` nếu kết quả rỗng để kích hoạt cơ chế nhảy nhanh không phạt khóa:

```python
async def search_brave(
    query: str,
    key: str,
    num_results: int = 5,
) -> Tuple[bool, str, int]:
    """Tìm kiếm qua Brave Web Search API."""
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "X-Subscription-Token": key,
        "Accept": "application/json",
    }
    params = {"q": query, "count": num_results}
    try:
        client = get_http_client()
        resp = await client.get(url, headers=headers, params=params, timeout=12.0)
        if resp.status_code != 200:
            return False, resp.text, resp.status_code
        data = resp.json()
        web_items = data.get("web", {}).get("results", [])
        if not web_items:
            return False, "EMPTY_RESULTS", 204
        lines = []
        for item in web_items[:num_results]:
            title = (item.get("title") or "No title").strip()
            u = (item.get("url") or "").strip()
            desc = (item.get("description") or "").strip()
            lines.append(f"- [{title}]({u})\n  {desc}")
        return True, "\n\n".join(lines), 200
    except httpx.TimeoutException:
        return False, "Timeout khi kết nối tới Brave API", 504
    except Exception as e:
        return False, str(e), 500
```

### Bước 3. Nối hàm mới vào `_execute_single_provider()`

Trong hàm `_execute_single_provider()` (khoảng dòng `785` của `search_pool.py`), thêm nhánh `elif provider_name == "brave":`:

```python
        elif provider_name == "brave":
            success, content, status = await search_brave(query, key, num_results)
```

### Bước 4. Đăng ký nhà cung cấp mới vào `QueryRouter` và `pool_status()`

1. Trong `QueryRouter.route()` (`search_pool.py:379`), thêm `"brave"` vào danh sách `provider_order` dự phòng (ví dụ `["tavily", "exa", "linkup", "brave"]`).
2. Trong hàm `pool_status()` (`search_pool.py:1010`), thêm `brave_keys = pool_mgr.get_keys("brave")` và gọi `format_provider("brave", "Brave", brave_keys, "Tìm kiếm web độc lập")` để hiển thị trạng thái khóa trên bảng điều khiển.

---

## Kiểm Chứng Kết Quả (`Verification`)

Sau khi thêm khóa vào `~/.mcp_env` (hoặc sau khi tích hợp nhà cung cấp mới), hãy chạy lệnh kiểm tra trực tiếp từ Terminal mà không cần mở IDE:

```bash
./tools/unified-search-mcp/.venv/bin/python -c '
import asyncio
from tools.unified_search_mcp.scripts.search_pool import pool_status
' 2>/dev/null || \
./tools/unified-search-mcp/.venv/bin/python -c '
import sys
sys.path.insert(0, "tools/unified-search-mcp/scripts")
import search_pool
print(search_pool.pool_status())
'
```

**Kết quả mong đợi:**
- Màn hình in ra bảng `## Trạng thái Unified Search Key Pool v2.0`.
- Dòng `Tavily`, `Exa`, `Linkup` hiển thị đúng số lượng khóa bạn đã nhập (ví dụ `3 key (3 khả dụng, 0 cooldown) | Con trỏ kế tiếp: Key #1`).
- Toàn bộ mã khóa hiển thị trên màn hình đều được che ở dạng `tvly...xxxx`.

---

## Xử Lý Sự Cố Thường Gặp (`Troubleshooting`)

| Triệu chứng lỗi | Nguyên nhân gốc rễ | Cách khắc phục triệt để |
|---|---|---|
| `pool_status()` báo `0 key được cấu hình` dù đã sửa file | Sửa nhầm file `.mcp_env.example` trong repo thay vì file `~/.mcp_env` ở thư mục Home của người dùng. | Chạy `cat ~/.mcp_env` để kiểm tra. Đảm bảo các dòng có định dạng `export TAVILY_KEY_POOL="..."`. |
| Lỗi `ModuleNotFoundError: No module named 'fastmcp'` | Đang gọi bằng `/usr/bin/python3` của hệ thống thay vì Python trong `.venv`. | Luôn dùng đường dẫn `<REPO_ROOT>/tools/unified-search-mcp/.venv/bin/python` trong `mcp_config.json`, hoặc chạy lại `./tools/install-all.sh`. |
| Tất cả các khóa báo `Quota/Auth (HTTP 401)` và bị cách ly `3600s` | Khóa API dán vào `~/.mcp_env` bị dư dấu ngoặc kép lồng nhau hoặc sai khóa. | Sửa lại khóa trong `~/.mcp_env`, sau đó xóa file trạng thái tạm bằng lệnh `rm -f ${TMPDIR:-/tmp}/unified_search_pool_state.json` để mở khóa ngay lập tức. |
| GitHub chặn lệnh `git push` báo phát hiện Secret (`GH013`) | Bạn vô tình dán khóa API thật vào một file nằm trong thư mục dự án thay vì `~/.mcp_env`. | Chạy `./tools/gstack-bin/gstack-redact-prepush` để tìm vị trí khóa bị lộ, chuyển khóa đó vào `~/.mcp_env` và sửa lại commit trước khi push. |

---

## Tài Liệu Liên Quan

- **Bài học từng bước (Tutorial):** [15 phút đầu tiên cài đặt và chạy thử toàn bộ công cụ](./tutorial-first-15-minutes-with-tools.md)
- **Tham chiếu kỹ thuật (Reference):** [Bảng biến môi trường, chữ ký hàm MCP & danh mục `tools/`](./reference-tools-and-api-config.md)
- **Giải thích kiến trúc (Explanation):** [Cơ chế định tuyến đa tín hiệu & xoay vòng khóa an toàn](./explanation-multi-signal-router-and-key-pool.md)
