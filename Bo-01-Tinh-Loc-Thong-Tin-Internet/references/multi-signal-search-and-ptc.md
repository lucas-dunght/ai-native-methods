# Giao thức Tìm kiếm Đa tín hiệu & Cô lập Ngữ cảnh PTC (`Multi-Signal Search & PTC Sandbox`)

Tài liệu này quy định cách AI Agent sử dụng hệ thống định tuyến tìm kiếm đa tín hiệu (`unified-search` MCP và họ công cụ `tavily-*`) kết hợp với kiến trúc cô lập ngữ cảnh kiểu **PTC (`Programmatic Tool Calling`)** ở Giai đoạn 2 của Bộ 01 v2.0.

## 1. Bảng Định tuyến Tìm kiếm Đa tín hiệu (`Multi-Signal Routing`)

Không dùng một lệnh tìm kiếm chung chung cho mọi câu hỏi. Agent phải phân tích bản chất thông tin cần thu thập để chọn đúng chế độ (`mode`) và công cụ.

| Bản chất thông tin cần thu thập | Chế độ `unified-search` (`mode`) | Công cụ bổ trợ (`tavily-*`) | Chiến lược lọc tín hiệu |
|---|---|---|---|
| Số liệu học thuật, bài báo khoa học, thống kê vĩ mô | `academic` | `tavily-search --include-domains` (`.edu`, `.gov`, `.org`) | Lọc lấy phần Methodology, Sample Size, kết quả định lượng và DOI |
| Văn bản pháp quy, nghị định, thông tư, tiêu chuẩn | `legal` | `tavily-extract --extract-depth advanced` | Giữ nguyên văn số hiệu điều khoản, ngày ban hành, ngày có hiệu lực |
| Doanh thu, báo cáo tài chính, hồ sơ công ty, đối thủ | `company` | `tavily-map` + `tavily-extract` | Lọc các dòng có đơn vị tiền tệ, tỷ lệ phần trăm, bảng giá, tên gói sản phẩm |
| Sự kiện mới diễn ra, biến động thị trường, thông cáo | `news` | `tavily-search --time-range month` | Ưu tiên truy tìm đường dẫn nguồn gốc (`primary_origin_url`) được bài báo nhắc tới |
| Tài liệu kỹ thuật, mã nguồn, thông số kiến trúc | `code` | `tavily-crawl --instructions` | Lọc lấy bảng thông số giới hạn hệ thống, cấu trúc API và benchmark |
| Tổng quan đa chiều cho lĩnh vực mới hoặc so sánh sâu | `deep` hoặc `hybrid` | `tavily-research --model pro` | Dùng báo cáo tổng hợp làm bản đồ chỉ dẫn để đi trích từng nguồn gốc độc lập |

Quy tắc vận hành.
- Luôn ưu tiên gọi qua `unified-search` (`web_search`, `web_extract`, `pool_status`) để tận dụng bộ định tuyến tự động và cơ chế xoay vòng cân bằng tải đa khóa API (`Tavily` + `Exa` + `Linkup`).
- Không gọi trực tiếp một API đơn lẻ khi hệ thống định tuyến chung đang sẵn sàng.

## 2. Kiến trúc Cô lập Ngữ cảnh kiểu PTC (`Programmatic Tool Calling Sandbox`)

### Tại sao phải cô lập ngữ cảnh?

Một lần tìm kiếm 8 kết quả kèm toàn văn trang web (`raw_content`) trả về trung bình từ 250.000 đến 400.000 ký tự (chứa đầy thanh điều hướng, chân trang, quảng cáo và mã kịch bản). Nếu nạp thẳng khối dữ liệu này vào ngữ cảnh của Agent, chất lượng trích xuất `Fact Card` sẽ suy giảm nghiêm trọng do nhiễu.

### Quy trình 3 bước `Save -> Triage -> Targeted Extract` (Qua CLI `scripts/bo01_refine_tool.py`)

**Bước 0 · Thực thi 1 Lệnh qua Công cụ CLI Chuẩn (`Recommended Deep Module Lever`).**
Thay vì tự viết lại script lọc văn bản ở mỗi lượt tìm kiếm, lưu kết quả tìm kiếm thô vào `/tmp/bo01_search_raw.json` rồi chạy trực tiếp lệnh `ptc-filter`:

```bash
python3 Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py ptc-filter \
  --input /tmp/bo01_search_raw.json \
  --keywords "tăng trưởng,2025,2026,tỷ USD,%" \
  --window-chars 600 \
  --max-snippets 3 \
  --output /tmp/bo01_search_filtered.json \
  --json
```

**Bước 1 · Tìm kiếm và Lưu xuống Đĩa (`Turn 1 · Search & Triage`).**
Lưu toàn bộ kết quả thô vào `/tmp/bo01_search_raw.json` hoặc `raw-sources/`. Chỉ in ra màn hình tiêu đề, URL, điểm số (`score`) và 150 ký tự tóm tắt để đánh giá.

```bash
python3 << 'PYEOF'
import json

# Đọc từ file kết quả tìm kiếm thô trên đĩa, không in toàn văn ra context
with open('/tmp/bo01_search_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = data.get('results', [])
print(f"Đã lưu {len(results)} kết quả vào /tmp/bo01_search_raw.json\n")
for idx, r in enumerate(results):
    score = r.get('score', 0.0)
    title = r.get('title', '')[:90]
    url = r.get('url', '')
    snippet = (r.get('content', '') or '')[:160].replace('\n', ' ')
    print(f"[{idx}] [score={score:.2f}] {title}")
    print(f"    URL: {url}")
    print(f"    Tóm tắt: {snippet}\n")
PYEOF
```

**Bước 2 · Lọc Đoạn văn Có Tín hiệu (`Turn 2 · Signal Filtering`).**
Sau khi chọn được các chỉ mục nguồn chất lượng cao (ví dụ nguồn `[0]`, `[2]`, `[4]`), viết đoạn lọc Python chỉ lấy những đoạn văn có độ dài hợp lệ và chứa từ khóa mục tiêu hoặc con số định lượng.

```bash
python3 << 'PYEOF'
import json

with open('/tmp/bo01_search_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keywords = ['gmv', 'billion', 'tỷ', 'tăng trưởng', '2024', '2025', 'market share']
selected_indices = [0, 2]

for idx in selected_indices:
    if idx >= len(data.get('results', [])):
        continue
    r = data['results'][idx]
    raw = r.get('raw_content') or r.get('content') or ''
    print("--- BEGIN UNTRUSTED EXTERNAL CONTENT ---")
    print(f"SOURCE_INDEX: {idx} | TITLE: {r.get('title')} | URL: {r.get('url')}")
    for para in raw.split('\n\n'):
        clean = para.strip()
        if len(clean) >= 60 and any(kw in clean.lower() for kw in keywords):
            print(f"  {clean}\n")
    print("--- END UNTRUSTED EXTERNAL CONTENT ---\n")
PYEOF
```

**Bước 3 · Chuỗi 5 công cụ mở rộng khi cần đào sâu (`Search -> Map -> Extract -> Crawl -> Research`).**
- Dùng `search` để tìm trang chủ của tổ chức hoặc báo cáo.
- Dùng `map` để liệt kê toàn bộ đường dẫn con trên domain đó mà không tốn băng thông tải nội dung.
- Dùng `extract` cho tối đa 20 URL quan trọng nhất vừa tìm được từ `map`.
- Dùng `crawl` kèm tham số `instructions` khi cần quét toàn bộ một chuyên mục tài liệu hoặc văn bản pháp quy.
- Dùng `research` khi cần bản tổng hợp đối chiếu đa chiều để rà soát xem còn góc khuất nào chưa thu thập.
