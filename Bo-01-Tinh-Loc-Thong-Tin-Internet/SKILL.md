---
name: internet-info-refinement
description: >
  Thu thập, tinh lọc, khử phòng vang và làm giàu thông tin từ internet thành kho sự thật nguyên tử (Fact Cards) có truy vết nguồn gốc, nhãn nhận định Fable 5.1 và cổng kiểm chứng định lượng bằng CLI tất định. Dùng khi cần nghiên cứu chủ đề mới, tổng hợp báo cáo có trích dẫn chặt chẽ, kiểm tra chéo thông tin mâu thuẫn hoặc chuẩn bị dữ liệu đầu vào cho Bộ 02 (Kernel Registry SOT) và Bộ 03 (Vibecode Kit v6.2).
---

# Internet Info Refinement · Tinh Lọc Thông Tin Internet (`v2.1 · Full-Stack 4 Lớp`)

Biến kết quả tìm kiếm nhiễu loạn từ internet thành **tập thẻ sự thật nguyên tử (`Fact Cards`)** có nguồn gốc độc lập, phân hạng tin cậy cơ học và thực thi qua công cụ CLI tất định `scripts/bo01_refine_tool.py`.

## 1. Phân Tầng Quy Mô & Rủi Ro Co Giãn (`R0–R3 Adaptive Scaling`)

Trước khi chạy, phân loại bài toán vào đúng tầng `R0..R3` để chọn đường chạy nhanh (`Fast-Track`) hoặc đầy đủ:

| Tầng | Quy mô & Đặc điểm Bài toán | Đường chạy khuyến nghị (`Fast-Track` vs `Full`) | Cổng bắt buộc |
|---|---|---|---|
| **R0 · Tra cứu nhanh** | `< 5` nguồn, kiểm chứng 1-2 con số hoặc sự kiện đơn lẻ | Gộp Giai đoạn 1-3-7 trong 1 lượt; lọc nhanh bằng `ptc-filter` và trả lời kèm trích dẫn `exact_quote` | Nhãn `Fable 5.1` + `exact_quote` |
| **R1 · Nghiên cứu nhỏ** | `5–12` nguồn, tổng hợp nhanh trong `10 phút` cho 1 chủ đề hẹp | Chạy `brief.md` rút gọn + `source-log.csv` + `Fact Cards` chính + `audit-echo` | `Indirect Prompting Restate` + `audit-echo` |
| **R2 · Nghiên cứu chuẩn** | `12–30` nguồn, có mâu thuẫn số liệu hoặc cần xuất sang Bộ 02 | Chạy đủ 7 giai đoạn + `conflict-queue.md` (`Decision Brief D<N>`) + `gate-check` + `export-bo02` | `D1` + `D<N>` + `gate-check PASS` |
| **R3 · Kiểm toán trọng yếu** | `> 30` nguồn, dữ liệu tài chính/pháp lý/y tế hoặc đa ngôn ngữ | Chạy đủ 7 giai đoạn + đối chiếu tối thiểu 2 nguồn gốc độc lập `tier-1` cho mọi kết luận cốt lõi | Toàn bộ 5 cổng + xuất `L1` sang Bộ 02 |

## 2. Công Cụ CLI Tất Định (`scripts/bo01_refine_tool.py` · Deep Module Lever)

Tuyệt đối không tự gõ lại script lọc văn bản hay đếm nguồn thủ công trong đầu. Sử dụng trực tiếp công cụ CLI chuẩn 4 lớp đi kèm bộ kỹ năng:

| Lệnh CLI (`python3 scripts/bo01_refine_tool.py ...`) | Chức năng tất định | Cờ hỗ trợ |
|---|---|---|
| `ptc-filter -i <raw.json> -k "từ khóa" -o <clean.json>` | Cắt cửa sổ ngữ cảnh `~1.200` ký tự quanh từ khóa, loại bỏ `>80%` rác HTML/menu và gắn cờ `untrusted_external_content` | `--window-chars`, `--max-snippets`, `--dry-run`, `--json` |
| `audit-echo -i <source-log.csv>` | Gom nhóm theo `primary_origin_url` / `independent_origin_id`, phát hiện cụm phòng vang (`Echo Chamber`) và đếm gốc độc lập | `--min-origins`, `--json` |
| `gate-check --independent-origins 2 --unresolved-conflicts 0` | Kiểm tra 4 điều kiện cổng định lượng trước khi tổng hợp báo cáo cuối hoặc xuất sang Bộ 02 | `--input`, `--citation-coverage`, `--expired-ttl`, `--json` |
| `export-bo02 -i <fact-cards.json> -o <l1-facts.yaml>` | Chuyển đổi `Fact Cards` đã xác minh sang định dạng `L1-stored-fact.yaml` của Bộ 02 kèm ánh xạ 4 nhãn Fable 5.1 | `--dry-run`, `--json` |
| `--self-test --json` | Chạy bộ kiểm thử nội tại kiểm chứng toàn bộ 4 lệnh trong `< 200ms` | `--json` |

## 3. Quy Trình 7 Giai Đoạn & Giám Sát Nhận Thức (`Indirect Prompting Restate`)

### Giai đoạn 1 · Khóa `brief.md` + `Indirect Prompting Restate` (`Cổng D1`)
1. **Diễn giải lại bằng lời của Agent (`Indirect Prompting Restate`):** Trước khi tìm kiếm, Agent bắt buộc tự diễn giải lại bài toán trong 3-5 dòng gồm: *(a) Quyết định thực tế nào phụ thuộc vào nghiên cứu này, (b) Ranh giới loại trừ (`Out-of-scope`) cùng (c) Ngưỡng nguồn độc lập tối thiểu*.
2. Nếu yêu cầu còn mơ hồ ở tầng `R2/R3`, trình thẻ **Decision Brief `D1`** (gồm `ELI10`, `Stakes`, phương án `A/B/C` kèm điểm `Completeness X/10`) để người dùng chốt trước khi chạy Giai đoạn 2.

### Giai đoạn 2 · Thu Thập Đa Tín Hiệu & Cô Lập Ngữ Cảnh PTC
- Ưu tiên định tuyến đa tín hiệu qua `unified-search` (`academic`, `legal`, `news`, `company`, `deep`, `hybrid`) hoặc `tavily-*`; dùng `/scrape` ở chế độ chỉ đọc cho trang cần phiên đăng nhập.
- Lưu kết quả thô xuống đĩa và chạy `python3 scripts/bo01_refine_tool.py ptc-filter` để nạp duy nhất các đoạn trích sạch vào ngữ cảnh suy luận (xem chi tiết tại `references/multi-signal-search-and-ptc.md`).
- Ghi nhận đầy đủ `primary_origin_url` và `authority_tier` vào `source-log.csv` (bản mẫu `templates/source-log.md`).

### Giai đoạn 3 · Trích Xuất Sự Thật Nguyên Tử & 4 Nhãn Fable 5.1
Mỗi tệp `fact-cards/F-YYYY-NNN.yaml` (bản mẫu `templates/fact-card.yaml`) chỉ chứa **một sự thật nguyên tử**, giữ nguyên con số, lưu câu gốc `exact_quote`, mã băm `content_hash` và gắn đúng 1 trong **4 nhãn nhận định Fable 5.1** (đồng bộ xuyên suốt Bộ 01, Bộ 02 và Bộ 03):
- `OBSERVED`: Trích trực tiếp từ tài liệu nguồn thu thập trong phiên (`-> EXTRACTED` ở Bộ 02).
- `DERIVED`: Tính toán tất định từ các thẻ `OBSERVED` có ghi rõ công thức (`-> INFERRED` ở Bộ 02).
- `PRIOR`: Tri thức nền của mô hình chưa có nguồn xác minh trong phiên (không bao giờ được gán `verified`).
- `ASSUMED`: Giả định làm việc tạm thời, bắt buộc ghi rõ rủi ro nếu sai và thêm vào `gap-checklist.md` (`-> AMBIGUOUS` ở Bộ 02).

### Giai đoạn 4 · Khử Trùng Lặp, Khử Phòng Vang & Giải Quyết Xung Đột (`Cổng D<N>`)
- Chạy `python3 scripts/bo01_refine_tool.py audit-echo -i source-log.csv --json` để gom các bài báo chép lại cùng một nguồn gốc về đúng số lượng gốc độc lập (`independent_origin_count`).
- Khi hai nguồn mâu thuẫn số liệu hoặc nhận định, tuyệt đối không tự chọn nguồn viết mượt hơn. Đưa cả hai vào `conflict-queue.md` (bản mẫu `templates/conflict-queue.md`) và lập thẻ **Decision Brief `D<N>`** để người dùng phán xử (xem `references/citation-graph-and-conflict-gate.md`).

### Giai đoạn 5 · Phát Hiện Lỗ Hổng & Truy Vấn Bù Đắp
- Lập `gap-checklist.md` (bản mẫu `templates/gap-checklist.md`) cho mọi luận điểm mới có 1 nguồn phụ, chuỗi thời gian đứt quãng hoặc nhãn `ASSUMED`, kèm câu lệnh truy vấn bù đắp cụ thể.

### Giai đoạn 6 · Phân Hạng Tin Cậy 3 Mức & Làm Giàu 4 Chiều
- **`verified`**: Nhãn `OBSERVED`/`DERIVED` có `independent_origin_count >= 2` hoặc `>= 1` nguồn chính thức `tier-1`.
- **`probable`**: Có 1 nguồn `tier-1`/`tier-2` nhưng `independent_origin_count == 1`.
- **`unverified`**: Chỉ có nguồn `tier-3`, không rõ nguồn gốc đầu tiên hoặc mang nhãn `PRIOR`/`ASSUMED`.
- Bổ sung khối `enrichment` gồm liên kết chéo, phân loại đa trục, trạng thái độ tươi (`current | historical | outdated`) và đánh dấu thẻ đủ chuẩn xuất sang Bộ 02.

### Giai đoạn 7 · Cổng Định Lượng (`Constraint Loop`), Xuất Báo Cáo 3 Phần & Cầu Nối Bộ 02
1. Chạy `python3 scripts/bo01_refine_tool.py gate-check --json` để xác nhận đủ 4 điều kiện: `independent_origin_count >= 2` (hoặc `tier-1` chính thức), `0` xung đột treo, `100%` trích dẫn khớp `Fact Card` và `0` thẻ quá hạn.
2. Xuất `report-final.md` (bản mẫu `templates/report-final.md`) gồm đúng 3 phần tách biệt: *(1) Kết luận cốt lõi từ `verified`, (2) Giả thuyết từ `probable`, (3) Câu hỏi mở từ `gap-checklist.md`*.
3. Khi chuyển giao sang Bộ 02, chạy `python3 scripts/bo01_refine_tool.py export-bo02 -i <fact-cards.json> -o <l1-stored-facts.yaml> --json` (xem `references/citation-graph-and-conflict-gate.md`).

## 4. Bản Đồ Tài Liệu Tham Chiếu (`Progressive Disclosure`)

- **Kiến trúc & Phương pháp luận:** `Methodology.md`, `Architecture.md`, `Quick-Start.md`
- **Giao thức chuyên sâu (`references/`):**
  - `references/multi-signal-search-and-ptc.md`: Định tuyến đa tín hiệu, cô lập PTC và lệnh `bo01_refine_tool.py ptc-filter`.
  - `references/citation-graph-and-conflict-gate.md`: Đồ thị nguồn gốc khử phòng vang (`audit-echo`), thẻ quyết định `Decision Brief D<N>`, cổng `gate-check` và xuất `export-bo02` sang Bộ 02.
  - `references/authenticated-scrape-and-guardrails.md`: Cào trình duyệt chỉ đọc (`gstack /scrape` + `/skillify`) và rào chắn chống Prompt Injection.
- **Biểu mẫu chuẩn (`templates/`):** `source-log.md`, `fact-card.yaml`, `conflict-queue.md`, `gap-checklist.md`, `report-final.md`, `extraction-and-synthesis-prompts.md`.
- **Ví dụ thực chiến (`examples/`):** `examples/worked-example.md`.
