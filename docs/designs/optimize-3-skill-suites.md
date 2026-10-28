---
status: PROMOTED
date: 2026-10-28
branch: main
mode: SELECTIVE EXPANSION
---
# CEO Plan: Toi Uu Hoa & Dong Bo Toan Dien 3 Bo Phuong Phap AI-Native (v2026.10 -> Full-Stack 4-Layer & Deep Module Levers)

**Branch:** `main`
**Base branch:** `main`
**Repository:** `lucas-dunght/ai-native-methods` (`/Users/tuandunghoang/projects/vibecode-kit`)
**Review Skill:** `/plan-ceo-review` (Mode: `SELECTIVE EXPANSION`)
**CEO Scope Summary:** `/Users/tuandunghoang/.gstack/projects/lucas-dunght-ai-native-methods/ceo-plans/2026-10-28-optimize-3-skill-suites-summary.md`

---

## 0. Pre-Review System Audit & Landscape Synthesis

### 0.1. Hien trang Kho luu tru (`OBSERVED`)
- **Chào mừng trở lại (Session Recovery):** Phiên làm việc gần nhất (`2026-10-26`) đã nâng cấp `Bo-03-Vibecode-Kit-v6` lên `v6.2 × pstack (@poteto)` và bổ sung Cẩm nang Toàn trình A đến Z vào `docs/cam-nang-lam-san-pham-a-den-z.md` (Commit `13cafa0`).
- **Kiểm toán cấu trúc cả 3 Bộ Kỹ năng hiện tại (`[measured: wc -l & find]`):**
  - **Bộ 01 (`Bo-01-Tinh-Loc-Thong-Tin-Internet` · `v2.0`):** Gồm `15` tệp (`1.184` dòng Markdown/YAML), `SKILL.md` dài `170` dòng (`[measured: wc -l]`). Chưa có thư mục `scripts/`.
  - **Bộ 02 (`Bo-02-Kernel-Registry-SOT` · `v2.0`):** Gồm `16` tệp (`1.049` dòng Markdown/YAML/CSV), `SKILL.md` dài `128` dòng (`[measured: wc -l]`). Chưa có thư mục `scripts/`.
  - **Bộ 03 (`Bo-03-Vibecode-Kit-v6` · `v6.2 × pstack`):** Gồm `21` tệp (`1.471` dòng Markdown), `SKILL.md` dài `102` dòng (`[measured: wc -l]`). Chưa có thư mục `scripts/`.
- **Prior learnings applied:**
  - **Prior learning applied: `[gstack-bin-requires-sibling-lib]` (confidence 10/10, from 2026-10-25)**
  - **Knowledge Item applied: `[enterprise-office-skills-catalog]` (`~/.gemini/knowledge/enterprise-office-skills-catalog.md:6` · Chuẩn Tier-1 Full-Stack 4 Lớp: `SKILL.md` + `scripts/*.py` + `references/*.md` + `templates/`)**

### 0.2. Taste Calibration (Chuan muc Doi chieu trong Kho luu tru)
- **Mẫu tốt cần phát huy (Good patterns):**
  - [`Bo-03-Vibecode-Kit-v6/SKILL.md:1-102`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-03-Vibecode-Kit-v6/SKILL.md#L1-L102): Thiết kế gọn (`102` dòng), phân tầng rủi ro `R0..R3` rõ ràng và trỏ sang `references/` + `templates/` theo đúng nguyên lý `Progressive Disclosure`.
  - [`Bo-03-Vibecode-Kit-v6/templates/Control-App-and-Feature-Map.md:25-118`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-03-Vibecode-Kit-v6/templates/Control-App-and-Feature-Map.md#L25-L118): Thiết kế công cụ dòng lệnh theo 6 tiêu chuẩn *Deep Modules* của John Ousterhout (`--dry-run`, `--json`, `--help`, `Actionable Error` có trường `next_command`).
  - [`Bo-02-Kernel-Registry-SOT/references/bo01-bo02-bo03-bridge.md:1-72`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/references/bo01-bo02-bo03-bridge.md#L1-L72): Định nghĩa rõ ánh xạ trường dữ liệu xuyên 3 Bộ.
- **Mẫu chưa đạt cần loại bỏ (Anti-patterns to avoid):**
  - **Khai báo lệnh CLI trong tài liệu nhưng file script không tồn tại trên đĩa:** [`Bo-02-Kernel-Registry-SOT/Architecture.md:104`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/Architecture.md#L104) và [`templates/L2-derived-fact.yaml:13`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/templates/L2-derived-fact.yaml#L13) ghi cứng `deterministic_eval_cmd: "python3 scripts/eval_l2.py --id ..."`, nhưng thư mục `scripts/` hoàn toàn không tồn tại.
  - **Nhúng các đoạn code Python rời rạc trong văn bản Markdown thay vì đóng gói thành CLI Tool:** [`Bo-01-Tinh-Loc-Thong-Tin-Internet/references/multi-signal-search-and-ptc.md:34-80`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-01-Tinh-Loc-Thong-Tin-Internet/references/multi-signal-search-and-ptc.md#L34-L80) và [`citation-graph-and-conflict-gate.md:36-65`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-01-Tinh-Loc-Thong-Tin-Internet/references/citation-graph-and-conflict-gate.md#L36-L65) bắt Agent tự gõ lại script Python mỗi lần chạy.

### 0.3. Landscape Check (Tong hop 3 Tang Tri thuc)
- *Search unavailable - proceeding with in-distribution knowledge only (Aside status: `NEEDS_ASIDE: Darwin`).*
- **[Layer 1 · Tried and true]:** Các bộ kỹ năng thế hệ đầu (`Tier-2 Prompt Skills`) chỉ gồm các tệp văn bản Markdown (`SKILL.md`, `references/`, `templates/`) mô tả quy trình bằng lời.
- **[Layer 2 · New and popular]:** Chuẩn `Tier-1 Full-Stack Engineered Skills` (4 lớp: `SKILL.md` + `scripts/*.py` + `references/` + `templates/`) và triết lý `Build the Lever` (`pstack` `@poteto`) chuyển toàn bộ các bước tính toán tất định, lọc ngữ cảnh PTC, kiểm toán SHA-256 và kiểm tra cổng định lượng thành công cụ CLI chạy bằng 1 lệnh.
- **[Layer 3 · First-principles Eureka]:**
  - **Eureka:** Bộ 03 (`Vibecode Kit v6.2`) đã giảng dạy nguyên lý *"Thay vì viết hướng dẫn kiểm thử dài dòng bằng chữ khiến Agent tốn hàng nghìn token tự viết script dùng một lần dễ gãy, hãy đóng gói Deep Module CLI (`--dry-run`, `--json`, `next_command`)"* - nhưng **chính bản thân 3 Bộ kỹ năng (`Bo-01`, `Bo-02`, `Bo-03`) lại đang có `0` file script thực thi trong `scripts/`!** Việc trang bị 3 công cụ CLI chuẩn Deep Module (`scripts/bo01_refine_tool.py`, `scripts/bo02_registry_tool.py`, `scripts/bo03_vibecode_tool.py`) ngay bên trong 3 Bộ sẽ biến cả 3 Bộ từ tài liệu hướng dẫn thành **Nền tảng Thực thi Tự Kiểm Chứng 4 Lớp (Tier-1 Full-Stack Skills)**.

---

## Step 0A · Premise Challenge (Thach thuc Gia dinh Goc)

1. **Vấn đề thực sự cần giải quyết (Real Problem):**
   Qua kiểm toán đối chiếu cả 3 Bộ (`Bo-01`, `Bo-02`, `Bo-03`), hệ sinh thái hiện có **4 điểm nghẽn cấu trúc** làm giảm hiệu năng thực thi của AI Agent:
   - **Điểm nghẽn 1 · Thiếu Lớp Công cụ CLI Thực thi Tất định (`0` thư mục `scripts/` trong cả 3 Bộ):**
     - Ở **Bộ 01**, Agent phải tự sinh code Python tạm thời để lọc ngữ cảnh PTC, tính `independent_origin_count`, phân hạng `trust_tier`, kiểm tra 4 điều kiện `Constraint Loop` và xuất `Fact Card` sang `L1` của Bộ 02.
     - Ở **Bộ 02**, [`Bo-02-Kernel-Registry-SOT/Architecture.md:104`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/Architecture.md#L104) gọi lệnh `python3 scripts/eval_l2.py --id ...`, nhưng file này chưa tồn tại trên đĩa (`FileNotFoundError`). Việc kiểm toán độ tươi SHA-256 (`FRESH/STALE/EXPIRED`), lan truyền `STALE` qua `dependency-index.csv`, chụp `ORIGINAL_TREE_FINGERPRINT` và đối chiếu `Feature Map` cũng chưa có CLI thực thi.
     - Ở **Bộ 03**, các thao tác khởi tạo `./bin/control-app`, chụp `WTREE_FINGERPRINT`, quét đồng bộ SHA-256 cho `Feature Map` (`/maintain-verification-skill`) và kiểm tra `Constraint Loop` văn phong/bảo mật vẫn đang nằm rải rác dưới dạng các đoạn bash rời trong Markdown.
   - **Điểm nghẽn 2 · Lệch pha Cơ chế Giám sát `pstack` & Thiếu Co giãn Quy mô (`R0–R3`) ở Bộ 01 và Bộ 02:**
     - Bộ 03 đã có phân tầng rủi ro co giãn (`R0..R3`) và bước `Indirect Prompting Restate` (*"Restate in your own words"*), trong khi [`Bo-01-Tinh-Loc-Thong-Tin-Internet/SKILL.md:33`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-01-Tinh-Loc-Thong-Tin-Internet/SKILL.md#L33) và [`Bo-02-Kernel-Registry-SOT/SKILL.md:42`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/SKILL.md#L42) vẫn ép mọi bài toán (kể cả tra cứu nhanh 5 nguồn hoặc kho tri thức nhỏ `< 30` mục) phải đi qua toàn bộ 7 giai đoạn / 5 phase nặng nề và chưa có bước `Indirect Prompting Restate` trước cổng `D1`.
     - `Bo-01/SKILL.md` hiện dài `170` dòng (chứa nhiều khối CSV/YAML mẫu lặp lại với `templates/`), tốn token ngữ cảnh hơn mức cần thiết khi nạp skill.
   - **Điểm nghẽn 3 · Lệch Hệ Nhãn Nhận Định (`Claim Taxonomy Drift`) & Tham chiếu Phiên bản Cũ:**
     - Bộ 01 dùng 4 nhãn Fable 5.1 (`OBSERVED | DERIVED | PRIOR | ASSUMED` tại `Bo-01/SKILL.md:80`), Bộ 02 dùng 3 nhãn cạnh (`EXTRACTED | INFERRED | AMBIGUOUS` tại `Bo-02/Architecture.md:200`), còn Bộ 03 lại viết 3 nhãn (`OBSERVED | INFERRED | UNVERIFIED` tại `Bo-03/SKILL.md:31-33`) mà chưa có bảng ánh xạ thống nhất.
     - [`Bo-01-Tinh-Loc-Thong-Tin-Internet/Architecture.md:219`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-01-Tinh-Loc-Thong-Tin-Internet/Architecture.md#L219) vẫn ghi `Vibecode Kit v6.1` thay vì `v6.2 × pstack`.
   - **Điểm nghẽn 4 · Lệch Trình cài đặt (`install-all.sh`), Rác Phiên bản ở Thư mục Gốc & KI Cũ:**
     - [`tools/install-all.sh:27-30`](file:///Users/tuandunghoang/projects/vibecode-kit/tools/install-all.sh#L27-L30) chỉ cài 3 Bộ vào `~/.gemini/config/skills/` mà bỏ sót `~/.claude/skills/` (khiến `~/.claude/skills/vibecode-kit-v6` vẫn kẹt ở bản cũ từ ngày `Sep 8` và thiếu hẳn Bộ 01, Bộ 02).
     - Thư mục gốc đang tồn tại song song nhiều bản `.docx` và `.skill` trùng lặp (`-v2.0`, `-v6.1`, `-v6.2` bên cạnh bản chính).
     - Bộ nhớ KI `~/.gemini/knowledge/vibecode-kit-v6-workflow.md` vẫn đang ở bản `v6.1`.
2. **Chi phí nếu không làm gì (Do-Nothing Cost):**
   - Agent chạy Bộ 01 và Bộ 02 tiếp tục tốn hàng nghìn token mỗi phiên để tự viết lại script lọc PTC, tính công thức `L2` và kiểm toán SHA-256 (hoặc gặp lỗi thiếu file `scripts/eval_l2.py`); người dùng chạy trên Claude Code bị dùng nhầm skill bản cũ tháng 9; và các tác vụ nghiên cứu nhỏ ở Bộ 01/02 bị quá tải thủ tục.

---

## Step 0B · Existing Code Leverage & Reality Rows

### Reality Rows (`gstack-plan-reality`)
| Premise | Claim | File:Line Receipt | Verdict |
|---|---|---|---|
| P1 | Cả 3 Bộ (`Bo-01`, `Bo-02`, `Bo-03`) hiện có `0` thư mục `scripts/` thực thi | `Bo-02-Kernel-Registry-SOT/Architecture.md:104` | `verified` |
| P2 | `Bo-02` gọi `python3 scripts/eval_l2.py` trong `Architecture.md` và `templates/L2-derived-fact.yaml` nhưng file chưa tồn tại | `Bo-02-Kernel-Registry-SOT/templates/L2-derived-fact.yaml:13` | `verified` |
| P3 | `Bo-01/SKILL.md` dài `170` dòng, bắt buộc chạy cố định 7 giai đoạn và chưa có phân tầng `R0..R3` hay `Indirect Prompting Restate` | `Bo-01-Tinh-Loc-Thong-Tin-Internet/SKILL.md:33` | `verified` |
| P4 | `Bo-01` dùng 4 nhãn (`OBSERVED/DERIVED/PRIOR/ASSUMED`) trong khi `Bo-03` ghi 3 nhãn (`OBSERVED/INFERRED/UNVERIFIED`) | `Bo-03-Vibecode-Kit-v6/references/claim-and-evidence-protocol.md:11` | `verified` |
| P5 | `Bo-01/Architecture.md:219` vẫn tham chiếu `Vibecode Kit v6.1` | `Bo-01-Tinh-Loc-Thong-Tin-Internet/Architecture.md:219` | `verified` |
| P6 | `tools/install-all.sh:27-30` chỉ chép 3 Bộ vào `~/.gemini/config/skills`, chưa chép vào `~/.claude/skills` | `tools/install-all.sh:27` | `verified` |

```text
REALITY: premise-table pass 6 claims verified with exact file:line receipts across the 3 skill suites, unverified=0 Bo-02-Kernel-Registry-SOT/Architecture.md:104
REALITY: already-done pass verified 0 scripts directories exist in Bo-01, Bo-02, Bo-03 Bo-01-Tinh-Loc-Thong-Tin-Internet/SKILL.md:1
REALITY: surface-check pass verified tools/install-all.sh and template CLI flags against repo files tools/install-all.sh:27
REALITY: binding-decisions pass verified Zero-Secret Policy and Constraint Loop (no em-dash, no comma before va) CLAUDE.md:19
REALITY: numbers pass 52 files (3704 lines total across 3 suites) measured via wc -l and find Bo-03-Vibecode-Kit-v6/SKILL.md:1
REALITY: deferred-asks pass no linked GitHub issue; user request provided inline CLAUDE.md:1
REALITY: pr-count pass default 1 PR per wave (no .gstack/ship-policy.json present) CLAUDE.md:1
PLAN_REALITY: phase=ceo rows=7/7 missing=none unverified=0 verdict=complete
```

---

## Step 0C · Dream State Mapping (Ban do Trang thai Ly tuong 12 Thang)

```text
  CURRENT STATE (2026.10 Baseline)               THIS PLAN (Full-Stack 4-Layer Optimization)        12-MONTH IDEAL
  +-----------------------------------+          +------------------------------------------+       +------------------------------------------+
  | - Bộ 03 đã lên v6.2 × pstack      |          | - Nâng cấp cả 3 Bộ lên chuẩn Tier-1      |       | - Mọi chu kỳ Nghiên cứu (Bộ 01) ->       |
  | - NHƯNG cả 3 Bộ đều thiếu lớp     |          |   Full-Stack 4 Lớp (SKILL.md + scripts/  |       |   Quản trị SOT (Bộ 02) -> Xây Sản phẩm   |
  |   công cụ thực thi scripts/*.py   |          |   + references/ + templates/):           |       |   (Bộ 03) vận hành khép kín qua 3 CLI    |
  |   (lệnh eval_l2.py bị lỗi thiếu   |  --->    |   1. Bộ 01: scripts/bo01_refine_tool.py  | --->  |   Deep Module trả JSON chuẩn hóa.        |
  |   file, lọc PTC phải gõ tay).     |          |   2. Bộ 02: scripts/bo02_registry_tool.py|       | - 0% lệch nhãn nhận định, 0% trôi mã băm |
  | - Bộ 01 & 02 chưa có co giãn      |          |      (+ scripts/eval_l2.py)              |       |   giữa Fact Card, L1/L2/L3 và Feature    |
  |   R0..R3 & Indirect Prompting.    |          |   3. Bộ 03: scripts/bo03_vibecode_tool.py|       |   Map trên cả Gemini & Claude Code.      |
  | - Lệch nhãn Claim Discipline,     |          | - Đồng bộ R0..R3, Indirect Prompting,    |       |                                          |
  |   rác file ở root & thiếu đồng bộ |          |   4 nhãn Fable 5.1, dọn root & đồng bộ   |       |                                          |
  |   sang ~/.claude/skills/.         |          |   install-all.sh + KI.                   |       |                                          |
  +-----------------------------------+          +------------------------------------------+       +------------------------------------------+
```

---

## Step 0F & 0G · Mode-Specific Analysis (`SELECTIVE EXPANSION`)

### 1. Three HOLD SCOPE Checks on Approved Baseline (`ROW-01` Option A & `ROW-03` Option A)
1. **Complexity check:** Các công cụ CLI (`bo01_refine_tool.py`, `bo02_registry_tool.py`, `bo03_vibecode_tool.py`) chỉ sử dụng thư viện chuẩn của Python (`stdlib`: `json`, `csv`, `hashlib`, `re`, `argparse`, `pathlib`, `datetime` + parser YAML gọn nhẹ không phụ thuộc gói ngoài), không thêm bất kỳ dịch vụ chạy ngầm hay thư viện bên thứ ba nào.
2. **Minimum changes vs. deferrable work:** Không có hạng mục nào trong `ROW-01` và `ROW-03` cần hoãn (`defer`), vì việc đồng bộ giữa `SKILL.md`, `scripts/*.py`, `references/`, `templates/`, `tools/install-all.sh` và các gói `.skill`/`.docx` phải diễn ra nguyên khối để tránh lệch mã băm hoặc thiếu file khi chạy.
3. **Stated invariants & acceptance criteria:** Bảo toàn 100% quy tắc `Zero-Secret Policy`, quy tắc không xóa vĩnh viễn file gốc (di chuyển các bản `.docx`/`.skill` trùng vào `_Archive/duplicate-deliverables-2026-10/`) và quy tắc `Constraint Loop` (`0` dấu `em-dash`, `0` chuỗi `dấu phẩy trước chữ và`).

### 2. 10x Ambition, Delight Scan & Platform Potential
- **10x Ambition:** Biến cả 3 Bộ kỹ năng (`Bộ 01`, `Bộ 02`, `Bộ 03`) thành một **Hệ điều hành Tri thức & Sản phẩm Tự Kiểm Chứng (`Self-Verifying 3-Suite AI-Native OS`)**: từ lọc nhiễu tìm kiếm web (Bộ 01) -> kiểm toán mã băm & tính công thức `L2` tất định (Bộ 02) -> đòn bẩy `./bin/control-app` & `Feature Map` (Bộ 03), tất cả đều thực thi bằng 1 câu lệnh CLI trả về biên nhận JSON có trường `next_command`.
- **Delight Scan (5 cải tiến 30 phút mang lại trải nghiệm vượt trội · Đã duyệt tích hợp):**
  1. **Tự kiểm thử nội tại (`--self-test`) trong cả 3 CLI + Tích hợp kiểm tra sống trong `tools/install-all.sh` (`EXP-01`):** Mỗi công cụ `scripts/*.py` có cờ `--self-test --json` chạy kiểm chứng toàn bộ các hàm lõi trên dữ liệu giả lập trong bộ nhớ chỉ mất `< 200ms`.
  2. **Nhúng khung `Indirect Prompting Restate` & Bảng chọn `R0–R3 Fast-Track` vào ngay bản mẫu (`templates/`) và `Quick-Start.md` của Bộ 01 & Bộ 02 (`EXP-02`):** Giúp người dùng và Agent áp dụng ngay chế độ chạy nhanh 10 phút (`R0/R1`) mà không phải tự thiết kế biểu mẫu.
  3. **Bảng Ánh xạ Chuẩn hóa 4 Nhãn Nhận định Fable 5.1 & Sổ cái Mã băm Xuyên 3 Bộ trong `bo01-bo02-bo03-bridge.md` & `claim-and-evidence-protocol.md` (`EXP-03`):** Khóa chặt sự tương đương cơ học giữa `OBSERVED / DERIVED / PRIOR / ASSUMED` (Bộ 01 & Bộ 03) với `EXTRACTED / INFERRED / AMBIGUOUS` (Bộ 02).
  4. **Hỗ trợ đọc/ghi YAML nguyên tử không cần cài đặt `PyYAML` ngoài (`Zero-Dependency YAML Parser/Emitter` trong `scripts/*.py`):** Đảm bảo 3 script chạy thành công 100% trên mọi máy Mac/Linux sạch chỉ có `python3` mặc định (và tự động dùng `PyYAML` nếu có).
  5. **Đồng bộ tự động cả `~/.gemini/config/skills/` lẫn `~/.claude/skills/` và cập nhật KI `~/.gemini/knowledge/vibecode-kit-v6-workflow.md`:** Xóa bỏ hoàn toàn tình trạng lệch phiên bản giữa Antigravity và Claude Code.

---

## Decision Ledger

| ID and owner | Contract and evidence | Current | Proposed | Status | Exact approval and scope |
|---|---|---|---|---|---|
| `ROW-01` (Step 0D · Optimization Approach Across the 3 Skill Suites) | `Bo-01-Tinh-Loc-Thong-Tin-Internet/` (`15` files), `Bo-02-Kernel-Registry-SOT/` (`16` files), `Bo-03-Vibecode-Kit-v6/` (`21` files), `tools/install-all.sh:27-30`, root `.skill`/`.docx` | Cả 3 Bộ chưa có thư mục công cụ `scripts/`; Bộ 01 & 02 chưa có phân tầng `R0–R3` và `Indirect Prompting Restate`; lệch nhãn `Claim Discipline`; `install-all.sh` chưa đồng bộ sang `~/.claude/skills/` | **Option A (10/10):** Nâng cấp cả 3 Bộ lên chuẩn Tier-1 Full-Stack 4 Lớp (bổ sung `scripts/bo01_refine_tool.py`, `scripts/bo02_registry_tool.py` + `eval_l2.py`, `scripts/bo03_vibecode_tool.py` chuẩn Deep Module CLI) + Đồng bộ `R0–R3`, `Indirect Prompting`, 4 nhãn `Fable 5.1` và tinh gọn `SKILL.md` + Cập nhật `install-all.sh`, đóng gói lại `.skill`/`.docx` và cập nhật KI. | `approved` | User answered `D1: A` (Completeness 10/10). Full 4-layer optimization across `Bo-01`, `Bo-02`, `Bo-03`, `tools/install-all.sh`, `.skill`, `.docx`, and KI. |
| `ROW-02` (Step 0E · Review Mode Selection) | Chế độ duyệt `/plan-ceo-review` (`SKILL.md:975-1023`) | `SELECTIVE EXPANSION` | `SELECTIVE EXPANSION` | `approved` | User answered `D2: A` (`SELECTIVE EXPANSION`). Mode handoff executed. |
| `ROW-03` (Step 0 · Prerequisite & Root Deliverable Cleanup Policy) | Root `.docx` & `.skill` files (`Bo-01*-v2.0.*`, `Bo-02*-v2.0.*`, `Bo-03*-v6.1.*`, `Bo-03*-v6.2.*`) | Thư mục gốc đang chứa các file `.docx` và `.skill` trùng phiên bản bên cạnh file chuẩn | **Option A:** Bỏ qua `/office-hours` VÀ chuyển các bản `.docx`/`.skill` có hậu tố phiên bản trùng lặp (`-v2.0`, `-v6.1`, `-v6.2`) vào `_Archive/duplicate-deliverables-2026-10/`, chỉ giữ lại bộ file chuẩn duy nhất ở thư mục gốc. | `approved` | User answered `D3: A`. Skip `/office-hours` and archive duplicate version-suffixed `.docx`/`.skill` files from root into `_Archive/duplicate-deliverables-2026-10/`. |
| `EXP-01` (Step 0G · Cherry-pick 1: `--self-test` in all 3 CLI Tools & Live Verification Gate in `tools/install-all.sh`) | `Bo-01/scripts/bo01_refine_tool.py`, `Bo-02/scripts/bo02_registry_tool.py`, `Bo-03/scripts/bo03_vibecode_tool.py`, `tools/install-all.sh:25-31` | `install-all.sh` chỉ copy thư mục mà chưa chạy kiểm thử xác nhận các công cụ CLI của 3 Bộ hoạt động tốt | **A) Add to this plan's scope (recommended):** Trang bị cờ `--self-test --json` (Zero-Dependency Python stdlib) cho cả 3 CLI (`bo01`, `bo02`, `bo03`) và tích hợp bước chạy kiểm thử sống (`Self-Test Gate`) ngay trong `tools/install-all.sh`. | `approved` | User answered `D4: A`. Add `--self-test --json` to all 3 CLI tools and integrate live self-test verification in `tools/install-all.sh`. |
| `EXP-02` (Step 0G · Cherry-pick 2: `R0–R3 Fast-Track & Indirect Prompting Restate` in `Bo-01` & `Bo-02` Templates and Quick-Start) | `Bo-01/templates/source-log.md`, `Bo-01/Quick-Start.md`, `Bo-02/templates/queues-and-migration-map.md`, `Bo-02/Quick-Start.md` | Các bản mẫu `templates/` và `Quick-Start.md` của Bộ 01 & Bộ 02 chưa có mục `Indirect Prompting Restate`, bảng chọn `R0–R3` và ví dụ gọi CLI `scripts/*.py` | **A) Add to this plan's scope (recommended):** Cập nhật trực tiếp `templates/` và `Quick-Start.md` của Bộ 01 & Bộ 02 để nhúng khung `Indirect Prompting Restate`, bảng phân tầng `R0–R3 Fast-Track` và câu lệnh gọi `scripts/bo01_refine_tool.py` / `scripts/bo02_registry_tool.py`. | `approved` | User answered `D5: A`. Update `templates/` and `Quick-Start.md` in `Bo-01` and `Bo-02` with `Indirect Prompting Restate`, `R0–R3` table, and CLI commands. |
| `EXP-03` (Step 0G · Cherry-pick 3: `Unified 4-Label Fable 5.1 Claim & Hash-Bridge Matrix` across `Bo-01`, `Bo-02`, `Bo-03`) | `Bo-02/references/bo01-bo02-bo03-bridge.md:1-72`, `Bo-03/references/claim-and-evidence-protocol.md:7-16` | Bộ 01 dùng 4 nhãn (`OBSERVED/DERIVED/PRIOR/ASSUMED`), Bộ 02 dùng 3 nhãn (`EXTRACTED/INFERRED/AMBIGUOUS`), Bộ 03 dùng 3 nhãn (`OBSERVED/INFERRED/UNVERIFIED`) | **A) Add to this plan's scope (recommended):** Nâng cấp `bo01-bo02-bo03-bridge.md` và `claim-and-evidence-protocol.md` với Bảng Ánh xạ Chuẩn hóa 4 Nhãn Fable 5.1 xuyên 3 Bộ và quy trình 1 lệnh CLI đồng bộ `Fact Card (Bộ 01) -> L1/L2 (Bộ 02) -> Feature Map (Bộ 03)`. | `approved` | User answered `D6: A`. Upgrade `bo01-bo02-bo03-bridge.md` and `claim-and-evidence-protocol.md` with the unified 4-label Fable 5.1 taxonomy and 1-command CLI bridge. |

---

## Danh Sách File Thực Thi Chi Tiết (Execution Manifest)

1. **Sao lưu & Dọn dẹp Thư mục Gốc (`_Archive/duplicate-deliverables-2026-10/`):**
   - Tạo thư mục `_Archive/duplicate-deliverables-2026-10/` và di chuyển các bản `.docx`/`.skill` trùng phiên bản ở root (`Bo-01-Tinh-Loc-Thong-Tin-Internet-v2.0.docx`, `Bo-02-Kernel-Registry-SOT-v2.0.docx`, `Bo-03-Vibecode-Kit-v6.1.docx`, `Bo-03-Vibecode-Kit-v6.2.docx`, `internet-info-refinement-v2.0.skill`, `kernel-registry-sot-v2.0.skill`, `vibecode-kit-v6.1.skill`, `vibecode-kit-v6.2.skill`) vào `_Archive/duplicate-deliverables-2026-10/`, giữ lại đúng 5 file `.docx` chuẩn và 3 file `.skill` chuẩn ở root.
2. **Xây dựng Lớp Công cụ CLI Thực thi Tất định (`scripts/*.py` · Chuẩn Deep Module + Zero-Dependency Python stdlib):**
   - Tạo mới `Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py` (`ptc-filter`, `audit-echo`, `gate-check`, `export-bo02`, `--dry-run`, `--json`, `--help`, `--self-test`).
   - Tạo mới `Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py` (`fingerprint`, `audit-freshness`, `eval-l2`, `sync-feature-map`, `--dry-run`, `--json`, `--help`, `--self-test`) và `Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py` (wrapper tương thích ngược với `Architecture.md:104` và `templates/L2-derived-fact.yaml:13`).
   - Tạo mới `Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py` (`init-control-app`, `wtree-fingerprint`, `maintain-features`, `constraint-check`, `--dry-run`, `--json`, `--help`, `--self-test`).
3. **Nâng cấp & Tinh gọn Bộ 01 (`Bo-01-Tinh-Loc-Thong-Tin-Internet/`):**
   - Tinh gọn `SKILL.md` (từ `170` dòng xuống `~115` dòng theo `Progressive Disclosure`), bổ sung Phân tầng Quy mô/Rủi ro `R0–R3`, bước `Indirect Prompting Restate` trước cổng `D1` và bảng lệnh `scripts/bo01_refine_tool.py`.
   - Cập nhật `README.md`, `Methodology.md`, `Architecture.md` (sửa `v6.1` -> `v6.2 × pstack` tại dòng 219 và tích hợp `scripts/bo01_refine_tool.py`), `Quick-Start.md`, `references/multi-signal-search-and-ptc.md`, `references/citation-graph-and-conflict-gate.md` và `templates/source-log.md`, `templates/extraction-and-synthesis-prompts.md`.
4. **Nâng cấp & Tinh gọn Bộ 02 (`Bo-02-Kernel-Registry-SOT/`):**
   - Tinh gọn `SKILL.md` (`~115` dòng), bổ sung Phân tầng Quy mô/Rủi ro `R0–R3`, bước `Indirect Prompting Restate` trước cổng `D1` và bảng lệnh `scripts/bo02_registry_tool.py`.
   - Cập nhật `README.md`, `Methodology.md`, `Architecture.md`, `Quick-Start.md`, `references/freshness-and-deterministic-l2.md`, `references/bo01-bo02-bo03-bridge.md` (Bảng Ánh xạ 4 Nhãn Fable 5.1 + Chuỗi lệnh CLI Liên thông 3 Bộ) và `templates/queues-and-migration-map.md`.
5. **Đồng bộ Bộ 03 (`Bo-03-Vibecode-Kit-v6/`):**
   - Cập nhật `SKILL.md`, `README.md`, `Architecture.md`, `Quick-Start.md` và `references/claim-and-evidence-protocol.md` (Hợp nhất 4 nhãn nhận định Fable 5.1 `OBSERVED | DERIVED (INFERRED) | PRIOR | ASSUMED (UNVERIFIED)` và tích hợp `scripts/bo03_vibecode_tool.py`).
6. **Cập nhật Trình cài đặt (`tools/install-all.sh`), Đóng gói `.skill` / `.docx` & Đồng bộ KI:**
   - Cập nhật `tools/install-all.sh` để cài 3 Bộ (kèm `scripts/*.py` có `chmod +x`) vào cả `~/.gemini/config/skills/` lẫn `~/.claude/skills/` và chạy cổng kiểm thử `--self-test` cho cả 3 Bộ.
   - Đóng gói lại `internet-info-refinement.skill`, `kernel-registry-sot.skill`, `vibecode-kit-v6.skill` và các file `.docx` ở root.
   - Cập nhật `README.md`, `CLAUDE.md`, `CHANGELOG.md` và KI `~/.gemini/knowledge/vibecode-kit-v6-workflow.md`.


**Approval readiness: PASS** - Mọi quyết định phạm vi (`ROW-01`, `ROW-02`, `ROW-03`) và 3 đề xuất mở rộng (`EXP-01`, `EXP-02`, `EXP-03`) cùng bước kiểm duyệt tài liệu `0H` đã được người dùng phê duyệt tường minh (`D1: A`, `D2: A`, `D3: A`, `D4: A`, `D5: A`, `D6: A`, `D7: A`). Số quyết định tồn đọng: `0`.

---

## Step 0I · Temporal Interrogation (Phong van Dong Thoi gian Thuc thi)

```text
  HOUR 1 (Foundation & Archive)      HOUR 2-3 (Core 3 CLI Levers)        HOUR 4 (Docs, Bridge & Templates)   HOUR 5+ (Install, Self-Test & Pack)
  +-------------------------------+  +--------------------------------+  +--------------------------------+  +---------------------------------+
  | - Tạo _Archive/duplicate-     |  | - Xây dựng 3 Deep Module CLI   |  | - Tinh gọn SKILL.md của Bộ 01  |  | - Nâng cấp tools/install-all.sh |
  |   deliverables-2026-10/ và    |  |   bằng Python stdlib:          |  |   (170 -> ~115 dòng) và Bộ 02  |  |   đồng bộ cả ~/.gemini/config/  |
  |   di chuyển 8 file .docx/     |  |   1. bo01_refine_tool.py       |  |   (128 -> ~115 dòng).          |  |   skills/ và ~/.claude/skills/  |
  |   .skill trùng phiên bản.     |->|   2. bo02_registry_tool.py     |->| - Đồng bộ R0..R3, Indirect     |->|   kèm cổng chạy --self-test.    |
  | - Thiết kế chuẩn JSON/YAML    |  |      + wrapper eval_l2.py      |  |   Prompting Restate, 4 nhãn    |  | - Đóng gói lại 3 file .skill,   |
  |   Zero-Dependency dùng chung  |  |   3. bo03_vibecode_tool.py     |  |   Fable 5.1 và cập nhật        |  |   5 file .docx và cập nhật KI   |
  |   cho cả 3 công cụ CLI.       |  | - Chạy --self-test --json.     |  |   Quick-Start + templates/.    |  |   vibecode-kit-v6-workflow.md.  |
  +-------------------------------+  +--------------------------------+  +--------------------------------+  +---------------------------------+
```

- **Giờ 1 (Foundation & Safe Archive):** Dọn sạch 8 file `.docx`/`.skill` hậu tố phiên bản trùng lặp ở thư mục gốc vào `_Archive/duplicate-deliverables-2026-10/` để khóa đúng danh sách file chuẩn trước khi đóng gói mới. Thiết lập bộ hàm đọc/ghi YAML/JSON nguyên tử bằng Python stdlib (`json`, `csv`, `hashlib`, `re`, `ast`, `argparse`, `pathlib`) và tự động tận dụng `PyYAML` nếu môi trường có sẵn.
- **Giờ 2-3 (Core 3 CLI Levers):** Hiện thực hóa 3 công cụ CLI (`bo01_refine_tool.py`, `bo02_registry_tool.py` + `eval_l2.py`, `bo03_vibecode_tool.py`). Điểm cốt lõi cần xử lý ở Giờ 2-3 là hàm tính biểu thức `eval-l2` trong `bo02_registry_tool.py`: tuyệt đối không dùng `eval()` mở của Python mà dùng trình thông dịch cây cú pháp trừu tượng an toàn (`ast.parse` chỉ cho phép các nút toán học `ast.Expression`, `ast.BinOp`, `ast.UnaryOp`, `ast.Constant`, `ast.Name`, `ast.Call` thuộc danh mục hàm toán học trắng `min`, `max`, `round`, `sum`, `abs`).
- **Giờ 4 (Progressive Disclosure, R0–R3, Indirect Prompting & 4-Label Bridge):** Tinh gọn `SKILL.md` của Bộ 01 và Bộ 02 xuống `~115` dòng; cập nhật `Architecture.md`, `Methodology.md`, `Quick-Start.md`, `references/` và `templates/` của cả 3 Bộ; khóa chặt bảng ánh xạ 4 nhãn Fable 5.1 (`OBSERVED | DERIVED | PRIOR | ASSUMED`).
- **Giờ 5+ (Dual-Host Installer, Self-Test Gate & Packaging):** Nâng cấp `tools/install-all.sh` để cài đặt đồng thời vào `~/.gemini/config/skills/` cùng `~/.claude/skills/`, kích hoạt kiểm thử sống `--self-test --json`, đóng gói lại `.skill` và `.docx`, đồng thời cập nhật KI `~/.gemini/knowledge/vibecode-kit-v6-workflow.md`.

---

## Deep Review Sections 1–11

### Current Scope Heading (Published Before Section 1)
- **Approved Baseline (`ROW-01` Option A + `ROW-02` Option A + `ROW-03` Option A):** Nâng cấp toàn diện cả 3 Bộ (`Bo-01`, `Bo-02`, `Bo-03`) lên kiến trúc Tier-1 Full-Stack 4 Lớp (`SKILL.md` + `scripts/*.py` + `references/` + `templates/`), di chuyển 8 file `.docx`/`.skill` trùng phiên bản ở root vào `_Archive/duplicate-deliverables-2026-10/`, đồng bộ trình cài đặt `tools/install-all.sh` cho cả Gemini cùng Claude Code, đóng gói lại `.skill`/`.docx` và cập nhật KI.
- **Approved Selective Expansions (`EXP-01`, `EXP-02`, `EXP-03`):**
  1. `EXP-01`: Trang bị cờ `--self-test --json` (Zero-Dependency Python stdlib) cho cả 3 công cụ CLI và tích hợp cổng kiểm thử sống vào `tools/install-all.sh`.
  2. `EXP-02`: Nhúng khung `Indirect Prompting Restate`, bảng chọn nhanh `R0–R3 Fast-Track` và lệnh gọi CLI vào `templates/` cùng `Quick-Start.md` của Bộ 01 và Bộ 02.
  3. `EXP-03`: Chuẩn hóa Bảng Ánh xạ 4 Nhãn Fable 5.1 (`OBSERVED | DERIVED | PRIOR | ASSUMED` <-> `EXTRACTED | INFERRED | AMBIGUOUS`) cùng chuỗi lệnh CLI liên thông 3 Bộ trong `bo01-bo02-bo03-bridge.md` và `claim-and-evidence-protocol.md`.

---

### Section 1 · Architecture Review

#### 1.1. System Architecture Diagram (Kiến trúc Liên thông 4 Lớp Xuyên 3 Bộ Kỹ Năng)

```text
  +===========================================================================================+
  |                     AI-NATIVE 3-SUITE OPERATING SYSTEM (v2026.10)                         |
  +===========================================================================================+
  |                                                                                           |
  |  [BỘ 01: INTERNET INFO REFINEMENT] (Bo-01-Tinh-Loc-Thong-Tin-Internet/)                   |
  |  +-- Layer 1: SKILL.md (~115 lines · R0..R3 Fast-Track · Indirect Prompting Restate)      |
  |  +-- Layer 2: scripts/bo01_refine_tool.py (Deep Module CLI · Python stdlib)               |
  |  |     |-- ptc-filter       (Lọc & cắt ~1.200 ký tự quanh từ khóa, loại >80% rác HTML)    |
  |  |     |-- audit-echo       (Kiểm tra 독립 origin count >= 2, phát hiện Echo Chamber)      |
  |  |     |-- gate-check       (Chấm 4 điều kiện cổng định lượng Stage 3 -> Stage 4)          |
  |  |     |-- export-bo02      (Xuất Fact Card chuẩn hóa sang L1 YAML cho Bộ 02)             |
  |  |     +-- --self-test      (Kiểm thử nội tại < 200ms trả JSON)                           |
  |  +-- Layer 3 & 4: references/*.md + templates/*.md (4 nhãn Fable 5.1)                     |
  |                                       |                                                   |
  |                                       | (1 lệnh CLI: bo01_refine_tool.py export-bo02)     |
  |                                       v                                                   |
  |  [BỘ 02: KERNEL REGISTRY SOT] (Bo-02-Kernel-Registry-SOT/)                                |
  |  +-- Layer 1: SKILL.md (~115 lines · R0..R3 Fast-Track · Indirect Prompting Restate)      |
  |  +-- Layer 2: scripts/bo02_registry_tool.py + scripts/eval_l2.py (Wrapper tương thích)    |
  |  |     |-- fingerprint      (Chụp ORIGINAL_TREE_FINGERPRINT SHA-256 toàn cây tài liệu)    |
  |  |     |-- audit-freshness  (Đối chiếu sha256(source), đánh dấu FRESH/STALE/EXPIRED)      |
  |  |     |-- eval-l2          (Tính công thức L2 bằng AST Safe Evaluator, 0% dùng eval mở)  |
  |  |     |-- sync-feature-map (Đồng bộ trạng thái L1/L2/L3 sang Feature Map của Bộ 03)      |
  |  |     +-- --self-test      (Kiểm thử nội tại < 200ms trả JSON)                           |
  |  +-- Layer 3 & 4: references/*.md + templates/*.yaml/csv/md                               |
  |                                       |                                                   |
  |                                       | (1 lệnh CLI: bo02_registry_tool.py sync-feature-map)
  |                                       v                                                   |
  |  [BỘ 03: VIBECODE KIT v6.2 x PSTACK] (Bo-03-Vibecode-Kit-v6/)                             |
  |  +-- Layer 1: SKILL.md (102 lines · R0..R3 · Indirect Prompting · 4 nhãn Fable 5.1)       |
  |  +-- Layer 2: scripts/bo03_vibecode_tool.py (Deep Module CLI · Python stdlib)             |
  |  |     |-- init-control-app (Sinh khung ./bin/control-app chuẩn 6 tiêu chí Deep Module)   |
  |  |     |-- wtree-fingerprint(Chụp & đối chiếu WTREE_FINGERPRINT chống ghi đè chéo)        |
  |  |     |-- maintain-features(Quét SHA-256 source_files trong references/features/)        |
  |  |     |-- constraint-check (Kiểm toán 0 em-dash, 0 'comma-va', 0 rò rỉ khóa bí mật)          |
  |  |     +-- --self-test      (Kiểm thử nội tại < 200ms trả JSON)                           |
  |  +-- Layer 3 & 4: references/*.md + templates/*.md                                        |
  |                                       |                                                   |
  |                                       v                                                   |
  |  [DUAL-HOST INSTALLER & DELIVERABLES] (tools/install-all.sh)                              |
  |  +-- Chạy --self-test --json trên cả 3 CLI -> Cài vào ~/.gemini/config/skills & ~/.claude |
  +===========================================================================================+
```

#### 1.2. Coupling, Scaling & Single Points of Failure
- **Tách biệt phụ thuộc (Zero External Coupling):** Cả 3 CLI hoạt động độc lập bằng Python 3 stdlib, giao tiếp với nhau qua định dạng tệp JSON/YAML/CSV/Markdown chuẩn hóa trên đĩa. Nếu người dùng chỉ cài riêng Bộ 01 hoặc Bộ 03, từng công cụ vẫn chạy độc lập 100%.
- **Khắc phục điểm lỗi đơn (`eval_l2.py`):** Tạo cả `scripts/bo02_registry_tool.py` (công cụ đa năng có subcommand `eval-l2`) lẫn `scripts/eval_l2.py` (script mỏng ủy quyền trực tiếp sang `bo02_registry_tool.py eval-l2`) để đảm bảo mọi tài liệu cũ hoặc lệnh gọi `python3 scripts/eval_l2.py --id ...` trong [`Bo-02-Kernel-Registry-SOT/Architecture.md:104`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/Architecture.md#L104) và [`templates/L2-derived-fact.yaml:13`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/templates/L2-derived-fact.yaml#L13) đều chạy trơn tru.
- **Section 1 Verdict:** `0` lỗi kiến trúc còn mở (4 điểm nghẽn kiến trúc phát hiện ở Step 0A đã được giải quyết triệt để trong thiết kế).

---

### Section 2 · Error & Rescue Map

Mọi đường dẫn thực thi trong 3 công cụ CLI và trình cài đặt đều phải bắt ngoại lệ tường minh và trả về JSON `Actionable Error` có trường `root_cause` cùng `next_command` để AI Agent tự sửa ngay ở lượt gọi kế tiếp:

| METHOD / CODEPATH | WHAT CAN GO WRONG | EXCEPTION CLASS | RESCUED? | RESCUE ACTION | USER / AGENT SEES |
|---|---|---|---|---|---|
| `bo01_refine_tool.py :: ptc-filter` | Tệp JSON kết quả tìm kiếm không tồn tại, rỗng hoặc sai cú pháp JSON | `FileNotFoundError`, `json.JSONDecodeError` | `Y` | Bắt lỗi, trả về JSON mã thoát `2` kèm hướng dẫn tạo tệp đầu vào hoặc chạy `--self-test` | `{"status":"ERROR","error_code":"INVALID_INPUT_JSON","root_cause":"...","next_command":"python3 scripts/bo01_refine_tool.py --self-test --json"}` |
| `bo01_refine_tool.py :: audit-echo` | Thiếu cột bắt buộc (`url`, `independent_origin_id`, `trust_tier`) trong `source-log` CSV/JSON | `KeyError`, `ValueError` | `Y` | Báo rõ tên cột bị thiếu và in lệnh mẫu kiểm tra cấu trúc bảng | `{"status":"ERROR","error_code":"MISSING_SOURCE_COLUMNS","root_cause":"Missing column: independent_origin_id","next_command":"..."}` |
| `bo01_refine_tool.py :: export-bo02` | Đường dẫn xuất sang `L1` nằm ngoài thư mục cho phép hoặc chưa tồn tại thư mục đích | `PermissionError`, `OSError` | `Y` | Kiểm tra `Path.resolve()`, tự tạo thư mục cha hợp lệ (nếu không phải `--dry-run`) hoặc trả lỗi đường dẫn an toàn | `{"status":"ERROR","error_code":"EXPORT_PATH_ERROR","root_cause":"...","next_command":"..."}` |
| `bo02_registry_tool.py :: audit-freshness` | Tệp nguồn `source_locator` trong bản ghi `L1` đã bị di chuyển hoặc đổi tên | `FileNotFoundError` | `Y` | Không làm sập tiến trình quét; đánh dấu bản ghi đó là `STALE` (`reason: MISSING_SOURCE_FILE`) và lan truyền sang `L2/L3` | Bản ghi trong báo cáo JSON có `"freshness":"STALE","reason":"MISSING_SOURCE_FILE","next_command":"..."` |
| `bo02_registry_tool.py :: eval-l2` (`& eval_l2.py`) | Công thức `formula` trong `L2` chứa cú pháp không hợp lệ, chia cho `0` hoặc gọi hàm ngoài danh sách toán học trắng | `SyntaxError`, `ZeroDivisionError`, `ValueError`, `KeyError` | `Y` | Trình thông dịch `AST Safe Evaluator` chặn mọi nút AST ngoài toán học cơ bản, bắt `ZeroDivisionError` và trả lỗi kèm tên biến `L1` bị thiếu | `{"status":"ERROR","error_code":"UNSAFE_OR_INVALID_FORMULA","root_cause":"...","next_command":"python3 scripts/bo02_registry_tool.py eval-l2 --help"}` |
| `bo03_vibecode_tool.py :: maintain-features` | Tệp mã nguồn liệt kê trong `source_files` của `references/features/*.md` không tồn tại hoặc lệch mã băm SHA-256 | `FileNotFoundError`, `ValueError` | `Y` | Đánh dấu tính năng là `STALE_HASH` hoặc `MISSING_SOURCE`, in lệnh cập nhật lại bảng `Feature Map` | `{"status":"STALE","stale_features":[...],"next_command":"python3 scripts/bo03_vibecode_tool.py maintain-features --update --dry-run --json"}` |
| `bo03_vibecode_tool.py :: constraint-check` | Phát hiện dấu `em-dash` (`-`), cụm `dấu phẩy trước chữ và` hoặc chuỗi giống khóa bí mật (`sk-`, `ghp_`, `AIza`) trong tệp Markdown | `ConstraintViolation` (Exit `1`) | `Y` | Liệt kê chính xác `file:line`, loại vi phạm và gợi ý chuỗi thay thế hợp lệ | `{"status":"FAIL","violations":[{"file":"...","line":12,"rule":"NO_EM_DASH"}],"next_command":"..."}` |
| `tools/install-all.sh :: self-test gate` | Một trong 3 công cụ CLI trả mã lỗi khác `0` khi chạy `--self-test --json` | Shell Exit `!= 0` (`set -euo pipefail`) | `Y` | Dừng ngay quá trình cài đặt trước khi ghi đè `~/.gemini` / `~/.claude`, in rõ tên script lỗi | Thông báo lỗi rõ ràng trên terminal kèm lệnh chạy riêng script đó để gỡ lỗi |

- **Section 2 Verdict:** `8` đường dẫn lỗi được lập bản đồ đầy đủ, `0` CRITICAL GAPS.

---

### Section 3 · Security & Threat Model

1. **Chặn Thực thi Mã tùy ý trong `eval-l2` (`No Raw eval()`):**
   - **Nguy cơ:** Nếu `bo02_registry_tool.py :: eval-l2` dùng hàm `eval()` mặc định của Python để tính trường `formula` trong tệp `L2-derived-fact.yaml`, một tệp YAML bị chỉnh sửa độc hại có thể chèn `__import__('os').system(...)`.
   - **Biện pháp bảo vệ tất định:** Sử dụng `ast.parse(expr, mode='eval')` và duyệt cây AST qua bộ kiểm duyệt trắng (`SAFE_AST_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.USub, ast.UAdd, ast.Call)` và `SAFE_FUNCTIONS = {'min': min, 'max': max, 'round': round, 'sum': sum, 'abs': abs}`). Bất kỳ lời gọi thuộc tính (`ast.Attribute`), truy cập chỉ mục (`ast.Subscript`), lambda hay hàm lạ nào đều bị từ chối ngay lập tức với mã lỗi `UNSAFE_OR_INVALID_FORMULA`. Kịch bản này được kiểm thử tự động ngay trong `--self-test`.
2. **Cách ly Dữ liệu Web Không Tin Cậy trong `ptc-filter` (`Prompt Injection Delimiters`):**
   - Khi `bo01_refine_tool.py :: ptc-filter` cắt các đoạn trích (`snippets`) từ nội dung web, công cụ tự động loại bỏ các thẻ `<script>`, `<style>`, bình luận HTML ẩn và bọc kết quả trong trường dữ liệu JSON tách biệt kèm cờ `"untrusted_external_content": true` để nhắc Agent chỉ trích xuất dữ liệu thực nghiệm, không thực thi mệnh lệnh nằm trong văn bản web.
3. **Chống Leo thang Đường dẫn (`Path Traversal Guard`) & Bảo vệ `Zero-Secret Policy`:**
   - Các lệnh ghi tệp (`export-bo02`, `init-control-app`, `sync-feature-map`) đều kiểm tra đường dẫn đích và hỗ trợ `--dry-run` để xem trước thay đổi mà không chạm vào đĩa.
   - Lệnh `bo03_vibecode_tool.py constraint-check` tích hợp bộ quét biểu thức chính quy phát hiện các mẫu khóa API phổ biến (`sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{30,}`, `AIza[0-9A-Za-z\-_]{35}`, `tvly-[A-Za-z0-9\-_]{16,}`) nhằm bảo vệ tuyệt đối quy tắc `Zero-Secret Policy` (`CLAUDE.md:19`).
- **Section 3 Verdict:** `0` lỗ hổng bảo mật mức Cao còn mở.

---

### Section 4 · Data Flow & Interaction Edge Cases

#### 4.1. Four-Path Data Flow Diagram (Happy, Nil, Empty & Error Paths)

```text
  [INPUT: Raw Search JSON / L1-L2 YAML / Feature Markdown]
                         |
                         v
            +-------------------------+
            | 1. INPUT & PATH CHECK   |---> [NIL PATH: Missing file / None arg]
            +------------+------------+     -> Return JSON {"status":"ERROR",
                         |                     "error_code":"MISSING_INPUT",
                         v                     "next_command":"... --help"} (Exit 2)
            +-------------------------+
            | 2. SCHEMA & EMPTY CHECK |---> [EMPTY PATH: 0 snippets / 0 records]
            +------------+------------+     -> Return JSON {"status":"EMPTY",
                         |                     "items_processed":0,
                         |                     "next_command":"..."} (Exit 0, no crash)
                         v
            +-------------------------+
            | 3. DETERMINISTIC ENGINE |---> [ERROR PATH: Corrupted YAML/JSON,
            | - PTC Window Slicing    |      Unsafe AST node in L2 formula,
            | - SHA-256 Streaming     |      DivByZero, or Constraint violation]
            | - AST Safe Math Eval    |     -> Rescue exception, log root_cause,
            +------------+------------+        return JSON Actionable Error (Exit 1/2)
                         |
                         v
            +-------------------------+
            | 4. DRY-RUN / PERSIST    |---> If --dry-run: skip disk write,
            | (Atomic write or stdout)|     return {"status":"DRY_RUN_OK", "preview":...}
            +------------+------------+     If live: atomic write + return JSON receipt
                         |
                         v
  [HAPPY PATH OUTPUT: Deterministic JSON Receipt + Updated Artifact]
```

#### 4.2. Edge Cases Mapped (8 Trường hợp Biên Được Xử lý Tất định)
1. **Tệp tìm kiếm web có bài viết chứa toàn mã rác HTML hoặc dài `> 100.000` ký tự:** `ptc-filter` chuẩn hóa khoảng trắng, loại bỏ thẻ `<script>/<style>` và chỉ giữ tối đa `N` cửa sổ ngữ cảnh (`~1.200` ký tự quanh từ khóa), đảm bảo đầu ra không bao giờ làm tràn cửa sổ ngữ cảnh của Agent.
2. **Nhiều URL khác nhau nhưng cùng chép lại từ 1 thông cáo báo chí gốc (`Echo Chamber`):** `audit-echo` gom nhóm theo `independent_origin_id` (hoặc tên miền gốc nếu chưa gán mã gốc độc lập) và chỉ tính là `1` nguồn gốc độc lập, chặn đứngảo giác đồng thuận.
3. **Môi trường Python trên máy người dùng không cài gói `PyYAML`:** Cả 3 CLI đều có bộ đọc/ghi tập con YAML chuẩn của bản ghi `Fact Card` / `L1` / `L2` (hỗ trợ cả JSON-in-YAML vì JSON hợp lệ là tập con chuẩn của YAML 1.2) bằng Python stdlib thuần túy, đồng thời tự động dùng `yaml.safe_load` nếu `PyYAML` có sẵn.
4. **Biểu thức `L2` tham chiếu đến một mã `L1` đang ở trạng thái `STALE` hoặc `EXPIRED`:** `eval-l2` phát hiện trạng thái đầu vào không còn `FRESH`, gắn cờ `"derived_freshness": "STALE_DEPENDENCY"` trong kết quả JSON để cảnh báo Agent không đưa số liệu cũ vào báo cáo chính thức.
5. **Tệp nhị phân hoặc tệp lớn trong thư mục khi chạy `fingerprint` / `wtree-fingerprint`:** Hàm băm SHA-256 đọc theo từng khối `65.536` byte (`streaming chunks`) và tự động bỏ qua các thư mục `.git/`, `__pycache__/`, `.DS_Store`, `node_modules/`.
6. **Chạy công cụ với cờ `--dry-run`:** Mọi lệnh có khả năng ghi tệp (`export-bo02`, `eval-l2 --write`, `sync-feature-map`, `init-control-app`, `maintain-features --update`) đều kiểm tra cờ `--dry-run` trước tiên và chỉ xuất bản xem trước (`preview`) ra JSON mà không tạo hay sửa bất kỳ tệp nào trên đĩa.
7. **Tệp Markdown có dấu `em-dash` nằm trong khối trích dẫn hoặc văn bản tiếng Việt:** `constraint-check` quét chính xác ký tự Unicode `U+2014` (`-`) và mẫu `dấu phẩy trước chữ và` trên các tệp Markdown mục tiêu, báo cáo số dòng chính xác để sửa triệt để.
8. **Chạy `tools/install-all.sh` nhiều lần liên tiếp (`Idempotency`):** Trình cài đặt tạo thư mục đích bằng `mkdir -p`, xóa bản sao cũ trong thư mục đích trước khi `cp -R` bản mới và cấp quyền thực thi `chmod +x` cho toàn bộ `scripts/*.py`.
- **Section 4 Verdict:** `8` trường hợp biên được lập bản đồ đầy đủ, `0` trường hợp bị bỏ sót.

---

### Section 5 · Code Quality Review

- **Chuẩn hóa Cấu trúc Deep Module CLI:** Cả 3 công cụ `bo01_refine_tool.py`, `bo02_registry_tool.py` và `bo03_vibecode_tool.py` tuân thủ cùng một mẫu thiết kế đồng nhất:
  - Sử dụng `argparse` với các subcommand tường minh và hỗ trợ `--dry-run`, `--json`, `--help`, `--self-test` ở cả cấp độ gốc lẫn cấp độ subcommand.
  - Mọi hàm nghiệp vụ trả về cấu trúc từ điển Python (`dict`) chuẩn hóa gồm `status`, `command`, `summary`, `data` và (khi có lỗi) `error_code`, `root_cause`, `next_command`.
  - Độ phức tạp chu trình (`cyclomatic complexity`) của từng hàm được giữ nhỏ gọn (`< 10`), tách bạch rõ lớp парсер đầu vào, lớp tính toán tất định và lớp xuất kết quả.
- **Section 5 Verdict:** `0` lỗi chất lượng mã nguồn.

---

### Section 6 · Test Review

#### 6.1. Test Coverage Diagram (Cơ chế Kiểm thử Tự thân `--self-test` & Kiểm toán Toàn kho)

```text
  +-----------------------------------------------------------------------------+
  |                    MULTI-LAYER VERIFICATION PIPELINE                        |
  +-----------------------------------------------------------------------------+
  |                                                                             |
  |  1. IN-MEMORY SELF-TEST SUITE (--self-test --json in all 3 CLI tools)       |
  |     +-- bo01_refine_tool.py --self-test --json                              |
  |     |     |-- Test PTC window slicing & HTML noise stripping (>75% saved)   |
  |     |     |-- Test Echo-chamber detection (3 URLs same origin -> count=1)   |
  |     |     |-- Test Stage 3->4 Quantitative Gate (PASS & FAIL cases)         |
  |     |     +-- Test Bo-01 Fact Card -> Bo-02 L1 YAML export (--dry-run)      |
  |     +-- bo02_registry_tool.py --self-test --json (& eval_l2.py)             |
  |     |     |-- Test SHA-256 directory tree fingerprint determinism           |
  |     |     |-- Test Freshness audit (FRESH -> STALE propagation on edit)     |
  |     |     |-- Test AST Safe L2 Evaluator (math PASS & unsafe AST REJECT)    |
  |     |     +-- Test Bo-02 L1/L2 -> Bo-03 Feature Map sync (--dry-run)        |
  |     +-- bo03_vibecode_tool.py --self-test --json                            |
  |           |-- Test ./bin/control-app scaffold generation (--dry-run)        |
  |           |-- Test WTREE_FINGERPRINT match & mismatch detection             |
  |           |-- Test Feature Map SHA-256 drift detection                      |
  |           +-- Test Constraint Loop scanner (em-dash, 'comma-va', secret regex)  |
  |                                    |                                        |
  |                                    v                                        |
  |  2. REPOSITORY CONSTRAINT & PACKAGING AUDIT                                 |
  |     +-- Run bo03_vibecode_tool.py constraint-check across all 3 suites      |
  |     +-- Verify 0 em-dashes, 0 'comma-va', 0 secrets in Bo-01, Bo-02, Bo-03      |
  |     +-- Run tools/install-all.sh (executes all 3 self-tests live)           |
  +-----------------------------------------------------------------------------+
```

- **Định nghĩa `no_claim` (Ngưỡng không suy diễn vượt bằng chứng):** Các bài kiểm thử `--self-test` chỉ khẳng định tính đúng đắn tất định của bộ lọc PTC, bộ kiểm toán mã băm SHA-256, bộ tính công thức toán học `L2` qua AST và bộ quét quy tắc văn phong/bảo mật; không tự động khẳng định độ chính xác ngữ nghĩa của nội dung bài viết trên Internet nếu nguồn gốc bên ngoài cung cấp số liệu sai.
- **Section 6 Verdict:** Sơ đồ kiểm thử đầy đủ, `0` khoảng trống kiểm thử (`0` test gaps).

---

### Section 7 · Performance Review

- **Tốc độ Thực thi CLI (`< 200ms`):** Cả 3 công cụ CLI chỉ nạp các mô-đun chuẩn của Python (`sys`, `os`, `json`, `csv`, `re`, `ast`, `hashlib`, `argparse`, `pathlib`, `datetime`, ` tempfile`), không nạp các thư viện nặng như `pandas` hay `numpy`, giúp thời gian khởi động và chạy `--self-test --json` dưới `200ms`.
- **Tiết kiệm Token Ngữ cảnh (`70%–90%`):**
  - Tinh gọn `Bo-01/SKILL.md` từ `170` dòng xuống `~115` dòng và `Bo-02/SKILL.md` từ `128` dòng xuống `~115` dòng giúp giảm lượng token nạp ban đầu mỗi khi kích hoạt skill.
  - Công cụ `bo01_refine_tool.py ptc-filter` cắt bỏ hơn `80%` rác giao diện HTML/menu/footer trước khi đưa vào cửa sổ ngữ cảnh của mô hình.
- **Section 7 Verdict:** `0` điểm nghẽn hiệu năng.

---

### Section 8 · Observability & Debuggability Review

- **Chuẩn Hóa Đầu Ra Quan Sát Được (`Structured JSON Receipts`):** Mọi lệnh trong cả 3 công cụ CLI khi gắn cờ `--json` đều xuất ra cấu trúc JSON đồng nhất có:
  - `status`: `"OK" | "DRY_RUN_OK" | "PASS" | "FAIL" | "STALE" | "EMPTY" | "ERROR"`
  - `tool` & `subcommand`: Tên công cụ và lệnh con vừa chạy
  - `metrics`: Các chỉ số định lượng đo đạc thực tế (như `raw_chars`, `filtered_chars`, `reduction_pct`, `independent_origin_count`, `fresh_count`, `stale_count`)
  - `next_command`: Câu lệnh gợi ý tiếp theo để Agent hoặc người dùng chạy ngay mà không phải đoán.
- **Section 8 Verdict:** `0` khoảng trống quan sát (`0` observability gaps).

---

### Section 9 · Deployment & Rollout Review

#### 9.1. Deployment Sequence Diagram

```text
  [Step 1: Archive Duplicate Root Deliverables]
     Move 8 version-suffixed .docx/.skill files -> _Archive/duplicate-deliverables-2026-10/
                         |
                         v
  [Step 2: Build & Self-Test 3 CLI Tools]
     Write scripts/bo01_refine_tool.py, scripts/bo02_registry_tool.py (+ eval_l2.py),
     scripts/bo03_vibecode_tool.py -> Run --self-test --json on all 3 (Must PASS 100%)
                         |
                         v
  [Step 3: Upgrade Docs, References & Templates Across Bo-01, Bo-02, Bo-03]
     Apply Progressive Disclosure (~115 lines SKILL.md), R0..R3, Indirect Prompting,
     4-Label Fable 5.1 Matrix -> Run bo03_vibecode_tool.py constraint-check (Must PASS 0 violations)
                         |
                         v
  [Step 4: Rebuild .skill & .docx Deliverables + Sync Dual Hosts & KI]
     Package 3 .skill archives + 5 .docx files -> Run tools/install-all.sh
     (installs to ~/.gemini/config/skills/ & ~/.claude/skills/ + runs Self-Test Gate)
     -> Update KI ~/.gemini/knowledge/vibecode-kit-v6-workflow.md
```

#### 9.2. Rollback Flowchart

```text
  [Detect Failure During Self-Test, Constraint Check, or Packaging]
                         |
                         +---> [If CLI Self-Test or Constraint Check Fails]
                         |        Fix offending file:line reported in JSON next_command
                         |        and re-run verification gate before touching ~/.gemini or ~/.claude
                         |
                         +---> [If Rollback of Root Deliverables is Needed]
                                  Restore archived files from _Archive/duplicate-deliverables-2026-10/
                                  and run `git checkout -- Bo-01* Bo-02* Bo-03* tools/install-all.sh`
```

- **Section 9 Verdict:** `0` rủi ro triển khai chưa được kiểm soát (`Reversibility: 5/5`).

---

### Section 10 · Long-Term Trajectory Review

- **Điểm Khả Đảo Ngược (`Reversibility: 5/5`):** Toàn bộ thay đổi là bổ sung lớp công cụ `scripts/*.py` không phụ thuộc thư viện ngoài, đồng bộ tài liệu Markdown và lưu trữ an toàn các tệp trùng vào `_Archive/duplicate-deliverables-2026-10/`.
- **Đánh giá Hồi cố Các Đề xuất Mở rộng Đã Nhận (`Selective Expansion Retrospective`):**
  - `EXP-01` (`--self-test` + cổng kiểm tra trong `install-all.sh`), `EXP-02` (`R0–R3 Fast-Track` + `Indirect Prompting Restate` trong `templates/` & `Quick-Start.md`) và `EXP-03` (Ma trận 4 nhãn Fable 5.1 + cầu nối CLI liên thông 3 Bộ) gắn kết chặt chẽ với nhau, biến 3 Bộ từ tài liệu rời rạc thành một dây chuyền khép kín mà không làm phình độ phức tạp bảo trì.
- **Section 10 Verdict:** `Reversibility: 5/5`, `0` khoản nợ kỹ thuật mới.

---

### Section 11 · Design & UX Review

- **Trạng thái:** `SKIPPED (no UI scope)` - Kế hoạch này nâng cấp 3 Bộ phương pháp kỹ năng AI-Native (`Markdown + CLI Python stdlib + Shell Installer`), không có giao diện người dùng đồ họa (GUI/Web Frontend). Trải nghiệm dòng lệnh (`CLI DX`) đã được chuẩn hóa qua `--help`, `--dry-run`, `--json` và `next_command`.

---

## Required Outputs · Stage 1 (Plan Body, Registries, Diagrams & Tasks)

### 1. NOT in Scope (Các hạng mục nằm ngoài phạm vi)
- **Xây dựng dịch vụ Web UI / Database Server chạy nền cho 3 Bộ kỹ năng (`Rejected` trong định hướng kiến trúc Step 0A/0F):** Cả 3 Bộ được thiết kế theo triết lý gọn nhẹ, chạy trực tiếp trên kho mã nguồn cục bộ qua tệp phẳng (`Markdown/YAML/CSV/JSON`) và Python stdlib để không tạo gánh nặng vận hành hạ tầng.
- **Sử dụng thư viện ngoài nặng nề (`pandas`, `scipy`, `sqlalchemy`) trong `scripts/*.py` (`Rejected` theo `EXP-01`):** Chỉ dùng Python 3 stdlib (kèm hỗ trợ tùy chọn `PyYAML` nếu có) để đảm bảo chạy tức thì trên mọi máy Mac/Linux.
- **Các hạng mục hoãn lại (`Deferred to TODOS.md`):** `0` hạng mục (Người dùng đã chọn phương án hoàn chỉnh `10/10` ở `ROW-01` và chấp thuận cả 3 đề xuất `EXP-01`, `EXP-02`, `EXP-03`).

### 2. What Already Exists (Tài nguyên có sẵn được tái sử dụng)
- [`Bo-03-Vibecode-Kit-v6/SKILL.md:1-102`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-03-Vibecode-Kit-v6/SKILL.md#L1-L102) và [`Bo-03-Vibecode-Kit-v6/Architecture.md:1-130`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-03-Vibecode-Kit-v6/Architecture.md#L1-L130): Đã có sẵn khung phân tầng `R0..R3`, `Indirect Prompting Restate` và triết lý `pstack` - được dùng làm chuẩn tham chiếu để đồng bộ sang Bộ 01 và Bộ 02.
- [`Bo-02-Kernel-Registry-SOT/references/bo01-bo02-bo03-bridge.md:1-72`](file:///Users/tuandunghoang/projects/vibecode-kit/Bo-02-Kernel-Registry-SOT/references/bo01-bo02-bo03-bridge.md#L1-L72): Đã có bảng ánh xạ trường dữ liệu cơ sở - được nâng cấp thêm Ma trận 4 Nhãn Fable 5.1 và chuỗi lệnh CLI liên thông.
- [`tools/install-all.sh:1-46`](file:///Users/tuandunghoang/projects/vibecode-kit/tools/install-all.sh#L1-L46): Đã có khung cài đặt cho `~/.gemini/config/skills/` - được mở rộng để cài đồng thờiทั้ง 3 Bộ vào `~/.claude/skills/` và chạy cổng kiểm thử `--self-test`.

### 3. Dream State Delta (Khoảng cách tới Trạng thái Lý tưởng 12 Tháng)
- Sau khi hoàn thành kế hoạch này, kho lưu trữ đạt **100% trạng thái mục tiêu** cho kiến trúc Tier-1 Full-Stack 4 Lớp trên cả 3 Bộ: có đủ công cụ CLI thực thi tất định (`bo01_refine_tool.py`, `bo02_registry_tool.py` + `eval_l2.py`, `bo03_vibecode_tool.py`), có tự kiểm thử `--self-test --json`, đồng bộ hoàn toàn phân tầng `R0..R3`, `Indirect Prompting Restate` và 4 nhãn Fable 5.1 trên cả Gemini lẫn Claude Code.

### 4. Failure Modes Registry

```text
  CODEPATH                                  | FAILURE MODE                     | RESCUED? | TEST? | USER SEES?                     | LOGGED?
  ------------------------------------------|----------------------------------|----------|-------|--------------------------------|--------
  bo01_refine_tool.py :: ptc-filter         | Invalid/missing search JSON      | Y        | Y     | JSON error + next_command      | Y
  bo01_refine_tool.py :: audit-echo         | Missing origin/tier columns      | Y        | Y     | JSON error + column name       | Y
  bo01_refine_tool.py :: gate-check         | Unresolved High/Med conflicts    | Y        | Y     | JSON gate=BLOCKED + reasons    | Y
  bo01_refine_tool.py :: export-bo02        | Invalid output path / dry-run    | Y        | Y     | JSON preview or path error     | Y
  bo02_registry_tool.py :: fingerprint      | Missing target directory         | Y        | Y     | JSON error + next_command      | Y
  bo02_registry_tool.py :: audit-freshness  | Missing source file in L1        | Y        | Y     | Marked STALE + reason in JSON  | Y
  bo02_registry_tool.py :: eval-l2          | Unsafe AST node or DivByZero     | Y        | Y     | JSON error (AST blocked)       | Y
  bo02_registry_tool.py :: sync-feature-map | Stale L1/L2 propagated to Bo-03  | Y        | Y     | JSON sync report + STALE flag  | Y
  bo03_vibecode_tool.py :: init-control-app | Existing file overwrite risk     | Y        | Y     | Protected by --dry-run/check   | Y
  bo03_vibecode_tool.py :: wtree-fingerprint| Worktree SHA-256 drift detected  | Y        | Y     | JSON status=DRIFT_DETECTED     | Y
  bo03_vibecode_tool.py :: maintain-features| Feature source file hash changed | Y        | Y     | JSON stale_features list       | Y
  bo03_vibecode_tool.py :: constraint-check | Em-dash, 'comma-va', or secret leak  | Y        | Y     | JSON violations file:line list | Y
  tools/install-all.sh :: self-test gate    | Any CLI self-test returns != 0   | Y        | Y     | Aborts install with clear msg  | Y
```
- **Tổng số:** `13` failure modes, `0` CRITICAL GAPS (không có hàng nào `RESCUED=N, TEST=N, USER SEES=Silent`).

### 5. Scope Expansion Decisions (`SELECTIVE EXPANSION`)
- **Accepted (Đã duyệt đưa vào phạm vi thực thi):**
  1. `EXP-01`: Trang bị cờ `--self-test --json` (Zero-Dependency Python stdlib) cho cả 3 CLI (`bo01_refine_tool.py`, `bo02_registry_tool.py`, `bo03_vibecode_tool.py`) và tích hợp cổng kiểm thử sống vào `tools/install-all.sh`.
  2. `EXP-02`: Nhúng khung `Indirect Prompting Restate`, bảng chọn `R0–R3 Fast-Track` và lệnh gọi CLI vào `templates/` và `Quick-Start.md` của Bộ 01 & Bộ 02.
  3. `EXP-03`: Chuẩn hóa Bảng Ánh xạ 4 Nhãn Fable 5.1 (`OBSERVED | DERIVED | PRIOR | ASSUMED` <-> `EXTRACTED | INFERRED | AMBIGUOUS`) và cầu nối CLI liên thông 3 Bộ trong `bo01-bo02-bo03-bridge.md` & `claim-and-evidence-protocol.md`.
- **Deferred (Hoãn sang `TODOS.md`):** Không có (`0` items).
- **Skipped (Từ chối):** Không có (`0` items).

### 6. Mandatory State Machine & Error Flow Diagrams

#### State Machine Diagram (Vòng đời Thực thi & Đồng bộ Mã băm Xuyên 3 Bộ)

```text
  [RAW WEB SOURCES]
         |
         | (bo01_refine_tool.py ptc-filter & audit-echo)
         v
  [CANDIDATE CLAIMS] ---(Conflict > 0 or Origin < 2)---> [BLOCKED AT GATE D3]
         |                                                       |
         | (bo01_refine_tool.py gate-check -> PASS)              | (Re-query / Drop claim)
         v                                                       v
  [VERIFIED FACT CARD] <-----------------------------------------+
         |
         | (bo01_refine_tool.py export-bo02)
         v
  [BO-02 L1/L2/L3 SOT: FRESH] ---(Source file edited / TTL passed)---> [SOT: STALE / EXPIRED]
         |                                                                     |
         | (bo02_registry_tool.py eval-l2 & sync-feature-map)                  | (Re-verify & update hash)
         v                                                                     v
  [BO-03 FEATURE MAP: SYNCED] <------------------------------------------------+
         |
         | (bo03_vibecode_tool.py maintain-features & constraint-check -> PASS)
         v
  [SHIPPED DELIVERABLE (.skill / .docx / Dual-Host Installed)]
```

#### Error Flow Diagram (Chu trình Tự Phục hồi Qua `Actionable Error` JSON)

```text
  [Agent / User runs scripts/bo0X_tool.py <subcommand> --json]
                         |
                         v
           +---------------------------+
           | Exception or Gate Failure |
           +-------------+-------------+
                         |
                         v
  [CLI catches exception & emits Structured JSON to stdout (Exit 1 or 2)]
  {
    "status": "ERROR",
    "error_code": "...",
    "root_cause": "Exact file:line or missing field reason",
    "next_command": "Exact runnable command to fix or inspect"
  }
                         |
                         v
  [Agent reads JSON.next_command -> Executes repair without guessing]
```

### 7. Stale Diagram Audit (Kiểm toán Sơ đồ ASCII trong Các Tệp Chạm Tới)

| File:Line | Sơ đồ hiện tại | Trạng thái | Hành động trong kế hoạch |
|---|---|---|---|
| `Bo-01-Tinh-Loc-Thong-Tin-Internet/Architecture.md:10-64` | Sơ đồ 7 Giai đoạn cố định của Bộ 01 | `STALE` (Thiếu phân tầng `R0–R3`, `Indirect Prompting Restate` và lệnh `scripts/bo01_refine_tool.py`) | Cập nhật sơ đồ để bổ sung cổng `R0–R3 Fast-Track`, `Indirect Prompting Restate` và các điểm gọi `bo01_refine_tool.py`. |
| `Bo-02-Kernel-Registry-SOT/Architecture.md:10-44` | Sơ đồ 5 Phase cố định của Bộ 02 | `STALE` (Thiếu phân tầng `R0–R3`, `Indirect Prompting Restate` và `scripts/bo02_registry_tool.py`) | Cập nhật sơ đồ để bổ sung `R0–R3 Fast-Track`, `Indirect Prompting Restate` và các lệnh `bo02_registry_tool.py`. |
| `Bo-02-Kernel-Registry-SOT/references/bo01-bo02-bo03-bridge.md:8-32` | Sơ đồ Liên thông Dữ liệu 3 Bộ | `STALE` (Chưa hiển thị 3 lệnh CLI cầu nối và 4 nhãn Fable 5.1 thống nhất) | Cập nhật sơ đồ gắn trực tiếp `bo01_refine_tool.py export-bo02` -> `bo02_registry_tool.py sync-feature-map` -> `bo03_vibecode_tool.py maintain-features`. |
| `Bo-03-Vibecode-Kit-v6/Architecture.md:10-43` | Sơ đồ Kiến trúc 5 Tầng `v6.2 × pstack` | `ACCURATE` (Chỉ cần gắn thêm tham chiếu `scripts/bo03_vibecode_tool.py` ở tầng đòn bẩy) | Bổ sung chú thích `scripts/bo03_vibecode_tool.py` bên cạnh `./bin/control-app`. |
| `Bo-03-Vibecode-Kit-v6/Methodology.md:23-49` | Sơ đồ Ma trận Điều phối & Quy trình | `ACCURATE` | Giữ nguyên. |

---

## Implementation Tasks

Synthesized from this review's findings. Each task derives from a specific finding above. Run with Claude Code or Codex; checkbox as you ship.
*(Assumption on effort ratios: scaffolding/packaging ~30x, CLI tool engineering with AST/self-test ~25x, multi-suite documentation & progressive disclosure ~15x).*

- [ ] **T1 (P1, human: ~1h / CC: ~3min)** - `Repository Root & Archive` - Archive 8 duplicate version-suffixed `.docx` and `.skill` deliverables into `_Archive/duplicate-deliverables-2026-10/`
  - Surfaced by: Step 0A Premise Challenge (Điểm nghẽn 4) & Decision `ROW-03` (`D3: A`)
  - Files: `_Archive/duplicate-deliverables-2026-10/`, `Bo-01-Tinh-Loc-Thong-Tin-Internet-v2.0.docx`, `Bo-02-Kernel-Registry-SOT-v2.0.docx`, `Bo-03-Vibecode-Kit-v6.1.docx`, `Bo-03-Vibecode-Kit-v6.2.docx`, `internet-info-refinement-v2.0.skill`, `kernel-registry-sot-v2.0.skill`, `vibecode-kit-v6.1.skill`, `vibecode-kit-v6.2.skill`
  - Verify: `ls -1 *.docx *.skill && ls -1 _Archive/duplicate-deliverables-2026-10/`
- [ ] **T2 (P1, human: ~4h / CC: ~10min)** - `Bo-01 CLI Lever` - Build `Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py` (`ptc-filter`, `audit-echo`, `gate-check`, `export-bo02`, `--dry-run`, `--json`, `--help`, `--self-test`)
  - Surfaced by: Step 0A (Điểm nghẽn 1), Section 1–8 & Decisions `ROW-01` (`D1: A`), `EXP-01` (`D4: A`)
  - Files: `Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py`
  - Verify: `python3 Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py --self-test --json`
- [ ] **T3 (P1, human: ~5h / CC: ~12min)** - `Bo-02 CLI Lever & AST Safe Evaluator` - Build `Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py` (`fingerprint`, `audit-freshness`, `eval-l2` with AST whitelist evaluator, `sync-feature-map`, `--dry-run`, `--json`, `--help`, `--self-test`) and backward-compatible wrapper `Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py`
  - Surfaced by: Step 0A (Điểm nghẽn 1 · missing `scripts/eval_l2.py` at `Bo-02/Architecture.md:104`), Section 2–3 & Decisions `ROW-01` (`D1: A`), `EXP-01` (`D4: A`)
  - Files: `Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py`, `Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py`
  - Verify: `python3 Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py --self-test --json && python3 Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py --self-test --json`
- [ ] **T4 (P1, human: ~4h / CC: ~10min)** - `Bo-03 CLI Lever` - Build `Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py` (`init-control-app`, `wtree-fingerprint`, `maintain-features`, `constraint-check`, `--dry-run`, `--json`, `--help`, `--self-test`)
  - Surfaced by: Step 0A (Điểm nghẽn 1), Section 1–8 & Decisions `ROW-01` (`D1: A`), `EXP-01` (`D4: A`)
  - Files: `Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py`
  - Verify: `python3 Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py --self-test --json`
- [ ] **T5 (P1, human: ~4h / CC: ~12min)** - `3-Suite Docs, Progressive Disclosure, R0-R3 & 4-Label Bridge` - Trim `Bo-01/SKILL.md` & `Bo-02/SKILL.md` to `~115` lines; add `R0–R3 Fast-Track`, `Indirect Prompting Restate`, CLI commands, and Unified 4-Label Fable 5.1 Claim Matrix across `Bo-01`, `Bo-02`, and `Bo-03`
  - Surfaced by: Step 0A (Điểm nghẽn 2 & 3), Section 7 Stale Diagram Audit & Decisions `ROW-01` (`D1: A`), `EXP-02` (`D5: A`), `EXP-03` (`D6: A`)
  - Files: `Bo-01-Tinh-Loc-Thong-Tin-Internet/SKILL.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/README.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/Methodology.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/Architecture.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/Quick-Start.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/references/multi-signal-search-and-ptc.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/references/citation-graph-and-conflict-gate.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/templates/source-log.md`, `Bo-01-Tinh-Loc-Thong-Tin-Internet/templates/extraction-and-synthesis-prompts.md`, `Bo-02-Kernel-Registry-SOT/SKILL.md`, `Bo-02-Kernel-Registry-SOT/README.md`, `Bo-02-Kernel-Registry-SOT/Methodology.md`, `Bo-02-Kernel-Registry-SOT/Architecture.md`, `Bo-02-Kernel-Registry-SOT/Quick-Start.md`, `Bo-02-Kernel-Registry-SOT/references/freshness-and-deterministic-l2.md`, `Bo-02-Kernel-Registry-SOT/references/bo01-bo02-bo03-bridge.md`, `Bo-02-Kernel-Registry-SOT/templates/queues-and-migration-map.md`, `Bo-03-Vibecode-Kit-v6/SKILL.md`, `Bo-03-Vibecode-Kit-v6/README.md`, `Bo-03-Vibecode-Kit-v6/Architecture.md`, `Bo-03-Vibecode-Kit-v6/Quick-Start.md`, `Bo-03-Vibecode-Kit-v6/references/claim-and-evidence-protocol.md`, `README.md`, `CLAUDE.md`, `CHANGELOG.md`
  - Verify: `python3 Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py constraint-check --paths Bo-01-Tinh-Loc-Thong-Tin-Internet Bo-02-Kernel-Registry-SOT Bo-03-Vibecode-Kit-v6 README.md CLAUDE.md CHANGELOG.md --json`
- [ ] **T6 (P1, human: ~2h / CC: ~6min)** - `Dual-Host Installer, Deliverables Packaging & KI Sync` - Upgrade `tools/install-all.sh` (sync to `~/.gemini/config/skills/` and `~/.claude/skills/` + run live `--self-test` gate), rebuild `.skill` and `.docx` deliverables, and update KI `~/.gemini/knowledge/vibecode-kit-v6-workflow.md`
  - Surfaced by: Step 0A (Điểm nghẽn 4), Section 9 & Decisions `ROW-01` (`D1: A`), `EXP-01` (`D4: A`)
  - Files: `tools/install-all.sh`, `internet-info-refinement.skill`, `kernel-registry-sot.skill`, `vibecode-kit-v6.skill`, `Bo-01-Tinh-Loc-Thong-Tin-Internet.docx`, `Bo-02-Kernel-Registry-SOT.docx`, `Bo-03-Vibecode-Kit-v6.docx`, `Cam-Nang-Toan-Trinh-Lam-San-Pham-A-Den-Z.docx`, `Tai-Lieu-Ky-Thuat-Toan-Dien-3-Bo-Skill-AI-Native.docx`, `/Users/tuandunghoang/.gemini/knowledge/vibecode-kit-v6-workflow.md`
  - Verify: `bash tools/install-all.sh`

---

## Completion Summary

```text
  +====================================================================+
  |            MEGA PLAN REVIEW - COMPLETION SUMMARY                   |
  +====================================================================+
  | Mode selected        | SELECTIVE EXPANSION                         |
  | System Audit         | 52 files (3,704 lines); 0 scripts/ dirs;    |
  |                      | missing eval_l2.py; taxonomy & host drift   |
  | Step 0               | SELECTIVE EXPANSION; ROW-01..03 & EXP-01..03|
  |                      | all approved (D1:A, D2:A, D3:A, D4:A..D7:A) |
  | Section 1  (Arch)    | 4 bottlenecks resolved, 0 open issues       |
  | Section 2  (Errors)  | 8 error paths mapped, 0 GAPS                |
  | Section 3  (Security)| 3 threats mitigated (AST whitelist), 0 High |
  | Section 4  (Data/UX) | 8 edge cases mapped, 0 unhandled            |
  | Section 5  (Quality) | 0 issues found (shared stdlib CLI pattern)  |
  | Section 6  (Tests)   | Diagram produced, 0 gaps (--self-test suite)|
  | Section 7  (Perf)    | 0 issues found (<200ms CLI, 70-90% PTC save)|
  | Section 8  (Observ)  | 0 gaps found (JSON receipts + next_command) |
  | Section 9  (Deploy)  | 0 risks flagged (_Archive + self-test gate) |
  | Section 10 (Future)  | Reversibility: 5/5, debt items: 0           |
  | Section 11 (Design)  | SKIPPED (no UI scope)                       |
  +--------------------------------------------------------------------+
  | NOT in scope         | written (2 items)                           |
  | What already exists  | written                                     |
  | Dream state delta    | written (100% 4-layer target achieved)      |
  | Error/rescue registry| 8 rows, 0 CRITICAL GAPS                     |
  | Failure modes        | 13 total, 0 CRITICAL GAPS                   |
  | TODOS.md updates     | 0 items proposed (all 3 expansions accepted)|
  | Scope proposals      | 3 proposed, 3 accepted (EXP + SEL)          |
  | CEO plan             | written                                     |
  | Outside voice        | codex unavailable (CLI model version check) |
  | Lake Score           | 1/1 recommendations chose complete option   |
  | Diagrams produced    | 9 (Dream, Temporal, Arch, DataFlow, Test,   |
  |                      |    Deploy, Rollback, StateMachine, Error)   |
  | Stale diagrams found | 3 (in Bo-01/Arch, Bo-02/Arch, Bridge doc)   |
  | Unresolved decisions | 0                                           |
  | Reality rows         | 7/7 rows (PLAN_REALITY), 0 unverified       |
  +====================================================================+
```

### Unresolved Decisions
None - all 7 decisions (`D1`–`D7` covering `ROW-01`, `ROW-02`, `ROW-03`, `EXP-01`, `EXP-02`, `EXP-03`, and Step `0H` Scope-Document Approval) have been explicitly answered and approved by the user.

---

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | 2 | CLEAR | 3 proposals, 3 accepted, 0 deferred |
| Outside Review | `codex` (auto during `/plan-ceo-review`) | Independent 2nd opinion | 1 | unavailable | MODEL_UNUSABLE (Codex CLI too old for gpt-6-astra); no completed external review |
| Eng Review | `/plan-eng-review` | Architecture & tests (required) | 0 | - | - |
| Design Review | `/plan-design-review` | UI/UX gaps | 0 | - | - |
| DX Review | `/plan-devex-review` | Developer experience gaps | 0 | - | - |

- **OUTSIDE COVERAGE:** `provider=codex, host=claude, phase=plan-review, status=unavailable` (`MODEL_UNUSABLE`: Codex CLI too old for `gpt-6-astra`; Plan agent type and TaskStop not offered in host - no completed external review).
- **VERDICT:** CEO CLEARED - eng review required

NO UNRESOLVED DECISIONS
