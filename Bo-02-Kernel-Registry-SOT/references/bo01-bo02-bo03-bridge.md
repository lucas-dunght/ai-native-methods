# Giao thức Liên thông Tự động Bộ 01 → Bộ 02 → Bộ 03 (`Three-Suite AI-Native Bridge v2.1`)

Tài liệu này định nghĩa đường ống dữ liệu, **Ma trận Chuẩn hóa 4 Nhãn Nhận định Fable 5.1** và **Chuỗi 3 Lệnh CLI Liên thông** xuyên suốt ba bộ phương pháp trong hệ sinh thái `ai-native-methods` gồm **Bộ 01 (`Internet Info Refinement v2.1`)**, **Bộ 02 (`Kernel Registry SOT v2.1`)** và **Bộ 03 (`Vibecode Kit v6.2 × pstack`)**.

## 1. Sơ đồ Liên thông Tổng thể & Chuỗi Lệnh CLI 3 Bộ

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ BỘ 01 · TINH LỌC THÔNG TIN INTERNET (v2.1 · Full-Stack 4 Lớp)           │
│ - Phân tầng R0-R3 + Indirect Prompting Restate                          │
│ - CLI: python3 scripts/bo01_refine_tool.py ptc-filter & audit-echo      │
│ - Đầu ra: Tập thẻ fact-cards/F-YYYY-NNN.yaml (verified · 4 nhãn Fable)  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
       [Chặng 1: python3 scripts/bo01_refine_tool.py export-bo02 --json]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ BỘ 02 · KERNEL REGISTRY & NGUỒN SỰ THẬT (v2.1 · Full-Stack 4 Lớp)       │
│ - Kho registry/ (L1 + L2 qua AST Safe Evaluator), obligations/ (L3)     │
│ - CLI: python3 scripts/bo02_registry_tool.py audit-freshness & eval-l2  │
│ - Đầu ra: Hệ thống Con trỏ [L1-*], [L2-*], [OBL-*], [L4-*] (FRESH)      │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
    [Chặng 2: python3 scripts/bo02_registry_tool.py sync-feature-map --json]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ BỘ 03 · VIBECODE KIT (v6.2 × pstack · Full-Stack 4 Lớp)                 │
│ - Chủ thầu đọc Feature Map & nhúng [L1-*], [OBL-*] vào Blueprint        │
│ - Thợ thi công theo Type Signatures Sketch & ./bin/control-app          │
│ - CLI: python3 scripts/bo03_vibecode_tool.py maintain-features          │
│   & constraint-check & wtree-fingerprint                                │
└─────────────────────────────────────────────────────────────────────────┘
```

## 2. Ma Trận Chuẩn Hóa 4 Nhãn Nhận Định Fable 5.1 Xuyên 3 Bộ (`Unified Claim & Provenance Matrix`)

Để xóa bỏ hoàn toàn độ lệch thuật ngữ giữa Bộ 01, Bộ 02 và Bộ 03, toàn bộ hệ sinh thái thống nhất sử dụng **4 Nhãn Nhận Định Fable 5.1** và ánh xạ cơ học 1-1 sang nhãn cạnh đồ thị của Bộ 02:

| Nhãn chuẩn Fable 5.1 (Bộ 01 & Bộ 03) | Nhãn tương đương cũ ở Bộ 03 (Tương thích ngược) | Nhãn xuất xứ cạnh trong `dependency-index.csv` & `ak-graphify` (Bộ 02) | Bản chất bằng chứng & Quy tắc qua cổng |
|---|---|---|---|
| **`OBSERVED`** | `OBSERVED` | **`EXTRACTED`** | Trích xuất trực tiếp từ tài liệu gốc, tệp mã nguồn (`file:line`), kết quả chạy CLI/test thực tế hoặc nguồn `tier-1/tier-2` có `exact_quote` + `source_hash`. Đủ điều kiện nạp vào `L1` và `L3`. |
| **`DERIVED`** | `INFERRED` | **`INFERRED`** | Tính toán tất định từ các mục `OBSERVED` qua công thức rõ ràng (`eval-l2` / `AST Safe Evaluator`) hoặc suy luận kiến trúc có `audit_trace`. Đủ điều kiện nạp vào `L2`. |
| **`PRIOR`** | `UNVERIFIED` | **`AMBIGUOUS`** | Tri thức nền có sẵn của mô hình AI nhưng chưa được xác minh bằng tài liệu hoặc phép đo trong phiên hiện tại. **Cấm** nâng lên `verified` và **cấm** nạp tự động vào `L1/L2/L3`. |
| **`ASSUMED`** | `UNVERIFIED` | **`AMBIGUOUS`** | Giả định làm việc tạm thời khi thiếu dữ liệu. Bắt buộc ghi rõ rủi ro nếu sai, đưa vào `gap-checklist.md` hoặc thẻ `Decision Brief D<N>` chờ con người phê duyệt. |

## 3. Chặng 1 · Chuyển đổi `Fact Card` (Bộ 01) sang `L1 Stored Fact` (Bộ 02)

### Điều kiện qua cổng (`Gate Criteria`)

Chỉ những thẻ `Fact Card` của Bộ 01 thỏa mãn đồng thời 3 điều kiện sau mới được phép nhập tự động vào kho `registry/stored-facts/` (`L1`) của Bộ 02:
1. `trust_tier == "verified"`.
2. `claim_label` là `OBSERVED` hoặc `DERIVED` (tuyệt đối không nhập thẻ `PRIOR` hay `ASSUMED`).
3. Không nằm trong bất kỳ mục xung đột nào chưa giải quyết của `conflict-queue.md` (đã qua `bo01_refine_tool.py gate-check`).

### Lệnh CLI Chuyển đổi Tự động (`1-Command Export`)

```bash
python3 Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py export-bo02 \
  --input research-cycle/fact-cards/F-2026-001.yaml \
  --output kernel-registry/registry/stored-facts/L1-F-2026-001.yaml \
  --json
```

### Quy tắc Ánh xạ Trường dữ liệu (`Schema Mapping`)

| Trường trong `fact-card.yaml` (Bộ 01) | Trường tương ứng trong `L1-stored-fact.yaml` (Bộ 02) |
|---|---|
| `enrichment.bo02_bridge.suggested_fact_id` (hoặc `fact_id`) | `fact_id` (ví dụ `L1-sea-digital-payments-gtv-2024`) |
| `domain` | `domain` |
| `value` (hoặc `content`) | `value` |
| `unit` | `unit` |
| `claim_label` (`OBSERVED` / `DERIVED`) | `claim_label` + `provenance_tag` (`EXTRACTED` / `INFERRED`) |
| `fact_id` (`F-YYYY-NNN`) | `source.bo01_fact_id` |
| `content_hash` / `source_hash` | `source.source_hash` |
| `date_extracted` | `date_updated` |

Đồng thời, thêm dòng liên kết vào `dependency-index.csv` của Bộ 02:

```csv
L1-sea-digital-payments-gtv-2024,F-2026-001,imported-from,EXTRACTED,reverify-bo01-card,2026-10-28,"Nhập tự động từ chu kỳ nghiên cứu Bộ 01"
```

## 4. Chặng 2 · Kết nối `Kernel Registry` (Bộ 02) vào `Vibecode Kit v6.2 × pstack` (Bộ 03)

Khi xây dựng phần mềm hoặc giải pháp số bằng **Bộ 03 (`Vibecode Kit v6.2 × pstack`)**, kho `Kernel Registry` của Bộ 02 kết hợp cùng bản đồ tính năng `Feature Map` (`references/features/README.md`) đóng vai trò là bộ nhớ nền tảng chống bịa đặt (`Anti-Hallucination Grounding`).

1. **Ở Bước 1 (`SCAN`) và Bước 2 (`RRI`) của Bộ 03:**
   - Chủ thầu (`Contractor`) đọc `manifest.csv` của Bộ 02 cùng `references/features/README.md` (`Feature Map`) trước tiên và thực hiện bước **Indirect Prompting Restate** để tự trả lời các câu hỏi về đơn giá, công thức tính phí (`L1`, `L2`), quy định pháp lý bắt buộc (`L3`), phong cách thương hiệu (`L4`) và câu lệnh `./bin/control-app`.
2. **Ở Bước 4 (`BLUEPRINT`) và Bước 5 (`TASK GRAPH / TIP`) của Bộ 03:**
   - Mọi yêu cầu chức năng (`REQ-ID`) và khung chữ ký kiểu (`Type Signatures Sketch`) liên quan đến số liệu hoặc quy tắc tuân thủ đều phải gắn kèm mã con trỏ của Bộ 02 (ví dụ `REQ-04 · Tính phí giao dịch theo công thức [L2-cross-border-fee] và tuân thủ [OBL-decree-13-001]`).
3. **Ở Bước 6 (`BUILD`), Bước 7 (`VERIFY`) và Bước 8 (`SHIP`) của Bộ 03:**
   - Chạy chuỗi lệnh CLI liên thông để đảm bảo `0%` lệch mã băm giữa kho tri thức và mã nguồn sản phẩm:
   ```bash
   # Bước A: Kiểm toán độ tươi & đồng bộ trạng thái SOT từ Bộ 02 sang Bộ 03
   python3 Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py sync-feature-map \
     --input kernel-registry/registry/stored-facts \
     --dry-run --json

   # Bước B: Kiểm toán mã băm Feature Map, dấu vân tay Worktree & quy tắc văn phong/bảo mật ở Bộ 03
   python3 Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py maintain-features --features-dir references/features --json
   python3 Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py wtree-fingerprint --dir . --json
   python3 Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py constraint-check --paths . --json
   ```
