# Giao Thức Phát Hành 2 Giai Đoạn, Vai Trò "Người Làm Vườn" (`The Gardener`), Vệ Sinh Kế Hoạch Tạm & Thẻ Hiệu Chuẩn 100 Điểm (`SHIP & Calibration Protocol`)

> **Bước 8 của Vibecode Kit v6.2 (`× pstack`) · Tốc độ Đi Kèm Chất Lượng · Tuần Tra Dòng Chảy PR · Giữ Sạch Kho Mã Nguồn**

---

## 1. Tốc Độ Đi Kèm Chất Lượng & Vai Trò "Người Làm Vườn" (`The Gardener`)

Trước thời đại AI Agent, số lượng PR hay số dòng code (`LOC`) thường bị xem là chỉ số phù phiếm (`vanity metric`). Nhưng khi hệ thống đã có quy trình tự kiểm chứng chặt chẽ qua `./bin/control-app` (Bài 1 của `@poteto`), khối lượng PR nhỏ độc lập (`sequence-verifiable-units`) chảy liên tục ở tốc độ cao cho phép kỹ sư thoát khỏi việc ngồi canh từng dòng code để chuyển sang vai trò **"Người làm vườn" (`The Gardener`)**:

### Bốn Nhiệm Vụ Tuần Tra Hàng Ngày Của `The Gardener`:
1. **Nhổ bỏ "cỏ dại kiến trúc" từ trong trứng nước (`Pulling Architectural Weeds Early`):**
   - Phát hiện và gộp ngay các hàm tiện ích bị viết lặp lại lần thứ 3 trong tuần ở các thư mục khác nhau (kết hợp kỹ năng `deslop-shared-libs`).
   - Chặn đứng sự lan tràn của các lệnh tắt kiểm tra chất lượng (`eslint-disable`, `@ts-ignore`, `# noqa`, `skip test`).
2. **Chủ động Refactor nền tảng ngay khi sản phẩm đang tăng trưởng nóng:**
   - Nhờ mạng lưới an toàn của `./bin/control-app` và các PR nhỏ độc lập, `The Gardener` có thể nâng cấp cấu trúc dữ liệu và làm sạch nợ kỹ thuật trực tiếp trên dòng chảy chính mà không gây gián đoạn dịch vụ (`zero downtime`).
3. **Vệ sinh File Kế hoạch Tạm sau khi Merge (`Temporary Plan Hygiene`):**
   - Các tệp kế hoạch thực thi tạm thời (`scratch plans`, bản nháp pha thực thi) chỉ có giá trị trong lúc đang xây dựng tính năng.
   - **Quy tắc bắt buộc:** Ngay sau khi các PR của kế hoạch đã được merge xong, phải xóa bỏ file kế hoạch tạm trong nhánh chính hoặc chuyển vào thư mục lưu trữ lịch sử (`_Archive/`) để kho mã nguồn không biến thành bãi rác gây nhiễu vùng nhớ ngữ cảnh cho các Agent thế hệ sau.
4. **Duy trì Hàng rào Bảo vệ cho Toàn đội (`Empowering Non-Engineers`):**
   - Giữ cho `./bin/control-app`, `Feature Map` (`references/features/README.md`) và hệ thống CI luôn xanh để cả kỹ sư lẫn các thành viên không chuyên (`PM`, `Designer`, `Ops`) đều có thể đóng góp tính năng an toàn, nhân 100 đến 1000 lần năng suất toàn đội.

---

## 2. Quy Trình Phát Hành Hai Giai Đoạn (`Dual-Stage Ship: beta -> official`)

Đối với các tính năng từ cấp `R2` trở lên, việc phát hành được thực hiện qua 2 nhịp kiểm soát:

### Giai đoạn 1: Nhánh Thử nghiệm (`Stage 1 · Beta / Staging`)
1. Đồng bộ nhánh cơ sở mới nhất (`git fetch origin main && git rebase origin/main`).
2. Chạy toàn bộ bộ kiểm thử tự động và lệnh kiểm chứng sống `./bin/control-app` để lấy dấu vân tay `WTREE_FINGERPRINT` với `DIRTY_FILES=0`.
3. Hợp nhất vào nhánh `beta` / `staging` và kích hoạt theo dõi hậu triển khai (`Canary Monitoring`): kiểm tra log lỗi, độ trễ phản hồi API và tỷ lệ thành công của luồng chính.

### Giai đoạn 2: Nhánh Chính thức (`Stage 2 · Official / Production`)
1. Khi nhánh `beta` hoạt động ổn định và Trọng tài độc lập (`C3`) đã đóng dấu `APPROVED`, tiến hành hợp nhất lên nhánh chính thức (`main` / `production`).
2. Thực hiện vệ sinh các nhánh `git worktree` cục bộ hoặc thu hồi các `Cloud Agent VM snapshots` đã hoàn thành nhiệm vụ.
3. Dọn dẹp hoặc lưu trữ file kế hoạch thực thi tạm thời (`Temporary Plan Cleanup`).

---

## 3. Bảo Trì `Feature Map` (`/maintain-verification-skill`) & Đồng Bộ Hậu Phát Hành (`Post-Ship Sync`)

Ngay sau khi phát hành thành công lên nhánh chính thức, Chủ thầu thực hiện đồng bộ hóa 2 tầng:
1. **Chạy `/maintain-verification-skill` cập nhật `Feature Map` (`references/features/README.md`):**
   - Bổ sung hoặc cập nhật mục tính năng vừa phát hành vào bảng `Feature Map` (tên tính năng, đường dẫn, tệp nguồn chính, lệnh `./bin/control-app` kiểm chứng và mã băm SHA-256 mới).
   - Chạy `./bin/control-app doctor --json` để xác nhận không có mục nào trong `Feature Map` bị trôi (`drift`) so với code thật.
2. **Đồng bộ Sổ cái Nguồn Sự Thật (`Kernel Registry SOT` & `Notion Hub`):**
   - Tính toán mã băm SHA-256 của các tài liệu kiến trúc và `Feature Map`, cập nhật những khối có thay đổi (`delta sync`) lên Bộ 02 (`Kernel Registry`) và cổng tài liệu chung.

---

## 4. Thẻ Hiệu Chuẩn 100 Điểm (`100-Point Calibration Card`) & Vòng Lặp Học Tập (`Retro Loop`)

Mỗi chu kỳ làm việc khép lại bằng việc chấm điểm khách quan trên thang **100 điểm** theo biểu mẫu [`templates/Calibration-Card.md`](../templates/Calibration-Card.md):

| Trụ cột đánh giá | Điểm tối đa | Tiêu chí đạt điểm tuyệt đối trong v6.2 (`× pstack`) |
|---|---|---|
| **1. Kỷ luật Khẳng định & `Indirect Prompting` (`Claim & Intent`)** | `20đ` | 100% khẳng định có nhãn `[OBSERVED: file:line]`; bản `Indirect Prompting Restate` và bộ tứ `/teach = /how + /why + /recall` bắt trúng bản chất bài toán ngay từ đầu. |
| **2. Lập Kế hoạch bằng Code (`Working Backwards & /architect`)** | `20đ` | Viết `Caller README (4 ô Diátaxis + /unslop)` trước; chạy `5-Phase /architect Arena` (`Type Signatures Sketch`); kích hoạt kịp thời `Scrap when wrong` nếu phát hiện lệch kiến trúc. |
| **3. Đòn bẩy Tự Kiểm Chứng (`./bin/control-app & Live Proof`)** | `25đ` | Khép kín vòng lặp kiểm chứng sống qua `./bin/control-app --json` (đủ `--dry-run`, `Actionable Error`, `seed/auth/dom/screenshot`); đính kèm `WTREE_FINGERPRINT` hợp lệ. |
| **4. Điều phối Cô lập & Tốc độ (`Worktree / Cloud Swarm`)** | `20đ` | Chia đúng các đơn vị `sequence-verifiable-units`; không vượt trần `~10 local worktrees` (chuyển sang `Cloud Agents + /swarm` khi `> 10`); 0 xung đột tệp tin. |
| **5. Vệ sinh "Người làm vườn" & Bảo trì Bộ nhớ (`Gardener & Feature Map`)** | `15đ` | Nhổ sạch cỏ dại kiến trúc; xóa/lưu trữ file plan tạm sau khi merge; cập nhật `Feature Map` (`references/features/README.md`) qua `/maintain-verification-skill` và vượt qua 100% `Constraint Loop`. |

> **Ngưỡng Chuẩn (`Pass Threshold`):** Phiên làm việc đạt từ **`90/100`** điểm trở lên được công nhận đạt chuẩn xuất sắc (`Gold Standard`). Mọi bài học mới phát hiện trong chu kỳ được đúc kết vào bộ nhớ liên dự án (`/learn`) để toàn bộ các phiên sau tự động kế thừa.
