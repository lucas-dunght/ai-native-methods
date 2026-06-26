# Methodology · Tinh lọc và làm giàu thông tin từ internet

## Triết lý nền

Internet là kho thông tin lớn nhưng độ tin cậy không đồng đều và độ trùng lặp rất cao. Khi đưa thông tin thô vào AI để tổng hợp, AI thường khuếch đại cả tín hiệu và nhiễu. Kết quả là một văn bản trông mạch lạc nhưng chứa lẫn lộn sự thật, ý kiến, đồn đoán và lỗi sự thật. Đối với một sinh viên hoặc nghiên cứu sinh, kết quả này có thể nguy hiểm vì khó phân biệt phần đáng tin với phần không.

Phương pháp này tiếp cận khác. Không yêu cầu AI làm thẩm phán cuối cùng cho độ tin cậy. AI chỉ làm các tác vụ deterministic và transparent. Phân loại nguồn theo nhãn rõ ràng. Trích sự thật theo bản mẫu cố định. Phát hiện trùng lặp và xung đột bằng so sánh cấu trúc. Mọi quyết định khó được surface cho người dùng phán xử.

Mục tiêu cuối không phải là một báo cáo đẹp. Là một tập sự thật có nguồn, có phân hạng tin cậy, không trùng lặp, có thể tra ngược về nguồn gốc. Báo cáo cuối là sản phẩm phụ. Tập sự thật là sản phẩm chính.

## Bốn nguyên tắc cốt lõi

### Nguyên tắc 1 · Mọi sự thật có nguồn

Không có sự thật mồ côi trong tập đầu ra. Mỗi mẩu sự thật phải gắn với ít nhất một URL hoặc một định danh nguồn truy được. Nếu một sự thật xuất phát từ nhiều nguồn cùng nói, ghi tất cả. Khi không có nguồn cụ thể, mẩu thông tin đó không phải sự thật mà chỉ là giả thuyết, ghi nhãn rõ ràng.

### Nguyên tắc 2 · Xung đột không bị AI tự xử

Khi hai nguồn nói khác nhau về cùng một sự kiện hoặc cùng một con số, AI không được tự chọn nguồn nào là đúng. AI nhiệm vụ duy nhất là làm sạch và đẩy cả hai vào hàng đợi xung đột để người quyết. Đây là ranh giới vai trò nghiêm ngặt. Chọn sai canonical fact có thể dẫn đến kết luận nghiên cứu sai và không có cách phát hiện sau này nếu AI tự xử.

### Nguyên tắc 3 · Phân hạng tin cậy ba mức

Mỗi sự thật trong tập đầu ra có một trong ba nhãn tin cậy.

Verified nghĩa là có ít nhất hai nguồn độc lập xác nhận hoặc một nguồn cấp cao có thẩm quyền ví dụ báo cáo của cơ quan chính phủ, tài liệu của tổ chức quốc tế chính thức, công bố của doanh nghiệp niêm yết.

Probable nghĩa là có một nguồn đáng tin nhưng chưa có cross-reference từ nguồn độc lập khác. Đa số sự thật từ báo chí kinh tế tier 1, blog của chuyên gia có danh tiếng, paper preprint chưa peer-reviewed.

Unverified nghĩa là nguồn có chất lượng không rõ ràng hoặc nguồn là social media, blog cá nhân, forum thảo luận. Vẫn lưu lại vì có thể có giá trị, nhưng phải được nâng cấp lên Probable hoặc Verified trước khi dùng làm cơ sở cho kết luận quan trọng.

### Nguyên tắc 4 · Làm giàu không phải tóm tắt

Tóm tắt rút gọn thông tin. Làm giàu thêm chiều thông tin mà nguồn gốc không có. Bốn dạng làm giàu trong phương pháp này.

Một, đối chiếu chéo. Mỗi sự thật được kiểm xem có mâu thuẫn hoặc bổ sung sự thật khác trong tập không.

Hai, gán phân loại. Mỗi sự thật được gán nhãn lĩnh vực, vai trò trong lập luận, mức độ quan trọng.

Ba, gắn ngữ cảnh tạm. Ngày thu thập, nguồn thu thập, query đã dùng để tìm ra nguồn này.

Bốn, đánh dấu lỗ hổng. Khi sự thật A có vẻ phụ thuộc sự thật B nhưng B không tồn tại trong tập, đánh dấu B là lỗ đặc tả cần điền sau.

## Quy trình bảy giai đoạn

Phương pháp đi qua bảy giai đoạn theo thứ tự cố định. Không skip giai đoạn nào. Có thể lặp một giai đoạn nếu cần thiết, nhưng không bỏ qua.

### Giai đoạn 1 · Định nghĩa câu hỏi và phạm vi

Trước khi thu thập, viết xuống ba thứ. Câu hỏi nghiên cứu chính cần trả lời. Phạm vi thời gian và địa lý của dữ liệu cần thu. Tiêu chí loại trừ rõ ràng cho nguồn không phù hợp.

Đầu ra giai đoạn 1 là một file nghiên cứu brief 1 đến 2 trang. Không có brief, không bắt đầu giai đoạn 2.

### Giai đoạn 2 · Thu thập có chủ đích

Thực hiện các query tìm kiếm, web scraping, gọi API. Lưu mỗi nguồn vào một source log với metadata đầy đủ. URL gốc, ngày thu, query đã dùng, độ dài, ngôn ngữ, định dạng.

Tránh thu bừa. Mỗi nguồn thu về phải có một lý do liên quan câu hỏi nghiên cứu ở giai đoạn 1. Ghi lý do thu vào source log.

Đầu ra giai đoạn 2 là source log đầy đủ và bộ nguồn thô chưa xử lý.

### Giai đoạn 3 · Trích sự thật theo bản mẫu

Đọc từng nguồn và trích các mẩu sự thật vào fact card. Mỗi fact card là một đơn vị nguyên tử của thông tin có ID duy nhất, nội dung sự thật, danh sách nguồn, vai trò trong lập luận, ngày trích.

Trích chỉ sự thật. Không trích quan điểm, suy luận, dự đoán trừ khi đó là sự thật về việc ai đó đã có quan điểm gì. Phân biệt sự thật về fact và sự thật về statement.

Đầu ra giai đoạn 3 là tập fact cards ban đầu, có thể dày tới hàng trăm hoặc nghìn cards với dự án vừa.

### Giai đoạn 4 · Phát hiện trùng lặp và xung đột

Quét tập fact cards để tìm các cards nói về cùng một sự thật. Cards nói cùng một thứ với cùng giá trị thì merge nguồn vào một card. Cards nói cùng một thứ với giá trị khác nhau thì giữ tách và đẩy vào conflict queue.

Cũng quét tìm các cards mâu thuẫn nhau dù không nói cùng một sự thật. Ví dụ một card nói thị trường tăng 20% năm 2024, một card khác nói thị trường giảm 5% năm 2024. Xung đột logic, đẩy vào conflict queue.

Đầu ra giai đoạn 4 là tập fact cards đã được deduplicate cộng với conflict queue chờ phán xử.

### Giai đoạn 5 · Phát hiện lỗ hổng

Đọc tập fact cards và tìm các điểm nghi vấn. Một sự thật được nhắc đến trong nguồn nhưng không có chi tiết cụ thể. Một quy luật được khẳng định nhưng không có evidence cụ thể. Một xu hướng được mô tả nhưng không có thời gian cụ thể.

Mỗi lỗ hổng đẩy vào gap checklist với mô tả cụ thể và hành động đề xuất. Hành động thường là thu thêm nguồn ở giai đoạn 2 cho vòng tiếp.

Đầu ra giai đoạn 5 là gap checklist.

### Giai đoạn 6 · Phán hạng tin cậy và làm giàu

Đi qua từng fact card và gán nhãn tin cậy verified, probable, hoặc unverified theo nguyên tắc 3. Cards có hai nguồn độc lập trở lên hoặc một nguồn cấp cao là verified. Cards có một nguồn đáng tin là probable. Cards còn lại là unverified.

Đồng thời làm giàu theo bốn dạng ở nguyên tắc 4. Đối chiếu chéo, gán phân loại, gắn ngữ cảnh tạm, đánh dấu lỗ hổng.

Đầu ra giai đoạn 6 là tập fact cards hoàn chỉnh có nhãn tin cậy và metadata làm giàu.

### Giai đoạn 7 · Tổng hợp và xuất

Dựa trên tập fact cards đã hoàn chỉnh, viết báo cáo tổng hợp trả lời câu hỏi nghiên cứu ở giai đoạn 1. Mọi khẳng định trong báo cáo phải tham chiếu fact card bằng ID. Không có khẳng định nào không có nguồn.

Báo cáo nên có ba phần. Phần một là tóm tắt kết luận chính dựa trên cards verified. Phần hai là các giả thuyết dựa trên cards probable cần kiểm chứng thêm. Phần ba là các câu hỏi mở từ gap checklist chưa giải quyết.

Đầu ra giai đoạn 7 là báo cáo cuối plus tập fact cards xuất ra file để tái sử dụng.

## Forcing functions

Bốn cơ chế ép để phương pháp không bị bỏ qua giai đoạn.

**Một, không bắt đầu giai đoạn 2 khi chưa có brief.** Người làm phải viết brief 1 đến 2 trang ra trước. Brief không có nghĩa là cần dùng giai đoạn 1 hoặc câu hỏi nghiên cứu chưa rõ ràng.

**Hai, không gán nhãn tin cậy bằng cảm tính.** Mỗi card có nhãn verified phải có thể trace ngược về ít nhất hai nguồn độc lập hoặc một nguồn cấp cao. Nếu không trace được, phải hạ xuống probable.

**Ba, conflict queue phải có deadline phán xử.** Cuối cycle research, mọi item trong conflict queue phải có quyết định human, không được skip. Cards xung đột chưa quyết không được dùng trong báo cáo cuối.

**Bốn, gap checklist được review ở giai đoạn 7.** Trước khi xuất báo cáo, review gap checklist. Các gap chưa giải quyết được liệt kê công khai trong phần 3 của báo cáo. Tránh che giấu lỗ hổng.

## Anti-pattern

Năm bẫy phổ biến cần tránh.

**Bẫy 1 · Paste vào AI và nhờ tóm tắt.** Cách này skip mọi gate kiểm chứng. Kết quả trông gọn nhưng không trace được nguồn, không phát hiện được xung đột, không phân hạng được tin cậy.

**Bẫy 2 · Trộn quan điểm với sự thật.** Card phải phân biệt rõ "X xảy ra" (sự thật về fact) với "Y nghĩ X" (sự thật về statement). Trộn hai loại là cách nhanh nhất tạo báo cáo sai.

**Bẫy 3 · Cho AI tự chọn canonical fact khi xung đột.** Đây là vi phạm nguyên tắc 2 ở dạng nghiêm trọng nhất. AI luôn chọn nguồn nào diễn đạt mạch lạc hơn, không phải nguồn nào chính xác hơn.

**Bẫy 4 · Bỏ qua nguồn unverified.** Cards unverified vẫn có giá trị. Chúng có thể chỉ ra xu hướng đang nổi hoặc topic chưa được nghiên cứu nhiều. Bỏ qua sớm có thể miss insight quan trọng.

**Bẫy 5 · Báo cáo cuối thay thế fact cards.** Sản phẩm chính của phương pháp là tập fact cards, không phải báo cáo. Báo cáo là sản phẩm phụ. Khi tổ chức nhận chuyển giao kết quả, nhận cả hai. Báo cáo cho con người đọc, cards cho hệ thống tái sử dụng.

## Đo lường thành công

Sau cycle nghiên cứu, đánh giá phương pháp đã work hay chưa qua bốn câu hỏi.

Tỷ lệ cards verified trên tổng số cards có lớn hơn 40% không. Nếu nhỏ hơn 30%, nguồn thu chưa đủ chất lượng, cần thu lại với nguồn cấp cao hơn.

Conflict queue có được clear hết trước khi xuất báo cáo không. Nếu còn item chưa clear, báo cáo phải declare rõ.

Gap checklist được nêu trong phần 3 báo cáo có ít hơn 10 item không. Nếu nhiều hơn, phạm vi nghiên cứu quá rộng, cần thu hẹp ở cycle sau.

Người đọc báo cáo có thể trace ngược một khẳng định bất kỳ về fact card và về nguồn gốc không. Test thử với 5 khẳng định ngẫu nhiên. Nếu không trace được, có lỗi trong quy trình.
