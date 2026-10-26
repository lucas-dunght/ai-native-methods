# Giao Thức Đòn Bẩy Tự Kiểm Chứng (`./bin/control-app`), Bản Đồ `Feature Map`, Chẩn Đoán Đa Giả Thuyết & Trọng Tài Độc Lập (`VERIFY Protocol`)

> **Bước 6 & Bước 7 của Vibecode Kit v6.2 (`× pstack`) · "Verification is all you need" · Xây Đòn Bẩy Bằng CLI Thay Vì Chỉ Viết Markdown**

---

## 1. Tại Sao Verification Là Hạ Tầng Cốt Lõi (`Verification as Critical Infrastructure`)?

Bài học nền tảng số 1 từ hệ thống `pstack` của `@poteto`:
> **Nếu AI Agent không thể tự kiểm chứng công việc của chính nó, mọi thứ khác đều trở nên vô nghĩa vì con người vẫn là nút thắt cổ chai (`bottleneck`).**

- **Verification thực chất là gì?** Không phải là chỉ chạy một bài unit test trên dữ liệu giả (`mock`), mà là Agent **tự chạy ứng dụng thật, tự thao tác trên giao diện/API, tự đọc log/trace và tự chụp bằng chứng (ảnh màn hình, video, cây DOM, phản hồi JSON)** để khép kín vòng lặp (`close the loop`) cho đến khi đạt kết quả đúng mà không cần con người ngồi canh (`babysitting`).
- Khi một nền tảng có rào chắn (`guardrails`) và công cụ tự kiểm chứng đủ mạnh, cả kỹ sư lẫn người không chuyên (`non-engineers`) đều có thể đóng góp tính năng an toàn, nhân **100 đến 1000 lần** năng suất của toàn đội.

---

## 2. Nguyên Lý "Build the Lever": Xây Đòn Bẩy `./bin/control-app` CLI (`Deep Modules`)

Sai lầm phổ biến nhất của các bộ kỹ năng AI truyền thống là chỉ viết hướng dẫn kiểm thử bằng chữ trong `SKILL.md` (ví dụ: *"Hãy mở trình duyệt, đăng nhập rồi kiểm tra trang thanh toán"*). Cách làm này khiến Agent phải tốn hàng nghìn token để tự viết các đoạn script dùng một lần (`one-off scripts`) mỗi khi cần test, vừa chậm vừa dễ gãy.

**Giải pháp của Vibecode Kit v6.2:** Đóng gói một công cụ dòng lệnh thân thiện với Agent mang tên **`./bin/control-app`** theo triết lý **Deep Modules** của John Ousterhout (xem biểu mẫu chi tiết tại [`templates/Control-App-and-Feature-Map.md`](../templates/Control-App-and-Feature-Map.md)).

### Sáu Tiêu Chuẩn Bắt Buộc Khi Thiết Kế `./bin/control-app` Cho Agent:
1. **Dễ ghép nối & Hé lộ chức năng tăng dần (`Composable Subcommands & Progressive Disclosure`):**
   - Chia thành các lệnh con rõ nghĩa: `./bin/control-app <seed|auth|flag|dom|screenshot|perf|repro|doctor>`.
2. **Bắt buộc có cờ `--dry-run` cho mọi lệnh gây tác dụng phụ:**
   - Bất kỳ lệnh nào làm thay đổi cơ sở dữ liệu, trạng thái phiên hoặc cấu hình đều phải hỗ trợ `--dry-run` để Agent kiểm tra trước tác động mà không làm hỏng môi trường.
3. **Thông báo lỗi chỉ dẫn hành động (`Actionable Error Messages`):**
   - Khi lệnh thất bại, thông báo lỗi phải mô tả rõ **nguyên nhân gốc (`root_cause`)** và **chỉ dẫn trực tiếp câu lệnh tiếp theo Agent cần chạy (`next_command`)** để tự phục hồi.
4. **Hỗ trợ `--help` chi tiết và trả đầu ra máy đọc được (`--json`):**
   - Mọi lệnh con đều có `--help` kèm ví dụ thực tế và trả về cấu trúc JSON thống nhất để Agent đọc kết quả chính xác 100%.
5. **Bao phủ trọn vẹn Trải nghiệm Phát triển (`Full DX Coverage`):**
   - `seed`: Nạp dữ liệu mẫu chuẩn xác vào DB kiểm thử.
   - `auth`: Giả lập đăng nhập người dùng thử nghiệm (`mock auth / test user`) không cần qua bước nhập mật khẩu thủ công hay OTP.
   - `flag`: Bật hoặc tắt `feature flag` ngay trong phiên làm việc (kể cả chuyển đổi giữa các phương án `/prototype`).
   - `dom`: Lấy bản chụp cây giao diện (`DOM / Accessibility Tree snapshot`) đã lọc nhiễu để tiết kiệm token.
   - `screenshot`: Chụp ảnh màn hình hoặc quay video tại đúng đường dẫn cần nghiệm thu.
   - `perf`: Đo thời gian phản hồi API, số lượng câu truy vấn SQL (`N+1 check`) và chỉ số hiển thị.
6. **Khép kín vòng lặp tự trị (`Autonomous Loop Closure`):**
   - Cho phép Thợ chạy chu trình `Sửa code -> Chạy ./bin/control-app -> Đọc JSON/Log -> Tự sửa tiếp` cho tới khi `ok: true`.

---

## 3. Bộ Nhớ Vật Chất Hóa (`Materialized Memory · Feature Map` & `/maintain-verification-skill`)

Khi ứng dụng phình to lên hàng trăm màn hình và API, Agent sẽ đốt sạch vùng nhớ ngữ cảnh (`context window`) chỉ để mò xem tính năng nằm ở đâu và làm sao để đi tới màn hình đó.

### Cấu trúc Bản đồ Tính năng (`Feature Map` tại `references/features/README.md`):
- Là bản đồ tra cứu nhanh từ góc nhìn người dùng: liệt kê danh mục mọi tính năng của sản phẩm, mục đích nghiệp vụ, đường dẫn URL/Route, tệp mã nguồn chính và **câu lệnh `./bin/control-app` cụ thể để chạm tới và kiểm chứng tính năng đó**.
- **Nguyên lý cốt lõi:** **Codebase là nguồn chân lý tối thượng (`Ultimate Source of Truth`)**, còn `Feature Map` là bản nén tiết kiệm token của codebase.

### Tác vụ Bảo trì Hàng ngày (`/maintain-verification-skill`):
- Để `Feature Map` và `./bin/control-app` không bị trôi (`drift`) so với code thật khi sản phẩm thay đổi liên tục, phải chạy quy trình bảo trì `/maintain-verification-skill` định kỳ hàng ngày hoặc ngay ở Bước 8 (`SHIP`):
  1. Quét danh sách các tệp định tuyến (`routes`), `controllers` và `components` đã thay đổi qua `git diff` hoặc đối chiếu mã băm SHA-256 trong Bộ 02 (`Kernel Registry`).
  2. Tự động phát hiện các đường dẫn mới chưa có trong `references/features/README.md` hoặc các lệnh `./bin/control-app` bị gãy.
  3. Cập nhật lại `references/features/README.md` và chạy `./bin/control-app doctor --json` để xác nhận toàn bộ các mục trong bản đồ đều hoạt động sống.

---

## 4. Chẩn Đoán Đa Giả Thuyết Khi Gặp Lỗi (`Multi-Hypothesis Root Cause Debugging`)

Khi một bài kiểm thử hoặc lệnh `./bin/control-app` báo lỗi, nghiêm cấm việc đoán mò và sửa bừa. Bắt buộc tuân thủ quy trình 4 bước:
1. **Dựng lại lỗi bằng `./bin/control-app repro` (`Reproduce First`):** Chạy lệnh tái hiện lỗi ổn định (hoặc dùng `/swarm` trên `Cloud Agents` nếu là lỗi chập chờn).
2. **Liệt kê tối thiểu 3 Giả thuyết Độc lập (`H1`, `H2`, `H3`):**
   - Đặt câu hỏi: *"Thí nghiệm nhỏ nhất nào (đọc log, in biến, kiểm tra git blame qua `/why`) sẽ bác bỏ `H1` và xác nhận `H2`?"*
3. **Chứng minh Nguyên nhân Gốc trước khi sửa (`Prove Root Cause Before Fix`):** Chỉ được sửa code sau khi đã chỉ ra đúng dòng code gây lỗi (`[OBSERVED: file:line]`).
4. **Khóa lỗi bằng Kiểm thử Hồi quy (`Regression Lock`):** Biến kịch bản tái hiện lỗi thành bài test tự động để lỗi đó không bao giờ quay lại.

---

## 5. Kiểm Thử Theo Bề Mặt (`Surface-Aware Live Verification`) & Vòng Lặp Ràng Buộc (`Constraint Loop`)

Mọi tính năng trước khi báo cáo hoàn thành ở Bước 7 (`VERIFY`) phải đi qua kiểm chứng sống theo đúng bề mặt bị tác động:
- **Bề mặt Giao diện Web/App (`UI Surface`):** Chạy `./bin/control-app dom` và `./bin/control-app screenshot` kiểm tra cả trạng thái chuẩn, trạng thái rỗng (`Empty`) và trạng thái lỗi (`Error`), xác nhận `0` lỗi Console/Uncaught Exception.
- **Bề mặt API / Backend (`API Surface`):** Gửi request thật qua `./bin/control-app` với cả dữ liệu hợp lệ (`2xx`), dữ liệu thiếu trường (`400`) và thiếu quyền (`401/403`).
- **Bề mặt CLI / Script / Tài liệu (`CLI & Docs Surface`):** Chạy kiểm tra cờ `--help`, `--dry-run`, `--json` và chạy **Vòng lặp Ràng buộc (`Constraint Loop`)** quét tự động toàn bộ các quy tắc định dạng/bảo mật cho tới khi đạt `0` vi phạm.

---

## 6. Trọng Tài Độc Lập (`Independent Arbiter C3`)

Đối với các tác vụ cấp `R2` và `R3`, người viết code (Thợ) không được tự chấm bài của chính mình ở cổng cuối:
- Chủ thầu khởi tạo một phiên đánh giá độc lập (**Trọng tài `C3`**) chỉ nhận vào: (1) Bản vẽ `Blueprint` gốc, (2) Thay đổi thực tế (`git diff`), (3) Kết quả chạy `./bin/control-app --json` và (4) Dấu vân tay `WTREE_FINGERPRINT`.
- Trọng tài `C3` kiểm tra độc lập từng tiêu chí chấp nhận (`AC-1..AC-N`). Chỉ khi Trọng tài đóng dấu `ARBITER_VERDICT: APPROVED`, gói việc mới được chuyển sang Bước 8 (`SHIP`).
