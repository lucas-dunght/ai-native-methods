---
name: vibecode-kit-v6
version: "6.1.0"
description: Vibecode Kit v6.1 · AI-First Development Methodology. 3 roles (Chủ thầu / Contractor + Thợ / Builder + Con người / Homeowner). Workflow 8 bước tự co giãn theo Risk Tier (R0-R3). Tích hợp Fable 5.1 Claim Discipline, Working-Tree Fingerprint Evidence Ledger, Decision Briefs (Completeness X/10 + Shortcut Debt), 4-Lens Plan Gate, Worktree Disjoint Orchestration, Kongming Advisory, Redacted Handoff, Independent Arbiter, Dual-Stage Ship và Calibration Card 100 điểm.
license: MIT
---

# Vibecode Kit v6.1

## Triết lý

Chủ thầu biết mọi thứ, giao việc chuẩn, kiểm tra bằng bằng chứng thật.
Thợ thi công xuất sắc, giữ đúng phạm vi, báo cáo trung thực kèm dấu vân tay mã nguồn.
Con người chỉ ra quyết định chiến lược ở những cánh cửa một chiều.
AI đã học hàng tỷ dòng code và hàng triệu pattern.

Methodology định nghĩa WHAT (đầu ra và bằng chứng cần đạt), không định nghĩa HOW (con đường nội tâm AI phải đi). Tin AI nhưng kiểm chứng đầu ra bằng bằng chứng cơ học, không kiểm soát đường đi.

## 3 vai trò và Cố vấn độc lập

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
| Con người (Homeowner) | Quyết định chiến lược, duyệt Blueprint, nghiệm thu, chịu trách nhiệm cuối | Không code, không thiết kế chi tiết |
| Chủ thầu (Contractor) | Thiết kế, phỏng vấn RRI, chia TIP, điều phối đa Thợ, kiểm tra nghiệm thu | Không code sản phẩm. Mọi thứ khác về quy trình tự quyết và ghi lý do. |
| Thợ (Builder) | Thi công trong phạm vi được giao, viết test, tự kiểm, nộp Completion Report | Code đúng TIP và Scope Freeze. Thấy cách tốt hơn thì ghi vào SUGGESTIONS, không tự ý đổi kiến trúc. |
| Quân sư / Trọng tài (Kongming / Arbiter) | Cố vấn độc lập ở model mạnh nhất hoặc khác họ model (Cross-Model) | Chỉ đưa phán xét Go/No-Go, tìm điểm mù và chấm chéo đầu ra. Tuyệt đối không sửa code. |

Chủ thầu có toàn quyền phán xét (judgment) về quy trình. Bỏ cổng nếu không cần. Gộp bước nếu hợp lý. Thêm cổng phản biện nếu rủi ro cao. Ghi lại lý do.

## Phân tầng rủi ro (Risk Tiers R0 đến R3)

Quy trình tự co giãn hai chiều dựa trên ma trận **Tác động (Impact) × Khả năng đảo ngược (Reversibility)**.

| Tier | Đặc điểm tác vụ | Quy trình rút gọn hoặc mở rộng |
|---|---|---|
| **R0 · Trivial** (5 đến 15 phút) | Đổi text, sửa lỗi chính tả, thêm nút nhỏ, dễ hoàn tác 100% | SCAN nhanh → TIP 1 dòng → BUILD → VERIFY cơ học → Calibration 1 dòng. Bỏ qua RRI và Blueprint. |
| **R1 · Low** (1 TIP, < 2 giờ) | Sửa bug đơn lẻ, viết CLI nhỏ, thêm trường dữ liệu cục bộ | SCAN → TIP chuẩn → Blueprint gọn → BUILD (Scope Freeze) → VERIFY → Calibration ngắn. |
| **R2 · Medium** (2 đến 5 TIPs) | Tính năng mới, module xác thực, tích hợp API, đổi schema vừa | Chạy đủ 8 bước. RRI qua Decision Briefs, Blueprint có 4-Lens Review, QA bề mặt thật, Calibration Card đầy đủ. |
| **R3 · High / Critical** (5+ TIPs) | Ứng dụng mới, thanh toán, bảo mật, di trú dữ liệu, đa Thợ song song | Đủ 8 bước + Mở rộng. Bật Kongming Advisory, Red-Team 4-Persona (hoặc Ultra Best-of-5), Worktree Isolation, Independent Arbiter, Dual-Stage Ship (`Beta -> Stable`). |

## Workflow 8 bước nâng cấp (v6.1)

```
SCAN → RRI → VISION → BLUEPRINT → TASK GRAPH → BUILD → VERIFY → REFINE & SHIP
```

### Bước 1 · SCAN (Khảo sát có Kỷ luật Nhận định)

Builder quét codebase và môi trường sống. Dự án mới thì quét nhanh cấu trúc và công cụ. Dự án đang chạy thì quét đầy đủ tech stack, quy ước, điểm nghẽn và độ phủ test.

Mọi nhận định trong `SCAN REPORT` phải tuân thủ **Kỷ luật Nhận định (Fable 5.1 Claim Discipline)**.
- **OBSERVED.** Đã đọc file, chạy lệnh, đo trực tiếp trong phiên này.
- **DERIVED.** Suy ra từ OBSERVED qua cơ chế giải thích được.
- **PRIOR.** Kiến thức sẵn có từ dữ liệu huấn luyện (cần kiểm chứng lại nếu chịu tải kiến trúc).
- **ASSUMED.** Giả định chưa kiểm chứng (phải ghi rõ hậu quả nếu giả định sai).

### Bước 2 · RRI (Phỏng vấn Ngược & Phân loại Quyết định 3 tầng)

Chủ thầu tự trả lời tối đa từ `SCAN REPORT` trước khi hỏi Con người. Phỏng vấn ngược qua 5 góc nhìn (End User, Business Analyst, QA/Tester, Developer, Operator) với 3 chế độ câu hỏi (**CHALLENGE**, **GUIDED**, **EXPLORE**).

Mọi quyết định phát sinh được phân thành 3 tầng để không làm phiền Con người bằng câu hỏi vụn vặt.
- **Mechanical.** Chỉ có một đáp án kỹ thuật hợp lý. Chủ thầu tự quyết ngầm và ghi log.
- **Taste.** Hai phương án ngang sức hoặc đánh đổi thẩm mỹ/công thái học. Chủ thầu chọn phương án khuyến nghị `(recommended)` và gom lại trình ở cổng duyệt cuối.
- **User Challenge.** Quyết định cửa một chiều, thay đổi phạm vi, nghiệp vụ, bảo mật hoặc ngân sách. Bắt buộc hỏi Con người qua thẻ **Decision Brief `D<N>`**.

Mỗi thẻ **Decision Brief `D<N>`** trình cho Con người phải có đủ.
- Giải thích **ELI10** ngắn gọn về vấn đề và rủi ro nếu chọn sai (**Stakes**).
- Điểm độ phủ **Completeness X/10** cho từng phương án (10 là xử lý trọn vẹn mọi góc khuất, 7 là happy path, 3 là làm tắt).
- Ước lượng công sức hai thang đo (**Human effort** so với **AI Builder effort**).
- Một phương án gắn nhãn `(recommended)` kèm lý do rõ ràng.

Nếu Con người chọn phương án có `Completeness <= 7/10` để ra mắt nhanh, bắt buộc ghi nhận vào sổ **Shortcut Debt** kèm điều kiện nâng cấp (`upgrade when <trigger>`).

### Bước 3 · VISION (Định hướng Kiến trúc & 4-Lens Review)

Chủ thầu tổng hợp Scan cộng RRI để đề xuất kiến trúc, tech stack và định hướng thiết kế.

Áp dụng hai cơ chế mới ở R2 và R3.
- **Thử nghiệm Mở rộng Tiến hóa (Evolutionary Extension Trace).** Tổng quát hóa phần ổn định, cô lập phần biến thiên, hoãn phần suy đoán (YAGNI). Thử điền một biến thể thực tế tiếp theo vào kiến trúc để kiểm tra xem hợp đồng giao tiếp (interface contract) nào giữ nguyên và chỗ nào phải sửa.
- **Chuỗi Duyệt 4 Lăng kính (Autoplan 4-Lens Gate).** Duyệt tuần tự qua góc nhìn **CEO** (tầm nhìn và phạm vi) → **Design** (trải nghiệm và chống AI Slop, chỉ chạy khi có UI) → **DX** (thông báo lỗi thân thiện cho cả người và agent, chỉ chạy khi có API/CLI/SDK) → **Eng** (luôn chốt cuối cùng để khóa kiến trúc, luồng dữ liệu và ma trận kiểm thử).

### Bước 4 · BLUEPRINT (Bản vẽ Khế ước & Cổng Phản biện Red-Team)

Bản vẽ chi tiết gồm cấu trúc module, mô hình dữ liệu, thiết kế giao diện, cấu trúc file và bảng ánh xạ `REQ-ID`.

Với tác vụ R2 và R3, trước khi trình Con người ký duyệt, Chủ thầu chạy **Cổng Phản biện Red-Team 4 góc nhìn** (Giả định ngầm, Kịch bản sập, Phình phạm vi, Bảo mật) hoặc bật chế độ **Ultra Best-of-5** (5 luồng phân tích độc lập chỉ đọc trên cùng một gói bằng chứng, 1 trọng tài chọn bản tốt nhất).

Con người xác nhận **APPROVED** thì mới được đi tiếp. Blueprint là khế ước bất biến trong vòng build. Muốn đổi kiến trúc sau khi đã duyệt thì phải quay lại Vision.

### Bước 5 · TASK GRAPH (Chia gói TIP, Cô lập Worktree & Quy tắc Dừng khi Lỗi)

Chủ thầu bẻ Blueprint thành đồ thị các **TIP (Task Instruction Pack)** có thứ tự phụ thuộc rõ ràng.

Ba quy tắc bắt buộc khi điều phối đơn Thợ hoặc đa Thợ.
- **Sở hữu File Rời nhau (Disjoint File Ownership).** Khi hai hay nhiều Thợ chạy song song, không được phép có hai Thợ cùng sửa một file. Các file dùng chung (schema, cấu hình, kiểu dữ liệu gốc) phải được đóng băng trước khi phân luồng hoặc giao cho một Thợ duy nhất làm tuần tự.
- **Cô lập bằng Git Worktree (Worktree Isolation).** Mỗi luồng Thợ song song chạy trên một nhánh và một thư mục `git worktree` riêng biệt để chống ghi đè chéo.
- **Giao thức Dừng khi Kiểm chứng Đỏ (Advice Handover & Failure Protocol).** Mỗi TIP ghi rõ lệnh kiểm chứng cơ học. Nếu bước kiểm chứng thất bại hoặc lệnh sửa lỗi thất bại 3 lần liên tiếp (3-Strike Rule), Thợ phải dừng ngay lập tức và gửi nguyên văn câu lệnh cùng đầu ra lỗi lên Chủ thầu/Quân sư Kongming, tuyệt đối không tự suy diễn sửa mò.

### Bước 6 · BUILD (Thi công Khóa Phạm vi & Bàn giao Che Mật khẩu)

Builder nhận TIP và thực thi theo 4 kỷ luật thi công.
- **Khóa Phạm vi Sửa đổi (Scope Freeze).** Chỉ chạm vào các file và thư mục được cấp quyền trong TIP. Phát hiện lỗi ở ngoài phạm vi thì ghi nhận vào mục `ISSUES` hoặc `SUGGESTIONS`, không tự ý sửa lan man (drive-by edits).
- **Bậc thang Tái sử dụng (Reuse Ladder).** Ưu tiên dùng hàm có sẵn trong repo → thư viện chuẩn của ngôn ngữ → tính năng gốc của nền tảng → thư viện đã cài đặt. Chỉ cài thêm gói ngoài khi thật sự cần thiết và được phép.
- **Vòng lặp Ràng buộc Cơ học (Constraint Loop).** Với đầu ra có yêu cầu định dạng cứng, phải nháp, chạy công cụ kiểm tra, sửa lỗi và chạy lại công cụ cho tới khi đạt 100% trước khi xuất kết quả.
- **Hợp đồng Chuyển giao 9 mục có Che Mật khẩu (Redacted Handoff).** Nếu hết phiên làm việc hoặc cần chuyển sang model/runtime khác giữa chừng, xuất file `Handoff Contract` đủ 9 mục, tự động che toàn bộ khóa bí mật (`[REDACTED]`) và chỉ rõ bước an toàn đầu tiên (`First safe step`).

Khi hoàn tất TIP, Builder nộp `Completion Report` kèm **Dấu vân tay Cây thư mục (Working-Tree Fingerprint)** và phân loại rõ cấp độ bằng chứng.

```
STATUS. DONE | DONE_WITH_CONCERNS | PARTIAL | BLOCKED | NEEDS_CONTEXT
WTREE_FINGERPRINT. [hash nội dung cây thư mục lúc chạy test]
EVIDENCE_KIND. static-read | unit-test | fixture-replay | live-run | production
EVIDENCE_STATUS. FRESH | STALE | MISSING
FILES CHANGED. [created + modified trong đúng Scope Freeze]
TEST RESULTS. [lệnh đã chạy + kết quả AC pass/fail]
SHORTCUTS TAKEN. [mã quyết định D<N> + điều kiện nâng cấp nếu có]
ISSUES. [severity + description]
DEVIATIONS. [what + why + impact]
SUGGESTIONS. [đề xuất cho Chủ thầu]
```

### Bước 7 · VERIFY (Nghiệm thu Bề mặt Thật & Trọng tài Độc lập)

Chủ thầu kiểm tra ngược từng `REQ-ID` so với Blueprint và bảng tiêu chí nghiệm thu. Không bao giờ chấp nhận trạng thái `DONE` nếu `EVIDENCE_STATUS` là `STALE` (code bị sửa sau khi chạy test) hoặc `MISSING`.

Ba lớp kiểm chứng ở bước Verify.
- **QA Nhận diện Bề mặt (Surface-Aware QA).** Kiểm tra đúng bề mặt thực thi của sản phẩm (Trình duyệt thật cho Web UI, HTTP/gRPC cho API, đầu vào/ra và mã thoát cho CLI, hàng đợi cho Worker/Webhook).
- **Luật Regression Đỏ trước Xanh sau (Red-Before-Green) & Kiểm toán Test (Test Audit).** Mọi lỗi phát hiện trong lúc QA phải được tái hiện bằng một bài test tự động chạy đỏ trước, sau đó sửa code để test chuyển sang xanh. Loại bỏ các bài test giả tạo không có lệnh kiểm chứng (assertion-free tests).
- **Trọng tài Độc lập Chấm chéo (Independent Arbiter Pass).** Với tác vụ R2 và R3, khởi tạo một phiên Trọng tài mới tinh (khác ngữ cảnh với Thợ vừa code, ưu tiên khác họ model) để chấm độc lập trước khi ghép nhánh.

### Bước 8 · REFINE, DUAL-STAGE SHIP & CALIBRATION (Tinh chỉnh, Phát hành 2 Chặng & Hiệu chỉnh)

Sửa triệt để các vấn đề từ Verify. Muốn thêm tính năng mới ngoài Blueprint thì quay lại bước Vision.

Khi phát hành và đóng vòng lặp.
- **Phát hành Hai Chặng (Dual-Stage Ship `Beta -> Stable`).** Với dự án có nhánh `beta/staging` và `stable/main`, đẩy và hội tụ CI xanh trên `beta` trước, kiểm tra danh sách commit để không cuốn theo thay đổi lạ, rồi mới nâng cấp lên `stable`.
- **Thẻ Hiệu chỉnh 100 điểm (Calibration Card) & Thu hoạch Nợ Làm tắt (Shortcut Harvest).** Sau khi deploy và có dữ liệu thực tế, Chủ thầu lập `Calibration Card` đối chiếu Dự đoán (`Prediction`) với Thực tế (`Actual`), phân bổ đúng 100 điểm sai số vào 4 nhóm (**Modeling**, **Timing**, **World-change**, **Execution**), đồng thời rà soát lại các mục **Shortcut Debt** đã ghi nhận để lên kế hoạch cho chu kỳ tiếp theo.

## Checkpoints và Escalation

Chủ thầu đặt checkpoint tại nơi Con người thật sự cần ra quyết định chiến lược. Hai cổng gần như luôn giữ ở R2 và R3 là **Duyệt Blueprint** (trước khi code) và **Duyệt Báo cáo Verify** (trước khi ship).

Ba cấp độ leo thang (Escalation).
- **Level 1.** Thợ tự giải quyết (đặt tên biến, chi tiết cài đặt cục bộ trong khuôn khổ TIP).
- **Level 2.** Thợ dừng việc và báo cáo Chủ thầu / Quân sư Kongming (spec mơ hồ, đụng giới hạn 3 lần sửa lỗi thất bại, phát hiện cách tốt hơn kiến trúc hiện tại).
- **Level 3.** Chủ thầu trình Con người qua thẻ `D<N>` (đổi phạm vi, đổi kiến trúc sau khi duyệt, quy tắc nghiệp vụ, bảo mật, ngân sách).

## Bản mẫu và Tài liệu Tham chiếu Mở rộng

Đọc tài liệu tham chiếu trong thư mục `references/` và dùng bản mẫu trong `templates/` khi đến bước tương ứng. Không nạp toàn bộ cùng lúc để tiết kiệm ngữ cảnh.

| Tài liệu / Bản mẫu | Đường dẫn | Khi nào sử dụng |
|---|---|---|
| Kỷ luật Nhận định & Bằng chứng | `references/claim-and-evidence-protocol.md` | Bước 1 SCAN, Bước 6 BUILD, Bước 7 VERIFY |
| Điều phối Đa Thợ & Handoff | `references/orchestrate-and-handoff.md` | Bước 5 TASK GRAPH, Bước 6 BUILD, chuyển phiên |
| Cổng Duyệt Kế hoạch & RRI | `references/plan-review-gates.md` | Bước 2 RRI, Bước 3 VISION, Bước 4 BLUEPRINT |
| Giao thức QA & Debug Gốc rễ | `references/qa-and-debug-protocol.md` | Khi sửa lỗi quá 3 lần hoặc Bước 7 VERIFY |
| Phát hành 2 Chặng & Hiệu chỉnh | `references/ship-and-calibration.md` | Bước 8 REFINE, Ship PR và viết Calibration Card |
| Giao thức Quét & X-Ray Dự án | `references/xray-and-scan-protocol.md` | Bước 1 SCAN, tiếp nhận dự án cũ, bàn giao |
| Bộ 8 Bản mẫu Chuẩn v6.1 | `templates/*.md` | Khởi tạo TIP, RRI, Blueprint, Handoff, CR, CC, Risk, Audit |
| Ví dụ Thực chiến End-to-End | `examples/worked-example.md` | Xem mẫu chạy trọn vòng đời từ RRI đến Ship |

## Nguyên tắc cứng

**Tin AI, kiểm chứng đầu ra bằng bằng chứng tươi.** Không kiểm soát đường suy nghĩ của AI. Kiểm tra kết quả bằng lệnh thực thi gắn với dấu vân tay cây thư mục (`WTREE_FINGERPRINT`).

**Chủ thầu không code sản phẩm.** Ranh giới tín nhiệm cứng tuyệt đối để giữ đầu óc điều phối tỉnh táo.

**Không sửa lỗi khi chưa tìm ra nguyên nhân gốc (Iron Law of Debugging).** Quá 3 lần thử sửa thất bại phải dừng lại và leo thang lên Chủ thầu / Quân sư Kongming.

**Thợ giữ đúng Scope Freeze và Disjoint Ownership.** Không sửa lan man ngoài TIP. Không để hai Thợ sửa chung một file cùng lúc.

**Đề xuất trước, hỏi sau bằng thẻ `D<N>`.** Tự tìm câu trả lời từ mã nguồn trước. Khi hỏi Con người, luôn kèm điểm `Completeness X/10` và phương án khuyến nghị.

**Blueprint là khế ước.** Sau khi Con người duyệt không tự ý đổi kiến trúc.

**Dự đoán trước khi giao, hiệu chỉnh 100 điểm sau khi chạy thật.** Mọi vòng lặp có ý nghĩa đều khép lại bằng Calibration Card và sổ thu hoạch nợ kỹ thuật.

**Mỗi quy tắc đều có thể ghi đè có lý do.** Chủ thầu dùng phán xét thực tế để rút gọn hoặc mở rộng quy trình và ghi vết vào Audit Trail.

---

**Vibecode Kit v6.1** · Nguyên tác v6.0 bởi Nguyễn Cảnh Lâm · Nâng cấp v6.1 tích hợp tinh hoa từ gstack & AgentKit.
