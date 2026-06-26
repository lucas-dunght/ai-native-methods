# Quick Start · Bộ 03 trong 20 phút

Hướng dẫn này giúp sinh viên chạy vibecode lần đầu trên một task nhỏ trong 20 phút.

## Bài toán mẫu

Sinh viên muốn xây một CLI tool nhỏ để đếm số dòng code Python trong một thư mục dự án. Đây là task R0 hoặc R1, đủ để demo workflow.

## Phút 0 đến 2 · Setup repo

```bash
mkdir vibecode-line-counter
cd vibecode-line-counter
git init
mkdir -p vibecode-artifacts/{TIP,RRI-logs,blueprints,completion-reports,calibration-cards}
mkdir -p src tests docs

echo "timestamp,step,role,action,reference,notes" > vibecode-artifacts/audit-trail.csv
```

## Phút 2 đến 5 · Viết TIP

Tạo `vibecode-artifacts/TIP/TIP-001.md`.

```markdown
# TIP-001 · Line counter CLI tool

**Date.** 2026-06-26
**Risk tier.** R1 (impact low, partial reversible)
**Deadline.** Trong session 20 phút này

## 1. Intent
Xây CLI tool đếm số dòng code Python trong một thư mục.
Chạy bằng lệnh `python lc.py <directory>`. Output số dòng tổng.

## 2. Why
Để biết quy mô của một dự án Python nhanh chóng.

## 3. Success criteria
- Chạy được không lỗi trên thư mục có file .py
- Output đúng số dòng (loại trừ dòng trống và comment)
- Có message rõ ràng khi thư mục không có file .py
- Hoàn thành trong 20 phút

## 4. Out of scope
- Đếm dòng code các ngôn ngữ khác
- GUI
- Output JSON hoặc CSV
- Stats về functions hoặc classes

## 5. Risk tier reasoning
R1 vì impact thấp (chỉ là tool cá nhân, sai không gây hậu quả lớn)
nhưng partial reversible (nếu output sai có thể cause confusion).
```

Update audit trail.

```bash
echo "2026-06-26T10:02:00,1,Chủ thầu,TIP_created,TIP-001,Khởi tạo line counter" >> vibecode-artifacts/audit-trail.csv
```

## Phút 5 đến 7 · Skip RRI cho R1

Theo bảng tier, R1 không bắt buộc RRI. Skip bước này.

Nếu TIP có ambiguity (ví dụ "dòng code có tính dòng comment hay không"), nên ad-hoc RRI ngắn. Trong case này, TIP đã rõ về out of scope.

## Phút 7 đến 10 · Blueprint đơn giản

Tạo `vibecode-artifacts/blueprints/BP-001.md`.

```markdown
# BP-001 · Line counter CLI

**Date.** 2026-06-26
**Linked TIP.** TIP-001

## 1. Architecture
Single Python script `lc.py`. Một function chính.

```
lc.py
├── parse_args()        Parse directory từ command line
├── count_lines(file)   Đếm dòng trong một file (skip empty và comment)
├── walk_directory(dir) Duyệt thư mục, gọi count_lines cho mỗi .py
└── main()              Orchestrate
```

## 2. Tech stack
- Language. Python 3.10+
- Library. argparse (built-in), pathlib (built-in)
- Không cần external dependency

## 3. Data model
Không có persistence. Tất cả trong memory.

## 4. External integrations
Không có.

## 5. Risk areas
- File encoding (UTF-8 vs other)
- Symbolic link gây infinite loop
- File quá lớn

## 6. Approval
**Approved by.** [Sinh viên ký]
**Date.** 2026-06-26
```

Update audit trail.

```bash
echo "2026-06-26T10:10:00,3,Thợ thi công,Blueprint_created,BP-001," >> vibecode-artifacts/audit-trail.csv
echo "2026-06-26T10:10:30,3,Chủ thầu,Blueprint_approved,BP-001," >> vibecode-artifacts/audit-trail.csv
```

## Phút 10 đến 15 · Build với AI

Mở Claude (qua web hoặc Cursor) và paste vào.

```
Tôi đang vibecode một CLI tool theo Blueprint sau.

[Paste BP-001.md content]

Hãy implement file lc.py theo Blueprint. Code phải:
- Chạy được không cần install thêm package
- Handle các risk areas đã nêu trong Blueprint (encoding, symlink, large file)
- Có docstring rõ
- Có error handling cơ bản

Trả về code đầy đủ trong một code block.
```

Claude trả về code. Copy vào `src/lc.py`.

Test nhanh.

```bash
python src/lc.py src/
```

Output ví dụ `42 lines of Python code in 1 file`.

Update audit trail.

```bash
echo "2026-06-26T10:15:00,4,Thợ thi công,Build_completed,BP-001,Test passed" >> vibecode-artifacts/audit-trail.csv
```

## Phút 15 đến 17 · Completion Report

Tạo `vibecode-artifacts/completion-reports/CR-001.md`.

```markdown
# CR-001 · Line counter CLI

**Date.** 2026-06-26
**Linked TIP.** TIP-001
**Linked Blueprint.** BP-001

## 1. Intent achieved
CLI tool `lc.py` chạy được, đếm dòng .py trong thư mục.

## 2. Deviations from Blueprint
- Không có deviation đáng kể

## 3. Known issues
- Chưa test với encoding khác UTF-8
- Symbolic link handling chưa test exhaustive

## 4. Pending work
- Test với edge cases nếu cần dùng nghiêm túc

## 5. Test results
Tested với src/ folder: 42 lines, output đúng.

## 6. Confidence level
- Overall. Medium (chưa test edge cases)
```

## Phút 17 đến 18 · Deploy

Đối với R1 task này, "deploy" nghĩa là commit và push.

```bash
git add .
git commit -m "Add line counter CLI tool"
```

Update audit trail.

```bash
echo "2026-06-26T10:18:00,7,Chủ nhà,Deployed,CR-001,Commit local repo" >> vibecode-artifacts/audit-trail.csv
```

## Phút 18 đến 20 · Calibration Card

Tạo `vibecode-artifacts/calibration-cards/CC-001.md`.

```markdown
# CC-001 · Line counter CLI

**Date deployed.** 2026-06-26
**Date calibrated.** 2026-06-26 (immediate)
**Linked TIP.** TIP-001

## 1. Prediction
- Chạy được không lỗi: Yes expected
- Output đúng số dòng: Yes expected
- Message khi không có .py file: Yes expected
- Hoàn thành 20 phút: Yes expected

## 2. Actual
- Chạy được không lỗi: Yes
- Output đúng số dòng: Yes (verified manually)
- Message khi không có .py: Yes
- Hoàn thành 20 phút: Yes (vừa kịp)

## 3. Delta
Không có sai số đáng kể.

## 4. Error allocation (100 điểm)
- Modeling. 0
- Timing. 0
- World-change. 0
- Execution. 0

Không có error allocation cần làm trong cycle này.

## 5. Lesson learned
- Workflow 8 bước có thể chạy trong 20 phút cho R1 task.
- Blueprint giúp catch các risk areas trước khi build.
- Để tăng confidence, cần test edge cases (encoding, symlink) trong cycle sau.

## 6. Action items
- [ ] Test với UTF-16 file trong cycle sau
- [ ] Test với symlink loop trong cycle sau
```

## Đã xong cycle 1

Sinh viên hoàn thành cycle vibecode đầu tiên trong 20 phút.

Đã có.
- TIP đầy đủ
- Blueprint đơn giản
- Code chạy được
- Completion Report
- Calibration Card
- Audit trail 5 entries

Workflow chưa hoàn hảo nhưng đã chạy qua đủ các bước cốt lõi.

## Bước tiếp theo

Cycle 2 thử một task R2 (impact medium) để trải nghiệm RRI và Blueprint nghiêm túc hơn. Ví dụ "xây web form upload file".

Cycle 3 thử R3 (impact high) để trải nghiệm full workflow. Ví dụ "xây feature payment integration".

Đọc Methodology.md để hiểu ba vai trò và lý do từng bước. Đọc Architecture.md để setup project structure production-ready.
