# Architecture · Kiến trúc Hệ thống Tinh lọc Thông tin (`v2.1 · Full-Stack 4 Lớp`)

## Sơ đồ Luồng dữ liệu, Phân tầng `R0–R3` và 5 Cổng kiểm soát

```text
               [YÊU CẦU NGHIÊN CỨU BAN ĐẦU CỦA NGƯỜI DÙNG]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1 · PHÂN TẦNG R0-R3, INDIRECT PROMPTING RESTATE & BRIEF       │
│ - Phân loại bài toán vào R0 (<5 nguồn), R1 (5-12), R2 (12-30), R3 (>30) │
│ - Indirect Prompting Restate: Agent tự diễn giải lại mục tiêu & loại trừ│
│ - Khóa 4 phần trong brief.md (trình thẻ Decision Brief D1 nếu R2/R3)    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                     [CỔNG 1 · BRIEF & D1 LOCKED]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2 · THU THẬP ĐA TÍN HIỆU & CÔ LẬP NGỮ CẢNH PTC               │
│ - unified-search / tavily-* / gstack /scrape (read-only)                │
│ - Chạy CLI: python3 scripts/bo01_refine_tool.py ptc-filter              │
│   (Cắt cửa sổ ~1.200 ký tự, lọc >80% rác HTML, gắn cờ UNTRUSTED)        │
│ - Ghi nhật ký source-log.csv (lưu rõ primary_origin_url)                │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                 [CỔNG 2 · PTC ISOLATION & ANTI-INJECTION]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 3 · TRÍCH XUẤT SỰ THẬT NGUYÊN TỬ (4 NHÃN FABLE 5.1)           │
│ - Tách từng khẳng định độc lập -> fact-cards/F-YYYY-NNN.yaml            │
│ - Lưu exact_quote, content_hash và gắn nhãn OBSERVED/DERIVED/PRIOR/ASSUMED│
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 4 · KHỬ TRÙNG LẶP, ĐỒ THỊ NGUỒN GỐC & HÀNG ĐỢI XUNG ĐỘT      │
│ - Chạy CLI: python3 scripts/bo01_refine_tool.py audit-echo              │
│   (Đếm independent_origin_count từ primary_origin_url, khử phòng vang)  │
│ - Đưa mọi mâu thuẫn số liệu/nhận định vào conflict-queue.md (Thẻ D<N>)  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
               [CỔNG 3 & 4 · ECHO-CHAMBER & CONFLICT GATE D<N>]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 5 & 6 · PHÁT HIỆN LỖ HỔNG, PHÂN HẠNG & LÀM GIÀU 4 CHIỀU      │
│ - Sinh gap-checklist.md kèm câu lệnh truy vấn bù đắp                    │
│ - Phân hạng verified / probable / unverified + khối enrichment          │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                 [CỔNG 5 · CONSTRAINT LOOP GATE (gate-check)]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 7 · BÁO CÁO 3 PHẦN & CẦU NỐI LIÊN THÔNG SANG BỘ 02 / BỘ 03   │
│ - Chạy CLI: python3 scripts/bo01_refine_tool.py gate-check --json       │
│ - Xuất report-final.md (Verified / Probable / Open Gaps)                │
│ - Chạy CLI: python3 scripts/bo01_refine_tool.py export-bo02 --json      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Cấu trúc Thư mục của một Chu kỳ Nghiên cứu (`Research Cycle Workspace`)

Mỗi bài toán nghiên cứu được tổ chức trong một thư mục độc lập để toàn bộ trạng thái nằm trên đĩa và có thể chạy qua nhiều vòng (`Cycle 1`, `Cycle 2`...) mà không phụ thuộc bộ nhớ tạm của khung chat.

```text
research-cycle-YYYY-MM-topic/
├── brief.md                        ← Giai đoạn 1: R0-R3, Indirect Prompting Restate & 4 phần cốt lõi
├── source-log.csv                  ← Giai đoạn 2: Nhật ký nguồn thu thập có cột primary_origin_url
├── raw-sources/                    ← Giai đoạn 2: Bản chụp văn bản đã lọc PTC từ từng nguồn
│   ├── S001.md
│   └── S002.md
├── fact-cards/                     ← Giai đoạn 3 & 6: Kho thẻ sự thật nguyên tử (1 sự thật = 1 file YAML)
│   ├── F-2026-001.yaml
│   └── F-2026-002.yaml
├── conflict-queue.md               ← Giai đoạn 4: Danh sách xung đột và các thẻ quyết định D<N>
├── gap-checklist.md                ← Giai đoạn 5: Danh sách lỗ hổng kèm câu lệnh truy vấn bù đắp
└── report-final.md                 ← Giai đoạn 7: Báo cáo xuất bản 3 phần kèm bảng đối chiếu nguồn
```

## Định dạng Dữ liệu Chuẩn của từng Tạo phẩm (`Data Schemas`)

### 1. Tệp `brief.md` (Bốn phần bắt buộc + `Indirect Prompting Restate`)

```markdown
# Brief nghiên cứu · [Tên chủ đề]

## 0. Phân tầng Quy mô (`R0–R3`) & Diễn giải lại (`Indirect Prompting Restate`)
- Phân tầng rủi ro/quy mô: R2 (Nghiên cứu chuẩn 12-30 nguồn, có xuất sang Bộ 02).
- Diễn giải lại bằng lời của Agent (Restate): Nghiên cứu này nhằm chốt dữ liệu đầu vào cho quyết định [X], tập trung vào ranh giới [Y] và loại trừ hoàn toàn [Z].

## 1. Câu hỏi nghiên cứu và Quyết định phụ thuộc
[Nêu rõ câu hỏi cần trả lời và quyết định thực tế nào sẽ dựa trên kết quả nghiên cứu này]

## 2. Phạm vi dữ liệu
- Thời gian: [Từ năm/tháng đến năm/tháng]
- Địa lý / Thị trường: [Khu vực áp dụng]
- Ngôn ngữ nguồn: [vi, en, ...]

## 3. Tiêu chí loại trừ và Tên miền ưu tiên
- Loại trừ: [Các loại bài viết PR, nguồn không ngày tháng, mảng không liên quan]
- Tên miền ưu tiên (`include_domains`): [Danh sách nếu có]
- Tên miền loại trừ (`exclude_domains`): [Danh sách nếu có]

## 4. Ngưỡng đầu ra mục tiêu
- Số lượng nguồn độc lập tối thiểu: [N]
- Số lượng thẻ sự thật dự kiến: [M]
- Tỷ lệ thẻ `verified` mục tiêu: [>= 40%]
```

### 2. Tệp `source-log.csv` (Nhật ký nguồn có cột chống phòng vang)

```csv
source_id,url,primary_origin_url,title,date_published,date_collected,query_used,search_mode,extraction_method,source_type,language,authority_tier,raw_snapshot_path,collection_reason
S001,https://gso.gov.vn/baocao-2025,https://gso.gov.vn/baocao-2025,"Báo cáo KT-XH 2025",2025-12-29,2026-10-25,"tăng trưởng thương mại điện tử Việt Nam 2025",legal,unified-extract,dữ liệu chính phủ,vi,tier-1,raw-sources/S001.md,"Số liệu chính thức từ Tổng cục Thống kê"
S002,https://baodautu.vn/tmdt-2025,https://gso.gov.vn/baocao-2025,"TMĐT Việt Nam tăng trưởng mạnh",2026-01-05,2026-10-25,"thương mại điện tử Việt Nam 2025",news,ptc-filter,báo chí,vi,tier-2,raw-sources/S002.md,"Bài báo trích dẫn lại báo cáo của GSO"
```

*Lưu ý kỹ thuật:* Trong ví dụ trên, cả `S001` và `S002` đều trỏ về cùng một `primary_origin_url` là `https://gso.gov.vn/baocao-2025`. Khi chạy `python3 scripts/bo01_refine_tool.py audit-echo -i source-log.csv --json`, công cụ sẽ tự động tính `independent_origin_count = 1`.

### 3. Tệp `fact-cards/F-YYYY-NNN.yaml` (Thẻ sự thật nguyên tử v2.1)

```yaml
fact_id: F-2026-001
content: "Một khẳng định đơn lẻ, giữ nguyên con số và đơn vị đo"
exact_quote: "Câu trích dẫn nguyên văn từ tài liệu nguồn làm bằng chứng trực tiếp"
content_hash: "sha256:8f3c2a1b"
claim_label: OBSERVED  # OBSERVED | DERIVED | PRIOR | ASSUMED

sources:
  - S001
  - S002
primary_origins:
  - https://gso.gov.vn/baocao-2025
independent_origin_count: 1

fact_type: numerical-claim  # numerical-claim | qualitative-claim | event | definition | statement
statement_attribution: null # Điền tên người/tổ chức phát biểu nếu fact_type là statement

domain: ten-linh-vuc
role: evidence-thesis-1     # background | evidence-thesis-N | counter-evidence | open-question

date_of_fact: 2025-12
date_extracted: 2026-10-25
extracted_by: agent         # human | agent

trust_tier: verified        # verified | probable | unverified
enrichment:
  related_facts: [F-2026-004]
  contradicts: []
  recency_status: current   # current | historical | outdated
  importance_rank: 1        # 1 (cao nhất) -> 5 (thấp nhất)
  bo02_export_ready: true   # true nếu đủ điều kiện nạp vào kho L1 của Bộ 02
notes: "Ghi chú ngắn gọn về ngữ cảnh hoặc phép tính nếu claim_label là DERIVED"
```

### 4. Tệp `conflict-queue.md` (Hàng đợi xung đột kèm thẻ quyết định `D<N>`)

Mỗi xung đột phải được trình bày theo đúng cấu trúc thẻ quyết định của Bộ 03 để người dùng giải quyết trong 30 giây.

```markdown
## Conflict C-001 · Chênh lệch số liệu quy mô thị trường năm 2025

- **Các thẻ mâu thuẫn:** `F-2026-014` (ghi nhận `20.5 tỷ USD`) và `F-2026-019` (ghi nhận `25.0 tỷ USD`).
- **Bối cảnh đời thường (`ELI10`):** Hai báo cáo lớn đang tính quy mô thị trường theo hai cách khác nhau. Một bên chỉ tính hàng hóa vật lý giao qua sàn, bên kia cộng thêm cả dịch vụ đặt đồ ăn và vé máy bay.
- **Mức độ ảnh hưởng (`Stakes`):** Quyết định trực tiếp đến con số TAM đưa vào bản kế hoạch kinh doanh và mục `L1-market-size-2025` trong Bộ 02.

### Các phương án lựa chọn (`Decision Brief D1`)
- **[A] Chọn `F-2026-014` (`20.5 tỷ USD`) làm chuẩn chính thức (Khuyến nghị · Completeness 9/10):** Phù hợp hoàn toàn với phạm vi dự án chỉ kinh doanh hàng hóa vật lý; giữ `F-2026-019` làm chú thích mở rộng.
- **[B] Chọn `F-2026-019` (`25.0 tỷ USD`) làm chuẩn chính thức (Completeness 6/10):** Phản ánh toàn bộ kinh tế số nhưng làm phình ảo quy mô phân khúc mục tiêu.
- **[C] Báo cáo song song cả hai khoảng số liệu (Completeness 8/10):** Minh bạch phương pháp đo của cả hai bên trong báo cáo cuối.

- **Trạng thái:** `resolved`
- **Phán quyết của con người:** Chọn phương án `[A]` (duyệt ngày `2026-10-25`).
```

### 5. Tệp `gap-checklist.md` (Danh sách lỗ hổng kèm truy vấn bù đắp)

```markdown
## Gap G-001
- **Mô tả lỗ hổng:** Chưa có số liệu tỷ lệ hoàn hàng của nhóm ngành thời trang năm 2025.
- **Phát sinh từ:** Thẻ `F-2026-008` và mục tiêu thứ 2 trong `brief.md`.
- **Hành động thu bù đề xuất:** Chạy `unified-search` chế độ `company` kết hợp `tavily-extract` trên báo cáo ngành logistics.
- **Câu lệnh truy vấn gợi ý:** `"tỷ lệ hoàn hàng" OR "return rate" thương mại điện tử thời trang Việt Nam 2025`
- **Độ ưu tiên:** `high`
```

## Liên kết Liên thông với Bộ 02 và Bộ 03

1. **Từ Bộ 01 sang Bộ 02 (`Kernel Registry SOT`):** Các thẻ sự thật đạt hạng `verified` có cờ `bo02_export_ready: true` sẽ được chuyển đổi tự động qua lệnh `python3 scripts/bo01_refine_tool.py export-bo02 -i <fact-cards.json> -o <l1-facts.yaml> --json` thành mục sự thật `L1-stored-fact.yaml` trong Bộ 02 (xem `references/citation-graph-and-conflict-gate.md`).
2. **Từ Bộ 01 sang Bộ 03 (`Vibecode Kit v6.2 × pstack`):** Khi thực hiện Giai đoạn 1 (`Context & Grounding`) hoặc Giai đoạn 2 (`Spec & Risk Plan`) của Bộ 03 mà cần khảo sát công nghệ, đối thủ cạnh tranh hoặc tài liệu API bên ngoài, Agent kích hoạt Bộ 01 ở chế độ `R1/R2` để thu thập dữ liệu sạch trước khi viết `Blueprint.md`.
