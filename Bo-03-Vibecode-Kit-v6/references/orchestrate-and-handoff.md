# Giao Thức Chia Nhỏ Đơn Vị Kiểm Chứng, Điều Phối `Worktree / Cloud Swarm` & Bàn Giao Khử Bí Mật (`Orchestrate & Handoff Protocol`)

> **Bước 5 & Bước 6 của Vibecode Kit v6.2 (`× pstack`) · Đơn vị `Sequence-Verifiable-Units` · Vượt Trần Phần Cứng Máy Cá Nhân (`~10 Agents`) bằng `Coordinator + Cloud Agents + /swarm`**

---

## 1. Chia Nhỏ Kế Hoạch Theo Đơn Vị Kiểm Chứng Độc Lập (`Sequence-Verifiable-Units`)

Sau khi thiết kế đã được chứng minh bằng code qua `/prototype` hoặc `5-Phase /architect Arena`, Chủ thầu mới xuất bản kế hoạch thực thi nhiều giai đoạn ở Bước 5 (`TASK GRAPH`) theo 3 nguyên tắc cứng:
1. **Chia thành các PR nhỏ độc lập (`Sequence-Verifiable-Units`):** Mỗi gói giao việc ([`TIP-template.md`](../templates/TIP-template.md)) phải là một đơn vị có thể biên dịch, chạy kiểm thử và merge độc lập mà không làm gãy nhánh chính.
2. **Gắn chặt với Kiểm chứng Sống (`Live Verification`):** Mọi bước trong kế hoạch đều phải đi kèm câu lệnh thực thi qua `./bin/control-app` ("chỉ vượt qua unit test là chưa đủ, bắt buộc phải chạy code thật và thu bằng chứng thật").
3. **Không giao nhau về quyền sở hữu tệp (`Disjoint File Ownership`):** Hai gói việc chạy song song (`TIP-A` và `TIP-B`) bắt buộc có tập hợp tệp được phép sửa hoàn toàn tách biệt:
   $$\text{owned\_files}(A) \cap \text{owned\_files}(B) = \emptyset$$
   Nếu hai gói việc cần chạm vào cùng một tệp cấu hình hoặc tệp định tuyến chung, phải xếp chúng chạy nối tiếp theo thứ tự trong đồ thị `DAG` hoặc tách phần chỉnh sửa tệp chung thành một bước khởi tạo ngắn trước khi phân nhánh.

---

## 2. Định Tuyến Điều Phối Song Song: `<= 10 Local Worktrees` vs. `> 10 Cloud Agents + /swarm`

Một bài học xương máu từ thực tế vận hành `pstack` của `@poteto`: **Việc lạm dụng quá nhiều `git worktree` trên một máy tính cá nhân sẽ nhanh chóng chạm trần phần cứng khi chạy vượt quá `~10` agents đồng thời** (ngốn hàng chục GB ổ cứng cho `node_modules`/build artifacts, đụng độ cổng mạng `port` và cơ sở dữ liệu kiểm thử, tràn bộ nhớ RAM làm treo máy trạm).

Do đó, Vibecode Kit v6.2 áp dụng kiến trúc điều phối hai tầng tự động phân luồng theo số lượng tác vụ song song:

```text
                       [CHỦ THẦU / COORDINATOR BOT (Giữ Context Sạch)]
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼ (Quy mô <= 10 nhánh song song)                  ▼ (Quy mô > 10 nhánh hoặc cần /swarm)
   +------------------------------------------------+ +------------------------------------------------+
   |      TẦNG 1: LOCAL GIT WORKTREES (<= 10)       | |   TẦNG 2: CLOUD AGENTS & /SWARM (> 10 AGENTS)  |
   | - Tạo nhánh tại .worktrees/tip-<id>            | | - Mỗi Cloud Agent chạy trên VM ảo hóa riêng    |
   | - Cấp phát APP_PORT = 3100 + <id> riêng biệt   | | - Khởi động tức thì từ VM Snapshot đã cài sẵn  |
   | - Khóa phạm vi sửa tệp bằng /freeze & /guard   | | - Có màn hình thật (virtual display) để chụp   |
   | - Chạy ./bin/control-app kiểm chứng cục bộ     | |   ảnh, quay video và chạy trình duyệt thật     |
   | - Thu hồi worktree ngay sau khi merge          | | - Hỗ trợ /swarm fan-out kiểm tra độ ổn định    |
   |                                                | |   hoặc auto-repro lỗi tự động từ Slack         |
   +------------------------------------------------+ +------------------------------------------------+
```

### Quy Trình Khởi Tạo Tầng 1 (`Local Git Worktree` cho `<= 10` nhánh):
```bash
TASK_ID="tip-01-order-cancel"
BRANCH_NAME="feat/${TASK_ID}"
WORKTREE_DIR=".worktrees/${TASK_ID}"

mkdir -p .worktrees
git worktree add -b "${BRANCH_NAME}" "${WORKTREE_DIR}" main
```
Khi hoàn tất và đã merge nhánh vào `main`, bắt buộc dọn dẹp ngay:
```bash
git worktree remove "${WORKTREE_DIR}"
git branch -d "${BRANCH_NAME}"
```

### Quy Trình Vận Hành Tầng 2 (`Coordinator Bot + Cloud Agents + /swarm` cho `> 10` nhánh):
1. **Vai trò của `Coordinator Bot`:** Đóng vai Chủ thầu điều phối trung tâm, hoàn toàn không tự chạy tác vụ nặng hay giữ hàng nghìn dòng log trong bộ nhớ ngữ cảnh của mình; chỉ gửi gói lệnh (`TIP` hoặc kịch bản tái hiện lỗi) và nhận về báo cáo JSON gọn nhẹ kèm đường dẫn bằng chứng.
2. **Môi trường `Cloud Agents`:** Mỗi Agent thực thi chạy trên một máy ảo đám mây độc lập được khởi tạo tức thì từ bản chụp (`VM snapshot` đã nạp sẵn dependencies và DB mẫu), có màn hình hiển thị thật (`virtual framebuffer / display`) để chạy `./bin/control-app screenshot` và quay video thao tác giao diện mà không bị giới hạn tài nguyên máy cá nhân.
3. **Kịch bản `/swarm` & Tự động tái hiện lỗi (`auto-repro`):**
   - **Kiểm chứng độ ổn định (`Stability Swarm`):** Khi cần săn lỗi chập chờn (`flaky test` / `race condition`) hoặc kiểm thử một tính năng trên 20 cấu hình dữ liệu khác nhau, `Coordinator` phát lệnh `/swarm` để tung đồng loạt hàng chục `Cloud Agents` chạy `./bin/control-app` song song và gom kết quả thống kê.
   - **Tự động tái hiện lỗi từ kênh chat (`Slack Auto-Repro`):** Ngay khi có người dùng hoặc tester báo lỗi trên Slack, `Coordinator Bot` đọc thông báo lỗi, thực hiện `Indirect Prompting Restate`, rồi điều động một đội `Cloud Agents` qua `/swarm` thử các tổ hợp trạng thái qua `./bin/control-app repro` cho đến khi dựng lại được kịch bản lỗi có thể tái hiện 100% kèm video bằng chứng và đề xuất PR sửa lỗi.

---

## 3. Cổng Chặn An Toàn Khi Thực Thi (`Safety Gates: /freeze, /guard, /careful`)

Để ngăn chặn việc Thợ vô tình phá hỏng các tệp ngoài phạm vi hoặc chạy các lệnh nguy hiểm:
1. **Khóa biên giới thư mục (`/freeze`):** Giới hạn quyền ghi tệp của Thợ chỉ nằm trong thư mục hoặc danh sách `owned_files` được chỉ định trong `TIP`.
2. **Bảo vệ toàn diện (`/guard` & `/careful`):** Chặn tự động các câu lệnh có nguy cơ hủy hoại dữ liệu (`git reset --hard`, `git push --force`, `rm -rf`, `DROP TABLE`) và bắt buộc mọi lệnh tác động trạng thái trong `./bin/control-app` phải kiểm tra cờ `--dry-run` trước khi chạy thật.
3. **Cơ chế Cứu hộ khi Thợ Bị Kẹt (`2-Strike Escalation & Scrap When Wrong`):**
   - Nếu Thợ gặp dấu hiệu kiến trúc sai (phải truyền tham số vá víu, lặp lại workaround hoặc dùng `any`), kích hoạt ngay **`Scrap when wrong`** để báo Chủ thầu thiết kế lại chữ ký hàm.
   - Nếu Thợ chạy kiểm thử thất bại quá **2 vòng liên tiếp** trên cùng một lỗi mà chưa tìm ra nguyên nhân gốc, bắt buộc dừng việc thử mò mẫm và chuyển hồ sơ cho Chủ thầu hoặc Quân sư (`@kongming`) phân tích.

---

## 4. Hợp Đồng Bàn Giao Đã Khử Bí Mật (`Redacted Handoff Contract`)

Khi phiên làm việc kéo dài chạm ngưỡng `70%` dung lượng vùng nhớ ngữ cảnh hoặc khi chuyển giao công việc giữa hai Agent khác nhau, bắt buộc kết hợp lệnh `/recall` (rút trích trạng thái từ transcript) và xuất tệp bàn giao theo mẫu [`templates/Handoff-Contract.md`](../templates/Handoff-Contract.md) với 3 yêu cầu bắt buộc:

1. **Đóng dấu `WTREE_FINGERPRINT`:** Ghi rõ mã commit và trạng thái cây làm việc tại thời điểm bàn giao.
2. **Liệt kê Bằng chứng Kiểm chứng Sống (`Live Verification Status`):** Ghi rõ những đơn vị `sequence-verifiable-units` nào đã chạy pass qua `./bin/control-app` và những đơn vị nào đang chờ.
3. **Quét Khử Bí mật Tự động (`Mandatory Secret Redaction`):** Chạy bộ lọc biểu thức chính quy để thay thế mọi chuỗi khóa nhạy cảm (`sk-...`, `tvly-...`, `ghp_...`, `AIza...`, `Bearer ...`) thành `<REDACTED_SECRET>` trước khi lưu tệp bàn giao xuống đĩa.
