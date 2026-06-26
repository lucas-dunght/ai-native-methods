# Source Log Template

Bản mẫu dạng table cho source log. Dùng được trong markdown hoặc convert sang CSV.

## Cấu trúc

| source_id | url | title | date_collected | query_used | source_type | language | authority_tier | collection_reason |
|---|---|---|---|---|---|---|---|---|
| S001 | https://example.com/report-2024 | "SEA Edtech Market 2024 Report" | 2026-06-26 | "Southeast Asia edtech market 2024" | học thuật | en | tier-1 | "Có số liệu market size 2023" |
| S002 | https://example.com/vietnam-data | "Vietnam Startup Investment Data 2024" | 2026-06-26 | "Vietnam edtech startup investment" | dữ liệu doanh nghiệp | vi | tier-2 | "Có dữ liệu startup VN" |
| S003 | ... | ... | ... | ... | ... | ... | ... | ... |

## Field reference

**source_id**. Định danh duy nhất theo format S followed by số 3 chữ số. S001, S002, S100.

**url**. URL gốc của nguồn. Lưu nguyên văn không rút gọn.

**title**. Tiêu đề bài hoặc tên báo cáo. Giữ nguyên ngôn ngữ gốc.

**date_collected**. Ngày thu thập theo format YYYY-MM-DD.

**query_used**. Query tìm kiếm đã dùng để tìm ra nguồn này.

**source_type**. Loại nguồn theo tập giá trị.
- báo chí
- học thuật
- blog cá nhân
- social media
- dữ liệu chính phủ
- tài liệu doanh nghiệp
- forum
- video
- podcast

**language**. Mã ngôn ngữ theo ISO 639-1. en, vi, zh, ja.

**authority_tier**. Phân hạng uy tín nguồn.
- tier-1. Chính phủ, tổ chức quốc tế, học thuật peer-reviewed, báo chí kinh tế lớn.
- tier-2. Báo chí phổ thông, blog chuyên gia có danh tiếng, preprint chưa peer-reviewed.
- tier-3. Social media, forum, blog ẩn danh.

**collection_reason**. Lý do thu nguồn này, liên quan câu hỏi nghiên cứu ra sao. Tránh thu bừa không có lý do.

## Lưu ý

Khi thu, không thu nguồn không có ngày publish hoặc không thể trace lại tác giả. Đây là dấu hiệu của nguồn không đáng tin.

Khi nghi ngờ tier, hạ xuống tier thấp hơn. Có thể nâng lên sau khi có cross-reference.

Khi nguồn cite một nguồn khác làm primary source, ghi cả hai và đánh dấu mối quan hệ trong field notes.
