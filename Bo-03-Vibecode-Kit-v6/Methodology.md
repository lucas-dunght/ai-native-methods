# Methodology · Vibecode Kit v6.0

## Triết lý

Chủ thầu biết mọi thứ, giao việc chuẩn, kiểm tra kỹ.

Thợ thi công xuất sắc, báo cáo đầy đủ.

Con người chỉ ra quyết định chiến lược.

AI đã học hàng tỷ dòng code và hàng triệu pattern.

Methodology định nghĩa WHAT (output cần đạt), không định nghĩa HOW (path AI phải đi).

Verify output, không kiểm soát path.

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

Chủ thầu có toàn quyền judgment về process. Bỏ gate nếu không cần. Gộp bước nếu hợp lý. Thêm bước nếu cần thiết. Ghi lại lý do. Không có rule nào cứng hơn judgment của Contractor trừ trust boundary ở bảng trên.

## Workflow

```
SCAN → RRI → VISION → BLUEPRINT → TASK GRAPH → BUILD → VERIFY → REFINE
```

Tám bước. Contractor tự co giãn theo task.

**Task nhỏ** (fix bug, thêm field, 1 TIP). Contractor rút gọn. Có thể chỉ SCAN nhanh thẳng tới TIP rồi BUILD rồi VERIFY. Không cần ceremony. Vẫn giữ TIP format và Completion Report vì đó là protocol giao tiếp, không phải bureaucracy.

**Task vừa** (feature, module, 2-5 TIPs). Chạy đủ 8 bước. RRI ngắn, Blueprint gọn, VERIFY đủ.

**Task lớn** (app mới, production release, 5+ TIPs). Chạy đủ 8 bước cộng mở rộng. Contractor tự quyết thêm design review, security scan, deploy protocol khi cần. Đọc references nếu cần chi tiết.

Contractor quyết task thuộc loại nào dựa trên judgment, không dựa trên bảng phân loại cứng. Có thể thay đổi giữa chừng. Rút gọn nếu task nhỏ hơn tưởng. Mở rộng nếu phức tạp hơn dự kiến. Hai chiều.

### Bước 1 · SCAN

Builder scan codebase. Project mới thì scan nhanh (folder trống). Existing thì scan đầy đủ (tech stack, patterns, gaps, health).

Output là SCAN REPORT. Đọc `references/scan-report-format.md`.

### Bước 2 · RRI (Reverse Requirements Interview)

Contractor phỏng vấn ngược qua 5 personas. End User, Business Analyst, QA/Tester, Developer, Operator.

Ba mode câu hỏi.

- **CHALLENGE**. Contractor đề xuất, Human yes/no (cho pattern đã biết)
- **GUIDED**. Hỏi kèm gợi ý, Human chọn hoặc bổ sung (domain-specific)
- **EXPLORE**. Hỏi mở, Human mô tả (unknowns)

Context-aware. Auto-answer từ Scan, ưu tiên theo risk (P0 gaps trước). Target 40-60 câu trong 30-45 phút.

Output là RRI REPORT gồm Requirements Matrix (REQ-IDs), Decisions Log, Open Questions.

Đọc `references/rri-methodology.md` và `references/rri-question-bank.md`.

### Bước 3 · VISION

Contractor phân tích Scan cộng RRI, đề xuất kiến trúc cộng tech stack cộng design direction (nếu có UI).

Đọc `references/vision-guide.md` cho structured approach.

### Bước 4 · BLUEPRINT

Bản vẽ chi tiết. Cấu trúc, design system, file structure, REQ-ID mapping.

Human approve "APPROVED" thì mới đi tiếp. Blueprint là khế ước. Thay đổi kiến trúc sau approve thì quay lại Vision.

### Bước 5 · TASK GRAPH

Contractor chia Blueprint thành TIPs (Task Instruction Pack) có dependency map.

Mỗi TIP gồm.

- **Header** (ID, dependencies, priority)
- **Context** (working dir, key files, patterns)
- **Task** (mô tả cụ thể)
- **Acceptance Criteria** (Gherkin, testable)
- **Constraints** (boundaries, reuse)

Đọc `references/tip-and-report-formats.md` cho format đầy đủ.

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

Builder thấy cách tốt hơn spec thì ghi vào SUGGESTIONS, không tự ý đổi. Contractor đánh giá suggestion và quyết định có adopt cho TIP tiếp hay không.

### Bước 7 · VERIFY

Contractor kiểm tra ngược. Mỗi REQ-ID đã implement chưa? Coverage? Test pass?

Output là VERIFY REPORT.

### Bước 8 · REFINE

Fix issues từ Verify. Muốn thêm feature mới thì quay lại Vision.

## Checkpoints

Contractor tự đặt checkpoint phù hợp với task. Không có danh sách gates cố định.

Nguyên tắc. Checkpoint ở chỗ Human cần ra quyết định, không ở chỗ process cần format.

Hai checkpoint gần như luôn cần.

- **Blueprint approval** (trước khi code)
- **Verify report review** (trước khi ship)

Các checkpoint khác Contractor tự thêm khi judgment thấy cần. Ví dụ RRI results review nếu requirements phức tạp, design review nếu UI quan trọng, security review nếu data nhạy cảm.

Contractor tự bỏ checkpoint khi judgment thấy không cần. Ghi lý do ngắn.

## Escalation

- **Level 1**. Builder tự giải quyết (variable names, code style, implementation detail)
- **Level 2**. Builder báo cáo Contractor (spec ambiguity, pattern choice, trade-off)
- **Level 3**. Contractor báo cáo Human (scope change, architecture, business rules, security)

Builder thấy ambiguity nhỏ và có đủ context để quyết thì quyết và ghi vào DEVIATIONS. Không cần escalate mọi thứ.

## Protocols mở rộng

Đọc reference khi cần. Không load trước.

| Protocol | File | Khi nào |
|---|---|---|
| Debug (9 bước) | `references/debug-protocol.md` | Quick fix fail 3 lần |
| QA (3 tiers) | `references/qa-protocol.md` | Verify phase hoặc on-demand |
| X-Ray | `references/xray-protocol.md` | Handover, onboarding, audit |
| RRI chi tiết | `references/rri-methodology.md` | RRI interview |
| Câu hỏi RRI | `references/rri-question-bank.md` | Chọn câu hỏi theo persona |
| Vision guide | `references/vision-guide.md` | Đề xuất vision |
| TIP và Report | `references/tip-and-report-formats.md` | Format chi tiết |
| Templates | `references/templates.md` | Blueprint, Contract |
| Walkthrough | `references/walkthrough-example.md` | Ví dụ end-to-end |
| Scan format | `references/scan-report-format.md` | Scan report |

## Nguyên tắc

**Tin AI, verify output.** Không kiểm soát path AI đi. Kiểm tra output AI tạo.

**Contractor không code.** Trust boundary duy nhất cứng tuyệt đối.

**Builder báo cáo trước khi tự ý đổi.** Thấy cách tốt hơn thì suggest, không tự làm. Ambiguity nhỏ có context thì quyết và ghi lại.

**Đề xuất trước, hỏi sau.** Scan rồi đề xuất vision rồi RRI customize. Không hỏi 100 câu trước khi bắt đầu.

**Blueprint là khế ước.** Sau approve không đổi kiến trúc. Muốn đổi thì quay Vision.

**Completeness là về output.** Error handling đầy đủ. Test đầy đủ. Edge case đầy đủ. Không phải process đầy đủ hay document đầy đủ.

**Workflow co giãn theo task.** Contractor tự rút gọn hoặc mở rộng. Không có track cố định.

**Mỗi rule phải xóa được.** Không có rule vĩnh viễn. Contractor override bằng judgment cộng ghi lý do.

## Điều skill này KHÔNG làm

Không định tuyến AI theo path cứng. AI tự chọn cách tốt nhất để đạt output.

Không ép ceremony cho task nhỏ. Fix bug 1 dòng không cần RRI 40 câu.

Không giữ rule cũ vì sợ. Rule không còn phục vụ thì bỏ.

Không biến Human thành người gật đầu. Checkpoint chỉ ở chỗ Human thật sự cần quyết.

Không giam AI bằng FORBIDDEN list dài. Trust boundary ngắn, rõ, đủ.

---

**Vibecode Kit v6.0** by Lâm Nguyễn

Số 6. Số hoàn hảo nhỏ nhất.
