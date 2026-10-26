# Phương Pháp Luận Vibecode Kit v6.2 (`× pstack`)

> **Quy trình 8 bước tự co giãn theo Rủi ro · Kỷ luật Bằng chứng · Đòn bẩy `/control-app` · Đấu trường Kiến trúc 5 Pha (`/architect`)**

---

## 1. Bốn Tầng Rủi Ro (`Risk Tiers R0 -> R3`) và Cơ chế Tự Co Giãn

Không phải bài toán nào cũng cần quy trình nặng nề như nhau. Trước khi bắt đầu, Chủ thầu phải phân loại yêu cầu vào đúng một trong 4 tầng rủi ro dưới đây để bật hoặc tắt các cổng kiểm soát tương ứng (đảm bảo các tác vụ nhỏ `R0`/`R1` chạy cực nhanh trong khi `R2`/`R3` được khóa chặt bằng chứng thực nghiệm):

| Cấp độ | Tên gọi | Dấu hiệu nhận diện | Chế độ vận hành (`v6.2 × pstack`) |
|---|---|---|---|
| **R0** | **Thay đổi Nhỏ (`Trivial`)** | Sửa lỗi chính tả, đổi nhãn văn bản, chỉnh màu sắc nhỏ trong `< 3` file, không đụng logic hay API. | **Gộp 1 lượt (`Fast-Track`):** Đọc nhanh `Feature Map` -> Sửa trực tiếp -> Chạy `./bin/control-app` hoặc test/build -> Báo cáo kèm `WTREE_FINGERPRINT`. |
| **R1** | **Thay đổi Vừa (`Standard`)** | Thêm hàm tiện ích, sửa lỗi có test tái hiện rõ ràng, nâng cấp thành phần giao diện cục bộ (`3–8` file). | **Rút gọn 4 nhịp:** `Indirect Prompting Restate` ngắn (2 câu) + đọc `Feature Map` -> Viết test đỏ -> Code xanh (áp dụng luật `Scrap when wrong` nếu lệch) -> Chạy `./bin/control-app` kiểm chứng sống -> Commit & Ship. |
| **R2** | **Thay đổi Hệ thống (`Systemic`)** | Tính năng mới xuyên suốt Frontend + Backend + Database, đổi cấu trúc bảng, tích hợp bên thứ ba (`> 8` file). | **Đầy đủ 8 bước chuẩn:** Bắt buộc chạy bộ tứ `/teach = /how + /why + /recall`, thiết kế ngược `Working Backwards (4 ô Diátaxis + /unslop)`, dựng `/prototype` (nếu có UI), chạy `5-Phase /architect Arena`, chia việc theo `sequence-verifiable-units`, điều phối `Worktree (<= 10)` hoặc `Cloud /swarm (> 10)` và kiểm chứng qua `./bin/control-app`. |
| **R3** | **Thay đổi Nghiêm trọng (`Critical`)** | Xác thực người dùng (Auth), phân quyền (RBAC), thanh toán, mật mã học, xóa/di chuyển dữ liệu lớn, hạ tầng Production. | **8 bước + Chế độ Cực đại (`Ultra / CSO`):** Bắt buộc có `5-Phase /architect Arena` đa model, tham vấn Quân sư (`Kongming`), kiểm toán bảo mật (`CSO / STRIDE`), Trọng tài độc lập (`C3`), phát hành 2 giai đoạn (`beta -> official`) và canh gác sau triển khai (`Canary`). |

---

## 2. Ba Vai Trò và Luồng Quyền Lực (`Chủ nhà / Người làm vườn · Chủ thầu · Thợ`)

```text
+---------------------------------------------------------------------------------------------------+
|                  CON NGƯỜI (CHỦ NHÀ / HOMEOWNER & NGƯỜI LÀM VƯỜN / THE GARDENER)                  |
|  1. Đặt đề bài -> 2. Duyệt bản diễn đạt lại (Indirect Prompting) & Chốt D<N> (Completeness X/10)  |
|  3. Tuần tra dòng chảy PR để nhổ cỏ dại kiến trúc từ sớm (The Gardener) & Nghiệm thu Live Proof   |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                             CHỦ THẦU (AI CONTRACTOR / COORDINATOR)                                |
|  - Bước 1 (SCAN): Đọc Feature Map, chạy Indirect Prompting Restate & /teach = /how + /why + /recall|
|  - Bước 2 (RRI): Hỏi tối đa 3 câu khử mơ hồ, lập Bảng Quyết định D<N> (Completeness X/10)          |
|  - Bước 3 (VISION): Working Backwards (Caller README · 4 ô Diátaxis + /unslop) & /prototype UI    |
|  - Bước 4 (BLUEPRINT): 5-Phase /architect Arena (Type Signatures Sketch) & Cổng 4 góc nhìn        |
|  - Bước 5 (TASK GRAPH): Chia sequence-verifiable-units; <=10 Local Worktrees vs >10 Cloud /swarm  |
|  - Bước 7 & 8 (VERIFY & SHIP): Chạy ./bin/control-app, gọi Trọng tài C3, xóa plan tạm sau merge   |
+------------------------+-------------------------------------------------+------------------------+
                         |                                                 |
                         v                                                 v
+------------------------------------------------+ +------------------------------------------------+
|             THỢ 1 (AI BUILDER #1)              | |             THỢ 2 (AI BUILDER #2)              |
|  - Làm việc trong nhánh cô lập (owned_files)   | |  - Làm việc trong nhánh cô lập (owned_files)   |
|  - Code từ Type Signatures Sketch theo TDD     | |  - Code từ Type Signatures Sketch theo TDD     |
|  - Báo SCRAP WHEN WRONG nếu phải dùng any/vá   | |  - Báo SCRAP WHEN WRONG nếu phải dùng any/vá   |
|  - Chạy ./bin/control-app đóng vòng lặp kiểm   | |  - Chạy ./bin/control-app đóng vòng lặp kiểm   |
+------------------------------------------------+ +------------------------------------------------+
```

### Quy tắc Phân quyền Cứng:
1. **Con người (`Chủ nhà & Người làm vườn`)** nắm quyền phủ quyết tối cao ở 3 điểm: (a) Duyệt bản diễn đạt lại đầu bài (`Indirect Prompting Restate`) và phương án tại `RRI`, (b) Duyệt kiến trúc tại `BLUEPRINT` và (c) Duyệt phát hành lên nhánh chính (`official`). Khi hệ thống đã có đòn bẩy kiểm chứng `./bin/control-app` chặt chẽ, kỹ sư thoát khỏi việc ngồi canh (`babysitting`) để đóng vai **Người làm vườn (`The Gardener`)**: liên tục tuần tra dòng chảy PR, nhổ bỏ "cỏ dại" từ trong trứng nước (như hàm tiện ích bị viết lặp lần thứ 3 trong tuần, lệnh tắt lint lan tràn) và chủ động refactor nền tảng ngay khi sản phẩm tăng trưởng nóng mà không gây downtime.
2. **Chủ thầu (`AI Contractor`)** không trực tiếp sửa code nghiệp vụ khi đang điều phối nhiều Thợ ở cấp `R2/R3` để giữ sạch vùng nhớ ngữ cảnh (`Context Window`) và giữ tính khách quan khi nghiệm thu.
3. **Thợ (`AI Builder`)** chỉ được phép sửa các tệp nằm trong danh sách `owned_files` của gói việc (`TIP`) được giao. Nếu phát hiện cần sửa tệp ngoài phạm vi, hoặc phát hiện kiến trúc trong `Blueprint` buộc phải truyền tham số vá víu qua nhiều tầng / ép kiểu `any`, Thợ phải dừng lại và phát tín hiệu **`Scrap when wrong`** về cho Chủ thầu.

---

## 3. Quy Trình 8 Bước Chuẩn (`Vibecode Kit v6.2 × pstack Workflow`)

### Bước 1: `SCAN` · Quét Thực Tế, Đọc `Feature Map`, `Indirect Prompting` & Bộ Tứ `/teach`
- **Mục tiêu:** Chặn đứng 2 điểm mù lớn nhất của Frontier Models (đầu bài mơ hồ và thiếu ngữ cảnh lịch sử/hệ thống) trước khi viết bất kỳ dòng code nào.
- **Hành động bắt buộc:**
  1. **Đọc Bộ nhớ Vật chất hóa (`Feature Map`):** Mở `references/features/README.md` (nếu dự án đã có) để nắm ngay danh mục tính năng, đường dẫn và lệnh `./bin/control-app` chạm tới màn hình/API liên quan mà không tốn hàng nghìn token mò mẫm.
  2. **Kỹ thuật `Indirect Prompting` (*"Restate in your own words"*):** Thay vì áp đặt ngay giả thuyết giải pháp, Chủ thầu đọc nguồn thông tin nhiễu (thread báo lỗi, log, yêu cầu thô) và diễn đạt lại bản chất bài toán bằng lời tự nhiên, ngắn gọn, không dùng từ lóng kỹ thuật che đậy để Chủ nhà xác nhận không bị lệch ý.
  3. **Xây dựng Mental Model hai chiều bằng bộ tứ `/teach = /how + /why + /recall`:**
     - `/how`: Truy vết cơ chế hoạt động hiện tại ở tầng runtime (tự động phân luồng các explorer agents chạy song song nếu hệ thống trải rộng trên nhiều thư mục/service).
     - `/why`: Truy tìm nguyên nhân lịch sử và ý đồ thiết kế bằng cách truy vấn song song `git log -S`, `git blame`, PR comments, ticket, tài liệu thiết kế và log lỗi (vì code chỉ cho biết *cái gì* đang chạy, không cho biết *tại sao* lại viết như vậy).
     - `/teach`: Yêu cầu Agent giải thích trực quan và chứng minh bằng code/dữ liệu thực tế vì sao phương án dự kiến tốt hơn hiện trạng (cơ chế ép Agent đọc code thật thay vì phán tự tin nhưng rỗng).
     - `/recall`: Rút trích ngữ cảnh từ lịch sử hội thoại hoặc phiên làm việc cũ (`transcripts`) thành bản tóm tắt trạng thái sạch.
- **Đầu ra:** Báo cáo thực trạng có đính kèm `file:line`, bản `Indirect Prompting Restate` và bảng phân loại tầng rủi ro (`R0–R3`).

### Bước 2: `RRI` · Phỏng Vấn Khử Mơ Hồ (`Requirement Readiness Index`)
- **Mục tiêu:** Đạt điểm rõ ràng yêu cầu `RRI >= 8.5/10` trước khi thiết kế.
- **Hành động:**
  - Nếu còn điểm mơ hồ về nghiệp vụ, hiệu năng, bảo mật hoặc trường hợp biên, Chủ thầu đặt **tối đa 3 câu hỏi trắc nghiệm** có kèm phương án khuyến nghị.
  - Mọi quyết định quan trọng được trình bày bằng **Bảng Quyết định `D<N>`**: có giải thích đơn giản (`ELI10`), điểm hoàn thiện (`Completeness X/10`), phân loại nợ kỹ thuật (`Shortcut Debt`) và bảng so sánh cam kết.
- **Đầu ra:** Tài liệu [`RRI-template.md`](./templates/RRI-template.md) đã được Chủ nhà phê duyệt (`Status: approved`).

### Bước 3: `VISION` · Thiết Kế Ngược `Working Backwards (Diátaxis + /unslop)` & Dựng `/prototype`
- **Mục tiêu:** Chống "ảo giác tiến độ" (`illusion of progress`) của các bản kế hoạch trừu tượng vốn chỉ mô tả tiểu tiết cài đặt bên trong mà bỏ quên trải nghiệm của người gọi API hoặc người dùng cuối.
- **Hành động:**
  1. **Thiết kế Ngược từ README (`Working Backwards` & Khung 4 ô `Diátaxis`):** Khi thiết kế module, dịch vụ hoặc gói dùng chung, bắt buộc viết `Caller README / Tutorial` trước từ góc nhìn người sử dụng theo đúng 4 góc nhìn `Diátaxis` (`Tutorial`, `How-to`, `Reference`, `Explanation`) và lọc bỏ toàn bộ văn phong AI rườm rà bằng quy tắc `/unslop`.
  2. **Lập kế hoạch giao diện bằng Code (`/prototype` Live Switcher):** Với các tính năng có giao diện hoặc trải nghiệm tương tác, thay vì tranh luận trên văn bản, dựng nhanh 2 đến 3 phương án thiết kế ẩn sau một nút chuyển trực tiếp trên màn hình (`Live UI Switcher`), dùng `./bin/control-app` chạy thật, chụp ảnh và đo đạc để Chủ nhà chọn phương án bằng bằng chứng thực nghiệm.
- **Đầu ra:** Bản nháp `Caller README (Diátaxis)` đã khử văn phong AI rườm rà và ảnh chụp/kết quả đo của 2 đến 3 phương án `/prototype` (nếu có UI).

### Bước 4: `BLUEPRINT` · Đấu Trường Kiến Trúc 5 Pha (`/architect Arena`) & Cổng Duyệt 4 Góc Nhìn
- **Mục tiêu:** Tránh hai sai lầm chết người khi lập kế hoạch: (1) chấp nhận ngay thiết kế đầu tiên của Agent và (2) review đối kháng quá đà trên bản kế hoạch chữ trừu tượng (khiến Agent tự bịa ra các rủi ro lý thuyết không bao giờ xảy ra để phòng thủ).
- **Hành động:**
  1. **Thực thi 5 Pha Kỷ luật của `/architect` (`Architecture Arena`):**
     - **Pha 1 (`Ground`):** Nạp kết quả `/how` và `/why` để khóa quyền sở hữu dữ liệu (`ownership`) và các ràng buộc bất biến.
     - **Pha 2 (`Sketch` · Đấu trường Chữ ký Kiểu):** Cho nhiều nhánh (đa model) độc lập phác thảo **`Type Signatures & Caller Usage Sketch`** (chỉ viết khung kiểu dữ liệu, chữ ký hàm và đoạn code minh họa nơi gọi hàm, **tuyệt đối chưa viết thân hàm**).
     - **Pha 3 (`Cross-judge & Synthesize`):** Dùng một model độc lập làm trọng tài chấm điểm các bản phác thảo theo rubric (độ sâu module Ousterhout, tính dễ ghép nối, an toàn kiểu dữ liệu) và tổng hợp thành bản thiết kế tốt nhất.
     - **Pha 4 (`Implement against the sketch`):** Chuyển khung chữ ký hàm sang bước thực thi để điền logic thật.
     - **Pha 5 (`Scrap when wrong`):** Khóa cứng các tín hiệu bắt buộc đập đi làm lại ngay nếu khi vào code thật phát hiện kiến trúc sai.
  2. **Chạy Cổng Duyệt Kế hoạch 4 Góc nhìn (`4-Lens Plan Gate`):**
     - **Lăng kính 1 (CEO / Scope):** Kiểm tra giá trị cốt lõi và loại bỏ tính năng thừa.
     - **Lăng kính 2 (Design / UX):** Kiểm tra trạng thái rỗng (`Empty`), đang tải (`Loading`), lỗi (`Error`) và quá tải (`Overflow`).
     - **Lăng kính 3 (Engineering / Architecture):** Kiểm tra sơ đồ luồng dữ liệu, **Bảng Ánh xạ Lỗi & Cứu hộ (`Error & Rescue Map`)** và chiến lược kiểm thử.
     - **Lăng kính 4 (Developer Experience / DX):** Kiểm tra khả năng điều khiển qua `./bin/control-app`, thông báo lỗi chỉ dẫn lệnh tiếp theo và tốc độ khởi chạy của Thợ.
- **Đầu ra:** Tài liệu [`Blueprint-template.md`](./templates/Blueprint-template.md) đạt trạng thái `NO UNRESOLVED DECISIONS`.

### Bước 5: `TASK GRAPH` · Chia Nhỏ Theo `Sequence-Verifiable-Units` & Phân Luồng `Worktree / Cloud Swarm`
- **Mục tiêu:** Chỉ xuất kế hoạch thực thi sau khi thiết kế đã được chứng minh qua `/prototype` hoặc `Type Signatures Sketch`, chia thành các đơn vị kiểm chứng độc lập và không làm nghẽn phần cứng máy cá nhân.
- **Hành động:**
  1. **Chia gói việc theo đơn vị kiểm chứng tuần tự (`sequence-verifiable-units`):** Mỗi gói giao việc ([`TIP-template.md`](./templates/TIP-template.md)) phải tương ứng với một PR nhỏ độc lập, có danh sách `owned_files` riêng biệt và gắn chặt với một câu lệnh **`Live Verification`** qua `./bin/control-app` ("chỉ pass unit test là chưa đủ, phải chạy code thật").
  2. **Định tuyến Thực thi Song song (`Local Worktrees <= 10` vs. `Cloud Agents + /swarm > 10`):**
     - **Khi số nhánh song song `<= 10`:** Sử dụng `git worktree` cục bộ trên máy cá nhân với port và cơ sở dữ liệu kiểm thử tách biệt.
     - **Khi số nhánh song song `> 10` hoặc cần chạy kiểm chứng quy mô lớn (`/swarm`, `auto-repro`):** Máy cá nhân sẽ chạm trần phần cứng (tốn ổ cứng, đụng độ port/DB, tràn RAM). Chủ thầu đóng vai `Coordinator Bot` (giữ context sạch) và đẩy việc nặng sang **`Cloud Agents`** (mỗi agent chạy trên máy ảo đám mây có snapshot khởi động tức thì và có màn hình ảo thật để quay video/chụp ảnh), kết hợp lệnh `/swarm` để fan-out hàng loạt agent kiểm chứng độ ổn định hoặc tự động tái hiện lỗi (`auto-repro`) ngay khi có báo lỗi từ Slack.
- **Đầu ra:** Đồ thị phụ thuộc (`DAG`) và bộ hồ sơ giao việc `TIP-01`, `TIP-02`...

### Bước 6: `BUILD` · Thợ Thực Thi TDD, Đòn Bẩy `./bin/control-app` & Kỷ Luật `Scrap When Wrong`
- **Mục tiêu:** Biến khung chữ ký kiểu (`Type Signatures Sketch`) thành mã nguồn sạch kèm đòn bẩy kiểm chứng tự động.
- **Hành động của Thợ:**
  1. Nếu tính năng mới chưa có subcommand tương ứng trong `./bin/control-app`, Thợ phải cập nhật hoặc xây dựng bổ sung đòn bẩy `./bin/control-app` trước theo biểu mẫu [`Control-App-and-Feature-Map.md`](./templates/Control-App-and-Feature-Map.md).
  2. Viết bài kiểm thử thất bại trước (`Red`) dựa trên tiêu chí chấp nhận trong `TIP`.
  3. Điền thân hàm vào khung `Type Signatures Sketch` để bài kiểm thử vượt qua (`Green`) và làm sạch mã (`Refactor`).
  4. **Kỷ luật `Scrap when wrong` (Đập đi làm lại khi kiến trúc sai):** Trong lúc viết code thật, nếu Thợ phát hiện bất kỳ dấu hiệu nào sau đây:
     - Phải truyền thêm tham số vá víu (`pass-through parameter hacks`) xuyên qua 3 tầng hàm không liên quan;
     - Phải lặp lại cùng một đoạn code chữa cháy (`workaround`) ở nhiều nơi;
     - Phải dùng kiểu `any`, `unknown` vô căn cứ hoặc ép kiểu cưỡng bức (`as unknown as T`) để vượt qua trình biên dịch;
     -> **Đó là bằng chứng thực nghiệm cho thấy kiến trúc ở Bước 4 đã sai.** Thợ **BẮT BUỘC DỪNG CODE NGAY**, phát tín hiệu `SCRAP_TRIGGERED` về Chủ thầu để quay lại Pha 2 của `/architect` thiết kế lại chữ ký hàm, tuyệt đối không cố đấm ăn xôi.
- **Đầu ra:** Nhánh mã nguồn hoàn chỉnh, test xanh 100%, không có cảnh báo trình biên dịch và đính kèm biên bản [`Completion-Report.md`](./templates/Completion-Report.md).

### Bước 7: `VERIFY` · Khép Kín Vòng Lặp Với `./bin/control-app` & Trọng Tài Độc Lập (`C3`)
- **Mục tiêu:** Biến Verification thành **Hạ tầng Cốt lõi (`Critical Infrastructure`)**: Agent tự chạy ứng dụng, tự thao tác, tự đọc log/trace và tự chụp bằng chứng (ảnh/video/JSON) để khép kín vòng lặp (`close the loop`) mà không cần con người ngồi canh.
- **Hành động:**
  1. **Kiểm chứng Sống bằng Đòn bẩy `./bin/control-app` (`Live Verification`):** Chạy `./bin/control-app` để seed DB chuẩn, giả lập người dùng thử nghiệm, bật/tắt feature flag, chụp cây giao diện (`DOM / accessibility tree`), chụp ảnh màn hình và thu thập kết quả JSON máy đọc được.
  2. **Kiểm tra Văn phong & Bảo mật (`Constraint Loop`):** Quét khóa bí mật, kiểm tra định dạng đầu ra và xác nhận 0 lỗi lint/typecheck.
  3. **Trọng tài Độc lập (`Independent Arbiter C3`):** Với các tác vụ cấp `R2` và `R3`, một phiên đánh giá độc lập (không dùng chung bộ nhớ với Thợ) sẽ đối chiếu mã nguồn thực tế với `Blueprint` gốc.
- **Đầu ra:** Biên bản nghiệm thu đóng dấu mã băm `WTREE_FINGERPRINT` ở trạng thái `DIRTY=false`.

### Bước 8: `REFINE & SHIP` · Phát Hành 2 Giai Đoạn, Vai Trò `The Gardener`, Xóa Plan Tạm & Bảo Trì `Feature Map`
- **Mục tiêu:** Đưa sản phẩm lên môi trường đích an toàn, giữ kho mã nguồn luôn sạch tinh tươm và cập nhật bộ nhớ tính năng cho các chu kỳ sau.
- **Hành động:**
  1. **Phát hành 2 giai đoạn (`Dual-Stage Ship`):** Hợp nhất vào nhánh thử nghiệm (`beta`) -> Chạy kiểm tra hậu triển khai (`Canary`) -> Hợp nhất vào nhánh chính thức (`official`).
  2. **Tuần tra theo vai trò "Người làm vườn" (`The Gardener`):** Quét phát hiện và nhổ bỏ sớm các mầm mống suy thoái kiến trúc (hàm tiện ích bị viết trùng lặp lần thứ 3 trong tuần, lệnh tắt kiểm tra lint `eslint-disable` / `@ts-ignore`, hoặc cấu hình lệch chuẩn).
  3. **Vệ sinh Kho mã nguồn (`Temporary Plan Cleanup`):** Ngay sau khi PR đã được merge hoàn tất, xóa bỏ các file kế hoạch thực thi tạm thời trong nhánh làm việc hoặc di chuyển vào thư mục lưu trữ `_Archive/` để không biến kho mã nguồn thành bãi rác gây nhiễu context cho các Agent thế hệ sau.
  4. **Bảo trì Bộ nhớ Vật chất hóa (`/maintain-verification-skill` & `Post-Ship Sync`):** Chạy quy trình cập nhật `Feature Map` (`references/features/README.md`) để phản ánh chính xác các tính năng, đường dẫn và lệnh `./bin/control-app` mới vừa phát hành; đồng bộ mã băm SHA-256 sang Bộ 02 (`Kernel Registry`) và chấm điểm [`Calibration-Card.md`](./templates/Calibration-Card.md) trên thang 100 điểm.

---

## 4. Ma Trận Ánh Xạ Kỹ Năng (`Vibecode v6.2 × AgentKit × gstack × pstack`)

| Bước trong Vibecode v6.2 | Kỹ năng AgentKit (`ak-*`) | Kỹ năng `gstack` | Đòn bẩy `pstack` (`@poteto`) | Biểu mẫu / Tài liệu đích |
|---|---|---|---|---|
| **1. SCAN** | `ak-scout`, `ak-fable-thinking` | `/investigate`, `/context-restore` | `Indirect Prompting Restate`, `/teach = /how + /why + /recall`, đọc `Feature Map` | `Risk-Tier-Classification.md` |
| **2. RRI** | `ak-brainstorm`, `ak-ask` | `/office-hours`, `/spec` | Khử điểm mù `Under-specified Intent` trước khi thiết kế | `RRI-template.md` |
| **3. VISION** | `ak-frontend-design`, `ak-ui-ux-pro-max` | `/design-consultation`, `/design-shotgun` | `Working Backwards (4 ô Diátaxis + /unslop)`, `/prototype` (Live Switcher) | `Blueprint-template.md` |
| **4. BLUEPRINT** | `ak-plan`, `ak-issue-to-plan`, `@kongming` | `/autoplan`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-devex-review` | `5-Phase /architect Arena` (`Ground -> Sketch Type Signatures -> Judge -> Implement -> Scrap`) | `Blueprint-template.md` |
| **5. TASK GRAPH** | `ak-worktree`, `ak-orchestrate`, `ak-handoff` | `/freeze`, `/guard` | `sequence-verifiable-units`, `Coordinator + Cloud Agents + /swarm (auto-repro)` | `TIP-template.md`, `Handoff-Contract.md` |
| **6. BUILD** | `ak-cook`, `ak-fix`, `ak-backend-development`, `ak-frontend-development` | `/careful`, `/codex` | Xây `./bin/control-app` (Deep Module), thực thi luật `Scrap when wrong` | `Control-App-and-Feature-Map.md`, `Completion-Report.md` |
| **7. VERIFY** | `ak-test`, `ak-web-testing`, `ak-code-review`, `ak-security` | `/review`, `/qa`, `/cso`, `/benchmark` | `Live Verification` qua `./bin/control-app --json` (khép kín vòng lặp) | `Audit-Trail-Loop.md` |
| **8. REFINE & SHIP** | `ak-ship`, `ak-git`, `ak-retro`, `post-ship-notion-sync` | `/ship`, `/land-and-deploy`, `/canary`, `/retro`, `/learn` | `The Gardener` tuần tra PR, xóa file plan tạm, `/maintain-verification-skill` | `Calibration-Card.md`, `references/features/README.md` |
