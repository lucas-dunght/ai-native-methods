# Giao thức Kiểm toán Độ tươi SHA-256 & Bộ tính `L2` Tất định (`Freshness & Deterministic L2 Protocol`)

Tài liệu này định nghĩa hai cơ chế kỹ thuật bảo vệ độ chính xác của kho `registry/` (`L1` và `L2`) và kho `obligations/` (`L3`) trong Bộ 02 v2.0.

## 1. Kiểm toán Độ tươi bằng Mã băm (`SHA-256 Freshness Audit`)

### Vấn đề của các Kho Tri thức Truyền thống

Khi một tệp bảng giá PDF hoặc một văn bản quy chế gốc được cập nhật bản mới trên đĩa nhưng người vận hành quên cập nhật tệp YAML trong `registry/`, AI Agent sẽ tiếp tục đọc con số cũ mà không hề hay biết.

### Thực thi Tất định qua Công cụ CLI `scripts/bo02_registry_tool.py` (`& scripts/eval_l2.py`)

Thay vì viết tay các đoạn mã kiểm toán ở mỗi phiên, sử dụng trực tiếp công cụ CLI chuẩn Deep Module đi kèm Bộ 02:

```bash
# 1. Chụp dấu vân tay ORIGINAL_TREE_FINGERPRINT (SHA-256 luồng 64KB) bảo chứng Copy-Only Scope Freeze
python3 Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py fingerprint --dir raw-docs --json

# 2. Kiểm toán độ tươi L1 và tự động lan truyền STALE qua dependency-index.csv
python3 Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py audit-freshness \
  --l1-file kernel-registry/registry/stored-facts \
  --base-dir . \
  --dependency-index kernel-registry/dependency-index.csv \
  --json

# 3. Tính công thức L2 qua trình thông dịch AST Safe Evaluator (0% dùng hàm eval() mở)
python3 Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py eval-l2 \
  --id L2-domain-key-NNN \
  --l2-file Bo-02-Kernel-Registry-SOT/templates/L2-derived-fact.yaml \
  --json

# Hoặc gọi qua wrapper tương thích ngược được khai báo trong deterministic_eval_cmd:
python3 Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py --id L2-domain-key-NNN --json
```

### Cơ chế 3 Trạng thái Độ tươi (`FRESH | STALE | EXPIRED`)

Mỗi tệp `L1-stored-fact.yaml` và `L3-obligation.yaml` bắt buộc lưu trường `source_hash` (16 ký tự đầu hoặc toàn bộ mã băm SHA-256 tính trên tệp tài liệu gốc tại thời điểm trích xuất) và trường `date_expires`.

Trước mỗi đợt xuất báo cáo hoặc chạy `Skill` quan trọng, `bo02_registry_tool.py audit-freshness` thực thi thuật toán kiểm toán độ tươi dưới đây.

```python
import datetime, hashlib, os, yaml

def compute_file_hash(path):
    if not os.path.exists(path):
        return "MISSING_SOURCE_FILE"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return f"sha256:{h.hexdigest()[:16]}"

def audit_l1_entry(yaml_path, today=None):
    today = today or datetime.date.today().isoformat()
    with open(yaml_path, "r", encoding="utf-8") as f:
        entry = yaml.safe_load(f)

    expires = str(entry.get("date_expires") or "")
    if expires and expires != "null" and expires < today:
        return "EXPIRED"

    src = entry.get("source", {})
    doc_path = src.get("document_path")
    recorded_hash = src.get("source_hash")
    if doc_path and recorded_hash:
        live_hash = compute_file_hash(doc_path)
        if live_hash != recorded_hash:
            return "STALE"
    return "FRESH"
```

### Lan truyền Trạng thái `STALE` qua `dependency-index.csv`

Khi một mục `L1-X` hoặc `OBL-Y` bị phát hiện chuyển sang `STALE` hoặc `EXPIRED`, hệ thống tra cứu `dependency-index.csv` để tìm toàn bộ các thành phần có `to_id == L1-X` hoặc `to_id == OBL-Y` và tự động đánh dấu cảnh báo theo cột `impact_if_stale`.
- Với mục `L2` (`recompute-l2`). Chuyển trạng thái của `L2` sang `STALE` và yêu cầu chạy lại bộ tính tất định.
- Với gói `Skill` (`block-skill-output`). Chặn không cho `Skill` xuất báo cáo chính thức cho tới khi mục dữ liệu gốc được làm mới (`FRESH`).

## 2. Bộ tính Công thức `L2` Tất định (`Deterministic L2 Evaluator`)

### Quy tắc Cấm AI Nhẩm tính (`Zero Mental Math Rule`)

Mô hình ngôn ngữ lớn rất giỏi suy luận ngữ nghĩa nhưng có thể mắc lỗi số học khi cộng hàng chục dòng dự toán hoặc nhân tỷ giá nhiều chữ số thập phân. Do đó, trong Bộ 02 v2.0, AI Agent **không bao giờ tự tính giá trị `L2` trong câu trả lời**, mà bắt buộc chạy script tính toán tất định từ các tệp `L1` đầu vào.

### Quy trình Tính toán và Ghi dấu vết `audit_trace`

1. Đọc tệp `L2-*.yaml`, lấy danh sách `formula.inputs`.
2. Kiểm tra từng tệp `L1` trong `formula.inputs`. Nếu bất kỳ tệp `L1` nào không ở trạng thái `FRESH` hoặc `status != active`, dừng lại và báo lỗi `STALE_INPUT`.
3. Thực thi phép tính (`sum`, `product`, `ratio`, `difference`, hoặc biểu thức `custom` trong môi trường Python an toàn chỉ chứa các biến số `L1`).
4. Ghi kết quả vào `computed_cache.last_computed_value`, lưu bảng mã băm `input_hashes` của từng đầu vào `L1` và ghi chuỗi phép tính tường minh vào `audit_trace` (ví dụ `"4500000 + 15000000 = 19500000"`).
