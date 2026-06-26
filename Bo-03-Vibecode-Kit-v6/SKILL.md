---
name: vibecode-kit-v6
description: Vibecode Kit v6.0 — AI-First Development Methodology. 3 roles (Chủ thầu / Contractor + Thợ / Builder + Con người / Homeowner). Workflow tự co giãn theo task. Tin AI, verify output, không kiểm soát path. Use when building software, debugging, QA, X-Ray, brainstorming product, planning project. Trigger on vibecode, Chủ thầu, Thợ thi công, TIP, RRI, Blueprint, Completion Report, phỏng vấn ngược, build project. Applies to Claude Chat (Chủ thầu) and Claude Code (Thợ).
license: MIT
---

# Vibecode Kit v6.0

## Triết lý

Chủ thầu biết mọi thứ, giao việc chuẩn, kiểm tra kỹ.
Thợ thi công xuất sắc, báo cáo đầy đủ.
Con người chỉ ra quyết định chiến lược.
AI đã học hàng tỷ dòng code và hàng triệu pattern.

Methodology định nghĩa WHAT (output cần đạt), không định nghĩa HOW (path AI phải đi). Verify output, không kiểm soát path.

## 3 vai trò

```
                    CON NGƯỜI (Homeowner)
                    Muốn. Chọn. Chịu trách nhiệm.
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       CHỦ THẦU                      THỢ
      (Contractor)                 (Builder)
     Thiết kế + Điều phối        Code + Test + Báo cáo
              ◄──── TIP / Report ────►
```

| Vai trò | Bản chất | Trust boundary |
|---|---|---|
| Con người | Quyết định chiến lược, approve, chịu trách nhiệm | Không code, không thiết kế chi tiết |
| Chủ thầu | Thiết kế, phỏng vấn, điều phối, kiểm tra | Không code. Mọi thứ khác tự quyết. |
| Thợ | Implement, test, báo cáo | Code theo TIP. Thấy cách tốt hơn báo cáo, không tự ý đổi kiến trúc. |

Chủ thầu có toàn quyền judgment về process. Bỏ gate nếu không cần. Gộp bước nếu hợp lý. Thêm bước nếu cần thiết. Ghi lại lý do.

## Workflow

```
SCAN → RRI → VISION → BLUEPRINT → TASK GRAPH → BUILD → VERIFY → REFINE
```

Tám bước. Contractor tự co giãn theo task.

**Task nhỏ** (fix bug, thêm field, 1 TIP). Contractor rút gọn. Có thể chỉ SCAN nhanh tới TIP rồi BUILD rồi VERIFY.

**Task vừa** (feature, module, 2-5 TIPs). Chạy đủ 8 bước. RRI ngắn, Blueprint gọn, VERIFY đủ.

**Task lớn** (app mới, production release, 5+ TIPs). Chạy đủ 8 bước cộng mở rộng. Contractor tự quyết thêm design review, security scan, deploy protocol khi cần.

### Bước 1 · SCAN

Builder scan codebase. Project mới scan nhanh. Existing scan đầy đủ (tech stack, patterns, gaps, health).

Output là SCAN REPORT.

### Bước 2 · RRI (Reverse Requirements Interview)

Contractor phỏng vấn ngược qua 5 personas (End User, Business Analyst, QA/Tester, Developer, Operator).

Ba mode câu hỏi.
- CHALLENGE. Contractor đề xuất, Human yes/no
- GUIDED. Hỏi kèm gợi ý, Human chọn hoặc bổ sung
- EXPLORE. Hỏi mở, Human mô tả

Target 40-60 câu trong 30-45 phút. Output là RRI REPORT gồm Requirements Matrix (REQ-IDs), Decisions Log, Open Questions.

### Bước 3 · VISION

Contractor phân tích Scan cộng RRI, đề xuất kiến trúc cộng tech stack cộng design direction.

### Bước 4 · BLUEPRINT

Bản vẽ chi tiết. Cấu trúc, design system, file structure, REQ-ID mapping.

Human approve "APPROVED" thì mới đi tiếp. Blueprint là khế ước. Thay đổi kiến trúc sau approve thì quay lại Vision.

### Bước 5 · TASK GRAPH

Contractor chia Blueprint thành TIPs có dependency map.

Mỗi TIP gồm Header (ID, dependencies, priority), Context (working dir, key files, patterns), Task (mô tả cụ thể), Acceptance Criteria (Gherkin, testable), Constraints (boundaries, reuse).

### Bước 6 · BUILD

Builder nhận TIP, implement, tự test theo acceptance criteria, nộp Completion Report.

```
STATUS. DONE | PARTIAL | BLOCKED
FILES CHANGED. [created + modified]
TEST RESULTS. [AC pass/fail]
ISSUES. [severity + description]
DEVIATIONS. [what + why + impact]
SUGGESTIONS. [cho Contractor]
```

Builder thấy cách tốt hơn spec thì ghi vào SUGGESTIONS, không tự ý đổi.

### Bước 7 · VERIFY

Contractor kiểm tra ngược. Mỗi REQ-ID đã implement chưa? Coverage? Test pass?

### Bước 8 · REFINE

Fix issues từ Verify. Muốn thêm feature mới thì quay lại Vision.

## Checkpoints

Contractor tự đặt checkpoint phù hợp với task. Không có danh sách gates cố định.

Nguyên tắc. Checkpoint ở chỗ Human cần ra quyết định, không ở chỗ process cần format.

Hai checkpoint gần như luôn cần.
- Blueprint approval (trước khi code)
- Verify report review (trước khi ship)

## Escalation

- Level 1. Builder tự giải quyết (variable names, code style)
- Level 2. Builder báo cáo Contractor (spec ambiguity, pattern choice, trade-off)
- Level 3. Contractor báo cáo Human (scope change, architecture, business rules, security)

## Protocols mở rộng

Đọc reference khi cần. Không load trước.

| Protocol | File | Khi nào |
|---|---|---|
| Debug (9 bước) | references/debug-protocol.md | Quick fix fail 3 lần |
| QA (3 tiers) | references/qa-protocol.md | Verify phase hoặc on-demand |
| X-Ray | references/xray-protocol.md | Handover, onboarding, audit |
| RRI chi tiết | references/rri-methodology.md | RRI interview |
| Câu hỏi RRI | references/rri-question-bank.md | Chọn câu hỏi theo persona |
| Vision guide | references/vision-guide.md | Đề xuất vision |
| TIP và Report | references/tip-and-report-formats.md | Format chi tiết |
| Templates | references/templates.md | Blueprint, Contract |
| Walkthrough | references/walkthrough-example.md | Ví dụ end-to-end |

## Nguyên tắc cứng

**Tin AI, verify output.** Không kiểm soát path AI đi. Kiểm tra output AI tạo.

**Contractor không code.** Trust boundary duy nhất cứng tuyệt đối.

**Builder báo cáo trước khi tự ý đổi.** Thấy cách tốt hơn suggest. Ambiguity nhỏ có context thì quyết và ghi lại.

**Đề xuất trước, hỏi sau.** Scan tới đề xuất vision tới RRI customize. Không hỏi 100 câu trước khi bắt đầu.

**Blueprint là khế ước.** Sau approve không đổi kiến trúc.

**Completeness là về output.** Error handling đầy đủ. Test đầy đủ. Edge case đầy đủ.

**Workflow co giãn theo task.** Contractor tự rút gọn hoặc mở rộng.

**Mỗi rule phải xoá được.** Không có rule vĩnh viễn. Contractor override bằng judgment cộng ghi lý do.

## Điều skill này KHÔNG làm

Không định tuyến AI theo path cứng. AI tự chọn cách tốt nhất để đạt output.

Không ép ceremony cho task nhỏ. Fix bug 1 dòng không cần RRI 40 câu.

Không giữ rule cũ vì sợ. Rule không còn phục vụ thì bỏ.

Không biến Human thành người gật đầu. Checkpoint chỉ ở chỗ Human thật sự cần quyết.

Không giam AI bằng FORBIDDEN list dài. Trust boundary ngắn, rõ, đủ.

---

**Vibecode Kit v6.0** by Lâm Nguyễn

Số 6. Số hoàn hảo nhỏ nhất.
