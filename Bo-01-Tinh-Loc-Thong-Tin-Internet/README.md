# Bộ 01 · Phương pháp tinh lọc và làm giàu thông tin từ internet

**Phiên bản 2026.06**

Khung làm việc đa giai đoạn biến thông tin thô thu thập từ internet thành tri thức có chất lượng kiểm chứng được. Đầu vào là kết quả tìm kiếm, web scraping, dump tài liệu, kết quả gọi API. Đầu ra là một tập sự thật có nguồn, có phân hạng tin cậy, không trùng lặp, có đối chiếu chéo, sẵn sàng dùng trong nghiên cứu hoặc ra quyết định.

## Khi nào dùng

Sinh viên hoặc người làm nghiên cứu cần tổng hợp thông tin từ nhiều nguồn web với mức độ tin cậy không đồng nhất. Sử dụng cho các tình huống điển hình.

Nghiên cứu thị trường cho luận văn hoặc đồ án tốt nghiệp. Tổng quan tài liệu khoa học. Due diligence cho startup hoặc dự án M&A. Phân tích đối thủ cạnh tranh. Theo dõi xu hướng ngành. Xây dữ liệu nền cho dự án phân tích.

## Khi nào không dùng

Khi nguồn dữ liệu đã được kiểm chứng và có cấu trúc, ví dụ dataset học thuật chuẩn. Khi câu hỏi nghiên cứu yêu cầu một nguồn nhất quán duy nhất ví dụ một paper kinh điển. Khi thời gian không cho phép đi qua đủ giai đoạn tinh lọc, trong trường hợp đó dùng tổng hợp nhanh không có gate kiểm chứng.

## Đặc điểm cốt lõi

Phương pháp này khác với việc chỉ paste kết quả Google vào AI và nhờ tóm tắt ở bốn điểm.

Một, mọi sự thật đều có nguồn truy được. Không có câu trả lời mồ côi.

Hai, các sự thật xung đột nhau được nêu ra để người quyết, không phải AI tự chọn.

Ba, mỗi sự thật có phân hạng tin cậy ba mức là verified, probable, unverified.

Bốn, tri thức được làm giàu bằng đối chiếu chéo và metadata, không phải chỉ tóm tắt.

## Cấu trúc thư mục

```
Bo-01-Tinh-Loc-Thong-Tin-Internet/
├── README.md            (file này)
├── Methodology.md       Triết lý và quy trình 7 giai đoạn
├── Architecture.md      Kiến trúc kỹ thuật và data structures
├── SKILL.md             Đặc tả skill cài đặt vào Claude hoặc agent khác
├── Quick-Start.md       Bắt đầu trong 10 phút
├── templates/
│   ├── source-log.md
│   ├── fact-card.yaml
│   ├── conflict-queue.md
│   ├── gap-checklist.md
│   └── enrichment-pass.md
└── examples/
    └── worked-example.md  (ẩn danh, lĩnh vực fintech tổng quát)
```

## Bắt đầu nhanh

Đọc Quick-Start.md để có thể chạy phương pháp lần đầu trong 10 phút trên một bài toán nhỏ. Sau khi đã chạy thử, đọc Methodology.md để hiểu vì sao phương pháp được thiết kế như vậy. Cuối cùng đọc Architecture.md nếu cần customize phương pháp cho dự án cụ thể.

## Đóng góp

Phương pháp được thiết kế để tiến hoá. Sinh viên hoặc giảng viên áp dụng phát hiện vấn đề hoặc đề xuất cải tiến vui lòng ghi vào tài liệu dự án và phản hồi lại. Phiên bản mới sẽ phản ánh trải nghiệm thực tế.
