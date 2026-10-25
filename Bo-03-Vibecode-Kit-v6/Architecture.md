# Architecture · Kiến trúc Kỹ thuật Vibecode Kit v6.1

## Tổng quan kiến trúc

Vibecode Kit v6.1 là một kiến trúc điều phối phát triển phần mềm lấy AI làm trung tâm, độc lập với ngôn ngữ lập trình và nền tảng lưu trữ. Ở phiên bản 6.1, kiến trúc bổ sung năm lớp hạ tầng kỹ thuật lấy cảm hứng từ `gstack` và `AgentKit (akkit)` gồm **Sổ cái Bằng chứng gắn Dấu vân tay Cây thư mục (Working-Tree Fingerprint Evidence Ledger)**, **Hợp đồng Chuyển giao có Che mật khẩu (Redacted Handoff Contract)**, **Không gian Thi công Cô lập Đa Thợ (Multi-Builder Worktree Isolation)**, **Cố vấn Kongming & Trọng tài Độc lập (Advisory & Arbiter Layer)** và **Đường ống Phát hành Hai Chặng (Dual-Stage Ship Pipeline)**.

Sơ đồ cấu trúc thư mục chuẩn của một dự án áp dụng Vibecode Kit v6.1.

```
Project-Root/ (Git repository)
│
├── vibecode-artifacts/                 Kho lưu trữ toàn bộ hiện vật của 8 bước
│   ├── scan-reports/                   Báo cáo khảo sát (SCAN-NNN.md + nhãn OBSERVED/ASSUMED)
│   ├── RRI-logs/                       Biên bản RRI, thẻ quyết định D<N> và Requirements Matrix
│   ├── blueprints/                     Bản vẽ khế ước (BP-NNN.md + kết quả 4-Lens / Red-Team)
│   ├── TIP/                            Gói giao việc (TIP-NNN.md + Scope Freeze + Failure Protocol)
│   ├── handoffs/                       Hợp đồng bàn giao chuyển phiên 9 mục đã che secret (HO-NNN.md)
│   ├── completion-reports/             Báo cáo hoàn thành của Thợ (CR-NNN.md + WTREE_FINGERPRINT)
│   ├── evidence-ledger/                Nhật ký bằng chứng chạy test và kết quả chấm của Arbiter
│   ├── calibration-cards/              Thẻ hiệu chỉnh 100 điểm và thu hoạch Shortcut Debt (CC-NNN.md)
│   ├── shortcut-ledger.csv             Sổ theo dõi các quyết định làm tắt (Completeness <= 7/10)
│   └── audit-trail.csv                 Nhật ký kiểm toán xuyên suốt mọi hành động
│
├── .worktrees/                         (Tùy chọn ở R2/R3) Các Git Worktree cô lập cho từng Thợ song song
│   ├── builder-tip-001/
│   └── builder-tip-002/
│
├── src/                                Mã nguồn sản phẩm (do Thợ viết trong ranh giới Scope Freeze)
├── tests/                              Bộ kiểm thử tự động (Unit, Integration, E2E, Regression)
├── docs/                               Tài liệu kỹ thuật và hướng dẫn sử dụng
└── AGENTS.md                           Chỉ dẫn gốc nạp tự động cho mọi AI Agent tham gia dự án
```

## Luồng vận hành chi tiết một chu kỳ Vibecode v6.1

```
START
  │
  ▼
Bước 1 · SCAN & X-RAY
  │  Thợ quét codebase, gắn nhãn nhận định (OBSERVED / DERIVED / PRIOR / ASSUMED)
  │  Lưu vibecode-artifacts/scan-reports/SCAN-NNN.md
  ▼
Phân loại Risk Tier (Impact × Reversibility -> R0 | R1 | R2 | R3)
  │
  ├── Nếu R0 ──► Viết TIP 1 dòng ──► BUILD (Scope Freeze) ──► VERIFY cơ học ──► Calibration 1 dòng ──► END
  │
  ▼
Bước 2 · RRI & DECISION BRIEFS (D<N>)
  │  Chủ thầu tự giải các câu Mechanical từ SCAN
  │  Trình các câu Taste và User Challenge qua thẻ D<N> (ELI10, Stakes, Completeness X/10)
  │  Ghi nhận Shortcut Debt vào shortcut-ledger.csv nếu chọn phương án Completeness <= 7/10
  ▼
Bước 3 · VISION & 4-LENS GATE
  │  Chủ thầu phác thảo kiến trúc + chạy Evolutionary Extension Trace (1 biến thể kế tiếp)
  │  Ở R2/R3, duyệt tuần tự qua 4 lăng kính. CEO -> Design (nếu có UI) -> DX (nếu có API/CLI) -> Eng
  ▼
Bước 4 · BLUEPRINT & RED-TEAM / ULTRA GATE
  │  Sinh vibecode-artifacts/blueprints/BP-NNN.md
  │  Ở R2/R3, chạy phản biện 4-Persona Red-Team (hoặc Ultra Best-of-5) + tham vấn Quân sư Kongming
  │  Con người ký duyệt APPROVED (nếu từ chối thì quay lại Bước 3)
  ▼
Bước 5 · TASK GRAPH & WORKTREE ALLOCATION
  │  Chủ thầu chia Blueprint thành các TIP-NNN.md có đồ thị phụ thuộc
  │  Kiểm tra Disjoint File Ownership (cấm 2 TIP song song sửa chung 1 file)
  │  Khởi tạo Git Worktree riêng cho từng luồng song song và gắn Failure Protocol (3-Strike Stop)
  ▼
Bước 6 · BUILD, CONSTRAINT LOOP & REDACTED HANDOFF
  │  Thợ thi công trong đúng Scope Freeze, ưu tiên Reuse Ladder
  │  Nếu đổi phiên/runtime giữa chừng, xuất HO-NNN.md (9 mục, che secret, chỉ rõ First safe step)
  │  Chạy test, chụp WTREE_FINGERPRINT và xuất Completion Report (CR-NNN.md)
  ▼
Bước 7 · VERIFY, SURFACE QA & INDEPENDENT ARBITER
  │  Kiểm tra WTREE_FINGERPRINT (đảm bảo bằng chứng FRESH, không STALE)
  │  Chạy QA trên bề mặt thật + Test Audit + viết test đỏ trước khi sửa xanh
  │  Ở R2/R3, phiên Trọng tài Độc lập (Arbiter C3) chấm chéo toàn bộ đầu ra với Blueprint
  ▼
Bước 8 · REFINE, DUAL-STAGE SHIP & CALIBRATION CARD
  │  Nếu có môi trường kép, chạy Dual-Stage Ship (hội tụ CI xanh ở Beta trước -> nâng lên Stable)
  │  Sau khi chạy thực tế, Chủ thầu lập Calibration Card (CC-NNN.md) phân bổ 100 điểm sai số
  │  Cập nhật trạng thái shortcut-ledger.csv và audit-trail.csv
  ▼
END CYCLE
```

## Đặc tả Kỹ thuật của 5 Thành phần Nâng cấp trong v6.1

### 1. Dấu vân tay Cây thư mục và Sổ cái Bằng chứng (Working-Tree Fingerprint & Evidence Ledger)

Trong môi trường làm việc với AI, lỗi phổ biến nhất là Thợ chạy bộ kiểm thử đạt kết quả xanh, sau đó sửa thêm vài dòng code "cho đẹp" rồi nộp báo cáo hoàn thành mà không chạy lại kiểm thử. Hoặc Thợ chỉ đọc file bằng mắt (`static-read`) nhưng lại báo cáo như thể đã chạy kiểm thử thực tế (`live-run`).

Để khóa chặt lỗ hổng này, Vibecode Kit v6.1 quy định cách tạo dấu vân tay nội dung cây thư mục (`WTREE_FINGERPRINT`) bằng lệnh chuẩn trên Unix/macOS.

```bash
# Tạo dấu vân tay nội dung toàn bộ mã nguồn đang theo dõi và file mới tạo
WTREE_FP=$( (git status --porcelain; git diff HEAD) | shasum -a 256 | cut -c1-16 )
echo "WTREE_FINGERPRINT. $WTREE_FP"
```

Mỗi bản ghi kiểm chứng trong `Completion Report` và `vibecode-artifacts/evidence-ledger/` phải khai báo minh bạch ba trường.
- **WTREE_FINGERPRINT.** Mã băm 16 ký tự của cây thư mục tại đúng thời điểm lệnh kiểm thử kết thúc.
- **EVIDENCE_KIND.** Cấp độ bằng chứng thực tế thuộc một trong năm mức `static-read`, `unit-test`, `fixture-replay`, `live-run`, `production`.
- **EVIDENCE_STATUS.** Trạng thái hiệu lực của bằng chứng. Chỉ đạt `FRESH` khi dấu vân tay hiện tại của cây thư mục trùng khớp tuyệt đối với dấu vân tay lúc chạy lệnh kiểm thử. Nếu lệch dù chỉ một ký tự trắng, trạng thái tự động chuyển thành `STALE` và bị chặn ở bước Verify.

### 2. Thẻ Quyết định `D<N>` và Sổ cái Nợ Làm tắt (Decision Briefs & Shortcut Debt Ledger)

Khi Chủ thầu cần trình một quyết định thuộc nhóm **Taste** hoặc **User Challenge** cho Con người ở bước RRI hoặc Blueprint, thẻ quyết định phải tuân theo cấu trúc chuẩn để Con người ra quyết định trong dưới 30 giây.

```markdown
### D01 · Chọn cơ chế lưu phiên đăng nhập cho ứng dụng
**Bối cảnh.** Nhánh feat/auth · Bước 2 RRI (Tầng User Challenge)
**Giải thích nhanh (ELI10).** Ứng dụng cần nhớ người dùng sau khi đăng nhập. Cách chọn sẽ quyết định việc chúng ta có thể khóa tài khoản bị lộ ngay lập tức hay phải đợi hết hạn tự nhiên.
**Rủi ro nếu chọn sai (Stakes).** Nếu dùng token không lưu trạng thái mà không có danh sách thu hồi, tài khoản bị đánh cắp vẫn truy cập được hệ thống cho tới khi token hết hạn.
**Khuyến nghị.** Chọn Phương án A vì đảm bảo an toàn thu hồi tức thì mà chỉ tốn thêm 10 phút thi công bằng AI.
**Độ hoàn thiện (Completeness).** A = 10/10, B = 7/10
**Thời gian thực hiện.** A (Thủ công 1 ngày / AI Builder 15 phút) · B (Thủ công 2 giờ / AI Builder 5 phút)

**Phương án A · Session lưu trong cơ sở dữ liệu kèm HttpOnly Cookie (recommended)**
- Ưu điểm 1. Thu hồi quyền truy cập của bất kỳ thiết bị nào ngay lập tức từ phía máy chủ.
- Ưu điểm 2. Không lộ token cho mã JavaScript phía trình duyệt, chống tấn công XSS đọc trộm.
- Nhược điểm. Cần thêm một bảng `sessions` và một truy vấn kiểm tra nhanh ở mỗi yêu cầu.

**Phương án B · JWT tự chứa không lưu trạng thái trên máy chủ (Stateless JWT)**
- Ưu điểm 1. Cài đặt cực nhanh, không cần tạo bảng mới trong cơ sở dữ liệu.
- Ưu điểm 2. Máy chủ xác thực chữ ký trực tiếp trong bộ nhớ mà không cần đọc đĩa.
- Nhược điểm. Không thể hủy phiên đơn lẻ ngay lập tức trước thời hạn nếu không xây thêm danh sách đen.

**Tổng kết đánh đổi (Net).** Đánh đổi thêm 1 bảng dữ liệu và 10 phút máy chạy để lấy khả năng kiểm soát bảo mật tuyệt đối.
```

Khi Con người chọn một phương án có điểm `Completeness <= 7/10` (như Phương án B ở trên), Chủ thầu ghi ngay vào `vibecode-artifacts/shortcut-ledger.csv` và Thợ gắn chú thích trực tiếp trong code theo mẫu.

```
// vibecode-shortcut(D01). Completeness 7/10. Upgrade when số lượng người dùng vượt 500 hoặc khi bật tính năng quản lý thiết bị đăng nhập.
```

Cơ chế này biến nợ kỹ thuật từ chỗ bị lãng quên thành một danh mục có điều kiện kích hoạt rõ ràng, được kiểm tra lại định kỳ ở bước Calibration.

### 3. Cô lập Không gian Thi công Đa Thợ (Multi-Builder Worktree Isolation & Disjoint Ownership)

Khi Task Graph ở Bước 5 chia dự án thành các TIP chạy song song (ví dụ `TIP-002` làm giao diện bảng điều khiển và `TIP-003` làm dịch vụ xuất báo cáo), Chủ thầu phải lập **Ma trận Sở hữu File (File Ownership Matrix)** trước khi phát lệnh Build.

```markdown
| Mã TIP | Thợ phụ trách | Nhánh & Worktree | Thư mục / File được phép ghi (Scope Freeze) | File dùng chung (Chỉ đọc) |
|---|---|---|---|---|
| TIP-001 | Builder-Core | main / worktree gốc | `src/types/shared.ts`, `src/db/schema.ts` | Không (chạy xong trước khi fan-out) |
| TIP-002 | Builder-UI | `.worktrees/tip-002` | `src/components/dashboard/**`, `tests/ui/**` | `src/types/shared.ts` (Frozen) |
| TIP-003 | Builder-API | `.worktrees/tip-003` | `src/services/export/**`, `tests/export/**` | `src/types/shared.ts`, `src/db/schema.ts` (Frozen) |
```

Cách khởi tạo và thu dọn Worktree chuẩn trên macOS/Linux.

```bash
# Chủ thầu tạo không gian cô lập cho từng Thợ từ nhánh cơ sở đã đóng băng contract
git worktree add -b feat/tip-002 .worktrees/tip-002 HEAD
git worktree add -b feat/tip-003 .worktrees/tip-003 HEAD

# Sau khi từng Thợ nộp Completion Report và qua cổng Arbiter C3 ở Bước 7
git merge --no-ff feat/tip-002 -m "feat(dashboard). tích hợp TIP-002 sau khi qua cổng Verify"
git merge --no-ff feat/tip-003 -m "feat(export). tích hợp TIP-003 sau khi qua cổng Verify"

# Chỉ gỡ worktree khi đã tích hợp thành công; giữ nguyên worktree lỗi để điều tra nếu thất bại
git worktree remove .worktrees/tip-002
git worktree remove .worktrees/tip-003
```

### 4. Hợp đồng Bàn giao Chuyển tiếp 9 mục có Che mật khẩu (Redacted Continuation Handoff)

Khi Chủ thầu (ví dụ trên Claude Chat) giao việc cho Thợ (ví dụ trên Antigravity hoặc Claude Code) thông qua Git repo, hoặc khi một phiên làm việc chuẩn bị đầy bộ nhớ ngữ cảnh cần chuyển sang phiên mới, hệ thống sử dụng chuẩn **Handoff 9 mục** tại `vibecode-artifacts/handoffs/HO-NNN.md`.

Chín mục bắt buộc theo đúng thứ tự gồm.
1. **Mission and current status** (Mục tiêu cần đạt, phần đã xong, phần còn lại).
2. **Scope and guardrails** (Thư mục làm việc, các file được phép sửa theo Scope Freeze, các hành động bị cấm).
3. **Current state** (Nhánh hiện tại, mã commit HEAD, `WTREE_FINGERPRINT`, danh sách file đang thay đổi).
4. **Decisions and rationale** (Các quyết định `D<N>` đã chốt và lý do loại bỏ các phương án khác).
5. **Work performed** (Những thay đổi và câu lệnh chính đã thực thi, đã che toàn bộ chuỗi nhạy cảm).
6. **Verification** (Các bài kiểm tra đã chạy kèm kết quả và những phần chưa kịp kiểm tra).
7. **Open risks and blockers** (Các câu hỏi mở, rủi ro tiềm ẩn hoặc rào cản bên ngoài).
8. **Exact next actions** (Danh sách hành động tiếp theo theo thứ tự, trong đó dòng đầu tiên bắt buộc đánh dấu `**First safe step.**`).
9. **Source pointers** (Đường dẫn tới TIP, Blueprint, Scan Report và các file mã nguồn trọng tâm).

Mọi nội dung trước khi ghi vào file Handoff phải đi qua bộ lọc **Redaction** để thay thế toàn bộ khóa API, chuỗi kết nối cơ sở dữ liệu, mật khẩu và giá trị trong `.env` bằng nhãn `[REDACTED:loại-khóa]`.

### 5. Đường ống Phát hành Hai Chặng và Vòng lặp Hiệu chỉnh (Dual-Stage Ship & Calibration Loop)

Ở Bước 8, đối với các dự án có phân tách môi trường thử nghiệm (`beta`, `dev`, `staging`) và môi trường chính thức (`main`, `master`, `stable`), quy trình phát hành hai chặng bảo vệ hệ thống khỏi các lỗi tích hợp muộn.

- **Chặng 1 · Hội tụ trên nhánh Beta.** Đẩy nhánh tính năng vào `beta`, chạy toàn bộ bộ kiểm thử tự động và QA bề mặt thật. Nếu CI trên nhánh `beta` báo đỏ do lỗi trong phạm vi dự án, tạo nhánh sửa lỗi tiếp nối và lặp lại cổng kiểm tra cho tới khi xanh hoàn toàn. Không bao giờ bước sang Chặng 2 khi nhánh `beta` còn đỏ hoặc đang treo.
- **Chặng 2 · Thăng cấp lên nhánh Stable.** Kiểm tra danh sách các commit sẽ được đưa từ `beta` lên `stable`. Nếu phát hiện có các commit lạ ngoài phạm vi TIP hiện tại bị cuốn theo, dừng lại và hỏi ý kiến Con người trước khi hợp nhất. Sau khi hợp nhất lên `stable` và xác nhận hệ thống vận hành xanh, đóng các mục kế hoạch liên quan.
- **Khép vòng bằng Calibration Card 100 điểm.** Sau khi sản phẩm đã phục vụ thực tế, Chủ thầu thu thập số liệu quan sát được, điền vào thẻ `CC-NNN.md`, chấm 100 điểm phân bổ sai số vào 4 giỏ (`Modeling`, `Timing`, `World-change`, `Execution`) và rút ra hành động cụ thể cho chu kỳ tiếp theo.

## Cấu hình Chỉ dẫn Chuẩn cho AI Agent (`AGENTS.md`)

Đặt file `AGENTS.md` sau ở thư mục gốc của dự án để mọi công cụ AI (Claude, Antigravity, Cursor, Codex) tự động tuân thủ chuẩn Vibecode Kit v6.1.

```markdown
# AGENTS.md · Quy ước Vận hành Vibecode Kit v6.1

File này là nguồn quy ước chung cho cả Chủ thầu (Contractor), Thợ thi công (Builder) và Trọng tài (Arbiter) trên kho mã nguồn này.

## 1. Giao thức Làm việc qua Git Repo
- Kho mã nguồn và thư mục `vibecode-artifacts/` là mặt bàn giao chính thức.
- Mọi nhận định kỹ thuật quan trọng phải phân biệt rõ 4 mức `OBSERVED`, `DERIVED`, `PRIOR`, `ASSUMED`.

## 2. Trách nhiệm của Chủ thầu (Contractor)
- Không viết code sản phẩm.
- Khảo sát hiện trạng trước khi hỏi. Phân loại quyết định thành `Mechanical`, `Taste`, `User Challenge`.
- Trình các quyết định quan trọng bằng thẻ `D<N>` có điểm `Completeness X/10`.
- Đảm bảo các TIP chạy song song có tập file sở hữu rời nhau (`Disjoint File Ownership`) trên các `git worktree` riêng.

## 3. Trách nhiệm của Thợ thi công (Builder)
- Chỉ sửa các file nằm trong mục `Scope Freeze` của TIP được giao.
- Dừng ngay lập tức và báo cáo nguyên văn log lỗi nếu kiểm chứng thất bại hoặc sửa 1 lỗi quá 3 lần không thành công (3-Strike Rule).
- Khi bàn giao giữa chừng, xuất file Handoff đủ 9 mục đã che sạch khóa bí mật (`[REDACTED]`).
- Khi hoàn thành TIP, bắt buộc chạy kiểm thử, lấy mã `WTREE_FINGERPRINT` và ghi đầy đủ `Completion Report`. Không bao giờ tuyên bố xong trong cửa sổ chat mà thiếu báo cáo và bằng chứng tươi (`FRESH`).
```

---

**Vibecode Kit v6.1** · Kiến trúc điều phối AI-Native chuẩn thực chiến.
