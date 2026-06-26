# Architecture · Kiến trúc kỹ thuật của Bộ 01

## Tổng quan

Kiến trúc gồm năm thành phần. Source Collector, Fact Extractor, Conflict Detector, Trust Classifier, Synthesizer. Mỗi thành phần là một module có input và output cố định. Các module nối với nhau theo pipeline tuần tự với checkpoint giữa các module để con người có thể can thiệp.

Toàn bộ pipeline có thể chạy thủ công với cặp người dùng và AI agent, hoặc tự động một phần với scripts hỗ trợ. Khuyến nghị cho sinh viên là chạy thủ công ở cycle đầu để hiểu logic, sau đó tự động hoá các tác vụ lặp lại.

## Sơ đồ luồng

```
Brief nghiên cứu → Source Collector → Source Log + Raw Sources
                                                  ↓
                          Fact Extractor ← (đọc raw sources)
                                                  ↓
                                          Fact Cards (raw)
                                                  ↓
                          Conflict Detector → Conflict Queue
                                                  ↓
                                          Fact Cards (deduped)
                                                  ↓
                          Trust Classifier → Cards có nhãn tin cậy
                                                  ↓
                                          Enrichment Pass
                                                  ↓
                          Synthesizer → Báo cáo cuối + Cards xuất
```

Checkpoint con người giữa các bước. Sau Conflict Detector, người phán xử conflict queue. Sau Trust Classifier, người review nhãn tin cậy. Trước Synthesizer, người review gap checklist.

## Thành phần 1 · Source Collector

Chịu trách nhiệm thu thập nguồn từ internet và lưu kèm metadata.

### Input

Brief nghiên cứu từ giai đoạn 1 chứa câu hỏi nghiên cứu, phạm vi, tiêu chí loại trừ.

### Output

Source Log dạng markdown table hoặc CSV, mỗi dòng là một nguồn với các cột bắt buộc.

```
source_id, url, title, date_collected, query_used, source_type,
 language, authority_tier, collection_reason
```

Trong đó `source_type` thuộc tập {báo chí, học thuật, blog cá nhân, social media, dữ liệu chính phủ, tài liệu doanh nghiệp, forum, video, podcast}.

`authority_tier` thuộc tập {tier-1, tier-2, tier-3} dựa trên uy tín của nguồn. Tier 1 là chính phủ, tổ chức quốc tế, học thuật peer-reviewed, báo chí kinh tế lớn. Tier 2 là báo chí phổ thông, blog của chuyên gia có danh tiếng, preprint chưa peer-reviewed. Tier 3 là social media, forum, blog ẩn danh.

### Công cụ

Web search qua một search engine hoặc API search. Web scraping qua Python với requests và BeautifulSoup hoặc Playwright cho trang dynamic. Gọi API khi có thể (Twitter API, Reddit API, GitHub API). Manual collection từ database học thuật.

### Lưu ý sinh viên

Tôn trọng robots.txt và terms of service của website. Không scrape ồ ạt site nhỏ. Khi không chắc, dùng API chính thức hoặc liên hệ chủ site.

## Thành phần 2 · Fact Extractor

Đọc từng nguồn thô và trích các mẩu sự thật vào fact card.

### Input

Một nguồn thô từ Source Collector. Có thể là HTML, PDF, markdown, transcript.

### Output

Một hoặc nhiều fact card cho mỗi nguồn. Mỗi card có cấu trúc YAML hoặc JSON.

```yaml
fact_id: F-2026-001
content: "Thị trường X tăng trưởng 18.5% trong năm 2024"
sources: [source_id_3, source_id_12]
fact_type: numerical-claim
domain: market-data
role: evidence-for-thesis-1
date_extracted: 2026-06-26
extracted_by: human  # hoặc agent
notes: "Số liệu công bố trong báo cáo quý 4"
```

Các trường bắt buộc là fact_id, content, sources, fact_type, date_extracted. Các trường khác là tuỳ chọn nhưng nên có cho dự án nghiêm túc.

`fact_type` thuộc tập {numerical-claim, qualitative-claim, event, statement, definition, relationship}. Phân biệt rõ giữa "X xảy ra" (event hoặc qualitative-claim) và "Y nói X" (statement).

### Công cụ

LLM với prompt template cho extraction. Prompt template trong thư mục templates ở file fact-extraction-prompt.md. Prompt yêu cầu LLM trả về JSON theo schema cố định.

### Lưu ý

Một fact card chỉ chứa một sự thật nguyên tử. Không gộp hai sự thật vào một card. Khi nghi ngờ, tách thành hai cards.

## Thành phần 3 · Conflict Detector

Quét tập fact cards để tìm trùng lặp và xung đột.

### Input

Tập fact cards thô từ Fact Extractor.

### Output

Hai thứ. Một tập fact cards đã deduplicate. Một conflict queue chứa các cặp cards mâu thuẫn nhau.

### Logic

Hai cards trùng lặp khi `content` của chúng nói cùng một sự thật với cùng giá trị. Phát hiện qua so sánh ngữ nghĩa (embedding similarity) hoặc so sánh cấu trúc nếu cards có schema rõ ràng. Khi trùng, merge các sources vào một card duy nhất.

Hai cards xung đột khi nói cùng một sự thật với giá trị khác nhau. Ví dụ một card nói thị trường tăng 18%, card khác nói thị trường tăng 25%. Đẩy cả hai vào conflict queue, không tự chọn.

### Công cụ

Vector embedding cho similarity search. Có thể dùng sentence-transformers hoặc OpenAI embeddings. Hoặc đơn giản hơn dùng LLM với prompt comparison cho từng cặp cards (tốn token hơn nhưng dễ thực hiện).

### Lưu ý

Threshold similarity nên đặt cao hơn 0.85 để tránh false positive merge. Khi nghi ngờ, giữ tách và đẩy vào hàng đợi review.

## Thành phần 4 · Trust Classifier

Gán nhãn tin cậy ba mức cho mỗi fact card.

### Input

Tập fact cards đã deduplicate sau Conflict Detector và phán xử conflict queue.

### Output

Tập fact cards có thêm trường `trust_tier` với giá trị verified, probable, hoặc unverified.

### Logic

Verified khi card có ít nhất một trong hai điều kiện. Hai nguồn độc lập (không cite lẫn nhau) cùng xác nhận. Một nguồn cấp cao tier-1 xác nhận.

Probable khi card có một nguồn tier-1 hoặc tier-2 đáng tin nhưng chưa có cross-reference.

Unverified khi card chỉ có nguồn tier-3 hoặc nguồn không rõ.

### Công cụ

Có thể tự động hoá bằng quy tắc cứng dựa trên metadata trong source log. Đếm số nguồn độc lập, tier cao nhất, có cross-reference không. Output deterministic.

### Lưu ý

"Nguồn độc lập" là khái niệm khó định nghĩa rigorously. Quy tắc đơn giản. Hai báo chí cite cùng một báo cáo gốc thì không độc lập, chỉ tính một nguồn. Hai báo cáo nghiên cứu của hai tổ chức khác nhau thì độc lập kể cả khi cùng một topic.

## Thành phần 5 · Enrichment Pass

Làm giàu metadata cho mỗi fact card.

### Input

Tập fact cards đã được Trust Classifier.

### Output

Cards có thêm các trường metadata làm giàu.

```yaml
enrichment:
  cross_references: [F-2026-005, F-2026-012]  # các facts liên quan
  classification: market-growth, fintech-segment
  recency_status: current  # hoặc historical, outdated
  importance_rank: high  # hoặc medium, low
  gaps_implied: [needs-data-for-2025-Q1, needs-source-for-claim-X]
```

### Logic

Cross-references tìm bằng similarity search nhưng với threshold thấp hơn deduplication, để tìm relate chứ không phải trùng.

Classification gán bằng LLM với taxonomy đã định sẵn trong project.

Recency status tự động dựa trên ngày publish của nguồn so với ngày thu thập.

Importance rank được người dùng đặt thủ công dựa trên role trong lập luận.

Gaps implied phát hiện bằng LLM khi quét card, tìm xem có claim hoặc số liệu nào card này dựa vào mà chưa có card khác trong tập support không.

## Thành phần 6 · Synthesizer

Tổng hợp tập cards thành báo cáo cuối.

### Input

Tập fact cards hoàn chỉnh sau Enrichment Pass.

### Output

Báo cáo cuối ba phần. Phần 1 kết luận chính dựa trên verified facts. Phần 2 giả thuyết dựa trên probable facts. Phần 3 câu hỏi mở từ gap checklist và unverified facts cần kiểm chứng.

### Logic

Mỗi câu trong báo cáo trích dẫn fact card bằng ID dạng inline `[F-2026-001]`. Khi pre-publish, generate phần References tự động từ tập card IDs đã được trích dẫn.

### Công cụ

LLM với prompt template trong templates/synthesis-prompt.md. Prompt yêu cầu LLM chỉ được trích dẫn fact card có trong tập input. Không được fabricate facts mới.

### Lưu ý

LLM có xu hướng paraphrase và mất chính xác. Yêu cầu LLM giữ nguyên văn các con số và tên riêng. Sau khi LLM ra báo cáo, làm pass thủ công kiểm tra các con số và tên có match với fact cards không.

## Data structures tổng kết

Toàn bộ pipeline xuất ra ba artifact chính cho mỗi cycle nghiên cứu.

```
research-cycle-YYYY-MM-DD/
├── brief.md                       (giai đoạn 1)
├── source-log.csv                 (giai đoạn 2)
├── raw-sources/                   (giai đoạn 2)
│   ├── source-001.html
│   ├── source-002.pdf
│   └── ...
├── fact-cards/                    (giai đoạn 3-6)
│   ├── F-2026-001.yaml
│   ├── F-2026-002.yaml
│   └── ...
├── conflict-queue.md              (giai đoạn 4)
├── gap-checklist.md               (giai đoạn 5)
├── enrichment-log.md              (giai đoạn 6)
└── report-final.md                (giai đoạn 7)
```

Cấu trúc thư mục này tái sử dụng được giữa các cycle. Khi sinh viên làm cycle thứ hai cho cùng một đề tài, có thể nạp lại fact cards cũ và bổ sung cards mới.

## Tools stack đề xuất

Đối với sinh viên không có ngân sách, stack tools đề xuất gồm.

LLM. Claude qua API hoặc Cursor. Hoặc GPT-4 qua API. Hoặc model open-source local như Llama nếu có GPU.

Search engine. Brave Search API miễn phí mức cơ bản. Hoặc Tavily Search API. Hoặc Serper.

Web scraping. Python với requests và BeautifulSoup cho trang tĩnh. Playwright cho trang dynamic.

Storage. Markdown files trong Git repo. YAML cho fact cards. CSV cho source log.

Embedding. sentence-transformers chạy local hoặc OpenAI embeddings API.

Vector search. Đối với tập card nhỏ dưới 1000 cards, không cần vector DB phức tạp. Chỉ cần numpy hoặc faiss in-memory.

## Tích hợp với Bộ 02 Kernel Registry

Đầu ra của Bộ 01 (fact cards) tương ứng với L1 Sự thật lưu sẵn trong Bộ 02 Kernel Registry. Sinh viên có thể chuyển trực tiếp tập fact cards từ Bộ 01 vào registry của Bộ 02 sau cycle nghiên cứu hoàn tất. Schema fact card được thiết kế tương thích.

## Tích hợp với Bộ 03 Vibecode Kit

Khi sinh viên dùng Vibecode Kit để xây ứng dụng dựa trên kết quả nghiên cứu của Bộ 01, fact cards là input cho TIP (Task Intent Prompt) và Blueprint. AI agent được giao việc có thể đọc fact cards trực tiếp để có context chính xác cho nhiệm vụ.
