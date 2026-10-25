# Sổ cái Kiểm toán, Bằng chứng và Nợ Kỹ thuật (Audit Trail Loop v6.1)

Hệ thống Vibecode Kit v6.1 duy trì khả năng truy vết hoàn toàn minh bạch qua các vòng lặp bằng ba bảng nhật ký dạng CSV gọn nhẹ, lưu trực tiếp trong thư mục `vibecode-artifacts/`. Không cần cài đặt cơ sở dữ liệu phức tạp, mọi công cụ dòng lệnh và AI agent đều có thể đọc và kiểm tra tức thì.

## 1. Nhật ký Kiểm toán Hành động (`vibecode-artifacts/audit-trail.csv`)

Ghi lại toàn bộ các mốc chuyển bước, phê duyệt, thi công và phát hành theo trình tự thời gian.

### Cấu trúc cột
- `timestamp` · Thời gian chuẩn ISO-8601 (`YYYY-MM-DDTHH:mm:ss`)
- `step` · Bước trong quy trình 8 bước (`1` đến `8`)
- `role` · Vai trò thực hiện (`Chủ nhà`, `Chủ thầu`, `Thợ thi công`, `Kongming`, `Arbiter`)
- `action` · Hành động chuẩn hóa (`SCAN_completed`, `RRI_completed`, `Decision_logged`, `Blueprint_created`, `Blueprint_approved`, `TIP_created`, `Build_started`, `Handoff_created`, `CR_created`, `Arbiter_verified`, `Shipped_beta`, `Shipped_stable`, `CC_created`, `Rule_overridden`)
- `reference` · Mã tài liệu tham chiếu (`SCAN-001`, `D01`, `BP-001`, `TIP-001`, `CR-001`, `CC-001`)
- `wtree_fp` · Dấu vân tay cây thư mục 16 ký tự tại thời điểm ghi nhận (hoặc `-` nếu không áp dụng)
- `notes` · Ghi chú ngắn gọn về kết quả hoặc lý do điều chỉnh quy trình

### Dữ liệu mẫu (`audit-trail.csv`)

```csv
timestamp,step,role,action,reference,wtree_fp,notes
2026-10-25T09:00:00,1,Thợ thi công,SCAN_completed,SCAN-001,8f3a19c04b2e1100,"Quét xong hiện trạng repo, phân loại R2"
2026-10-25T09:20:00,2,Chủ thầu,RRI_completed,RRI-001,8f3a19c04b2e1100,"Tự giải 8 câu từ Scan, trình 2 thẻ D01 và D02"
2026-10-25T09:30:00,2,Chủ nhà,Decision_logged,D01,8f3a19c04b2e1100,"Chọn phương án B (Completeness 7/10), ghi nhận Shortcut Debt"
2026-10-25T09:50:00,4,Chủ thầu,Blueprint_created,BP-001,8f3a19c04b2e1100,"Đã qua cổng 4-Lens và Red-Team 4 góc nhìn"
2026-10-25T10:00:00,4,Chủ nhà,Blueprint_approved,BP-001,8f3a19c04b2e1100,"APPROVED khế ước kiến trúc"
2026-10-25T10:10:00,5,Chủ thầu,TIP_created,TIP-001,8f3a19c04b2e1100,"Khóa Scope Freeze cho module xác thực"
2026-10-25T11:15:00,6,Thợ thi công,CR_created,CR-001,c49d20a17e5b9921,"Hoàn thành TIP-001, 14 unit tests + live-run FRESH"
2026-10-25T11:30:00,7,Arbiter,Arbiter_verified,CR-001,c49d20a17e5b9921,"Trọng tài độc lập kiểm tra khớp WTREE_FINGERPRINT, đạt 100% AC"
2026-10-25T11:45:00,8,Chủ nhà,Shipped_beta,CR-001,c49d20a17e5b9921,"Hợp nhất vào nhánh beta, CI xanh"
2026-10-25T16:00:00,8,Chủ nhà,Shipped_stable,CR-001,c49d20a17e5b9921,"Thăng cấp lên nhánh main sau khi kiểm tra danh sách commit"
2026-10-27T09:00:00,8,Chủ thầu,CC_created,CC-001,c49d20a17e5b9921,"Hiệu chỉnh sau 2 ngày chạy thật, thu hoạch Shortcut D01"
```

---

## 2. Sổ cái Nợ Làm tắt (`vibecode-artifacts/shortcut-ledger.csv`)

Theo dõi mọi quyết định mà Chủ nhà chủ động chọn phương án có điểm độ phủ `Completeness <= 7/10` để đổi lấy tốc độ ra mắt, đảm bảo không có khoản nợ kỹ thuật nào bị rơi vào quên lãng.

### Cấu trúc cột
- `decision_id` · Mã thẻ quyết định (`D01`, `D02`...)
- `tip_id` · Mã gói công việc thực thi (`TIP-001`...)
- `completeness` · Điểm độ hoàn thiện của phương án đã chọn (`7/10`, `5/10`...)
- `code_marker_location` · Đường dẫn file và vị trí gắn nhãn `vibecode-shortcut(D<N>)`
- `description` · Tóm tắt phần góc khuất đã tạm hoãn
- `upgrade_trigger` · Điều kiện cụ thể kích hoạt việc nâng cấp lên `10/10`
- `status` · Trạng thái (`OPEN`, `TRIGGERED`, `UPGRADED_IN_TIP_NNN`, `RETIRED`)

### Dữ liệu mẫu (`shortcut-ledger.csv`)

```csv
decision_id,tip_id,completeness,code_marker_location,description,upgrade_trigger,status
D01,TIP-001,7/10,src/auth/jwt.ts:42,"Dùng Stateless JWT chưa có bảng thu hồi phiên tức thì","Khi số người dùng vượt 500 hoặc khi bật tính năng quản lý thiết bị",OPEN
D04,TIP-003,6/10,src/export/csv.ts:18,"Xuất CSV đồng bộ trong bộ nhớ chưa tách luồng chạy nền","Khi file xuất vượt quá 50.000 dòng hoặc thời gian phản hồi > 3 giây",UPGRADED_IN_TIP_008
```

---

## 3. Sổ cái Bằng chứng Kiểm thử (`vibecode-artifacts/evidence-ledger/evidence.csv`)

Lưu trữ bằng chứng chạy lệnh kiểm chứng gắn chặt với dấu vân tay cây thư mục (`WTREE_FINGERPRINT`), phục vụ bước Verify và Trọng tài Arbiter đối chiếu.

### Cấu trúc cột
- `timestamp` · Thời điểm chạy lệnh kiểm tra
- `tip_id` · Mã gói công việc
- `ac_id` · Mã tiêu chí nghiệm thu (`AC1`, `AC2`, `G0`...)
- `evidence_kind` · Cấp độ bằng chứng (`static-read`, `unit-test`, `fixture-replay`, `live-run`, `production`)
- `command` · Câu lệnh thực tế đã chạy
- `exit_code` · Mã thoát của câu lệnh (`0` là thành công)
- `wtree_fp` · Dấu vân tay cây thư mục ngay khi lệnh kết thúc
- `status` · Trạng thái hiệu lực (`FRESH` nếu khớp cây thư mục hiện tại, `STALE` nếu code đã thay đổi sau đó)

### Dữ liệu mẫu (`evidence-ledger/evidence.csv`)

```csv
timestamp,tip_id,ac_id,evidence_kind,command,exit_code,wtree_fp,status
2026-10-25T11:12:00,TIP-001,AC1,unit-test,"npm test -- tests/auth.spec.ts",0,c49d20a17e5b9921,FRESH
2026-10-25T11:13:30,TIP-001,AC2,live-run,"curl -sf http://localhost:3000/api/health",0,c49d20a17e5b9921,FRESH
```

## 4. Quy trình Vòng lặp Kiểm toán ở Cuối mỗi Chu kỳ

1. Trước khi bước qua cổng **Verify (Bước 7)**, chạy lệnh tính lại `WTREE_FINGERPRINT` hiện tại của kho mã nguồn và so sánh với cột `wtree_fp` trong `evidence.csv` và `CR-NNN.md`. Nếu khác nhau, đánh dấu bằng chứng là `STALE` và yêu cầu Thợ chạy lại bộ kiểm thử.
2. Khi viết **Calibration Card (Bước 8)**, đọc toàn bộ các dòng có trạng thái `OPEN` trong `shortcut-ledger.csv` để kiểm tra xem điều kiện `upgrade_trigger` đã chạm ngưỡng thực tế hay chưa. Nếu đã chạm, tự động tạo TIP nâng cấp cho chu kỳ tiếp theo.
