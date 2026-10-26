# Phiếu Phân Loại Tầng Rủi Ro & Định Tuyến Quy Trình (`Risk-Tier Classification · v6.2 × pstack`)

- **Mã Tác vụ / Yêu cầu:** `[TASK-ID / Tên yêu cầu]`
- **Ngày tạo:** `[YYYY-MM-DD]`
- **Người phân loại:** `[Chủ thầu / AI Contractor]`

---

## 1. Bảng Kiểm Nhận Diện Nhanh (`5-Point Risk Scan`)

| Tiêu chí khảo sát (`[OBSERVED]`) | Giá trị đo được | Tác động tới Cấp độ Rủi ro |
|---|---|---|
| **1. Số lượng tệp dự kiến chạm tới (`File Count`)** | `[X files]` | `< 3`: `R0` · `3-8`: `R1` · `> 8`: `R2/R3` |
| **2. Thay đổi Cấu trúc Dữ liệu / Hợp đồng API (`Schema / API`)** | `[Có / Không]` | Nếu `Có` -> Tối thiểu `R2` |
| **3. Chạm tới Bảo mật, Xác thực, Thanh toán, Hạ tầng (`Critical Surface`)** | `[Có / Không]` | Nếu `Có` -> Bắt buộc `R3` |
| **4. Đã có trong `Feature Map` (`references/features/README.md`) & có lệnh `./bin/control-app`?** | `[Có / Chưa]` | Nếu `Chưa` -> Cần bổ sung subcommand vào `./bin/control-app` và cập nhật `Feature Map` |
| **5. Số lượng gói việc độc lập dự kiến chạy song song (`Parallel Units`)** | `[N units]` | `<= 10`: `Local Git Worktrees` · `> 10`: `Coordinator + Cloud Agents + /swarm` |

---

## 2. Quyết Định Phân Tầng & Các Cổng Bắt Buộc (`Adaptive Gate Routing`)

- **Cấp độ Rủi ro được chốt:** **`[R0 / R1 / R2 / R3]`**
- **Lý do chọn (`[OBSERVED: file:line]`):** `[Giải thích ngắn gọn dựa trên bằng chứng quét mã nguồn]`.

### Các Cổng Được Bật Theo Cấp Độ Đã Chọn (Đánh dấu `[x]`):
- [ ] **Chế độ `R0 (Fast-Track)`:** Đọc `Feature Map` -> Sửa trực tiếp -> Chạy `./bin/control-app` hoặc test/build -> Đóng dấu `WTREE_FINGERPRINT`.
- [ ] **Chế độ `R1 (4-Step Standard)`:** `Indirect Prompting Restate` ngắn (2 câu) + đọc `Feature Map` -> TDD (`Red -> Green`, áp dụng luật `Scrap when wrong` nếu lệch) -> Kiểm chứng sống qua `./bin/control-app --json` -> Ship kèm `WTREE_FINGERPRINT`.
- [ ] **Chế độ `R2 (8-Step Systemic)`:** Đầy đủ 8 bước (`SCAN + /teach (/how+/why+/recall) -> RRI -> VISION Working Backwards Diátaxis + /prototype -> BLUEPRINT 5-Phase /architect Arena + 4-Lens -> TASK GRAPH sequence-verifiable-units -> BUILD -> VERIFY ./bin/control-app + Arbiter C3 -> SHIP + Xóa plan tạm + /maintain-verification-skill`).
- [ ] **Chế độ `R3 (8-Step Ultra + CSO)`:** Đầy đủ 8 bước `R2` + Tham vấn Quân sư (`@kongming`) + Kiểm toán Bảo mật (`CSO / STRIDE`) + Phát hành 2 giai đoạn (`beta -> official`) + Canh gác sau triển khai (`Canary`).
