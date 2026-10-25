# Quick Start · Bộ 01 v2.0 trong 10 phút

Hướng dẫn này giúp bạn chạy trọn vẹn một vòng lặp tinh lọc thông tin v2.0 (tích hợp tìm kiếm đa tín hiệu, cô lập ngữ cảnh PTC, kiểm tra phòng vang và cổng định lượng) trên một bài toán nhỏ chỉ trong 10 phút.

## Bài toán mẫu

Bạn cần nghiên cứu nhanh quy mô và tốc độ tăng trưởng của thị trường giáo dục trực tuyến (`EdTech`) tại Đông Nam Á giai đoạn 2023 đến 2025 để làm dữ liệu đầu vào cho buổi thuyết trình dự án khởi nghiệp.

## Phút 0 đến 2 · Khởi tạo thư mục và viết Brief (`Giai đoạn 1`)

Tạo cấu trúc thư mục cho chu kỳ nghiên cứu và mở file `brief.md`.

```bash
mkdir -p research-cycle-edtech/{raw-sources,fact-cards}
```

Điền bốn phần bắt buộc vào `research-cycle-edtech/brief.md`.

```markdown
# Brief nghiên cứu · EdTech Đông Nam Á 2023-2025

## 1. Câu hỏi nghiên cứu và Quyết định phụ thuộc
Quy mô thị trường và động lực tăng trưởng chính của EdTech Đông Nam Á giai đoạn 2023-2025 là gì? Kết quả dùng để chốt phân khúc khách hàng mục tiêu cho dự án MVP.

## 2. Phạm vi dữ liệu
- Thời gian. 2023 đến 2025.
- Địa lý. 6 nước ASEAN chính gồm Singapore, Việt Nam, Indonesia, Thái Lan, Malaysia, Philippines.
- Phân khúc. K-12 và đào tạo kỹ năng nghề nghiệp (upskilling).

## 3. Tiêu chí loại trừ và Tên miền ưu tiên
- Loại trừ các bài viết quảng cáo khóa học không nêu nguồn khảo sát và bài viết không có ngày công bố.
- Ưu tiên báo cáo từ tổ chức quốc tế, cơ quan chính phủ và hãng nghiên cứu thị trường.

## 4. Ngưỡng đầu ra mục tiêu
- Tối thiểu 3 thẻ sự thật nguyên tử, kiểm tra rõ nguồn gốc độc lập (`primary_origin_url`).
```

## Phút 2 đến 5 · Thu thập Đa tín hiệu và Lọc Cô lập PTC (`Giai đoạn 2`)

Thay vì đổ toàn bộ trang web thô vào khung chat, dùng `unified-search` hoặc `tavily` kết hợp bộ lọc Python để lưu bản thô vào `/tmp/` và chỉ in ra các dòng chứa số liệu.

```bash
python3 << 'PYEOF'
# Ví dụ minh họa lọc dữ liệu theo chuẩn PTC (Programmatic Tool Calling)
sample_results = [
    {
        "source_id": "S001",
        "url": "https://sea-research.example.org/edtech-2024",
        "primary_origin_url": "https://sea-research.example.org/edtech-2024",
        "title": "ASEAN EdTech Market Report 2024",
        "authority_tier": "tier-1",
        "snippet": "ASEAN EdTech market reached USD 6.7 billion in 2023 and is projected to grow 16% annually."
    },
    {
        "source_id": "S002",
        "url": "https://vn-technews.example.com/edtech-boom",
        "primary_origin_url": "https://sea-research.example.org/edtech-2024",
        "title": "EdTech Đông Nam Á chạm mốc 6.7 tỷ USD",
        "authority_tier": "tier-2",
        "snippet": "Theo báo cáo ASEAN EdTech Market Report 2024, quy mô thị trường đạt 6.7 tỷ USD năm 2023."
    },
    {
        "source_id": "S003",
        "url": "https://moe-sg.example.gov.sg/ai-in-schools-2024",
        "primary_origin_url": "https://moe-sg.example.gov.sg/ai-in-schools-2024",
        "title": "AI Adaptive Learning in Public Schools",
        "authority_tier": "tier-1",
        "snippet": "Singapore deployed AI adaptive grading across 28 public secondary schools in 2024."
    }
]
for r in sample_results:
    print(f"[{r['source_id']}] ({r['authority_tier']}) {r['title']}")
    print(f"  URL: {r['url']} | Gốc: {r['primary_origin_url']}")
    print(f"  Trích đoạn: {r['snippet']}\n")
PYEOF
```

Ghi 3 nguồn này vào `research-cycle-edtech/source-log.csv`. Chú ý rằng `S002` dẫn lại báo cáo của `S001`, nên cả hai có chung `primary_origin_url`.

```csv
source_id,url,primary_origin_url,title,date_published,date_collected,query_used,search_mode,extraction_method,source_type,language,authority_tier,raw_snapshot_path,collection_reason
S001,https://sea-research.example.org/edtech-2024,https://sea-research.example.org/edtech-2024,"ASEAN EdTech Market Report 2024",2024-09-15,2026-10-25,"ASEAN EdTech market size 2023 2024",company,unified-search,báo cáo nghiên cứu,en,tier-1,raw-sources/S001.md,"Số liệu gốc quy mô thị trường ĐNA"
S002,https://vn-technews.example.com/edtech-boom,https://sea-research.example.org/edtech-2024,"EdTech Đông Nam Á chạm mốc 6.7 tỷ USD",2024-09-20,2026-10-25,"quy mô thị trường edtech Đông Nam Á",news,ptc-filter,báo chí,vi,tier-2,raw-sources/S002.md,"Bài báo tiếng Việt dẫn lại S001"
S003,https://moe-sg.example.gov.sg/ai-in-schools-2024,https://moe-sg.example.gov.sg/ai-in-schools-2024,"AI Adaptive Learning in Public Schools",2024-10-02,2026-10-25,"Singapore AI education public schools 2024",academic,unified-extract,dữ liệu chính phủ,en,tier-1,raw-sources/S003.md,"Báo cáo chính thức của Bộ Giáo dục Singapore"
```

## Phút 5 đến 7 · Trích Fact Cards kèm Nhãn Fable 5.1 & Khử Phòng vang (`Giai đoạn 3 & 4`)

Tạo 2 file thẻ sự thật trong `research-cycle-edtech/fact-cards/`.

File `fact-cards/F-2026-001.yaml`.

```yaml
fact_id: F-2026-001
content: "Thị trường EdTech Đông Nam Á đạt quy mô 6.7 tỷ USD trong năm 2023"
exact_quote: "ASEAN EdTech market reached USD 6.7 billion in 2023"
content_hash: "sha256:4a91e0c2"
claim_label: OBSERVED
sources: [S001, S002]
primary_origins: ["https://sea-research.example.org/edtech-2024"]
independent_origin_count: 1
fact_type: numerical-claim
domain: market-size
role: evidence-thesis-1
date_extracted: 2026-10-25
extracted_by: agent
trust_tier: probable
notes: "Dù có 2 bài viết (S001 và S002) nhưng S002 dẫn lại S001 nên chỉ tính là 1 nguồn gốc độc lập. Xếp hạng probable cho tới khi có nguồn độc lập thứ hai."
```

File `fact-cards/F-2026-002.yaml`.

```yaml
fact_id: F-2026-002
content: "Singapore triển khai hệ thống AI chấm bài và học tập thích ứng tại 28 trường trung học công lập trong năm 2024"
exact_quote: "Singapore deployed AI adaptive grading across 28 public secondary schools in 2024."
content_hash: "sha256:9c72b4d1"
claim_label: OBSERVED
sources: [S003]
primary_origins: ["https://moe-sg.example.gov.sg/ai-in-schools-2024"]
independent_origin_count: 1
fact_type: event
domain: ai-adoption
role: evidence-thesis-2
date_extracted: 2026-10-25
extracted_by: agent
trust_tier: verified
notes: "Nguồn công bố trực tiếp từ cơ quan chính phủ (tier-1 chính thức) nên đạt chuẩn verified."
```

Nhờ quy tắc kiểm tra phòng vang (`Echo-Chamber Check`), bạn tránh được cái bẫy ngộ nhận rằng con số `6.7 tỷ USD` đã được hai nguồn độc lập xác nhận!

## Phút 7 đến 8 · Ghi nhận Lỗ hổng (`Giai đoạn 5 & 6`)

Tạo file `research-cycle-edtech/gap-checklist.md` để ghi lại những gì cần thu thập tiếp ở vòng sau.

```markdown
# Gap Checklist · EdTech ĐNA

## Gap G-001
- Mô tả. Thẻ F-2026-001 (quy mô 6.7 tỷ USD) mới chỉ có 1 nguồn gốc độc lập (`independent_origin_count = 1`).
- Hành động đề xuất. Tìm thêm một báo cáo độc lập từ Google/Temasek/Bain hoặc Bộ Kế hoạch Đầu tư để đối chiếu chéo.
- Truy vấn gợi ý. `mode: company`, query: `"Southeast Asia edtech market size 2023" -site:sea-research.example.org`
- Độ ưu tiên. high
```

## Phút 8 đến 10 · Kiểm tra Constraint Loop và Xuất Báo cáo (`Giai đoạn 7`)

Tạo file `research-cycle-edtech/report-final.md` theo đúng cấu trúc 3 phần.

```markdown
# Báo cáo · Xu hướng EdTech Đông Nam Á 2023-2025 (Cycle 1)

## 1. Kết luận cốt lõi (Verified Facts)
Singapore đang dẫn đầu khu vực về đưa AI vào trường công lập, với 28 trường trung học công lập đã triển khai hệ thống chấm bài và học tập thích ứng bằng AI trong năm 2024 [F-2026-002].

## 2. Giả thuyết cần kiểm chứng thêm (Probable Facts)
Quy mô thị trường EdTech Đông Nam Á ước đạt 6.7 tỷ USD trong năm 2023 [F-2026-001]. Dù xuất hiện trên nhiều mặt báo, số liệu này hiện bắt nguồn từ một báo cáo gốc duy nhất nên cần thêm một nguồn độc lập thứ hai để xác nhận.

## 3. Câu hỏi mở và Lỗ hổng dữ liệu (Open Gaps)
- Cần thu thập nguồn độc lập thứ hai cho quy mô thị trường 6.7 tỷ USD (Gap G-001).
- Chưa có thẻ sự thật chi tiết về phân khúc đào tạo kỹ năng nghề nghiệp (upskilling) tại Việt Nam và Indonesia.
```

## Hoàn tất Cycle 1 và Bước tiếp theo

Chỉ trong 10 phút, bạn đã nắm được toàn bộ tinh thần của Bộ 01 v2.0.
- Tách bạch rõ tín hiệu với nhiễu qua lọc PTC.
- Phát hiện được bài báo chép lại nguồn gốc nhờ `primary_origin_url`.
- Tách biệt rạch ròi sự thật đã xác minh (`verified`) với giả thuyết (`probable`) và lỗ hổng (`gaps`).

Khi áp dụng vào dự án thật, hãy đọc `Methodology.md`, `Architecture.md` và 3 file giao thức trong `references/` để khai thác tối đa sức mạnh của bộ công cụ.
