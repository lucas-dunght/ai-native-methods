# Ví dụ Thực chiến End-to-End · Xây dựng Hệ thống Quản lý Đăng ký Đề tài bằng Vibecode Kit v6.1

Tài liệu này minh họa toàn bộ vòng đời 8 bước của **Vibecode Kit v6.1** trên một dự án thực tế ở phân tầng rủi ro **R2 (Medium Risk)**, cho thấy cách Con người (Chủ nhà), Chủ thầu (Contractor), hai Thợ thi công song song (Builders) và Trọng tài độc lập (Arbiter) phối hợp nhịp nhàng qua các hiện vật chuẩn.

---

## Bối cảnh bài toán

Một bộ môn đại học cần xây dựng module **Đăng ký và Phân công Đề tài Đồ án** tích hợp vào cổng thông tin nội bộ hiện có (dùng Node.js, TypeScript, SQLite và giao diện Web). Sinh viên gửi nguyện vọng đăng ký đề tài, giảng viên duyệt nhận hướng dẫn và hệ thống tự động chặn việc đăng ký vượt chỉ tiêu tối đa của từng giảng viên.

---

## Bước 1 · SCAN (Khảo sát Hiện trạng kèm Kỷ luật Nhận định)

Thợ thi công quét kho mã nguồn hiện tại và xuất file `vibecode-artifacts/scan-reports/SCAN-001.md`.

```markdown
# SCAN-001 · Khảo sát Cổng thông tin Bộ môn

**Date.** 2026-10-25
**WTREE_FINGERPRINT.** `7a11b09e4c82d105`

## 1. Hiện trạng kỹ thuật
- **OBSERVED.** Dự án đang dùng TypeScript 5.x, Express và cơ sở dữ liệu SQLite (`better-sqlite3`) tại `src/db/connection.ts`.
- **OBSERVED.** Đã có sẵn bảng `users` (phân vai `student`, `lecturer`, `admin`) và middleware xác thực phiên tại `src/middleware/auth.ts`.
- **OBSERVED.** Bộ kiểm thử hiện tại dùng `vitest` (`npm test` chạy xanh 18/18 bài trong 0.4 giây).
- **DERIVED.** Vì `better-sqlite3` thực thi đồng bộ trên một tiến trình, có thể dùng giao dịch (`db.transaction(...)`) để khóa chặt việc kiểm tra chỉ tiêu giảng viên mà không sợ lỗi tranh chấp đồng thời (race condition).

## 2. Khoảng trống và Phân tầng rủi ro
- **ASSUMED.** Mỗi giảng viên có hạn mức hướng dẫn tối đa mặc định (cần đối chiếu Kernel Registry Bộ 02 hoặc hỏi Chủ nhà ở bước RRI).
- **DERIVED.** Tính năng tác động tới toàn bộ sinh viên và giảng viên trong đợt đăng ký nhưng có thể hoàn tác qua bảng đăng ký nên xếp ở mức **R2 (Medium Risk)**.
```

---

## Bước 2 · RRI (Phỏng vấn Ngược và Thẻ Quyết định `D<N>`)

Chủ thầu đọc `SCAN-001.md`, tự giải các câu hỏi kỹ thuật cơ học (như tái sử dụng `src/middleware/auth.ts` và dùng `db.transaction`), sau đó lập `vibecode-artifacts/RRI-logs/RRI-001.md` trình Chủ nhà đúng 2 quyết định quan trọng.

```markdown
# RRI-001 · Phỏng vấn Ngược Module Đăng ký Đề tài

## 1. Quyết định Tầng 1 · Mechanical (Chủ thầu tự quyết)
- **M01.** Dùng `db.transaction` của SQLite khi giảng viên bấm Duyệt để kiểm tra số lượng đề tài đã nhận và cập nhật trạng thái trong cùng một giao dịch nguyên tử.
- **M02.** Bắt buộc chỉ người dùng có vai trò `student` mới được tạo đăng ký và chỉ `lecturer` được gán cho đề tài mới được duyệt.

## 2. Quyết định Tầng 2 · Taste (Đề xuất mặc định)
- **T01 (End User).** Khi sinh viên bị giảng viên từ chối nguyện vọng 1, hệ thống giữ lại lịch sử từ chối kèm lý do ngắn và cho phép sinh viên gửi đăng ký mới sang giảng viên khác `(recommended · Completeness 10/10)`. -> **Chủ nhà đồng ý.**

## 3. Quyết định Tầng 3 · User Challenge (Thẻ Quyết định Chiến lược)

### D01 · Cơ chế thông báo khi trạng thái đăng ký thay đổi
**Bối cảnh.** Nhánh `feat/topic-registration` · Bước 2 RRI
**Giải thích nhanh (ELI10).** Khi giảng viên duyệt hoặc từ chối đề tài, sinh viên cần biết kết quả để chủ động bước tiếp theo. Chúng ta cần chọn giữa việc hiển thị trạng thái trực tiếp trên bảng điều khiển web kèm xuất danh sách hay tích hợp thêm dịch vụ gửi thư điện tử tự động ngay trong đợt này.
**Rủi ro nếu chọn sai (Stakes).** Nếu tích hợp máy chủ gửi thư bên thứ ba ngay lúc này nhưng chưa có tài khoản SMTP của trường, tiến độ ra mắt sẽ bị chặn lại.
**Khuyến nghị.** Chọn Phương án B (Hiển thị trực tiếp trên cổng thông tin + hộp thư thông báo nội bộ trong ứng dụng) để ra mắt đúng hạn tuần này, ghi nhận việc gửi email vào sổ nợ làm tắt để nâng cấp khi phòng CNTT cấp khóa SMTP.
**Độ hoàn thiện (Completeness).** A = 10/10 · B = 7/10
**Thời gian thực hiện.** A (Thủ công 2 ngày / AI Builder 40 phút + chờ cấp SMTP) · B (Thủ công 4 giờ / AI Builder 15 phút)

**Phương án A · Thông báo trong ứng dụng kèm gửi Email tự động qua SMTP**
- Ưu điểm 1. Sinh viên nhận được tin báo ngay trên điện thoại mà không cần mở trang web.
- Ưu điểm 2. Đầy đủ tính năng như các hệ thống quản lý đào tạo thương mại.
- Nhược điểm. Phụ thuộc vào việc xin cấp tài khoản SMTP của trường và xử lý hàng đợi gửi thư lỗi.

**Phương án B · Thông báo nổi bật ngay trên Bảng điều khiển Web + Xuất bảng tổng hợp CSV (recommended)**
- Ưu điểm 1. Chủ động 100% về kỹ thuật, không phụ thuộc hạ tầng bên ngoài, chạy được ngay.
- Ưu điểm 2. Giảng viên và giáo vụ có thể tải file CSV danh sách đã duyệt để công bố tức thì.
- Nhược điểm. Sinh viên cần đăng nhập vào cổng thông tin để xem trạng thái cập nhật.

**Lựa chọn của Chủ nhà.** Chọn **Phương án B**.
**Ghi nhận Shortcut Debt.** Lưu mã `D01` (`Completeness 7/10`) vào `shortcut-ledger.csv` với điều kiện nâng cấp `Upgrade when phòng CNTT bàn giao thông tin máy chủ SMTP học kỳ mới`.

## 4. Ma trận Yêu cầu (REQ-IDs)
- **REQ-01 (P0).** Sinh viên gửi đăng ký đề tài (tiêu đề, tóm tắt, giảng viên nguyện vọng) khi chưa có đề tài nào đang chờ hoặc đã duyệt.
- **REQ-02 (P0).** Giảng viên xem danh sách chờ và bấm Duyệt hoặc Từ chối (kèm lý do); hệ thống chặn cứng nếu số đề tài đã duyệt của giảng viên chạm trần định mức `L1-MAX-TOPICS-PER-LECTURER = 5` (tham chiếu Kernel Registry Bộ 02).
- **REQ-03 (P1).** Hiển thị bảng trạng thái trực quan trên giao diện web cho sinh viên/giảng viên và hỗ trợ xuất danh sách đã duyệt ra CSV.
```

---

## Bước 3 & 4 · VISION & BLUEPRINT (Duyệt 4 Lăng kính và Phản biện Red-Team)

Chủ thầu lập bản vẽ `vibecode-artifacts/blueprints/BP-001.md`, chạy qua 4 lăng kính (`CEO -> Design -> DX -> Eng`) và phản biện Red-Team.

- **Phát hiện từ cổng Red-Team (Failure Mode Injector).** Nếu một sinh viên mở hai tab trình duyệt và bấm nút "Gửi đăng ký" cùng lúc, hệ thống có thể tạo ra 2 bản ghi `PENDING` cho cùng một sinh viên.
- **Cách khóa ngay trong Blueprint.** Thêm ràng buộc chỉ mục duy nhất có điều kiện trong SQLite (`CREATE UNIQUE INDEX idx_active_student_reg ON registrations(student_id) WHERE status IN ('PENDING', 'APPROVED')`) để cơ sở dữ liệu chặn cứng từ tầng thấp nhất.
- **Vết Mở rộng Tiến hóa (Extension Trace).** Tách hàm `notifyStatusChange(regId, newStatus)` thành một điểm nối riêng (hiện tại ghi vào bảng `notifications` nội bộ theo quyết định `D01`). Khi có SMTP ở vòng sau, chỉ cần gắn thêm bộ gửi email vào hàm này mà không phải sửa logic duyệt đề tài.

Chủ nhà xem xét và ký **`APPROVED`** cho `BP-001.md`.

---

## Bước 5 · TASK GRAPH (Chia 3 Gói TIP với Ma trận Sở hữu File Rời nhau)

Chủ thầu chia `BP-001.md` thành 3 gói `TIP` có thể chạy phần lõi trước và chạy song song 2 nhánh giao diện/xuất báo cáo trên 2 `git worktree` riêng biệt.

| Mã TIP | Phụ thuộc | Nhánh / Worktree | File được phép ghi (Scope Freeze) | Mô tả ngắn |
|---|---|---|---|---|
| **TIP-001** | Không | Nhánh gốc `feat/topic-reg` | `src/db/migrations/002_reg.sql`, `src/types/registration.ts`, `src/services/registrationService.ts`, `tests/registrationService.test.ts` | Xây dựng bảng dữ liệu, đóng băng kiểu `Registration` và xử lý nghiệp vụ đăng ký/duyệt đề tài có khóa giao dịch |
| **TIP-002** | TIP-001 | `.worktrees/tip-002` (`feat/tip-002-ui`) | `src/routes/registrationRoutes.ts`, `src/views/registration/**`, `tests/registrationRoutes.test.ts` | Xây dựng API endpoints và giao diện đăng ký/duyệt đề tài đủ 4 trạng thái (rỗng, đang tải, lỗi, đầy đủ) |
| **TIP-003** | TIP-001 | `.worktrees/tip-003` (`feat/tip-003-csv`) | `src/services/exportCsvService.ts`, `tests/exportCsvService.test.ts` | Xây dựng bộ xuất danh sách đề tài đã duyệt ra chuẩn CSV UTF-8 BOM cho giáo vụ |

Nhận thấy `TIP-002` và `TIP-003` có danh sách file được phép ghi hoàn toàn rời nhau (`Disjoint File Ownership`) và chỉ đọc file `src/types/registration.ts` đã đóng băng ở `TIP-001`, Chủ thầu cho chạy `TIP-001` trước, sau đó phát lệnh chạy song song `TIP-002` và `TIP-003`.

---

## Bước 6 · BUILD (Thi công Khóa Phạm vi và Chụp Dấu vân tay)

1. **Thợ 1 hoàn thành `TIP-001`.** Viết migration có `UNIQUE INDEX`, cài đặt `registrationService.ts` kèm dòng chú thích `// vibecode-shortcut(D01). Completeness 7/10. Upgrade when có SMTP.` tại hàm thông báo. Chạy `npx vitest run tests/registrationService.test.ts` đạt 8/8 bài kiểm thử xanh (bao gồm bài test giảng viên duyệt đề tài thứ 6 bị chặn cứng). Chụp `WTREE_FINGERPRINT` đạt `91c4e82a003f7712` và nộp `CR-001.md`.
2. **Thợ 2 và Thợ 3 chạy song song trên 2 Worktree.**
   - Thợ 2 hoàn thành `TIP-002` trên `.worktrees/tip-002`, nộp `CR-002.md` với bằng chứng `live-run` và `WTREE_FINGERPRINT` `b40291fa8812c304`.
   - Thợ 3 hoàn thành `TIP-003` trên `.worktrees/tip-003`, áp dụng **Vòng lặp Ràng buộc Cơ học (Constraint Loop)** để kiểm tra file CSV xuất ra có đúng mã byte UTF-8 BOM (`EF BB BF`) và thoát ký tự dấu phẩy an toàn, nộp `CR-003.md` với `WTREE_FINGERPRINT` `e77120cb3910a441`.

---

## Bước 7 · VERIFY (QA Bề mặt Thật và Trọng tài Độc lập Chấm chéo)

Chủ thầu khởi tạo một phiên **Trọng tài Độc lập (Arbiter C3)** để kiểm tra cả 3 gói trước khi hợp nhất.
- Trọng tài chạy lại lệnh tính `WTREE_FINGERPRINT` trên từng nhánh và xác nhận cả 3 báo cáo đều ở trạng thái **`FRESH`**.
- Trọng tài kiểm tra danh sách file thay đổi bằng `git diff --name-only` và xác nhận không có Thợ nào vi phạm `Scope Freeze`.
- Trọng tài khởi động máy chủ thật và chạy kiểm thử bề mặt trình duyệt. Mọi yêu cầu `REQ-01`, `REQ-02`, `REQ-03` đều đạt 100%.
- Chủ thầu hợp nhất `feat/tip-002-ui` và `feat/tip-003-csv` vào nhánh tính năng, chạy lại toàn bộ 34 bài kiểm thử của dự án đạt xanh tuyệt đối rồi dọn dẹp 2 thư mục worktree.

---

## Bước 8 · DUAL-STAGE SHIP & CALIBRATION CARD 100 ĐIỂM

1. **Phát hành Hai Chặng (`Beta -> Stable`).**
   - Đẩy nhánh lên môi trường `staging/beta` cho giáo vụ và 2 giảng viên dùng thử trong 1 buổi sáng.
   - Sau khi xác nhận CI xanh và không có commit lạ xen vào, hợp nhất chính thức lên nhánh `main` (`stable`).
2. **Lập Thẻ Hiệu chỉnh `CC-001.md` sau đợt mở đăng ký thật.**
   - **Quan sát thực tế (`OBSERVED`).** Hệ thống chặn chính xác 100% các trường hợp vượt chỉ tiêu 5 sinh viên/giảng viên và không có bản ghi trùng nào. Tuy nhiên, có 4 sinh viên nhập tóm tắt đề tài dài hơn 2.000 từ làm giao diện danh sách của giảng viên bị kéo dài khó đọc.
   - **Phân bổ 100 điểm sai số.**
     - `Modeling.` 70 điểm (Trong RRI và Blueprint chưa quy định giới hạn số ký tự tối đa cho ô tóm tắt đề tài).
     - `Timing.` 0 điểm.
     - `World-change.` 0 điểm.
     - `Execution.` 30 điểm (Giao diện danh sách chưa cắt gọn chuỗi dài bằng CSS `line-clamp`).
   - **Hành động cho Chu kỳ tiếp theo.** Thêm giới hạn 300 từ cho phần tóm tắt và bật `line-clamp` trên bảng danh sách ở gói `TIP-004` (phân tầng `R0`, xử lý trong 10 phút).
