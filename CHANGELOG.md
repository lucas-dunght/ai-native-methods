# Changelog · `ai-native-methods`

Mọi thay đổi quan trọng của kho lưu trữ `ai-native-methods` đều được ghi nhận tại đây.

## [2026.10.28] - 2026-10-28 · Nâng Cấp Chuẩn Tier-1 Full-Stack 4 Lớp & Đồng Bộ Toàn Diện 3 Bộ Kỹ Năng

### Added
- **Lớp Công cụ CLI Thực thi Tất định (`scripts/*.py` · Chuẩn Deep Module + Zero-Dependency Python stdlib):**
  - **Bộ 01 (`Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py`):** Bổ sung 4 lệnh tất định `ptc-filter` (cắt cửa sổ ngữ cảnh ~1.200 ký tự, lọc >80% rác HTML, gắn cờ `untrusted_external_content`), `audit-echo` (kiểm toán độc lập nguồn gốc và phát hiện cụm phòng vang), `gate-check` (chấm 4 tiêu chí cổng định lượng) và `export-bo02` (xuất `Fact Card` sang `L1-stored-fact.yaml` kèm ánh xạ 4 nhãn Fable 5.1) cùng bộ tự kiểm thử `--self-test --json` (`< 25ms`).
  - **Bộ 02 (`Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py` & `scripts/eval_l2.py`):** Hiện thực hóa `fingerprint` (`ORIGINAL_TREE_FINGERPRINT` SHA-256 luồng 64KB), `audit-freshness` (kiểm toán `FRESH/STALE/EXPIRED` và lan truyền `STALE` qua `dependency-index.csv`), `eval-l2` (tính công thức `L2` bằng trình thông dịch **AST Safe Evaluator** chặn 100% thực thi mã tùy ý, kèm wrapper tương thích ngược `scripts/eval_l2.py`) và `sync-feature-map` cùng `--self-test --json`.
  - **Bộ 03 (`Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py`):** Hiện thực hóa `init-control-app` (sinh khung `./bin/control-app`), `wtree-fingerprint` (chụp và đối chiếu dấu vân tay cây làm việc), `maintain-features` (đồng bộ mã băm SHA-256 cho `Feature Map`) và `constraint-check` (kiểm toán tự động `0` dấu `em-dash`, `0` cụm `dấu phẩy trước chữ và` và `0` rò rỉ khóa bí mật) cùng `--self-test --json`.
- **Tài liệu Thiết kế CEO (`docs/designs/optimize-3-skill-suites.md`):** Quảng bá bản kế hoạch tối ưu hóa toàn diện 3 Bộ kỹ năng (đã duyệt qua `/plan-ceo-review` ở chế độ `SELECTIVE EXPANSION` với điểm Spec Review `9.8/10`).

### Changed
- **Đồng bộ Phân tầng Co giãn `R0–R3` & `Indirect Prompting Restate` sang Bộ 01 và Bộ 02:**
  - Tinh gọn `Bo-01/SKILL.md` (`170 -> 79` dòng) và `Bo-02/SKILL.md` (`128 -> 62` dòng) theo nguyên lý `Progressive Disclosure`.
  - Nhúng khung `Indirect Prompting Restate`, bảng chọn nhanh `R0–R3 Fast-Track` và lệnh gọi CLI vào `Quick-Start.md` cùng `templates/` của Bộ 01 và Bộ 02.
- **Hợp nhất Ma trận 4 Nhãn Nhận định Fable 5.1 xuyên 3 Bộ (`OBSERVED | DERIVED | PRIOR | ASSUMED`):**
  - Chuẩn hóa bảng ánh xạ 1-1 giữa `OBSERVED / DERIVED / PRIOR / ASSUMED` (Bộ 01 & Bộ 03) với `EXTRACTED / INFERRED / AMBIGUOUS` (Bộ 02) trong `Bo-02/references/bo01-bo02-bo03-bridge.md` và `Bo-03/references/claim-and-evidence-protocol.md`.
- **Nâng cấp `tools/install-all.sh` & Dọn dẹp Thư mục Gốc:**
  - Chuyển 8 tệp `.docx`/`.skill` có hậu tố phiên bản trùng lặp ở thư mục gốc vào `_Archive/duplicate-deliverables-2026-10/`, chỉ giữ bộ tệp chuẩn duy nhất ở root.
  - Nâng cấp `tools/install-all.sh` để chạy cổng kiểm thử sống `--self-test --json` trên cả 3 CLI và đồng bộ cả 3 Bộ kỹ năng vào `~/.gemini/config/skills/` lẫn `~/.claude/skills/`.

## [2026.10] - 2026-10-26

### Added
- **Bộ 03 (`Bo-03-Vibecode-Kit-v6` · `v6.2 × pstack @poteto`):**
  - Thêm biểu mẫu thực thi thứ 9 [`Bo-03-Vibecode-Kit-v6/templates/Control-App-and-Feature-Map.md`](./Bo-03-Vibecode-Kit-v6/templates/Control-App-and-Feature-Map.md) cung cấp khung CLI `./bin/control-app` đạt 6 tiêu chuẩn *Deep Modules* của John Ousterhout (`subcommands`, `--dry-run`, thông báo lỗi chỉ dẫn lệnh tiếp theo `next_command`, `--json`, bao phủ trọn DX: `seed`, `auth`, `flag`, `dom`, `screenshot`, `perf`, `doctor`) và bản đồ `Feature Map` (`references/features/README.md`) kèm quy trình `/maintain-verification-skill`.
  - Thêm Cẩm nang Toàn trình làm sản phẩm AI-Native từ A đến Z (`v2.2`) tại [`docs/cam-nang-lam-san-pham-a-den-z.md`](./docs/cam-nang-lam-san-pham-a-den-z.md) và đóng gói [`Cam-Nang-Lam-San-Pham-AI-Native-A-Den-Z.docx`](./Cam-Nang-Lam-San-Pham-AI-Native-A-Den-Z.docx).
- **Nhật ký phát hành & Hiệu chuẩn (`plans/journals/`):**
  - Thêm biên bản phát hành và Thẻ Hiệu chuẩn 100 điểm (`99/100 · GOLD STANDARD`) cho đợt nâng cấp `v6.2 × pstack` (PR `#6` / Issue `#5`).

### Changed
- **Bộ 03 (`Bo-03-Vibecode-Kit-v6/`):** Nâng cấp toàn bộ 21 tệp Markdown từ `v6.1` lên `v6.2 (× pstack @poteto)`:
  - Tích hợp `Indirect Prompting Restate` (*"Restate in your own words"*) và bộ tứ `/teach = /how + /why + /recall` vào Bước 1-2 (`SCAN` & `RRI`).
  - Tích hợp `Working Backwards` (`Caller README` theo 4 ô `Diátaxis` + `/unslop`), thực nghiệm giao diện `/prototype` (`Live UI Switcher`) và đấu trường kiến trúc 5 pha `/architect Arena` (`Ground -> Sketch Type Signatures -> Cross-judge -> Implement -> Scrap when wrong`) vào Bước 3-4 (`VISION` & `BLUEPRINT`).
  - Tích hợp đơn vị kiểm chứng độc lập (`sequence-verifiable-units`), định tuyến `<= 10 Local Worktrees` vs. `> 10 Coordinator + Cloud Agents + /swarm` (`auto-repro`), vai trò `The Gardener` và quy tắc xóa/lưu trữ file plan tạm sau khi merge vào Bước 5-8.
- **Bộ 02 (`Bo-02-Kernel-Registry-SOT/`) & Bộ 01 (`Bo-01-Tinh-Loc-Thong-Tin-Internet/`):** Cập nhật cầu nối kiểm toán mã băm SHA-256 với `Feature Map` (`references/features/README.md`) của Bộ 03 `v6.2`.
- **Đóng gói `.skill` & `.docx`:** Cập nhật `vibecode-kit-v6.skill`, `vibecode-kit-v6.2.skill`, `Bo-03-Vibecode-Kit-v6.docx`, `Bo-03-Vibecode-Kit-v6.2.docx` và `0-Tong-Quan-Chuyen-Giao.docx`.
