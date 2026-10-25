# Methodology · Vibecode Kit v6.1

## Triết lý nền tảng

Chủ thầu biết tổng thể, giao việc rõ ràng, nghiệm thu bằng bằng chứng cơ học.

Thợ thi công xuất sắc trong phạm vi được giao, tự kiểm tra kỹ, báo cáo trung thực kèm dấu vân tay mã nguồn.

Con người giữ quyền phán xét cuối cùng ở các quyết định chiến lược và chịu trách nhiệm về sản phẩm.

AI đã học hàng tỷ dòng code và hàng triệu mẫu thiết kế. Phương pháp luận định nghĩa cái cần đạt (WHAT và tiêu chuẩn bằng chứng), không trói buộc từng bước suy nghĩ nội tâm của AI (HOW).

Tin AI nhưng luôn kiểm chứng đầu ra. Một báo cáo tự khen "đã xong" không có giá trị nếu thiếu bằng chứng kiểm thử gắn với trạng thái mã nguồn hiện hành.

## Ba vai trò chính và Lớp Cố vấn Độc lập

```
                     CON NGƯỜI (Homeowner)
                     Muốn. Chọn. Chịu trách nhiệm.
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
        CHỦ THẦU                      THỢ
       (Contractor)                 (Builder)
      Thiết kế + Điều phối        Code + Test + Báo cáo
               ◄── TIP / Handoff / Report ──►
               │                         ▲
               └──► QUÂN SƯ / TRỌNG TÀI ─┘
                   (Kongming / Arbiter C3)
                 Phản biện độc lập · Không code
```

| Vai trò | Bản chất | Ranh giới tín nhiệm (Trust boundary) |
|---|---|---|
| Con người (Homeowner) | Đề ra mục tiêu, chọn phương án ở cửa một chiều, duyệt Blueprint, quyết định phát hành | Không viết code, không sa đà vào chi tiết kỹ thuật vụn vặt |
| Chủ thầu (Contractor) | Khảo sát, phỏng vấn ngược, thiết kế Blueprint, chia TIP, điều phối đa Thợ, nghiệm thu | Không viết code sản phẩm. Có toàn quyền điều chỉnh quy trình theo thực tế và ghi lại lý do. |
| Thợ (Builder) | Nhận TIP, viết code trong phạm vi khóa, viết test, tự chạy kiểm tra, lập báo cáo hoàn thành | Chỉ sửa các file thuộc quyền sở hữu của TIP. Thấy cách tốt hơn thì đề xuất, không tự ý đổi kiến trúc. |
| Quân sư / Trọng tài (Kongming / Arbiter) | Phiên AI độc lập (ưu tiên model mạnh nhất hoặc khác họ model) đóng vai cố vấn và chấm chéo | Chỉ đưa lời khuyên Go/No-Go, vạch trần điểm mù và chấm đối chiếu. Tuyệt đối không sửa code. |

Tại sao phiên bản v6.1 bổ sung lớp **Quân sư và Trọng tài độc lập**? Khi cùng một phiên AI vừa lập kế hoạch, vừa viết code, vừa tự chấm điểm, nó rất dễ mắc thiên kiến tự xác nhận (self-grading bias). Tách một phiên Trọng tài có ngữ cảnh mới tinh (hoặc khác dòng mô hình như Claude chấm chéo với GPT/Codex) giúp phát hiện lỗi kiến trúc và lỗi lách luật kiểm thử trước khi sản phẩm tới tay Con người.

## Phân tầng rủi ro (Risk Tiers R0 đến R3) và Sự co giãn của Quy trình

Không có một quy trình cứng nhắc áp cho mọi việc. Chủ thầu phân loại tác vụ dựa trên hai trục là **Mức độ tác động nếu sai (Impact)** và **Khả năng đảo ngược (Reversibility)**.

| Mức tác động \ Khả năng đảo ngược | Đảo ngược tức thì (Reversible) | Đảo ngược một phần (Partial) | Khó hoặc không thể đảo ngược (Irreversible) |
|---|---|---|---|
| **Thấp (Low)** | **R0** (Trivial) | **R1** (Low) | **R2** (Medium) |
| **Trung bình (Medium)** | **R1** (Low) | **R2** (Medium) | **R3** (High) |
| **Cao / Nghiêm trọng (High / Critical)** | **R2** (Medium) | **R3** (High) | **R3** (Critical) |

Cách quy trình 8 bước tự co giãn theo từng phân tầng.

- **Tác vụ R0 (5 đến 15 phút, ví dụ sửa nhãn nút bấm, chỉnh màu sắc).** Chủ thầu rút gọn tối đa. Quét nhanh file liên quan, viết TIP một dòng, Thợ sửa và chạy kiểm tra nhanh, ghi một dòng hiệu chỉnh vào nhật ký. Bỏ qua RRI và Blueprint.
- **Tác vụ R1 (1 TIP, dưới 2 giờ, ví dụ thêm bộ lọc cục bộ, sửa một lỗi đơn lẻ).** Có TIP chuẩn, Blueprint ngắn gọn nửa trang, Thợ thi công với khóa phạm vi (`Scope Freeze`), nộp Completion Report có bằng chứng chạy test và thẻ hiệu chỉnh ngắn.
- **Tác vụ R2 (2 đến 5 TIPs, ví dụ làm tính năng đăng nhập, tạo module báo cáo).** Chạy đầy đủ 8 bước. Phỏng vấn RRI bằng thẻ quyết định `D<N>`, duyệt kế hoạch qua 4 lăng kính, chia Task Graph rõ ràng, kiểm thử bề mặt thật và lập Calibration Card 100 điểm sau khi phát hành.
- **Tác vụ R3 (5+ TIPs, ứng dụng mới, thanh toán, phân quyền bảo mật hoặc chạy nhiều Thợ song song).** Chạy đủ 8 bước kèm toàn bộ cơ chế bảo vệ nâng cao. Bật cố vấn Kongming ở các điểm chốt, phản biện Red-Team 4 góc nhìn (hoặc Ultra Best-of-5), cô lập từng Thợ trên một Git Worktree riêng, nghiệm thu qua Trọng tài độc lập và phát hành 2 chặng (`Beta -> Stable`).

Chủ thầu có quyền nâng hoặc hạ phân tầng ngay giữa chừng nếu phát hiện bài toán phức tạp hơn hoặc đơn giản hơn dự kiến ban đầu, miễn là ghi rõ lý do vào Audit Trail.

## Tám bước trong một chu kỳ Vibecode v6.1

```
SCAN → RRI → VISION → BLUEPRINT → TASK GRAPH → BUILD → VERIFY → REFINE & SHIP
```

### Bước 1 · SCAN (Khảo sát Hiện trạng và Kỷ luật Nhận định)

Trước khi đặt câu hỏi hay vẽ kiến trúc, Builder phải khảo sát thực tế kho mã nguồn và môi trường vận hành. Với dự án mới hoàn toàn, kiểm tra nhanh thư mục, công cụ dòng lệnh và môi trường sẵn có. Với dự án đang tồn tại, quét toàn diện cấu trúc thư mục, công nghệ sử dụng, các quy ước ngầm, lỗ hổng bảo mật và độ phủ kiểm thử.

Điểm nâng cấp cốt lõi ở v6.1 là mọi khẳng định quan trọng trong `SCAN REPORT` phải gắn một trong bốn nhãn **Kỷ luật Nhận định (Fable 5.1 Claim Discipline)**.
- **OBSERVED.** Sự thật đã quan sát trực tiếp trong phiên làm việc thông qua việc đọc file, chạy lệnh hoặc đo đạc.
- **DERIVED.** Kết luận suy ra một cách logic từ các dữ kiện OBSERVED kèm cơ chế rõ ràng.
- **PRIOR.** Kiến thức tổng quát từ dữ liệu huấn luyện của mô hình. Nếu thông tin này ảnh hưởng đến thiết kế, bắt buộc phải chạy công cụ kiểm tra để nâng cấp lên OBSERVED.
- **ASSUMED.** Giả định chưa thể kiểm chứng ngay. Phải viết rõ câu cảnh báo về hậu quả nếu giả định này sai.

Ảo giác nguy hiểm nhất của AI là viết một điều thuộc nhóm PRIOR hoặc ASSUMED bằng giọng văn khẳng định chắc nịch như thể đã OBSERVED. Kỷ luật này chặn đứng ảo giác ngay từ bước đầu tiên. Đọc chi tiết tại `references/claim-and-evidence-protocol.md` và `references/xray-and-scan-protocol.md`.

### Bước 2 · RRI (Phỏng vấn Ngược và Phân loại Quyết định 3 tầng)

Sau khi có kết quả Scan, Chủ thầu tự trả lời tất cả những gì mã nguồn đã thể hiện rõ. Những khoảng trống còn lại mới đưa vào phiên **Phỏng vấn Ngược (Reverse Requirements Interview)** qua 5 góc nhìn đại diện.
1. **End User** (Người dùng cuối quan tâm luồng trải nghiệm và tốc độ phản hồi).
2. **Business Analyst** (Chuyên viên nghiệp vụ quan tâm quy tắc miền, dữ liệu biên và tính hợp lệ).
3. **QA / Tester** (Kỹ sư kiểm thử quan tâm kịch bản lỗi, trạng thái rỗng và dữ liệu độc hại).
4. **Developer** (Lập trình viên quan tâm khả năng bảo trì, tích hợp và nợ kỹ thuật).
5. **Operator** (Người vận hành quan tâm triển khai, giám sát, sao lưu và khôi phục khi sự cố).

Ba chế độ đặt câu hỏi gồm **CHALLENGE** (Chủ thầu đề xuất phương án tối ưu, Con người chỉ cần gật hoặc lắc), **GUIDED** (Hỏi kèm 2 đến 3 lựa chọn gợi ý có phân tích ưu nhược điểm) và **EXPLORE** (Hỏi mở cho các ý tưởng hoàn toàn mới).

Để tránh làm Con người mệt mỏi vì hàng chục câu hỏi vụn vặt, v6.1 áp dụng **Phân loại Quyết định 3 tầng (Decision Classification)**.
- **Tầng 1 · Mechanical (Cơ học).** Những câu hỏi chỉ có một đáp án kỹ thuật đúng đắn hiển nhiên (ví dụ bật kiểm tra kiểu tĩnh, dùng biến môi trường cho khóa bí mật). Chủ thầu tự quyết định và ghi vào Decisions Log.
- **Tầng 2 · Taste (Khẩu vị và Đánh đổi cân bằng).** Những lựa chọn có hai hướng khả thi tương đương. Chủ thầu đánh dấu phương án khuyến nghị `(recommended)` và gom lại thành một bảng tóm tắt để Con người duyệt nhanh ở cuối bước.
- **Tầng 3 · User Challenge (Thách thức Chiến lược và Cửa một chiều).** Những quyết định làm thay đổi phạm vi, chi phí, trải nghiệm cốt lõi hoặc không thể hoàn tác dễ dàng. Chủ thầu bắt buộc trình bày dưới dạng thẻ **Decision Brief `D<N>`**.

Mỗi thẻ **Decision Brief `D<N>`** bao gồm giải thích giản dị (**ELI10**), hậu quả nếu chọn sai (**Stakes**), điểm số độ hoàn thiện (**Completeness X/10**), thời gian thực hiện theo hai thang đo (**Con người làm thủ công** so với **AI Builder thực thi**) và phương án khuyến nghị. Nếu Con người chủ động chọn một phương án làm tắt có điểm `Completeness <= 7/10` để kịp tiến độ, quyết định đó tự động sinh ra một mục **Nợ Làm tắt (Shortcut Debt)** kèm điều kiện kích hoạt nâng cấp rõ ràng. Đọc thêm tại `references/plan-review-gates.md`.

### Bước 3 · VISION (Định hướng Kiến trúc, Vết Mở rộng Tiến hóa và 4-Lens Review)

Từ báo cáo Scan và RRI, Chủ thầu phác thảo tầm nhìn kỹ thuật gồm kiến trúc tổng thể, bộ công nghệ và định hướng giao diện.

Phiên bản v6.1 bổ sung hai công cụ sắc bén vào bước Vision.
- **Vết Mở rộng Tiến hóa (Evolutionary Extension Trace).** Để tránh cả hai thái cực là thiết kế quá cứng nhắc hoặc trừu tượng hóa quá đà (over-engineering), Chủ thầu chọn một biến thể thực tế tiếp theo có khả năng xảy ra cao nhất (ví dụ thêm cổng thanh toán thứ hai hoặc hỗ trợ thêm một định dạng xuất file) và thử dẫn nó qua kiến trúc đề xuất. Phần nào giữ nguyên được chính là giao diện ổn định (stable contract), phần nào phải sửa chính là vùng biến thiên cần cô lập. Những thứ chỉ là tưởng tượng xa xôi chưa có căn cứ thì kiên quyết cắt bỏ theo nguyên tắc YAGNI.
- **Chuỗi Duyệt 4 Lăng kính (Autoplan 4-Lens Sequential Gate).** Với tác vụ R2 và R3, Chủ thầu tự rà soát tầm nhìn theo đúng thứ tự bốn chiếc mũ. Đầu tiên là **Lăng kính CEO** để hỏi xem sản phẩm 10 sao nằm ở đâu và chọn chế độ mở rộng hay thu hẹp phạm vi. Thứ hai là **Lăng kính Design** (khi có giao diện) để chấm điểm bố cục, phân cấp thị giác và loại bỏ các mẫu giao diện rập khuôn kiểu AI (AI Slop). Thứ ba là **Lăng kính DX** (khi làm API, CLI hoặc thư viện) để tối ưu thời gian chạy thử lần đầu và thiết kế thông báo lỗi rõ ràng cho cả lập trình viên lẫn AI agent. Cuối cùng luôn là **Lăng kính Eng** để khóa chặt sơ đồ luồng dữ liệu, máy trạng thái, xử lý ngoại lệ và ma trận kiểm thử.

### Bước 4 · BLUEPRINT (Bản vẽ Khế ước và Cổng Phản biện Độc lập)

Blueprint là bản vẽ kỹ thuật chi tiết hóa Vision thành sơ đồ kiến trúc, danh sách module, cấu trúc bảng dữ liệu, cây thư mục và bảng ánh xạ từng yêu cầu `REQ-ID` vào thành phần code tương ứng.

Trước khi trình Con người phê duyệt ở các dự án R2 và R3, Blueprint phải đi qua **Cổng Phản biện Red-Team 4 góc nhìn** (tấn công vào Giả định ngầm, Kịch bản sập hệ thống, Nguy cơ phình phạm vi và Lỗ hổng bảo mật). Với những bài toán kiến trúc đặc biệt phức tạp hoặc gây tranh cãi, Chủ thầu có thể kích hoạt chế độ **Ultra Verifier (Best-of-5)** bằng cách đóng gói một bộ ngữ cảnh bất biến cho 5 luồng phân tích độc lập cùng đề xuất giải pháp, sau đó dùng mô hình mạnh nhất chấm chọn phương án vượt trội.

Khi Con người ký xác nhận **APPROVED**, Blueprint trở thành khế ước cứng. Mọi thay đổi kiến trúc phát sinh sau thời điểm này đều phải quay lại cập nhật từ bước Vision và duyệt lại.

### Bước 5 · TASK GRAPH (Đồ thị Gói Công việc TIP, Cô lập Worktree và Giao thức Dừng)

Chủ thầu chia nhỏ Blueprint thành một đồ thị các **TIP (Task Instruction Pack)** có thứ tự trước sau rõ ràng. Mỗi TIP là một đơn vị giao việc tự chứa gồm Header, Context, Task, Acceptance Criteria (viết theo chuẩn Gherkin hoặc lệnh kiểm tra cơ học), Scope Freeze và Failure Protocol.

Khi dự án có nhiều TIP có thể chạy song song cho nhiều Thợ, Chủ thầu bắt buộc tuân thủ hai nguyên tắc điều phối từ `ak-orchestrate`.
- **Quyền Sở hữu File Rời nhau (Disjoint File Ownership).** Không bao giờ giao hai TIP chạy cùng lúc có quyền sửa chung một file. Các file nền tảng dùng chung (như định nghĩa kiểu dữ liệu, cấu hình cơ sở dữ liệu, file điều hướng gốc) phải được hoàn thành ở TIP giai đoạn trước hoặc giao cho một Thợ duy nhất đảm nhận.
- **Cô lập bằng Không gian Git Worktree (Worktree Isolation).** Mỗi Thợ chạy song song làm việc trên một nhánh và một thư mục `git worktree` độc lập để quá trình biên dịch và chạy thử không làm hỏng cây thư mục của nhau.

Đặc biệt, khi sử dụng chế độ **Cố vấn Kongming (`--advice`)** hoặc giao việc cho các mô hình Thợ tốc độ cao, mỗi TIP đều nhúng sẵn **Giao thức Dừng khi Kiểm chứng Đỏ (Failure Protocol)**. Nếu lệnh kiểm tra thất bại và Thợ không thể giải quyết bằng nguyên nhân hiển nhiên trong vòng 3 lần thử, Thợ phải dừng ngay lập tức, giữ nguyên hiện trường và gửi báo cáo lỗi về cho Chủ thầu/Kongming phân tích thay vì tự ý sửa xóa liên tiếp.

### Bước 6 · BUILD (Thi công Khóa Phạm vi, Vòng lặp Ràng buộc và Handoff An toàn)

Thợ nhận TIP và tiến hành xây dựng sản phẩm trong ranh giới đã khóa. Bốn nguyên tắc thi công của Thợ ở v6.1 gồm.

1. **Khóa Phạm vi (Scope Freeze).** Chỉ tạo mới hoặc chỉnh sửa các file nằm trong danh sách cho phép của TIP. Nếu phát hiện lỗi hoặc code xấu ở thư mục khác, ghi vào phần `SUGGESTIONS` trong báo cáo, tuyệt đối không tiện tay sửa luôn.
2. **Bậc thang Tái sử dụng (Reuse Ladder).** Trước khi viết hàm mới hoặc cài thêm thư viện ngoài, luôn tìm kiếm theo thứ tự ưu tiên từ hàm tiện ích có sẵn trong dự án, thư viện chuẩn của ngôn ngữ, tính năng nguyên bản của nền tảng rồi mới tới các gói đã cài sẵn trong `package.json` hay `requirements.txt`.
3. **Vòng lặp Ràng buộc Cơ học (Constraint Loop).** Khi bài toán có các ràng buộc hình thức nghiêm ngặt (như chuẩn cấu trúc JSON/YAML, giới hạn độ dài, quy tắc văn phong hoặc không lộ khóa bí mật), Thợ không được chỉ đọc bằng mắt thường rồi kết luận đã đạt. Thợ phải tạo bản nháp, chạy lệnh hoặc script kiểm tra cơ học, sửa từng lỗi phát hiện được và chạy lại kiểm tra cho tới khi đạt 100%.
4. **Hợp đồng Bàn giao Chuyển tiếp 9 mục (Redacted Handoff Contract).** Khi một tác vụ kéo dài qua nhiều phiên làm việc hoặc cần chuyển từ Chủ thầu sang Thợ trên một công cụ khác, người bàn giao xuất một file Markdown chuẩn 9 mục tại `vibecode-artifacts/handoffs/` (hoặc `plans/handoffs/`), tự động quét và che toàn bộ thông tin nhạy cảm (`[REDACTED]`) và đánh dấu rõ bước hành động an toàn đầu tiên (`First safe step`).

Khi hoàn thành TIP, Thợ xuất `Completion Report` kèm theo **Dấu vân tay Cây thư mục (`WTREE_FINGERPRINT`)** và cấp độ bằng chứng thực tế đã chạy.

### Bước 7 · VERIFY (Nghiệm thu Bề mặt Thật, Kiểm toán Test và Trọng tài Độc lập)

Chủ thầu không bao giờ nghiệm thu chỉ bằng cách đọc lời tóm tắt của Thợ. Bước Verify kiểm tra ngược từng yêu cầu `REQ-ID` qua ba hàng rào.

- **Tính tươi mới của Bằng chứng (Evidence Freshness).** Kiểm tra xem `WTREE_FINGERPRINT` lúc chạy test có khớp với trạng thái file hiện tại trên đĩa hay không. Nếu có bất kỳ chỉnh sửa nào sau lần chạy test cuối, bằng chứng đó bị đánh dấu là `STALE` và bắt buộc phải chạy lại. Đồng thời kiểm tra đúng cấp độ bằng chứng (`static-read`, `unit-test`, `fixture-replay`, `live-run`, `production`), không chấp nhận việc dùng dữ liệu giả lập (mock) để thay thế cho bài kiểm tra tích hợp thật khi TIP yêu cầu `live-run`.
- **QA Nhận diện Bề mặt và Kiểm toán Test (Surface-Aware QA & Test Audit).** Kiểm tra trực tiếp trên bề mặt sản phẩm (mở trình duyệt thật kiểm tra giao diện và lỗi console đối với ứng dụng web, gọi request thật đối với API, chạy lệnh với tham số biên đối với CLI). Mọi lỗi tìm thấy phải được viết thành bài test tái hiện lỗi chạy đỏ trước khi sửa code cho xanh. Đồng thời rà soát để loại bỏ các bài test vô bổ không có câu lệnh khẳng định kết quả.
- **Trọng tài Độc lập Chấm chéo (Independent Arbiter Pass).** Với dự án R2 và R3, Chủ thầu mở một phiên Trọng tài độc lập không chia sẻ lịch sử trò chuyện của Thợ để đối chiếu mã nguồn, kết quả chạy test và Blueprint trước khi phê duyệt.

### Bước 8 · REFINE, DUAL-STAGE SHIP & CALIBRATION (Tinh chỉnh, Phát hành 2 Chặng và Hiệu chỉnh 100 điểm)

Những lỗi hoặc thiếu sót phát hiện ở bước Verify được đưa vào bước Refine để xử lý dứt điểm. Nếu phát sinh mong muốn thêm tính năng mới nằm ngoài Blueprint, Chủ thầu ghi nhận cho vòng lặp tiếp theo và quay về bước Vision chứ không nhồi nhét vào cuối chu kỳ hiện tại.

Khi sản phẩm đạt chuẩn nghiệm thu, quá trình phát hành và học hỏi diễn ra qua hai bước.
- **Phát hành Hai Chặng (Dual-Stage Ship `Beta -> Stable`).** Đối với các dự án có môi trường thử nghiệm và môi trường chính thức, code được hợp nhất và kiểm tra hội tụ CI xanh trên nhánh `beta/staging` trước. Chỉ khi nhánh thử nghiệm hoạt động ổn định và được xác nhận không cuốn theo các commit ngoài phạm vi, Chủ thầu mới trình Con người đẩy lên nhánh `stable/main`.
- **Thẻ Hiệu chỉnh 100 điểm (Calibration Card) và Thu hoạch Nợ Làm tắt (Shortcut Harvest).** Sau khi sản phẩm chạy thực tế, Chủ thầu lập `Calibration Card` để so sánh dự đoán ban đầu ở TIP với kết quả quan sát được. Nếu có độ lệch (Delta), Chủ thầu bắt buộc phân bổ đúng 100 điểm sai số vào 4 nguyên nhân gốc rễ gồm **Modeling** (hiểu sai bài toán hoặc thiết kế sai), **Timing** (phát hành sai thời điểm hoặc lệch nhịp phối hợp), **World-change** (môi trường, dữ liệu hoặc thư viện bên ngoài thay đổi) và **Execution** (thi công lỗi hoặc kiểm thử sót). Cùng lúc đó, toàn bộ các mục **Shortcut Debt** đã đánh dấu ở bước RRI và Build được gom lại để quyết định thời điểm nâng cấp ở chu kỳ kế tiếp.

## Tích hợp Liên hoàn Ba Bộ Phương pháp (Bộ 01 · Bộ 02 · Bộ 03)

Vibecode Kit v6.1 phát huy sức mạnh tối đa khi kết hợp cùng hai bộ phương pháp anh em trong kho `ai-native-methods`.

- Khi bước **SCAN / VISION** cần nghiên cứu thị trường, tìm hiểu công nghệ mới hoặc phân tích đối thủ cạnh tranh từ internet, Chủ thầu kích hoạt **Bộ 01 (Tinh lọc và làm giàu thông tin từ internet)** để thu về các thẻ sự thật (`Fact Cards`) đã được phân hạng tin cậy (`Verified`, `Probable`, `Unverified`) và xử lý xung đột rõ ràng.
- Khi dự án cần sử dụng các con số định mức, bảng giá, công thức tính toán, quy định pháp lý hoặc giọng văn thương hiệu, Chủ thầu và Thợ tham chiếu trực tiếp vào **Bộ 02 (Kernel Registry SOT)** theo đúng bốn xuất xứ `L1` (sự thật lưu sẵn), `L2` (sự thật dẫn xuất), `L3` (nghĩa vụ pháp quy) và `L4` (phong cách tự do) thông qua mã định danh ID thay vì viết cứng vào code hay prompt.

## Mười nguyên tắc cốt lõi của Vibecode Kit v6.1

1. **Tin AI, kiểm chứng đầu ra bằng bằng chứng tươi.** Không kiểm soát luồng suy nghĩ nội tâm của AI, nhưng mọi tuyên bố hoàn thành phải đi kèm kết quả chạy kiểm tra gắn với dấu vân tay mã nguồn hiện tại.
2. **Chủ thầu không viết code sản phẩm.** Ranh giới cứng tuyệt đối để người thiết kế và nghiệm thu không bị cuốn vào việc tự bảo vệ code của chính mình.
3. **Kỷ luật Nhận định rõ ràng.** Luôn phân biệt điều đã tận mắt đo đạc (`OBSERVED`), điều suy luận (`DERIVED`), kiến thức cũ (`PRIOR`) và giả định (`ASSUMED`).
4. **Đề xuất trước, hỏi sau qua thẻ quyết định `D<N>`.** Tự khai thác mã nguồn để trả lời các câu hỏi cơ học, chỉ hỏi Con người ở những quyết định chiến lược kèm điểm `Completeness X/10`.
5. **Blueprint là khế ước bất biến.** Đã duyệt kiến trúc thì giữ nguyên trong suốt pha thi công. Muốn đổi kiến trúc phải quay lại Vision.
6. **Không sửa mò khi chưa rõ nguyên nhân gốc.** Quá 3 lần thử sửa lỗi thất bại liên tiếp phải dừng lại ngay để phân tích lại từ đầu hoặc tham vấn Quân sư Kongming.
7. **Cô lập không gian và khóa phạm vi khi thi công.** Mỗi Thợ giữ đúng `Scope Freeze` và sở hữu tập file rời nhau trên các `git worktree` riêng biệt khi chạy song song.
8. **Chấm chéo độc lập trước khi phát hành.** Ở các tác vụ quan trọng, người kiểm tra nghiệm thu phải là một phiên Trọng tài độc lập với phiên Thợ vừa viết code.
9. **Mọi đường tắt đều phải để lại dấu vết.** Chọn phương án rút gọn (`Completeness <= 7/10`) là hợp lệ khi cần tốc độ, nhưng bắt buộc ghi nhận điều kiện nâng cấp vào sổ nợ kỹ thuật.
10. **Dự đoán trước khi làm, hiệu chỉnh 100 điểm sau khi chạy thật.** Không có chu kỳ nào thực sự kết thúc nếu thiếu thẻ Calibration Card để cả Con người và hệ thống AI khôn lên ở vòng sau.

---

**Vibecode Kit v6.1** · Nguyên tác v6.0 bởi Nguyễn Cảnh Lâm · Nâng cấp v6.1 tích hợp tinh hoa từ gstack & AgentKit.
