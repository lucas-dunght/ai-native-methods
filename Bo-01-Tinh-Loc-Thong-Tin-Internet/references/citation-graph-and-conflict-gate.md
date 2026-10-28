# Giao thức Khử Phòng vang, Thẻ Quyết định Xung đột `D<N>` & Cổng Định lượng (`Citation Graph & Conflict Gate`)

Tài liệu này định nghĩa ba cơ chế kiểm soát chất lượng cốt lõi của Bộ 01 v2.0 gồm Luật Chống Phòng vang (`Echo-Chamber Rule`), Giao thức Phán xử Xung đột bằng thẻ `Decision Brief D<N>` và Vòng lặp Kiểm tra Định lượng (`Constraint Loop Gate`).

## 1. Luật Chống Phòng vang (`Citation Graph / Echo-Chamber Rule`)

### Bản chất của Hiện tượng Phòng vang trên Internet

Trên internet, một con số thống kê từ một bài khảo sát nhỏ hoặc một thông cáo báo chí thường được 10 đến 20 tờ báo và trang tin trích dẫn lại. Nếu AI đếm số lượng đường link (`URL count`) để đánh giá độ tin cậy, AI sẽ lầm tưởng con số đó đã được 20 nguồn xác nhận và gán nhãn `verified`.

### Quy tắc `1 Gốc = 1 Datum`

Trong Bộ 01 v2.0, đơn vị đo lường độ tin cậy không phải là số lượng bài viết (`sources`), mà là **số lượng nguồn gốc độc lập (`independent_origin_count`)**.

1. Khi đọc nguồn `S-NNN`, Agent bắt buộc tìm câu trả lời cho câu hỏi *"Tác giả bài viết này tự đo đạc ra con số này, hay dẫn lại từ một báo cáo/tổ chức khác?"*.
2. Nếu bài viết dẫn lại từ tổ chức hoặc báo cáo `X`, điền URL hoặc định danh chuẩn của `X` vào cột `primary_origin_url` trong `source-log.csv`.
3. Khi gộp các nguồn cho một `Fact Card`, tập hợp `primary_origins` chỉ giữ lại các gốc phân biệt.
   - Ví dụ. Thẻ `F-2026-005` được trích từ 4 bài báo `S002`, `S004`, `S007`, `S010`, nhưng cả 4 bài đều ghi *"Theo báo cáo của Hiệp hội Thương mại Điện tử năm 2024"*. Khi đó `independent_origin_count = 1`.
4. Nếu một bài viết sử dụng cụm từ mơ hồ như *"Theo các chuyên gia"*, *"Theo một nghiên cứu gần đây"* mà không nêu tên tổ chức và năm công bố, gán `primary_origin_url: unknown` và không cộng điểm vào `independent_origin_count`.

## 2. Phán xử Xung đột bằng Thẻ `Decision Brief D<N>`

Khi phát hiện hai hay nhiều `Fact Cards` mâu thuẫn nhau ở Giai đoạn 4, Agent phải lập thẻ quyết định `D<N>` trong `conflict-queue.md` trước khi sang Giai đoạn 6.

Cấu trúc bắt buộc của mỗi thẻ `D<N>` trong `conflict-queue.md`.
- **Tiêu đề `D<N> · Conflict C-NNN`.** Tóm tắt ngắn gọn chỉ số hoặc sự kiện đang mâu thuẫn.
- **Giải thích ELI10.** Giải thích bằng ngôn ngữ đời thường vì sao hai nguồn lại đưa ra hai con số khác nhau (do khác công thức tính, khác thời điểm cắt số liệu, hay một nguồn tính gộp còn nguồn kia tính ròng).
- **Rủi ro nếu chọn sai (`Stakes`).** Nêu rõ kết luận nghiên cứu hoặc bài toán kinh doanh sẽ bị lệch như thế nào nếu chọn nhầm nguồn.
- **Khuyến nghị (`Recommendation`) và Điểm độ phủ (`Completeness X/10`).** Đề xuất phương án tối ưu kèm nhãn `(recommended)` dựa trên thứ bậc uy tín `authority_tier`, độ minh bạch của phương pháp đo (`methodology`) và độ khớp với `brief.md`.

## 3. Cổng Kiểm tra Định lượng & Liên thông Bộ 02 (`Constraint Loop Gate` ở Giai đoạn 4 & 7)

Trước khi xuất bản `report-final.md`, Agent ưu tiên gọi trực tiếp 3 lệnh CLI tất định trong `scripts/bo01_refine_tool.py` để kiểm toán phòng vang, chấm cổng định lượng và xuất sang Bộ 02:

```bash
# 1. Kiểm toán đồ thị nguồn gốc & phát hiện phòng vang (Echo-Chamber Check)
python3 Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py audit-echo \
  --input source-log.csv --min-origins 2 --json

# 2. Chấm 4 điều kiện cổng định lượng trước khi xuất báo cáo cuối
python3 Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py gate-check \
  --independent-origins 2 --unresolved-conflicts 0 --citation-coverage 100 --expired-ttl 0 --json

# 3. Xuất Fact Cards đạt chuẩn sang định dạng L1-stored-fact.yaml của Bộ 02
python3 Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py export-bo02 \
  --input fact-cards/F-2026-001.yaml --output l1-export.yaml --dry-run --json
```

Ngoài ra, có thể chạy đoạn mã kiểm chứng chi tiết dưới đây trên thư mục chu kỳ nghiên cứu để đối chiếu chéo toàn bộ mã trích dẫn trong `report-final.md`.

```python
import glob, re, yaml

def verify_research_cycle(cycle_dir):
    cards = {}
    for path in sorted(glob.glob(f"{cycle_dir}/fact-cards/*.yaml")):
        with open(path, "r", encoding="utf-8") as f:
            card = yaml.safe_load(f)
            cards[card["fact_id"]] = card

    total = len(cards)
    verified = sum(1 for c in cards.values() if c.get("trust_tier") == "verified")
    verified_ratio = (verified / total) if total > 0 else 0.0

    with open(f"{cycle_dir}/conflict-queue.md", "r", encoding="utf-8") as f:
        conflict_text = f.read()
    unresolved_conflicts = conflict_text.count("[chưa quyết]")

    with open(f"{cycle_dir}/report-final.md", "r", encoding="utf-8") as f:
        report_text = f.read()
    cited_ids = set(re.findall(r"\[(F-\d{4}-\d{3})\]", report_text))
    missing_ids = cited_ids - set(cards.keys())

    print(f"Tổng số thẻ: {total} | Verified: {verified} ({verified_ratio:.1%})")
    print(f"Xung đột chưa giải quyết: {unresolved_conflicts}")
    print(f"Mã trích dẫn không tồn tại: {missing_ids}")
    assert verified_ratio >= 0.40, "FAIL: Tỷ lệ thẻ verified dưới 40%"
    assert unresolved_conflicts == 0, "FAIL: Còn xung đột chưa được phán xử"
    assert len(missing_ids) == 0, f"FAIL: Báo cáo chứa mã trích dẫn ảo {missing_ids}"
    print("PASS: Chu kỳ nghiên cứu đạt chuẩn Bộ 01 v2.0!")
```
