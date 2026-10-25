---
name: kernel-registry-sot
version: "2.0.0"
description: Tổ chức tri thức theo bốn xuất xứ L1 (Sự thật lưu sẵn), L2 (Sự thật dẫn xuất), L3 (Nghĩa vụ pháp quy), L4 (Phong cách tự do) với ba kho registry, obligations, style. Tích hợp kiểm toán độ tươi bằng mã băm (FRESH/STALE/EXPIRED), bộ tính L2 tất định bằng script, phân tầng chỉ mục từ CSV lên ak-graphify và gstack /sync-gbrain (kèm brain_trust_policy), cổng duyệt Decision Brief D<N>, khóa phạm vi chỉ sao chép (Copy-Only Scope Freeze) và cầu nối ETL liên thông Bộ 01 -> Bộ 02 -> Bộ 03. Kích hoạt khi: "tổ chức lại tri thức", "xây kernel registry", "thiết lập SOT", "refactor knowledge base", "phân loại tài liệu nội bộ", "tổ chức bảng giá BOM văn bản pháp quy".
license: MIT
---

# Kernel Registry SOT Skill · v2.0 (2026.10)

## Mục đích

Skill này hướng dẫn AI Agent đi qua năm phase của phương pháp **Kernel Registry v2.0** để tổ chức lại tri thức phân tán của một tổ chức hoặc dự án theo bốn xuất xứ `L1`, `L2`, `L3`, `L4`. Agent thực thi kiểm kê, tính mã băm kiểm chứng độ tươi, phát hiện xung đột và dựng cấu trúc mới bằng sao chép an toàn. Con người phán xử các xung đột sự thật và ký duyệt bản đồ di trú qua thẻ quyết định **Decision Brief `D<N>`**.

## Khi nào kích hoạt

Kích hoạt trên các yêu cầu của người dùng.

- "Giúp tôi tổ chức lại thư mục tri thức nội bộ X"
- "Thiết lập nguồn sự thật chuẩn (SOT) cho doanh nghiệp hoặc dự án Y"
- "Xây dựng Kernel Registry kết nối với Vibecode Kit cho dự án Z"
- "Tái cấu trúc knowledge base hiện tại để AI Agent không trích dẫn nhầm"
- "Phân loại bảng giá, định mức BOM, văn bản pháp quy và sổ tay thương hiệu"
- "Nhập các Fact Cards đã kiểm chứng từ Bộ 01 vào kho tri thức lâu dài"

Không kích hoạt khi.

- Dữ liệu chỉ là bảng log sự kiện thô phục vụ thống kê thuần túy chưa cần lớp ngữ nghĩa
- Nhóm làm việc quá nhỏ và không có nhu cầu tái sử dụng tri thức qua nhiều chu kỳ
- Hệ thống SOT đa tầng hiện hữu đã vận hành tốt với bằng chứng kiểm toán đầy đủ

## Bốn xuất xứ và Chế độ kiểm chứng (v2.0)

| Xuất xứ | Bản chất tri thức | Kho lưu trữ | Chế độ kiểm chứng cơ học |
|---|---|---|---|
| **L1 · Sự thật lưu sẵn** | Giá bán, định mức `BOM`, mã linh kiện, ma trận năng lực, điều khoản số liệu cứng, hoặc `Fact Card` hạng `verified` từ Bộ 01 | `registry/stored-facts/` | Đối chiếu trực tiếp với tài liệu nguồn qua `source_hash` (`SHA-256`) và hạn hiệu lực `date_expires` (`FRESH / STALE / EXPIRED`) |
| **L2 · Sự thật dẫn xuất** | Tổng dự toán, biên lợi nhuận, doanh thu kế hoạch tính từ các đầu vào `L1` | `registry/derived-facts/` | Lưu công thức và danh sách ID đầu vào `L1`. Tính giá trị bằng lệnh script tất định (`deterministic_eval_cmd`) kèm `audit_trace`, cấm AI nhẩm tính |
| **L3 · Sinh có ràng buộc** | Nghĩa vụ tuân thủ rút từ nghị định, thông tư, quy chế nội bộ, tiêu chuẩn ISO/SOC2 | `obligations/<source-id>/` | Truy vết về đúng điều khoản gốc (`article`), kiểm tra `source_hash` của văn bản pháp quy và đánh dấu `compliance_check_type` |
| **L4 · Phán xét tự do** | Giọng điệu lãnh đạo (`Voice CEO`), phong cách thương hiệu, gu thẩm mỹ thiết kế | `style/` | Đứng **NGOÀI** đường kiểm cơ học. Là đầu vào định hướng văn phong, tuyệt đối không trộn chung với kho `registry/` |

## Quy trình thực hiện 5 Phase (v2.0)

Agent đi qua năm phase theo thứ tự cố định. Dừng lại xin phê duyệt của con người qua thẻ `Decision Brief D<N>` trước khi thực thi Phase 5.

### Phase 1 · Kiểm kê có Dấu vân tay (`Inventory & Source Fingerprinting`)

1. Xác nhận phạm vi các thư mục cần khảo sát với người dùng. Nếu phạm vi chưa rõ, hỏi ngay qua thẻ `D1`, tuyệt đối không tự đoán.
2. Quét toàn bộ tệp trong phạm vi ở chế độ chỉ đọc (`read-only`). Ghi lại mã băm tổng của thư mục gốc (`ORIGINAL_TREE_FINGERPRINT`) để làm bằng chứng bảo toàn dữ liệu.
3. Xuất bảng `manifest.csv` đầy đủ theo mẫu tại `templates/manifest.csv`.

```csv
component_id,component_type,path,domain,source_hash,date_added,date_updated,freshness_status,status
```

**Đầu ra.** File `manifest.csv` và dấu vân tay `ORIGINAL_TREE_FINGERPRINT`.

### Phase 2 · Phân loại theo 4 Xuất xứ và Phân tầng Quyết định 3 Mức

Đọc từng tệp (hoặc từng phần trong tệp hỗn hợp) để gán nhãn `L1`, `L2`, `L3`, `L4` theo bản mẫu `templates/classification-table.csv`.

```csv
file_path,section_scope,classified_as,confidence,decision_tier,selectivity_priority,reason,notes
```

Áp dụng **Phân loại Quyết định 3 tầng** để tăng tốc mà không làm phiền người dùng.
- **Mechanical (`confidence: high`).** Các bảng giá CSV, định mức số liệu rõ ràng (`L1`), bảng công thức tổng (`L2`), văn bản quy chế chính thức (`L3`), tài liệu hướng dẫn giọng văn (`L4`). Agent tự phân loại và ghi lý do.
- **Taste (`confidence: medium`).** Tài liệu có thể tách nhỏ thành nhiều mục `L1` hoặc giữ nguyên khối tùy tần suất tra cứu. Agent gắn nhãn khuyến nghị `(recommended)` theo quy tắc **Selectivity** (chỉ tách nhỏ phần vừa lặp nhiều, vừa tất định, vừa đắt giá khi sai).
- **User Challenge (`confidence: low` hoặc tài liệu pha trộn nhiều xuất xứ).** Đẩy vào `queues/unclassified-queue.md` dưới dạng thẻ quyết định `Decision Brief D<N>` để con người phán xử.

**Đầu ra.** File `classification-table.csv` và `queues/unclassified-queue.md`.

### Phase 3 · Phát hiện Xung đột, Lỗ hổng và Kiểm toán Độ tươi (`Conflict & Staleness Audit`)

Đây là phase mang lại giá trị cốt lõi cao nhất. Agent quét toàn bộ tập tài liệu để phát hiện 5 loại vấn đề và lập thẻ `Decision Brief D<N>` trong `queues/conflict-queue.md`.

1. **Xung đột giá trị chuẩn (`Canonical Conflict`).** Hai tài liệu cùng quy định một mã hàng (`SKU`) hoặc một định mức nhưng có hai con số khác nhau (ví dụ bản nháp và bản ban hành, hoặc bảng giá hai phòng ban lệch nhau).
2. **Đứt gãy đầu vào `L2` (`Missing L1 Inputs`).** Một chỉ số dẫn xuất `L2` hoặc một báo cáo nhắc tới một con số cơ sở nhưng không tìm thấy mục `L1` tương ứng trong kho.
3. **Hết hạn hoặc Trôi mã băm (`EXPIRED / STALE Provenance`).** Mục dữ liệu dựa trên văn bản đã quá ngày `date_expires` hoặc tệp nguồn gốc đã bị sửa đổi làm lệch `source_hash`.
4. **Chồng lấn nghĩa vụ trong `Skills` (`Skill Obligation Drift`).** Các tài liệu hướng dẫn quy trình (`SKILL.md`) tự viết lại quy định pháp lý bằng văn xuôi thay vì trỏ ID về kho `obligations/`, dẫn đến nguy cơ lệch chuẩn khi quy định thay đổi.
5. **Nhiễm chéo `L4` vào `L1/L2` (`Style Contamination`).** Các nhận định chủ quan hoặc khẩu hiệu truyền thông bị đặt lẫn trong bảng thông số kỹ thuật hoặc bảng giá.

**CRITICAL.** Agent tuyệt đối không tự chọn giá trị chuẩn khi có xung đột. Mọi mục trong `conflict-queue.md` đều phải trình bày theo chuẩn thẻ `D<N>` (`ELI10`, `Stakes`, `Completeness X/10`, `(recommended)`) để con người phán xử.

**Đầu ra.** File `queues/conflict-queue.md` và báo cáo kiểm toán độ tươi.

### Phase 4 · Đề xuất Cấu trúc Đích, Chọn Tầng Chỉ mục và Bản đồ Di trú (`Migration Map`)

1. **Áp dụng nguyên tắc Chọn lọc Nước đi đầu (`Selectivity First-Move`).** Ưu tiên tái cấu trúc lô có giá trị cao nhất trước (thường là cụm số liệu `L1` và `L2` như bảng giá, `BOM`, ma trận năng lực và các nghĩa vụ `L3` trọng yếu). Không ép nguyên tử hóa các tài liệu chỉ đọc một lần.
2. **Chọn tầng chỉ mục phụ thuộc (`Tiered Indexing`)** theo giao thức `references/hybrid-indexing-and-gbrain.md`.
   - **Tầng Cơ bản (< 500 thành phần).** Sử dụng duy nhất file `dependency-index.csv` gọn nhẹ, dễ kiểm tra bằng `grep` hoặc Python.
   - **Tầng Mở rộng (>= 500 thành phần hoặc kho kết hợp mã nguồn + tài liệu đa phương thức).** Giữ `dependency-index.csv` làm sổ cái gốc và bật bổ sung đồ thị tri thức `ak-graphify` (gắn nhãn cạnh `EXTRACTED`, `INFERRED`, `AMBIGUOUS`) hoặc đồng bộ vào `gbrain` qua `/sync-gbrain` sau khi đã kiểm tra chính sách `brain_trust_policy` (`personal` / `shared` / `deny`) và chạy `--audit` chống rò rỉ dữ liệu nhạy cảm.
3. **Lập Bản đồ Di trú (`Migration Map`).** Chỉ rõ từng tệp hoặc từng mục dữ liệu sẽ được **sao chép** từ đường dẫn cũ nào sang đường dẫn mới nào trong `kernel-registry/`.

**DỪNG LẠI TẠI CỔNG DUYỆT PHASE 4.** Trình bản đồ di trú và các thẻ `D<N>` còn mở cho con người phê duyệt (`APPROVED`) trước khi thực hiện bất kỳ thao tác tạo kho nào ở Phase 5.

**Đầu ra.** Bản đề xuất cấu trúc đích và `Migration Map` đã được người dùng ký duyệt.

### Phase 5 · Thực thi Sao chép Khóa Phạm vi (`Copy-Only Scope Freeze`) & Nghiệm thu

Chỉ thực thi sau khi người dùng đã duyệt Phase 4.

1. **Khóa phạm vi chỉ sao chép (`Copy-Only Scope Freeze`).** Dựng cây thư mục `kernel-registry/` (gồm `registry/stored-facts/`, `registry/derived-facts/`, `obligations/`, `style/`, `skills/`, `queues/`, `manifest.csv`, `dependency-index.csv`) bằng cách sao chép và trích xuất sang tệp mới. Tuyệt đối không xóa, không di chuyển làm mất tệp gốc, không sửa đổi bất kỳ tệp nào trong thư mục nguồn ban đầu.
2. **Chạy Bộ tính `L2` Tất định (`Deterministic L2 Evaluation`).** Với mọi mục `L2`, chạy script tính toán từ các tệp `L1` đầu vào và ghi kết quả kèm dấu vết `audit_trace`.
3. **Kiểm chứng Bảo toàn Dữ liệu và Liên kết (`Verification Gate`).**
   - Chụp lại mã băm thư mục nguồn gốc và chứng minh nó khớp 100% với `ORIGINAL_TREE_FINGERPRINT` ở Phase 1 (`0` file gốc bị biến đổi).
   - Chạy kiểm tra toàn vẹn con trỏ trên `dependency-index.csv` và các `skills/` để đảm bảo 100% mã `from_id` và `to_id` đều tồn tại trong `manifest.csv`.
4. **Xuất Báo cáo Hoàn tất (`Completion Report`).** Ghi rõ số lượng mục `L1`, `L2`, `L3`, `L4` đã khởi tạo, trạng thái độ tươi `FRESH` và các mục còn chờ trong hàng đợi.

**Đầu ra.** Cây thư mục `kernel-registry/` hoàn chỉnh và `Completion Report`.

## Năm cơ chế ép buộc cứng (`Forcing Functions`)

1. **Bảo toàn tuyệt đối bản gốc (`Zero Source Mutation`).** Không xóa, không ghi đè, không di chuyển phá vỡ cấu trúc thư mục gốc. Kiểm chứng bằng đối chiếu `ORIGINAL_TREE_FINGERPRINT`.
2. **Không tự xử xung đột.** Mọi mâu thuẫn giữa hai nguồn dữ liệu phải đi qua thẻ quyết định `Decision Brief D<N>` do con người ký duyệt.
3. **Không để AI nhẩm tính `L2`.** Mọi đại lượng dẫn xuất `L2` phải lưu công thức tường minh và được tính bằng lệnh cơ học từ các đầu vào `L1` có trạng thái `FRESH`.
4. **Không trộn `L4` vào `Registry` và không lặp lại luật trong `Skill`.** Kho `style/` (`L4`) đứng tách biệt hoàn toàn. Các `Skill` chỉ chứa con trỏ (`Pointer ID`) trỏ tới `registry/`, `obligations/` và `style/`.
5. **Chỉ nâng cấp công cụ khi quy mô đòi hỏi.** Luôn bắt đầu bằng `dependency-index.csv` trên hệ thống tệp Git. Chỉ bật thêm `ak-graphify` hoặc `gbrain` khi vượt ngưỡng quy mô và đã khóa chính sách bảo mật.

## Tài liệu tham chiếu và Bản mẫu

Đọc tài liệu trong `references/` và dùng bản mẫu trong `templates/` khi thực thi từng phase.

| Tài liệu / Bản mẫu | Đường dẫn | Khi nào sử dụng |
|---|---|---|
| Kiểm toán Độ tươi & Bộ tính `L2` | `references/freshness-and-deterministic-l2.md` | Phase 1, Phase 3 & Phase 5 · Kiểm tra SHA-256 và tính công thức L2 |
| Chỉ mục Phân tầng CSV, Graphify & GBrain | `references/hybrid-indexing-and-gbrain.md` | Phase 4 & Phase 5 · Thiết kế `dependency-index.csv` và mở rộng quy mô lớn |
| Cầu nối Liên thông Bộ 01 → Bộ 02 → Bộ 03 | `references/bo01-bo02-bo03-bridge.md` | Khi nhập `Fact Cards` từ Bộ 01 hoặc nối `Kernel Registry` vào `Vibecode Kit v6.1` |
| Bộ 8 Bản mẫu Chuẩn v2.0 | `templates/*` | Khởi tạo `L1`, `L2`, `L3`, `L4`, `manifest`, `classification`, `dependency-index`, `queues` |
| Ví dụ Thực chiến End-to-End | `examples/worked-example.md` | Xem luồng chạy mẫu 5 phase từ kiểm kê đến nghiệm thu bảo toàn dữ liệu |
