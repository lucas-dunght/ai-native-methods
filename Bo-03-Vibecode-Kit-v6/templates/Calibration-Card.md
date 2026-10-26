# Thẻ Hiệu Chuẩn Chất Lượng 100 Điểm (`100-Point Calibration Card · v6.2 × pstack`)

- **Mã Phiên / Dự án:** `[EPIC-YYYY-MM]`
- **Cấp độ Rủi ro (`Risk Tier`):** `[R0 / R1 / R2 / R3]`
- **Dấu Vân Tay Cuối (`Final WTREE_FINGERPRINT`):** `HEAD=[hash] TREE=[hash] WTREE=[sig] DIRTY_FILES=0`

---

## 1. Bảng Chấm Điểm 5 Trụ Cột (`100-Point Rubric`)

| Trụ cột Đánh giá | Điểm Tối đa | Điểm Đạt được | Bằng chứng Cụ thể (`[OBSERVED]`) |
|---|---|---|---|
| **1. Kỷ luật Khẳng định & `Indirect Prompting` (`Claim & Intent`)** | `20` | `[20]` | 100% khẳng định có `file:line`; bản `Indirect Prompting Restate` và bộ tứ `/teach = /how + /why + /recall` bắt trúng bản chất bài toán. |
| **2. Lập Kế hoạch bằng Code (`Working Backwards & /architect`)** | `20` | `[20]` | Đã viết `Caller README (4 ô Diátaxis + /unslop)` trước; chạy `5-Phase /architect Arena` (`Type Signatures Sketch`); tuân thủ luật `Scrap when wrong`. |
| **3. Đòn bẩy Tự Kiểm Chứng (`./bin/control-app & Live Proof`)** | `25` | `[25]` | Khép kín vòng lặp kiểm chứng sống qua `./bin/control-app --json` (đủ `--dry-run`, `Actionable Error`, `seed/auth/dom/screenshot`) và đóng dấu `WTREE_FINGERPRINT`. |
| **4. Điều phối Cô lập & Tốc độ (`Worktree / Cloud Swarm`)** | `20` | `[20]` | Chia đúng các đơn vị `sequence-verifiable-units`; tuân thủ ngưỡng `<= 10 Local Worktrees` vs `> 10 Cloud Agents + /swarm`; 0 xung đột tệp tin. |
| **5. Vệ sinh "Người làm vườn" & Bảo trì Bộ nhớ (`Gardener & Feature Map`)** | `15` | `[15]` | Nhổ sạch cỏ dại kiến trúc; xóa/lưu trữ file plan tạm sau khi merge; chạy `/maintain-verification-skill` cập nhật `Feature Map` và đạt `0` lỗi `Constraint Loop`. |
| **TỔNG ĐIỂM HIỆU CHUẨN** | **`100`** | **`[100 / 100]`** | **Xếp hạng: `GOLD STANDARD (>= 90)`** |

---

## 2. Bài Học Đúc Kết Sau Phiên Làm Việc (`Retro & Learnings`)

- **Điểm làm tốt cần phát huy (`Keep`):**
  - `[Ví dụ: Khung Type Signatures Sketch ở Pha 2 của /architect giúp phát hiện sớm lỗi thiết kế trước khi viết thân hàm]`.
- **Điểm cần cải thiện ở chu kỳ tới (`Improve`):**
  - `[Ví dụ: Bổ sung thêm subcommand mới vào ./bin/control-app cho luồng webhook]`.
- **Bài học lưu vào bộ nhớ dài hạn (`/learn`):**
  - `[Tên quy tắc / mẫu thiết kế mới đã được lưu vào bộ nhớ liên dự án]`.
