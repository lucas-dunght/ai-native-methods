# Methodology · Tinh lọc và làm giàu thông tin từ internet (v2.0 · 2026.10)

## Triết lý nền

Internet là kho thông tin khổng lồ nhưng độ tin cậy phân hóa mạnh, độ nhiễu định dạng (HTML rác, thanh điều hướng, quảng cáo) rất lớn và hiệu ứng phòng vang (hàng chục trang báo chép lại cùng một nguồn) diễn ra phổ biến. Khi đổ thẳng kết quả tìm kiếm thô vào cửa sổ ngữ cảnh của AI để nhờ tóm tắt, hai thảm họa xảy ra cùng lúc. Một là ngữ cảnh của AI bị ngập bởi hàng trăm nghìn ký tự rác làm suy giảm năng lực suy luận. Hai là AI khuếch đại cả tín hiệu lẫn tin đồn, tạo ra một văn bản trôi chảy nhưng trộn lẫn sự thật, ý kiến chủ quan và số liệu sai lệch.

Phương pháp Tinh lọc và Làm giàu Thông tin v2.0 tiếp cận theo hướng cơ học và minh bạch.
- Không đổ rác vào ngữ cảnh suy luận. Dữ liệu thô được xử lý qua lớp đệm cô lập kiểu **PTC (`Programmatic Tool Calling`)** để chỉ đưa tín hiệu tinh khiết vào mô hình.
- Không yêu cầu AI làm thẩm phán cuối cùng khi các nguồn mâu thuẫn. AI thực thi các quy tắc tất định gồm phân loại nguồn, trích xuất sự thật nguyên tử kèm trích dẫn nguyên văn (`exact_quote`), kiểm tra đồ thị nguồn gốc (`Citation Graph`) để khử phòng vang và đóng gói mọi xung đột thành thẻ **Decision Brief `D<N>`** cho con người phán xử.
- Sản phẩm chính của phương pháp là **tập thẻ sự thật (`Fact Cards`) có thể truy vết và nạp thẳng vào hệ thống khác (như Bộ 02 Kernel Registry và Bộ 03 Vibecode Kit)**. Báo cáo tổng hợp cuối cùng chỉ là một góc nhìn xuất ra từ tập thẻ sự thật đó.

## Sáu nguyên tắc cốt lõi (v2.0)

### Nguyên tắc 1 · Mọi sự thật đều có nguồn gốc độc lập và nhãn nhận định (`Fable 5.1 Claim Discipline`)

Không có sự thật mồ côi trong tập đầu ra. Mỗi thẻ sự thật phải gắn với ít nhất một định danh nguồn trong `source-log.csv`, lưu câu trích dẫn nguyên văn (`exact_quote`) và bắt buộc mang một trong bốn nhãn nhận định theo chuẩn Fable 5.1.
- **OBSERVED.** Đọc và trích trực tiếp từ tài liệu nguồn đã thu thập trong phiên làm việc hiện tại.
- **DERIVED.** Tính toán hoặc suy diễn tất định từ các thẻ `OBSERVED` thông qua công thức rõ ràng.
- **PRIOR.** Tri thức nền có sẵn của mô hình AI chưa được kiểm chứng bằng nguồn thu thập trong phiên. Thẻ `PRIOR` không bao giờ được nâng lên hạng `verified`.
- **ASSUMED.** Giả định làm việc tạm thời, bắt buộc phải đi kèm mô tả rủi ro nếu sai và gắn vào danh sách lỗ hổng (`gap-checklist.md`).

### Nguyên tắc 2 · Cô lập ngữ cảnh tìm kiếm và Rào chắn chống Prompt Injection

Một lệnh tìm kiếm toàn văn bản thường trả về từ 200.000 đến 400.000 ký tự HTML và văn bản phụ. Đưa trực tiếp khối dữ liệu này vào ngữ cảnh của Agent làm loãng sự chú ý và gây tốn kém token.

Phương pháp v2.0 bắt buộc tách bước **Tải dữ liệu (`Fetch/Save`)** và bước **Suy luận (`Reason`)**. Dữ liệu thô từ `unified-search` hoặc `tavily-*` được lưu xuống đĩa (`/tmp/` hoặc `raw-sources/`), sau đó lọc qua script Python để chỉ trích xuất các đoạn văn chứa số liệu, mốc thời gian và thuật ngữ mục tiêu. Đồng thời, toàn bộ nội dung từ internet đều được bao bọc trong rào chắn `UNTRUSTED WEB CONTENT` để ngăn chặn các đoạn mã hoặc chỉ dẫn độc hại cài cắm trên trang web điều khiển ngược lại Agent.

### Nguyên tắc 3 · Xung đột không bị AI tự xử mà trình qua thẻ `Decision Brief D<N>`

Khi hai nguồn nói khác nhau về cùng một sự kiện hoặc cùng một con số, AI tuyệt đối không tự chọn nguồn nào diễn đạt mượt hơn làm sự thật chuẩn (`canonical`). AI có trách nhiệm đặt cả hai thẻ vào `conflict-queue.md` và lập thẻ quyết định **Decision Brief `D<N>`** gồm giải thích ngắn gọn (`ELI10`), hậu quả nếu chọn sai (`Stakes`), phân tích độ uy tín và phương pháp luận của từng nguồn, điểm độ phủ (`Completeness X/10`) cùng một phương án khuyến nghị `(recommended)` để con người ký duyệt.

### Nguyên tắc 4 · Phân hạng tin cậy ba mức có khử phòng vang (`Echo-Chamber Check`)

Mỗi sự thật trong tập đầu ra mang một trong ba nhãn tin cậy dựa trên số lượng **nguồn gốc độc lập (`independent_origin_count`)**, không đếm theo số lượng đường link bài viết. Hai hay mười bài báo cùng trích dẫn lại một báo cáo gốc duy nhất chỉ được tính là một nguồn độc lập (`1 datum`).

- **Verified.** Thẻ mang nhãn `OBSERVED` hoặc `DERIVED`, được xác nhận bởi ít nhất **hai nguồn gốc độc lập (`independent_origin_count >= 2`)** hoặc **một nguồn cấp cao chính thức hạng `tier-1`** (cơ quan nhà nước, tổ chức quốc tế, báo cáo kiểm toán chính thức, công trình khoa học peer-reviewed).
- **Probable.** Thẻ có một nguồn `tier-1` (báo chí kinh tế, báo cáo tư vấn) hoặc `tier-2` đáng tin cậy nhưng mới chỉ có một gốc dữ liệu duy nhất (`independent_origin_count == 1`).
- **Unverified.** Thẻ chỉ có nguồn `tier-3` (mạng xã hội, diễn đàn, blog ẩn danh), hoặc không truy được nguồn gốc đầu tiên, hoặc mang nhãn `PRIOR` / `ASSUMED`. Vẫn lưu trữ để theo dõi tín hiệu sớm nhưng cấm đưa vào phần kết luận cốt lõi.

### Nguyên tắc 5 · Làm giàu bốn chiều thay vì tóm tắt

Tóm tắt làm mất chi tiết. Làm giàu bổ sung bốn lớp thông tin cấu trúc mà nguồn đơn lẻ không có.
- **Một, đối chiếu chéo (`Cross-reference`).** Liên kết các thẻ sự thật bổ sung hoặc giải thích nguyên nhân và hệ quả cho nhau.
- **Hai, phân loại đa trục (`Taxonomy classification`).** Gắn nhãn lĩnh vực, vai trò trong luận điểm và mức độ trọng yếu.
- **Ba, định vị ngữ cảnh và độ tươi (`Recency & Provenance`).** Ghi nhận ngày công bố của dữ liệu gốc, ngày thu thập, chế độ tìm kiếm (`search_mode`) và công cụ bóc tách đã dùng.
- **Bốn, phát hiện lỗ hổng kéo theo (`Implied Gaps`).** Khi thẻ A nhắc tới một tiền đề B chưa có bằng chứng trong kho, tự động sinh mục lỗ hổng `G-NNN` để truy vấn bù đắp.

### Nguyên tắc 6 · Kiểm chứng cơ học bằng Vòng lặp Ràng buộc (`Constraint Loop`)

Mọi báo cáo nghiên cứu trước khi bàn giao phải đi qua bước kiểm tra tự động để đảm bảo không có mã trích dẫn ảo, không có con số bị làm tròn sai lệch so với `Fact Card` gốc và không còn xung đột treo.

## Quy trình bảy giai đoạn chi tiết

```
Giai đoạn 1: Brief & Thẻ D1
     ↓
Giai đoạn 2: Thu thập Đa tín hiệu + Cô lập PTC + /scrape
     ↓
Giai đoạn 3: Trích Fact Cards Nguyên tử (Fable 5.1 Claim Labels)
     ↓
Giai đoạn 4: Khử trùng lặp + Khử phòng vang + Hàng đợi Xung đột D<N>
     ↓
Giai đoạn 5: Phát hiện Lỗ hổng (Gap Checklist + Query bù đắp)
     ↓
Giai đoạn 6: Phân hạng Tin cậy (Verified/Probable/Unverified) + Làm giàu 4 chiều
     ↓
Giai đoạn 7: Cổng Constraint Loop + Báo cáo 3 phần + Xuất sang Bộ 02
```

### Giai đoạn 1 · Định nghĩa câu hỏi, phạm vi và tiêu chí loại trừ

Viết xuống bốn nội dung cốt lõi vào `brief.md` gồm câu hỏi nghiên cứu gắn với quyết định thực tế, phạm vi thời gian và địa lý, tiêu chí loại trừ kèm tên miền ưu tiên hoặc cấm cùng ngưỡng chất lượng đầu ra. Nếu yêu cầu ban đầu còn mơ hồ, Agent dùng thẻ `Decision Brief D1` để giúp người dùng khóa phạm vi ngay từ đầu.

### Giai đoạn 2 · Thu thập có chủ đích qua Định tuyến Đa tín hiệu và Cô lập PTC

Thay vì tìm kiếm thủ công rời rạc, Agent phối hợp ba lớp công cụ.
- **Lớp 1 · Tìm kiếm đa tín hiệu (`unified-search` / `tavily-search`).** Chọn chế độ phù hợp (`academic`, `legal`, `news`, `company`, `deep`, `hybrid`), lưu kết quả thô xuống đĩa và lọc qua Python sandbox để chọn các URL có điểm tín hiệu cao nhất.
- **Lớp 2 · Bóc tách sâu (`tavily-map`, `tavily-extract`, `tavily-crawl`, `tavily-research`).** Lập bản đồ cấu trúc website, bóc tách toàn văn Markdown sạch của những trang được chọn và chạy nghiên cứu tổng hợp đa nguồn cho các chủ đề phức tạp.
- **Lớp 3 · Trình duyệt phiên thật chỉ đọc (`gstack /scrape` + `/skillify`).** Dùng cho các trang dữ liệu động hoặc cổng thông tin yêu cầu đăng nhập tài khoản của người dùng, tuân thủ nghiêm ngặt hợp đồng chỉ đọc (`read-only`) và không chạm vào mật khẩu.

### Giai đoạn 3 · Trích sự thật nguyên tử theo bản mẫu

Đọc từng nguồn đã lọc và tách thành các `Fact Cards` độc lập. Mỗi card chỉ chứa một khẳng định duy nhất, lưu kèm câu trích dẫn nguyên văn (`exact_quote`), mã băm (`content_hash`) và nhãn nhận định (`OBSERVED`, `DERIVED`, `PRIOR`, `ASSUMED`). Phân biệt rạch ròi giữa sự kiện thực tế và lời phát biểu của một cá nhân hay tổ chức.

### Giai đoạn 4 · Phát hiện trùng lặp, khử phòng vang và lập hàng đợi xung đột

So sánh ngữ nghĩa và cấu trúc giữa các thẻ.
- Các thẻ trùng nội dung và giá trị được gộp danh sách nguồn.
- Kiểm tra cột `primary_origin_url` để gom các bài báo chép lại cùng một nguồn gốc về đúng số lượng gốc độc lập (`independent_origin_count`).
- Các thẻ mâu thuẫn số liệu hoặc ngược chiều nhận định được đưa vào `conflict-queue.md` dưới dạng thẻ quyết định `Decision Brief D<N>` chờ con người phán xử.

### Giai đoạn 5 · Phát hiện lỗ hổng và lập kế hoạch thu bù

Rà soát toàn bộ tập thẻ để phát hiện các tuyên bố thiếu dữ liệu chứng minh, các chuỗi thời gian bị đứt quãng hoặc các giả định `ASSUMED` chưa được kiểm chứng. Mỗi lỗ hổng trong `gap-checklist.md` đều phải đi kèm câu lệnh truy vấn gợi ý và chế độ tìm kiếm tương ứng để vòng thu thập tiếp theo thực thi ngay.

### Giai đoạn 6 · Phân hạng tin cậy và làm giàu bốn chiều

Áp dụng quy tắc phân hạng `verified`, `probable`, `unverified` dựa trên số lượng nguồn gốc độc lập và cấp độ uy tín `authority_tier`. Bổ sung khối `enrichment` gồm liên kết chéo, phân loại, trạng thái độ tươi (`current`, `historical`, `outdated`), thứ hạng quan trọng và đánh dấu các thẻ `verified` đủ chuẩn để chuyển giao sang kho `L1` của Bộ 02.

### Giai đoạn 7 · Kiểm tra Constraint Loop và tổng hợp xuất bản

Chạy kiểm tra cơ học 4 tiêu chí hoàn thành, sau đó tổng hợp thành báo cáo 3 phần rõ ràng (Kết luận từ `verified`, Giả thuyết từ `probable`, Câu hỏi mở từ `gap-checklist`). Xuất đồng thời báo cáo cho con người đọc và thư mục `fact-cards/` cho hệ thống AI tái sử dụng.

## Cơ chế ép buộc (`Forcing Functions`)

Năm hàng rào kỹ thuật ngăn quy trình bị cắt xén.

**Một, cổng chặn Brief.** Không chạy bất kỳ lệnh tìm kiếm hay cào dữ liệu nào khi `brief.md` chưa khóa đủ 4 thành phần.

**Hai, cổng chặn Cô lập PTC và Chống Injection.** Không nạp trực tiếp dữ liệu tìm kiếm thô chưa qua lọc vào ngữ cảnh chính và luôn đặt nội dung web trong rào chắn không đáng tin.

**Ba, cổng chặn Phòng vang.** Không cấp nhãn `verified` cho một thẻ nếu các nguồn của nó thực chất chỉ chép lại cùng một `primary_origin_url` (trừ khi nguồn gốc đầu tiên đó là tài liệu chính thức hạng `tier-1`).

**Bốn, cổng chặn Hàng đợi Xung đột.** Báo cáo cuối không được phép xuất bản khi trong `conflict-queue.md` vẫn còn thẻ `D<N>` chưa được con người phê duyệt.

**Năm, cổng chặn Đối chiếu Trích dẫn.** Mọi con số, tên riêng và mã `[F-YYYY-NNN]` trong báo cáo cuối phải khớp tuyệt đối với dữ liệu trong thư mục `fact-cards/`.

## Năm bẫy phổ biến cần tránh (`Anti-patterns`)

**Bẫy 1 · Đổ thẳng kết quả tìm kiếm vào LLM và nhờ tóm tắt.** Vừa làm tràn ngữ cảnh bởi HTML rác, vừa bỏ qua toàn bộ kiểm tra phòng vang và xung đột.

**Bẫy 2 · Ảo giác đa nguồn từ hiệu ứng phòng vang.** Thấy 5 tờ báo cùng đăng một con số liền tin là đã kiểm chứng chéo, trong khi cả 5 bài đều dịch lại từ một bài blog duy nhất.

**Bẫy 3 · Trộn lẫn sự thật (`Fact`) với phát ngôn (`Statement`) và suy đoán (`Prior`).** Không gắn nhãn `claim_label` khiến người đọc nhầm kiến thức phỏng đoán của mô hình với số liệu đo đạc thực tế.

**Bẫy 4 · Để AI tự làm trọng tài xóa bỏ xung đột.** AI có xu hướng chọn nguồn viết câu chữ trau chuốt hơn thay vì nguồn có phương pháp đo lường chuẩn xác hơn.

**Bẫy 5 · Coi bài báo cáo văn xuôi là sản phẩm duy nhất.** Bỏ quên hoặc làm mất tập `Fact Cards` YAML khiến các chu kỳ nghiên cứu sau hoặc các dự án phần mềm ở Bộ 02 và Bộ 03 phải làm lại từ đầu.

## Đo lường thành công

Đánh giá chất lượng mỗi chu kỳ nghiên cứu qua năm chỉ số định lượng.

1. **Tỷ lệ sự thật đã kiểm chứng (`Verified Ratio`).** Số lượng thẻ `verified` đạt từ `40%` tổng số thẻ trở lên.
2. **Độ sạch xung đột (`Conflict Clearance`).** `100%` mục trong `conflict-queue.md` đã có phán quyết trước khi xuất báo cáo.
3. **Kiểm soát lỗ hổng (`Gap Bound`).** Số lượng lỗ hổng mức `high` còn mở trong phần 3 của báo cáo nhỏ hơn `10` mục.
4. **Độ toàn vẹn trích dẫn (`Citation Traceability`).** Kiểm tra ngẫu nhiên hoặc tự động 100% mã `[F-YYYY-NNN]` trong báo cáo đều mở ra đúng file YAML và đúng câu `exact_quote` trong nguồn gốc.
5. **Hiệu suất ngữ cảnh (`Context Efficiency`).** Dung lượng dữ liệu đưa vào ngữ cảnh suy luận được nén tối thiểu `20 lần` so với dữ liệu HTML/JSON thô lưu trên đĩa.
