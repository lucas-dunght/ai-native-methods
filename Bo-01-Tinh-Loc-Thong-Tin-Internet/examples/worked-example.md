# Worked Example · Nghiên cứu Thị trường Thanh toán Số Đông Nam Á (Bộ 01 v2.0 End-to-End)

Tài liệu này trình bày một ví dụ thực chiến hoàn chỉnh chạy qua đủ 7 giai đoạn của **Bộ 01 v2.0 (2026.10)** cho bài toán nghiên cứu thị trường thanh toán số xuyên biên giới tại Đông Nam Á, từ bước lập `Brief` cho tới khi xuất báo cáo cuối và bàn giao thẻ sự thật `L1` sang **Bộ 02 (`Kernel Registry SOT`)**.

---

## Giai đoạn 1 · Lập Brief và Khóa Phạm vi (`brief.md`)

**Bối cảnh.** Một nhóm phát triển sản phẩm Fintech muốn xây dựng ví thanh toán hỗ trợ khách du lịch và tiểu thương thanh toán mã QR xuyên biên giới giữa Việt Nam, Thái Lan và Singapore.

```markdown
# Brief nghiên cứu · Thanh toán QR Xuyên biên giới ĐNA (2024-2026)

## 1. Câu hỏi nghiên cứu và Quyết định phụ thuộc
Quy mô giao dịch thanh toán số tại Đông Nam Á và tốc độ kết nối mã QR xuyên biên giới giữa Việt Nam, Thái Lan và Singapore trong giai đoạn 2024-2026 đạt mức nào? Kết quả dùng để quyết định thứ tự ưu tiên tích hợp cổng thanh toán ở Bộ 03 (Vibecode Kit).

## 2. Phạm vi dữ liệu
- Thời gian. Số liệu thực tế từ 2023 đến 2025 và dự báo đến 2026.
- Địa lý. Đông Nam Á, trọng tâm là hành lang Việt Nam, Thái Lan, Singapore.

## 3. Tiêu chí loại trừ
- Loại trừ các bài viết PR ví điện tử không công bố nguồn thống kê.
- Loại trừ dữ liệu trước năm 2023.

## 4. Ngưỡng chất lượng mục tiêu
- Tỷ lệ thẻ `verified >= 50%`, xử lý sạch 100% xung đột qua thẻ `Decision Brief D<N>`, xuất các thẻ `verified` sang chuẩn `L1` của Bộ 02.
```

---

## Giai đoạn 2 · Thu thập Đa tín hiệu & Lọc Cô lập PTC (`source-log.csv`)

Agent gọi `unified-search` ở các chế độ `company`, `legal`, `news` và lọc qua `/tmp/` để thu về 5 nguồn chất lượng cao.

```csv
source_id,url,primary_origin_url,title,date_published,date_collected,query_used,search_mode,extraction_method,source_type,language,authority_tier,raw_snapshot_path,collection_reason
S001,https://economysea.withgoogle.com/2024,https://economysea.withgoogle.com/2024,"e-Conomy SEA 2024 Report",2024-11-05,2026-10-25,"Southeast Asia digital payments GMV 2024",company,unified-extract,báo cáo nghiên cứu,en,tier-1,raw-sources/S001.md,"Báo cáo gốc của Google, Temasek và Bain"
S002,https://fintechnews.sg/sea-payments-2024,https://economysea.withgoogle.com/2024,"SEA Digital Payments Reach US$114B",2024-11-06,2026-10-25,"SEA digital payments 114B 2024",news,ptc-search,báo chí,en,tier-2,raw-sources/S002.md,"Bài báo trích dẫn lại báo cáo e-Conomy SEA 2024"
S003,https://bis.org/publ/qtrpdf/r_qt2409_asean_qr.htm,https://bis.org/publ/qtrpdf/r_qt2409_asean_qr.htm,"BIS Quarterly Review: ASEAN Fast Payment Links",2024-09-22,2026-10-25,"ASEAN cross-border QR payment volume BIS 2024",academic,unified-extract,tổ chức quốc tế,en,tier-1,raw-sources/S003.md,"Báo cáo độc lập của Ngân hàng Thanh toán Quốc tế BIS"
S004,https://sbv.gov.vn/asean-qr-link-2024,https://sbv.gov.vn/asean-qr-link-2024,"Kết nối thanh toán bán lẻ song phương qua mã QR Việt Nam - Thái Lan - Singapore",2024-12-10,2026-10-25,"thanh toán QR xuyên biên giới Việt Nam Thái Lan Ngân hàng Nhà nước",legal,unified-search,dữ liệu chính phủ,vi,tier-1,raw-sources/S004.md,"Công bố chính thức từ Ngân hàng Nhà nước Việt Nam"
S005,https://asean-blog.example.com/qr-estimate-2024,unknown,"ASEAN Digital Wallet Trends",2024-10-18,2026-10-25,"ASEAN digital wallet GMV 2024",news,ptc-search,blog cá nhân,en,tier-3,raw-sources/S005.md,"Bài blog nêu con số GMV khác biệt không rõ nguồn"
```

---

## Giai đoạn 3 · Trích xuất Sự thật Nguyên tử (`fact-cards/*.yaml`)

Từ 5 nguồn trên, Agent trích xuất được 5 thẻ sự thật nguyên tử. Dưới đây là 3 thẻ tiêu biểu.

### Thẻ `F-2026-001.yaml` (Đã gộp `S001` và `S002`)

```yaml
fact_id: F-2026-001
content: "Tổng giá trị giao dịch (GMV) mảng thanh toán số tại Đông Nam Á đạt 1.140 tỷ USD trong năm 2024"
exact_quote: "Digital payments gross transaction value (GTV) across Southeast Asia reached US$1,140 billion in 2024"
content_hash: "sha256:7d81c4a9"
claim_label: OBSERVED
sources: [S001, S002]
primary_origins: ["https://economysea.withgoogle.com/2024"]
independent_origin_count: 1
fact_type: numerical-claim
domain: market-sizing
role: evidence-thesis-1
date_extracted: 2026-10-25
extracted_by: agent
notes: "S002 dẫn lại báo cáo gốc S001 (Google, Temasek, Bain). Vì S001 là báo cáo nghiên cứu gốc tier-1 uy tín nên đủ chuẩn đối chiếu."
```

### Thẻ `F-2026-002.yaml` (Trích từ `S003` và `S004` · 2 nguồn gốc độc lập)

```yaml
fact_id: F-2026-002
content: "Hệ thống thanh toán nhanh qua mã QR của Việt Nam, Thái Lan và Singapore đã kết nối liên thông chính thức ở cấp ngân hàng trung ương tính đến cuối năm 2024"
exact_quote: "Bilateral retail QR payment linkages between Vietnam, Thailand, and Singapore are live under central bank oversight as of late 2024"
content_hash: "sha256:3e92b1f0"
claim_label: OBSERVED
sources: [S003, S004]
primary_origins:
  - "https://bis.org/publ/qtrpdf/r_qt2409_asean_qr.htm"
  - "https://sbv.gov.vn/asean-qr-link-2024"
independent_origin_count: 2
fact_type: event
domain: payment-infrastructure
role: evidence-thesis-2
date_extracted: 2026-10-25
extracted_by: agent
notes: "Xác nhận độc lập bởi cả Ngân hàng Thanh toán Quốc tế (BIS) và Ngân hàng Nhà nước Việt Nam (SBV)."
```

### Thẻ `F-2026-003.yaml` (Trích từ `S005` · Xung đột với `F-2026-001`)

```yaml
fact_id: F-2026-003
content: "Tổng giá trị giao dịch thanh toán số tại Đông Nam Á đạt 114 tỷ USD trong năm 2024"
exact_quote: "SEA digital payments totaled US$114B in 2024"
content_hash: "sha256:1b44d9e2"
claim_label: OBSERVED
sources: [S005]
primary_origins: ["unknown"]
independent_origin_count: 0
fact_type: numerical-claim
domain: market-sizing
role: conflict-candidate
date_extracted: 2026-10-25
extracted_by: agent
notes: "Con số 114 tỷ USD thấp hơn 10 lần so với báo cáo gốc S001 (1.140 tỷ USD), nghi ngờ do tác giả blog đọc nhầm hàng đơn vị."
```

---

## Giai đoạn 4 · Khử Phòng vang và Phán xử Xung đột bằng Thẻ `D1` (`conflict-queue.md`)

Agent phát hiện mâu thuẫn giữa `F-2026-001` (`1.140 tỷ USD`) và `F-2026-003` (`114 tỷ USD`) và trình thẻ quyết định `D1` cho con người.

```markdown
### D1 · Conflict C-001 · Chênh lệch 10 lần về tổng giá trị giao dịch (GTV) thanh toán số ĐNA năm 2024

- **Giải thích ELI10.** Báo cáo gốc `e-Conomy SEA 2024` (`S001`, hạng `tier-1`) công bố tổng giá trị giao dịch thanh toán số đạt `1.140 tỷ USD`. Ngược lại, bài blog `S005` (`tier-3`, không nêu nguồn gốc) ghi là `114 tỷ USD` (trùng với con số doanh thu ròng của mảng thương mại điện tử thay vì tổng giá trị giao dịch thanh toán).
- **Rủi ro nếu chọn sai (Stakes).** Chọn nhầm `F-2026-003` sẽ làm sai lệch quy mô dòng tiền thanh toán khu vực đi 10 lần.
- **Khuyến nghị (Recommendation).** Chọn **A** (Giữ `F-2026-001` làm chuẩn và đánh dấu `F-2026-003` là `deprecated` do lỗi trích dẫn của blog `tier-3`).
- **Điểm độ phủ (Completeness).** `A = 10/10`, `B = 2/10`.
- **Quyết định của con người.** `[x] Phương án A (Đã duyệt bởi Trưởng nhóm Nghiên cứu ngày 2026-10-25)`.
```

---

## Giai đoạn 5 & 6 · Phân tích Lỗ hổng, Phân hạng Tin cậy & Xuất Cầu nối Bộ 02

- **Phân hạng tin cậy.**
  - `F-2026-001` đạt `verified` (nguồn gốc `tier-1` trực tiếp).
  - `F-2026-002` đạt `verified` (`independent_origin_count = 2` từ BIS và SBV).
  - `F-2026-003` chuyển sang trạng thái `deprecated` sau phán quyết `D1`.
- **Cầu nối xuất sang Bộ 02 (`bo02_bridge`).**
  Thẻ `F-2026-001` và `F-2026-002` được gắn `bo02_bridge.export_ready: true` để nạp thẳng thành `L1-sea-digital-payments-gtv-2024` và `L1-asean-qr-bilateral-link-2024` trong `Kernel Registry`.

---

## Giai đoạn 7 · Kiểm tra Constraint Loop & Báo cáo Cuối (`report-final.md`)

Kết quả chạy `Constraint Loop`.
- Tỷ lệ thẻ `verified` trên các thẻ đang hoạt động đạt `100%` (`>= 40%`).
- Số lượng xung đột treo bằng `0`.
- Số lượng lỗ hổng mở bằng `1` (`< 10`).
- `100%` mã trích dẫn `[F-2026-001]`, `[F-2026-002]` khớp hoàn toàn với tệp YAML.

```markdown
# Báo cáo Tổng hợp · Thanh toán QR Xuyên biên giới Đông Nam Á (2024-2026)

## 1. Kết luận cốt lõi (Verified Facts)
Tổng giá trị giao dịch (GTV) mảng thanh toán số tại Đông Nam Á đã đạt quy mô 1.140 tỷ USD trong năm 2024 [F-2026-001]. Về hạ tầng kỹ thuật và pháp lý, hệ thống thanh toán bán lẻ qua mã QR giữa Việt Nam, Thái Lan và Singapore đã hoàn tất kết nối liên thông chính thức dưới sự giám sát của các ngân hàng trung ương tính đến cuối năm 2024 [F-2026-002].

## 2. Giả thuyết cần kiểm chứng thêm (Probable Facts)
Hiện không có giả thuyết treo chưa xác minh trong phạm vi cốt lõi của chu kỳ này.

## 3. Câu hỏi mở và Lỗ hổng dữ liệu (Open Gaps)
- Gap G-001. Cần thu thập bảng biểu phí chuyển đổi ngoại tệ chi tiết ở tầng ngân hàng thương mại thành viên (NAPAS và PromptPay) để nạp vào công thức tính biên lợi nhuận `L2` ở Bộ 02.
```
