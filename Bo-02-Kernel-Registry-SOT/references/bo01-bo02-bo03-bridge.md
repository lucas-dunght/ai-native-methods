# Giao thức Liên thông Tự động Bộ 01 → Bộ 02 → Bộ 03 (`Three-Suite AI-Native Bridge`)

Tài liệu này định nghĩa đường ống dữ liệu xuyên suốt ba bộ phương pháp trong hệ sinh thái `ai-native-methods` gồm **Bộ 01 (Tinh lọc thông tin Internet v2.0)**, **Bộ 02 (Kernel Registry SOT v2.0)** và **Bộ 03 (Vibecode Kit v6.2 × pstack)**.

## 1. Sơ đồ Liên thông Tổng thể

```
┌─────────────────────────────────────────────────────────────────┐
│ BỘ 01 · TINH LỌC THÔNG TIN INTERNET (v2.0)                      │
│ - Thu thập đa tín hiệu + Lọc cô lập PTC + Khử phòng vang        │
│ - Đầu ra: Tập thẻ fact-cards/F-YYYY-NNN.yaml (verified)         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        [Chặng 1: Cầu nối ETL Bộ 01 -> Bộ 02 (Fact Card -> L1)]
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ BỘ 02 · KERNEL REGISTRY & NGUỒN SỰ THẬT (v2.0)                  │
│ - Kho registry/ (L1 + L2 tất định), obligations/ (L3), style/   │
│ - Kiểm toán độ tươi SHA-256 (FRESH / STALE / EXPIRED)           │
│ - Đầu ra: Hệ thống Con trỏ [L1-*], [L2-*], [OBL-*], [L4-*]      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        [Chặng 2: Cầu nối Bộ 02 <-> Bộ 03 (Pointers + Feature Map)]
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ BỘ 03 · VIBECODE KIT (v6.2 × pstack)                            │
│ - Chủ thầu đọc Feature Map & nhúng [L1-*], [OBL-*] vào Blueprint│
│ - Thợ thi công theo Type Signatures Sketch & ./bin/control-app  │
│ - Bước 8 chạy /maintain-verification-skill đồng bộ SHA-256      │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Chặng 1 · Chuyển đổi `Fact Card` (Bộ 01) sang `L1 Stored Fact` (Bộ 02)

### Điều kiện qua cổng (`Gate Criteria`)

Chỉ những thẻ `Fact Card` của Bộ 01 thỏa mãn đồng thời 3 điều kiện sau mới được phép nhập tự động vào kho `registry/stored-facts/` (`L1`) của Bộ 02.
1. `trust_tier == "verified"`.
2. `claim_label` là `OBSERVED` hoặc `DERIVED` (tuyệt đối không nhập thẻ `PRIOR` hay `ASSUMED`).
3. Không nằm trong bất kỳ mục xung đột nào chưa giải quyết của `conflict-queue.md`.

### Quy tắc Ánh xạ Trường dữ liệu (`Schema Mapping`)

| Trường trong `fact-card.yaml` (Bộ 01) | Trường tương ứng trong `L1-stored-fact.yaml` (Bộ 02) |
|---|---|
| `enrichment.bo02_bridge.suggested_fact_id` | `fact_id` (ví dụ `L1-sea-digital-payments-gtv-2024`) |
| `domain` | `domain` |
| `enrichment.bo02_bridge.numeric_value` (hoặc `content`) | `value` |
| `enrichment.bo02_bridge.unit` | `unit` |
| `fact_id` (`F-YYYY-NNN`) | `source.bo01_fact_id` |
| `content_hash` | `source.source_hash` |
| `date_extracted` | `date_updated` |

Đồng thời, tự động thêm một dòng vào `dependency-index.csv` của Bộ 02.

```csv
L1-sea-digital-payments-gtv-2024,F-2026-001,imported-from,EXTRACTED,reverify-bo01-card,2026-10-25,"Nhập tự động từ chu kỳ nghiên cứu Bộ 01"
```

## 3. Chặng 2 · Kết nối `Kernel Registry` (Bộ 02) vào `Vibecode Kit v6.2 × pstack` (Bộ 03)

Khi xây dựng phần mềm hoặc giải pháp số bằng **Bộ 03 (`Vibecode Kit v6.2 × pstack`)**, kho `Kernel Registry` của Bộ 02 kết hợp cùng bản đồ tính năng `Feature Map` (`references/features/README.md`) đóng vai trò là bộ nhớ nền tảng chống bịa đặt (`Anti-Hallucination Grounding`).

1. **Ở Bước 1 (`SCAN`) và Bước 2 (`RRI`) của Bộ 03.**
   - Chủ thầu (`Contractor`) đọc `manifest.csv` của Bộ 02 cùng `references/features/README.md` (`Feature Map`) trước tiên để tự trả lời các câu hỏi về đơn giá, công thức tính phí (`L1`, `L2`), quy định pháp lý bắt buộc (`L3`), phong cách thương hiệu (`L4`) và câu lệnh `./bin/control-app` chạm tới từng màn hình mà không cần hỏi lại Con người những điều đã có trong kho.
2. **Ở Bước 4 (`BLUEPRINT`) và Bước 5 (`TASK GRAPH / TIP`) của Bộ 03.**
   - Mọi yêu cầu chức năng (`REQ-ID`) và khung chữ ký kiểu (`Type Signatures Sketch`) liên quan đến số liệu hoặc quy tắc tuân thủ đều phải gắn kèm mã con trỏ của Bộ 02 (ví dụ `REQ-04 · Tính phí giao dịch theo công thức [L2-cross-border-fee] và tuân thủ [OBL-decree-13-001]`).
3. **Ở Bước 6 (`BUILD`), Bước 7 (`VERIFY`) và Bước 8 (`SHIP`) của Bộ 03.**
   - Thợ (`Builder`) đọc giá trị trực tiếp từ tệp YAML của Bộ 02 để viết bài kiểm thử đơn vị (`unit-test`) và chạy kiểm chứng sống qua `./bin/control-app --json`.
   - Khi nghiệm thu ở Bước 7 và phát hành ở Bước 8, Chủ thầu kiểm tra dấu vân tay `WTREE_FINGERPRINT` của mã nguồn (Bộ 03), trạng thái `verification_status == FRESH` của các con trỏ dữ liệu (Bộ 02) và chạy `/maintain-verification-skill` để cập nhật mã băm SHA-256 trong `Feature Map`.
