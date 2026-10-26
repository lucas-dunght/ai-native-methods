# AI-Native Methods · Ba phương pháp làm việc với AI

![License](https://img.shields.io/badge/license-MIT-black.svg)
![Version](https://img.shields.io/badge/version-2026.10-blue.svg)
![Language](https://img.shields.io/badge/lang-Vietnamese-red.svg)

Bộ tài liệu chuyển giao ba phương pháp làm việc với AI cho sinh viên, giảng viên đại học và các nhóm phát triển sản phẩm. Mọi thương hiệu cụ thể đã được loại bỏ. Mỗi phương pháp đứng độc lập, có thể áp dụng riêng hoặc kết hợp thành một chuỗi liên hoàn từ thu thập tri thức internet, tổ chức nguồn sự thật nội bộ cho tới xây dựng và phát hành phần mềm.

---

## Tổng quan ba bộ (Phiên bản đồng bộ 2026.10)

### Bộ 01 · Phương pháp tinh lọc và làm giàu thông tin từ internet (v2.0)

Khung làm việc 7 giai đoạn biến thông tin thô thu thập từ internet thành tri thức nguyên tử có chất lượng kiểm chứng cơ học. Đầu vào là kết quả tìm kiếm đa tín hiệu (`unified-search` / `tavily-*`), lọc cô lập ngữ cảnh kiểu PTC (`Programmatic Tool Calling`), cào trình duyệt phiên thật chỉ đọc (`gstack /scrape` + `/skillify`) và nghiên cứu tổng hợp (`tavily-research`). Đầu ra là tập thẻ sự thật (`Fact Cards`) có nguồn gốc độc lập, có nhãn nhận định Fable 5.1 (`OBSERVED` / `DERIVED` / `PRIOR` / `ASSUMED`), đã khử phòng vang (`Echo-Chamber Check`), giải quyết xung đột qua thẻ quyết định `Decision Brief D<N>` và vượt qua cổng kiểm tra định lượng (`Constraint Loop Gate`).

Dùng cho nghiên cứu thị trường, phân tích đối thủ cạnh tranh, tổng quan tài liệu khoa học, thẩm định dự án (`due diligence`) và tạo dữ liệu đầu vào `L1` cho Bộ 02.

📂 [`Bo-01-Tinh-Loc-Thong-Tin-Internet/`](./Bo-01-Tinh-Loc-Thong-Tin-Internet/)

### Bộ 02 · Kernel Registry và nguồn sự thật đa xuất xứ (v2.0)

Khung tổ chức tri thức theo bốn xuất xứ độc lập gồm Sự thật lưu sẵn (`L1`), Sự thật dẫn xuất (`L2`), Nghĩa vụ rút từ văn bản pháp quy (`L3`) và Phán xét phong cách tự do (`L4`). Mỗi xuất xứ có chế độ kiểm chứng riêng và lưu trong kho riêng.

Bản nâng cấp **v2.0 (2026.10)** bổ sung kiểm toán độ tươi bằng mã băm SHA-256 (`FRESH / STALE / EXPIRED`), bộ tính công thức `L2` tất định bằng script kèm dấu vết `audit_trace`, phân tầng chỉ mục phụ thuộc từ `dependency-index.csv` lên đồ thị tri thức `ak-graphify` và bộ nhớ đồng bộ `gstack /sync-gbrain` (có kiểm soát `brain_trust_policy` và kiểm toán rò rỉ `--audit`), khóa phạm vi chỉ sao chép (`Copy-Only Scope Freeze`) và cầu nối liên thông tự động giữa Bộ 01, Bộ 02 và Bộ 03.

Dùng cho quản trị tri thức doanh nghiệp, xây dựng trợ lý AI nội bộ chống bịa số liệu và làm nền tảng dữ liệu chuẩn cho Bộ 03.

📂 [`Bo-02-Kernel-Registry-SOT/`](./Bo-02-Kernel-Registry-SOT/)

### Bộ 03 · Vibecode Kit (v6.2 × `pstack`)

Khung làm việc để xây sản phẩm phần mềm bằng cách điều phối đội ngũ AI agent. Ba vai trò chính (Chủ thầu, Thợ thi công, Chủ nhà / Người làm vườn `The Gardener`) kết hợp cùng lớp Cố vấn và Trọng tài độc lập (Kongming / Arbiter). Quy trình 8 bước tự co giãn theo phân tầng rủi ro R0 đến R3.

Bản nâng cấp **v6.2 (2026.10 · `Vibecode × pstack @poteto`)** hợp nhất toàn bộ nền tảng của v6.1 (`gstack` + `AgentKit` + `Fable 5.1`) với hai trụ cột cốt lõi từ hệ thống `pstack` của Lauren Tan (`@poteto`) gồm:
- **Đòn bẩy Hạ tầng Tự Kiểm Chứng (`Build the Lever` · `./bin/control-app` CLI) & Bộ nhớ Vật chất hóa (`Feature Map`):** Đóng gói CLI `./bin/control-app` theo 6 tiêu chuẩn *Deep Modules* của John Ousterhout (`subcommands`, `--dry-run`, báo lỗi chỉ rõ lệnh tiếp theo `next_command`, `--json`, bao phủ trọn DX: `seed`, `auth`, `flag`, `dom`, `screenshot`, `perf`) kết hợp bản đồ `references/features/README.md` (`Feature Map`) được đồng bộ hàng ngày qua `/maintain-verification-skill`.
- **Chỉ đạo Mô hình Tiên tiến & Lập kế hoạch bằng Code (`Supervising Smarter Models`):** Nhúng kỹ thuật `Indirect Prompting` (*"Restate in your own words"*), bộ tứ nhận thức hai chiều `/teach = /how + /why + /recall`, thiết kế ngược `Working Backwards` (`Caller README` theo 4 ô `Diátaxis` + `/unslop`), thực nghiệm giao diện `/prototype` (`Live UI Switcher`) và đấu trường kiến trúc 5 pha `/architect Arena` (`Ground -> Sketch Type Signatures & Caller Usage -> Cross-judge & Synthesize -> Implement -> Scrap when wrong`).
- **Định tuyến `Local Worktrees (<= 10)` vs. `Cloud Agents + /swarm (> 10)` & Vai trò "Người làm vườn" (`The Gardener`):** Chia kế hoạch thành các đơn vị kiểm chứng độc lập (`sequence-verifiable-units`), vượt trần phần cứng máy cá nhân bằng `Coordinator Bot + Cloud VM Snapshots + /swarm` (tự động tái hiện lỗi Slack `auto-repro`), xóa file plan tạm sau khi merge và tuần tra dòng chảy PR để nhổ cỏ dại kiến trúc từ sớm.

Dùng cho đồ án xây ứng dụng, luận văn có deliverable phần mềm, dự án incubator, MVP và đội ngũ kỹ thuật AI-Native.

📂 [`Bo-03-Vibecode-Kit-v6/`](./Bo-03-Vibecode-Kit-v6/) · 📘 [Cẩm nang Toàn trình làm sản phẩm từ A đến Z (`docs/cam-nang-lam-san-pham-a-den-z.md`)](./docs/cam-nang-lam-san-pham-a-den-z.md)

### Bộ Công Cụ & Kỹ Năng Đi Kèm (`tools/` · All-in-One Bootstrap)

Để người dùng mới có thể vận hành ngay cả ba bộ phương pháp mà không cần tự tìm kiếm từng công cụ bên ngoài, thư mục [`tools/`](./tools/) đóng gói sẵn toàn bộ hệ sinh thái phụ trợ đã được khử sạch mọi khóa API/Token cá nhân.
- **`tools/unified-search-mcp/`** chứa máy chủ MCP `Unified Search Pool v2.0` (định tuyến đa tín hiệu 8 chế độ qua `Tavily`, `Exa` và `Linkup` kèm xoay vòng khóa Round-Robin và mẫu `.mcp_env.example`).
- **`tools/skills/`** chứa **58 kỹ năng phụ trợ (`Companion Skills`)** gồm 8 kỹ năng `tavily-*`, 19 kỹ năng `akkit` (`ak-fable-thinking`, `ak-graphify`, `ak-orchestrate`, `ak-ship`...) và 31 kỹ năng `gstack` (`scrape`, `skillify`, `setup-gbrain`, `sync-gbrain`, `autoplan`, `qa`, `cso`...).
- **`tools/gstack-bin/`** và **`tools/hooks/`** chứa 21 tiện ích dòng lệnh (`gstack-wtree`, `gstack-evidence`, `gstack-verify-gate`...) và 13 mô-đun kiểm định hợp đồng PR (`pr-body-contract.cjs`, `writing-language.cjs`...).

📂 [`tools/`](./tools/) · 📖 [`docs/`](./docs/) (Tài liệu hướng dẫn cấu hình API Key Pool, mở rộng công cụ theo chuẩn Diataxis và **Cẩm nang Toàn trình A đến Z**: [Cẩm nang làm sản phẩm A đến Z](./docs/cam-nang-lam-san-pham-a-den-z.md) · [Tutorial 15 phút](./docs/tutorial-first-15-minutes-with-tools.md) · [How-To thêm API Key & thêm Provider mới](./docs/how-to-configure-and-extend-api-tools.md) · [Reference kỹ thuật](./docs/reference-tools-and-api-config.md) · [Giải thích kiến trúc](./docs/explanation-multi-signal-router-and-key-pool.md))

---

## Cấu trúc mỗi bộ

Mỗi bộ là một thư mục độc lập với cấu trúc nhất quán.

```
Bo-XX-Ten-Phuong-Phap/
├── README.md            Tổng quan ngắn
├── Methodology.md       Triết lý và phương pháp chi tiết
├── Architecture.md      Kiến trúc kỹ thuật và thành phần
├── SKILL.md             Đặc tả skill để cài vào Claude, Antigravity hoặc agent khác
├── Quick-Start.md       Hướng dẫn bắt đầu trong 10 đến 20 phút
├── templates/           Bản mẫu sẵn dùng
├── references/          Tài liệu giao thức chuyên sâu (nạp theo ngữ cảnh)
└── examples/            Ví dụ thực chiến từ đầu đến cuối
```

Ngoài các file markdown, mỗi bộ còn có hai dạng deliverable ở thư mục gốc.

- **File `.docx`** ở root repo. Bản tài liệu cho người đọc, mở được trên Word, Pages, Google Docs.
- **File `.skill`** ở root repo. Bản đóng gói zip của `SKILL.md` cùng các thư mục `templates/`, `references/` và `examples/`. Cài vào Claude hoặc hệ thống AI agent bằng cách nạp file vào mục Skills.

---

## Bắt đầu nhanh

### Cho sinh viên và kỹ sư muốn dùng một bộ cụ thể

1. Mở thư mục Bộ tương ứng.
2. Đọc `README.md` trước.
3. Đọc `Quick-Start.md` và chạy thử trong 10 đến 20 phút.
4. Đọc `Methodology.md` để hiểu cơ sở lý luận.
5. Đọc `Architecture.md` và `references/` khi cần tùy biến hoặc mở rộng quy mô.

### Cho giảng viên muốn dùng làm tài liệu môn học

1. Đọc `Methodology.md` của bộ liên quan để đánh giá mức độ phù hợp với học phần.
2. Có thể dùng `Methodology.md` làm sườn bài giảng tuần đầu.
3. Các bản mẫu trong `templates/` và tình huống trong `examples/` dùng làm bài tập thực hành.
4. File `.docx` ở root tiện in ấn hoặc phát trực tiếp cho sinh viên.

### Cho người muốn cài trọn bộ Skill và Công cụ vào Antigravity hoặc Claude Code (1 lệnh)

1. Mở Terminal tại thư mục gốc của repo và chạy lệnh cài đặt tự động:
   ```bash
   chmod +x tools/install-all.sh
   ./tools/install-all.sh
   ```
   Script sẽ cài đặt cả 3 Bộ Phương Pháp cốt lõi, 58 kỹ năng phụ trợ (`tavily-*`, `ak-*`, `gstack`), 21 tiện ích `gstack-bin`, 13 `hooks` và khởi tạo máy chủ MCP `unified-search` kèm file mẫu `~/.mcp_env`.
2. Nếu dùng Claude Desktop / Web, bạn cũng có thể tải trực tiếp các file `.skill` ở thư mục gốc (`internet-info-refinement.skill`, `kernel-registry-sot.skill`, `vibecode-kit-v6.skill`) vào mục Settings → Capabilities → Skills.

---

## Triết lý chung

Ba bộ chia sẻ bốn nguyên tắc nền tảng.

**Một, AI không thay thế phán xét cuối cùng của con người.** Mọi quyết định có hậu quả nghiêm trọng hoặc đi qua cánh cửa một chiều phải được trình qua thẻ quyết định `Decision Brief D<N>` để một con người ký nhận trách nhiệm. AI hỗ trợ khảo sát, tổng hợp, đề xuất, phản biện và thi công. Con người chọn hướng và chịu trách nhiệm.

**Hai, mọi khẳng định và báo cáo hoàn thành đều phải có bằng chứng cơ học truy ngược được.** Không chấp nhận nguồn thông tin mồ côi hoặc hiệu ứng phòng vang (Bộ 01 v2.0), không trộn lẫn sự thật cứng với phong cách cá nhân hoặc để dữ liệu trôi mã băm (Bộ 02 v2.0) và không nghiệm thu phần mềm khi thiếu đòn bẩy kiểm chứng sống `./bin/control-app` gắn với dấu vân tay mã nguồn (Bộ 03 v6.2).

**Ba, không tự xây cái thị trường hoặc kho mã nguồn đã có sẵn.** Trước khi tự dựng quy trình hay viết hàm mới, luôn rà soát bậc thang tái sử dụng từ công cụ sẵn có trong dự án, thư viện chuẩn cho tới các mô hình ngôn ngữ lớn.

**Bốn, dự đoán trước khi làm, hiệu chỉnh sau khi chạy thật.** Mọi can thiệp đáng kể đều có tiêu chí dự đoán trước khi triển khai. Sau mỗi chu kỳ, đo kết quả thực tế và phân bổ sai số để hệ thống liên tục tiến hóa.

---

## Phối hợp liên hoàn ba bộ

Khi thực hiện một dự án nghiên cứu và phát triển sản phẩm hoàn chỉnh, cả ba bộ kết nối tự động qua cầu nối dữ liệu chuẩn.

```
Bộ 01 v2.0 (Tinh lọc thông tin từ internet · PTC + Echo-Chamber Check)
   │
   │  Fact Cards hạng verified (exact_quote + content_hash)
   ▼
Bộ 02 v2.0 (Kernel Registry SOT · SHA-256 Freshness + L2 Tất định + Feature Map Bridge)
   │
   │  Con trỏ [L1-*], [L2-*], [OBL-*], [L4-*] trạng thái FRESH + references/features/README.md
   ▼
Bộ 03 v6.2 × pstack (./bin/control-app + /teach + 5-Phase /architect Arena + Cloud /swarm)
   │
   │  Sản phẩm phần mềm + WTREE_FINGERPRINT + Calibration Card 100 điểm
   ▼
Deliverable cuối đã kiểm chứng toàn diện
```

Không bắt buộc dùng cả ba cùng lúc. Mỗi bộ đều có thể vận hành độc lập.

---

## Đối tượng sử dụng

- Sinh viên thạc sĩ và cử nhân năm cuối các ngành Phân tích dữ liệu, Trí tuệ nhân tạo, Khoa học máy tính, Hệ thống thông tin, Kinh tế lượng.
- Giảng viên hướng dẫn đồ án tốt nghiệp và luận văn.
- Nhóm khởi nghiệp và kỹ sư phát triển sản phẩm theo mô hình AI-Native.
- Nghiên cứu sinh áp dụng vào đề tài thực nghiệm cá nhân.

---

## Phiên bản

Phiên bản hiện hành của toàn bộ kho tài liệu là **2026.10** (Bộ 01 v2.0, Bộ 02 v2.0 và Bộ 03 v6.2 × `pstack`). Khi áp dụng vào dự án, vui lòng ghi rõ phiên bản đã sử dụng trong báo cáo để thuận tiện đối chiếu.

---

## Đóng góp

Phương pháp được thiết kế để tiến hóa qua trải nghiệm thực tế. Sinh viên, giảng viên hoặc kỹ sư áp dụng phát hiện vấn đề hoặc đề xuất cải tiến vui lòng mở Issue hoặc Pull Request.

Khi đóng góp, vui lòng tuân thủ ba quy tắc văn phong.
- Không dùng dấu gạch ngang dài (em-dash) trong markdown (thay bằng dấu chấm, dấu phẩy hoặc dấu chấm giữa `·`)
- Không đặt dấu phẩy trước chữ "và"
- Không lạm dụng dấu hai chấm trong câu văn xuôi

---

## License

[MIT License](./LICENSE)

Copyright © 2026 Nguyễn Cảnh Lâm

---

## Tác giả

**Nguyễn Cảnh Lâm**
Chief AI Officer, Real-time Robotics

📧 nclamvn@gmail.com
🐙 [github.com/nclamvn](https://github.com/nclamvn)

---

## Trích dẫn

Khi sử dụng trong báo cáo học thuật hoặc dự án, vui lòng trích dẫn theo mẫu.

```
Nguyễn, C. L. (2026). AI-Native Methods · Ba phương pháp làm việc với AI
(Version 2026.10 · Bộ 01 v2.0, Bộ 02 v2.0, Bộ 03 v6.2 × pstack) [Computer software]. GitHub.
https://github.com/lucas-dunght/ai-native-methods
```
