# Quick Start · Bộ 02 trong 15 phút

Hướng dẫn này giúp sinh viên thiết lập kernel registry đầu tiên trên một tập tài liệu nhỏ trong 15 phút.

## Bài toán mẫu

Sinh viên có một CLB Khởi nghiệp tại trường với tập tài liệu sau.

- Bảng đóng phí thành viên (CSV)
- Quy chế CLB (PDF)
- Voice CEO của club leader (markdown)
- Bảng tài chính tháng (Excel)

Mục tiêu là thiết lập kernel registry để CLB và một AI assistant nội bộ có thể truy cập đúng nguồn sự thật.

## Phút 0 đến 3 · Setup folder

Tạo cây thư mục theo Architecture.

```bash
mkdir -p kernel-registry/{registry/{stored-facts,derived-facts},obligations,style,skills,queues}
touch kernel-registry/manifest.csv
touch kernel-registry/dependency-index.csv
```

Khởi tạo manifest.csv với header.

```csv
component_id,component_type,path,domain,date_added,date_updated,status
```

Khởi tạo dependency-index.csv với header.

```csv
from_id,to_id,relationship,date_added
```

## Phút 3 đến 6 · Phân loại 4 tài liệu

Đi qua mỗi tài liệu và quyết định thuộc xuất xứ nào.

**Bảng đóng phí thành viên (CSV)**. Đây là dữ liệu cứng, mỗi entry là một fact về thành viên đã đóng phí. Thuộc L1.

**Quy chế CLB (PDF)**. Văn bản chứa các nghĩa vụ và quy định cho thành viên. Trích nghĩa vụ ra L3.

**Voice CEO của club leader (markdown)**. Đây là phán xét tự do về tone. Thuộc L4.

**Bảng tài chính tháng (Excel)**. Có cả số liệu thô (L1) và các tổng tính từ số liệu (L2). Cần tách.

## Phút 6 đến 10 · Tạo L1 và L3 entries

### L1 entry cho bảng đóng phí

Tạo file `registry/stored-facts/membership-fee-2026-q1.yaml`.

```yaml
fact_id: L1-membership-fee-2026-Q1
fact_type: L1
domain: membership-finance
key: total-fee-collected-2026-Q1
value: 4500000
unit: VND
source:
  type: internal-document
  document_id: membership-fee-log
  document_path: docs/membership-fee-2026-Q1.csv
date_effective: 2026-04-01
date_updated: 2026-04-15
updated_by: human
status: active
notes: "Tổng phí thu được Q1 2026 từ 30 thành viên"
```

Cập nhật manifest.csv.

```csv
L1-membership-fee-2026-Q1,L1-stored-fact,registry/stored-facts/membership-fee-2026-q1.yaml,membership-finance,2026-04-15,2026-04-15,active
```

### L3 entry cho quy chế CLB

Tạo thư mục `obligations/club-charter-2026/` và file `obligations.yaml`.

```yaml
source_metadata:
  source_id: club-charter-2026
  title: "Quy chế CLB Khởi nghiệp 2026"
  authority: "Ban điều hành CLB"
  date_issued: 2026-01-15
  date_effective: 2026-01-15

obligations:
  - obligation_id: OBL-club-charter-001
    description: "Thành viên đóng phí 150000 VND mỗi quý"
    article: "Điều 3, khoản 1"
    severity: medium
    applies_to: all-members
    date_added: 2026-04-15

  - obligation_id: OBL-club-charter-002
    description: "Thành viên phải tham gia ít nhất 1 hoạt động mỗi tháng"
    article: "Điều 4, khoản 1"
    severity: low
    applies_to: all-members
    date_added: 2026-04-15
```

Copy quy chế PDF vào `obligations/club-charter-2026/source-doc.pdf`.

Cập nhật manifest.csv.

```csv
club-charter-2026,obligation-source,obligations/club-charter-2026/,membership-rules,2026-04-15,2026-04-15,active
```

## Phút 10 đến 12 · Tạo L4 voice book

Copy voice của CEO vào `style/voice-guide.md`.

Không cần schema cứng cho L4. Chỉ cần lưu prose có cấu trúc dễ đọc.

```markdown
# Voice Guide · CLB Khởi nghiệp

## Tone tổng quát
Trẻ trung, năng động, hướng hành động. Không quá formal,
nhưng cũng không slangy.

## Vocabulary ưa thích
- "Chiến binh khởi nghiệp" cho thành viên active
- "Sandbox" cho không gian thử ý tưởng

## Vocabulary cấm
- "Anh em" trong văn bản chính thức
- "Combo" trong tài liệu seminar
```

Cập nhật manifest.csv.

```csv
style-voice-guide,L4-style,style/voice-guide.md,brand-voice,2026-04-15,2026-04-15,active
```

## Phút 12 đến 14 · Tạo L2 từ bảng tài chính

Trong bảng tài chính có một cell "Tổng chi tháng" = sum của các cột chi tiết. Đây là L2.

Tạo file `registry/derived-facts/total-expense-2026-04.yaml`.

```yaml
fact_id: L2-total-expense-2026-04
fact_type: L2
domain: club-finance
key: total-expense-month-04-2026
formula:
  type: sum
  inputs:
    - L1-rent-2026-04
    - L1-printing-2026-04
    - L1-event-cost-2026-04
unit: VND
date_updated: 2026-05-01
status: active
notes: "Tổng chi tháng 4 = thuê + in ấn + sự kiện"
```

Nếu các L1 inputs chưa được tạo, đẩy vào TODO list (sẽ làm cycle sau).

## Phút 14 đến 15 · Cập nhật dependency index

Thêm các quan hệ vào dependency-index.csv.

```csv
L2-total-expense-2026-04,L1-rent-2026-04,derives-from,2026-05-01
L2-total-expense-2026-04,L1-printing-2026-04,derives-from,2026-05-01
L2-total-expense-2026-04,L1-event-cost-2026-04,derives-from,2026-05-01
OBL-club-charter-001,club-charter-2026,extracted-from,2026-04-15
OBL-club-charter-002,club-charter-2026,extracted-from,2026-04-15
```

## Đã xong cycle 1

Sinh viên đã thiết lập kernel registry với 4 thành phần.

- 1 L1 entry (tổng phí thu được)
- 1 L2 entry (tổng chi tháng, với inputs chưa tạo)
- 2 L3 entries (nghĩa vụ từ quy chế CLB)
- 1 L4 entry (voice guide)
- 1 dependency index ban đầu
- 1 manifest đầy đủ

Registry chưa đầy đủ. Còn cần tạo L1 inputs cho L2, thêm các nghĩa vụ khác trong quy chế, mở rộng voice guide. Đó là việc cho cycle sau.

## Bước tiếp theo

Cycle 2 hoàn thành registry cho lĩnh vực tài chính của CLB.

Cycle 3 tạo skill đầu tiên reference các L1 L3 L4 entries. Ví dụ skill "Sinh báo cáo tài chính tháng".

Cycle 4 trở đi mở rộng sang các lĩnh vực khác (events, marketing, members).

Đọc Methodology.md để hiểu vì sao phân tách 4 xuất xứ. Đọc Architecture.md khi cần scale lên hoặc tích hợp với tools khác.
