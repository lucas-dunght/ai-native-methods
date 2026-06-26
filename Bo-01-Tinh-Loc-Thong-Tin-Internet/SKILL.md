---
name: internet-info-refinement
description: Tinh lọc và làm giàu thông tin thu thập từ internet thành tập sự thật có nguồn, có phân hạng tin cậy. Use when researching market data, doing literature review, building competitive analysis, due diligence, or any task where raw internet information needs to be turned into verified knowledge. Triggers on requests like "tổng hợp thông tin", "nghiên cứu thị trường", "phân tích đối thủ", "due diligence", "literature review", "tìm hiểu xu hướng". Do NOT trigger for tasks where source is already curated dataset.
license: MIT
---

# Internet Info Refinement Skill

## Mục đích

Skill này hướng dẫn agent đi qua bảy giai đoạn của phương pháp tinh lọc thông tin để biến tập nguồn internet thô thành tập fact cards có cấu trúc, đã được phân hạng tin cậy, không trùng lặp và có thể trace ngược về nguồn.

## Khi nào kích hoạt

Trigger trên các yêu cầu user.

- "Giúp tôi nghiên cứu thị trường X"
- "Tổng hợp thông tin về Y"
- "Phân tích đối thủ cạnh tranh của Z"
- "Literature review về topic W"
- "Due diligence cho startup V"
- "Tìm hiểu xu hướng U trong vài năm gần đây"

Không trigger khi.

- Dataset đã có sẵn và clean
- Câu hỏi yêu cầu paper kinh điển duy nhất
- User chỉ cần tóm tắt một bài báo cụ thể

## Quy trình thực hiện

Agent đi qua bảy giai đoạn theo thứ tự.

### Giai đoạn 1 · Brief

Hỏi user ba câu trước khi bắt đầu thu thập.

1. Câu hỏi nghiên cứu cụ thể là gì?
2. Phạm vi thời gian và địa lý của dữ liệu?
3. Tiêu chí loại trừ cho nguồn không phù hợp?

Nếu user chưa rõ một trong ba câu, không bắt đầu giai đoạn 2. Yêu cầu user làm rõ trước.

Output. Brief 1 đến 2 trang dạng markdown.

### Giai đoạn 2 · Thu thập có chủ đích

Lập danh sách query, thực hiện search, scrape, hoặc gọi API. Mỗi nguồn lưu vào source log với metadata đầy đủ.

Cấu trúc source log.

```csv
source_id, url, title, date_collected, query_used, source_type,
language, authority_tier, collection_reason
```

Authority tier theo quy tắc.
- Tier 1. Chính phủ, tổ chức quốc tế, học thuật peer-reviewed, báo chí kinh tế lớn.
- Tier 2. Báo chí phổ thông, blog chuyên gia, preprint.
- Tier 3. Social media, forum, blog ẩn danh.

Output. Source log đầy đủ và bộ nguồn thô.

### Giai đoạn 3 · Trích sự thật

Đọc từng nguồn và trích các fact card. Mỗi card là một đơn vị nguyên tử.

Cấu trúc fact card.

```yaml
fact_id: F-YYYY-NNN
content: "Một câu khẳng định cụ thể"
sources: [source_id_1, source_id_2]
fact_type: numerical-claim  # hoặc qualitative-claim, event, statement, definition, relationship
domain: market-data
role: evidence-for-thesis-1
date_extracted: YYYY-MM-DD
extracted_by: agent
notes: "Ghi chú thêm nếu cần"
```

Quy tắc trích. Một card chỉ chứa một sự thật. Phân biệt fact (X xảy ra) và statement (Y nói X). Không trích quan điểm chưa được attribute cụ thể.

Output. Tập fact cards thô.

### Giai đoạn 4 · Phát hiện trùng lặp và xung đột

Quét tập cards bằng similarity comparison. Cards trùng lặp thì merge sources. Cards xung đột thì đẩy vào conflict queue, KHÔNG tự chọn canonical.

Conflict queue entry format.

```markdown
## Conflict ID C-NNN
- Card A: F-YYYY-001 nói "..."
- Card B: F-YYYY-005 nói "..."
- Source độc lập của A: [...]
- Source độc lập của B: [...]
- Đề xuất phán xử: [agent đưa đề xuất, user quyết định cuối]
```

Output. Tập cards deduplicate cộng conflict queue.

CRITICAL. Agent KHÔNG tự xử conflict. Đẩy lên user phán xử.

### Giai đoạn 5 · Phát hiện lỗ hổng

Quét tập cards tìm các điểm nghi vấn cần thu thêm. Sự thật được nhắc nhưng không có chi tiết. Quy luật được khẳng định nhưng thiếu evidence. Xu hướng được mô tả nhưng thiếu thời gian.

Gap checklist format.

```markdown
## Gap G-NNN
- Description: Card F-YYYY-XXX claim Y nhưng không có nguồn support cho con số Z
- Suggested action: Thu thêm nguồn về Z từ tier-1 source
- Priority: high  # hoặc medium, low
```

Output. Gap checklist.

### Giai đoạn 6 · Phân hạng tin cậy và làm giàu

Gán nhãn `trust_tier` cho mỗi card.

- Verified. Hai nguồn độc lập hoặc một nguồn tier-1.
- Probable. Một nguồn tier-1 hoặc tier-2 không có cross-reference.
- Unverified. Chỉ tier-3 hoặc không rõ.

Làm giàu metadata.

```yaml
enrichment:
  cross_references: [F-YYYY-XXX, F-YYYY-YYY]
  classification: tag-1, tag-2
  recency_status: current  # hoặc historical, outdated
  importance_rank: high
  gaps_implied: [G-NNN]
```

Output. Tập cards hoàn chỉnh.

### Giai đoạn 7 · Tổng hợp

Viết báo cáo ba phần.

1. Kết luận chính dựa trên verified facts. Mọi khẳng định trích dẫn `[F-YYYY-XXX]`.
2. Giả thuyết dựa trên probable facts cần kiểm chứng.
3. Câu hỏi mở từ gap checklist chưa giải quyết.

Output. Báo cáo cuối plus tập cards xuất ra file.

## Ranh giới vai trò

Agent làm.

- Thu thập nguồn
- Trích fact cards theo bản mẫu
- Phát hiện trùng lặp bằng similarity
- Phát hiện xung đột structural
- Phát hiện gap
- Gán trust tier theo quy tắc cứng
- Làm giàu metadata
- Tổng hợp báo cáo

Agent KHÔNG làm.

- Tự chọn canonical fact khi xung đột
- Fabricate fact không có trong nguồn
- Paraphrase con số hoặc tên riêng (giữ nguyên văn)
- Skip giai đoạn nào của quy trình
- Bắt đầu giai đoạn 2 khi brief chưa rõ

## Forcing functions

Bốn cơ chế cứng.

1. Không bắt đầu giai đoạn 2 khi brief chưa có đủ ba thành phần (câu hỏi, phạm vi, tiêu chí loại trừ).
2. Mọi card nhãn verified phải trace ngược về ít nhất hai nguồn độc lập hoặc một nguồn tier-1.
3. Conflict queue phải có quyết định human trước khi xuất báo cáo cuối.
4. Gap checklist được nêu trong phần 3 của báo cáo cuối, không che giấu.

## Templates

Templates đi kèm trong thư mục `templates/`.
- `source-log.md` Bản mẫu source log
- `fact-card.yaml` Bản mẫu fact card
- `conflict-queue.md` Bản mẫu conflict queue
- `gap-checklist.md` Bản mẫu gap checklist
- `enrichment-pass.md` Bản mẫu enrichment pass
- `synthesis-prompt.md` Prompt cho LLM ở giai đoạn 7

## Anti-pattern cần tránh

- Paste nguồn vào LLM và nhờ tóm tắt mà không qua giai đoạn 3-6.
- Trộn quan điểm với sự thật trong cùng một card.
- Cho LLM tự chọn canonical fact khi xung đột.
- Bỏ qua nguồn unverified mà không xem xét.
- Báo cáo cuối thay thế tập fact cards (cards là sản phẩm chính).

## Đo lường thành công

- Tỷ lệ cards verified >= 40% tổng cards
- Conflict queue được clear trước khi xuất báo cáo
- Gap checklist < 10 item trong phần 3 báo cáo
- Mọi khẳng định trong báo cáo trace ngược về fact card và về nguồn gốc
