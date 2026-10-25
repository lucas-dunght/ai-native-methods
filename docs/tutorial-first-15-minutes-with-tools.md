# Bài Học Thực Hành (Tutorial) · 15 Phút Đầu Tiên Cài Đặt `tools/` & Chạy Truy Vấn Đa Tín Hiệu (`2026.10`)

Trong bài thực hành này, bạn sẽ đi từ một máy tính mới vừa tải kho lưu trữ `ai-native-methods` đến việc cài đặt hoàn chỉnh **3 Bộ Phương Pháp**, **58 kỹ năng phụ trợ (`Companion Skills`)**, nạp khóa API vào **`Unified Search Pool v2.0`** và nhìn thấy kết quả định tuyến đa tín hiệu hoạt động thực tế chỉ trong 3 bước đầu tiên.

---

## Những Gì Bạn Cần Chuẩn Bị (`What You'll Need`)

- Máy tính chạy macOS, Linux hoặc Windows (WSL2 / PowerShell).
- Đã cài đặt `git` và `python3` (phiên bản `3.10` trở lên).
- Ít nhất **1 khóa API miễn phí** từ `https://app.tavily.com` (nhận ngay 1.000 lượt tìm kiếm miễn phí/tháng không cần thẻ tín dụng).

---

## Bước 1 · Tải Kho Lưu Trữ & Chạy Trình Cài Đặt 1 Lệnh

Mở Terminal, tải kho lưu trữ về máy và chạy trình khởi tạo trọn gói `tools/install-all.sh`:

```bash
git clone https://github.com/lucas-dunght/ai-native-methods.git
cd ai-native-methods
chmod +x tools/install-all.sh
./tools/install-all.sh
```

**Kết quả hiển thị ngay trên màn hình:**
- Hệ thống tự động sao chép 3 Bộ Phương Pháp cốt lõi (`internet-info-refinement`, `kernel-registry-sot`, `vibecode-kit-v6`) và 58 kỹ năng phụ trợ vào `~/.gemini/config/skills/`.
- Hệ thống cài đặt 21 tiện ích `gstack-bin` và 13 `hooks` kiểm định.
- Hệ thống khởi tạo môi trường ảo Python tại `tools/unified-search-mcp/.venv/`, tạo file `~/.mcp_env` (quyền `0600`) và in ra đoạn cấu hình JSON dành riêng cho máy của bạn.

---

## Bước 2 · Nạp Khóa API Đầu Tiên Vào `~/.mcp_env` & Kiểm Tra Bảng Điều Khiển

Mở file `~/.mcp_env` vừa được tạo tự động và điền khóa Tavily (hoặc Exa, Linkup) của bạn vào:

```bash
cat << 'EOF' > ~/.mcp_env
# --- UNIFIED SEARCH KEY POOL ---
export TAVILY_KEY_POOL="<YOUR_TAVILY_API_KEY>"
export EXA_KEY_POOL=""
export LINKUP_KEY_POOL=""
EOF
chmod 600 ~/.mcp_env
```

Ngay lập tức, hãy kiểm tra bảng điều khiển trạng thái khóa bằng lệnh sau:

```bash
./tools/unified-search-mcp/.venv/bin/python -c '
import sys
sys.path.insert(0, "tools/unified-search-mcp/scripts")
import search_pool
print(search_pool.pool_status())
'
```

**Kết quả hiển thị ngay trên màn hình:**
```text
## Trạng thái Unified Search Key Pool v2.0 (Smart Multi-Signal Engine)
### 1. Tình trạng Kho API Key & Cân bằng tải (Round-Robin):
**Tavily** (Pháp lý VN, thời sự, dữ liệu thực tế, Q&A RAG): 1 key (1 khả dụng, 0 cooldown) | Con trỏ kế tiếp: **Key #1**
  - Key #1 (`tvly...xxxx`): ✅ Sẵn sàng [OK: 0 | Lỗi: 0] 🎯 *(Key kế tiếp)*
```

Bạn đã thấy khóa của mình được nạp thành công và tự động che các ký tự ở giữa (`tvly...xxxx`) để bảo mật!

---

## Bước 3 · Chạy Thử Bộ Định Tuyến Đa Tín Hiệu & Kiểm Chứng Cây Thư Mục

Hãy kiểm tra xem bộ định tuyến đa tín hiệu (`QueryRouter`) phân loại các câu hỏi thực tế của **Bộ 01** như thế nào và thử lấy dấu vân tay cây thư mục (`WTREE_FINGERPRINT`) của **Bộ 02 / Bộ 03**:

```bash
./tools/unified-search-mcp/.venv/bin/python -c '
import sys
sys.path.insert(0, "tools/unified-search-mcp/scripts")
from search_pool import QueryRouter

queries = [
    "Quy định mức đóng BHXH bắt buộc của công ty năm 2026",
    "arXiv paper on LLM multi-agent orchestration benchmark",
    "So sánh toàn diện kiến trúc RAG và Long-Context LLM"
]
for q in queries:
    order, label, _ = QueryRouter.route(q)
    print(f"Truy vấn: {q}\n  -> Định tuyến: {label} | Thứ tự ưu tiên: {order}\n")
'
```

**Kết quả hiển thị ngay trên màn hình:**
```text
Truy vấn: Quy định mức đóng BHXH bắt buộc của công ty năm 2026
  -> Định tuyến: Pháp lý & Quy định chính sách (Tavily #1 - Legal/Policy RAG) | Thứ tự ưu tiên: ['tavily', 'linkup', 'exa']

Truy vấn: arXiv paper on LLM multi-agent orchestration benchmark
  -> Định tuyến: Học thuật & Bài báo khoa học (Exa #1 - Research Paper) | Thứ tự ưu tiên: ['exa', 'linkup', 'tavily']

Truy vấn: So sánh toàn diện kiến trúc RAG và Long-Context LLM
  -> Định tuyến: Tổng hợp & Phân tích chuyên sâu (Linkup #1 - Deep Synthesis) | Thứ tự ưu tiên: ['linkup', 'exa', 'tavily']
```

Lưu ý ở câu truy vấn đầu tiên: mặc dù câu hỏi có chữ *"công ty"*, quy tắc chống bắt nhầm (`Anti-Hijacking`) đã giữ truy vấn ở nhánh **Pháp lý (`Tavily #1`)** thay vì đẩy nhầm sang nhánh Startup của Exa.

---

## Bước 4 · Kiểm Tra Công Cụ Quản Trị Vân Tay & Hợp Đồng PR (`Bộ 02 & Bộ 03`)

Chạy lệnh sau để thử tạo dấu vân tay cây thư mục (`gstack-wtree`) và kiểm tra bộ lọc bảo mật (`gstack-redact`):

```bash
echo "=== 1. Dấu vân tay cây thư mục hiện tại ==="
git rev-parse --short HEAD

echo "=== 2. Kiểm tra mô-đun ngôn ngữ viết PR ==="
node tools/hooks/writing-language.cjs --json
```

**Kết quả hiển thị:**
- Dòng 1 in ra mã băm commit hiện hành của nhánh `main`.
- Dòng 2 trả về cấu hình JSON `{"language":"en","source":"default","fallback":"none"}` xác nhận các mô-đun kiểm định Node.js trong `tools/hooks/` đã hoạt động hoàn hảo.

---

## Những Gì Bạn Vừa Thiết Lập Được (`What You Built`)

Chỉ sau 4 bước ngắn gọn, máy tính của bạn đã có sẵn một trạm làm việc AI-Native hoàn chỉnh:
1. **3 Bộ Phương Pháp (`2026.10`)** và **58 Companion Skills** đã được kích hoạt trong `~/.gemini/config/skills/`.
2. **Máy chủ MCP `unified-search` v2.0** đã kết nối với file khóa `~/.mcp_env` an toàn tuyệt đối (không bao giờ lọt khóa vào Git).
3. **Bộ công cụ dòng lệnh `gstack-bin` và `hooks`** đã sẵn sàng phục vụ quy trình kiểm chứng bằng chứng của **Bộ 02** và **Bộ 03**.

### Bước Tiếp Theo Khuyến Nghị
- Muốn thêm nhiều khóa để xoay vòng tải hoặc tích hợp thêm API mới (như Brave Search): đọc ngay [How to · Cách Thêm API Key Pool & Tích Hợp Nhà Cung Cấp API Mới](./how-to-configure-and-extend-api-tools.md).
- Muốn tra cứu chi tiết từng tham số hàm và biến môi trường: xem [Tham Chiếu Kỹ Thuật `tools/` & Cấu Hình API](./reference-tools-and-api-config.md).
- Muốn hiểu sâu lý do thiết kế kiến trúc: xem [Giải Thích Kiến Trúc Bộ Định Tuyến Đa Tín Hiệu & Xoay Vòng Khóa](./explanation-multi-signal-router-and-key-pool.md).
