# Bộ 03 · Vibecode Kit v6.1

**Phiên bản 2026.10 (v6.1)**

Khung phương pháp luận và điều phối kỹ thuật để xây dựng sản phẩm phần mềm hoặc giải pháp số bằng cách phối hợp đội ngũ AI agent thay vì viết code thủ công từng dòng. Giữ vững nền tảng ba vai trò rõ ràng và quy trình 8 bước tự co giãn của v6.0, phiên bản v6.1 tích hợp thêm các cơ chế kiểm soát chất lượng thực chiến mới nhất từ **gstack (v1.91)** và **AgentKit / akkit (v2.x–4.x)**.

## Khi nào dùng

Sinh viên, nhà nghiên cứu, nhóm khởi nghiệp hoặc tổ chức muốn xây dựng phần mềm có chất lượng kiểm chứng được trong các tình huống.

Đồ án tốt nghiệp hoặc luận văn thạc sĩ có sản phẩm phần mềm chạy thật. Dự án nghiên cứu tại phòng thí nghiệm cần đóng gói thành công cụ web, mobile, API hoặc CLI. Nhóm khởi nghiệp muốn xây dựng và phát hành sản phẩm khả dụng tối thiểu (MVP) tốc độ cao nhưng không rơi vào bẫy "code rác do AI sinh tự phát". Kỹ sư và quản lý kỹ thuật muốn điều phối nhiều phiên AI chạy song song an toàn trên cùng một kho mã nguồn.

## Khi nào không dùng

Khi hệ thống yêu cầu chứng chỉ an toàn sinh mạng hoặc tài chính cấp độ đặc biệt nghiêm ngặt (hàng không, thiết bị y tế cấy ghép, lõi ngân hàng) mà chưa có đội ngũ kỹ sư chuyên gia thẩm định độc lập. Khi mục tiêu duy nhất của người học là tự tay gõ từng dòng lệnh để rèn luyện cú pháp cơ bản của một ngôn ngữ lập trình mới.

## Tám đặc điểm cốt lõi của phiên bản v6.1

Khác biệt hoàn toàn với cách "dán yêu cầu mơ hồ vào khung chat để AI tự viết code" ở tám cơ chế.

Một, **ba vai trò chính cộng một lớp cố vấn/trọng tài độc lập** (Con người làm Chủ nhà, AI điều phối làm Chủ thầu, AI viết code làm Thợ thi công, cùng Quân sư Kongming và Trọng tài Arbiter chấm chéo). Tuyệt đối không lẫn vai.

Hai, **quy trình 8 bước tự co giãn theo phân tầng rủi ro từ R0 đến R3**. Tác vụ 5 phút chạy gọn trong 5 phút, tác vụ lớn tự động bật đầy đủ các cổng bảo vệ.

Ba, **kỷ luật nhận định và sổ cái bằng chứng gắn dấu vân tay mã nguồn** (`Fable 5.1 Claim Discipline` + `Working-Tree Fingerprint`). Chặn đứng tình trạng AI tự báo cáo "đã chạy xanh" nhưng thực tế chưa chạy hoặc đã sửa code sau khi chạy kiểm thử.

Bốn, **phỏng vấn ngược thông minh bằng thẻ quyết định `D<N>` và sổ nợ làm tắt (`Shortcut Debt`)**. Phân loại quyết định thành `Mechanical`, `Taste` và `User Challenge`. Mỗi lựa chọn trình cho Con người đều có điểm độ phủ `Completeness X/10` và điều kiện nâng cấp rõ ràng nếu chọn phương án làm tắt.

Năm, **duyệt kế hoạch qua 4 lăng kính (`CEO -> Design -> DX -> Eng`) và phản biện Red-Team 4 góc nhìn**. Khoanh vùng kiến trúc bằng vết mở rộng tiến hóa (`Evolutionary Extension Trace`) trước khi viết dòng code đầu tiên.

Sáu, **điều phối đa Thợ song song không giẫm chân nhau**. Áp dụng quy tắc sở hữu file rời nhau (`Disjoint File Ownership`), cô lập bằng `git worktree`, khóa phạm vi sửa đổi (`Scope Freeze`) và bàn giao chuyển phiên bằng hợp đồng 9 mục đã che mật khẩu (`Redacted Handoff`).

Bảy, **kiểm thử bề mặt thật và luật dừng sau 3 lần thất bại (`3-Strike Stop`)**. Mọi lỗi tìm thấy ở bước QA phải có bài kiểm thử tái hiện lỗi chạy đỏ trước khi sửa xanh. Thợ gặp lỗi kiểm chứng quá 3 lần phải dừng ngay và báo cáo lên Chủ thầu/Kongming.

Tám, **phát hành hai chặng (`Beta -> Stable`) gắn liền với thẻ hiệu chỉnh 100 điểm (`Calibration Card`)**. Dự đoán trước khi giao việc, đo đạc thực tế sau khi phát hành và phân bổ 100 điểm sai số để hệ thống ngày càng chính xác qua từng vòng lặp.

## Cấu trúc thư mục

```
Bo-03-Vibecode-Kit-v6/
├── README.md                              Tổng quan phương pháp và cấu trúc Bộ 03 (file này)
├── Methodology.md                         Triết lý 3+1 vai trò, phân tầng R0-R3 và 8 bước v6.1
├── Architecture.md                        Kiến trúc kỹ thuật, Fingerprint Ledger, Worktree & Handoff
├── SKILL.md                               Đặc tả skill để cài đặt vào Claude, Antigravity, Cursor
├── Quick-Start.md                         Hướng dẫn thực hành trọn 1 chu kỳ v6.1 trong 20 phút
├── templates/                             Bộ 8 bản mẫu sẵn dùng cho dự án
│   ├── TIP-template.md                    Gói giao việc (kèm Scope Freeze & Failure Protocol)
│   ├── Blueprint-template.md              Bản vẽ kiến trúc (kèm Extension Trace & 4-Lens Gate)
│   ├── RRI-template.md                    Biên bản phỏng vấn ngược & Thẻ quyết định D<N>
│   ├── Completion-Report.md               Báo cáo hoàn thành (kèm WTREE_FINGERPRINT & Evidence)
│   ├── Handoff-Contract.md                Hợp đồng bàn giao chuyển phiên 9 mục có Redaction
│   ├── Calibration-Card.md                Thẻ hiệu chỉnh 100 điểm & Thu hoạch Shortcut Debt
│   ├── Risk-Tier-Classification.md        Ma trận phân tầng rủi ro R0-R3 & Định tuyến mô hình
│   └── Audit-Trail-Loop.md                Mẫu sổ cái kiểm toán, bằng chứng và nợ kỹ thuật
├── references/                            Tài liệu chuyên sâu nạp theo ngữ cảnh
│   ├── claim-and-evidence-protocol.md     Fable 5.1 Claim Discipline, Constraint Loop & Evidence
│   ├── orchestrate-and-handoff.md         Điều phối đa Thợ Worktree, Kongming, Arbiter & Handoff
│   ├── plan-review-gates.md               Decision Briefs, 4-Lens Gate, Red-Team & Ultra Best-of-5
│   ├── qa-and-debug-protocol.md           Surface QA, Red-Before-Green, Test Audit & Debug Gốc rễ
│   ├── ship-and-calibration.md            Dual-Stage Ship (Beta->Stable) & Calibration 100 điểm
│   └── xray-and-scan-protocol.md          Giao thức quét SCAN và giải phẫu dự án X-Ray
└── examples/
    └── worked-example.md                  Ví dụ thực chiến từ đầu đến cuối một dự án R2
```

## Bắt đầu nhanh

1. Đọc `Quick-Start.md` để chạy thử chu kỳ Vibecode v6.1 đầu tiên trên một bài toán nhỏ trong 20 phút.
2. Đọc `Methodology.md` để nắm vững tư duy phân vai, phân loại quyết định `D<N>` và tám bước co giãn.
3. Đọc `Architecture.md` và thư mục `references/` khi cần triển khai dự án quy mô lớn, chạy nhiều Thợ song song hoặc thiết lập cổng kiểm chứng tự động.
4. Xem `examples/worked-example.md` để quan sát cách toàn bộ các hiện vật (`SCAN`, `RRI`, `Blueprint`, `TIP`, `Handoff`, `Completion Report`, `Calibration Card`) liên kết với nhau trong thực tế.

## Lịch sử tiến hóa

Phiên bản v6.0 đặt nền móng cho mô hình Chủ thầu · Thợ · Chủ nhà với triết lý kiểm chứng đầu ra thay vì kiểm soát đường đi. Phiên bản **v6.1 (2026.10)** hoàn thiện toàn bộ hệ thống bản mẫu và giao thức mở rộng, đồng thời kết tinh những bài học thực chiến đắt giá nhất từ hai bộ công cụ `gstack` và `AgentKit (akkit)` để phục vụ cả cá nhân làm dự án độc lập lẫn tổ chức điều phối đội ngũ AI quy mô lớn.
