# Bộ 02 · Phương Pháp Kernel Registry & Nguồn Sự Thật Duy Nhất Bốn Xuất Xứ (`v2.1 · Full-Stack 4 Lớp`)

> **Tên kỹ năng:** `kernel-registry-sot`
> **Phiên bản:** `2.1` (Chuẩn Tier-1 Full-Stack 4 Lớp · Tích hợp Deep Module CLI `scripts/bo02_registry_tool.py` + `scripts/eval_l2.py`, Trình thông dịch Toán học An toàn `AST Safe Evaluator`, Phân tầng co giãn `R0–R3`, `Indirect Prompting Restate` và Cầu nối Mã băm Liên thông 3 Bộ)
> **Vai trò trong hệ sinh thái 3 Bộ:** Lớp Quản trị Tri thức & Nguồn Sự Thật Trung tâm (nhận `Fact Cards` đã xác minh từ **Bộ 01 · Internet Info Refinement** và cấp phát con trỏ sự thật `L1/L2`, nghĩa vụ `L3`, phong cách `L4` cùng trạng thái độ tươi cho **Bộ 03 · Vibecode Kit v6.2 × pstack**).

## Điểm Mới Cốt Lõi Của Phiên Bản `v2.1` (`Full-Stack 4 Lớp`)

| Hạng mục | Trước đây (`v2.0` thuần văn bản) | Phiên bản `v2.1` (Full-Stack 4 Lớp) |
|---|---|---|
| **Lớp Công cụ CLI Thực thi Tất định (`scripts/`)** | Tài liệu tham chiếu `python3 scripts/eval_l2.py` nhưng thư mục `scripts/` chưa tồn tại trên đĩa | Trang bị đầy đủ `scripts/bo02_registry_tool.py` (`fingerprint`, `audit-freshness`, `eval-l2`, `sync-feature-map`, `--self-test --json`) và wrapper tương thích ngược `scripts/eval_l2.py` |
| **Tính toán `L2` An toàn Tuyệt đối (`AST Safe Evaluator`)** | Mô tả khái niệm tính công thức bằng script nhưng chưa khóa cơ chế chống thực thi mã tùy ý | Sử dụng `ast.parse(..., mode='eval')` với danh sách nút AST toán học trắng (`0%` dùng hàm `eval()` mở), được kiểm chứng tự động trong `--self-test` |
| **Co giãn theo quy mô (`R0–R3`) & `Indirect Prompting`** | Mọi kho tài liệu đều phải đi qua đủ 5 Phase nặng nề | Phân tầng `R0..R3` (cập nhật nhanh 2 phút ở `R0`, dựng kho nhỏ 15 phút ở `R1`) và bắt buộc bước `Indirect Prompting Restate` ở đầu Phase 1 |
| **Ma trận 4 Nhãn Fable 5.1 & Cầu nối CLI 3 Bộ** | Nhãn đồ thị (`EXTRACTED / INFERRED / AMBIGUOUS`) chưa có bảng ánh xạ cơ học với 4 nhãn Fable 5.1 của Bộ 01 & Bộ 03 | Khóa chặt Ma trận Ánh xạ 4 Nhãn Fable 5.1 và lệnh `sync-feature-map` trong `references/bo01-bo02-bo03-bridge.md` |

## Cấu Trúc Thư Mục Chuẩn 4 Lớp (`SKILL.md` + `scripts/` + `references/` + `templates/`)

```text
Bo-02-Kernel-Registry-SOT/
├── README.md                                        ← Tổng quan & điểm mới v2.1 (file này)
├── SKILL.md                                         ← Lớp 1: Chỉ dẫn cốt lõi cho AI Agent (~95 dòng)
├── Methodology.md                                   ← Triết lý 4 xuất xứ (L1-L4), R0-R3 & quy trình 5 Phase
├── Architecture.md                                  ← Kiến trúc 3 kho, CLI Lever, con trỏ Skill & cổng kiểm soát
├── Quick-Start.md                                   ← Hướng dẫn thực hành 15 phút với CLI bo02_registry_tool.py
├── scripts/
│   ├── bo02_registry_tool.py                        ← Lớp 2: Deep Module CLI (fingerprint, audit-freshness, eval-l2, sync-feature-map, --self-test)
│   └── eval_l2.py                                   ← Wrapper tương thích ngược cho lệnh deterministic_eval_cmd trong L2 YAML
├── references/                                      ← Lớp 3: Giao thức chuyên sâu (Progressive Disclosure)
│   ├── freshness-and-deterministic-l2.md            ← Kiểm toán độ tươi SHA-256 & AST Safe Evaluator cho L2
│   ├── hybrid-indexing-and-gbrain.md                ← Chỉ mục phụ thuộc 2 tầng (CSV + ak-graphify + /sync-gbrain)
│   └── bo01-bo02-bo03-bridge.md                     ← Ma trận 4 Nhãn Fable 5.1 & chuỗi lệnh CLI liên thông 3 Bộ
├── templates/                                       ← Lớp 4: Biểu mẫu chuẩn hóa
│   ├── L1-stored-fact.yaml                          ← Bản mẫu sự thật lưu sẵn L1 có source_hash & verification_status
│   ├── L2-derived-fact.yaml                         ← Bản mẫu sự thật dẫn xuất L2 có formula & audit_trace
│   ├── L3-obligation.yaml                           ← Bản mẫu nghĩa vụ L3 có điều khoản gốc & superseded_by
│   ├── L4-style.yaml                                ← Bản mẫu hồ sơ phong cách L4
│   ├── manifest.csv                                 ← Bảng kiểm kê thành phần toàn kho
│   ├── dependency-index.csv                         ← Bảng chỉ mục phụ thuộc kèm provenance_tag
│   ├── classification-table.csv                     ← Bảng phân loại tài liệu nguồn ở Phase 2
│   └── queues-and-migration-map.md                  ← Hàng đợi quyết định D<N>, R0-R3 Restate & Biên bản Copy-Only
└── examples/
    └── worked-example.md                            ← Ví dụ thực chiến chuyển đổi kho tài liệu hỗn hợp sang SOT
```

## Cách Bắt Đầu Nhanh

1. **Chạy tự kiểm thử công cụ CLI (`< 200ms`):**
   ```bash
   python3 Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py --self-test --json
   python3 Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py --id L2-domain-key-NNN --json
   ```
2. **Nếu bạn muốn thực hành ngay trong 15 phút:** Đọc `Quick-Start.md` rồi xem `examples/worked-example.md`.
3. **Nếu bạn muốn hiểu sâu nguyên lý 4 xuất xứ và cơ chế lan truyền `STALE`:** Đọc `Methodology.md` và `Architecture.md`.
4. **Nếu bạn cài đặt cho AI Agent (`Claude Code` / `Antigravity`):** Chạy `bash tools/install-all.sh` ở thư mục gốc của kho lưu trữ.
