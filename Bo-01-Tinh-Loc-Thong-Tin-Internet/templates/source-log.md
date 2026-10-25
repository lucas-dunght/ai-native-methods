# Source Log Template · Nhật ký Nguồn Thu thập (v2.0)

Nhật ký ghi lại toàn bộ các nguồn thu thập ở Giai đoạn 2, bao gồm cả đường dẫn nguồn gốc đầu tiên (`primary_origin_url`) để phục vụ kiểm tra chống phòng vang (`Echo-Chamber Check`).

## Cấu trúc CSV Chuẩn

```csv
source_id,url,primary_origin_url,title,date_published,date_collected,query_used,search_mode,extraction_method,source_type,language,authority_tier,raw_snapshot_path,collection_reason
S001,https://economysea.withgoogle.com/2024,https://economysea.withgoogle.com/2024,"e-Conomy SEA 2024 Report",2024-11-05,2026-10-25,"Southeast Asia digital payments GMV 2024",company,unified-extract,báo cáo nghiên cứu,en,tier-1,raw-sources/S001.md,"Số liệu gốc về quy mô GMV khu vực ĐNA"
S002,https://technews.example.com/sea-2024,https://economysea.withgoogle.com/2024,"Kinh tế số ĐNA bứt phá năm 2024",2024-11-08,2026-10-25,"kinh tế số Đông Nam Á 2024",news,ptc-search,báo chí,vi,tier-2,raw-sources/S002.md,"Bài báo phân tích lại báo cáo e-Conomy SEA"
S003,https://sbv.gov.vn/qr-payment-stats-2024,https://sbv.gov.vn/qr-payment-stats-2024,"Thống kê thanh toán không dùng tiền mặt 2024",2025-01-15,2026-10-25,"thanh toán QR Việt Nam tăng trưởng 2024",legal,unified-search,dữ liệu chính phủ,vi,tier-1,raw-sources/S003.md,"Số liệu thống kê chính thức từ Ngân hàng Nhà nước"
```

## Giải thích các cột bắt buộc

- **source_id.** Định danh duy nhất theo mẫu `S001`, `S002`...
- **url.** Đường dẫn trực tiếp nơi thu thập tài liệu.
- **primary_origin_url.** Đường dẫn của tài liệu gốc hoặc thông cáo gốc mà bài viết trích dẫn số liệu. Nếu chính `url` là nguồn gốc đầu tiên thì điền giống `url`. Nếu bài viết không nêu nguồn gốc thì điền `unknown`.
- **search_mode.** Chế độ tìm kiếm đã dùng (`auto`, `academic`, `legal`, `news`, `company`, `code`, `deep`, `hybrid`, `browser-scrape`).
- **extraction_method.** Công cụ bóc tách (`unified-search`, `unified-extract`, `ptc-search`, `tavily-map-extract`, `tavily-research`, `gstack-scrape`).
- **authority_tier.** Phân hạng uy tín của nguồn gồm `tier-1`, `tier-2`, `tier-3`.
- **raw_snapshot_path.** Đường dẫn tới tệp văn bản đã lọc PTC lưu trên đĩa để đối chiếu khi kiểm toán.
