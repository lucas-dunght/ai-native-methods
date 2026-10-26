# Ví Dụ Thực Chiến Toàn Trình (`Worked Example · Vibecode Kit v6.2 × pstack`)

> **Bài toán thực tế:** Xây dựng tính năng *"Cho phép khách hàng tự hủy đơn hàng và hoàn tiền tự động (`Idempotent Order Cancellation`)"* trên hệ thống Thương mại Điện tử.

---

## Bước 1 · `SCAN` (Đọc `Feature Map`, `Indirect Prompting Restate` & Bộ tứ `/teach`)

**Chủ thầu (`AI Contractor`) thực thi:**
1. **Tra cứu `Feature Map` (`[OBSERVED: references/features/README.md:12]`):**
   - Tính năng `FEAT-02 (Order Detail)` hiện nằm tại `src/orders/order-service.ts` và `src/pages/OrderDetail.tsx`, lệnh chạm là `./bin/control-app dom --route /orders/ORD-01 --json`.
2. **Bản Diễn Đạt Lại Bằng Lời Tự Nhiên (`Indirect Prompting Restate`):**
   - **Hiện trạng đang chạy:** Hệ thống mới chỉ có luồng tạo đơn (`createOrder` tại `src/orders/order-service.ts:18-64`), khách hàng muốn hủy đơn phải nhắn tin cho bộ phận CSKH hủy tay.
   - **Nhu cầu thật:** Khách hàng cần nút tự hủy đơn ngay trên trang chi tiết đơn hàng khi đơn ở trạng thái `PENDING` hoặc `PAID`, đảm bảo bấm đúp nhiều lần cũng không bao giờ bị hoàn tiền 2 lần (`idempotent`).
   - **Ranh giới bất biến:** Không được phép hủy đơn đã chuyển sang trạng thái đang giao (`SHIPPED`).
3. **Mô hình Nhận thức Hai chiều (`/teach = /how + /why + /recall`):**
   - **`/how` (Runtime):** `[OBSERVED: src/payments/stripe-gateway.ts:42-79]` hàm `refundCharge(chargeId, idempotencyKey)` gọi trực tiếp cổng thanh toán bên thứ ba và có thể mất tới `3.5s` khi mạng chậm.
   - **`/why` (Lịch sử Git/PR):** `[OBSERVED: git log -S "refundCharge" -> PR #142]` cho thấy trước đây từng xảy ra lỗi khóa bảng (`row lock timeout`) khi gọi cổng thanh toán bên trong giao dịch cơ sở dữ liệu (`DB transaction`). Do đó, bước gọi hoàn tiền bắt buộc phải tách ra khỏi `DB transaction` qua hàng đợi `Outbox`.
   - **`/teach` (Chứng minh thực nghiệm):** Sơ đồ đối chiếu cho thấy việc ghi bản ghi `OutboxRefundJob` cùng giao dịch đổi trạng thái `CANCELLED` giúp giảm thời gian giữ khóa DB từ `3.500ms` xuống `< 15ms`.
4. **Phân loại Rủi ro (`Risk Tier`):** Chạm tới tiền tệ, cơ sở dữ liệu và giao diện (`6 files`) -> Xếp hạng **`R2` (kèm kiểm tra an toàn thanh toán của `R3`)**.

---

## Bước 2 · `RRI` (Phỏng Vấn Khử Mơ Hồ & Bảng Quyết Định `D1`)

Chủ thầu phát hiện 1 điểm cần chốt với Chủ nhà và trình bày **Bảng Quyết định `D1`**:

### Quyết định `D1`: Cơ chế xử lý hoàn tiền khi khách hủy đơn ở trạng thái `PAID`
- **`ELI10`:** Khi khách bấm nút "Hủy đơn", nếu chờ cổng thanh toán ngân hàng trả lời ngay lập tức thì khách có thể phải nhìn vòng quay chờ 3 đến 5 giây hoặc bị lỗi nếu ngân hàng bảo trì. Nếu chúng ta ghi nhận lệnh hủy ngay vào bảng tạm (`Outbox`) rồi để tiến trình ngầm hoàn tiền trong vài giây sau, khách sẽ nhận được phản hồi tức thì.
- **`Khuyến nghị:`** Chọn **Phương án A (`Completeness: 10/10`)** theo đúng bài học lịch sử từ bước `/why` (`PR #142`).

```text
Cam kết thực hiện                        | Hiện tại | A (Recommended: Outbox) | B (Gọi trực tiếp)
-----------------------------------------+----------+-------------------------+------------------
Chống hoàn tiền trùng (Idempotency Key)  | Không    | Có (10/10)              | Có
Tự động thử lại khi cổng thanh toán lỗi  | Không    | Có (10/10)              | Không (Nợ Type-2)
```
> **Phản hồi của Chủ nhà:** *"Duyệt Phương án A (`D1: A`). Bản Indirect Prompting Restate hoàn toàn chính xác."* -> **Điểm `RRI = 9.6/10` (`APPROVED`)**.

---

## Bước 3 · `VISION` (`Working Backwards Diátaxis + /unslop` & `/prototype` Switcher)

1. **Thiết kế Ngược từ README (`Working Backwards · 4 Ô Diátaxis + /unslop`):**
   - **`Tutorial`:**
     ```typescript
     const receipt = await cancelOrder({
       orderId: "ORD-2026-01",
       actorId: "USR-88",
       idempotencyKey: "cancel-ORD-2026-01-v1",
       reason: "CHANGED_MIND",
     });
     ```
   - **`How-to`:** Nếu `receipt.status === "REFUND_QUEUED"`, hiển thị hộp thoại tiến trình hoàn tiền kèm mã `receipt.refundJobId`.
   - **`Reference`:** Trả mã lỗi `ORDER_ALREADY_SHIPPED (409)` nếu đơn đã giao cho đơn vị vận chuyển.
   - **`Explanation`:** Sử dụng mẫu `Transactional Outbox` để đảm bảo tính nguyên tử giữa trạng thái đơn hàng và lệnh hoàn tiền.
2. **Thực nghiệm Giao diện bằng Code Nháp (`/prototype` Live UI Switcher):**
   - Dựng 2 phương án hộp thoại xác nhận hủy đơn ẩn sau cờ `./bin/control-app flag --set proto_variant=A|B --json`.
   - Chụp ảnh thực nghiệm qua `./bin/control-app screenshot --route /orders/ORD-01 --json`. Chủ nhà chọn `Variant B` (có thanh trạng thái tiến độ hoàn tiền rõ ràng).

---

## Bước 4 · `BLUEPRINT` (`5-Phase /architect Arena` & Cổng Duyệt 4 Góc Nhìn)

### Pha 2 & Pha 3 của `/architect Arena`: Khung Chữ Ký Kiểu (`Type Signatures Sketch` · Chưa viết thân hàm)
```typescript
export type CancelResultStatus = "CANCELLED_NO_REFUND" | "CANCELLED_REFUND_QUEUED";

export interface CancelOrderCommand {
  readonly orderId: string;
  readonly actorId: string;
  readonly idempotencyKey: string;
  readonly reason: "CHANGED_MIND" | "DUPLICATE_ORDER" | "FOUND_CHEAPER";
}

export interface CancelOrderReceipt {
  readonly orderId: string;
  readonly status: CancelResultStatus;
  readonly refundJobId: string | null;
}

export declare function cancelOrder(cmd: CancelOrderCommand): Promise<CancelOrderReceipt>;
```
- **Điểm chấm của Trọng tài (`Cross-Judge Rubric`):** Sketch Nhánh A đạt **`96/100`** (Module sâu theo chuẩn Ousterhout, khóa chặt trạng thái bằng kiểu và kiểm chứng trực tiếp qua `./bin/control-app`).
- **Luật `Scrap when wrong`:** Khóa cứng điều kiện dừng nếu Thợ phải truyền tham số vá víu qua 3 tầng hoặc dùng `any`.
- **Cổng 4 Góc nhìn (`4-Lens Gate`):** Cả 4 lăng kính (`CEO`, `Design`, `Eng`, `DX`) đều đóng dấu `CLEAR · NO UNRESOLVED DECISIONS`.

---

## Bước 5 · `TASK GRAPH` (`Sequence-Verifiable-Units` & Điều Phối `Local Worktrees <= 10`)

Vì dự án chỉ có **2 đơn vị kiểm chứng độc lập (`2 <= 10`)**, Chủ thầu sử dụng `Local Git Worktrees` (chưa cần đẩy lên `Cloud Agents + /swarm`):
- **`TIP-01` (`Unit 1 · Backend` · `.worktrees/tip-01-backend`):**
  - `owned_files`: `src/orders/cancel-order.ts`, `tests/orders/cancel-order.test.ts`
  - `Live Verification`: `./bin/control-app seed --dry-run --json && ./bin/control-app dom --route /api/orders/ORD-01 --json`
- **`TIP-02` (`Unit 2 · Frontend` · `.worktrees/tip-02-frontend`):**
  - `owned_files`: `src/components/CancelOrderModal.tsx`, `tests/components/CancelOrderModal.test.tsx`
  - `Live Verification`: `./bin/control-app screenshot --route /orders/ORD-01 --json`
- Kiểm tra giao nhau: `owned_files(TIP-01) ∩ owned_files(TIP-02) = ∅`.

---

## Bước 6 & Bước 7 · `BUILD & VERIFY` (TDD, `./bin/control-app` Live Proof & Trọng Tài `C3`)

1. **Thực thi TDD & Kiểm tra `Scrap when wrong`:**
   - Hai Thợ hoàn thành code từ khung `Type Signatures Sketch` với `0` lần kích hoạt `Scrap when wrong` (`0` kiểu `any`, `0` tham số vá víu).
   - Toàn bộ `12/12` bài kiểm thử tự động chuyển sang màu xanh (`[measured: npm test -> 12 passed in 1.14s]`).
2. **Kiểm chứng Sống qua Đòn bẩy `./bin/control-app` (`Close the Loop`):**
   ```bash
   ./bin/control-app auth --role member --json
   ./bin/control-app dom --route /orders/ORD-01 --json
   ./bin/control-app screenshot --route /orders/ORD-01 --json
   ```
   - Kết quả trả về `{"ok":true,"status_code":200,"order_state_after":"CANCELLED_REFUND_QUEUED","measured_ms":14}`.
3. **Đóng dấu Vân tay & Trọng tài `C3`:**
   ```text
   WTREE_FINGERPRINT: HEAD=7c4a91b TREE=8f2e1d04a93c WTREE=4b90e12a7c88d019 DIRTY_FILES=0
   ARBITER_VERDICT: APPROVED (All AC-1..AC-4 verified with live ./bin/control-app receipts)
   ```

---

## Bước 8 · `REFINE & SHIP` (`Dual-Stage Ship`, `The Gardener`, Xóa Plan Tạm & Bảo Trì `Feature Map`)

1. **Phát hành 2 giai đoạn (`beta -> official`):** Hợp nhất lên `beta`, theo dõi Canary `0` lỗi phát sinh, sau đó hợp nhất lên `main`.
2. **Tuần tra theo vai trò "Người làm vườn" (`The Gardener`) & Vệ sinh File Plan Tạm:**
   - Nhổ bỏ 1 hàm định dạng tiền tệ bị viết lặp trong nhánh UI và gộp về `src/utils/currency.ts`.
   - Thu hồi 2 nhánh `.worktrees/tip-01-backend` và `.worktrees/tip-02-frontend`, đồng thời chuyển tệp kế hoạch thực thi tạm vào `_Archive/` để giữ kho mã nguồn sạch tuyệt đối.
3. **Bảo trì Bộ nhớ Vật chất hóa (`/maintain-verification-skill`):**
   - Cập nhật mục `FEAT-02` trong `references/features/README.md` (`Feature Map`) kèm mã băm SHA-256 mới và chạy `./bin/control-app doctor --json` (`drift_detected: false`).
4. **Thẻ Hiệu chuẩn 100 Điểm (`Calibration Card`):**
   - Tổng điểm phiên làm việc đạt **`99/100` (`GOLD STANDARD`)**.
