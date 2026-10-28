---
name: kernel-registry-sot
description: >
  Thiết kế, kiểm toán và vận hành kiến trúc Nguồn Sự Thật Duy Nhất (Kernel Registry SOT v2.1) theo bốn xuất xứ tri thức (L1 Sự thật lưu sẵn, L2 Sự thật dẫn xuất tất định qua AST Safe Evaluator, L3 Nghĩa vụ có ràng buộc, L4 Phán xét tự do) kèm kiểm toán độ tươi bằng mã băm SHA-256, chỉ mục phụ thuộc phân tầng và kỷ luật sao chép khóa phạm vi (Copy-Only Scope Freeze).
---

# Kernel Registry SOT · Nguồn Sự Thật Duy Nhất Bốn Xuất Xứ (`v2.1 · Full-Stack 4 Lớp`)

Phân lập tri thức tổ chức và dự án thành **bốn xuất xứ có chế độ kiểm chứng riêng biệt (`L1`, `L2`, `L3`, `L4`)**, thực thi kiểm toán mã băm SHA-256 và tính công thức `L2` tất định qua công cụ CLI `scripts/bo02_registry_tool.py` (kèm `scripts/eval_l2.py`).

## 1. Phân Tầng Quy Mô & Rủi Ro Co Giãn (`R0–R3 Adaptive Scaling`)

Trước khi chạy, phân loại quy mô kho tài liệu vào đúng tầng `R0..R3` để chọn đường chạy nhanh (`Fast-Track`) hoặc đầy đủ:

| Tầng | Quy mô Kho Tri thức | Đường chạy khuyến nghị (`Fast-Track` vs `Full`) | Cổng bắt buộc |
|---|---|---|---|
| **R0 · Cập nhật đơn lẻ** | `< 10` mục, thêm/sửa 1-2 sự thật `L1` hoặc tính lại 1 công thức `L2` | Chạy trực tiếp `eval-l2` và `audit-freshness` trên tệp mục tiêu trong 2 phút | `eval-l2` + `source_hash` |
| **R1 · Kho dự án nhỏ** | `10–30` mục, thiết lập nhanh `kernel-registry/` lần đầu trong `15 phút` | Chạy `Indirect Prompting Restate` + `fingerprint` + tạo `L1/L2/L3/L4` cốt lõi + `manifest.csv` | `fingerprint` trước/sau khớp `100%` |
| **R2 · Kho tiêu chuẩn** | `30–500` thành phần, có xung đột liên phòng ban hoặc liên kết sang Bộ 03 | Chạy đủ 5 Phase + `queues/conflict-queue.md` (`D<N>`) + `dependency-index.csv` + `sync-feature-map` | Duyệt `Migration Map` + `0` xung đột treo |
| **R3 · Kho doanh nghiệp lớn** | `> 500` thành phần hoặc kết hợp mã nguồn đa ngôn ngữ + tài liệu pháp quy | Chạy đủ 5 Phase + đồ thị `ak-graphify` (`AST` + `Docs`) + đồng bộ `/sync-gbrain --audit` | Toàn bộ 5 cổng + kiểm toán `--audit` |

## 2. Công Cụ CLI Tất Định (`scripts/bo02_registry_tool.py` & `scripts/eval_l2.py`)

Tuyệt đối không để AI tự nhẩm tính giá trị `L2` trong đầu hay đoán trạng thái độ tươi. Sử dụng trực tiếp công cụ CLI chuẩn 4 lớp đi kèm bộ kỹ năng:

| Lệnh CLI (`python3 scripts/bo02_registry_tool.py ...`) | Chức năng tất định | Cờ hỗ trợ |
|---|---|---|
| `fingerprint --dir <raw-docs/>` | Chụp mã băm `ORIGINAL_TREE_FINGERPRINT` (`SHA-256` luồng 64KB) toàn cây thư mục để bảo chứng `Copy-Only Scope Freeze` | `--dir`, `--json` |
| `audit-freshness -i <L1-dir> -b <base-dir> -d dependency-index.csv` | Đối chiếu `source_hash` và `date_expires` của `L1`; đánh dấu `FRESH / STALE / EXPIRED` và lan truyền `STALE` sang `L2/L3/Skills` | `--l1-file`, `--base-dir`, `--dependency-index`, `--json` |
| `eval-l2 --id <L2-ID> --l2-file <path> --l1-file <path>` *(hoặc `python3 scripts/eval_l2.py --id <L2-ID>`)* | Tính giá trị `L2` bằng trình thông dịch **AST Safe Math Evaluator** (chỉ cho phép toán tử số học và `min/max/round/sum/abs`, `0%` dùng `eval()` mở) | `--id`, `--vars`, `--output`, `--dry-run`, `--json` |
| `sync-feature-map -i <sot.yaml> -o <bridge.json>` | Đồng bộ trạng thái độ tươi `L1/L2/L3` sang `Feature Map` của Bộ 03 (`READY_FOR_SPEC` hoặc `BLOCK_RELEASE_AND_REVERIFY`) | `--dry-run`, `--json` |
| `--self-test --json` | Chạy bộ kiểm thử nội tại kiểm chứng toàn bộ 4 lệnh và bộ chặn bảo mật AST trong `< 200ms` | `--json` |

## 3. Bốn Xuất Xứ Tri Thức & Ánh Xạ 4 Nhãn Fable 5.1

| Xuất xứ | Bản chất & Kho lưu trữ | Chế độ kiểm chứng cơ học | Ánh xạ Nhãn Nhận Định Fable 5.1 & Đồ thị |
|---|---|---|---|
| **L1 · Stored Facts** | Số liệu đo được, bảng giá, định mức, `Fact Card` từ Bộ 01 (`registry/stored-facts/`) | Khớp `source_hash` (`SHA-256`) với tài liệu gốc và chưa quá hạn `date_expires` (`FRESH`) | `OBSERVED` <-> `provenance_tag: EXTRACTED` |
| **L2 · Derived Facts** | Chỉ số tổng hợp tính từ `L1` (`registry/derived-facts/`) | Thực thi công thức qua `eval-l2` (`AST Safe Evaluator`) và lưu `audit_trace` | `DERIVED` (`INFERRED`) <-> `provenance_tag: INFERRED` |
| **L3 · Obligations** | Nghĩa vụ pháp lý, quy chế, tiêu chuẩn bắt buộc (`obligations/<source-id>/`) | Truy vết điều khoản `article`, kiểm tra hiệu lực và lịch sử `superseded_by` | `OBSERVED` / `DERIVED` <-> `EXTRACTED` / `INFERRED` |
| **L4 · Free Judgment** | Giọng văn thương hiệu, gu thẩm mỹ, triết lý lãnh đạo (`style/`) | Đứng ngoài đường kiểm đúng sai cơ học (`non-mechanically-verifiable`) | Tách biệt khỏi `L1/L2/L3`; nếu chưa xác minh thì gắn `PRIOR` / `ASSUMED` (`AMBIGUOUS`) |

## 4. Quy Trình 5 Phase & Giám Sát Nhận Thức (`Indirect Prompting Restate`)

1. **Phase 1 · `Indirect Prompting Restate`, Kiểm kê & Chụp dấu vân tay gốc:**
   - Trước khi phân loại, Agent tự diễn giải lại bài toán trong 3-5 dòng (`Indirect Prompting Restate`): *(a) Cụm dữ liệu nào có tần suất tra cứu và rủi ro sai lệch cao nhất cần ưu tiên đưa vào `registry/` trước (`Selectivity`), (b) Thư mục gốc nào cần khóa bảo vệ (`Copy-Only`) cùng (c) Tầng quy mô `R0..R3`*.
   - Chạy `python3 scripts/bo02_registry_tool.py fingerprint --dir <raw-docs> --json` để lưu `ORIGINAL_TREE_FINGERPRINT` và lập `manifest.csv`.
2. **Phase 2 · Phân loại `L1/L2/L3/L4` & Phân tầng Quyết định:** Xử lý tự động các mục rõ ràng (`Mechanical`), gắn khuyến nghị chọn lọc (`Taste`) và đẩy tệp pha trộn nhiều xuất xứ vào `queues/unclassified-queue.md` kèm thẻ **Decision Brief `D<N>`**.
3. **Phase 3 · Kiểm toán Độ tươi & Hàng đợi Xung đột (`Cổng D<N>`):** Chạy `audit-freshness` để tìm số liệu mâu thuẫn, công thức thiếu đầu vào hoặc tài liệu hết hạn; lập thẻ `Decision Brief D<N>` trong `queues/conflict-queue.md`.
4. **Phase 4 · Đề xuất Cấu trúc Đích & Bản đồ Di trú (`Cổng Duyệt Con Người`):** Lập `queues/migration-map.md` theo nguyên tắc chọn lọc (`Anti-Big-Bang`) và dừng lại chờ người dùng phê duyệt trước khi tạo kho.
5. **Phase 5 · Sao chép Khóa Phạm vi (`Copy-Only`), Tính `L2` & Nghiệm thu:** Dựng `kernel-registry/` hoàn toàn bằng thao tác sao chép, chạy `eval-l2`, cập nhật `dependency-index.csv` và chạy lại `fingerprint` để chứng minh `PRE_MIGRATION_FINGERPRINT == POST_MIGRATION_FINGERPRINT` (`100%`).

## 5. Bản Đồ Tài Liệu Tham Chiếu (`Progressive Disclosure`)

- **Kiến trúc & Phương pháp luận:** `Methodology.md`, `Architecture.md`, `Quick-Start.md`
- **Giao thức chuyên sâu (`references/`):**
  - `references/freshness-and-deterministic-l2.md`: Kiểm toán độ tươi SHA-256 (`audit-freshness`) và tính toán tất định `L2` qua `AST Safe Evaluator` (`eval-l2`).
  - `references/hybrid-indexing-and-gbrain.md`: Chỉ mục 2 tầng (`dependency-index.csv` + `ak-graphify` + `gstack /sync-gbrain`).
  - `references/bo01-bo02-bo03-bridge.md`: Ma trận 4 Nhãn Fable 5.1 và chuỗi lệnh CLI liên thông `Bộ 01 -> Bộ 02 -> Bộ 03`.
- **Biểu mẫu chuẩn (`templates/`):** `L1-stored-fact.yaml`, `L2-derived-fact.yaml`, `L3-obligation.yaml`, `L4-style.yaml`, `manifest.csv`, `dependency-index.csv`, `classification-table.csv`, `queues-and-migration-map.md`.
- **Ví dụ thực chiến (`examples/`):** `examples/worked-example.md`.
