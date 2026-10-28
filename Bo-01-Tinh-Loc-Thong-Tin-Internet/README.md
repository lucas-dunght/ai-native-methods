# Bộ 01 · Phương Pháp Tinh Lọc và Làm Giàu Thông Tin Internet (`v2.1 · Full-Stack 4 Lớp`)

> **Tên kỹ năng:** `internet-info-refinement`
> **Phiên bản:** `2.1` (Chuẩn Tier-1 Full-Stack 4 Lớp · Tích hợp Deep Module CLI `scripts/bo01_refine_tool.py`, Phân tầng co giãn `R0–R3`, `Indirect Prompting Restate`, Cô lập Ngữ cảnh PTC, Đồ thị Nguồn gốc Khử Phòng vang và Kỷ luật 4 Nhãn Fable 5.1)
> **Vai trò trong hệ sinh thái 3 Bộ:** Lớp Thu thập & Tinh lọc Tri thức Đầu vào (cung cấp `Fact Cards` đã xác minh cho **Bộ 02 · Kernel Registry SOT** và tài liệu nghiên cứu kỹ thuật cho **Bộ 03 · Vibecode Kit v6.2 × pstack**).

## Điểm Mới Cốt Lõi Của Phiên Bản `v2.1` (`Full-Stack 4 Lớp`)

| Hạng mục | Trước đây (`v2.0` thuần văn bản) | Phiên bản `v2.1` (Full-Stack 4 Lớp) |
|---|---|---|
| **Lớp Công cụ CLI Tất định (`scripts/`)** | Agent phải tự gõ lại các đoạn code Python tạm thời trong Markdown mỗi lần lọc PTC hoặc đếm nguồn | Trang bị `scripts/bo01_refine_tool.py` (`ptc-filter`, `audit-echo`, `gate-check`, `export-bo02`, `--self-test --json`) chạy bằng 1 lệnh |
| **Co giãn theo quy mô & rủi ro (`R0–R3`)** | Bắt buộc chạy cứng nhắc cả 7 giai đoạn cho mọi bài toán | Phân tầng co giãn `R0..R3`: tra cứu nhỏ (`R0/R1`) có đường chạy nhanh `Fast-Track` 10 phút; bài toán phức tạp (`R2/R3`) mở đủ 7 giai đoạn |
| **Giám sát Nhận thức (`Indirect Prompting`)** | Chưa có bước buộc Agent tự diễn giải lại bài toán trước khi tìm kiếm | Bắt buộc bước **Indirect Prompting Restate** (diễn giải lại bằng lời của Agent) trước cổng `D1` |
| **Liên thông Tự động sang Bộ 02** | Chuyển đổi thủ công từ `Fact Card` sang `L1` | Lệnh `bo01_refine_tool.py export-bo02` xuất thẳng `Fact Card` sang `L1-stored-fact.yaml` kèm ánh xạ 4 nhãn Fable 5.1 (`OBSERVED/DERIVED/PRIOR/ASSUMED`) |

## Cấu Trúc Thư Mục Chuẩn 4 Lớp (`SKILL.md` + `scripts/` + `references/` + `templates/`)

```text
Bo-01-Tinh-Loc-Thong-Tin-Internet/
├── README.md                                        ← Tổng quan & điểm mới v2.1 (file này)
├── SKILL.md                                         ← Lớp 1: Chỉ dẫn cốt lõi cho AI Agent (~105 dòng)
├── Methodology.md                                   ← Triết lý nền, 6 nguyên tắc, R0-R3 & 7 giai đoạn
├── Architecture.md                                  ← Kiến trúc luồng dữ liệu, CLI Lever & 5 cổng kiểm soát
├── Quick-Start.md                                   ← Hướng dẫn thực hành 10 phút với CLI bo01_refine_tool.py
├── scripts/
│   └── bo01_refine_tool.py                          ← Lớp 2: Deep Module CLI (ptc-filter, audit-echo, gate-check, export-bo02, --self-test)
├── references/                                      ← Lớp 3: Giao thức chuyên sâu (Progressive Disclosure)
│   ├── multi-signal-search-and-ptc.md               ← Định tuyến đa tín hiệu, cô lập PTC & lệnh ptc-filter
│   ├── citation-graph-and-conflict-gate.md          ← Đồ thị nguồn gốc (audit-echo), thẻ D<N>, gate-check & export-bo02
│   └── authenticated-scrape-and-guardrails.md       ← Cào trình duyệt chỉ đọc (/scrape) & chống Prompt Injection
├── templates/                                       ← Lớp 4: Biểu mẫu chuẩn hóa
│   ├── source-log.md                                ← Nhật ký nguồn thu thập (có R0-R3, Indirect Prompting & primary_origin_url)
│   ├── fact-card.yaml                               ← Thẻ sự thật nguyên tử v2.1 (có content_hash, claim_label, primary_origins)
│   ├── conflict-queue.md                            ← Hàng đợi xung đột tích hợp thẻ quyết định D<N>
│   ├── gap-checklist.md                             ← Danh sách lỗ hổng kèm câu lệnh truy vấn bù đắp
│   ├── report-final.md                              ← Khung báo cáo 3 phần tách biệt độ tin cậy
│   └── extraction-and-synthesis-prompts.md          ← Bộ prompt chuẩn có rào chắn chống Prompt Injection & CLI gate
└── examples/
    └── worked-example.md                            ← Ví dụ hoàn chỉnh 1 vòng nghiên cứu thực tế
```

## Cách Bắt Đầu Nhanh

1. **Chạy tự kiểm thử công cụ CLI (`< 200ms`):**
   ```bash
   python3 Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py --self-test --json
   ```
2. **Nếu bạn muốn thực hành ngay trong 10 phút:** Đọc `Quick-Start.md` rồi xem `examples/worked-example.md`.
3. **Nếu bạn muốn hiểu sâu nguyên lý và cổng kiểm soát:** Đọc `Methodology.md` và `Architecture.md`.
4. **Nếu bạn cài đặt cho AI Agent (`Claude Code` / `Antigravity`):** Chạy `bash tools/install-all.sh` ở thư mục gốc của kho lưu trữ để tự động kiểm thử `--self-test` và đồng bộ kỹ năng vào cả `~/.gemini/config/skills/internet-info-refinement/` lẫn `~/.claude/skills/internet-info-refinement/`.
