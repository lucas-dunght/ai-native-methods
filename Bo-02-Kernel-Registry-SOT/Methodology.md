# Methodology · Kernel Registry và Bốn Xuất Xứ Tri Thức (v2.0 · 2026.10)

## Triết lý nền

Mọi tổ chức và dự án đều vận hành dựa trên tri thức. Tuy nhiên, sai lầm phổ biến nhất khi triển khai hệ thống tri thức cho AI Agent là cố gắng gom tất cả tài liệu vào "một nguồn sự thật duy nhất" (một cơ sở dữ liệu Vector chung hoặc một trang Wiki duy nhất) như thể mọi loại thông tin đều có cùng một bản chất kiểm chứng.

Trong thực tế, tri thức tổ chức có bốn bản chất hoàn toàn khác nhau.
- Một bảng giá bán lẻ hoặc định mức vật tư là **sự thật lưu sẵn (`L1`)** có thể đối chiếu cơ học từng con số với tài liệu gốc.
- Một bảng tổng dự toán hoặc biên lợi nhuận gộp là **sự thật dẫn xuất (`L2`)** bắt buộc phải tính bằng công thức toán học từ `L1`, không bao giờ được lưu chết một con số rời rạc.
- Một quy định bảo vệ dữ liệu cá nhân là **nghĩa vụ có ràng buộc (`L3`)** rút ra từ văn bản pháp luật có hiệu lực và phạm vi áp dụng cụ thể.
- Phong cách viết thư của nhà sáng lập hoặc gu thiết kế giao diện là **phán xét tự do (`L4`)** dùng để truyền cảm hứng sáng tạo, hoàn toàn nằm ngoài đường kiểm đúng sai cơ học.

Trộn lẫn cả bốn loại này vào chung một kho lưu trữ sẽ tạo ra hai hậu quả nghiêm trọng. Một là AI Agent dùng giọng văn quảng cáo (`L4`) để tự suy diễn lại bảng giá (`L1`) hoặc tự nhẩm tính sai tổng dự toán (`L2`). Hai là khi một thông tư pháp lý (`L3`) hoặc một đơn giá gốc (`L1`) thay đổi, tổ chức không có cách nào biết được những báo cáo, công thức hay kỹ năng AI (`Skills`) nào đang bị lệch chuẩn (`STALE`).

Phương pháp **Kernel Registry v2.0** giải quyết tận gốc bài toán này bằng cách phân lập tri thức theo bốn xuất xứ vào ba kho chuyên biệt, gắn mã băm kiểm chứng độ tươi (`SHA-256 Content-Hash`), dùng script tính toán tất định cho `L2`, quản lý dây chuyền phụ thuộc qua bảng chỉ mục phân tầng và bảo vệ dữ liệu gốc bằng kỷ luật sao chép khóa phạm vi (`Copy-Only Scope Freeze`).

## Bốn xuất xứ và Chế độ tin cậy (v2.0)

### L1 · Sự thật lưu sẵn (`Stored Facts`)

Bao gồm bảng giá sản phẩm, từng dòng định mức nguyên vật liệu (`BOM`), mã linh kiện, ma trận năng lực kỹ thuật, điều khoản hợp đồng định lượng, hoặc các `Fact Cards` đã đạt hạng `verified` chuyển giao sang từ **Bộ 01**.

Chế độ tin cậy của `L1` là **đối chiếu cơ học kèm kiểm toán độ tươi**.
- Mỗi mục `L1` được lưu dưới dạng tệp YAML có định danh duy nhất (`fact_id`), kiểu dữ liệu rõ ràng, đường dẫn tới tài liệu gốc kèm vị trí trang/ô (`page`, `cell`), mã băm `source_hash` của tài liệu gốc và ngày hết hạn `date_expires`.
- Khi cần dùng số liệu `L1` trong báo cáo hoặc trong `Skill`, hệ thống nhúng qua mã định danh con trỏ (ví dụ `L1-product-X-price-2026-Q4`), tuyệt đối không để mô hình ngôn ngữ tự gõ lại con số bằng trí nhớ.

### L2 · Sự thật dẫn xuất (`Derived Facts`)

Bao gồm tổng dự toán chi phí, doanh thu kế hoạch quý, tỷ suất lợi nhuận, các chỉ số tổng hợp được tính từ một hoặc nhiều mục `L1`.

Chế độ tin cậy của `L2` là **tính toán tất định bằng mã thực thi (`Deterministic Evaluation`)**.
- Tệp YAML của `L2` không lưu một con số tĩnh mà lưu cấu trúc công thức (`formula`), danh sách các mã đầu vào `L1` (`inputs`), câu lệnh tính toán tất định (`deterministic_eval_cmd`) và dấu vết kiểm toán (`audit_trace`) ghi nhận mã băm của các đầu vào lúc chạy phép tính.
- Khi bất kỳ mục `L1` đầu vào nào thay đổi giá trị hoặc chuyển sang trạng thái `STALE`, mục `L2` phụ thuộc tự động được đánh dấu `STALE` và phải chạy lại lệnh tính toán. AI Agent tuyệt đối không được tự tính nhẩm giá trị `L2` trong đầu.

### L3 · Sinh có ràng buộc (`Constrained Obligations`)

Bao gồm các nghĩa vụ pháp lý, quy định tuân thủ và quy tắc vận hành rút từ nghị định, thông tư, tiêu chuẩn ngành (ISO, SOC2, PCI-DSS) hoặc điều lệ chính thức của tổ chức.

Chế độ tin cậy của `L3` là **truy vết điều khoản gốc và kiểm tra hiệu lực**.
- Mỗi văn bản pháp quy có một thư mục riêng trong kho `obligations/`, lưu kèm tệp văn bản gốc (PDF/Markdown), mã băm `source_hash` và tệp `obligations.yaml`.
- Mỗi nghĩa vụ có mã định danh `OBL-<source_id>-NNN`, trích dẫn chính xác điều khoản gốc (`article`), mức độ nghiêm trọng (`severity`) và loại kiểm tra tuân thủ (`compliance_check_type`).
- Khi văn bản pháp quy được sửa đổi hoặc thay thế, nghĩa vụ cũ được chuyển sang trạng thái `deprecated` kèm con trỏ `superseded_by` trỏ sang nghĩa vụ mới, tuyệt đối không xóa lịch sử.

### L4 · Phán xét tự do (`Free Judgment & Style`)

Bao gồm giọng điệu thương hiệu (`Brand Voice`), phong cách lãnh đạo (`Voice CEO`), từ vựng ưa thích hoặc cấm kỵ, nguyên tắc thẩm mỹ thiết kế.

Chế độ tin cậy của `L4` là **đầu vào định hướng sáng tạo, đứng ngoài đường kiểm cơ học**.
- `L4` được lưu hoàn toàn tách biệt trong kho `style/` dưới dạng các tài liệu Markdown có cấu trúc kèm một tệp hồ sơ định danh `L4-style.yaml`.
- Tách riêng `L4` giúp ngăn chặn ảo giác nguy hiểm rằng nhận định phong cách cá nhân cũng là sự thật cứng giống như bảng giá hay quy định pháp luật.

## Ba kho lưu trữ, Con trỏ Skill và Chỉ mục phụ thuộc phân tầng

### 1. Ba kho độc lập (`Registry`, `Obligations`, `Style`)

- **Kho `registry/`** chứa `stored-facts/` (`L1`) và `derived-facts/` (`L2`). Mọi mục trong kho này đều phải kiểm tra được bằng script.
- **Kho `obligations/`** chứa các nghĩa vụ `L3` gắn chặt với văn bản pháp quy gốc.
- **Kho `style/`** chứa các tài liệu phong cách `L4`.

### 2. Skills là gói quy trình chứa con trỏ, không chứa sách luật riêng

Khi viết một `Skill` cho AI Agent (ví dụ kỹ năng lập báo cáo tài chính, kỹ năng soạn hợp đồng, hoặc các gói `TIP` trong **Bộ 03 Vibecode Kit v6.1**), nếu người viết chép trực tiếp các con số đơn giá hoặc nội dung điều khoản pháp lý vào trong tệp `SKILL.md`, tệp `SKILL.md` đó sẽ lập tức bị lỗi thời ngay khi bảng giá hoặc thông tư thay đổi.

Giải pháp chuẩn của Bộ 02.
1. Tách toàn bộ số liệu cứng đưa vào `registry/` (`L1`, `L2`) và tách toàn bộ quy tắc bắt buộc đưa vào `obligations/` (`L3`).
2. Trong `SKILL.md` chỉ lưu quy trình thực hiện cùng danh sách **con trỏ định danh (`Pointer IDs`)** trỏ tới các mục `L1`, `L2`, `L3` và đường dẫn `style/`.

### 3. Chỉ mục phụ thuộc phân tầng (`Tiered Dependency Indexing`)

Để trả lời tức thì câu hỏi *"Khi thông tư X hoặc đơn giá Y thay đổi thì những công thức, báo cáo và Skill nào bị ảnh hưởng?"*, Bộ 02 v2.0 áp dụng kiến trúc chỉ mục hai tầng.

- **Tầng 1 · Bảng `dependency-index.csv` (Mặc định bắt buộc cho mọi dự án dưới 500 thành phần).** Một tệp CSV văn bản thuần ghi rõ cặp quan hệ `from_id -> to_id` kèm nhãn xuất xứ quan hệ (`provenance_tag: EXTRACTED | INFERRED | AMBIGUOUS`). Đơn giản, minh bạch, quản lý phiên bản qua Git và tra cứu trong vài mili-giây bằng `ripgrep` hoặc script Python.
- **Tầng 2 · Đồ thị `ak-graphify` và Bộ nhớ `gstack /sync-gbrain` (Mở rộng khi kho vượt 500 thành phần hoặc kết hợp mã nguồn đa ngôn ngữ).** Khi dự án lớn dần, sử dụng `ak-graphify` để tự động bóc tách cây cú pháp (`AST`) và tài liệu thành đồ thị truy vấn MCP (`query_graph`, `shortest_path`), kết hợp với `/sync-gbrain` để đồng bộ chỉ mục có kiểm soát chính sách tin cậy (`brain_trust_policy: personal | shared | deny`) và kiểm toán chống rò rỉ dữ liệu nhạy cảm (`--audit`).

## Quy trình năm Phase nâng cấp (v2.0)

```
Phase 1: Kiểm kê & Chụp mã băm gốc (ORIGINAL_TREE_FINGERPRINT)
     ↓
Phase 2: Phân loại L1/L2/L3/L4 & Phân tầng Quyết định (Mechanical / Taste / User Challenge)
     ↓
Phase 3: Phát hiện Xung đột, Lỗ hổng & Kiểm toán Độ tươi (Thẻ Decision Brief D<N>)
     ↓
Phase 4: Đề xuất Cấu trúc Đích (Selectivity) & Bản đồ Di trú ──► [Cổng Duyệt Con Người]
     ↓
Phase 5: Thực thi Sao chép Khóa Phạm vi (Copy-Only Scope Freeze) + Tính L2 + Nghiệm thu
```

### Phase 1 · Kiểm kê và Chụp dấu vân tay gốc

Duyệt toàn bộ thư mục nguồn ở chế độ chỉ đọc. Lập bảng kiểm kê `manifest.csv` ghi nhận đường dẫn, loại tệp, lĩnh vực và mã băm `source_hash` (`SHA-256`) của từng tệp. Tính mã băm tổng `ORIGINAL_TREE_FINGERPRINT` của cả cây thư mục gốc để làm mốc đối chiếu an toàn ở cuối quy trình.

### Phase 2 · Phân loại bốn xuất xứ và Lọc quyết định 3 tầng

Gán từng tệp (hoặc từng phần trong tệp hỗn hợp) về `L1`, `L2`, `L3`, `L4`. Các trường hợp rõ ràng (`Mechanical`) được Agent xử lý tự động. Các trường hợp đánh đổi cách chia nhỏ (`Taste`) được gắn nhãn khuyến nghị theo nguyên tắc chọn lọc (`Selectivity`). Các tệp mơ hồ hoặc pha trộn nhiều xuất xứ (`User Challenge`) được đưa vào `queues/unclassified-queue.md` kèm thẻ `Decision Brief D<N>`.

### Phase 3 · Phát hiện xung đột, lỗ hổng và kiểm toán độ tươi

Quét toàn bộ kho tài liệu để tìm các con số mâu thuẫn nhau giữa các phòng ban, các công thức `L2` thiếu đầu vào `L1`, các văn bản đã quá hạn hiệu lực (`EXPIRED`) và các `Skill` đang chép lặp lại nội dung quy chế. Đóng gói toàn bộ xung đột thành các thẻ `Decision Brief D<N>` trong `queues/conflict-queue.md`.

### Phase 4 · Đề xuất cấu trúc đích theo nguyên tắc Selectivity và Bản đồ di trú

Không đập đi xây lại toàn bộ tài liệu cùng một lúc (`Anti-Big-Bang`). Ưu tiên thiết lập kho `registry/` cho cụm dữ liệu có tần suất tra cứu cao nhất và chi phí sai sót đắt nhất trước. Trình bày cây thư mục đích và bảng ánh xạ di trú (`Migration Map`) từ tệp gốc sang tệp đích, sau đó **dừng lại chờ con người ký duyệt**.

### Phase 5 · Thực thi sao chép khóa phạm vi, tính `L2` và nghiệm thu

Sau khi được duyệt, Agent dựng cấu trúc `kernel-registry/` hoàn toàn bằng thao tác **sao chép**, chạy script tính toán cho các mục `L2`, sinh `dependency-index.csv`, kiểm tra lại `ORIGINAL_TREE_FINGERPRINT` để chứng minh thư mục gốc còn nguyên vẹn 100% và xuất báo cáo nghiệm thu (`Completion Report`).

## Sáu bẫy phổ biến cần tránh (`Anti-patterns`)

**Bẫy 1 · Một sổ cái duy nhất cho mọi loại tri thức.** Nhồi chung bảng giá, quy chế pháp lý và văn phong CEO vào một kho khiến AI Agent không phân biệt được đâu là quy tắc bắt buộc và đâu là lời văn tham khảo.

**Bẫy 2 · Nguyên tử hóa máy móc mọi tài liệu.** Cắt vụn cả những biên bản họp chỉ đọc một lần thành hàng trăm tệp YAML nhỏ lẻ làm chi phí bảo trì phình to và khiến hệ thống nhanh chóng bị bỏ hoang.

**Bẫy 3 · Để AI tự chọn sự thật chuẩn và tự nhẩm tính `L2`.** AI chọn nhầm bảng giá cũ hoặc cộng nhầm tổng dự toán mà không để lại dấu vết công thức.

**Bẫy 4 · Di chuyển hoặc sửa trực tiếp làm hỏng thư mục tài liệu gốc.** Vi phạm kỷ luật `Copy-Only Scope Freeze` gây mất mát dữ liệu lịch sử của tổ chức.

**Bẫy 5 · Chép lặp lại quy định vào từng `Skill`.** Không dùng con trỏ `Pointer ID` khiến mỗi lần thay đổi thông tư hay bảng giá phải đi sửa thủ công hàng chục tệp `SKILL.md`.

**Bẫy 6 · Dựng cơ sở dữ liệu đồ thị nặng nề ngay từ ngày đầu.** Bỏ qua bước chuẩn hóa `dependency-index.csv` và kiểm toán xung đột ở Phase 3 khiến đồ thị chứa toàn dữ liệu rác.

## Đo lường thành công

Một hệ thống `Kernel Registry v2.0` đạt chuẩn khi thỏa mãn năm chỉ số kiểm chứng cơ học.

1. **Độ chính xác truy vấn (`Query Accuracy`).** Tỷ lệ AI Agent truy xuất đúng giá trị `L1/L2` và điều khoản `L3` qua con trỏ đạt từ `95%` trở lên.
2. **Bảo toàn bản gốc (`Zero Source Mutation`).** Mã băm `ORIGINAL_TREE_FINGERPRINT` của thư mục tài liệu gốc trước và sau Phase 5 khớp nhau `100%`.
3. **Độ toàn vẹn dây chuyền phụ thuộc (`Dependency Integrity`).** `100%` liên kết trong `dependency-index.csv` và con trỏ trong `skills/` đều trỏ tới các `component_id` hợp lệ và có trạng thái độ tươi rõ ràng (`FRESH / STALE / EXPIRED`).
4. **Tính tất định của `L2` (`Deterministic L2`).** `100%` mục `L2` có câu lệnh tính toán chạy ra kết quả khớp với `audit_trace`.
5. **Kỷ luật làm sạch hàng đợi (`Queue Hygiene`).** Mọi xung đột trọng yếu trong `conflict-queue.md` đều có phán quyết của con người trước khi đưa mục dữ liệu đó vào trạng thái `active`.
