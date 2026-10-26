# CLAUDE.md · Chỉ Dẫn Điều Phối AI Agent Cho Kho Lưu Trữ `ai-native-methods` (`2026.10`)

Kho lưu trữ này chứa **3 Bộ Phương Pháp Làm Việc Cùng AI** cùng toàn bộ hệ sinh thái công cụ thực thi nằm trong thư mục [`tools/`](./tools/) và bộ tài liệu hướng dẫn kỹ thuật trong [`docs/`](./docs/).

---

## 1. Cấu Trúc Kho Lưu Trữ & Khởi Tạo Nhanh

- `Bo-01-Tinh-Loc-Thong-Tin-Internet/` (`internet-info-refinement` v2.0): Phương pháp tinh lọc và làm giàu thông tin từ internet qua 7 giai đoạn.
- `Bo-02-Kernel-Registry-SOT/` (`kernel-registry-sot` v2.0): Phương pháp quản trị Nguồn Sự Thật Đa Xuất Xứ (`L1 / L2 / L3 / L4`) kết nối mã băm SHA-256 với `Feature Map`.
- `Bo-03-Vibecode-Kit-v6/` (`vibecode-kit-v6` v6.2 × `pstack`): Phương pháp xây dựng và phát hành phần mềm điều phối đa tác tử theo 8 bước co giãn theo tầng rủi ro `R0..R3`, tích hợp Đòn bẩy `./bin/control-app` CLI (Deep Module), `Feature Map` (`references/features/README.md` + `/maintain-verification-skill`), `Indirect Prompting Restate`, bộ tứ `/teach = /how + /why + /recall`, `Working Backwards (4 ô Diátaxis + /unslop)`, `/prototype` Switcher, `5-Phase /architect Arena (Type Signatures Sketch + Scrap when wrong)` và định tuyến `<= 10 Local Worktrees` vs `> 10 Coordinator + Cloud Agents + /swarm`.
- `tools/`: Chứa trình cài đặt 1 lệnh `./tools/install-all.sh`, máy chủ MCP `unified-search` (`tools/unified-search-mcp/`), 58 kỹ năng phụ trợ (`tools/skills/{tavily,akkit,gstack}/`), 21 tiện ích dòng lệnh (`tools/gstack-bin/`) và 13 mô-đun kiểm định (`tools/hooks/`).
- `docs/`: Bộ tài liệu hướng dẫn công cụ và cấu hình API theo chuẩn Diataxis 4 góc nhìn (`Tutorial`, `How-To`, `Reference`, `Explanation`) cùng Cẩm nang Toàn trình làm sản phẩm AI-Native từ A đến Z ([`docs/cam-nang-lam-san-pham-a-den-z.md`](./docs/cam-nang-lam-san-pham-a-den-z.md)).

---

## 2. Quy Tắc An Ninh & Bảo Mật Khóa API (`Zero-Secret Policy`)

1. **Không bao giờ đưa API Key hoặc Token vào Git.** Mọi khóa API (`TAVILY_KEY_POOL`, `EXA_KEY_POOL`, `LINKUP_KEY_POOL`, `TAVILY_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`) bắt buộc lưu tại `~/.mcp_env` (quyền `0600`, nằm ngoài kho lưu trữ). Trong kho lưu trữ chỉ lưu file mẫu [`tools/unified-search-mcp/.mcp_env.example`](./tools/unified-search-mcp/.mcp_env.example).
2. **Kiểm tra chống rò rỉ trước khi commit/push.** Luôn chạy kiểm tra bằng `./tools/gstack-bin/gstack-redact` hoặc xác nhận không có chuỗi khóa thật trước khi đẩy mã nguồn lên GitHub.
3. **Quy tắc văn phong kho lưu trữ (`Constraint Loop`).** Mọi tài liệu Markdown tiếng Việt trong kho lưu trữ này tuân thủ hai quy tắc cơ học:
   - Không sử dụng dấu gạch ngang dài (`em-dash`). Thay bằng dấu chấm, dấu phẩy hoặc dấu chấm giữa `·`.
   - Không đặt dấu phẩy ngay trước chữ `"và"`.

---

## 3. Bảng Định Tuyến Kỹ Năng (`Skill Routing`)

Khi yêu cầu của người dùng khớp với một trong các tác vụ dưới đây, hãy ưu tiên kích hoạt kỹ năng tương ứng đã được cài đặt từ kho lưu trữ này:

### 3.1. Định tuyến 3 Bộ Phương Pháp Cốt Lõi
- Thu thập, kiểm chứng chéo thông tin từ internet, lập thẻ `Fact Card`, khử phòng vang trích dẫn (`Echo-Chamber Check`) -> Kích hoạt **`/internet-info-refinement`** (`Bo-01-Tinh-Loc-Thong-Tin-Internet/SKILL.md`).
- Tổ chức kho tri thức nội bộ theo 4 xuất xứ (`L1/L2/L3/L4`), kiểm toán mã băm SHA-256 (`FRESH/STALE/EXPIRED`), tính toán dẫn xuất `L2` tất định -> Kích hoạt **`/kernel-registry-sot`** (`Bo-02-Kernel-Registry-SOT/SKILL.md`).
- Điều phối dự án phần mềm từ khảo sát (`SCAN` + `Indirect Prompting` + `/teach`), phỏng vấn ngược (`RRI`), thiết kế ngược `Working Backwards` & đấu trường `5-Phase /architect Arena` (`BLUEPRINT`), chia đơn vị kiểm chứng độc lập (`sequence-verifiable-units` · `TIP`), thi công `Local Worktrees (<= 10)` hoặc `Cloud /swarm (> 10)`, kiểm chứng sống qua `./bin/control-app` đến phát hành (`The Gardener` + xóa plan tạm + `/maintain-verification-skill`) -> Kích hoạt **`/vibecode-kit-v6`** (`Bo-03-Vibecode-Kit-v6/SKILL.md`).

### 3.2. Định tuyến Hệ Sinh Thái Công Cụ Phụ Trợ (`tools/skills/`)
- **Tìm kiếm đa tín hiệu & lọc ngữ cảnh PTC:** Ưu tiên gọi MCP `unified-search` (`web_search`, `web_extract`, `pool_status`) kết hợp `/tavily-dynamic-search`, `/tavily-map`, `/tavily-crawl`, `/tavily-research`.
- **Cào dữ liệu từ phiên trình duyệt đã đăng nhập:** Kích hoạt `/scrape` và đóng băng thành kỹ năng 200ms qua `/skillify` (dùng `/setup-browser-cookies` khi cần đồng bộ phiên).
- **Xây dựng đồ thị tri thức & đồng bộ GBrain:** Kích hoạt `/ak-graphify`, `/setup-gbrain` và `/sync-gbrain`.
- **Phân tích chiến lược, kiến trúc & duyệt kế hoạch 4 góc nhìn:** Kích hoạt `/ak-brainstorm`, `/ak-plan`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/plan-devex-review` hoặc `/autoplan`.
- **Thi công, gỡ lỗi, kiểm thử & kiểm toán bảo mật:** Kích hoạt `/ak-cook`, `/ak-fix`, `/ak-debug`, `/investigate`, `/qa`, `/qa-only`, `/test-audit`, `/ak-security` hoặc `/cso`.
- **Điều phối song song, bàn giao phiên & phát hành:** Kích hoạt `/ak-worktree`, `/ak-orchestrate`, `/ak-handoff`, `/context-save`, `/context-restore`, `/review`, `/ak-review-pr`, `/ak-ship`, `/ship` hoặc `/land-and-deploy`.
- **Viết mới hoặc đồng bộ tài liệu kỹ thuật:** Kích hoạt `/document-generate` hoặc `/document-release`.

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming -> invoke office-hours
- Bugs, errors, "why is this broken", 500 errors -> invoke investigate
- Ship, deploy, push, create PR -> invoke ship
- QA, test the site, find bugs -> invoke qa
- Code review, check my diff -> invoke review
- Update docs after shipping -> invoke document-release
- Weekly retro -> invoke retro
- Design system, brand -> invoke design-consultation
- Visual audit, design polish -> invoke design-review
- Architecture review -> invoke plan-eng-review
- Save progress, checkpoint, resume -> invoke context-save
- Code quality, health check -> invoke health
