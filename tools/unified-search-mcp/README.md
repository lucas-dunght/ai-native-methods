# Hướng Dẫn Cài Đặt & Cấu Hình Unified Search Pool
### (Tài liệu triển khai đa nền tảng: macOS, Ubuntu / Linux, Windows)
### (Tích hợp: Antigravity, Claude, Cursor, Zed, Hermes Agent, DeepSeek Harness)

Tài liệu này cung cấp hướng dẫn triển khai **chuẩn hóa, độc lập và có thể chạy trên bất kỳ máy tính hoặc máy chủ nào** (macOS, Ubuntu/Linux, Windows) cho hệ thống **Unified Search Pool (Local FastMCP Proxy)** — công cụ proxy thông minh gộp nhiều tài khoản Tavily, Exa, Linkup với cơ chế Failover và Cooldown tự động.

---

## 1. Tổng Quan Kiến Trúc

```
                [ AI Clients: Antigravity / Claude / Cursor / Zed / Hermes / DeepSeek ]
                                                    |
                                                    v
                                  [ Unified Search MCP Proxy ]
                             (Python Script: scripts/search_pool.py)
                                                    |
                 +----------------------------------+----------------------------------+
                 |                                  |                                  |
                 v                                  v                                  v
         [ Tavily Pool ]                      [ Exa Pool ]                      [ Linkup Pool ]
      (Tối đa 5+ API Keys)                (Tối đa 5+ API Keys)               (Tối đa 5+ API Keys)
     - Cooldown 1h nếu lỗi               - Cooldown 1h nếu lỗi              - Cooldown 1h nếu lỗi
     - Tự động chuyển key                - Chuẩn hóa contents text          - Fallback tầng cuối
```

### 🌟 Đặc điểm cốt lõi (Phiên bản v2.0 Smart Engine):
- **Tập trung hóa công cụ**: AI chỉ cần 1 công cụ tìm kiếm duy nhất (`web_search`), tiết kiệm tối đa token context.
- **Tối đa hóa Free Quota & Cân bằng tải (Round-Robin)**: Xoay vòng con trỏ tuần tự giữa 5-6+ tài khoản trong **cùng một dịch vụ** để chia tải đều, và thử hết 100% key của dịch vụ đó trước khi failover sang dịch vụ khác.
- **Định tuyến Đa Tín Hiệu Có Trọng Số (Weighted Multi-Signal Router)**: Chấm điểm đa tín hiệu để chọn công cụ tối ưu nhất, chống bắt nhầm từ khóa (ví dụ: câu hỏi pháp lý/thuế/tin tức có từ *"công ty"* vẫn được định tuyến chuẩn xác về Tavily thay vì bị đẩy nhầm vào kho hồ sơ Startup của Exa).
- **Empty-Result Fast-Jump (HTTP 204)**: Nếu một công cụ trả về 0 kết quả cho truy vấn khó, hệ thống không phạt key mà nhảy ngay sang công cụ tiếp theo để tiết kiệm credit.
- **Tiered Circuit Breaker & Bảo mật Shared State (`key_id` SHA-256)**: Phân tầng thời gian cách ly thông minh (`401/402/403/432/433` hết quota $\rightarrow$ 3600s; `429` Rate Limit $\rightarrow$ 60s; `5xx` lỗi mạng $\rightarrow$ 30s). Đồng bộ trạng thái qua `$TMPDIR/unified_search_pool_state.json` (quyền `0600`), trong đó mọi khóa Cooldown đều được băm 1 chiều bằng `sha256(key)[:16]` và khóa `stats` được che (`provider:tvly...GEzP`) — **tuyệt đối không bao giờ ghi raw API key ra đĩa**.
- **Chế độ Hybrid (`mode="hybrid"`) & TTL Cache (300s)**: Hỗ trợ chạy song song 2 công cụ đầu bảng kèm khử trùng lặp URL, đồng thời lưu bộ nhớ đệm 5 phút cho các truy vấn lặp lại.

---

## 2. Bảng Đường Dẫn Cấu Hình Chuẩn Theo Từng Hệ Điều Hành

| Thành Phần / Ứng Dụng | macOS | Ubuntu / Linux | Windows |
| :--- | :--- | :--- | :--- |
| **Python Venv Thực Thi** | `<PROJECT_DIR>/.venv/bin/python` | `<PROJECT_DIR>/.venv/bin/python` | `<PROJECT_DIR>\.venv\Scripts\python.exe` |
| **Script MCP Chính** | `<PROJECT_DIR>/scripts/search_pool.py` | `<PROJECT_DIR>/scripts/search_pool.py` | `<PROJECT_DIR>\scripts\search_pool.py` |
| **File Biến Môi Trường** | `~/.mcp_env` | `~/.mcp_env` | `%USERPROFILE%\.mcp_env` |
| **Antigravity Global** | `~/.gemini/config/mcp_config.json` | `~/.gemini/config/mcp_config.json` | `%USERPROFILE%\.gemini\config\mcp_config.json` |
| **Antigravity IDE** | `~/.gemini/antigravity-ide/mcp_config.json` | `~/.gemini/antigravity-ide/mcp_config.json` | `%USERPROFILE%\.gemini\antigravity-ide\mcp_config.json` |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` | `~/.config/Claude/claude_desktop_config.json` | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Claude Code CLI** | `~/.claude.json` | `~/.claude.json` | `%USERPROFILE%\.claude.json` |
| **OpenCode CLI** | `~/.config/opencode/opencode.json` | `~/.config/opencode/opencode.json` | `%USERPROFILE%\.config\opencode\opencode.json` |
| **OpenAI Codex CLI / App** | `~/.codex/config.toml` | `~/.codex/config.toml` | `%USERPROFILE%\.codex\config.toml` |
| **Gemini CLI** | `~/.gemini/settings.json` | `~/.gemini/settings.json` | `%USERPROFILE%\.gemini\settings.json` |
| **Hermes Agent (Nous)** | `~/.hermes/config.yaml` | `~/.hermes/config.yaml` | `%USERPROFILE%\.hermes\config.yaml` |
| **DeepSeek Harness (`dsh`)** | `~/.dsh/profiles/<profile>/cordis.patch.yml` | `~/.dsh/profiles/<profile>/cordis.patch.yml` | `%USERPROFILE%\.dsh\profiles\<profile>\cordis.patch.yml` |
| **Cursor / Cline / Roo Code** | `~/Library/Application Support/Cursor/...` | `~/.config/Cursor/...` | `%APPDATA%\Cursor\...` |
| **Zed Editor** | `~/.config/zed/settings.json` | `~/.config/zed/settings.json` | `%APPDATA%\Zed\settings.json` |

---

## 3. Cài Đặt Môi Trường Nhanh (1 Lệnh Tự Động)

Hệ thống đã chuẩn bị sẵn script tự động phát hiện đường dẫn máy của bạn, khởi tạo môi trường ảo Python và sinh sẵn đoạn cấu hình tương thích 100%:

### 🍎/🐧 Trên macOS & Ubuntu / Debian Linux:
Mở Terminal, di chuyển vào thư mục dự án và chạy:
```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```
*Script sẽ tự động tạo `.venv`, cài đặt thư viện `fastmcp` và `httpx`, sau đó in trực tiếp đoạn JSON/YAML có điền sẵn đường dẫn máy của bạn ra màn hình.*

### 🪟 Trên Windows (PowerShell):
Mở PowerShell, di chuyển vào thư mục dự án và chạy:
```powershell
.\scripts\setup_env.ps1
```
*Script sẽ tự động khởi tạo `.venv`, cài thư viện và in ra đoạn JSON đã được escape dấu gạch chéo `\\` chuẩn cú pháp.*

---

## 4. Cài Đặt Thủ Công (Nếu Không Dùng Script Tự Động)

Yêu cầu: **Python 3.10 trở lên**.

### 4.1. macOS & Linux:
```bash
# 1. Di chuyển vào thư mục dự án của bạn
cd /path/to/your/project

# 2. Tạo virtualenv (dùng uv hoặc python3)
uv venv .venv --python 3.12 || python3 -m venv .venv

# 3. Cài đặt thư viện FastMCP và HTTPX
./.venv/bin/pip install "fastmcp>=0.1.0" "httpx>=0.27.0"

# 4. Phân quyền thực thi cho script
chmod +x scripts/search_pool.py
```

### 4.2. Windows (PowerShell):
```powershell
# 1. Di chuyển vào thư mục dự án
cd C:\path\to\your\project

# 2. Tạo virtualenv
python -m venv .venv

# 3. Cài đặt thư viện
.\.venv\Scripts\pip.exe install "fastmcp>=0.1.0" "httpx>=0.27.0"
```

---

## 5. Cấu Hình Biến Môi Trường & Danh Sách Key Pool

File `search_pool.py` sử dụng `Path.home() / ".mcp_env"` nên tương thích trên mọi máy tính mà không cần sửa code.

### 5.1. Nội dung file `.mcp_env`
- Trên macOS / Linux: `~/.mcp_env`
- Trên Windows: `%USERPROFILE%\.mcp_env` (Ví dụ `C:\Users\YourUser\.mcp_env`)

Mẫu cấu hình (ngăn cách các key bằng dấu phẩy `,`):
```bash
# --- UNIFIED SEARCH KEY POOL (Hỗ trợ 5 key mỗi loại, ngăn cách bằng dấu phẩy) ---
export TAVILY_KEY_POOL="tvly-key1-xxx,tvly-key2-xxx,tvly-key3-xxx,tvly-key4-xxx,tvly-key5-xxx"
export EXA_KEY_POOL="exa-key1-xxx,exa-key2-xxx,exa-key3-xxx,exa-key4-xxx,exa-key5-xxx"
export LINKUP_KEY_POOL="linkup-key1-xxx,linkup-key2-xxx,linkup-key3-xxx,linkup-key4-xxx,linkup-key5-xxx"
```

### 5.2. Đồng bộ biến môi trường trên từng OS:

#### 🍎 macOS:
```bash
chmod 600 ~/.mcp_env
source ~/.mcp_env

# Đồng bộ vào GUI session cho Claude Desktop, Antigravity IDE
launchctl setenv TAVILY_KEY_POOL "$TAVILY_KEY_POOL"
launchctl setenv EXA_KEY_POOL "$EXA_KEY_POOL"
launchctl setenv LINKUP_KEY_POOL "$LINKUP_KEY_POOL"

# Tự động nạp mỗi khi mở terminal
echo 'if [ -f "$HOME/.mcp_env" ]; then source "$HOME/.mcp_env"; fi' >> ~/.zshrc
```

#### 🐧 Ubuntu / Linux:
```bash
chmod 600 ~/.mcp_env
echo 'if [ -f "$HOME/.mcp_env" ]; then source "$HOME/.mcp_env"; fi' >> ~/.bashrc
source ~/.bashrc

# Nếu chạy môi trường GUI desktop (Gnome / KDE):
systemctl --user set-environment TAVILY_KEY_POOL="$TAVILY_KEY_POOL"
systemctl --user set-environment EXA_KEY_POOL="$EXA_KEY_POOL"
systemctl --user set-environment LINKUP_KEY_POOL="$LINKUP_KEY_POOL"
```

#### 🪟 Windows (Chạy trong PowerShell):
```powershell
# Nạp trực tiếp vào User Environment Variables của Windows:
[System.Environment]::SetEnvironmentVariable('TAVILY_KEY_POOL', 'tvly-key1-xxx,tvly-key2-xxx,tvly-key3-xxx', 'User')
[System.Environment]::SetEnvironmentVariable('EXA_KEY_POOL', 'exa-key1-xxx,exa-key2-xxx,exa-key3-xxx', 'User')
[System.Environment]::SetEnvironmentVariable('LINKUP_KEY_POOL', 'linkup-key1-xxx,linkup-key2-xxx,linkup-key3-xxx', 'User')
```

---

## 6. Mẫu Cấu Hình Cho Từng Ứng Dụng AI (Clients)

> 💡 **Ký hiệu đường dẫn placeholder**:
> - `<PYTHON_EXE>`: Đường dẫn tuyệt đối đến file python trong `.venv` (VD: `/home/user/project/.venv/bin/python` hoặc `C:\\project\\.venv\\Scripts\\python.exe`).
> - `<SCRIPT_PATH>`: Đường dẫn tuyệt đối đến file `search_pool.py` (VD: `/home/user/project/scripts/search_pool.py` hoặc `C:\\project\\scripts\\search_pool.py`).

---

### 6.1. Google Antigravity (Global & IDE)
- **Vị trí file**:
  - Global: `~/.gemini/config/mcp_config.json` (Windows: `%USERPROFILE%\.gemini\config\mcp_config.json`)
  - IDE: `~/.gemini/antigravity-ide/mcp_config.json` (Windows: `%USERPROFILE%\.gemini\antigravity-ide\mcp_config.json`)

```json
{
  "mcpServers": {
    "unified-search": {
      "command": "<PYTHON_EXE>",
      "args": [
        "<SCRIPT_PATH>"
      ]
    }
  }
}
```

---

### 6.2. Claude Desktop
- **Vị trí file**:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
  - Linux: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "unified-search": {
      "command": "<PYTHON_EXE>",
      "args": [
        "<SCRIPT_PATH>"
      ]
    }
  }
}
```
*(Khởi động lại hoàn toàn Claude Desktop bằng Cmd+Q hoặc Quit khay hệ thống)*

---

### 6.3. Claude Code (CLI)
- **Vị trí file**: `~/.claude.json` (Windows: `%USERPROFILE%\.claude.json`)

**Cấu hình JSON:**
```json
{
  "mcpServers": {
    "unified-search": {
      "type": "stdio",
      "command": "<PYTHON_EXE>",
      "args": [
        "<SCRIPT_PATH>"
      ],
      "env": {}
    }
  }
}
```

**Hoặc thêm nhanh bằng lệnh CLI:**
- macOS / Linux:
  ```bash
  claude mcp add unified-search "<PYTHON_EXE>" "<SCRIPT_PATH>"
  ```
- Windows:
  ```powershell
  claude mcp add unified-search "<PYTHON_EXE>" "<SCRIPT_PATH>"
  ```

---

### 6.4. Hermes Agent (Nous Research)
- **Vị trí file**: `~/.hermes/config.yaml` (Windows: `%USERPROFILE%\.hermes\config.yaml`)

```yaml
mcp_servers:
  unified-search:
    command: "<PYTHON_EXE>"
    args:
      - "<SCRIPT_PATH>"
    env: {}
    timeout: 120
    connect_timeout: 30
```
*(Trong giao diện TUI của Hermes, gõ lệnh `/reload-mcp` để nạp ngay lập tức)*

---

### 6.5. DeepSeek Harness (`dsh`)
- **Vị trí file**: `~/.dsh/profiles/<profile>/cordis.patch.yml` (Windows: `%USERPROFILE%\.dsh\profiles\<profile>\cordis.patch.yml`)

```yaml
- id: mcp-unified-search
  name: "@deepseek-ai/dsh-mcp-client"
  config:
    serverName: unified-search
    transport: stdio
    command: "<PYTHON_EXE>"
    args:
      - "<SCRIPT_PATH>"
    env: {}
```
*(Cài đặt plugin nếu profile chưa có: `npx @deepseek-ai/dsh plugin --profile <profile> add @deepseek-ai/dsh-mcp-client`)*

---

### 6.6. Cursor / VS Code (Cline, Roo Code, Continue)
- **Cấu hình MCP Settings:**
```json
{
  "mcpServers": {
    "unified-search": {
      "command": "<PYTHON_EXE>",
      "args": [
        "<SCRIPT_PATH>"
      ],
      "disabled": false,
      "autoApprove": [
        "web_search",
        "web_extract",
        "pool_status"
      ]
    }
  }
}
```

---

### 6.7. Zed Editor
- **Vị trí file**: `~/.config/zed/settings.json` (Windows: `%APPDATA%\Zed\settings.json`)

```json
{
  "experimental": {
    "context_servers": {
      "servers": {
        "unified-search": {
          "command": "<PYTHON_EXE>",
          "args": [
            "<SCRIPT_PATH>"
          ]
        }
      }
    }
  }
}
```

---

### 6.8. OpenCode CLI
- **Vị trí file**: `~/.config/opencode/opencode.json` (Windows: `%USERPROFILE%\.config\opencode\opencode.json`)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "unified-search": {
      "command": [
        "<PYTHON_EXE>",
        "<SCRIPT_PATH>"
      ],
      "enabled": true,
      "type": "local"
    }
  }
}
```
*(Kiểm tra kết nối bằng lệnh: `opencode mcp list`)*

---

### 6.9. OpenAI Codex CLI & Codex App
- **Vị trí file**: `~/.codex/config.toml` (Windows: `%USERPROFILE%\.codex\config.toml`)

```toml
[mcp_servers.unified-search]
  command = "<PYTHON_EXE>"
  args = ["<SCRIPT_PATH>"]
  enabled = true
  startup_timeout_sec = 15
  tool_timeout_sec = 120
```
*(Kiểm tra kết nối bằng lệnh: `codex mcp list`)*

---

### 6.10. Gemini CLI
- **Vị trí file**: `~/.gemini/settings.json` (Windows: `%USERPROFILE%\.gemini\settings.json`)

```json
{
  "mcpServers": {
    "unified-search": {
      "command": "<PYTHON_EXE>",
      "args": [
        "<SCRIPT_PATH>"
      ],
      "env": {}
    }
  }
}
```

---

## 7. Chế Độ Định Tuyến Đa Tín Hiệu Có Trọng Số (v2.0 Smart Engine)

### 🌟 7.1. Ma Trận Chấm Điểm Đa Tín Hiệu (Weighted Multi-Signal Scoring):
Thay vì bắt từ khóa đơn lẻ dễ nhầm lẫn, `web_search` v2.0 chấm điểm đồng thời tất cả các tín hiệu trong câu hỏi kèm quy tắc **Chống bắt nhầm (Anti-Hijacking)**:

| Thể Loại Truy Vấn | Dấu Hiệu Nhận Diện & Trọng Số | Thứ Tự Ưu Tiên | Điểm Mạnh & Tối Ưu Hóa Tham Số |
| :--- | :--- | :---: | :--- |
| **Pháp lý, Thuế, Bảo hiểm & Chính sách VN** | *luật, nghị định, thông tư, quy định, bảo hiểm xã hội, bhxh, thuế thu nhập, bảng lương, mức phạt, thủ tục...* (`Trọng số x4.0`) | **Tavily** $\rightarrow$ Linkup $\rightarrow$ Exa | Kích hoạt `topic="general"` + `include_answer=True`. **Chống bắt nhầm** vào nhóm Company ngay cả khi câu hỏi chứa từ *"công ty"* hoặc *"doanh nghiệp"*. |
| **Thời sự, Tin nóng & Giá cả hôm nay** | *hôm nay, tin tức, mới nhất, thời tiết, giá vàng, tỷ giá, chứng khoán, vn-index, breaking news, latest...* (`Trọng số x2.5`) | **Tavily** $\rightarrow$ Linkup $\rightarrow$ Exa | Tự động chọn `topic="general"` (cho dữ liệu Việt Nam thời gian thực) hoặc `topic="news"` (tin quốc tế) kèm tóm tắt AI trực tiếp. |
| **Học thuật & Bài báo khoa học** | *arxiv, research paper, scientific paper, luận án, whitepaper, peer-reviewed, sota, doi:...* (`Trọng số x3.5`) | **Exa** $\rightarrow$ Linkup $\rightarrow$ Tavily | Kích hoạt Exa `search_type="auto"` với `category="research paper"`, truy cập trực tiếp kho bài báo arXiv và hội thảo khoa học. |
| **Lập trình, Mã nguồn & Tài liệu kỹ thuật** | *github, source code, python, typescript, rust, sdk, api, library, thuật toán, traceback, dockerfile, mcp server...* (`Trọng số x3.0`) | **Exa** $\rightarrow$ Tavily $\rightarrow$ Linkup | Chỉ bật `category="github"` khi tìm đúng repo GitHub; còn lại mở rộng `search_type="auto"` để bao phủ cả trang Docs chính thức và StackOverflow. |
| **Hồ sơ Startup, Gọi vốn & Đối thủ** | *startup, venture capital, series a, funding round, founder, nhà sáng lập, đối thủ cạnh tranh, crunchbase...* (`Trọng số x2.5`) | **Exa** $\rightarrow$ Linkup $\rightarrow$ Tavily | Kích hoạt tra cứu ngữ nghĩa thị trường khởi nghiệp và hồ sơ doanh nghiệp. |
| **Tổng hợp & Phân tích chuyên sâu** | *tìm hiểu sâu, phân tích toàn diện, tổng hợp chi tiết, deep dive, so sánh chi tiết, báo cáo phân tích...* (`Trọng số x3.2`) | **Linkup** $\rightarrow$ Exa $\rightarrow$ Tavily | Kích hoạt Linkup `outputType="sourcedAnswer"`, trả về bài phân tích tổng hợp đa chiều kèm danh sách nguồn trích dẫn. |
| **Chế độ Hybrid (`mode="hybrid"`)** | *Khi truyền tham số `mode="hybrid"` cho câu hỏi khó cần kiểm chứng chéo* | **Top 1 + Top 2 chạy song song** | Chạy đồng thời (`asyncio.gather`) 2 công cụ đầu bảng, tự động khử trùng lặp URL và hợp nhất kết quả. |

### 🔁 7.2. Nguyên Tắc Xoay Vòng & Tự Phục Hồi (v2.0):
- **Cân bằng tải Round-Robin trong cùng công cụ**: Tự động xoay vòng con trỏ (`Key #1 -> #2 -> ... -> #6`) giữa các tài khoản của cùng một dịch vụ để chia đều hạn mức và tránh chạm ngưỡng Rate Limit khi gọi song song.
- **Ưu tiên tối đa cùng công cụ**: Luôn thử hết toàn bộ 6 keys khỏe mạnh của công cụ số 1 trước khi chuyển sang công cụ số 2.
- **Empty-Result Fast-Jump (HTTP 204)**: Nếu công cụ số 1 trả về 0 kết quả (`results == []`), hệ thống hiểu rằng key vẫn tốt nhưng công cụ đó không có dữ liệu $\rightarrow$ **Không phạt key** và lập tức nhảy sang công cụ số 2 để tiết kiệm credit.
- **Tiered Circuit Breaker (Cách ly phân tầng)**:
  - Mã `401, 402, 403, 432, 433` (Hết credit / Key hỏng): Cách ly **3600 giây (1 giờ)**.
  - Mã `429` (Giới hạn tốc độ ngắn hạn): Cách ly **60 giây**.
  - Mã `500, 502, 503, 504` (Lỗi mạng / Timeout tạm thời): Cách ly **30 giây**.
- **Chia sẻ trạng thái đa tiến trình an toàn (Zero Raw-Key Persistence)**:
  - Lưu trạng thái Cooldown, con trỏ Round-Robin và bộ đếm thống kê vào `$TMPDIR/unified_search_pool_state.json` với quyền truy cập giới hạn `0600` (`rw-------`).
  - **Băm 1 chiều (`key_id`)**: Mọi truy cập vào `cooldowns` (`is_cooled_down`, `record_success`, `mark_failure`, `pool_status`) đều đi qua hàm `key_id(key) = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]`.
  - **Tự động lọc sạch khóa cũ**: `_load_state()` và `_save_state()` chỉ giữ các khóa khớp biểu thức chính quy `[0-9a-f]{16}`, tự động loại bỏ mọi bản ghi raw key cũ nếu từng tồn tại.
  - **Che khóa thống kê (`stats`)**: Chỉ lưu dưới dạng đã mask (`tavily:tvly...GEzP`), đảm bảo raw API key không bao giờ xuất hiện trên ổ đĩa hay bản sao lưu.

### 🛠️ 7.3. Danh Mục Công Cụ MCP:
1. `web_search(query, num_results=5, provider='auto', mode='auto')`:
   - `provider`: `'auto'` | `'tavily'` | `'exa'` | `'linkup'`
   - `mode`: `'auto'` | `'news'` | `'legal'` | `'academic'` | `'code'` | `'company'` | `'deep'` | `'hybrid'`
2. `web_extract(url)`: Bóc tách nội dung toàn văn trang web qua Tavily Extract $\rightarrow$ Exa Contents (cắt gọn 25,000 ký tự an toàn).
3. `pool_status()`: Báo cáo thời gian thực trạng thái 18 keys, vị trí con trỏ Round-Robin kế tiếp (`🎯`), bộ đếm `OK / Lỗi` và thời gian Cooldown còn lại.

---

## 8. Kiểm Thử Nhanh & Kiểm Tra Bảo Mật Từ Dòng Lệnh

### 8.1. macOS & Linux:
```bash
# 1. Kiểm tra cú pháp và trạng thái pool & con trỏ Round-Robin
./.venv/bin/python -m py_compile scripts/search_pool.py
./.venv/bin/python -c "from scripts.search_pool import pool_status; print(pool_status())"

# 2. Test tìm kiếm thực tế
./.venv/bin/python -c "import asyncio; from scripts.search_pool import web_search; print(asyncio.run(web_search('quy định đóng bảo hiểm xã hội của công ty năm 2026', num_results=2)))"
```

### 8.2. Windows (PowerShell):
```powershell
# 1. Kiểm tra trạng thái pool & con trỏ Round-Robin
& ".\.venv\Scripts\python.exe" -c "from scripts.search_pool import pool_status; print(pool_status())"

# 2. Test tìm kiếm thực tế
& ".\.venv\Scripts\python.exe" -c "import asyncio; from scripts.search_pool import web_search; print(asyncio.run(web_search('quy định đóng bảo hiểm xã hội của công ty năm 2026', num_results=2)))"
```

### 8.3. Regression Test Bảo Mật (Chống Rò Rỉ Raw API Key Ra State File — Bắt Buộc Khi Nâng Cấp):
Chạy đoạn kiểm tra dưới đây để xác nhận `STATE_FILE` chỉ lưu mã băm 16 ký tự hex (`key_id`) và tuyệt đối không ghi raw API key ra đĩa:

```bash
./.venv/bin/python -c "
from scripts.search_pool import pool_mgr, key_id, STATE_FILE
fake = 'tvly-YOUR_TAVILY_API_KEY'
assert not pool_mgr.is_cooled_down(fake)
pool_mgr.mark_failure('tavily', fake, 429, 'test')
assert pool_mgr.is_cooled_down(fake)                 # Cooldown vẫn hoạt động
assert fake not in STATE_FILE.read_text()            # ★ Raw key KHÔNG vào file
assert key_id(fake) in STATE_FILE.read_text()        # ★ Chỉ có hash 16 hex
pool_mgr.record_success('tavily', fake)              # Dọn entry test
pool_mgr.stats.pop(f'tavily:{pool_mgr.mask_key(fake)}', None)
pool_mgr._save_state()
print('PASS: Không rò rỉ raw key ra đĩa!')
"
```

---

## 9. Xử Lý Sự Cố Thường Gặp & Vệ Sinh Bảo Mật (Troubleshooting & Security Hygiene)

### Q1: Báo lỗi "Tất cả các tài khoản đều cạn credit hoặc chưa cấu hình"
- **Xử lý**:
  - Dùng tool `pool_status` để xem key nào đang dính cooldown và lý do cụ thể (`HTTP 401/402/429`).
  - Điền thêm key mới vào file `.mcp_env`. Nhờ cơ chế kiểm tra `mtime`, hệ thống sẽ tự động nạp lại key mới ngay lập tức mà không cần khởi động lại.

### Q2: Trên Windows báo lỗi cú pháp JSON
- **Nguyên nhân**: Dấu gạch chéo ngược `\` trong JSON không được escape.
- **Xử lý**: Trong file JSON, đổi `C:\path\to\...` thành `C:\\path\\to\\...`. Hoặc chạy script `.\scripts\setup_env.ps1` để sinh sẵn JSON đã escape chính xác.

### Q3: Muốn reset trạng thái Cooldown, bộ đếm thống kê hoặc vệ sinh State File cũ?
- Nếu máy từng chạy phiên bản cũ (trước khi có bản vá `key_id` SHA-256), hãy kiểm tra và xóa sạch file trạng thái tạm thời để đảm bảo không còn bản ghi cũ trên đĩa:
  ```bash
  SF="${TMPDIR:-/tmp}/unified_search_pool_state.json"
  grep -c "tvly-dev-\|^.*-[0-9a-f]\{12\}" "$SF" 2>/dev/null || true   # >0 = file cũ từng chứa raw key
  rm -f "$SF"                                                         # Reset toàn bộ cursor/cooldown/stats
  ```
- Trên Windows PowerShell:
  ```powershell
  Remove-Item "$env:TEMP\unified_search_pool_state.json" -Force -ErrorAction SilentlyContinue
  ```
- Lưu ý: Nếu file state cũ trên máy của bạn từng báo kết quả `grep > 0` (từng chứa raw key trên đĩa), khuyến nghị **rotate (đổi mới) API key** đó trên trang quản trị của nhà cung cấp.

