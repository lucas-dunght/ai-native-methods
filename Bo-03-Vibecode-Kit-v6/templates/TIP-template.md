# Gói Giao Việc Cho Thợ (`Task Implementation Package · TIP · v6.2 × pstack`)

- **Mã Gói việc (`TIP ID`):** `[TIP-01]`
- **Đơn vị Kiểm chứng Tuần tự (`Sequence-Verifiable-Unit`):** `[Unit 1 / PR độc lập #1]`
- **Thuộc Bản vẽ (`Blueprint Ref`):** `[EPIC-YYYY-MM]`
- **Nhánh Làm việc (`Worktree / Cloud Agent Branch`):** `[feat/tip-01-...]`
- **Thư mục Cô lập (`Worktree Path / Cloud VM ID`):** `[.worktrees/tip-01-... hoặc cloud-vm-snap-01]`
- **Mã Commit Cơ sở (`Base Commit`):** `[a1b2c3d]`

---

## 1. Mục Tiêu Ngắn Gọn & Bối Cảnh (`/how + /why Summary`)

- `[Mô tả trong 2 đến 3 câu mục tiêu duy nhất của đơn vị kiểm chứng độc lập này và lý do lịch sử cần lưu ý từ bước /why]`.

---

## 2. Khung Chữ Ký Kiểu Cần Hiện Thực Hóa (`Approved Type Signatures Sketch`)

> Thợ điền thân hàm thật vào đúng khung chữ ký đã được duyệt tại Pha 3 của `/architect Arena`:

```typescript
// Dán khung Type Signatures & Caller Usage Sketch của gói việc này tại đây
export declare function targetFunction(input: TargetInput): Promise<TargetOutput>;
```

---

## 3. Ranh Giới Tệp Tin Độc Quyền (`Disjoint File Ownership`)

- **Danh sách tệp ĐƯỢC PHÉP tạo mới hoặc chỉnh sửa (`owned_files`):**
  - `[src/path/to/fileA.ts]`
  - `[tests/path/to/fileA.test.ts]`
- **Danh sách tệp CHỈ ĐỌC để tham khảo (`read_only_context`):**
  - `[references/features/README.md]`
  - `[src/types/shared.ts]`
- **Ràng buộc Cứng (`Freeze Rule`):** Tuyệt đối không chỉnh sửa bất kỳ tệp nào nằm ngoài danh sách `owned_files`.

---

## 4. Luật Đập Đi Làm Lại Khi Kiến Trúc Sai (`Scrap When Wrong Gate`)

> Trong quá trình viết code thật, nếu gặp bất kỳ dấu hiệu nào dưới đây thì **BẮT BUỘC DỪNG CODE NGAY** và gửi báo cáo `SCRAP_TRIGGERED` về Chủ thầu (không được cố đấm ăn xôi):
- [ ] Phải truyền thêm tham số vá víu (`pass-through parameter hacks`) xuyên qua `>= 3` tầng hàm không liên quan;
- [ ] Phải lặp lại cùng một đoạn code chữa cháy (`workaround`) ở `>= 2` vị trí;
- [ ] Phải dùng kiểu `any`, `@ts-ignore` hoặc ép kiểu cưỡng bức (`as unknown as T`) để vượt qua trình biên dịch.

---

## 5. Tiêu Chí Chấp Nhận Cơ Học (`Acceptance Criteria · AC`)

- [ ] **`AC-1 (Happy Path):`** `[Khi đầu vào hợp lệ X, hàm/API trả về kết quả Y với mã 200]`.
- [ ] **`AC-2 (Edge Case):`** `[Khi dữ liệu rỗng hoặc trùng lặp IdempotencyKey, hệ thống xử lý an toàn không tạo bản ghi trùng]`.
- [ ] **`AC-3 (Error Rescue):`** `[Khi dịch vụ phụ thuộc lỗi, trả về mã lỗi chuẩn hóa kèm trường next_command và không làm lộ stack trace]`.

---

## 6. Quy Trình Thực Thi Bắt Buộc Của Thợ (`TDD + Live Verification via ./bin/control-app`)

1. **Bước 1 (`Red`):** Viết bài kiểm thử tự động kiểm tra đủ `AC-1`, `AC-2`, `AC-3` và chạy lệnh test để xác nhận bài kiểm thử thất bại đúng lý do.
2. **Bước 2 (`Green`):** Điền thân hàm vào khung `Type Signatures Sketch` trong `owned_files` để toàn bộ bài kiểm thử chuyển sang màu xanh.
3. **Bước 3 (`Refactor & Lint`):** Làm sạch mã nguồn, đảm bảo `0` lỗi kiểu dữ liệu (`typecheck`) và `0` cảnh báo `lint`.
4. **Bước 4 (`Live Verification` · Chỉ pass unit test là chưa đủ, phải chạy code thật):**
   ```bash
   ./bin/control-app seed --dry-run --json
   ./bin/control-app dom --route [target-route] --json
   ./bin/control-app screenshot --route [target-route] --json
   ```
5. **Bước 5 (`Evidence Seal`):** Chụp dấu vân tay `WTREE_FINGERPRINT` và điền đầy đủ vào biểu mẫu [`Completion-Report.md`](../templates/Completion-Report.md).
