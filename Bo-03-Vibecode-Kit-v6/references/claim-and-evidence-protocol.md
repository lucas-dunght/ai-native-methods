# Giao Thức Kỷ Luật Khẳng Định & Sổ Cái Bằng Chứng (`Claim & Evidence Protocol`)

> **Nền tảng Đạo đức Bằng chứng của Vibecode Kit v6.2 (`× pstack`) · Cấm Bịa Đặt Kết Quả · Đóng Dấu Vân Tay Cây Làm Việc (`WTREE_FINGERPRINT`) & Bằng Chứng `./bin/control-app --json`**

---

## 1. Phân Loại Bốn Cấp Độ Khẳng Định Fable 5.1 (`Unified Four-Tier Claim Taxonomy`)

Mọi câu khẳng định kỹ thuật mà Chủ thầu hoặc Thợ đưa ra trong báo cáo khảo sát (`SCAN`), giải thích hai chiều (`/teach`), bản vẽ (`BLUEPRINT`) hay biên bản hoàn thành (`Completion Report`) đều phải gắn nhãn nguồn gốc theo **Ma trận 4 Nhãn Fable 5.1** (đồng bộ 100% với Bộ 01 và Bộ 02):

| Nhãn chuẩn Fable 5.1 | Nhãn tương thích ngược | Ánh xạ sang Bộ 02 (`dependency-index.csv`) | Định nghĩa & Yêu cầu bằng chứng bắt buộc |
|---|---|---|---|
| **`[OBSERVED]`** | `[OBSERVED]` | `EXTRACTED` | Sự thật đã được kiểm chứng trực tiếp bằng công cụ đọc tệp, tìm kiếm mã, truy vấn lịch sử (`/why`) hoặc chạy lệnh thực thi (`./bin/control-app`, `bo03_vibecode_tool.py`, `test`). Phải kèm địa chỉ `[OBSERVED: path/to/file:line]` hoặc biên nhận JSON. |
| **`[DERIVED]`** | `[INFERRED]` | `INFERRED` | Suy luận logic hoặc phép tính tất định rút ra từ một hoặc nhiều bằng chứng `[OBSERVED]`. Phải nêu rõ dựa trên `[OBSERVED]` nào và công thức/cơ chế suy diễn. |
| **`[PRIOR]`** | `[UNVERIFIED]` | `AMBIGUOUS` | Tri thức nền có sẵn của mô hình về thư viện, giao thức hoặc hệ thống ngoài nhưng chưa chạy lệnh xác minh trực tiếp trong kho mã hiện tại. Không được dùng làm bằng chứng nghiệm thu. |
| **`[ASSUMED]`** | `[UNVERIFIED]` | `AMBIGUOUS` | Giả định làm việc tạm thời khi chưa có môi trường thử nghiệm hoặc chờ quyết định. Bắt buộc liệt kê rủi ro nếu sai và đưa vào thẻ quyết định `Decision Brief D<N>`. |

---

## 2. Năm Hành Vi Bị Cấm Tuyệt Đối (`Zero-Fabrication Iron Rules`)

1. **Cấm bịa kết quả chạy `./bin/control-app` hoặc kết quả kiểm thử:** Tuyệt đối không được viết `"All tests passed"` hay `"Đã kiểm tra giao diện hoạt động tốt"` nếu chưa thực sự gọi công cụ chạy lệnh và đọc mã thoát (`exit code 0`).
2. **Cấm bịa đường dẫn tệp, tên hàm hoặc cờ dòng lệnh (`No Hallucinated Symbols`):** Trước khi trích dẫn một hàm hoặc một subcommand trong bản kế hoạch, phải dùng công cụ đọc tệp, `grep` hoặc `--help` để xác nhận nó thực sự tồn tại.
3. **Cấm phán tự tin nhưng rỗng khi giải thích (`/teach Anti-Hallucination Rule`):** Khi thực hiện lệnh `/teach` để chứng minh vì sao phương án thiết kế mới tốt hơn hiện trạng, bắt buộc phải đặt cạnh nhau đoạn code hiện tại (`file:line`) và khung chữ ký kiểu mới (`Type Signatures Sketch`), tuyệt đối không dùng lời lẽ chung chung.
4. **Cấm che giấu lỗi hoặc sửa bài kiểm thử để lấy màu xanh giả tạo (`No Test Weakening`):** Khi bài kiểm thử hoặc lệnh `./bin/control-app` thất bại, không được xóa câu lệnh `assert`, đổi điều kiện kiểm tra sang giá trị sai hoặc thêm cờ bỏ qua kiểm tra (`skip`, `@ts-ignore`).
5. **Cấm ngoại suy số liệu hiệu năng hoặc độ phủ (`No Extrapolated Metrics`):** Mọi con số về thời gian phản hồi (`ms`), dung lượng bộ nhớ hay tỷ lệ độ phủ kiểm thử (`%`) đều phải có nhãn `[measured: <command>]` đi kèm.

---

## 3. Bằng Chứng Từ Đòn Bẩy `./bin/control-app --json` (`Machine-Readable Live Receipts`)

Trong Vibecode Kit v6.2 (`× pstack`), bằng chứng hạng nhất (`First-Class Evidence`) không chỉ là log chữ thuần túy mà là **biên nhận JSON máy đọc được** xuất ra từ đòn bẩy `./bin/control-app` kèm đường dẫn tới ảnh chụp màn hình hoặc bản chụp cây giao diện (`DOM / Accessibility Tree snapshot`):

```json
{
  "ok": true,
  "subcommand": "verify-flow",
  "route": "/orders/ORD-2026-099/cancel",
  "dry_run": false,
  "assertions": {
    "status_code": 200,
    "order_state_after": "CANCELLED",
    "refund_job_queued": true,
    "dom_toast_text": "Đơn hàng đã được hủy thành công"
  },
  "artifacts": {
    "dom_snapshot": ".tmp/artifacts/ord-cancel-dom.json",
    "screenshot": ".tmp/artifacts/ord-cancel-screen.png"
  },
  "measured_ms": 42
}
```

---

## 4. Quy Trình Đóng Dấu Vân Tay Cây Làm Việc (`WTREE_FINGERPRINT Protocol`)

Để ngăn chặn tình trạng "báo cáo kiểm thử trên một phiên bản code nhưng lại bàn giao một phiên bản code khác", mọi biên bản ở Bước 6 (`BUILD`), Bước 7 (`VERIFY`) và Bước 8 (`SHIP`) đều phải chạy câu lệnh sau và dán kết quả nguyên bản vào mục `Evidence Ledger`:

```bash
COMMIT_HASH="$(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')"
TREE_HASH="$(git rev-parse HEAD^{tree} 2>/dev/null || echo 'no-tree')"
DIRTY_COUNT="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
WTREE_SIG="$( (git status --porcelain; git diff HEAD) 2>/dev/null | shasum -a 256 | cut -c1-16 )"
echo "WTREE_FINGERPRINT: HEAD=${COMMIT_HASH} TREE=${TREE_HASH:0:12} WTREE=${WTREE_SIG} DIRTY_FILES=${DIRTY_COUNT}"
```

### Ý nghĩa của 4 thành phần trong `WTREE_FINGERPRINT`:
- **`HEAD`:** Mã băm rút gọn của commit hiện tại trên nhánh làm việc.
- **`TREE`:** Mã băm cấu trúc cây thư mục của commit hiện tại.
- **`WTREE`:** Mã băm SHA-256 (16 ký tự đầu) tính trên toàn bộ danh sách tệp thay đổi và nội dung `git diff HEAD`. Bất kỳ thay đổi nào dù chỉ 1 ký tự khoảng trắng cũng sẽ làm đổi mã `WTREE`.
- **`DIRTY_FILES`:** Số lượng tệp chưa được commit tại thời điểm chụp. Khi đóng gói phát hành ở Bước 8 (`SHIP`), giá trị này bắt buộc phải bằng `0`.
