# Quick Start · Chạy Vibecode Kit v6.1 trong 20 phút

Hướng dẫn này giúp bạn trải nghiệm trọn vẹn một vòng đời Vibecode Kit v6.1 (bao gồm cả các cơ chế mới như nhãn nhận định `OBSERVED`, khóa phạm vi `Scope Freeze`, dấu vân tay `WTREE_FINGERPRINT` và thẻ hiệu chỉnh `Calibration Card`) trên một bài toán thực tế trong 20 phút.

## Bài toán mẫu

Xây dựng một công cụ dòng lệnh (CLI) bằng Python có tên `lc.py` để đếm tổng số dòng code Python thực chất (bỏ qua dòng trống và dòng chú thích) trong một thư mục bất kỳ. Theo ma trận phân loại rủi ro, đây là tác vụ mức **R1** (tác động thấp, đảo ngược dễ dàng), rất phù hợp để làm quen với quy trình.

## Phút 0 đến 2 · Khởi tạo kho dự án và cấu trúc hiện vật

Mở terminal trên macOS hoặc Linux và chạy các lệnh sau.

```bash
mkdir vibecode-line-counter
cd vibecode-line-counter
git init
mkdir -p vibecode-artifacts/{scan-reports,RRI-logs,blueprints,TIP,handoffs,completion-reports,evidence-ledger,calibration-cards}
mkdir -p src tests docs

echo "timestamp,step,role,action,reference,wtree_fp,notes" > vibecode-artifacts/audit-trail.csv
echo "decision_id,tip_id,completeness,description,upgrade_trigger,status" > vibecode-artifacts/shortcut-ledger.csv
```

## Phút 2 đến 4 · Bước 1 SCAN nhanh và Phân loại R1

Tạo báo cáo khảo sát ngắn tại `vibecode-artifacts/scan-reports/SCAN-001.md` áp dụng **Kỷ luật Nhận định (Claim Discipline)**.

```markdown
# SCAN-001 · Khảo sát khởi tạo Line Counter CLI

**Date.** 2026-10-25
**Role.** Thợ thi công (Builder)

## 1. Trạng thái môi trường
- **OBSERVED.** Kho Git mới khởi tạo, thư mục `src/` và `tests/` hiện đang trống.
- **OBSERVED.** Máy trạm có sẵn Python 3.11+ cùng các thư viện chuẩn `argparse`, `pathlib`, `unittest`.
- **ASSUMED.** Các file `.py` cần đếm dùng bảng mã UTF-8 chuẩn; nếu gặp file nhị phân hoặc lỗi bảng mã thì bỏ qua an toàn kèm cảnh báo thay vì làm sập chương trình.

## 2. Đề xuất phân tầng rủi ro
- **DERIVED.** Công cụ chỉ đọc file cục bộ, không ghi đè dữ liệu người dùng nên xếp ở mức **R1 (Low Risk)**. Có thể bỏ qua phỏng vấn RRI dài dòng, đi thẳng vào TIP và Blueprint gọn.
```

## Phút 4 đến 7 · Bước 2 đến 5 · Viết Blueprint gọn và Gói giao việc TIP-001

Với tác vụ R1, Chủ thầu gộp nhanh định hướng vào `vibecode-artifacts/blueprints/BP-001.md` và xuất gói giao việc `vibecode-artifacts/TIP/TIP-001.md` có khóa phạm vi (`Scope Freeze`) cùng giao thức dừng khi lỗi (`Failure Protocol`).

Tạo file `vibecode-artifacts/blueprints/BP-001.md`.

```markdown
# BP-001 · Kiến trúc Line Counter CLI

**Date.** 2026-10-25
**Linked Scan.** SCAN-001
**Risk tier.** R1

## 1. Cấu trúc module
Một file thực thi `src/lc.py` và một file kiểm thử `tests/test_lc.py`.
- `count_lines_in_file(path)` đọc từng dòng với `errors="replace"`, bỏ qua dòng rỗng và dòng bắt đầu bằng `#`.
- `scan_directory(root_path)` duyệt đệ quy các file `.py` nhưng bỏ qua các đường dẫn liên kết mềm (`is_symlink()`) để tránh vòng lặp vô tận.
- `main()` xử lý tham số dòng lệnh và in kết quả chuẩn.

## 2. Vết mở rộng tiến hóa (Extension Trace)
- Nếu vòng sau cần đếm thêm file `.ts` hoặc `.js`, chỉ cần tách bộ lọc đuôi file và ký tự chú thích thành một bảng cấu hình nhỏ mà không phải viết lại hàm duyệt thư mục. Hiện tại giữ nguyên cho `.py` (YAGNI).

## 3. Phê duyệt
**Status.** APPROVED bởi Chủ nhà (2026-10-25)
```

Tạo file `vibecode-artifacts/TIP/TIP-001.md`.

```markdown
# TIP-001 · Thi công Line Counter CLI và Bộ kiểm thử

**Date.** 2026-10-25
**Risk tier.** R1
**Linked Blueprint.** BP-001

## 1. Intent
Xây dựng công cụ dòng lệnh `python3 src/lc.py <directory>` đếm tổng số dòng code Python thực chất (loại trừ dòng trống và dòng chỉ chứa chú thích `#`).

## 2. Scope Freeze (Khóa phạm vi sửa đổi)
- **Allowed write paths.** `src/lc.py`, `tests/test_lc.py`
- **Forbidden paths.** Không cài thêm gói ngoài, không sửa bất kỳ file nào ngoài danh sách trên.

## 3. Acceptance Criteria (Tiêu chí nghiệm thu cơ học)
- AC1. Chạy `python3 -m unittest discover -s tests` đạt trạng thái OK (kiểm tra đủ trường hợp dòng trống, dòng `#`, thư mục rỗng và symlink).
- AC2. Chạy `python3 src/lc.py src` trả về mã thoát `0` và in ra đúng định dạng `<N> lines of Python code in <M> file(s)`.
- AC3. Khi thư mục không có file `.py`, in thông báo `0 lines of Python code in 0 file(s)` và thoát với mã `0`.

## 4. Failure Protocol (Giao thức dừng khi lỗi)
- Nếu bài kiểm thử thất bại quá 3 lần thử sửa liên tiếp, dừng ngay lập tức và báo cáo nguyên văn đầu ra lỗi cho Chủ thầu, không tự ý đổi thiết kế.
```

Ghi vết vào sổ cái kiểm toán.

```bash
echo "2026-10-25T10:07:00,5,Chủ thầu,TIP_created,TIP-001,-,Khởi tạo TIP-001 kèm Scope Freeze" >> vibecode-artifacts/audit-trail.csv
```

## Phút 7 đến 14 · Bước 6 BUILD và Chụp Dấu vân tay `WTREE_FINGERPRINT`

Giao `BP-001.md` và `TIP-001.md` cho AI Builder (Thợ thi công). Thợ viết `src/lc.py` và `tests/test_lc.py`, sau đó chạy bộ kiểm thử và chụp dấu vân tay cây thư mục ngay tại thời điểm test xanh.

```bash
# 1. Chạy bộ kiểm thử tự động và chạy thử trên thư mục thật
python3 -m unittest discover -s tests -v
python3 src/lc.py src

# 2. Chụp dấu vân tay nội dung cây thư mục ngay sau khi test xanh
WTREE_FP=$( (git status --porcelain; git diff HEAD 2>/dev/null) | shasum -a 256 | cut -c1-16 )
echo "WTREE_FINGERPRINT. $WTREE_FP"
```

## Phút 14 đến 17 · Bước 6 & 7 · Nộp Completion Report và Nghiệm thu

Thợ tạo báo cáo hoàn thành tại `vibecode-artifacts/completion-reports/CR-001.md`.

```markdown
# CR-001 · Báo cáo hoàn thành Line Counter CLI

**Date.** 2026-10-25
**Linked TIP.** TIP-001
**Linked Blueprint.** BP-001

## 1. Bảng tổng hợp kiểm chứng (Evidence Summary)
- **STATUS.** DONE
- **WTREE_FINGERPRINT.** `a1b2c3d4e5f60123` (khớp trạng thái file hiện tại)
- **EVIDENCE_KIND.** `unit-test` + `live-run` (chạy trực tiếp trên CLI)
- **EVIDENCE_STATUS.** `FRESH`

## 2. Các file đã thay đổi (trong đúng Scope Freeze)
- Tạo mới `src/lc.py`
- Tạo mới `tests/test_lc.py`

## 3. Kết quả kiểm thử theo tiêu chí
- **OBSERVED.** AC1 đạt (4 bài unit test chạy xanh trong 0.01s).
- **OBSERVED.** AC2 đạt (`python3 src/lc.py src` in ra `38 lines of Python code in 1 file(s)`).
- **OBSERVED.** AC3 đạt (thư mục trống in ra `0 lines of Python code in 0 file(s)`).

## 4. Độ lệch và Đề xuất (Deviations & Suggestions)
- **DEVIATIONS.** Không có.
- **SUGGESTIONS.** Chuỗi nhiều dòng nằm trong cặp dấu nháy ba (`"""docstring"""`) hiện vẫn được tính là dòng code. Nếu Chủ thầu muốn loại trừ cả docstring ở vòng sau, nên dùng module chuẩn `tokenize` thay vì chỉ kiểm tra ký tự `#` ở đầu dòng.
```

Chủ thầu kiểm tra lại dấu vân tay `WTREE_FINGERPRINT`, xác nhận bằng chứng đang ở trạng thái `FRESH` và chú ý tới đề xuất rất sắc sảo của Thợ ở mục `SUGGESTIONS` mà Thợ đã không tự ý làm vượt phạm vi.

## Phút 17 đến 20 · Bước 8 · Phát hành (Commit) và Viết Thẻ Hiệu chỉnh 100 điểm

Đóng gói phiên bản vào Git và tạo thẻ hiệu chỉnh tại `vibecode-artifacts/calibration-cards/CC-001.md`.

```bash
git add .
git commit -m "feat(cli). hoàn thành công cụ đếm dòng code theo TIP-001"
```

Nội dung `vibecode-artifacts/calibration-cards/CC-001.md`.

```markdown
# CC-001 · Thẻ Hiệu chỉnh Line Counter CLI

**Date deployed.** 2026-10-25
**Date calibrated.** 2026-10-25
**Linked TIP.** TIP-001
**Linked Completion Report.** CR-001

## 1. Dự đoán (Prediction) vs Thực tế (Actual)
- Chạy ổn định và đếm đúng dòng không trống, không `#`. Thực tế đạt 100%.
- Tuy nhiên, khi chạy thử trên một dự án có nhiều docstring dài (`"""..."""`), con số đếm được cao hơn kỳ vọng khoảng 15% vì TIP-001 mới chỉ định nghĩa chú thích là dòng bắt đầu bằng `#`.

## 2. Phân bổ sai số (Tổng = 100 điểm)
- **Modeling.** 100 điểm (Định nghĩa trong TIP-001 về "dòng chú thích" chưa tính đến docstring nhiều dòng của Python).
- **Timing.** 0 điểm
- **World-change.** 0 điểm
- **Execution.** 0 điểm (Thợ đã thi công chính xác 100% theo đúng TIP và còn chủ động cảnh báo điểm này trong mục SUGGESTIONS).

## 3. Bài học và Hành động cho Chu kỳ 2
- **Bài học.** Khi định nghĩa quy tắc phân tích cú pháp mã nguồn trong TIP, cần làm rõ cách xử lý cả chú thích một dòng lẫn chuỗi tài liệu nhiều dòng.
- **Hành động.** Mở `TIP-002` ở chu kỳ tiếp theo để nâng cấp bộ đếm sang dùng thư viện chuẩn `tokenize` như Thợ đã đề xuất.
```

## Tổng kết sau 20 phút

Bạn đã hoàn thành trọn vẹn một vòng đời Vibecode Kit v6.1 với đầy đủ các nguyên tắc bảo vệ chất lượng hiện đại nhất.
- Có báo cáo khảo sát phân biệt rõ sự thật đã đo đạc (`OBSERVED`) và giả định (`ASSUMED`).
- Có gói giao việc khóa chặt phạm vi sửa đổi (`Scope Freeze`).
- Có báo cáo hoàn thành gắn dấu vân tay cây thư mục (`WTREE_FINGERPRINT`) chứng minh kết quả kiểm thử là tươi mới (`FRESH`).
- Có thẻ hiệu chỉnh 100 điểm giúp phát hiện chính xác sai số nằm ở khâu đặc tả (`Modeling`) chứ không phải khâu thi công (`Execution`).

Bước tiếp theo, hãy xem file `examples/worked-example.md` để nắm cách áp dụng Vibecode Kit v6.1 cho một dự án ứng dụng web mức **R2/R3** có phỏng vấn quyết định `D<N>`, điều phối nhiều Thợ song song trên `git worktree` và phát hành hai chặng.
