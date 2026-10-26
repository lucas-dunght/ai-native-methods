# Changelog · `ai-native-methods`

Mọi thay đổi quan trọng của kho lưu trữ `ai-native-methods` đều được ghi nhận tại đây.

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
