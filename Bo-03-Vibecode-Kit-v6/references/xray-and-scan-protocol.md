# Giao Thức Quét X-Ray, `Indirect Prompting`, Bộ Tứ `/teach` & Khử Mơ Hồ (`SCAN & RRI Protocol`)

> **Bước 1 & Bước 2 của Vibecode Kit v6.2 (`× pstack`) · Đọc trước khi hỏi · Hiểu cả Runtime (`/how`) lẫn Lịch sử (`/why`) trước khi thiết kế**

---

## 1. Quy Tắc Đọc Bộ Nhớ Tính Năng & Quét X-Ray (`Step 1A · Feature Map & Fast Scan`)

Khi nhận yêu cầu từ Chủ nhà, Chủ thầu **tuyệt đối không hỏi ngược ngay những thông tin đã có sẵn trong kho mã nguồn** và **không mò mẫm mù quáng làm tràn vùng nhớ ngữ cảnh (`context window`)**. Bắt buộc thực hiện tuần tự:

1. **Tra cứu Bộ nhớ Vật chất hóa (`Feature Map`):**
   - Đọc ngay tệp `references/features/README.md` (nếu dự án đã có) để xác định tính năng đang nằm ở đâu, tệp nguồn nào chịu trách nhiệm, đường dẫn URL/API nào liên quan và câu lệnh `./bin/control-app` nào dùng để chạm tới màn hình đó.
2. **Quét Cấu trúc & Cấu hình Cốt lõi (`Structure & Config Scan`):**
   - Kiểm tra tệp cấu hình dự án (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `CLAUDE.md`, `README.md`) để xác định ngôn ngữ, framework, trình chạy test và quy ước hiện hành.
3. **Định vị Điểm Chạm Chính xác (`Exact File & Symbol Locator`):**
   - Dùng công cụ tìm kiếm tệp và tìm kiếm nội dung (`grep`) để xác định chính xác danh sách tệp, hàm, lớp và kiểu dữ liệu liên quan kèm số dòng (`file:line`).

---

## 2. Kỹ Thuật `Indirect Prompting` (*"Restate in your own words"*) (`Step 1B`)

Dù rất thông minh, các mô hình hiện đại (Frontier Models) vẫn thất bại vì hai điểm mù lớn:
1. **Đầu bài mơ hồ (`Under-specified intent`):** Người dùng chỉ mô tả triệu chứng bề nổi hoặc dùng từ ngữ đa nghĩa.
2. **Thiếu ngữ cảnh lịch sử/hệ thống (`Missing context`):** Người dùng áp đặt ngay giả thuyết sửa lỗi chủ quan của mình trong câu lệnh, dẫn Agent đi lệch hướng theo định kiến sai.

### Quy trình `Indirect Prompting Restate` Bắt buộc:
- Thay vì nhảy vào viết code hoặc hùa theo giả thuyết ban đầu của người dùng, Chủ thầu phải đọc toàn bộ nguồn thông tin nhiễu (thread báo lỗi Slack, log hệ thống, mô tả yêu cầu thô) và viết một mục riêng mang tên **`Indirect Prompting Restate`**:
  > *"Diễn đạt lại bản chất bài toán bằng lời của chính bạn và bằng ngôn ngữ tự nhiên dễ hiểu (`restate in your own words and in plain English`)."*
- Bản diễn đạt lại này phải trả lời 3 ý trong tối đa 5 dòng:
  1. **Hiện trạng đang chạy (`What is happening now`):** Hệ thống thực tế đang xử lý luồng dữ liệu như thế nào (`[OBSERVED: file:line]`).
  2. **Điểm gãy / Nhu cầu thật (`What is the real gap`):** Bản chất vấn đề người dùng đang gặp phải là gì (tách khỏi giải pháp gợi ý ban đầu).
  3. **Ranh giới không được phá vỡ (`What must stay intact`):** Các luồng hoặc hợp đồng API nào phải được bảo toàn.
- Việc ép Agent nén thông tin nhiễu thành bài toán có cấu trúc bằng lời tự nhiên giúp Chủ nhà bắt lỗi hiểu sai ngay từ Bước 1 trước khi một dòng code nào được viết ra.

---

## 3. Xây Dựng Mental Model Hai Chiều Bằng Bộ Tứ `/teach = /how + /why + /recall` (`Step 1C`)

Một dòng code trong kho lưu trữ chỉ cho biết **cái gì đang chạy**, hoàn toàn không cho biết **tại sao nó lại được viết như vậy**. Để tránh việc đập nhầm một chốt chặn an toàn lịch sử, Chủ thầu thực thi tổ hợp 4 lệnh nhận thức:

| Lệnh con | Mục tiêu nhận thức | Nguồn truy vấn & Hành động cơ học |
|---|---|---|
| **`/how`** | Truy vết cơ chế hoạt động hiện tại ở tầng `Runtime`. | Lần theo luồng gọi hàm từ điểm vào (`Entrypoint -> Service -> DB/External API`). Tự động phân luồng (`fan-out`) các explorer agents chạy song song nếu tính năng trải rộng trên nhiều thư mục hoặc microservice. |
| **`/why`** | Truy tìm nguyên nhân lịch sử và ý đồ thiết kế ban đầu. | Truy vấn song song `git log -S "<symbol>" -p`, `git blame`, bình luận trên PR cũ (`PR comments`), mã ticket/issue, tài liệu thiết kế (`ADR / docs`) và log sự cố cũ để hiểu các ràng buộc ẩn. |
| **`/teach`** | Kiểm chứng mô hình nhận thức và chặn ảo giác (`Anti-Hallucination`). | Yêu cầu Agent giải thích trực quan (bằng sơ đồ ASCII và dẫn chứng `file:line` thực tế) cho Chủ nhà hiểu cơ chế hiện tại và **chứng minh vì sao phương án mới tốt hơn hiện trạng**. Việc bắt Agent "dạy lại" cho mình chính là cơ chế ép Agent phải đọc code thật thay vì phán tự tin nhưng rỗng (`confidently hallucinating`). |
| **`/recall`** | Khôi phục ngữ cảnh liên phiên làm việc. | Rút trích ngữ cảnh từ lịch sử hội thoại hoặc các phiên làm việc trước (`transcripts / handoff contracts`) thành một bản tóm tắt trạng thái hiện tại gọn sạch để nạp vào phiên mới mà không phải mò lại từ đầu. |

---

## 4. Phỏng Vấn Khử Mơ Hồ & Bảng Quyết Định `D<N>` (`Step 2 · RRI Gate`)

Sau khi đã có bản `Indirect Prompting Restate` và kết quả `/teach`, nếu điểm rõ ràng yêu cầu (`Requirement Readiness Index · RRI`) chưa đạt `8.5/10`, Chủ thầu tiến hành hỏi Chủ nhà theo quy tắc:

1. **Giới hạn Tối đa 3 Câu hỏi Trắc nghiệm:** Không hỏi câu hỏi mở lan man; mỗi câu hỏi phải có từ 2 đến 3 phương án rõ ràng và đặt phương án khuyến nghị lên đầu kèm tiền tố `(Recommended)`.
2. **Định dạng Bảng Quyết định `D<N>` (`Decision Brief Format`):**
   - **`ELI10` (Giải thích cho trẻ 10 tuổi):** Nêu bản chất quyết định bằng ngôn ngữ đời thường, không dùng từ lóng kỹ thuật để che giấu sự phức tạp.
   - **`Completeness Score (X/10)`:** Chấm điểm độ trọn vẹn của từng phương án trên thang 10.
   - **Nguyên tắc *"Boil the Lake"*:** Trong thời đại AI viết code với chi phí biên tiệm cận 0, nếu Phương án A đạt độ hoàn thiện `10/10` chỉ tốn thêm của AI vài phút so với Phương án B (`7/10` nhưng để lại nợ kỹ thuật), **luôn khuyến nghị Phương án A**.
   - **Phân loại Nợ Đường tắt (`Shortcut Debt Classification`):** Mọi phương án cắt giảm phạm vi phải ghi rõ loại nợ phát sinh:
     - `Type-1 (Accidental Complexity)`: Nợ làm bẩn kiến trúc, cần tránh tuyệt đối.
     - `Type-2 (Deferred Edge Case)`: Trường hợp biên hiếm gặp được hoãn có chủ đích và ghi vào `TODOS.md`.
     - `Type-3 (Scale Boundary)`: Giới hạn tải sẽ chỉ chạm tới khi quy mô tăng gấp 10 lần.

---

## 5. Công Thức Tính Điểm `RRI` (`Requirement Readiness Index`)

Điểm `RRI` được tính trên thang `10.0` từ 5 trụ cột (mỗi trụ cột tối đa `2.0` điểm):
1. **Mục tiêu & Đầu ra (`Goal & Output` · `2.0đ`):** Bản `Indirect Prompting Restate` đã được Chủ nhà xác nhận và định nghĩa rõ trạng thái hoàn thành.
2. **Ngữ cảnh Runtime & Lịch sử (`/how + /why` · `2.0đ`):** Đã xác định rõ luồng runtime hiện tại và lý do lịch sử của các ràng buộc liên quan.
3. **Trường hợp Biên & Xử lý Lỗi (`Edge Cases & Error Recovery` · `2.0đ`):** Đã làm rõ hành vi khi dữ liệu rỗng, mạng lỗi, quyền truy cập bị từ chối hoặc dữ liệu trùng lặp.
4. **Ràng buộc Phi chức năng (`Non-functional Constraints` · `2.0đ`):** Đã chốt yêu cầu về bảo mật, độ trễ và tương thích ngược.
5. **Đòn bẩy Kiểm chứng (`Verification Lever` · `2.0đ`):** Đã biết rõ câu lệnh `./bin/control-app` hoặc kịch bản kiểm thử nào sẽ dùng để chứng minh tính năng hoạt động.

> **Cổng Chặn Cứng (`Hard Gate`):** Chỉ khi `RRI >= 8.5/10` và không còn quyết định `D<N>` nào ở trạng thái `unresolved`, Chủ thầu mới được phép chuyển sang Bước 3 (`VISION`) và Bước 4 (`BLUEPRINT`).
