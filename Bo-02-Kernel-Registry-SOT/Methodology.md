# Methodology · Kernel Registry và bốn xuất xứ

## Triết lý nền

Mọi tổ chức đều có tri thức. Cách lưu trữ tri thức quyết định chất lượng quyết định và tốc độ vận hành. Nhưng đa số tổ chức rơi vào một sai lầm cơ bản. Họ cố tạo "một nguồn sự thật duy nhất" (single source of truth) như thể mọi loại tri thức đều có chế độ tin giống nhau.

Không phải vậy. Một bảng giá sản phẩm là sự thật cứng có thể verify cơ học. Một nghĩa vụ pháp lý là sự thật được rút từ văn bản pháp quy có authority cụ thể. Voice CEO là phán xét tự do không thể verify bằng máy. Trộn cả ba vào một sổ cái là tạo ảo giác rằng voice CEO kiểm được như bảng giá.

Phương pháp này phân lập tri thức theo bốn xuất xứ. Mỗi xuất xứ có chế độ tin khác nhau và lưu trong kho khác nhau. Skills (gói hướng dẫn quy trình) không có sách luật riêng. Skills chỉ chứa pointer tới registry và obligations, không lặp nội dung.

Mục tiêu cuối là một hệ thống tri thức mà AI agent và con người cùng truy cập, không bị nhầm lẫn giữa các loại sự thật và có thể truy ngược về nguồn gốc mỗi quyết định.

## Bốn xuất xứ

### L1 · Sự thật lưu sẵn

Giá sản phẩm, từng dòng ma trận năng lực, định mức, part number, điều khoản hợp đồng cứng. Đây là sự thật có thể đo được hoặc deterministic. Verify bằng cách nhìn vào nguồn gốc. Lưu dưới dạng key-value có kiểu, có ID, có nguồn, có ngày cập nhật.

Ở registry, L1 được transclude bằng ID. Không bao giờ để model viết lại như văn. Khi cần dùng giá sản phẩm X trong báo cáo, reference ID L1-product-X-price, không paste giá trị.

### L2 · Sự thật dẫn xuất

Tổng dự toán, doanh thu kế hoạch, các đại lượng tính từ L1 bằng công thức cố định. L2 không lưu giá trị mà lưu công thức cộng nguồn input. Khi L1 thay đổi, L2 tự cập nhật theo công thức.

L2 cũng thuộc registry như L1 nhưng đánh dấu là derived. Lý do tách. Khi L1 sai, biết ngay L2 phụ thuộc sai theo. Khi audit, có thể trace từ L2 ngược về L1 input.

### L3 · Sinh có ràng buộc

Không phải con số. Là nghĩa vụ rút từ văn bản pháp quy. Mỗi nghị định, thông tư, khung tiêu chuẩn quốc tế, được trích thành các nghĩa vụ có ID. Mỗi nghĩa vụ có nguồn cụ thể trong văn bản gốc.

Ví dụ một nghị định về bảo vệ dữ liệu cá nhân có thể được trích ra 30 nghĩa vụ rõ ràng. Mỗi nghĩa vụ có ID, mô tả ngắn, link tới điều khoản gốc trong nghị định, ngày hiệu lực.

L3 lưu trong kho riêng gọi là obligations book, không trộn với registry L1 và L2.

### L4 · Phán xét tự do

Voice CEO, phong cách công ty, tinh thần văn bản, taste của leadership. Cái này đứng NGOÀI đường kiểm. Nó là input để sinh, không phải thứ đối chiếu cơ học.

L4 lưu trong kho riêng gọi là style book, tách riêng hoàn toàn. Lý do tách. Style cạnh bảng giá tạo ảo giác rằng voice CEO kiểm được như giá. Sai và nguy hiểm.

## Ba kho, không một SOT

Tương ứng với bốn xuất xứ, có ba kho lưu trữ với ba chế độ tin khác nhau.

### Kho registry

Cho L1 và L2. Khóa, giá trị có kiểu, ID, cột nguồn, ngày cập nhật, ngày hết hiệu lực. Chế độ tin "verify cơ học". Có thể test programmatically.

### Kho obligations

Cho L3. Mỗi nguồn (nghị định, thông tư, khung tiêu chuẩn) một sổ riêng. Mỗi nghĩa vụ một ID và một cột ghi nó rút từ điều khoản nào. Chế độ tin "trace về văn bản gốc".

### Kho style

Cho L4. Đứng ngoài đường kiểm. Chế độ tin "input để sinh, không verify". Lưu dạng tài liệu prose, có thể có version history nhưng không có công thức verify.

## Skills là gói nội dung, không phải kho riêng

Một skill (gói hướng dẫn cho AI agent thực hiện một loại công việc cụ thể) thường chứa ngầm các nghĩa vụ và quy tắc. Vấn đề. Khi skill viết các nghĩa vụ này dạng prose lặp lại nội dung từ kho obligations, khi obligations thay đổi, skill không tự cập nhật.

Giải pháp. Với mỗi skill, làm hai việc.

Một, đọc skill và trích các nghĩa vụ ẩn bên trong, gán ID, đưa vào kho obligations.

Hai, để skill trỏ tới các ID nghĩa vụ đó thay vì lặp lại nội dung. Skill không có sách luật riêng. Nó chỉ là danh sách con trỏ tới registry và obligations, cộng phần hướng dẫn quy trình thực hiện.

Hệ quả. Khi nghĩa vụ thay đổi trong obligations, mọi skill trỏ tới nó tự nhiên cập nhật theo. Không có drift.

## Dependency thread

Quan hệ giữa các thành phần (nguồn, nghĩa vụ, skill, tài liệu) cần track lại để có thể lần ngược khi cần thiết.

Một dependency index dạng bảng đơn giản đủ cho mục đích này. Nguồn nào sinh ra nghĩa vụ nào, nghĩa vụ nào treo vào tài liệu nào hoặc skill nào.

Khi một thông tư thay đổi, không cần quét toàn bộ tổ chức. Chỉ tra dependency index để biết các nhánh treo vào thông tư đó và rà lại từng nhánh.

Không cần graph database phức tạp. Một bảng CSV grep được là đủ cho bước này.

## Quy trình năm phase

Phương pháp đi qua năm phase theo thứ tự. Dừng lại xin duyệt giữa phase 4 và 5. Làm theo lô nhỏ, báo cáo từng bước, không cố xử lý tất cả trong một lượt.

### Phase 1 · Kiểm kê

Duyệt mọi thư mục được cấp. Lập manifest liệt kê mọi file gồm đường dẫn, loại, nội dung có vẻ là gì, ngày sửa cuối, lĩnh vực có vẻ thuộc về. Chưa di chuyển gì hết. Chỉ đọc và ghi.

Output. Manifest đầy đủ.

### Phase 2 · Phân loại

Gán mỗi file (và nơi cần thì mỗi phần trong file), về L1 L2 L3 hay L4 và về kho tương ứng. Xuất bảng phân loại. File nào không chắc thì đánh dấu, không đoán.

Output. Bảng phân loại theo xuất xứ.

### Phase 3 · Phát hiện xung đột và lỗ hổng

Đây là phase có giá trị nhất. Tìm và nêu ra, không tự sửa. Các bản trùng và mâu thuẫn của cùng một sự thật. Hai giá cho một SKU, master và sanitized. Các tham chiếu đã hết hiệu lực. Các sự thật được nhắc tới trong tài liệu nhưng không tồn tại trong bất kỳ file nguồn nào. Các skill có nghĩa vụ chồng lấn nhau. Tất cả đẩy vào hàng đợi quyết định cho user.

Output. Hàng đợi xung đột và lỗ hổng.

### Phase 4 · Đề xuất cấu trúc đích và bản đồ di trú

Đề xuất cây thư mục mới theo ba kho cộng skills cộng dependency index cộng hai hàng đợi cho human. Kèm bản đồ từ file cũ sang file mới cho mỗi file.

Dừng lại ở đây. Chờ user duyệt trước khi đụng vào cấu trúc.

Output. Đề xuất cấu trúc đích và migration map.

### Phase 5 · Thực thi sau khi duyệt

Chỉ sau khi user đồng ý. Dựng cấu trúc mới bằng cách SAO CHÉP, để nguyên bản gốc tại chỗ hoặc trong một thư mục archive. Gán ID cho phần có cấu trúc. Sinh dependency index. Xuất completion report ghi rõ đã làm gì, còn gì trong hàng đợi chờ user.

Output. Cấu trúc kernel registry đã được dựng cộng completion report.

## Ranh giới vai trò

Phần quan trọng nhất của phương pháp. Đọc kỹ.

Agent thi công. Làm phần kiểm kê, phân loại sơ bộ, phát hiện trùng lặp và xung đột, đề xuất cấu trúc và sau khi user duyệt thì dựng cấu trúc bằng cách sao chép.

Agent KHÔNG được tự quyết khi hai file đụng nhau. Hai bảng giá khác nhau cho cùng một SKU, một bản master và một bản sanitized, một BOM cũ và một BOM mới. Agent không chọn cái nào đúng. Agent nêu cả hai vào hàng đợi cho user phán xử. Chọn sai cái canonical là lỗi chết người. Đó là phán xét của người ký, không phải của agent.

Khi không chắc một file thuộc xuất xứ nào, đừng đoán. Đẩy nó vào hàng đợi chưa phân loại.

## Forcing functions

Năm cơ chế ép để phương pháp không thoái hoá.

**Không xoá file.** Không ghi đè file. Không di chuyển phá vỡ bản gốc. Chỉ sao chép cho tới khi user duyệt.

**Không tự chọn canonical** khi có xung đột sự thật. Nêu ra, để user quyết.

**Không atomize mọi thứ.** Chỉ cấu trúc hoá phần vừa lặp nhiều, vừa deterministic, vừa đắt khi sai. Tài liệu chạm một lần rồi thôi thì để nguyên, đừng phí công.

**Không dựng graph database** hay máy móc nặng. Một bảng dependency index là đủ.

**Không gộp style vào registry.** L4 đứng riêng tuyệt đối.

## Anti-pattern

Sáu bẫy thường gặp.

**Bẫy 1 · Một SOT duy nhất.** Mọi tri thức bị nhồi vào một database hoặc một wiki. Khi truy vấn, không phân biệt được loại sự thật, dẫn đến quyết định sai.

**Bẫy 2 · Atomize mọi tài liệu.** Mỗi tài liệu phải nhỏ nhất có thể, từng câu thành một entry. Hệ quả. Overhead lớn, không ai duy trì nổi, registry chết sau 3 tháng.

**Bẫy 3 · Agent tự quyết canonical.** Cho AI chọn nguồn nào đúng khi conflict. Trông tiện nhưng AI luôn chọn nguồn nào diễn đạt mạch lạc hơn, không phải nguồn nào chính xác.

**Bẫy 4 · Trộn style vào registry.** Voice của CEO lưu chung bảng giá. Tạo ảo giác voice verify được như giá. Nguy hiểm vì khi quyết định dựa trên voice, không biết voice đã được "verify" hay chỉ là một entry trong DB.

**Bẫy 5 · Build graph database trước.** Quá phức tạp cho bước khởi đầu. Bắt đầu bằng CSV. Khi scale lên đáng kể (hàng ngàn entities), mới cân nhắc graph DB.

**Bẫy 6 · Skip phase 3.** Bỏ qua phát hiện xung đột, đi thẳng vào dựng cấu trúc. Hệ quả. Cấu trúc mới chứa nguyên các xung đột chưa giải quyết. Registry không đáng tin từ ngày đầu.

## Selectivity · nước đi đầu

Đừng đề xuất dựng lại tất cả cùng lúc. Kiểm kê thì làm trên toàn bộ. Nhưng phần restructure ở phase 4 ưu tiên cụm giá trị cao nhất trước.

Cụm giá trị cao nhất thường là registry cho nhóm con số gồm giá, BOM, ma trận năng lực, part number. Đây là phần được tra cứu nhiều, deterministic và đắt khi sai. Chứng minh cụm này gọn gàng và truy được trước.

Các cụm còn lại làm thành các lô sau. Mỗi lô là thêm một gói lên cấu trúc đã chạy. Tránh big bang restructure.

## Điểm dừng

Bốn tình huống agent phải ngừng và hỏi user.

Bất kỳ thao tác có thể phá dữ liệu.

Bất kỳ xung đột sự thật cần phán xử.

Khi tỷ lệ file không phân loại được vượt mức agent thấy đáng ngờ.

Khi phạm vi thư mục không rõ.

Trong mọi trường hợp nghi ngờ, nghiêng về dừng và hỏi, không nghiêng về tự xử.

## Đo lường thành công

Sau khi triển khai kernel registry, đánh giá qua bốn câu hỏi.

Tỷ lệ truy vấn từ AI agent về registry trả về đúng giá trị có lớn hơn 95% không.

Khi một sự thật L1 thay đổi, có dễ trace ngược tất cả các tài liệu, skill, báo cáo phụ thuộc nó qua dependency index không.

Conflict queue có được clear định kỳ không hay tích đọng không xử lý.

Skill có lặp nội dung từ registry hay chỉ chứa pointer ID.

Nếu bốn câu trên đều positive, kernel registry đang hoạt động đúng. Nếu một trong bốn negative, có vấn đề trong cài đặt hoặc bảo trì.
