# Kiến Trúc Kỹ Thuật Vibecode Kit v6.2 (`× pstack`)

> **Đặc tả Sổ cái Bằng chứng · Đòn bẩy `./bin/control-app` CLI · Bộ nhớ `Feature Map` · Đấu trường `/architect` 5 Pha · Điều phối `Cloud /swarm`**

---

## 1. Sơ Đồ Kiến Trúc Tổng Thể (`Vibecode Kit v6.2 × pstack Engine`)

```text
+---------------------------------------------------------------------------------------------------+
|                   TẦNG 1: NHẬN THỨC HAI CHIỀU & KHỬ MƠ HỒ (SCAN & RRI LAYER)                      |
|  [Feature Map: references/features/README.md] ---> [Indirect Prompting: Restate in plain English] |
|  [/teach = /how (Runtime) + /why (Git/PR/Ticket) + /recall (Transcripts)] ---> [Decision D<N>]   |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|              TẦNG 2: LẬP KẾ HOẠCH BẰNG CODE & CỔNG 4 GÓC NHÌN (VISION & BLUEPRINT LAYER)          |
|  [Working Backwards: Caller README 4 ô Diátaxis + /unslop] ---> [/prototype: Live UI Switcher]    |
|  [5-Phase /architect Arena: Ground -> Sketch Type Signatures -> Judge -> Implement -> Scrap]      |
|  [4-Lens Gate: CEO -> Design -> Eng (Error & Rescue Map) -> DX]                                   |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|             TẦNG 3: ĐỊNH TUYẾN ĐIỀU PHỐI SONG SONG (DISJOINT ORCHESTRATION & SWARM LAYER)         |
|  [Sequence-Verifiable-Units (TIPs)] ---> | <= 10 Agents: Local Git Worktrees (Isolated Ports/DB)  |
|                                          | >  10 Agents: Coordinator Bot + Cloud VMs + /swarm     |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|             TẦNG 4: ĐÒN BẨY TỰ KIỂM CHỨNG & SỔ CÁI MÃ BĂM (VERIFICATION LEVER & LEDGER)           |
|  [./bin/control-app & scripts/bo03_vibecode_tool.py (init-control-app, wtree-fingerprint, ...)]   |
|  [4-Label Claim Discipline (OBSERVED/DERIVED/PRIOR/ASSUMED)] + [WTREE_FINGERPRINT] + [Arbiter]    |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|             TẦNG 5: PHÁT HÀNH, NGƯỜI LÀM VƯỜN & BẢO TRÌ BỘ NHỚ (GARDENER & SYNC LAYER)            |
|  [Dual-Stage Ship (beta -> official)] ---> [The Gardener PR Patrol & Xóa File Plan Tạm]           |
|  [bo03_vibecode_tool.py maintain-features & constraint-check (SHA-256 Sync)] + [100-Pt Card]      |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Cơ Chế 1: Đòn Bẩy Hạ Tầng Tự Kiểm Chứng (`Build the Lever · ./bin/control-app CLI`)

Thay vì viết hướng dẫn kiểm thử dài dòng bằng chữ trong `SKILL.md` (khiến AI Agent tốn hàng nghìn token tự viết script dùng một lần mỗi khi cần test), mỗi dự án áp dụng Vibecode Kit v6.2 bắt buộc đóng gói một công cụ dòng lệnh **`./bin/control-app`** theo triết lý *Deep Modules* của John Ousterhout (giao diện gọi cực kỳ đơn giản nhưng ẩn giấu toàn bộ sự phức tạp bên dưới).

### Sáu Tiêu Chuẩn Thiết Kế `./bin/control-app` Cho AI Agent:
1. **Dễ ghép nối & Hé lộ chức năng tăng dần (`Composable & Progressive Disclosure`):** Tổ chức thành các `subcommands` rõ ràng (`seed`, `auth`, `flag`, `dom`, `screenshot`, `perf`, `repro`, `doctor`).
2. **An toàn tuyệt đối với `--dry-run`:** Mọi lệnh có nguy cơ gây tác dụng phụ (ghi DB, xóa cache, gửi webhook, đổi cờ) bắt buộc hỗ trợ cờ `--dry-run` để in ra kế hoạch tác động mà không làm thay đổi trạng thái thật.
3. **Thông báo lỗi chỉ dẫn hành động (`Actionable Error Messages`):** Khi gặp lỗi, đầu ra không được chỉ báo `"Failed"` mà phải mô tả rõ nguyên nhân gốc (`root_cause`) và **chỉ dẫn trực tiếp câu lệnh tiếp theo Agent cần chạy** trong trường `next_command`.
4. **Đầu ra máy đọc được (`--help` & `--json`):** Mọi subcommand đều có `--help` chi tiết kèm ví dụ và trả kết quả ở định dạng JSON chuẩn hóa để Agent phân tích tức thì mà không phải đoán văn bản tự do.
5. **Bao phủ trọn vẹn Trải nghiệm Phát triển (`Full DX Coverage`):**
   - `seed`: Khởi tạo dữ liệu mẫu chuẩn xác theo kịch bản kiểm thử.
   - `auth`: Giả lập phiên đăng nhập của người dùng thử nghiệm (`mock auth / test user`) theo từng vai trò (`admin`, `member`, `guest`).
   - `flag`: Bật hoặc tắt `feature flag` ngay trong phiên kiểm thử (kể cả bật nút chuyển `/prototype`).
   - `dom`: Trích xuất cây giao diện (`DOM / Accessibility Tree snapshot`) gọn nhẹ, tiết kiệm token.
   - `screenshot`: Chụp ảnh màn hình hoặc quay video ngắn tại đúng đường dẫn/trạng thái cần nghiệm thu.
   - `perf`: Đo thời gian phản hồi API, dung lượng gói tin hoặc chỉ số Web Vitals.
6. **Khép kín vòng lặp (`Close the Loop`):** Cho phép Agent tự chạy ứng dụng -> tự thao tác -> tự đọc log/trace -> tự chụp bằng chứng cho đến khi đạt kết quả đúng mà không cần con người ngồi canh (`babysitting`).

### Mẫu Cấu Trúc Phản Hồi JSON Chuẩn Của `./bin/control-app`:
```json
{
  "ok": false,
  "subcommand": "dom",
  "target": "/checkout",
  "dry_run": false,
  "error": {
    "code": "AUTH_SESSION_EXPIRED",
    "root_cause": "Test user session token for role 'buyer' is missing or expired in .tmp/session.json",
    "next_command": "./bin/control-app auth --user buyer@example.com --role buyer --json"
  },
  "timestamp": "2026-10-26T09:00:00Z"
}
```

---

## 3. Cơ Chế 2: Bộ Nhớ Vật Chất Hóa (`Materialized Memory · Feature Map` & `/maintain-verification-skill`)

Khi ứng dụng phình to, Agent tốn rất nhiều vùng nhớ ngữ cảnh (`context window`) chỉ để mò xem tính năng nằm ở đâu và làm sao để đi tới màn hình đó. Vibecode Kit v6.2 giải quyết bằng **`Feature Map`** đặt tại `references/features/README.md`:

- **Vai trò của `Feature Map`:** Là bản đồ tra cứu nhanh từ góc nhìn người dùng, liệt kê mọi tính năng hiện có, mục đích nghiệp vụ, đường dẫn URL/API, danh sách tệp nguồn chính, câu lệnh `./bin/control-app` để chạm tới tính năng đó và mã băm SHA-256 của tệp nguồn.
- **Nguyên tắc Nguồn Chân Lý:** **Codebase là nguồn chân lý tối thượng**, còn `Feature Map` là bản nén tiết kiệm token của codebase.
- **Tác vụ Bảo trì Định kỳ (`/maintain-verification-skill`):** Chạy tự động mỗi ngày hoặc ngay ở Bước 8 (`SHIP`) sau mỗi PR để quét các route/module vừa thay đổi, cập nhật lại `references/features/README.md` và đối chiếu mã băm SHA-256 với Bộ 02 (`Kernel Registry SOT`) nhằm ngăn chặn hiện tượng trôi lệch (`drift`).

---

## 4. Cơ Chế 3: `Indirect Prompting` & Mô Hình Nhận Thức Hai Chiều (`/teach = /how + /why + /recall`)

Để giám sát những mô hình AI viết code nhanh hơn con người trên codebase khổng lồ, Bước 1 (`SCAN`) áp dụng cơ chế khóa 2 điểm mù của Frontier Models:

1. **Kỹ thuật `Indirect Prompting` (*"Restate in your own words and in plain English"*):**
   - Trước khi đề xuất giải pháp hay chạm vào code, Chủ thầu phải đọc nguồn thông tin nhiễu (thread báo lỗi Slack, log hệ thống, mô tả yêu cầu thô) và viết mục **`Indirect Prompting Restate`** bằng ngôn ngữ tự nhiên, rõ ràng.
   - Bước này ép Agent nén thông tin nhiễu thành bài toán có cấu trúc và giúp Chủ nhà bắt lỗi hiểu sai ngay từ giây đầu tiên.
2. **Tổ hợp 4 Lệnh Xây Dựng Mental Model Hai Chiều (`/teach = /how + /why + /recall`):**
   - `/how`: Truy vết cơ chế hoạt động hiện tại ở tầng runtime; tự động fan-out nhiều explorer agents chạy song song nếu tính năng đi qua nhiều thư mục hoặc microservice.
   - `/why`: Truy tìm nguyên nhân lịch sử và ý đồ thiết kế qua `git log -S`, `git blame`, PR comments, ticket và log sự cố cũ (ngăn chặn việc Agent xóa nhầm một đoạn code trông có vẻ thừa nhưng thực chất là chốt chặn lỗi Production).
   - `/teach`: Bắt buộc Agent giải thích trực quan và chứng minh bằng code/dữ liệu thực tế vì sao phương án mới tốt hơn hiện tại (triệt tiêu hiện tượng phán tự tin nhưng rỗng · `confidently hallucinating`).
   - `/recall`: Rút trích ngữ cảnh từ lịch sử hội thoại cũ (`transcripts`) thành bản tóm tắt trạng thái gọn sạch để nạp vào phiên mới mà không phải mò lại từ đầu.

---

## 5. Cơ Chế 4: `Working Backwards (Diátaxis + /unslop)`, `/prototype` & Đấu Trường 5 Pha `/architect`

Để xóa bỏ "ảo giác tiến độ" của các bản kế hoạch văn bản trừu tượng, Bước 3 (`VISION`) và Bước 4 (`BLUEPRINT`) bắt buộc thực thi lập kế hoạch bằng tài liệu người dùng và bằng code:

1. **Thiết kế Ngược từ README (`Working Backwards` & Khung 4 Ô `Diátaxis` + `/unslop`):**
   - Khi thiết kế module hoặc gói dùng chung, phải viết `Caller README` trước để đóng vai người gọi API, chia rõ 4 ô `Diátaxis`: `Tutorial` (hướng dẫn cầm tay cho người mới), `How-to` (kịch bản giải quyết tác vụ cụ thể), `Reference` (đặc tả tham số/kiểu trả về) và `Explanation` (lý do thiết kế & đánh đổi).
   - Chạy bộ lọc `/unslop` để cắt bỏ toàn bộ từ ngữ sáo rỗng của AI, giữ lại ví dụ code chạy được và thông số định lượng.
2. **Playbook `/prototype` (Nút chuyển giao diện trực tiếp · `Live UI Switcher`):**
   - Khi thiết kế giao diện hoặc luồng tương tác, dựng nhanh 2 đến 3 phương án ẩn sau một nút chuyển (`switcher` bật qua `./bin/control-app flag --set proto_variant=B`), chụp ảnh và đo đạc thực tế để chọn phương án thắng cuộc bằng bằng chứng thực nghiệm.
3. **Đấu Trường Kiến Trúc 5 Pha (`/architect Arena`):**
   - **Pha 1 (`Ground`):** Nạp kết quả `/how` và `/why` để khóa ranh giới sở hữu (`ownership`) và bất biến hệ thống.
   - **Pha 2 (`Sketch` · `Architecture Arena`):** Cho 2 đến 3 nhánh (đa model) độc lập phác thảo **`Type Signatures & Caller Usage Sketch`** (chỉ viết kiểu dữ liệu, chữ ký hàm và đoạn code nơi gọi hàm, **chưa viết thân hàm**).
   - **Pha 3 (`Cross-judge & Synthesize`):** Dùng một model độc lập làm trọng tài chấm điểm theo rubric (độ sâu module, tính an toàn kiểu, độ gọn của nơi gọi) và tổng hợp bản thiết kế tốt nhất.
   - **Pha 4 (`Implement against the sketch`):** Giao cho Thợ điền thân hàm thật theo TDD.
   - **Pha 5 (`Scrap when wrong`):** Nếu khi vào code thật phát hiện phải truyền thêm tham số vá víu qua nhiều tầng, lặp lại một workaround ở nhiều chỗ hoặc phải dùng `any` / ép kiểu cưỡng bức -> **Đập đi làm lại ngay từ Pha 2**, vì đó là bằng chứng thực nghiệm cho thấy kiến trúc đã sai.

---

## 6. Cơ Chế 5: Sổ Cái Bằng Chứng & Dấu Vân Tay Cây Làm Việc (`WTREE_FINGERPRINT`)

Mọi báo cáo kiểm thử, review code hoặc bàn giao giữa Thợ và Chủ thầu đều phải chạy đoạn lệnh chụp dấu vân tay trạng thái Git dưới đây và đính kèm vào đầu biên bản:

```bash
COMMIT_HASH="$(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')"
TREE_HASH="$(git rev-parse HEAD^{tree} 2>/dev/null || echo 'no-tree')"
DIRTY_COUNT="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
WTREE_SIG="$( (git status --porcelain; git diff HEAD) 2>/dev/null | shasum -a 256 | cut -c1-16 )"
echo "WTREE_FINGERPRINT: HEAD=${COMMIT_HASH} TREE=${TREE_HASH:0:12} WTREE=${WTREE_SIG} DIRTY_FILES=${DIRTY_COUNT}"
```

### Quy tắc Bất biến của Sổ cái:
- Một chứng nhận `REVIEW: CLEAR` hoặc `QA: PASS` chỉ có hiệu lực trên đúng cặp `(HEAD, WTREE)` tại thời điểm đóng dấu.
- Nếu bất kỳ tệp nào bị chỉnh sửa sau khi review (`WTREE` thay đổi), chứng nhận cũ tự động chuyển sang trạng thái `STALE` và bắt buộc phải chạy lại bước kiểm chứng.

---

## 7. Cơ Chế 6: Định Tuyến Điều Phối Song Song (`<= 10 Local Worktrees` vs. `> 10 Cloud Agents + /swarm`)

Dùng nhiều `git worktree` trên một máy tính cá nhân sẽ nhanh chóng chạm trần phần cứng (tốn dung lượng ổ cứng, đụng độ port/DB, tràn RAM) khi chạy vượt quá `~10` agents đồng thời. Vibecode Kit v6.2 phân tách rõ 2 tầng điều phối:

| Tiêu chí | Tầng 1: `Local Git Worktrees` (`<= 10 Agents`) | Tầng 2: `Coordinator Bot + Cloud Agents + /swarm` (`> 10 Agents`) |
|---|---|---|
| **Quy mô áp dụng** | Từ `2` đến tối đa `10` gói việc (`TIP`) độc lập. | Trên `10` nhánh song song, kiểm thử độ ổn định hàng loạt hoặc tự động tái hiện lỗi (`auto-repro`) từ Slack. |
| **Môi trường chạy** | Các thư mục `.worktrees/<task-id>` trên máy trạm cục bộ, phân bổ port và schema DB riêng biệt. | `Coordinator Bot` giữ context sạch trên máy điều phối và đẩy việc nặng sang `Cloud Agents` (máy ảo đám mây có snapshot khởi động tức thì và màn hình thật để quay video/chụp ảnh). |
| **Ràng buộc tệp tin** | Khóa cứng `owned_files` không giao nhau (`A ∩ B = ∅`) kèm cổng chặn `/freeze` & `/guard`. | Mỗi Cloud VM chạy một `sequence-verifiable-unit` hoặc một kịch bản `/swarm` độc lập và trả về gói bằng chứng (`JSON + screenshot/video + patch`). |
| **Vệ sinh hậu kỳ** | Dọn dẹp `git worktree remove` và xóa file plan tạm sau khi merge. | Hủy snapshot tạm sau khi thu hoạch bằng chứng và cập nhật `Feature Map` qua `/maintain-verification-skill`. |

### Cấu trúc Tệp Trạng Thái Điều Phối (`.vibecode/orchestrate-state.json`):
```json
{
  "epic_id": "EPIC-2026-10",
  "base_branch": "main",
  "base_commit": "a1b2c3d",
  "risk_tier": "R2",
  "execution_mode": "LOCAL_WORKTREES_OR_CLOUD_SWARM",
  "active_workers": 2,
  "hardware_ceiling_limit": 10,
  "tasks": [
    {
      "tip_id": "TIP-01",
      "sequence_unit": 1,
      "worker_role": "backend-builder",
      "worktree_path": ".worktrees/tip-01-api",
      "branch": "feat/tip-01-api",
      "owned_files": ["src/api/orders.ts", "tests/api/orders.test.ts"],
      "live_verification_cmd": "./bin/control-app dom --route /api/orders --json",
      "status": "COMPLETED",
      "scrap_triggered": false,
      "wtree_fingerprint": "HEAD=9f8e7d6 TREE=4c3b2a109876 WTREE=e0d1c2b3a4f56789 DIRTY_FILES=0"
    }
  ]
}
```
