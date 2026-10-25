# Architecture · Kiến trúc kỹ thuật của Bộ 01 (v2.0 · 2026.10)

## Tổng quan

Kiến trúc kỹ thuật của Bộ 01 v2.0 gồm sáu module kết nối tuần tự qua các tệp dữ liệu văn bản chuẩn (`CSV`, `YAML`, `Markdown`) và một vùng đệm cô lập ngữ cảnh (`PTC Sandbox`). Các cổng kiểm duyệt của con người (`Human Checkpoints`) được đặt tại những điểm ra quyết định chiến lược thông qua thẻ **Decision Brief `D<N>`**.

Toàn bộ đường ống có thể vận hành linh hoạt ở hai chế độ. Chế độ tương tác bán tự động (dành cho sinh viên và nhà nghiên cứu chạy các chu kỳ đầu) và chế độ điều phối bằng script kết hợp AI Agent (dành cho dự án quy mô lớn cần thu thập hàng trăm nguồn và chuyển giao tự động sang Bộ 02).

## Sơ đồ luồng kiến trúc (v2.0)

```
Brief nghiên cứu (brief.md · Cổng D1)
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ 1. Multi-Signal Source Collector & PTC Sandbox                │
│    - unified-search (auto/academic/legal/news/company/deep)   │
│    - tavily (search/map/extract/crawl/research)               │
│    - gstack /scrape + /skillify (trang cần phiên đăng nhập)   │
│    - Lọc nhiễu qua /tmp/ & bọc rào UNTRUSTED WEB CONTENT      │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
             source-log.csv + raw-sources/ (kèm primary_origin_url)
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 2. Atomic Fact Extractor (Fable 5.1 Claim Discipline)         │
│    - Tách sự thật nguyên tử + exact_quote + content_hash      │
│    - Gắn nhãn OBSERVED | DERIVED | PRIOR | ASSUMED            │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
                    fact-cards/F-YYYY-NNN.yaml (raw)
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 3. Echo-Chamber & Conflict Detector                           │
│    - Gộp thẻ trùng + Tính independent_origin_count            │
│    - Sinh thẻ Decision Brief D<N> vào conflict-queue.md       │
└───────────────────────────────┬───────────────────────────────┘
                                │
         ◄── [Human Checkpoint: Phán xử Conflict Queue D<N>]
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 4. Gap Analyzer & Trust Classifier                            │
│    - Sinh gap-checklist.md kèm query bù đắp                   │
│    - Gán nhãn verified / probable / unverified cơ học         │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 5. 4D Enrichment Pass & Bộ 02 ETL Exporter                    │
│    - Đối chiếu chéo, phân loại, độ tươi, đánh dấu xuất L1     │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 6. Constraint Loop Verifier & Synthesizer                     │
│    - Kiểm tra 4 ngưỡng định lượng & khớp 100% mã [F-YYYY-NNN] │
│    - Xuất report-final.md + gói Fact Cards chuẩn              │
└───────────────────────────────────────────────────────────────┘
```

## Thành phần 1 · Multi-Signal Source Collector & PTC Sandbox

Chịu trách nhiệm định tuyến truy vấn, thu thập dữ liệu từ web, lọc nhiễu ngoài ngữ cảnh và ghi nhật ký nguồn kèm dấu vết nguồn gốc đầu tiên.

### Đầu vào

File `brief.md` chứa câu hỏi nghiên cứu, phạm vi thời gian và địa lý, danh sách tên miền ưu tiên hoặc loại trừ.

### Cơ chế Định tuyến Đa Tín hiệu (`Multi-Signal Routing`)

Thay vì dùng một công cụ tìm kiếm đơn lẻ, module này chọn công cụ theo tín hiệu truy vấn.
- **Tin tức, tài chính, pháp lý, học thuật đa nguồn.** Gọi MCP `unified-search` (`web_search` với `mode` tương ứng gồm `news`, `legal`, `academic`, `company`, `code`, `deep`, `hybrid` và `web_extract`) để tận dụng bộ xoay vòng 18 khóa API qua ba công cụ `Tavily`, `Exa` và `Linkup`.
- **Khám phá cấu trúc và cào toàn bộ chuyên mục tài liệu.** Dùng `tavily-map` để lấy danh sách URL và `tavily-crawl` / `tavily-extract` để bóc tách nội dung Markdown sạch.
- **Báo cáo tổng quan đa góc nhìn.** Dùng `tavily-research` (`--model pro`) để lấy khung tham chiếu ban đầu, sau đó bóc tách từng nguồn được trích dẫn.
- **Trang yêu cầu đăng nhập hoặc ứng dụng web động.** Dùng `gstack /scrape` qua trình duyệt phiên thật (hoặc headless browser kèm `/setup-browser-cookies`). Nếu một trang bảng giá hoặc cổng dữ liệu cần lấy định kỳ, dùng `/skillify` để biên dịch thành kỹ năng trình duyệt chạy trong 200ms.

### Cơ chế Cô lập Ngữ cảnh PTC (`Programmatic Tool Calling`)

Mọi kết quả tìm kiếm có kèm nội dung trang (`raw_content`) bắt buộc phải ghi ra tệp tạm trong `/tmp/` hoặc `raw-sources/` và xử lý bằng script Python. Chỉ kết quả đã lọc (tiêu đề, URL, điểm số và các đoạn văn khớp từ khóa hoặc chứa số liệu) mới được in ra `stdout` để đưa vào ngữ cảnh của Agent. Toàn bộ nội dung trích xuất từ web phải được đặt trong cặp thẻ cảnh báo `--- BEGIN UNTRUSTED EXTERNAL CONTENT ---` và `--- END UNTRUSTED EXTERNAL CONTENT ---`.

### Đầu ra · `source-log.csv`

```csv
source_id,url,primary_origin_url,title,date_published,date_collected,query_used,search_mode,extraction_method,source_type,language,authority_tier,raw_snapshot_path,collection_reason
S001,https://economysea.withgoogle.com/report,https://economysea.withgoogle.com/report,"e-Conomy SEA 2024",2024-11-05,2026-10-25,"Southeast Asia digital payments GMV 2024",company,unified-extract,tài liệu doanh nghiệp,en,tier-1,raw-sources/S001.md,"Báo cáo gốc đo lường quy mô GMV khu vực"
S002,https://technewspaper.example/sea-gmv,https://economysea.withgoogle.com/report,"SEA Digital Economy Hits New High",2024-11-07,2026-10-25,"SEA fintech growth 2024",news,ptc-search,báo chí,en,tier-2,raw-sources/S002.md,"Bài báo phân tích lại báo cáo e-Conomy SEA"
```

Trường `primary_origin_url` là chìa khóa để phát hiện hiện tượng phòng vang. Ở ví dụ trên, dù `S001` và `S002` là hai URL khác nhau nhưng cùng trỏ về một `primary_origin_url`, do đó hệ thống tự động nhận diện chúng chỉ là `1 datum`.

## Thành phần 2 · Atomic Fact Extractor (Kỷ luật Nhận định Fable 5.1)

Đọc từng đoạn văn bản đã lọc từ `raw-sources/` và chuyển hóa thành các thẻ sự thật nguyên tử (`Fact Cards`).

### Đầu ra · Schema `fact-cards/F-YYYY-NNN.yaml`

```yaml
fact_id: F-2026-001
content: "Thị trường thanh toán số Đông Nam Á đạt tổng giá trị giao dịch 114 tỷ USD trong năm 2024"
exact_quote: "Southeast Asia digital payments GMV reached US$114B in 2024"
content_hash: "sha256:8f3c2a1b"
claim_label: OBSERVED
sources:
  - S001
  - S002
primary_origins:
  - "https://economysea.withgoogle.com/report"
independent_origin_count: 1
fact_type: numerical-claim
domain: digital-payments
role: evidence-for-thesis-1
date_extracted: 2026-10-25
extracted_by: agent
notes: "S002 trích dẫn lại S001 nên independent_origin_count = 1"
```

Các quy tắc bảo toàn dữ liệu.
- `claim_label` nhận một trong bốn giá trị `OBSERVED`, `DERIVED`, `PRIOR`, `ASSUMED`.
- `exact_quote` giữ nguyên văn câu gốc trong tài liệu nguồn để kiểm toán viên hoặc script có thể đối chiếu tức thì.
- `content_hash` là 8 ký tự đầu của mã băm SHA-256 tính trên chuỗi `content + exact_quote`, giúp phát hiện nếu nội dung thẻ bị sửa đổi ngoài ý muốn ở các bước sau.

## Thành phần 3 · Echo-Chamber & Conflict Detector

Quét toàn bộ thư mục `fact-cards/` để gộp các thẻ trùng, tính số lượng nguồn gốc độc lập và lập hàng đợi xung đột.

### Logic xử lý

1. **Tính `independent_origin_count`.** Với mỗi thẻ, tập hợp toàn bộ `primary_origin_url` từ các nguồn trong danh sách `sources`. Số phần tử duy nhất (`unique set size`) của tập `primary_origin_url` chính là `independent_origin_count`.
2. **Gộp trùng (`Merge`).** Hai thẻ cùng chỉ số, cùng kỳ thời gian và cùng giá trị thì gộp `sources` và tính lại `independent_origin_count`.
3. **Đóng gói Xung đột theo chuẩn `Decision Brief D<N>`.** Khi hai thẻ cùng chỉ số và kỳ thời gian nhưng lệch giá trị, xuất vào `conflict-queue.md` theo cấu trúc thẻ quyết định `D<N>` để con người phê duyệt.

## Thành phần 4 · Gap Analyzer & Trust Classifier

### Bộ phân tích lỗ hổng (`Gap Analyzer`)

Quét tìm các thẻ mang nhãn `ASSUMED` hoặc `PRIOR`, các chuỗi số liệu bị khuyết năm hoặc khuyết quốc gia trong phạm vi `brief.md`, sau đó xuất ra `gap-checklist.md` kèm cấu hình truy vấn bù đắp (`suggested_query`, `search_mode`, `target_tier`).

### Bộ phân hạng tin cậy tất định (`Deterministic Trust Classifier`)

Áp dụng hàm phân loại cơ học không phụ thuộc cảm tính của mô hình.

```python
def classify_trust_tier(card, source_map):
    if card["claim_label"] in ("PRIOR", "ASSUMED"):
        return "unverified"
    tiers = [source_map[s]["authority_tier"] for s in card["sources"]]
    indep_count = card.get("independent_origin_count", 0)
    if indep_count >= 2 and any(t in ("tier-1", "tier-2") for t in tiers):
        return "verified"
    if indep_count == 1 and "tier-1" in tiers:
        return "verified"
    if indep_count >= 1 and any(t in ("tier-1", "tier-2") for t in tiers):
        return "probable"
    return "unverified"
```

Lưu ý. Trong trường hợp nguồn `tier-1` chỉ là một bài báo kinh tế điểm tin chứ không phải báo cáo nghiên cứu gốc hoặc số liệu thống kê chính thức, người dùng có thể cấu hình hạ mức `indep_count == 1` của báo chí xuống `probable` để ép buộc phải có nguồn độc lập thứ hai mới đạt `verified`.

## Thành phần 5 · 4D Enrichment Pass & Bộ 02 ETL Exporter

Bổ sung khối `enrichment` vào từng thẻ sự thật đã phân hạng và chuẩn bị gói dữ liệu xuất sang Bộ 02 (`Kernel Registry`).

```yaml
trust_tier: verified
enrichment:
  cross_references: [F-2026-005, F-2026-012]
  classification: [market-sizing, sea-fintech]
  recency_status: current
  importance_rank: high
  gaps_implied: [G-002]
  bo02_bridge:
    export_ready: true
    target_layer: L1
    suggested_fact_id: L1-sea-digital-payments-gmv-2024
    unit: USD
    numeric_value: 114000000000
```

## Thành phần 6 · Constraint Loop Verifier & Synthesizer

Trước khi sinh báo cáo cuối (`report-final.md`), chạy script kiểm chứng `Constraint Loop`.

```python
# Kiểm tra tự động 4 điều kiện hoàn thành của Bộ 01 v2.0
assert verified_ratio >= 0.40, "Tỷ lệ thẻ verified chưa đạt 40%"
assert unresolved_conflicts == 0, "Còn xung đột chưa được con người phán xử trong conflict-queue.md"
assert high_priority_open_gaps < 10, "Còn từ 10 lỗ hổng mức cao trở lên chưa đóng"
assert missing_citation_ids == set(), f"Báo cáo trích dẫn mã thẻ không tồn tại: {missing_citation_ids}"
```

Sau khi vượt qua cổng kiểm tra, `Synthesizer` xuất `report-final.md` gồm đúng 3 phần tách biệt và bảng danh mục tài liệu tham chiếu tự động kết xuất từ `source-log.csv`.

## Cấu trúc thư mục của một chu kỳ nghiên cứu

```
research-cycle-YYYY-MM-DD/
├── brief.md                       (Giai đoạn 1 · Đã khóa qua cổng D1)
├── source-log.csv                 (Giai đoạn 2 · Kèm primary_origin_url & search_mode)
├── raw-sources/                   (Giai đoạn 2 · Bản lưu Markdown/JSON đã lọc PTC)
│   ├── S001.md
│   └── S002.md
├── fact-cards/                    (Giai đoạn 3 đến 6 · Thẻ sự thật nguyên tử YAML)
│   ├── F-2026-001.yaml
│   └── F-2026-002.yaml
├── conflict-queue.md              (Giai đoạn 4 · Các thẻ Decision Brief D<N> đã phán xử)
├── gap-checklist.md               (Giai đoạn 5 · Danh sách lỗ hổng & query bù đắp)
├── enrichment-log.md              (Giai đoạn 6 · Nhật ký làm giàu & cầu nối Bộ 02)
└── report-final.md                (Giai đoạn 7 · Báo cáo 3 phần đã qua Constraint Loop)
```

## Tích hợp liên thông với Bộ 02 và Bộ 03

- **Nối sang Bộ 02 (`Kernel Registry SOT`).** Mọi thẻ `Fact Card` có `trust_tier: verified` và `bo02_bridge.export_ready: true` được chuyển thẳng thành tệp `registry/stored-facts/L1-*.yaml` trong Bộ 02, giữ nguyên mã băm `content_hash` và đường dẫn nguồn.
- **Nối sang Bộ 03 (`Vibecode Kit v6.1`).** Khi xây dựng sản phẩm phần mềm ở Bộ 03, Chủ thầu (`Contractor`) đính kèm các mã thẻ `[F-YYYY-NNN]` vào tài liệu `RRI`, `Blueprint` và gói giao việc `TIP` để Thợ (`Builder`) thi công dựa trên dữ liệu thị trường và quy định đã được kiểm chứng.
