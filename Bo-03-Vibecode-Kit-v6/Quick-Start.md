# Cẩm Nang Khởi Động Nhanh (`Quick-Start · 5 Phút`)

> **Cách áp dụng Vibecode Kit v6.2 (`× pstack @poteto`) ngay trong dự án của bạn**

---

## 1. Cài Đặt Nhanh Trong 30 Giây

Nếu bạn đang dùng Claude Code, Cursor hoặc Antigravity IDE, hãy cài đặt kỹ năng `vibecode-kit-v6` vào thư mục kỹ năng toàn cục:

```bash
mkdir -p ~/.gemini/config/skills/vibecode-kit-v6
cp -R Bo-03-Vibecode-Kit-v6/* ~/.gemini/config/skills/vibecode-kit-v6/
```

Hoặc giải nén trực tiếp từ gói `.skill`:
```bash
unzip -o vibecode-kit-v6.skill -d ~/.gemini/config/skills/
```

---

## 2. Khởi Tạo Đòn Bẩy `./bin/control-app` & `Feature Map` Cho Dự Án Mới (1 Phút)

Để AI Agent không tốn hàng nghìn token mò đường trong codebase và tự viết script kiểm thử dùng một lần mỗi khi chạy, hãy khởi tạo ngay 2 hiện vật cốt lõi từ biểu mẫu [`templates/Control-App-and-Feature-Map.md`](./templates/Control-App-and-Feature-Map.md):
1. **Công cụ CLI `./bin/control-app`:** Hỗ trợ `--dry-run`, `--json`, `--help`, thông báo lỗi chỉ dẫn trực tiếp lệnh tiếp theo (`next_command`) và các subcommands `seed`, `auth`, `flag`, `dom`, `screenshot`, `perf`.
2. **Bản đồ tính năng `references/features/README.md` (`Feature Map`):** Danh mục mọi tính năng từ góc nhìn người dùng kèm lệnh `./bin/control-app` để chạm tới.

---

## 3. Ba Mẫu Câu Lệnh Khởi Động Chuẩn (`Copy & Paste Prompts`)

### Kịch bản A: Sửa lỗi hoặc thay đổi nhỏ/vừa (`R0 / R1`)
```text
Kích hoạt kỹ năng vibecode-kit-v6 (Chế độ R1 - 4 nhịp):
Bài toán: [Mô tả lỗi hoặc tính năng nhỏ cần sửa].
Yêu cầu:
1. Đọc Feature Map (references/features/README.md) và viết 2 câu Indirect Prompting Restate ("diễn đạt lại bản chất bài toán bằng lời tự nhiên") kèm nhãn [OBSERVED: file:line].
2. Viết test tái hiện lỗi trước (Red) -> Sửa code tối thiểu để test xanh (Green). Nếu phát hiện phải ép kiểu any hoặc truyền tham số vá víu, dừng lại báo Scrap when wrong.
3. Chạy ./bin/control-app --json để kiểm chứng sống (Live Verification) và đính kèm mã băm WTREE_FINGERPRINT vào báo cáo hoàn tất.
```

### Kịch bản B: Xây dựng tính năng lớn hoặc thiết kế hệ thống mới (`R2`)
```text
Kích hoạt kỹ năng vibecode-kit-v6 (Vai trò: Chủ thầu - Cấp độ R2):
Bài toán: [Mô tả tính năng lớn cần xây dựng].
Yêu cầu:
1. Bước 1 (SCAN): Đọc Feature Map, viết Indirect Prompting Restate và chạy bộ tứ /teach = /how (Runtime) + /why (Git/PR/Ticket history) + /recall.
2. Bước 2 (RRI): Hỏi tối đa 3 câu trắc nghiệm kèm Bảng Quyết định D<N> (Completeness X/10) để chốt yêu cầu đạt RRI >= 8.5/10.
3. Bước 3 & 4 (VISION & BLUEPRINT): Thiết kế ngược Working Backwards (Caller README theo 4 ô Diátaxis + /unslop), dựng /prototype Live Switcher (nếu có UI), chạy 5-Phase /architect Arena (phác thảo Type Signatures & Caller Usage Sketch chưa viết thân hàm) và duyệt qua 4 lăng kính.
4. Bước 5 (TASK GRAPH): Chia thành các đơn vị kiểm chứng độc lập (sequence-verifiable-units) gắn lệnh ./bin/control-app. Dùng Local Worktrees nếu <= 10 nhánh hoặc đẩy sang Coordinator + Cloud Agents + /swarm nếu > 10 nhánh.
```

### Kịch bản C: Giao việc cho Thợ trong nhánh cô lập (`Builder Prompt`)
```text
Kích hoạt kỹ năng vibecode-kit-v6 (Vai trò: Thợ thực thi gói việc TIP-01):
Đọc tệp gói việc tại: [đường dẫn tới TIP-01.md].
Ràng buộc cứng:
1. Chỉ được phép chỉnh sửa các tệp trong danh sách owned_files.
2. Điền thân hàm vào khung Type Signatures Sketch theo đúng chu trình TDD (Red -> Green -> Refactor).
3. Luật Scrap when wrong: Nếu phải truyền tham số vá víu qua 3 tầng, lặp lại workaround hoặc dùng any / ép kiểu cưỡng bức, DỪNG CODE NGAY và báo SCRAP_TRIGGERED về Chủ thầu.
4. Chạy lệnh Live Verification qua ./bin/control-app --json và xuất báo cáo theo mẫu templates/Completion-Report.md có đóng dấu WTREE_FINGERPRINT.
```

---

## 4. Bảng Kiểm Nhanh Trước Khi Merge (`The Gardener 60-Second Checklist`)

- [ ] Bản `Indirect Prompting Restate` và mọi quyết định `D<N>` trong `Blueprint` đều đã được phê duyệt (`0 unresolved decisions`)?
- [ ] Khung chữ ký kiểu (`Type Signatures Sketch`) có giữ được sự trong sáng mà không cần ép kiểu `any` hay truyền tham số vá víu (`0 Scrap triggers`)?
- [ ] Đã chạy kiểm chứng sống (`Live Verification`) bằng `./bin/control-app --json` kèm bằng chứng ảnh chụp/DOM/log thật chưa?
- [ ] Có dấu hiệu "cỏ dại kiến trúc" nào cần **Người làm vườn (`The Gardener`)** nhổ bỏ không (hàm tiện ích viết lặp lần thứ 3, lệnh tắt lint)?
- [ ] Đã xóa hoặc chuyển lưu trữ file kế hoạch tạm thời (`Temporary Plan Cleanup`) và chạy `/maintain-verification-skill` cập nhật `references/features/README.md` chưa?
- [ ] Biên bản nghiệm thu đã có dòng `WTREE_FINGERPRINT` với `DIRTY_FILES=0` chưa?
