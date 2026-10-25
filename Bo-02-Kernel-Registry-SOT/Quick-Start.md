# Quick Start · Bộ 02 v2.0 trong 15 phút

Hướng dẫn này giúp bạn thiết lập một **Kernel Registry v2.0** đầu tiên (có kiểm toán độ tươi bằng mã băm, tính công thức `L2` tất định và kiểm chứng bảo toàn bản gốc `Copy-Only Scope Freeze`) trên một tập tài liệu mẫu chỉ trong 15 phút.

## Bài toán mẫu

Một Câu lạc bộ Khởi nghiệp Công nghệ có 4 tài liệu đang nằm lẫn lộn trong thư mục `raw-club-docs/`.
1. `membership-fee-2026-Q4.csv` (Bảng thu phí thành viên Quý 4).
2. `sponsor-grant-2026-Q4.csv` (Bảng tài trợ nhận được trong Quý 4).
3. `club-charter-2026.pdf` (Quy chế hoạt động chính thức của CLB).
4. `leader-voice.md` (Ghi chú phong cách truyền thông của Chủ nhiệm CLB).

Mục tiêu là dựng `kernel-registry/` theo 4 xuất xứ `L1`, `L2`, `L3`, `L4` để AI Agent nội bộ trả lời chính xác câu hỏi tài chính và quy chế mà không làm hỏng thư mục gốc.

## Phút 0 đến 3 · Khởi tạo Cấu trúc và Chụp Dấu vân tay Gốc (`Phase 1`)

Tạo cây thư mục `kernel-registry/` và ghi nhận mã băm của thư mục tài liệu gốc để đảm bảo kỷ luật `Copy-Only Scope Freeze`.

```bash
mkdir -p kernel-registry/{registry/{stored-facts,derived-facts},obligations/club-charter-2026,style,skills,queues}
```

Khởi tạo `kernel-registry/manifest.csv` và `kernel-registry/dependency-index.csv`.

```csv
# kernel-registry/manifest.csv
component_id,component_type,path,domain,source_hash,date_added,date_updated,freshness_status,status
```

```csv
# kernel-registry/dependency-index.csv
from_id,to_id,relationship,provenance_tag,impact_if_stale,date_added,notes
```

## Phút 3 đến 6 · Phân loại 4 Tài liệu theo 4 Xuất xứ (`Phase 2 & 3`)

- **Bảng thu phí (`membership-fee-2026-Q4.csv`) và Bảng tài trợ (`sponsor-grant-2026-Q4.csv`).** Dữ liệu định lượng cứng đo đếm được. Đưa vào **`L1`** (`registry/stored-facts/`).
- **Tổng ngân sách hoạt động Quý 4.** Tính bằng tổng phí thành viên cộng tiền tài trợ. Đưa vào **`L2`** (`registry/derived-facts/`).
- **Quy chế CLB (`club-charter-2026.pdf`).** Văn bản quy định quyền và nghĩa vụ bắt buộc. Trích các điều khoản vào **`L3`** (`obligations/club-charter-2026/obligations.yaml`).
- **Phong cách truyền thông (`leader-voice.md`).** Phán xét tự do về giọng điệu, đứng ngoài đường kiểm cơ học. Đưa vào **`L4`** (`style/`).

## Phút 6 đến 10 · Tạo Mục `L1`, `L3` và `L4` kèm Mã băm Độ tươi (`Phase 5 · Bước 1`)

### 1. Tạo hai mục `L1` trong `registry/stored-facts/`

File `kernel-registry/registry/stored-facts/L1-membership-fee-2026-Q4.yaml`.

```yaml
fact_id: L1-membership-fee-2026-Q4
fact_type: L1
domain: club-finance
key: total-membership-fee-2026-Q4
value: 4500000
unit: VND
source:
  type: internal-document
  document_id: membership-fee-log-Q4
  document_path: raw-club-docs/membership-fee-2026-Q4.csv
  source_hash: "sha256:3a7bd3e2"
date_effective: 2026-10-01
date_expires: 2026-12-31
date_updated: 2026-10-25
updated_by: human
verification_status: FRESH
status: active
notes: "Tổng phí thu từ 30 thành viên trong Quý 4/2026"
```

File `kernel-registry/registry/stored-facts/L1-sponsor-grant-2026-Q4.yaml`.

```yaml
fact_id: L1-sponsor-grant-2026-Q4
fact_type: L1
domain: club-finance
key: total-sponsor-grant-2026-Q4
value: 15000000
unit: VND
source:
  type: internal-document
  document_id: sponsor-grant-log-Q4
  document_path: raw-club-docs/sponsor-grant-2026-Q4.csv
  source_hash: "sha256:8c14f9b0"
date_effective: 2026-10-01
date_expires: 2026-12-31
date_updated: 2026-10-25
updated_by: human
verification_status: FRESH
status: active
notes: "Khoản tài trợ sự kiện Hackathon Quý 4/2026"
```

### 2. Tạo sổ nghĩa vụ `L3` trong `obligations/club-charter-2026/obligations.yaml`

```yaml
source_metadata:
  source_id: club-charter-2026
  title: "Quy chế Hoạt động CLB Khởi nghiệp 2026"
  authority: "Ban Chủ nhiệm CLB"
  date_issued: 2026-01-15
  date_effective: 2026-01-15
  source_document_path: "./source-doc.pdf"
  source_hash: "sha256:5d22a1e9"
  verification_status: FRESH

obligations:
  - obligation_id: OBL-club-charter-001
    description: "Thành viên chính thức đóng phí hoạt động 150.000 VND mỗi quý trước ngày 15 của tháng đầu quý"
    article: "Điều 3, khoản 1"
    severity: medium
    applies_to: all-active-members
    compliance_check_type: financial-check
    date_added: 2026-10-25
    status: active
```

### 3. Tạo hồ sơ phong cách `L4` trong `style/`

Sao chép `leader-voice.md` vào `kernel-registry/style/voice-guide.md` và tạo tệp định danh `kernel-registry/style/L4-style.yaml` với `verification_mode: non-mechanically-verifiable`.

## Phút 10 đến 13 · Tạo Công thức `L2` và Tính toán Tất định (`Phase 5 · Bước 2`)

Tạo tệp `kernel-registry/registry/derived-facts/L2-total-budget-2026-Q4.yaml`. Thay vì nhẩm tính, lưu rõ công thức cộng hai đầu vào `L1` và ghi dấu vết kiểm toán `audit_trace`.

```yaml
fact_id: L2-total-budget-2026-Q4
fact_type: L2
domain: club-finance
key: total-budget-2026-Q4
formula:
  type: sum
  expression: "L1_membership_fee + L1_sponsor_grant"
  inputs:
    - L1-membership-fee-2026-Q4
    - L1-sponsor-grant-2026-Q4
computed_cache:
  last_computed_value: 19500000
  unit: VND
  computed_at: 2026-10-25T10:40:00Z
  input_hashes:
    L1-membership-fee-2026-Q4: "sha256:3a7bd3e2"
    L1-sponsor-grant-2026-Q4: "sha256:8c14f9b0"
  audit_trace: "4500000 + 15000000 = 19500000"
verification_status: FRESH
status: active
notes: "Tổng ngân sách Quý 4 = Phí thành viên + Tài trợ"
```

## Phút 13 đến 15 · Cập nhật `manifest.csv` và `dependency-index.csv`

Điền danh mục vào `kernel-registry/manifest.csv`.

```csv
component_id,component_type,path,domain,source_hash,date_added,date_updated,freshness_status,status
L1-membership-fee-2026-Q4,L1-stored-fact,registry/stored-facts/L1-membership-fee-2026-Q4.yaml,club-finance,sha256:3a7bd3e2,2026-10-25,2026-10-25,FRESH,active
L1-sponsor-grant-2026-Q4,L1-stored-fact,registry/stored-facts/L1-sponsor-grant-2026-Q4.yaml,club-finance,sha256:8c14f9b0,2026-10-25,2026-10-25,FRESH,active
L2-total-budget-2026-Q4,L2-derived-fact,registry/derived-facts/L2-total-budget-2026-Q4.yaml,club-finance,sha256:computed,2026-10-25,2026-10-25,FRESH,active
club-charter-2026,L3-obligation-source,obligations/club-charter-2026/obligations.yaml,club-governance,sha256:5d22a1e9,2026-10-25,2026-10-25,FRESH,active
L4-club-voice,L4-style,style/L4-style.yaml,brand-voice,sha256:none,2026-10-25,2026-10-25,N/A,active
```

Điền dây chuyền phụ thuộc vào `kernel-registry/dependency-index.csv`.

```csv
from_id,to_id,relationship,provenance_tag,impact_if_stale,date_added,notes
L2-total-budget-2026-Q4,L1-membership-fee-2026-Q4,derives-from,EXTRACTED,recompute-l2,2026-10-25,"Đầu vào phí thành viên"
L2-total-budget-2026-Q4,L1-sponsor-grant-2026-Q4,derives-from,EXTRACTED,recompute-l2,2026-10-25,"Đầu vào tiền tài trợ"
OBL-club-charter-001,club-charter-2026,extracted-from,EXTRACTED,review-obligation,2026-10-25,"Trích từ Điều 3 khoản 1"
```

## Hoàn tất Cycle 1 và Bước tiếp theo

Chỉ trong 15 phút, bạn đã dựng xong một `Kernel Registry v2.0` chuẩn mực.
- Bốn loại tri thức (`L1`, `L2`, `L3`, `L4`) nằm đúng kho chuyên biệt.
- Khi tệp `membership-fee-2026-Q4.csv` thay đổi, mã băm `source_hash` sẽ báo hiệu ngay cho `L1-membership-fee-2026-Q4` và `L2-total-budget-2026-Q4` biết cần cập nhật lại.
- Thư mục tài liệu gốc `raw-club-docs/` được bảo toàn nguyên vẹn 100%.

Đọc tiếp `Methodology.md`, `Architecture.md` và 3 giao thức trong `references/` để áp dụng cho các dự án doanh nghiệp lớn và kết nối với Bộ 01 cùng Bộ 03.
