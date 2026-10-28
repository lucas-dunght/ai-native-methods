# Bộ 03 · Vibecode Kit v6.2 (`× pstack`)

> **Phương pháp Phát triển Phần mềm AI-First · 3 Vai trò + Đòn bẩy Tự Kiểm Chứng (`/control-app`) + Đấu trường Kiến trúc 5 Pha (`/architect`)**
> Phiên bản `2026.10` (`v6.2 · Vibecode × pstack`) · Hợp nhất 39 kỹ năng AgentKit (`ak-*`), 10 điểm mạnh thực chứng từ Claude Fable 5.1, toàn bộ hệ kỹ năng `gstack` và 2 trụ cột nền tảng `pstack` của `@poteto` (*Verification is all you need* & *The art of supervising someone smarter than you*).

## 1. Tại sao cần Vibecode Kit v6.2?

Trong kỷ nguyên các mô hình AI tiên tiến (Frontier Models) viết code nhanh hơn con người trên những codebase lớn hơn trí nhớ cá nhân, nút thắt cổ chai không còn nằm ở tốc độ gõ phím mà dịch chuyển sang **hai điểm nghẽn cốt lõi**:
1. **Thiếu Hạ tầng Tự Kiểm Chứng (`Verification Bottleneck`):** Nếu AI không thể tự chạy ứng dụng, tự thao tác giao diện/API, tự đọc log/trace và tự chụp bằng chứng để khép kín vòng lặp (`close the loop`), con người sẽ bị biến thành người ngồi canh (`babysitting`) và mọi tốc độ sinh code đều trở nên vô nghĩa.
2. **Hai Điểm Mù của Frontier Models & "Ảo giác Tiến độ" (`Supervision Bottleneck`):** Dù thông minh, mô hình vẫn thất bại vì (a) đầu bài mơ hồ (`under-specified intent`) và (b) thiếu ngữ cảnh lịch sử/hệ thống (`missing context`). Đồng thời, việc lập kế hoạch văn bản trừu tượng (`Plan Mode` truyền thống) dễ tạo ra "ảo giác tiến độ" (chi tiết hóa quá mức tiểu tiết cài đặt nhưng bỏ trống trải nghiệm người gọi API).

**Vibecode Kit v6.2** giải quyết triệt để cả hai điểm nghẽn thông qua mô hình **3 vai trò phối hợp**, **Đòn bẩy Hạ tầng CLI (`/control-app`)**, **Bộ nhớ Vật chất hóa (`Feature Map`)** và **Kỷ luật Giám sát & Lập kế hoạch bằng Code (`Indirect Prompting`, `/teach`, `Working Backwards Diátaxis`, `/prototype`, `5-Phase /architect Arena`, `Scrap when wrong`)**:

| Vai trò | Định danh | Trách nhiệm cốt lõi trong v6.2 |
|---|---|---|
| **Chủ nhà + Người làm vườn** | **Con người (`Homeowner` & `The Gardener`)** | Đặt bài toán, duyệt bản diễn đạt lại (`Indirect Prompting Restate`), chốt phương án ở cổng quyết định (`D<N>`), tuần tra dòng chảy PR để nhổ cỏ dại kiến trúc từ sớm (`The Gardener`) và nghiệm thu bằng chứng thực tế. |
| **Chủ thầu** | **AI Điều phối (`Contractor` / `Coordinator`)** | Chạy bộ tứ `/teach = /how + /why + /recall` và đọc `Feature Map` để nắm địa hình, điều hành `Working Backwards (Diátaxis + /unslop)`, dựng `/prototype` và mở đấu trường `5-Phase /architect Arena`, chia việc theo đơn vị `sequence-verifiable-units`, điều phối `Local Worktrees (<= 10)` hoặc `Cloud Agents + /swarm (> 10)` và gác cổng chất lượng. |
| **Thợ** | **AI Thực thi (`Builder`)** | Viết code theo TDD từ khung chữ ký kiểu (`Type Signatures & Caller Usage Sketch`), báo hiệu dừng ngay khi kiến trúc sai (`Scrap when wrong`), chạy đòn bẩy `./bin/control-app` để tự kiểm chứng sống (`Live Verification`) và đóng gói PR kèm mã băm `WTREE_FINGERPRINT`. |

---

## 2. Mười Sáu Nâng Cấp Cốt Lõi của v6.2 (`10 Nền tảng v6.1 + 6 Đòn bẩy pstack`)

### A. Mười Nền Tảng Thực Chứng từ v6.1 (Giữ nguyên 100%)
1. **Kỷ luật 4 Nhãn Khẳng định Fable 5.1 & Đạo đức Bằng chứng (`Unified 4-Label Claim Discipline`):** Phân tách `OBSERVED` (kèm `file:line`), `DERIVED` (`INFERRED`), `PRIOR` và `ASSUMED` (`UNVERIFIED`) đồng bộ 100% với Bộ 01 và Bộ 02. Cấm bịa kết quả test, đường dẫn file, mã commit hay thông số đo đạc.
2. **Dấu vân tay Cây làm việc (`WTREE_FINGERPRINT`) & CLI `scripts/bo03_vibecode_tool.py`:** Mọi biên bản kiểm thử, review và bàn giao phải đóng dấu bộ tứ `HEAD` + `WTREE` + `TREE` + `DIRTY` (hoặc chạy `python3 scripts/bo03_vibecode_tool.py wtree-fingerprint --dir . --json`). Thay đổi 1 dòng code làm vô hiệu hóa mọi dấu `CLEAR` trước đó.
3. **Bảng Quyết định Chuẩn hóa (`Decision Brief D<N>`):** Trình bày quyết định theo cấu trúc `ELI10`, điểm `Completeness X/10`, phân loại `Shortcut Debt` và nguyên tắc *"Boil the Lake"*.
4. **Cổng Duyệt Kế hoạch 4 Góc nhìn (`4-Lens Plan Gate`):** Duyệt kế hoạch qua 4 lăng kính tuần tự: **CEO / Phạm vi** -> **Thiết kế / UX** -> **Kỹ thuật / Kiến trúc** -> **Trải nghiệm Lập trình viên (DX)**.
5. **Điều phối Cô lập Nhánh & Tệp tin (`Disjoint Orchestration`):** Tách nhánh làm việc độc lập với danh sách `owned_files` không giao nhau và cổng chặn an toàn (`Safety Gates`).
6. **Tham vấn Quân sư Độc lập (`Kongming Advisory`):** Mời mô hình mạnh nhất đóng vai Quân sư độc lập khi gặp quyết định kiến trúc khó hoặc khi Thợ kẹt quá 2 vòng sửa lỗi.
7. **Hợp đồng Bàn giao Đã Khử Bí mật (`Redacted Handoff Contract`):** Đóng gói ngữ cảnh bàn giao giữa các phiên làm việc kèm cơ chế quét khử 100% khóa bí mật (`Secret Redaction`).
8. **Kiểm thử Theo Bề mặt & Trọng tài Độc lập (`Surface-Aware QA & Independent Arbiter`):** Kết hợp Trọng tài độc lập (`C3`) đối chiếu chéo với tiêu chí chấp nhận gốc trước khi cho phép phát hành.
9. **Phát hành Hai Giai đoạn & Đồng bộ Hậu phát hành (`Dual-Stage Ship & Post-Ship Sync`):** Phát hành qua 2 nhịp (`beta` -> `official`), tự động kiểm toán tài liệu và đồng bộ lên kho tri thức chung theo mã băm SHA-256.
10. **Thẻ Hiệu chuẩn 100 Điểm & Vòng lặp Tự hoàn thiện (`Calibration Card & Retro Loop`):** Chấm điểm chất lượng phiên làm việc trên thang 100 điểm và rút bài học sau mỗi chu kỳ.

### B. Sáu Đòn Bẩy Đột Phá Mới trong v6.2 (`Vibecode × pstack @poteto`)
11. **Đòn bẩy Hạ tầng Tự Kiểm Chứng (`Build the Lever · ./bin/control-app CLI`):** Thay vì chỉ viết hướng dẫn kiểm thử bằng chữ trong `SKILL.md` khiến Agent tốn hàng nghìn token viết script dùng một lần mỗi khi chạy, mỗi dự án phải đóng gói một CLI `./bin/control-app` theo 6 tiêu chuẩn *Deep Modules* của John Ousterhout: (1) `subcommands` dễ ghép nối, (2) cờ `--dry-run` bắt buộc cho mọi lệnh có tác dụng phụ, (3) thông báo lỗi chỉ dẫn trực tiếp lệnh tiếp theo cần chạy (`Actionable Error`), (4) `--help` chi tiết và đầu ra `--json` máy đọc được, (5) bao phủ trọn vẹn DX (seed DB, giả lập auth/test user, bật/tắt feature flag trong phiên, chụp DOM/a11y tree, chụp ảnh màn hình, đo hiệu năng) và (6) đóng vòng lặp kiểm chứng tự động (`close the loop`).
12. **Bộ nhớ Vật chất hóa (`Materialized Memory · Feature Map` & `/maintain-verification-skill`):** Duy trì bản đồ tra cứu nhanh từ góc nhìn người dùng tại `references/features/README.md` (danh mục tính năng, mục đích, đường dẫn và lệnh `./bin/control-app` để chạm tới). Chạy tác vụ bảo trì định kỳ `/maintain-verification-skill` để đối chiếu mã băm SHA-256 và giữ `Feature Map` không bị trôi (`drift`) so với codebase thật.
13. **Kỹ thuật "Diễn đạt lại bằng lời của bạn" (`Indirect Prompting`) & Bộ tứ `/teach = /how + /why + /recall`:** Khắc phục 2 điểm mù của Frontier Models bằng cách bắt buộc Chủ thầu đọc nguồn thông tin nhiễu và diễn đạt lại bản chất bài toán bằng lời tự nhiên (*"Restate in your own words and in plain English"*) trước khi đề xuất giải pháp. Xây dựng mô hình nhận thức hai chiều bằng `/how` (truy vết runtime đa luồng), `/why` (truy vết lịch sử Git/PR/ticket/log), `/teach` (dạy lại trực quan bằng dữ liệu thật để chặn ảo giác) và `/recall` (rút trích trạng thái từ lịch sử phiên cũ).
14. **Thiết kế Ngược từ README (`Working Backwards · 4 ô Diátaxis + /unslop`):** Chống "ảo giác tiến độ" của `Plan Mode` truyền thống bằng cách viết `README / Caller Tutorial` từ góc nhìn người gọi API trước khi thiết kế ruột hàm, phân tách rõ 4 ô `Diátaxis` (`Tutorial`, `How-to`, `Reference`, `Explanation`) và lọc sạch văn phong AI rườm rà qua `/unslop`.
15. **Lập Kế hoạch bằng Code (`/prototype` Switcher, `5-Phase /architect Arena` & Luật `Scrap when wrong`):** Với giao diện, dựng nhanh 2 đến 3 phương án ẩn sau nút chuyển trực tiếp (`Live UI Switcher` · `/prototype`) và dùng `./bin/control-app` chụp ảnh/đo đạc thực nghiệm. Với kiến trúc hệ thống, chạy 5 pha `/architect`: (1) `Ground` (`/how` + `/why`), (2) `Sketch` (cho nhiều nhánh/model độc lập viết `Type Signatures & Caller Usage Sketch` chưa có thân hàm), (3) `Cross-judge & Synthesize` (model trọng tài chấm điểm theo rubric và tổng hợp), (4) `Implement against the sketch` và (5) `Scrap when wrong` (đập đi làm lại ngay nếu khi vào code thật phải truyền tham số vá víu, lặp lại một workaround ở nhiều nơi hoặc dùng `any` / ép kiểu cưỡng bức).
16. **Vai trò "Người làm vườn" (`The Gardener`), Điều phối `Cloud /swarm (> 10 Agents)` & Vệ sinh File Plan Tạm:** Chia kế hoạch thực thi thành các đơn vị kiểm chứng độc lập (`sequence-verifiable-units`) gắn với `Live Verification`. Khi số lượng nhánh song song vượt ngưỡng trần phần cứng máy cá nhân (`> 10 local worktrees`), `Coordinator Bot` đẩy việc nặng sang `Cloud Agents` (môi trường ảo hóa có snapshot tức thì và màn hình thật) kết hợp `/swarm` để kiểm chứng độ ổn định hoặc tự động tái hiện lỗi (`auto-repro`) từ Slack. Sau khi merge PR, xóa hoặc chuyển lưu trữ file plan tạm để giữ sạch kho mã nguồn, giúp kỹ sư làm tròn vai trò **Người làm vườn (`The Gardener`)** tuần tra dòng chảy PR và nhổ cỏ dại kiến trúc từ trong trứng nước.

---

## 3. Cấu trúc Bộ Tài liệu (`Progressive Disclosure`)

| Tệp tin / Thư mục | Mục đích sử dụng |
|---|---|
| [`README.md`](./README.md) | Tổng quan triết lý, bảng phân vai và 16 nâng cấp cốt lõi của Vibecode Kit v6.2 (`× pstack`). |
| [`Methodology.md`](./Methodology.md) | Quy trình 8 bước tự co giãn theo cấp độ rủi ro (`R0 -> R3`) tích hợp `pstack` và ma trận kỹ năng. |
| [`Architecture.md`](./Architecture.md) | Kiến trúc kỹ thuật: Sổ cái bằng chứng, Đòn bẩy `./bin/control-app`, `Feature Map`, `5-Phase /architect Arena` và `Cloud /swarm`. |
| [`SKILL.md`](./SKILL.md) | Tệp chỉ dẫn gốc (System Prompt) nạp trực tiếp cho AI Agent khi kích hoạt kỹ năng `vibecode-kit-v6`. |
| [`scripts/bo03_vibecode_tool.py`](./scripts/bo03_vibecode_tool.py) | Công cụ CLI chuẩn 4 lớp (`init-control-app`, `wtree-fingerprint`, `maintain-features`, `constraint-check`, `--self-test`). |
| [`Quick-Start.md`](./Quick-Start.md) | Cẩm nang khởi động nhanh trong 5 phút kèm các câu lệnh mẫu. |
| [`references/`](./references/) | 6 tài liệu giao thức chuyên sâu (Claim Discipline, X-Ray & `/teach`, Plan Gates & `/architect`, Orchestrate & `/swarm`, QA & `/control-app`, Ship & Gardener). |
| [`templates/`](./templates/) | 9 biểu mẫu chuẩn hóa: `Risk-Tier`, `RRI`, `Blueprint`, `TIP`, `Control-App-and-Feature-Map`, `Handoff`, `Completion-Report`, `Audit-Trail`, `Calibration-Card`. |
| [`examples/worked-example.md`](./examples/worked-example.md) | Ví dụ thực chiến xuyên suốt từ bước đặt bài toán đến bước phát hành có đầy đủ `./bin/control-app`, `Feature Map`, `/architect Arena` và mã băm kiểm chứng. |
