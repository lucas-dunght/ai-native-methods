# Bộ 01 · Phương pháp tinh lọc và làm giàu thông tin từ internet

**Phiên bản 2026.10 (v2.0)**

Khung làm việc đa giai đoạn biến thông tin thô thu thập từ internet thành tri thức có chất lượng kiểm chứng cơ học. Đầu vào là kết quả tìm kiếm đa tín hiệu (`unified-search` / `tavily-*`), trích xuất ngữ cảnh cô lập kiểu PTC (`Programmatic Tool Calling`), cào dữ liệu qua trình duyệt phiên thật chỉ đọc (`gstack /scrape`) và báo cáo nghiên cứu sâu (`tavily-research`). Đầu ra là một tập sự thật nguyên tử (`Fact Cards`) có nguồn gốc độc lập, có nhãn nhận định (`Fable 5.1 Claim Discipline`), có phân hạng tin cậy ba mức, đã khử phòng vang (`Echo-Chamber Check`), sẵn sàng chuyển giao trực tiếp sang Bộ 02 (`Kernel Registry SOT`) và Bộ 03 (`Vibecode Kit v6.1`).

## Khi nào dùng

Sinh viên, nhà nghiên cứu hoặc đội ngũ sản phẩm cần tổng hợp thông tin từ nhiều nguồn web với mức độ tin cậy không đồng nhất trong các tình huống điển hình.

Nghiên cứu thị trường cho luận văn hoặc đồ án tốt nghiệp. Tổng quan tài liệu khoa học và công nghệ. Thẩm định chuyên sâu (`due diligence`) cho startup hoặc dự án đầu tư. Phân tích đối thủ cạnh tranh và bảng giá thị trường. Theo dõi văn bản pháp lý và xu hướng ngành. Xây dựng tập dữ liệu sự thật nền tảng (`L1 Stored Facts`) cho hệ thống AI Agent.

## Khi nào không dùng

Khi nguồn dữ liệu đã được kiểm chứng và chuẩn hóa sẵn, ví dụ tập dữ liệu học thuật chuẩn hoặc cơ sở dữ liệu nội bộ đã qua kiểm toán. Khi câu hỏi nghiên cứu chỉ yêu cầu tóm tắt một bài báo hoặc một tài liệu đơn lẻ duy nhất. Khi tác vụ ở mức `R0` chỉ cần tra cứu nhanh một cú pháp lệnh trong 1 phút.

## Đặc điểm cốt lõi của bản v2.0 (2026.10)

Phương pháp này khác biệt hoàn toàn với việc dán kết quả tìm kiếm vào AI và nhờ tóm tắt ở bảy điểm cốt lõi.

Một, **Định tuyến tìm kiếm đa tín hiệu và cô lập ngữ cảnh PTC**. Tự động chọn chế độ tìm kiếm (`academic`, `legal`, `news`, `company`, `code`, `deep`, `hybrid`) qua xoay vòng đa công cụ (`Tavily` + `Exa` + `Linkup`). Toàn bộ dữ liệu HTML thô hàng trăm KB được lưu ở bộ đệm đĩa (`/tmp/` hoặc `raw-sources/`) và lọc bằng script Python trước khi đưa vào ngữ cảnh của AI, giúp giảm 100 đến 200 lần nhiễu.

Hai, **Thu thập trang đăng nhập chỉ đọc và rào chắn chống Prompt Injection**. Với các trang web động hoặc cần phiên đăng nhập thật, sử dụng trình duyệt chỉ đọc (`gstack /scrape`) và đóng băng luồng cào lặp lại thành kỹ năng chạy trong 200ms (`/skillify`). Mọi nội dung từ web đều bị cô lập trong rào chắn `UNTRUSTED WEB CONTENT` để ngăn chặn tấn công chèn lệnh ẩn.

Ba, **Kỷ luật nhận định Fable 5.1 và trích dẫn nguyên văn có mã băm**. Mỗi `Fact Card` bắt buộc gắn nhãn nhận định (`OBSERVED`, `DERIVED`, `PRIOR`, `ASSUMED`), lưu kèm câu trích dẫn nguyên văn (`exact_quote`) và mã băm nội dung (`content_hash`) để chống AI tự ý làm tròn số hoặc suy diễn.

Bốn, **Kiểm tra chống phòng vang (`Citation Graph / Echo-Chamber Rule`)**. Hai bài báo cùng dẫn lại một báo cáo gốc chỉ được tính là một nguồn độc lập (`1 datum`). Hệ thống truy vết `primary_origin_url` trước khi cấp nhãn `verified`.

Năm, **Phán xử xung đột bằng thẻ quyết định `Decision Brief D<N>`**. Khi hai nguồn mâu thuẫn, AI tuyệt đối không tự chọn sự thật chuẩn (`canonical`). AI đóng gói xung đột thành thẻ `D<N>` gồm giải thích `ELI10`, rủi ro `Stakes`, điểm độ phủ `Completeness X/10` và phương án khuyến nghị `(recommended)` để con người phán xử.

Sáu, **Làm giàu bốn chiều và cầu nối tự động sang Bộ 02**. Tri thức được đối chiếu chéo, gắn phân loại, kiểm tra độ mới và xuất thẳng sang định dạng `L1-stored-fact.yaml` của Bộ 02 (`Kernel Registry`).

Bảy, **Cổng kiểm tra định lượng (`Constraint Loop Gate`)**. Trước khi xuất báo cáo cuối, script tự động kiểm tra 4 chỉ số cứng gồm tỷ lệ `verified >= 40%`, hàng đợi xung đột bằng `0`, danh sách lỗ hổng `< 10` và `100%` mã trích dẫn `[F-YYYY-NNN]` đều tồn tại thật trên đĩa.

## Cấu trúc thư mục

```
Bo-01-Tinh-Loc-Thong-Tin-Internet/
├── README.md                                        (file này)
├── Methodology.md                                   Triết lý v2.0 và quy trình 7 giai đoạn nâng cấp
├── Architecture.md                                  Kiến trúc kỹ thuật 6 module, PTC sandbox và data structures
├── SKILL.md                                         Đặc tả skill v2.0.0 cài đặt cho AI Agent
├── Quick-Start.md                                   Thực hành trọn vòng lặp trong 10 phút
├── templates/
│   ├── source-log.md                                Nhật ký nguồn kèm primary_origin_url và search_mode
│   ├── fact-card.yaml                               Thẻ sự thật nguyên tử kèm claim_label và exact_quote
│   ├── conflict-queue.md                            Hàng đợi xung đột trình bày theo thẻ Decision Brief D<N>
│   ├── gap-checklist.md                             Danh sách lỗ hổng kèm gợi ý truy vấn đa tín hiệu
│   ├── enrichment-pass.md                           Bản mẫu làm giàu 4 chiều và kiểm tra phòng vang
│   └── extraction-and-synthesis-prompts.md          Prompt trích xuất chống injection và tổng hợp báo cáo
├── references/
│   ├── multi-signal-search-and-ptc.md               Giao thức tìm kiếm đa tín hiệu và cô lập ngữ cảnh PTC
│   ├── authenticated-scrape-and-guardrails.md       Giao thức cào trình duyệt chỉ đọc và chống Prompt Injection
│   └── citation-graph-and-conflict-gate.md          Giao thức khử phòng vang, thẻ D<N> và cổng định lượng
└── examples/
    └── worked-example.md                            Ví dụ thực chiến end-to-end (Thị trường Thanh toán số ĐNA)
```

## Bắt đầu nhanh

Đọc `Quick-Start.md` để chạy phương pháp lần đầu trong 10 phút trên một bài toán mẫu. Sau đó đọc `Methodology.md` để nắm vững triết lý 4 nguyên tắc và 7 giai đoạn v2.0. Cuối cùng đọc `Architecture.md` và thư mục `references/` khi cần triển khai thu thập tự động quy mô lớn hoặc nối dữ liệu sang Bộ 02 và Bộ 03.

## Đóng góp

Phương pháp được thiết kế để tiến hóa liên tục cùng hệ sinh thái AI-Native. Sinh viên, giảng viên hoặc kỹ sư áp dụng phát hiện điểm nghẽn vui lòng ghi nhận vào nhật ký dự án để cập nhật cho các phiên bản tiếp theo.
