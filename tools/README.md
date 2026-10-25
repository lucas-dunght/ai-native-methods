# Bộ Công Cụ & Kỹ Năng Đi Kèm (`tools/` · Phiên bản 2026.10)

Thư mục `tools/` đóng gói đầy đủ toàn bộ các công cụ, máy chủ MCP, kỹ năng phụ trợ (`Companion Skills`), tiện ích dòng lệnh (`CLI Binaries`) và bộ kiểm định hợp đồng phát hành (`Governance Hooks`) được tham chiếu trong ba bộ phương pháp của kho lưu trữ này. Người dùng mới khi tải kho lưu trữ về máy có thể cài đặt và sử dụng ngay lập tức mà không cần tự đi tìm từng công cụ rời rạc bên ngoài.

> **Cam kết An ninh & Bảo mật:** Toàn bộ mã nguồn trong `tools/` đã được kiểm toán tự động để đảm bảo **không chứa bất kỳ API Key, Token hay đường dẫn cá nhân cứng nào**. Mọi khóa API đều được nạp động từ file `~/.mcp_env` trên máy của người dùng (kèm mẫu `.mcp_env.example`).

---

## 1. Cài Đặt Nhanh Bằng 1 Lệnh (Bootstrap)

Trên macOS hoặc Linux, mở Terminal tại thư mục gốc của kho lưu trữ và chạy lệnh sau:

```bash
chmod +x tools/install-all.sh
./tools/install-all.sh
```

Lệnh trên sẽ tự động thực hiện 5 bước:
1. Cài đặt **3 Bộ Phương Pháp cốt lõi** (`internet-info-refinement` v2.0, `kernel-registry-sot` v2.0, `vibecode-kit-v6` v6.1) vào `~/.gemini/config/skills/`.
2. Cài đặt **58 Companion Skills** thuộc 3 nhóm (`tavily`, `akkit`, `gstack`) vào `~/.gemini/config/skills/`.
3. Cài đặt **21 tiện ích CLI (`gstack-bin`)** vào `~/.gemini/config/skills/bin/` và hook đồng bộ Antigravity vào `~/.gstack/hooks/post-upgrade-antigravity.sh`.
4. Cài đặt **13 Governance Hooks** (`pr-body-contract.cjs`, `writing-language.cjs`, `privacy-checker.cjs`...) vào `~/.claude/hooks/lib/`.
5. Khởi tạo môi trường ảo Python `.venv` cho máy chủ MCP **`unified-search` v2.0**, tạo file mẫu `~/.mcp_env` (nếu chưa tồn tại) và in sẵn đoạn cấu hình JSON để dán vào `mcp_config.json`.

---

## 2. Cấu Trúc Chi Tiết Thư Mục `tools/`

```text
tools/
├── README.md                         # Tài liệu hướng dẫn tổng quan này
├── install-all.sh                    # Script cài đặt trọn gói 1 lệnh (macOS / Linux)
├── unified-search-mcp/               # Máy chủ MCP Unified Search Pool v2.0 (dùng cho Bộ 01)
│   ├── README.md                     # Hướng dẫn cài đặt đa nền tảng (macOS, Linux, Windows)
│   ├── .mcp_env.example              # Mẫu cấu hình biến môi trường (TAVILY/EXA/LINKUP Pool)
│   └── scripts/
│       ├── search_pool.py            # FastMCP Proxy 8 chế độ + xoay vòng Round-Robin + Failover
│       ├── setup_env.sh              # Trình cài đặt tự động trên macOS / Linux
│       └── setup_env.ps1             # Trình cài đặt tự động trên Windows PowerShell
├── skills/                           # 58 Kỹ năng phụ trợ (Companion Skills)
│   ├── tavily/                       # 8 kỹ năng tìm kiếm, cào dữ liệu & PTC Context Isolation (Bộ 01)
│   ├── akkit/                        # 19 kỹ năng AgentKit v2.x-4.x (Fable 5.1, Graphify, Orchestrate, Ship...)
│   └── gstack/                       # 31 kỹ năng GStack v1.91 (Scrape, Skillify, GBrain, Autoplan, QA, CSO...)
├── gstack-bin/                       # 21 tiện ích dòng lệnh (gstack-wtree, gstack-evidence, gstack-verify-gate...)
└── hooks/                            # 13 mô-đun kiểm định PR, bảo mật & ngôn ngữ (pr-body-contract.cjs...)
```

---

## 3. Bảng Ánh Xạ Công Cụ Theo Từng Bộ Phương Pháp

| Bộ Phương Pháp | Công cụ / Kỹ năng được sử dụng | Vị trí đóng gói trong `tools/` |
|---|---|---|
| **Bộ 01 · Tinh Lọc Thông Tin Internet (v2.0)** | - Máy chủ MCP `unified-search` (8 chế độ định tuyến đa tín hiệu)<br>- Bộ kỹ năng `tavily-search`, `tavily-map`, `tavily-extract`, `tavily-crawl`, `tavily-research`, `tavily-dynamic-search` (PTC)<br>- Trình duyệt chỉ đọc `gstack /scrape`, `/skillify`, `/setup-browser-cookies`<br>- Kỷ luật phân loại mệnh đề `ak-fable-thinking` | - `tools/unified-search-mcp/`<br>- `tools/skills/tavily/`<br>- `tools/skills/gstack/scrape/`, `skillify/`, `setup-browser-cookies/`<br>- `tools/skills/akkit/ak-fable-thinking/` |
| **Bộ 02 · Kernel Registry & Nguồn Sự Thật (v2.0)** | - Đồ thị tri thức tự động `ak-graphify`<br>- Bộ não lai Markdown + Vector `setup-gbrain`, `sync-gbrain`<br>- Khóa vùng chỉnh sửa & đặc tả `freeze`, `unfreeze`, `spec`<br>- Kiểm toán vân tay thư mục `gstack-wtree`, `gstack-diff-scope` | - `tools/skills/akkit/ak-graphify/`<br>- `tools/skills/gstack/setup-gbrain/`, `sync-gbrain/`<br>- `tools/skills/gstack/freeze/`, `unfreeze/`, `spec/`<br>- `tools/gstack-bin/gstack-wtree`, `gstack-diff-scope` |
| **Bộ 03 · Vibecode Kit (v6.1)** | - Sổ cái bằng chứng & cổng kiểm chứng `gstack-evidence`, `gstack-verify-gate`<br>- Cổng duyệt kế hoạch 4 góc nhìn `autoplan`, `plan-ceo-review`, `plan-eng-review`, `plan-design-review`, `plan-devex-review`<br>- Điều phối đa tiến trình & bàn giao `ak-orchestrate`, `ak-worktree`, `ak-handoff`, `gstack-redact`<br>- Kiểm thử, gỡ lỗi & bảo mật `qa`, `investigate`, `test-audit`, `cso`, `ak-debug`, `ak-test`, `ak-security`<br>- Phát hành & kiểm định hợp đồng PR `ak-ship`, `ak-review-pr`, `ship`, `land-and-deploy`, `canary`, `pr-body-contract.cjs` | - `tools/gstack-bin/`<br>- `tools/skills/gstack/`<br>- `tools/skills/akkit/`<br>- `tools/hooks/` |
