# Architecture · Kiến trúc Kernel Registry

## Tổng quan

Hệ thống gồm ba kho lưu trữ chính cộng một dependency index cộng hai hàng đợi human. Tổng cộng sáu thành phần. Mọi thành phần dùng định dạng văn bản đơn giản (YAML, CSV, Markdown) để dễ version qua Git và dễ inspect bằng mắt.

Không có database engine bắt buộc. Có thể nâng cấp lên database sau khi scale lên.

## Sơ đồ thành phần

```
Kernel Registry (filesystem-based)
│
├── registry/                  Kho L1 + L2
│   ├── stored-facts/          L1 entries
│   │   ├── product-price-001.yaml
│   │   ├── capability-matrix-001.yaml
│   │   └── ...
│   └── derived-facts/         L2 entries
│       ├── total-revenue-Q1.yaml
│       └── ...
│
├── obligations/               Kho L3
│   ├── decree-XXX-2024/       Một thư mục cho mỗi nguồn pháp quy
│   │   ├── obligations.yaml   Các nghĩa vụ rút từ nguồn này
│   │   └── source-doc.pdf     Văn bản gốc lưu kèm
│   ├── circular-YYY-2024/
│   └── ...
│
├── style/                     Kho L4 (không trộn với registry)
│   ├── voice-guide.md
│   ├── tone-examples.md
│   └── ...
│
├── skills/                    Skills là gói nội dung
│   ├── skill-X/
│   │   ├── SKILL.md           Pointer tới registry và obligations
│   │   └── templates/
│   └── ...
│
├── dependency-index.csv       Quan hệ giữa các thành phần
│
├── queues/                    Hàng đợi human phán xử
│   ├── conflict-queue.md
│   └── unclassified-queue.md
│
└── manifest.csv               Inventory tất cả thành phần
```

## Thành phần 1 · Registry (L1 + L2)

### Subfolder stored-facts cho L1

Mỗi L1 entry là một file YAML có schema cố định.

```yaml
fact_id: L1-product-price-001
fact_type: L1
domain: product-pricing
value: 12500000
unit: VND
key: product-X-retail-price-2026-Q2
source:
  type: internal-document
  document_id: pricing-table-2026-Q2
  document_path: docs/pricing/pricing-table-2026-Q2.pdf
  page: 3
  cell: B7
date_effective: 2026-04-01
date_expires: 2026-06-30
date_updated: 2026-04-01
updated_by: human
status: active
notes: "Giá retail SKU X-001 cho Q2 2026"
```

Trường bắt buộc. fact_id, fact_type, domain, key, source, date_updated, status. Trường khác tuỳ chọn.

`status` thuộc tập {active, deprecated, superseded}. Khi entry deprecated, không xoá. Đánh dấu deprecated và thêm pointer tới entry mới superseded nó.

### Subfolder derived-facts cho L2

L2 entry không lưu giá trị mà lưu công thức.

```yaml
fact_id: L2-total-revenue-Q1-2026
fact_type: L2
domain: financial-metrics
key: total-revenue-Q1-2026
formula:
  type: sum
  inputs:
    - L1-revenue-product-A-Q1-2026
    - L1-revenue-product-B-Q1-2026
    - L1-revenue-product-C-Q1-2026
unit: VND
date_updated: 2026-04-15
updated_by: agent
status: active
notes: "Tổng doanh thu Q1 = sum của 3 sản phẩm"
```

Khi truy vấn L2, hệ thống tính giá trị từ công thức và inputs. Khi L1 inputs thay đổi, L2 tự cập nhật.

`formula.type` thuộc tập {sum, product, ratio, difference, custom}. Khi custom, có một field `formula.expression` chứa expression Python hoặc DSL.

### Truy vấn registry

API đơn giản dạng `get(fact_id)` hoặc `query(domain, key)`. Có thể implement bằng Python script vài chục dòng đọc YAML files. Không cần ORM hoặc database engine.

## Thành phần 2 · Obligations (L3)

Mỗi nguồn pháp quy (nghị định, thông tư, khung tiêu chuẩn) có một thư mục riêng.

```yaml
# decree-XXX-2024/obligations.yaml

source_metadata:
  source_id: decree-XXX-2024
  title: "Nghị định XXX/2024 về bảo vệ dữ liệu cá nhân"
  authority: "Chính phủ"
  date_issued: 2024-03-15
  date_effective: 2024-07-01

obligations:
  - obligation_id: OBL-decree-XXX-001
    description: "Tổ chức xử lý dữ liệu cá nhân phải có cán bộ bảo vệ dữ liệu cá nhân nếu xử lý dữ liệu của trên 10000 người"
    article: "Điều 5, khoản 2"
    severity: high
    applies_to: organizations-processing-personal-data
    date_added: 2024-04-01

  - obligation_id: OBL-decree-XXX-002
    description: "Phải thông báo cho cơ quan bảo vệ dữ liệu trong 72 giờ khi có sự cố lộ dữ liệu"
    article: "Điều 12, khoản 1"
    severity: high
    applies_to: all-data-controllers
    date_added: 2024-04-01

  - ...
```

Mỗi obligation có ID duy nhất theo format `OBL-source_id-NNN`. Khi nghị định được sửa đổi bổ sung, có thể thêm obligations mới hoặc đánh dấu obligations cũ deprecated, nhưng không xoá.

Văn bản gốc lưu kèm trong thư mục để có thể reference khi cần.

## Thành phần 3 · Style (L4)

Style book lưu prose, không structured. Không cố ép vào schema cứng.

```
style/
├── voice-guide.md         Tổng quan voice
├── tone-examples.md       Ví dụ tone cho các tình huống
├── vocabulary.md          Từ ngữ ưa thích và cấm
└── audience-profiles.md   Profile các nhóm khán giả
```

Style book có thể có version history qua Git nhưng không có công thức verify.

Khi skill cần style, skill reference path tới file style. Ví dụ trong SKILL.md viết "khi sinh văn bản, đọc style/voice-guide.md trước".

## Thành phần 4 · Skills (gói nội dung)

Mỗi skill là một thư mục với SKILL.md là pointer chính.

```markdown
# skills/skill-X/SKILL.md

# Skill X · Sinh báo cáo tài chính quý

## Khi nào dùng
[mô tả use case]

## Quy trình
1. Đọc dữ liệu từ registry. Reference:
   - L1-revenue-product-A-{quarter}
   - L1-revenue-product-B-{quarter}
   - L2-total-revenue-{quarter}

2. Đọc obligations áp dụng:
   - OBL-financial-disclosure-001
   - OBL-financial-disclosure-002

3. Sinh báo cáo theo style:
   - style/voice-guide.md
   - style/audience-profiles.md (chọn profile board-of-directors)

4. Output format theo template:
   - skills/skill-X/templates/quarterly-report.md
```

Skill không có sách luật riêng. Mọi obligation, mọi data fact, mọi style được reference qua pointer.

## Thành phần 5 · Dependency Index

Một file CSV duy nhất theo dõi quan hệ giữa các thành phần.

```csv
from_id,to_id,relationship,date_added
L2-total-revenue-Q1-2026,L1-revenue-product-A-Q1-2026,derives-from,2026-04-15
L2-total-revenue-Q1-2026,L1-revenue-product-B-Q1-2026,derives-from,2026-04-15
OBL-decree-XXX-001,decree-XXX-2024,extracted-from,2024-04-01
skill-X,L1-revenue-product-A-Q1-2026,references,2026-04-15
skill-X,OBL-financial-disclosure-001,must-comply,2026-04-15
skill-X,style/voice-guide.md,uses,2026-04-15
```

Relationships hợp lệ. derives-from, extracted-from, references, must-comply, uses, supersedes, deprecates.

Khi cần audit "Nghị định XXX thay đổi thì những thành phần nào bị ảnh hưởng", grep dependency index với `to_id` = `decree-XXX-2024`. Output là danh sách trực tiếp, có thể follow chain.

## Thành phần 6 · Queues

### Conflict queue

Khi phase 3 phát hiện hai L1 entries nói khác nhau về cùng một sự thật, đẩy vào conflict queue.

```markdown
# queues/conflict-queue.md

## Conflict C-001
- Date: 2026-04-20
- Entry A: L1-product-price-001 nói giá X = 12.5 triệu VND, nguồn pricing-table-2026-Q2 trang 3
- Entry B: L1-product-price-001-alt nói giá X = 13.0 triệu VND, nguồn pricing-table-2026-Q2-revised trang 3
- Đề xuất phán xử của agent: Entry B có file revised, có thể là bản update của Entry A. Cần user xác nhận.
- Quyết định của user: [chưa quyết]
- Người phán xử: [...]
- Ngày phán xử: [...]
```

### Unclassified queue

Khi phase 2 phát hiện file không rõ thuộc L1/L2/L3/L4, đẩy vào unclassified queue.

```markdown
# queues/unclassified-queue.md

## Unclassified U-001
- File: docs/strategy/board-meeting-notes-2026-Q1.md
- Phát hiện: file chứa cả số liệu (như L1), nghĩa vụ về reporting (như L3) và voice của CEO (như L4)
- Đề xuất: tách thành 3 phần và đẩy mỗi phần vào kho tương ứng
- Quyết định của user: [chưa quyết]
```

Queues phải được clear định kỳ, không tích đọng.

## Thành phần 7 · Manifest

Inventory toàn bộ thành phần trong kernel registry.

```csv
component_id,component_type,path,domain,date_added,date_updated,status
L1-product-price-001,L1-stored-fact,registry/stored-facts/product-price-001.yaml,product-pricing,2026-04-01,2026-04-01,active
L2-total-revenue-Q1-2026,L2-derived-fact,registry/derived-facts/total-revenue-Q1.yaml,financial-metrics,2026-04-15,2026-04-15,active
decree-XXX-2024,obligation-source,obligations/decree-XXX-2024/,data-protection,2024-04-01,2024-04-01,active
skill-X,skill,skills/skill-X/,reporting,2026-04-15,2026-04-15,active
```

Manifest là entry point để hệ thống biết có gì trong registry. Khi audit hoặc khi nạp registry vào AI agent context, đọc manifest trước.

## Luồng vận hành

### Thêm một fact mới

1. Determine L1 hay L2 hay L3 hay L4.
2. Tạo file YAML theo template tương ứng.
3. Gán ID duy nhất.
4. Cập nhật manifest.csv.
5. Nếu fact phụ thuộc fact khác, cập nhật dependency-index.csv.
6. Commit qua Git.

### Truy vấn fact

1. AI agent hoặc human nhận query.
2. Đọc manifest.csv để xác định component_id liên quan.
3. Đọc file tương ứng để get giá trị hoặc reference.
4. Đối với L2, tính giá trị từ formula và inputs.
5. Trả về kết quả với metadata về nguồn.

### Cập nhật một thông tư

1. Cập nhật obligations.yaml trong thư mục thông tư đó.
2. Đánh dấu obligations cũ deprecated, thêm obligations mới.
3. Grep dependency-index.csv để tìm các thành phần phụ thuộc.
4. Review từng thành phần phụ thuộc, cập nhật nếu cần.
5. Commit qua Git với commit message rõ thông tư nào đã được cập nhật.

### Audit khi có incident

1. Identify entry point của incident (báo cáo sai, quyết định sai).
2. Trace ngược qua dependency-index.csv.
3. Identify root cause (L1 sai, công thức L2 sai, obligation thay đổi mà skill không update, style chỉ dẫn sai).
4. Fix root cause.
5. Re-run các thành phần phụ thuộc để propagate fix.

## Versioning

Toàn bộ registry trong một Git repo. Mỗi thay đổi là một commit. Commit message theo format `[L1|L2|L3|L4|skill|dep] <component_id>: <hành động>`. Ví dụ `[L1] product-price-001: update giá Q2 2026`.

Tags Git cho các phiên bản registry được công bố nội bộ. Ví dụ `registry-v2026.06`.

## Tools đề xuất

Đối với tổ chức nhỏ hoặc dự án sinh viên.

Storage. Git repo với markdown, YAML, CSV files.
Search. ripgrep hoặc git grep cho find theo content.
Versioning. Git.
CI. GitHub Actions hoặc GitLab CI cho validation YAML schema và check dependency consistency.

Đối với tổ chức lớn hoặc khi scale lên hàng ngàn entries.

Storage. PostgreSQL với JSONB cho YAML content, hoặc DuckDB cho query analytics.
Search. Elasticsearch hoặc Meilisearch.
Versioning. Git LFS hoặc DVC.
Pipeline. Airflow hoặc Prefect cho ETL.

Không upgrade lên stack lớn quá sớm. Bắt đầu với filesystem-based, scale up khi có evidence cụ thể.

## Tích hợp với Bộ 01

Output của Bộ 01 (fact cards) là L1-equivalent. Sinh viên có thể convert fact cards thành L1 entries bằng một script ETL đơn giản. Schema fact card được thiết kế tương thích với schema L1.

## Tích hợp với Bộ 03

Khi Vibecode Kit (Bộ 03) được dùng để xây ứng dụng, AI agent có thể access kernel registry để có context chính xác. Skills của Bộ 03 reference registry entries qua ID, đảm bảo agent không drift hoặc fabricate.
