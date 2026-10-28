# Architecture · Kiến trúc Kỹ thuật của Bộ 02 (`v2.1 · Full-Stack 4 Lớp`)

## Tổng quan

Hệ thống **Kernel Registry v2.1** được thiết kế theo kiến trúc tệp văn bản chuẩn hóa trên Git (`Filesystem-First Git SOT`) kết hợp với công cụ CLI tất định `scripts/bo02_registry_tool.py` (kèm wrapper `scripts/eval_l2.py`), phân tầng quy mô co giãn `R0–R3`, bước giám sát nhận thức `Indirect Prompting Restate`, bộ kiểm toán độ tươi bằng mã băm (`SHA-256 Freshness Engine`), trình thông dịch công thức `L2` an toàn (`AST Safe Evaluator`, `0%` dùng `eval()` mở), lớp mở rộng chỉ mục phân tầng (`CSV -> ak-graphify -> gstack /sync-gbrain`) và cầu nối liên thông trực tiếp với **Bộ 01** và **Bộ 03**.

Mọi thành phần đều sử dụng định dạng `YAML`, `CSV` và `Markdown` thuần túy để con người có thể kiểm tra bằng mắt thường, quản lý lịch sử thay đổi từng dòng qua `git diff` và kiểm chứng tự động qua CI/CD.

## Sơ đồ kiến trúc tổng thể (`v2.1 · Full-Stack 4 Lớp`)

```text
[Bộ 01 · Fact Cards Verified] ──(bo01_refine_tool.py export-bo02)──┐
[Tài liệu nội bộ gốc (Read-Only)] ─────────────────────────────────┼──► Phase 1: R0-R3 + Indirect Prompting Restate
                                                                   │    + bo02_registry_tool.py fingerprint (SHA-256)
                                                                   │    + Phase 2-4 (Phân loại L1-L4, Thẻ D<N>, Migration Map)
                                                                   ▼
Kernel Registry v2.1 (Copy-Only Scope Freeze · Bảo toàn 100% bản gốc · Thực thi qua scripts/bo02_registry_tool.py)
│
├── scripts/                               Lớp Công cụ CLI Tất định (Deep Module Levers)
│   ├── bo02_registry_tool.py              fingerprint | audit-freshness | eval-l2 | sync-feature-map | --self-test
│   └── eval_l2.py                         Wrapper tương thích ngược cho deterministic_eval_cmd
│
├── registry/                              Kho L1 + L2 (Kiểm chứng cơ học)
│   ├── stored-facts/                      Mục L1 (kèm source_hash & verification_status: FRESH/STALE/EXPIRED)
│   │   ├── L1-product-price-001.yaml
│   │   └── L1-sea-digital-payments-gtv-2024.yaml
│   └── derived-facts/                     Mục L2 (kèm formula, AST Safe eval-l2 & audit_trace)
│       └── L2-total-revenue-Q1-2026.yaml
│
├── obligations/                           Kho L3 (Truy vết điều khoản pháp quy gốc)
│   └── decree-13-2023-nd-cp/
│       ├── obligations.yaml               Các nghĩa vụ OBL-* kèm source_hash
│       └── source-doc.pdf                 Bản sao văn bản gốc
│
├── style/                                 Kho L4 (Đứng NGOÀI đường kiểm cơ học)
│   ├── L4-style.yaml                      Metadata định danh hồ sơ phong cách
│   ├── voice-guide.md
│   └── vocabulary.md
│
├── skills/                                Gói quy trình chỉ chứa Con trỏ (Pointer IDs)
│   └── financial-report-skill/
│       └── SKILL.md                       Trỏ tới [L1-*], [L2-*], [OBL-*], [L4-*]
│
├── dependency-index.csv                   Chỉ mục phụ thuộc kèm provenance_tag (Tầng 1)
├── manifest.csv                           Bảng kiểm kê toàn bộ thành phần & độ tươi
│
├── queues/                                Hàng đợi phán xử theo thẻ Decision Brief D<N>
│   ├── conflict-queue.md
│   ├── unclassified-queue.md
│   └── migration-map.md
│
└── .graph-and-brain/                      Tầng mở rộng khi quy mô >= 500 entries (Tầng 2 · R3)
    ├── graphify-out/graph.json            Đồ thị AST + Tài liệu (EXTRACTED/INFERRED/AMBIGUOUS)
    └── gbrain-sync-config.json            Cấu hình đồng bộ GBrain & brain_trust_policy
```

## Thành phần 1 · Kho `registry/` (`L1` Stored Facts & `L2` Derived Facts)

### 1.1. Schema chuẩn của `L1` (`registry/stored-facts/*.yaml`)

Mỗi tệp `L1` lưu một sự thật định lượng hoặc định danh đã được xác minh, kèm mã băm `source_hash` của tài liệu gốc và trạng thái độ tươi `verification_status`.

```yaml
fact_id: L1-product-price-001
fact_type: L1
domain: product-pricing
key: product-X-retail-price-2026-Q4
value: 12500000
unit: VND
source:
  type: internal-document  # hoặc bo01-fact-card | external-regulation
  document_id: pricing-table-2026-Q4
  document_path: raw-docs/pricing/pricing-table-2026-Q4.pdf
  source_hash: "sha256:9f86d081884c7d65"
  bo01_fact_id: null       # Điền F-YYYY-NNN nếu nhập từ Bộ 01
  page: 3
  cell: B7
date_effective: 2026-10-01
date_expires: 2026-12-31
date_updated: 2026-10-25
updated_by: human
verification_status: FRESH # FRESH | STALE | EXPIRED
status: active             # active | deprecated | superseded
superseded_by: null
notes: "Giá bán lẻ niêm yết SKU X-001 áp dụng cho Quý 4/2026"
```

Cơ chế chuyển trạng thái tự động.
- Nếu tệp tại `source.document_path` bị sửa đổi làm mã băm thực tế khác với `source.source_hash`, script kiểm toán lập tức chuyển `verification_status` sang `STALE`.
- Nếu ngày hiện tại vượt quá `date_expires`, trạng thái chuyển sang `EXPIRED`.
- Khi một mục `L1` bị thay thế bởi mục mới, giữ nguyên tệp cũ, đổi `status: superseded` và điền mã mục mới vào `superseded_by`.

### 1.2. Schema chuẩn của `L2` (`registry/derived-facts/*.yaml`)

Mục `L2` lưu công thức tính toán tất định từ các đầu vào `L1` kèm dấu vết kiểm toán `audit_trace`.

```yaml
fact_id: L2-total-revenue-Q4-2026
fact_type: L2
domain: financial-metrics
key: total-revenue-Q4-2026
formula:
  type: sum  # sum | product | ratio | difference | custom
  expression: "L1_rev_A + L1_rev_B + L1_rev_C"
  inputs:
    - L1-revenue-product-A-Q4-2026
    - L1-revenue-product-B-Q4-2026
    - L1-revenue-product-C-Q4-2026
deterministic_eval_cmd: "python3 scripts/eval_l2.py --id L2-total-revenue-Q4-2026"
computed_cache:
  last_computed_value: 485000000
  unit: VND
  computed_at: 2026-10-25T10:30:00Z
  input_hashes:
    L1-revenue-product-A-Q4-2026: "sha256:1a2b3c4d"
    L1-revenue-product-B-Q4-2026: "sha256:5e6f7a8b"
    L1-revenue-product-C-Q4-2026: "sha256:9c0d1e2f"
  audit_trace: "150000000 + 210000000 + 125000000 = 485000000"
verification_status: FRESH
status: active
notes: "Tổng doanh thu kế hoạch Quý 4 tính bằng tổng 3 dòng sản phẩm A, B, C"
```

Nếu bất kỳ mã băm nào trong `input_hashes` thay đổi so với tệp `L1` hiện tại, `verification_status` của `L2` tự động chuyển thành `STALE` để bắt buộc tính lại.

## Thành phần 2 · Kho `obligations/` (`L3` Constrained Obligations)

Mỗi nguồn văn bản pháp quy hoặc quy chế chính thức được đặt trong một thư mục riêng kèm bản sao văn bản gốc và mã băm kiểm chứng.

```yaml
source_metadata:
  source_id: decree-13-2023-nd-cp
  title: "Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân"
  authority: "Chính phủ Việt Nam"
  date_issued: 2023-04-17
  date_effective: 2023-07-01
  date_expires: null
  source_document_path: "./source-doc.pdf"
  source_hash: "sha256:4f3c8e9a1b2d7c6e"
  verification_status: FRESH

obligations:
  - obligation_id: OBL-decree-13-001
    description: "Tổ chức xử lý dữ liệu cá nhân nhạy cảm phải chỉ định bộ phận và nhân sự bảo vệ dữ liệu cá nhân"
    article: "Điều 28, khoản 2"
    severity: critical
    applies_to: data-controllers-and-processors
    compliance_check_type: mandatory-gate
    date_added: 2026-10-25
    status: active
    superseded_by: null
```

## Thành phần 3 · Kho `style/` (`L4` Free Judgment)

Kho `style/` lưu các tài liệu hướng dẫn văn phong bằng Markdown đi kèm một tệp định danh `L4-style.yaml` ghi rõ ràng buộc không kiểm chứng cơ học (`verification_mode: non-mechanically-verifiable`).

```yaml
style_id: L4-brand-voice-core
fact_type: L4
domain: brand-communication
verification_mode: non-mechanically-verifiable
files:
  - style/voice-guide.md
  - style/vocabulary.md
date_updated: 2026-10-25
updated_by: human
status: active
notes: "Chỉ dùng làm đầu vào điều chỉnh giọng văn và thẩm mỹ, tuyệt đối không dùng để suy diễn số liệu L1/L2 hay nghĩa vụ L3."
```

## Thành phần 4 · Gói `skills/` (Kiến trúc Con trỏ `Pointer-Only`)

Mỗi `Skill` trong tổ chức (hoặc các `SKILL.md` / `Blueprint` của Bộ 03) không chép lại giá trị của `L1/L2` hay câu chữ của `L3`, mà tham chiếu qua bảng con trỏ chuẩn.

```markdown
# Skill · Lập Báo cáo Tài chính & Tuân thủ Quý 4

## Con trỏ Nguồn Sự thật (`Kernel Registry Pointers`)
- **Dữ liệu số liệu (`L1` & `L2`).**
  - `[L1-product-price-001]` · Đơn giá bán lẻ SKU X-001
  - `[L2-total-revenue-Q4-2026]` · Tổng doanh thu kế hoạch Quý 4
- **Nghĩa vụ bắt buộc (`L3`).**
  - `[OBL-decree-13-001]` · Kiểm tra điều kiện bảo vệ dữ liệu khách hàng trong báo cáo
- **Phong cách trình bày (`L4`).**
  - `[L4-brand-voice-core]` (`style/voice-guide.md`)

## Quy tắc thực thi
Trước khi xuất báo cáo, chạy kiểm tra độ tươi trên toàn bộ con trỏ. Nếu bất kỳ con trỏ `L1`, `L2`, `L3` nào có trạng thái `STALE` hoặc `EXPIRED`, dừng lại và yêu cầu cập nhật kho trước.
```

## Thành phần 5 · Chỉ mục Phụ thuộc Phân tầng (`dependency-index.csv` + `Graphify` / `GBrain`)

### Tầng 1 · `dependency-index.csv` (Bắt buộc cho mọi quy mô)

```csv
from_id,to_id,relationship,provenance_tag,impact_if_stale,date_added,notes
L2-total-revenue-Q4-2026,L1-revenue-product-A-Q4-2026,derives-from,EXTRACTED,recompute-l2,2026-10-25,"Đầu vào công thức tổng doanh thu"
OBL-decree-13-001,decree-13-2023-nd-cp,extracted-from,EXTRACTED,review-obligation,2026-10-25,"Trích từ Điều 28 khoản 2"
skill-quarterly-report,L2-total-revenue-Q4-2026,references,EXTRACTED,block-skill-output,2026-10-25,"Skill dùng con trỏ L2"
skill-quarterly-report,OBL-decree-13-001,must-comply,EXTRACTED,block-skill-output,2026-10-25,"Skill phải tuân thủ nghĩa vụ bảo mật"
skill-quarterly-report,L4-brand-voice-core,uses,EXTRACTED,advisory-only,2026-10-25,"Skill áp dụng giọng văn thương hiệu"
```

Trong đó cột `provenance_tag` kế thừa chuẩn phân loại độ tin cậy liên kết của `ak-graphify` gồm.
- `EXTRACTED`. Liên kết tường minh rút trực tiếp từ khai báo `inputs`, `pointers` hoặc AST.
- `INFERRED`. Liên kết do AI phát hiện qua phân tích ngữ nghĩa tài liệu ở Phase 2 và Phase 3.
- `AMBIGUOUS`. Liên kết nghi ngờ, cần con người xác nhận trong hàng đợi trước khi khóa.

### Tầng 2 · Mở rộng lên `ak-graphify` và `gstack /sync-gbrain` (Khi quy mô >= 500 thành phần)

Khi tổ chức có hàng nghìn tệp tài liệu kết hợp cùng kho mã nguồn phần mềm, xem giao thức chi tiết tại `references/hybrid-indexing-and-gbrain.md` để kết nối `dependency-index.csv` với đồ thị `graphify-out/graph.json` và bộ nhớ `gbrain` (có kiểm tra `brain_trust_policy` và kiểm toán rò rỉ `--audit`).

## Thành phần 6 & 7 · Hàng đợi Quyết định `D<N>` (`queues/`) và Bảng Kiểm kê (`manifest.csv`)

- `queues/conflict-queue.md`. Chứa các thẻ quyết định `Decision Brief D<N>` cho mọi xung đột giá trị giữa các nguồn.
- `queues/unclassified-queue.md`. Chứa các thẻ `D<N>` cho các tài liệu pha trộn nhiều xuất xứ cần con người quyết định cách tách.
- `queues/migration-map.md`. Bảng ánh xạ đường dẫn sao chép từ thư mục gốc sang `kernel-registry/` kèm biên bản kiểm chứng `ORIGINAL_TREE_FINGERPRINT`.
- `manifest.csv`. Danh mục trung tâm liệt kê toàn bộ các thành phần trong `Kernel Registry` cùng trạng thái độ tươi (`FRESH / STALE / EXPIRED`).

## Tích hợp Liên thông Bộ 01 → Bộ 02 → Bộ 03

Xem đặc tả kỹ thuật chi tiết và script chuyển đổi tự động tại `references/bo01-bo02-bo03-bridge.md`.
- **Từ Bộ 01 sang Bộ 02.** Mọi thẻ `Fact Card` có `trust_tier: verified` từ Bộ 01 được ánh xạ tự động sang tệp `L1-stored-fact.yaml` trong `registry/stored-facts/` với trường `source.bo01_fact_id` giữ nguyên liên kết truy ngược.
- **Từ Bộ 02 sang Bộ 03 (`Vibecode Kit v6.2 × pstack`).** Trong bước `SCAN`, `RRI`, `BLUEPRINT` và `BUILD` của Bộ 03, Chủ thầu và Thợ truy xuất trực tiếp `manifest.csv` cùng bản đồ tính năng `references/features/README.md` (`Feature Map`), nhúng mã định danh `[L1-*]`, `[L2-*]`, `[OBL-*]`, `[L4-*]` vào bảng tiêu chí nghiệm thu (`REQ-ID`) và câu lệnh kiểm chứng sống `./bin/control-app`. Ở Bước 8 (`SHIP`), tác vụ `/maintain-verification-skill` tự động cập nhật mã băm SHA-256 của từng tính năng trong `Feature Map` và đồng bộ ngược về `manifest.csv` của Bộ 02 để đảm bảo tài liệu và mã nguồn không bao giờ bị trôi (`drift`).
