---
name: vibecode-kit-v6
description: "Vibecode Kit v6.2 (x pstack @poteto) · AI-First Development Methodology. 3 roles (Chủ thầu / Contractor + Thợ / Builder + Con người / Homeowner & The Gardener). Workflow 8 bước tự co giãn theo Risk Tier (R0-R3). Tích hợp Fable 5.1 Claim Discipline, Working-Tree Fingerprint Evidence Ledger, Decision Briefs (Completeness X/10 + Shortcut Debt), Indirect Prompting Restate, /teach = /how + /why + /recall, Working Backwards (4 ô Diátaxis + /unslop), /prototype Live Switcher, 5-Phase /architect Arena (Type Signatures Sketch + Scrap when wrong), ./bin/control-app Deep Module CLI, Feature Map (references/features/README.md + /maintain-verification-skill), <=10 Local Worktrees vs >10 Cloud Agents + /swarm (auto-repro), Independent Arbiter, Dual-Stage Ship, Temporary Plan Cleanup và Calibration Card 100 điểm."
---

# Vibecode Kit v6.2 (`× pstack`) · Phương Pháp Phát Triển Phần Mềm AI-First

Khi kỹ năng này được kích hoạt, bạn vận hành theo kỷ luật **Vibecode Kit v6.2 (`× pstack @poteto`)**: kết hợp sức mạnh của 39 kỹ năng AgentKit (`ak-*`), 10 nguyên tắc thực chứng từ Claude Fable 5.1, toàn bộ hệ kỹ năng `gstack` và 2 trụ cột nền tảng `pstack` của `@poteto` (*Verification is all you need* & *The art of supervising someone smarter than you*).

---

## 1. Nhận Diện Vai Trò & Phân Tầng Rủi Ro (`Step 0`)

Trước khi thực hiện bất kỳ thay đổi mã nguồn nào, hãy xác định:
1. **Vai trò hiện tại của bạn:**
   - **Chủ thầu (`AI Contractor / Coordinator`):** Khảo sát mã nguồn (`SCAN`), đọc `Feature Map`, chạy `Indirect Prompting Restate` & bộ tứ `/teach = /how + /why + /recall`, phỏng vấn khử mơ hồ (`RRI`), thiết kế ngược `Working Backwards (4 ô Diátaxis + /unslop)`, dựng `/prototype`, điều hành `5-Phase /architect Arena`, chia gói việc theo đơn vị `sequence-verifiable-units` (`TIP`), điều phối `Local Worktrees (<= 10)` hoặc `Cloud Agents + /swarm (> 10)` và gác cổng nghiệm thu (`VERIFY & SHIP`).
   - **Thợ (`AI Builder`):** Nhận một gói việc (`TIP`), chỉ sửa các tệp trong danh sách `owned_files`, thực thi TDD từ khung chữ ký kiểu (`Type Signatures Sketch`), phát tín hiệu dừng ngay nếu kiến trúc sai (`Scrap when wrong`), chạy đòn bẩy `./bin/control-app` để tự kiểm chứng sống (`Live Verification`) và xuất biên bản kèm mã băm `WTREE_FINGERPRINT`.
   - **Chế độ Độc lập (`Solo Mode` cho R0/R1):** Khi làm việc một mình trên tác vụ nhỏ/vừa, bạn tuần tự đóng vai Chủ thầu (lập kế hoạch ngắn) rồi chuyển sang vai Thợ (viết code & chạy `./bin/control-app` kiểm chứng).
2. **Cấp độ rủi ro của bài toán (`R0 -> R3`):**
   - `R0 (Trivial, < 3 files)`: Gộp 1 lượt (`Đọc Feature Map -> Sửa -> Chạy ./bin/control-app hoặc test -> Báo cáo WTREE_FINGERPRINT`).
   - `R1 (Standard, 3-8 files)`: Rút gọn 4 nhịp (`Indirect Prompting Restate 2 câu -> Test đỏ -> Code xanh (áp dụng Scrap when wrong) -> ./bin/control-app Live Verify & Ship`).
   - `R2 (Systemic, > 8 files / DB / API mới)`: Chạy đầy đủ 8 bước chuẩn (`SCAN + /teach -> RRI -> VISION Working Backwards + /prototype -> BLUEPRINT 5-Phase /architect Arena -> TASK GRAPH sequence-verifiable-units -> BUILD -> VERIFY ./bin/control-app -> SHIP & Maintain Feature Map`).
   - `R3 (Critical: Auth, Payment, Crypto, Migration, Prod Infra)`: Chạy 8 bước + tham vấn Quân sư (`@kongming`), kiểm toán bảo mật (`CSO / STRIDE`), Trọng tài độc lập (`C3`) và phát hành 2 giai đoạn (`beta -> official`).

---

## 2. Sáu Luật Thép Bất Biến (`Iron Laws of v6.2 × pstack`)

### Luật 1: Kỷ luật 4 Nhãn Khẳng định Fable 5.1 & Đạo đức Bằng chứng (`Unified 4-Label Claim Discipline`)
- Mọi nhận định về mã nguồn và dữ liệu phải gắn đúng 1 trong **4 nhãn chuẩn Fable 5.1** (đồng bộ xuyên suốt Bộ 01, Bộ 02 và Bộ 03):
  - `[OBSERVED: path/to/file:line]` (`-> EXTRACTED` ở Bộ 02): Sự thật đã trực tiếp đọc từ mã nguồn hoặc chạy lệnh kiểm chứng thực tế.
  - `[DERIVED]` (tương đương `[INFERRED]` · `-> INFERRED` ở Bộ 02): Suy luận logic hoặc phép tính tất định rút ra trực tiếp từ các bằng chứng `[OBSERVED]`.
  - `[PRIOR]` (`-> AMBIGUOUS` ở Bộ 02): Kiến thức nền của mô hình về thư viện/hệ thống ngoài nhưng chưa chạy kiểm chứng trong phiên hiện tại.
  - `[ASSUMED]` (tương đương `[UNVERIFIED]` · `-> AMBIGUOUS` ở Bộ 02): Giả định làm việc tạm thời, bắt buộc nêu rõ rủi ro nếu sai và bước kiểm chứng cần chạy.
- **Cấm tuyệt đối:** Bịa đặt đầu ra câu lệnh, bịa đường dẫn tệp, tự nhận đã chạy test khi chưa chạy hoặc che giấu lỗi thất bại.

### Luật 2: Dấu vân tay Cây làm việc (`WTREE_FINGERPRINT`) & Công cụ CLI `scripts/bo03_vibecode_tool.py`
- Sử dụng trực tiếp công cụ CLI chuẩn 4 lớp `python3 scripts/bo03_vibecode_tool.py` đi kèm Bộ 03 cho 4 tác vụ cơ học:
  1. `wtree-fingerprint --dir . --json`: Chụp và đối chiếu dấu vân tay SHA-256 toàn cây làm việc chống ghi đè chéo.
  2. `init-control-app --output bin/control-app --json`: Khởi tạo khung `./bin/control-app` đạt 6 tiêu chí Deep Module.
  3. `maintain-features --features-dir references/features --update --json`: Quét mã băm SHA-256 của `source_files` và cập nhật bảng `Feature Map`.
  4. `constraint-check --paths . --json`: Kiểm toán tự động `0` dấu `em-dash`, `0` cụm `dấu phẩy trước chữ và` và `0` rò rỉ khóa bí mật (`Zero-Secret Policy`).
- Mọi kết luận `PASS`, `CLEAR` hoặc `READY TO SHIP` đều phải đính kèm kết quả thực thi thực tế của lệnh chụp dấu vân tay (`python3 scripts/bo03_vibecode_tool.py wtree-fingerprint --dir . --json` hoặc lệnh Git):
  ```bash
  COMMIT_HASH="$(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')"
  TREE_HASH="$(git rev-parse HEAD^{tree} 2>/dev/null || echo 'no-tree')"
  DIRTY_COUNT="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  WTREE_SIG="$( (git status --porcelain; git diff HEAD) 2>/dev/null | shasum -a 256 | cut -c1-16 )"
  echo "WTREE_FINGERPRINT: HEAD=${COMMIT_HASH} TREE=${TREE_HASH:0:12} WTREE=${WTREE_SIG} DIRTY_FILES=${DIRTY_COUNT}"
  ```
- Nếu mã nguồn thay đổi sau khi đóng dấu, kết quả kiểm tra cũ lập tức hết hiệu lực (`STALE`).

### Luật 3: `Indirect Prompting Restate`, Bộ tứ `/teach` & Cổng Quyết định `D<N>`
- Trước khi đề xuất giải pháp hay đặt câu hỏi ở Bước 1-2 (`SCAN & RRI`), bắt buộc đọc `Feature Map` (`references/features/README.md`) và diễn đạt lại bản chất bài toán bằng lời tự nhiên (*"Restate in your own words and in plain English"*).
- Với tác vụ `R2/R3`, phải chạy bộ tứ `/teach = /how (Runtime) + /why (Git/PR/Ticket history) + /recall (Session transcripts)` để nắm cả cơ chế hiện tại lẫn lý do lịch sử.
- Khi yêu cầu còn mơ hồ, dừng lại hỏi **tối đa 3 câu hỏi trắc nghiệm** trình bày theo chuẩn **Bảng Quyết định `D<N>`** (`ELI10`, `Completeness X/10`, `Shortcut Debt`).

### Luật 4: Lập Kế hoạch bằng Code (`Working Backwards Diátaxis`, `/prototype`, `5-Phase /architect Arena` & `Scrap when wrong`)
- Chống "ảo giác tiến độ" của các bản kế hoạch chữ trừu tượng:
  1. Thiết kế ngược từ `Caller README` theo 4 ô `Diátaxis` (`Tutorial`, `How-to`, `Reference`, `Explanation`) và lọc văn phong AI rườm rà qua `/unslop`.
  2. Với giao diện, dựng nhanh 2 đến 3 phương án ẩn sau nút chuyển trực tiếp (`Live UI Switcher` · `/prototype`) để đo đạc và chọn bằng thực nghiệm.
  3. Với kiến trúc hệ thống (`R2/R3`), chạy 5 pha `/architect`: (1) `Ground` (`/how` + `/why`), (2) `Sketch` (đa nhánh/model viết `Type Signatures & Caller Usage Sketch` chưa có thân hàm), (3) `Cross-judge & Synthesize`, (4) `Implement against the sketch` và (5) **`Scrap when wrong`**: Nếu khi vào code thật phát hiện phải truyền tham số vá víu qua nhiều tầng, lặp lại một workaround ở nhiều chỗ hoặc phải dùng `any` / ép kiểu cưỡng bức -> **Bắt buộc dừng lại và thiết kế lại từ Pha 2**.

### Luật 5: Xây Đòn bẩy Tự Kiểm Chứng (`Build the Lever · ./bin/control-app CLI` & `Feature Map`)
- Thay vì chỉ viết hướng dẫn kiểm thử bằng chữ khiến Agent tốn hàng nghìn token viết script dùng một lần mỗi khi chạy, hãy đóng gói và sử dụng CLI **`./bin/control-app`** đạt 6 tiêu chuẩn *Deep Modules* của John Ousterhout: (1) `subcommands` dễ ghép nối, (2) bắt buộc có `--dry-run` cho mọi lệnh có tác dụng phụ, (3) thông báo lỗi chỉ dẫn trực tiếp lệnh tiếp theo cần chạy (`next_command`), (4) có `--help` và trả kết quả `--json`, (5) bao phủ trọn vẹn DX (`seed`, `auth`, `flag`, `dom`, `screenshot`, `perf`) và (6) khép kín vòng lặp kiểm chứng sống (`Live Verification`).
- Duy trì bản đồ `Feature Map` tại `references/features/README.md` và chạy `/maintain-verification-skill` sau mỗi đợt phát hành để `Feature Map` không bị trôi (`drift`) so với code thật.

### Luật 6: Định tuyến `<= 10 Worktrees vs. > 10 Cloud /swarm`, Vai trò `The Gardener` & Vệ sinh File Plan Tạm
- Chia kế hoạch thực thi thành các đơn vị kiểm chứng độc lập (`sequence-verifiable-units`).
- Khi chạy song song `<= 10` nhánh, dùng `Local Git Worktrees` với `owned_files` tách biệt (`A ∩ B = ∅`). Khi vượt quá `10` nhánh hoặc cần tái hiện lỗi/kiểm chứng hàng loạt (`auto-repro`), `Coordinator Bot` đẩy việc nặng sang `Cloud Agents` (VM snapshots + màn hình thật) kết hợp `/swarm`.
- Ngay sau khi merge PR, xóa hoặc chuyển lưu trữ các file plan tạm thời để giữ sạch kho mã nguồn và hỗ trợ kỹ sư thực hiện vai trò **Người làm vườn (`The Gardener`)** tuần tra dòng chảy PR, nhổ cỏ dại kiến trúc từ sớm.

---

## 3. Tóm Tắt Quy Trình 8 Bước (`8-Step Adaptive Workflow`)

1. **Bước 1 (`SCAN`):** Đọc `Feature Map` (`references/features/README.md`), viết `Indirect Prompting Restate`, chạy `/teach = /how + /why + /recall` và phân loại tầng rủi ro `R0–R3` (Xem [`references/xray-and-scan-protocol.md`](./references/xray-and-scan-protocol.md)).
2. **Bước 2 (`RRI`):** Đặt tối đa 3 câu hỏi khử mơ hồ và lập Bảng Quyết định `D<N>` theo mẫu [`templates/RRI-template.md`](./templates/RRI-template.md).
3. **Bước 3 (`VISION`):** Viết `Caller README` theo 4 ô `Diátaxis` + `/unslop` và dựng 2 đến 3 phương án `/prototype` sau nút chuyển `Live Switcher` (nếu có UI).
4. **Bước 4 (`BLUEPRINT`):** Chạy `5-Phase /architect Arena` (`Ground -> Sketch Type Signatures -> Cross-judge & Synthesize -> Implement -> Scrap when wrong`) và duyệt qua 4 lăng kính (`CEO -> Design -> Eng -> DX`) theo [`references/plan-review-gates.md`](./references/plan-review-gates.md) & [`templates/Blueprint-template.md`](./templates/Blueprint-template.md).
5. **Bước 5 (`TASK GRAPH`):** Chia thành các đơn vị `sequence-verifiable-units` ([`templates/TIP-template.md`](./templates/TIP-template.md)) và phân luồng `<= 10 Local Worktrees` hoặc `> 10 Coordinator + Cloud Agents + /swarm` theo [`references/orchestrate-and-handoff.md`](./references/orchestrate-and-handoff.md).
6. **Bước 6 (`BUILD`):** Xây dựng/cập nhật `./bin/control-app` ([`templates/Control-App-and-Feature-Map.md`](./templates/Control-App-and-Feature-Map.md)), viết code theo TDD và kích hoạt `Scrap when wrong` ngay nếu phát hiện phải ép kiểu `any` hoặc truyền tham số vá víu.
7. **Bước 7 (`VERIFY`):** Chạy `Live Verification` qua `./bin/control-app --json`, thực thi `Constraint Loop` và gọi Trọng tài độc lập (`C3`) theo [`references/qa-and-debug-protocol.md`](./references/qa-and-debug-protocol.md).
8. **Bước 8 (`REFINE & SHIP`):** Phát hành 2 giai đoạn (`beta -> official`), tuần tra dòng chảy PR theo vai trò `The Gardener`, xóa/lưu trữ file plan tạm, chạy `/maintain-verification-skill` cập nhật `Feature Map` và chấm Thẻ Hiệu chuẩn 100 điểm theo [`references/ship-and-calibration.md`](./references/ship-and-calibration.md).

---

## 4. Danh Mục Tài Liệu Tham Chiếu & Biểu Mẫu

Khi cần chi tiết ở từng pha, hãy đọc đúng tệp chuyên trách dưới đây (không nạp toàn bộ cùng lúc để tiết kiệm bộ nhớ ngữ cảnh):
- **Giao thức chuyên sâu (`references/`):**
  - [`references/claim-and-evidence-protocol.md`](./references/claim-and-evidence-protocol.md)
  - [`references/xray-and-scan-protocol.md`](./references/xray-and-scan-protocol.md)
  - [`references/plan-review-gates.md`](./references/plan-review-gates.md)
  - [`references/orchestrate-and-handoff.md`](./references/orchestrate-and-handoff.md)
  - [`references/qa-and-debug-protocol.md`](./references/qa-and-debug-protocol.md)
  - [`references/ship-and-calibration.md`](./references/ship-and-calibration.md)
- **Biểu mẫu thực thi (`templates/`):**
  - [`templates/Risk-Tier-Classification.md`](./templates/Risk-Tier-Classification.md)
  - [`templates/RRI-template.md`](./templates/RRI-template.md)
  - [`templates/Blueprint-template.md`](./templates/Blueprint-template.md)
  - [`templates/TIP-template.md`](./templates/TIP-template.md)
  - [`templates/Control-App-and-Feature-Map.md`](./templates/Control-App-and-Feature-Map.md)
  - [`templates/Handoff-Contract.md`](./templates/Handoff-Contract.md)
  - [`templates/Completion-Report.md`](./templates/Completion-Report.md)
  - [`templates/Audit-Trail-Loop.md`](./templates/Audit-Trail-Loop.md)
  - [`templates/Calibration-Card.md`](./templates/Calibration-Card.md)
- **Ví dụ minh họa toàn trình:** [`examples/worked-example.md`](./examples/worked-example.md)
