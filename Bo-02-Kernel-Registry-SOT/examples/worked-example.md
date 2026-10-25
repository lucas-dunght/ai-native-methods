# Worked Example · Tái cấu trúc Kho Tri thức Doanh nghiệp Fintech (Bộ 02 v2.0 End-to-End)

Tài liệu này minh họa một ví dụ thực chiến hoàn chỉnh chạy qua đủ **5 Phase của Bộ 02 v2.0 (2026.10)** để tổ chức lại kho tài liệu phân tán của một doanh nghiệp dịch vụ thanh toán số, đồng thời nối dữ liệu trực tiếp từ **Bộ 01** sang **Bộ 03 (`Vibecode Kit v6.1`)**.

---

## Bối cảnh Đầu vào

Doanh nghiệp có thư mục tài liệu nội bộ `company-docs/` đang chứa 5 tệp chưa được phân loại, cộng với 1 thẻ sự thật thị trường (`F-2026-001`) vừa được kiểm chứng từ **Bộ 01**.
1. `company-docs/sales/merchant-fee-2026-Q4-signed.pdf` (Biểu phí thu hộ tiểu thương Quý 4 bản ký duyệt: `1.2%`).
2. `company-docs/finance/merchant-fee-2026-Q4-draft.xlsx` (Bảng tính nháp ghi mức phí thu hộ là `1.5%`, kèm công thức tính doanh thu phí dự kiến).
3. `company-docs/legal/decree-13-2023-nd-cp.pdf` (Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân).
4. `company-docs/brand/product-copy-style.md` (Hướng dẫn văn phong giao diện ứng dụng ví điện tử).
5. `company-docs/ops/onboarding-sop-and-ideas.md` (Tài liệu hỗn hợp vừa có quy định kiểm tra KYC bắt buộc, vừa có ý tưởng trang trí màn hình chào mừng).

---

## Phase 1 · Kiểm kê và Chụp Dấu vân tay Bảo toàn (`Inventory & Fingerprinting`)

Agent quét thư mục `company-docs/` ở chế độ chỉ đọc và ghi nhận dấu vân tay bảo toàn bản gốc.
- `ORIGINAL_TREE_FINGERPRINT`: `sha256:6b86b273ff34fce19d6b804eff5a3f57` (`5` tệp, tổng dung lượng `1.42 MB`).

---

## Phase 2 · Phân loại theo 4 Xuất xứ & Lọc Quyết định 3 Tầng (`classification-table.csv`)

```csv
file_path,section_scope,classified_as,confidence,decision_tier,selectivity_priority,reason,notes
company-docs/sales/merchant-fee-2026-Q4-signed.pdf,Bảng biểu phí trang 2,L1,high,Mechanical,P0-high-value,Biểu phí giao dịch cứng áp dụng toàn hệ thống,Xung đột giá trị với bản nháp trong thư mục finance
company-docs/finance/merchant-fee-2026-Q4-draft.xlsx,Công thức tính doanh thu ròng ở Sheet 2,L2,high,Mechanical,P0-high-value,Công thức nhân tổng GMV với tỷ lệ phí thu hộ,Tách phần công thức vào derived-facts
company-docs/legal/decree-13-2023-nd-cp.pdf,Điều 13 và Điều 28,L3,high,Mechanical,P0-high-value,Nghĩa vụ xin sự đồng ý của chủ thể dữ liệu và bảo mật thông tin,Trích vào kho obligations/
company-docs/brand/product-copy-style.md,Toàn bộ tệp,L4,high,Mechanical,P1-normal,Quy chuẩn giọng văn thân thiện trên ứng dụng,Đưa vào kho style/
company-docs/ops/onboarding-sop-and-ideas.md,Mục 1 (Quy định KYC) và Mục 2 (Ý tưởng giao diện),MIXED,low,User_Challenge,P1-normal,Tệp pha trộn nghĩa vụ tuân thủ KYC (L3) và gợi ý thẩm mỹ (L4),Đẩy vào unclassified-queue.md trình thẻ D2
```

---

## Phase 3 · Phát hiện Xung đột & Trình Thẻ Quyết định `D1`, `D2` (`queues/`)

Agent phát hiện 1 xung đột biểu phí (`C-001`) và 1 tệp pha trộn (`U-001`), lập tức trình hai thẻ quyết định `D1` và `D2` cho Giám đốc Sản phẩm.

```markdown
### D1 · Conflict C-001 · Mức phí thu hộ tiểu thương Quý 4/2026 (`1.2%` so với `1.5%`)

- **Giải thích ELI10.** Tệp PDF đã ký của bộ phận Kinh doanh quy định mức phí thu hộ mã QR là `1.2%`, trong khi tệp Excel nháp của bộ phận Tài chính vẫn để con số cũ `1.5%`.
- **Rủi ro nếu chọn sai (Stakes).** Nếu hệ thống thanh toán ở Bộ 03 code theo mức `1.5%`, tiểu thương sẽ bị thu thừa `0.3%` mỗi giao dịch, vi phạm hợp đồng đã ký.
- **Khuyến nghị (Recommendation).** Chọn **A** (Lấy `1.2%` từ tệp PDF đã ký làm chuẩn `L1-merchant-qr-fee-rate-2026-Q4` và chỉ trích xuất công thức tính doanh thu từ tệp Excel sang `L2`).
- **Điểm độ phủ (Completeness).** `A = 10/10`, `B = 2/10`.
- **Quyết định của con người.** `[x] Phương án A (Đã duyệt ngày 2026-10-25)`.

### D2 · Unclassified U-001 · Tách tệp hỗn hợp `onboarding-sop-and-ideas.md`

- **Giải thích ELI10.** Tệp này trộn chung quy định bắt buộc xác thực căn cước công dân (`eKYC`) với các ý tưởng viết lời chào khách hàng mới.
- **Khuyến nghị (Recommendation).** Chọn **A** (Trích quy định `eKYC` thành nghĩa vụ `OBL-internal-kyc-001` trong kho `L3` và chuyển phần lời chào sang `style/onboarding-tone.md` ở kho `L4`).
- **Điểm độ phủ (Completeness).** `A = 10/10`, `B = 5/10`.
- **Quyết định của con người.** `[x] Phương án A (Đã duyệt ngày 2026-10-25)`.
```

---

## Phase 4 · Đề xuất Cấu trúc Đích & Duyệt Bản đồ Di trú (`Migration Map`)

Doanh nghiệp có tổng cộng `18` thành phần trong lô đầu tiên (`< 500`), nên Agent chọn **Tầng 1 (`dependency-index.csv` thuần túy)** và trình `Migration Map`. Giám đốc Sản phẩm xác nhận **APPROVED**.

---

## Phase 5 · Thực thi Sao chép Khóa Phạm vi (`Copy-Only Scope Freeze`) & Nghiệm thu

Agent dựng cấu trúc `kernel-registry/` bằng cách sao chép, nhập thêm thẻ `F-2026-001` từ **Bộ 01** thành mục `L1-sea-digital-payments-gtv-2024` và chạy script tính toán cho mục `L2-projected-fee-revenue-2026-Q4`.

### 1. Mục `L1-merchant-qr-fee-rate-2026-Q4.yaml`

```yaml
fact_id: L1-merchant-qr-fee-rate-2026-Q4
fact_type: L1
domain: pricing-policy
key: merchant-qr-fee-rate
value: 0.012
unit: ratio
source:
  type: internal-document
  document_id: merchant-fee-2026-Q4-signed
  document_path: company-docs/sales/merchant-fee-2026-Q4-signed.pdf
  source_hash: "sha256:4a8c91e02b7f11d3"
  page: 2
date_effective: 2026-10-01
date_expires: 2026-12-31
date_updated: 2026-10-25
updated_by: human
verification_status: FRESH
status: active
notes: "Tỷ lệ phí thu hộ qua mã QR = 1.2% theo quyết định D1"
```

### 2. Mục `L2-projected-fee-revenue-2026-Q4.yaml` (Tính tất định bằng script)

```yaml
fact_id: L2-projected-fee-revenue-2026-Q4
fact_type: L2
domain: financial-metrics
key: projected-fee-revenue-2026-Q4
formula:
  type: product
  expression: "L1_target_gmv_q4 * L1_merchant_qr_fee_rate"
  inputs:
    - L1-target-gmv-2026-Q4
    - L1-merchant-qr-fee-rate-2026-Q4
computed_cache:
  last_computed_value: 600000000
  unit: VND
  computed_at: 2026-10-25T11:00:00Z
  input_hashes:
    L1-target-gmv-2026-Q4: "sha256:2f99a1c4"
    L1-merchant-qr-fee-rate-2026-Q4: "sha256:4a8c91e0"
  audit_trace: "50000000000 * 0.012 = 600000000"
verification_status: FRESH
status: active
notes: "Doanh thu phí dự kiến Quý 4 = 50 tỷ VND GMV * 1.2% = 600 triệu VND"
```

### 3. Biên bản Nghiệm thu Phase 5 (`Completion Report`)

- **Kiểm chứng bảo toàn thư mục gốc (`[OBSERVED]`).** Mã băm của `company-docs/` sau khi chạy đạt `sha256:6b86b273ff34fce19d6b804eff5a3f57`, khớp `100%` với `ORIGINAL_TREE_FINGERPRINT` (`0` tệp gốc bị xóa hay sửa đổi).
- **Độ tươi và Tính tất định.** `100%` mục `L1`, `L2`, `L3` đạt trạng thái `FRESH`.
- **Sẵn sàng bàn giao sang Bộ 03 (`Vibecode Kit v6.1`).** Gói giao việc `TIP-01` của Bộ 03 đã nhúng trực tiếp con trỏ `[L1-merchant-qr-fee-rate-2026-Q4]` và `[OBL-decree-13-001]` vào bảng tiêu chí nghiệm thu của module thanh toán.
