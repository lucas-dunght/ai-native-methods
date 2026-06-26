# Quick Start · Bộ 01 trong 10 phút

Hướng dẫn này giúp sinh viên chạy phương pháp lần đầu trên một bài toán nhỏ trong khoảng 10 phút. Mục tiêu là làm quen với quy trình, chưa cần làm chuẩn 100%.

## Bài toán mẫu

Sinh viên muốn tìm hiểu xu hướng phát triển của thị trường giáo dục trực tuyến tại Đông Nam Á trong giai đoạn 2022 đến 2024. Đây là bài toán research nhỏ, đủ để demo phương pháp.

## Phút 0 đến 2 · Brief

Mở một file mới `brief.md` và điền ba câu.

```markdown
# Brief nghiên cứu · Edtech ĐNA 2022-2024

## Câu hỏi nghiên cứu
Thị trường giáo dục trực tuyến tại Đông Nam Á
phát triển theo xu hướng nào trong giai đoạn 2022-2024?
Các yếu tố thúc đẩy chính là gì?

## Phạm vi
- Thời gian. 2022 đến 2024.
- Địa lý. 6 nước ĐNA chính (Singapore, Việt Nam, Indonesia,
  Philippines, Malaysia, Thái Lan).
- Loại sản phẩm. K-12 và upskilling.

## Tiêu chí loại trừ
- Báo cáo không có số liệu cụ thể.
- Bài viết quảng cáo trá hình.
- Nguồn không có ngày publish.
```

## Phút 2 đến 5 · Thu thập 5 nguồn đầu tiên

Mở file `source-log.csv` và bắt đầu thu. Cho cycle đầu, mục tiêu là 5 nguồn để có cảm giác về phương pháp.

Query gợi ý.

- "Southeast Asia edtech market 2024 report"
- "Vietnam online education growth statistics"
- "Indonesia K-12 edtech 2023 2024"
- "ASEAN upskilling platform usage"
- "Southeast Asia edtech investment 2024"

Mỗi query mở Google hoặc Brave Search, chọn 1 nguồn tốt nhất từ top 5 kết quả. Ghi vào source log.

```csv
source_id,url,title,date_collected,query_used,source_type,authority_tier
S001,https://example.com/report,"SEA Edtech Market 2024",2026-06-26,"Southeast Asia edtech market 2024 report",học thuật,tier-1
S002,...
```

## Phút 5 đến 7 · Trích 3 fact cards

Đọc nhanh 2 nguồn đầu tiên, trích 3 mẩu sự thật vào fact card.

Mỗi card là một file YAML trong thư mục `fact-cards/`.

```yaml
fact_id: F-2026-001
content: "Thị trường edtech ĐNA đạt 6.7 tỷ USD trong năm 2023"
sources: [S001]
fact_type: numerical-claim
domain: market-size
role: evidence-thesis-1
date_extracted: 2026-06-26
extracted_by: human
```

```yaml
fact_id: F-2026-002
content: "Việt Nam có 23 startup edtech được đầu tư từ 2022 đến 2024"
sources: [S002]
fact_type: numerical-claim
domain: investment
role: evidence-thesis-2
date_extracted: 2026-06-26
extracted_by: human
```

```yaml
fact_id: F-2026-003
content: "Singapore áp dụng AI chấm bài tự động cho 12 trường công lập"
sources: [S001]
fact_type: qualitative-claim
domain: ai-adoption
role: example-thesis-3
date_extracted: 2026-06-26
extracted_by: human
```

## Phút 7 đến 8 · Phân hạng nhanh

Mỗi card đã có ít nhất một nguồn. Áp quy tắc gán trust tier.

- F-2026-001 chỉ có 1 nguồn tier-1, gán `probable`.
- F-2026-002 chỉ có 1 nguồn tier-2, gán `probable`.
- F-2026-003 chỉ có 1 nguồn tier-1, gán `probable`.

Cập nhật mỗi card thêm trường `trust_tier: probable`.

Sau cycle này, để upgrade lên verified, cần thu thêm nguồn độc lập thứ hai cho mỗi card. Đó là việc cho cycle sau.

## Phút 8 đến 10 · Báo cáo tóm tắt

Tạo file `report-final.md` với cấu trúc 3 phần.

```markdown
# Báo cáo · Edtech ĐNA 2022-2024 · Cycle 1

## 1. Kết luận chính (verified facts)

Chưa có verified facts trong cycle này. Cần ít nhất một nguồn
độc lập thứ hai cho mỗi claim để upgrade từ probable lên verified.

## 2. Giả thuyết (probable facts cần kiểm chứng)

Thị trường edtech ĐNA có quy mô đáng kể, đạt 6.7 tỷ USD năm 2023 [F-2026-001].
Việt Nam là một trong các nước active nhất về startup edtech với 23 startup
được đầu tư từ 2022-2024 [F-2026-002]. Singapore dẫn đầu trong áp dụng AI vào
giáo dục, với 12 trường công lập đã chấm bài tự động bằng AI [F-2026-003].

## 3. Câu hỏi mở

- Cần kiểm chứng con số 6.7 tỷ USD từ ít nhất một nguồn tier-1 độc lập khác.
- Chưa có dữ liệu cho Indonesia, Philippines, Malaysia, Thái Lan.
- Yếu tố thúc đẩy chính chưa được trích cards cụ thể.
```

## Đã xong cycle 1

Sinh viên hoàn thành cycle 1 trong 10 phút với 1 brief, 5 nguồn (trong source log), 3 fact cards có trust tier và 1 báo cáo tóm tắt 3 phần.

Sản phẩm chưa hoàn chỉnh, nhưng quy trình đã được thử qua đủ các giai đoạn cốt lõi.

## Bước tiếp theo

Cycle 2 mục tiêu thu thêm 15 nguồn, trích 20 cards, upgrade ít nhất 50% cards lên verified. Cycle 3 hoàn thiện conflict queue và gap checklist.

Khi đã quen quy trình, sinh viên có thể tự động hoá các giai đoạn lặp đi lặp lại bằng script Python hoặc dùng Claude với SKILL.md được nạp.

Đọc Methodology.md sau khi xong cycle 1 để hiểu sâu hơn lý do từng giai đoạn được thiết kế như vậy. Đọc Architecture.md khi cần customize hoặc tự động hoá.
