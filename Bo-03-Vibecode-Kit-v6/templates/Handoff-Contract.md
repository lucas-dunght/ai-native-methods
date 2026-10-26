# Hợp Đồng Bàn Giao Đã Khử Bí Mật (`Redacted Handoff Contract · v6.2 × pstack`)

- **Phiên Bàn giao (`From Session / Role`):** `[Session A · Chủ thầu / Thợ]`
- **Phiên Tiếp nhận (`To Session / Role`):** `[Session B · Chủ thầu / Thợ / Trọng tài C3]`
- **Thời điểm Bàn giao:** `[YYYY-MM-DDTHH:MM:SSZ]`
- **Trạng thái Khử Bí mật (`Secret Redaction`):** `VERIFIED (0 secrets present)`

---

## 1. Dấu Vân Tay Cây Làm Việc Tại Thời Điểm Bàn Giao (`WTREE_FINGERPRINT`)

```text
WTREE_FINGERPRINT: HEAD=[commit_hash] TREE=[tree_hash] WTREE=[wtree_sig] DIRTY_FILES=[count]
```

---

## 2. Tóm Tắt Ngữ Cảnh Hai Chiều (`/recall` + `/how` + `/why` Summary)

- **Bản diễn đạt lại bài toán (`Indirect Prompting Restate`):** `[Tóm tắt 2 câu bản chất bài toán đã được Chủ nhà duyệt]`.
- **Các quyết định lịch sử & kiến trúc đã khóa (`/why` & `D<N>`):**
  - `D1`: `[Đã chọn Phương án A (10/10) · Không được thay đổi quyết định này]`.
  - `Architecture Sketch`: `[Đang thực thi theo khung chữ ký kiểu tại Blueprint mục 4.1]`.

---

## 3. Tiến Độ Đơn Vị Kiểm Chứng Độc Lập (`Sequence-Verifiable-Units Progress`)

### A. Đã Hoàn Thành & Đã Kiểm Chứng Sống (`Completed & Live Verified` `[OBSERVED]`):
- [x] `TIP-01` (`Unit 1`): Đã hoàn thiện tại `[src/fileA.ts:1-80]`, pass `4/4` tests và pass `./bin/control-app dom --route /api/orders --json`.

### B. Đang Dang Dở hoặc Cần Làm Tiếp (`Next Actionable Steps`):
- [ ] `TIP-02` (`Unit 2`): Cần hoàn thiện `[src/fileB.tsx]` theo đúng tiêu chí `AC-1`, `AC-2` trong `TIP-02.md` và chạy `./bin/control-app screenshot --route /orders/ORD-01 --json`.
- [ ] Sau khi merge: Xóa file kế hoạch tạm và chạy `/maintain-verification-skill` cập nhật `references/features/README.md`.

---

## 4. Cạm Bẫy Cần Tránh & Môi Trường Giả Lập (`Dead Ends & Redacted Environment`)

- **Hướng tiếp cận đã thử nhưng thất bại (`Do Not Repeat`):**
  - `[Không dùng thư viện X vì xung đột với phiên bản Node hiện tại]`.
- **Biến môi trường cần thiết (Đã khử khóa thật):**
  ```env
  API_BASE_URL="https://api.example.com"
  PROVIDER_API_KEY="<REDACTED_SECRET>"
  ```
