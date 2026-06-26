# Architecture · Kiến trúc Vibecode Kit v6

## Tổng quan

Vibecode Kit v6 là một workflow chứ không phải một stack technical cụ thể. Có thể implement trên nhiều platform khác nhau. Phần này mô tả kiến trúc khái niệm, các artifact bắt buộc và một stack đề xuất cho sinh viên.

Các thành phần kiến trúc.

```
Vibecode Workflow
│
├── Project Folder (Git repo)
│   │
│   ├── vibecode-artifacts/         Thư mục lưu artifacts của 8 bước
│   │   ├── TIP/                    Task Intent Prompts
│   │   ├── RRI-logs/               RRI conversation logs
│   │   ├── blueprints/             Architecture blueprints
│   │   ├── completion-reports/     Completion Reports
│   │   ├── calibration-cards/      Calibration Cards sau deploy
│   │   └── audit-trail.csv         Audit Trail Loop
│   │
│   ├── src/                        Source code thực tế (do AI viết)
│   ├── tests/                      Tests (do AI viết hoặc human)
│   ├── docs/                       Documentation
│   └── README.md
│
└── AI Agent Configuration
    ├── claude-config              (hoặc cursor-config, etc.)
    ├── agent-instructions.md      Instructions cho AI agent
    └── skill-pointers/            Pointers tới các skill cần thiết
```

## Workflow chi tiết

### Khởi tạo dự án

1. Tạo Git repo cho dự án.
2. Tạo folder structure trên.
3. Khởi tạo audit-trail.csv với header.
4. Setup AI agent với agent-instructions.md trỏ tới vibecode-artifacts.

### Một cycle vibecode

```
START
  │
  ▼
Chủ thầu viết TIP (Bước 1)
  │
  ▼
Lưu TIP vào vibecode-artifacts/TIP/TIP-NNN.md
  │
  ▼
Log vào audit-trail.csv (action: TIP_created)
  │
  ▼
Risk tier R2 hoặc R3?
  │
  ├── Yes ──► AI agent thực hiện RRI (Bước 2)
  │             │
  │             ▼
  │           Lưu RRI log vào vibecode-artifacts/RRI-logs/
  │             │
  │             ▼
  │           Chủ thầu trả lời. Update TIP nếu cần.
  │
  ├── No ───► Skip RRI
  │
  ▼
AI agent sinh Blueprint (Bước 3, skip ở R0)
  │
  ▼
Chủ thầu approve hoặc revise blueprint
  │
  ▼
AI agent build code (Bước 4)
  │
  ▼
Chủ thầu review nếu R2 R3, skip nếu R0 R1
  │
  ▼
AI agent viết Completion Report (Bước 5, skip ở R0)
  │
  ▼
Chủ nhà re-assess risk tier (Bước 6)
  │
  ▼
Chủ nhà deploy hoặc veto (Bước 7)
  │
  ├── Deploy ──► Wait for evidence
  │                │
  │                ▼
  │              Chủ thầu viết Calibration Card (Bước 8)
  │                │
  │                ▼
  │              END
  │
  └── Veto ────► Quay về Bước 1 với context updated
```

## Artifact formats

### TIP (vibecode-artifacts/TIP/TIP-NNN.md)

```markdown
# TIP-001 · [Tên task ngắn]

**Date.** YYYY-MM-DD
**Risk tier.** R[0|1|2|3]
**Deadline.** YYYY-MM-DD

## 1. Intent
[1 đến 3 câu mô tả cái cần tạo]

## 2. Why
[Context nghiệp vụ hoặc cá nhân]

## 3. Success criteria
- [Criterion 1, đo được]
- [Criterion 2, đo được]
- [Criterion 3, đo được]

## 4. Out of scope
- [Cái không nằm trong task này]

## 5. Risk tier reasoning
[Tại sao tier này, theo bảng map Impact × Reversibility]
```

### Blueprint (vibecode-artifacts/blueprints/BP-NNN.md)

```markdown
# BP-001 · [Tên task]

**Date.** YYYY-MM-DD
**Linked TIP.** TIP-001

## 1. Architecture diagram
[ASCII art hoặc link đến file diagram]

## 2. Tech stack
- Language. [...]
- Framework. [...]
- Database. [...]
- Hosting. [...]

## 3. Modules
### Module A
- Responsibility.
- Interface.
- Dependencies.

### Module B
- ...

## 4. Data model
[Schema bảng hoặc structure dữ liệu]

## 5. External integrations
- [API X]
- [Service Y]

## 6. Risk areas
[Chỗ có khả năng sai cao]

## 7. Approval
**Approved by.** [Tên Chủ thầu]
**Date.** YYYY-MM-DD
```

### Completion Report (vibecode-artifacts/completion-reports/CR-NNN.md)

```markdown
# CR-001 · [Tên task]

**Date.** YYYY-MM-DD
**Linked TIP.** TIP-001
**Linked Blueprint.** BP-001

## 1. Intent achieved
[Tóm tắt đã làm gì]

## 2. Deviations from Blueprint
- [Deviation 1, lý do]
- [Deviation 2, lý do]

## 3. Known issues
- [Bug 1]
- [Limitation 1]

## 4. Pending work
- [Cái chưa làm, lý do]

## 5. Test results
[Output test]

## 6. Confidence level
- Module A. [High|Medium|Low]
- Module B. [High|Medium|Low]
- Overall. [High|Medium|Low]
```

### Calibration Card (vibecode-artifacts/calibration-cards/CC-NNN.md)

```markdown
# CC-001 · [Tên task]

**Date deployed.** YYYY-MM-DD
**Date calibrated.** YYYY-MM-DD (sau khi có evidence)
**Linked TIP.** TIP-001

## 1. Prediction
[Lấy từ success criteria của TIP]

## 2. Actual
[Đã quan sát được gì sau deploy]

## 3. Delta
[Khoảng cách giữa prediction và actual]

## 4. Error allocation (100 điểm)
- Modeling. NN điểm
- Timing. NN điểm
- World-change. NN điểm
- Execution. NN điểm

## 5. Lesson learned
[Điều rút ra cho cycle sau]

## 6. Action items
- [Action 1 cho cycle sau]
- [Action 2 cho cycle sau]
```

### Audit Trail (vibecode-artifacts/audit-trail.csv)

```csv
timestamp,step,role,action,reference,notes
2026-06-26T10:00:00,1,Chủ thầu,TIP_created,TIP-001,"Khởi tạo task A"
2026-06-26T10:15:00,2,Thợ thi công,RRI_question,TIP-001,"AI hỏi về data source"
2026-06-26T10:25:00,2,Chủ thầu,RRI_answer,TIP-001,"Trả lời RRI"
2026-06-26T10:30:00,3,Thợ thi công,Blueprint_created,BP-001,"AI sinh blueprint"
2026-06-26T11:00:00,3,Chủ thầu,Blueprint_approved,BP-001,
2026-06-26T11:05:00,4,Thợ thi công,Build_started,BP-001,
2026-06-26T14:00:00,4,Thợ thi công,Build_completed,BP-001,"Commit hash abc123"
2026-06-26T14:15:00,5,Thợ thi công,CR_created,CR-001,
2026-06-26T14:30:00,7,Chủ nhà,Deployed,CR-001,"Deploy to staging"
2026-06-27T09:00:00,8,Chủ thầu,CC_created,CC-001,"Sau 1 ngày observe"
```

## AI Agent Configuration

### Agent Instructions (agent-instructions.md)

File này được nạp vào AI agent ở đầu mỗi conversation.

```markdown
# Vibecode Agent Instructions

Bạn là Thợ thi công trong dự án vibecode này.

## Workflow

Bạn đi qua các bước theo thứ tự. Khi user (Chủ thầu) đưa cho bạn một TIP, bạn.

1. Đọc TIP kỹ.
2. Nếu task ở R2 hoặc R3, thực hiện RRI. Hỏi 3 đến 10 câu cụ thể.
3. Sau khi RRI, sinh Blueprint.
4. Chờ Chủ thầu approve Blueprint.
5. Build code theo Blueprint.
6. Viết Completion Report khi xong.

## Constraints

Bạn KHÔNG.
- Tự skip bước nào.
- Tự deploy code (chỉ Chủ nhà có quyền).
- Quyết định trade-off architecture quan trọng mà không hỏi Chủ thầu.
- Implement thứ không có trong TIP.

Bạn LUÔN.
- Log mọi quyết định vào audit trail.
- Cập nhật Completion Report khi có discovery mới.
- Hỏi khi không chắc.

## Skill pointers

Bạn có thể access các skills sau khi cần.
- skill-pointers/code-review.md
- skill-pointers/security-check.md
- skill-pointers/testing-strategy.md
```

### Skill Pointers

Mỗi skill pointer là một file ngắn trỏ tới phương pháp chi tiết hơn.

```markdown
# skill-pointers/code-review.md

Khi cần review code, follow các bước.
1. Đọc Blueprint để hiểu intent.
2. So code với Blueprint, tìm deviation.
3. Check security: SQL injection, XSS, secrets exposure.
4. Check performance: N+1 queries, unbounded loops.
5. Report deviation và issues trong Completion Report.

Reference: methodology/code-review.md
```

## Tools stack đề xuất

Đối với sinh viên không có ngân sách lớn.

**AI Agent.** Claude (qua Cursor IDE hoặc Claude Code CLI). Hoặc GPT-4 qua API. Free tier của các tool này đủ cho student project.

**Version control.** Git với GitHub Education (free pro).

**IDE.** VS Code với extensions cho language target.

**Hosting.** Vercel hoặc Netlify cho web app (free tier). Railway hoặc Fly.io cho backend.

**Database.** SQLite cho dự án nhỏ. PostgreSQL trên Supabase free tier khi cần.

**Monitoring.** Sentry free tier cho error tracking.

Đối với dự án production-grade hoặc startup.

**AI Agent.** Claude API hoặc OpenAI API với paid tier.

**CI/CD.** GitHub Actions.

**Infrastructure.** AWS, GCP, hoặc Cloudflare.

**Observability.** Datadog hoặc New Relic.

## Workflow tự co giãn theo tier

### R0 example (5 phút)

User muốn thêm một button vào trang web có sẵn.

```
1. TIP một dòng. "Thêm button Reset ở góc trên phải, click để reset form."
2. Skip RRI, skip Blueprint.
3. Build (AI viết code, 2 phút).
4. Skip Completion Report formal.
5. Deploy (commit và push, 1 phút).
6. Calibration ngắn. "Button work, không break gì khác. Lesson: nhớ test với form đã có data."
```

Tổng 5 phút. Không có Blueprint hoặc Completion Report formal. Vẫn có TIP và Calibration.

### R2 example (2 ngày)

User muốn thêm authentication system vào web app.

```
1. TIP đầy đủ. Intent, why, success criteria, out of scope, risk tier R2 (impact medium, partial reversible).
2. RRI 5 câu. AI hỏi về choice giữa email-password vs OAuth, session management strategy, password requirements.
3. Chủ thầu trả lời. Update TIP.
4. AI sinh Blueprint 1 trang. Tech stack, modules, data model, security considerations.
5. Chủ thầu approve Blueprint.
6. AI build. Chia 4 subtask: signup form, login form, session middleware, password reset.
7. Chủ thầu review từng subtask.
8. AI viết Completion Report. List 2 deviations và 1 known issue.
9. Chủ nhà re-assess. Pass.
10. Deploy to staging.
11. Test 1 ngày.
12. Deploy production.
13. Sau 3 ngày, Chủ thầu viết Calibration Card.
```

Tổng 2 ngày với 8 bước đầy đủ.

## Tích hợp với Bộ 01 và Bộ 02

Khi AI agent cần context cụ thể về domain (số liệu, văn bản pháp quy, voice), agent reference vào kernel registry (Bộ 02) qua ID.

Khi AI agent cần research thêm thông tin từ internet trước khi build (ví dụ "có ai đã làm tương tự chưa"), agent có thể trigger workflow của Bộ 01 để thu thông tin có cấu trúc.

Ba bộ tích hợp tốt khi sinh viên làm full dự án. Bộ 01 cho research phase. Bộ 02 cho knowledge phase. Bộ 03 cho build phase.
