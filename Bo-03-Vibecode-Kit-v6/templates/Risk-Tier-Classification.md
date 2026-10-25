# Phân tầng Rủi ro (Risk Tier Classification) & Định tuyến Quy trình v6.1

Tài liệu này dùng làm bản mẫu phân loại mức độ rủi ro cho từng yêu cầu hoặc gói công việc (`TIP`), từ đó quyết định độ co giãn của quy trình 8 bước, cấp độ bằng chứng nghiệm thu và chế độ giám sát AI tương ứng.

## 1. Ma trận Phân tầng Rủi ro (Impact × Reversibility)

Xác định phân tầng của tác vụ bằng cách giao hai trục **Mức độ tác động nếu xảy ra lỗi (Impact)** và **Khả năng hoàn tác/đảo ngược (Reversibility)**.

| Mức tác động (Impact) \ Khả năng đảo ngược (Reversibility) | Đảo ngược tức thì (Reversible · 1 lệnh revert, không mất dữ liệu) | Đảo ngược một phần (Partial · cần script chỉnh lại hoặc ảnh hưởng cục bộ) | Khó hoặc không thể đảo ngược (Irreversible · đổi schema dữ liệu thật, thanh toán, bảo mật, công bố đối ngoại) |
|---|---|---|---|
| **Thấp (Low · giao diện phụ, công cụ nội bộ nhỏ)** | **R0 (Trivial)** | **R1 (Low)** | **R2 (Medium)** |
| **Trung bình (Medium · tính năng người dùng thường xuyên, API nội bộ)** | **R1 (Low)** | **R2 (Medium)** | **R3 (High)** |
| **Cao (High · luồng nghiệp vụ chính, xác thực, dữ liệu khách hàng)** | **R2 (Medium)** | **R3 (High)** | **R3 (Critical)** |
| **Nghiêm trọng (Critical · tài chính, pháp lý, hạ tầng cốt lõi)** | **R3 (High)** | **R3 (Critical)** | **R3 (Critical)** |

## 2. Bảng Co giãn Quy trình 8 Bước theo Risk Tier

| Bước trong Workflow | R0 · Trivial (5 đến 15 phút) | R1 · Low (1 TIP · < 2 giờ) | R2 · Medium (2 đến 5 TIPs) | R3 · High / Critical (5+ TIPs) |
|---|---|---|---|---|
| **1. SCAN** | Đọc nhanh file cần sửa | Quét cục bộ module liên quan (`SCAN-NNN`) | Quét đầy đủ codebase + gắn nhãn Claim Discipline | Quét toàn diện + X-Ray + đối chiếu Kernel Registry (Bộ 02) |
| **2. RRI** | Bỏ qua | Hỏi nhanh 1 đến 3 câu nếu mơ hồ | RRI chuẩn 5 Personas + Thẻ quyết định `D<N>` | RRI sâu + Phân loại 3 tầng + Khóa danh mục Shortcut Debt |
| **3. VISION** | Bỏ qua | Gộp vào Blueprint | Vision + Extension Trace + Duyệt 4 Lăng kính (`4-Lens Gate`) | Vision + Extension Trace + 4-Lens Gate + Tham vấn Kongming |
| **4. BLUEPRINT** | Bỏ qua | Blueprint gọn nửa trang | Blueprint đầy đủ + Phản biện Red-Team 4 góc nhìn | Blueprint + Red-Team + Ultra Best-of-5 + Chủ nhà ký duyệt cứng |
| **5. TASK GRAPH** | TIP 1 dòng | 1 file `TIP-NNN.md` có Scope Freeze | Đồ thị 2 đến 5 TIPs + Ma trận sở hữu file | Đồ thị đa TIP + Cô lập từng Thợ trên `git worktree` riêng |
| **6. BUILD** | Sửa trực tiếp | Thi công trong Scope Freeze + chụp `WTREE_FINGERPRINT` | Thi công + Constraint Loop + Handoff 9 mục nếu chuyển phiên | Đa Thợ thi công song song + Luật dừng 3-Strike báo Kongming |
| **7. VERIFY** | Chạy lệnh kiểm tra nhanh | Unit test + kiểm tra `WTREE_FINGERPRINT` tươi (`FRESH`) | QA bề mặt thật + Test đỏ trước khi sửa xanh + Test Audit | Đầy đủ QA bề mặt thật + Trọng tài độc lập (`Arbiter C3`) chấm chéo |
| **8. REFINE & SHIP** | Commit + ghi 1 dòng hiệu chỉnh | Commit + Calibration Card ngắn | Ship PR + Calibration Card 100 điểm + Rà soát Shortcut Debt | Phát hành 2 chặng (`Beta -> Stable`) + Calibration 100 điểm đầy đủ |

## 3. Định tuyến Năng lực Mô hình (Capability & Supervision Routing)

Lấy cảm hứng từ cơ chế định tuyến mô hình của `ak-orchestrate` và `gstack`, mỗi vai trò trong từng phân tầng được khuyến nghị cấu hình như sau.

| Vai trò trong Vibecode v6.1 | Tác vụ R0 / R1 | Tác vụ R2 | Tác vụ R3 |
|---|---|---|---|
| **Chủ thầu (Contractor)** | Mô hình thông minh tiêu chuẩn (Smart tier) | Mô hình suy luận mạnh (Frontier tier) | Mô hình suy luận mạnh nhất + bật chế độ tư duy sâu |
| **Thợ thi công (Builder)** | Mô hình tốc độ cao (Fast / Smart tier) | Mô hình lập trình chuẩn (Smart tier) | Mô hình lập trình chuẩn chạy trên các Worktree cô lập |
| **Quân sư (Kongming Advisory)** | Không bắt buộc | Bật khi gặp lỗi quá 3 lần (3-Strike) | Bật xuyên suốt ở 5 điểm chốt (trước và sau mỗi pha lớn) |
| **Trọng tài (Independent Arbiter)** | Chủ thầu kiêm nhiệm kiểm tra nhanh | Phiên mới độc lập ngữ cảnh | Phiên mới độc lập ngữ cảnh và ưu tiên khác họ mô hình (Cross-Model) |

## 4. Phiếu Đánh giá Phân tầng Rủi ro cho Tác vụ Mới (Copy vào TIP hoặc RRI)

```markdown
### Đánh giá Risk Tier cho Tác vụ · [Tên tác vụ]
- **Mức độ tác động nếu sai (Impact).** [Low | Medium | High | Critical] vì [lý do cụ thể].
- **Khả năng đảo ngược (Reversibility).** [Reversible | Partial | Irreversible] vì [lý do cụ thể].
- **Phân tầng kết luận.** **R[0|1|2|3]**
- **Cấp độ bằng chứng nghiệm thu tối thiểu (Evidence Floor).** `[unit-test | fixture-replay | live-run | production]`
- **Các cơ chế bảo vệ kích hoạt.** `[Scope Freeze | 4-Lens Gate | Red-Team | Worktree Isolation | Kongming Advisory | Arbiter C3 | Dual-Stage Ship]`
```
