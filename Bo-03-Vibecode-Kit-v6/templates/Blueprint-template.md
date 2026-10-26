# Bản Vẽ Kiến Trúc & Kế Hoạch Thực Thi (`Blueprint · v6.2 × pstack`)

- **Mã Dự án / Epic:** `[EPIC-YYYY-MM]`
- **Cấp độ Rủi ro (`Risk Tier`):** `[R1 / R2 / R3]`
- **Chế độ Duyệt (`Review Mode`):** `[SELECTIVE EXPANSION / HOLD SCOPE / SCOPE EXPANSION / SCOPE REDUCTION]`
- **Điểm RRI đầu vào:** `[X.X / 10.0]` (`Status: APPROVED`)

---

## 1. Bối Cảnh & Giả Định Gốc Đã Kiểm Chứng (`Premise & Reality Ledger · Pha 1 Ground`)

| Mã Giả định | Khẳng định thực trạng (`/how` Runtime + `/why` Lịch sử Git/PR) | Bằng chứng (`[OBSERVED: file:line]`) | Kết luận |
|---|---|---|---|
| `P1` | `[Hiện trạng module A và lý do lịch sử viết như vậy qua /why]` | `[src/moduleA.ts:12-45]` | `verified` |
| `P2` | `[Lệnh kiểm chứng hiện có trong Feature Map references/features/README.md]` | `[references/features/README.md:10]` | `verified` |

---

## 2. Thiết Kế Ngược Từ README (`Working Backwards · 4 Ô Diátaxis + /unslop`)

> **Chống "Ảo giác Tiến độ":** Trước khi thiết kế ruột hàm, đóng vai người gọi API / người dùng cuối để viết tài liệu sử dụng theo 4 ô `Diátaxis` (đã lọc bỏ 100% văn phong AI rườm rà qua `/unslop`):

1. **`Tutorial` (Trải nghiệm chạy thử trong 60 giây):**
   ```typescript
   // Đoạn code ngắn nhất để người mới gọi chạy thành công tính năng
   const receipt = await cancelOrder({ orderId: "ORD-01", actorId: "USR-99", reason: "CHANGED_MIND" });
   ```
2. **`How-to` (Giải quyết kịch bản thực tế):**
   - Kịch bản 1: `[Hủy đơn hàng chưa thanh toán (PENDING) -> hủy tức thì]`
   - Kịch bản 2: `[Hủy đơn hàng đã thanh toán (PAID) -> tạo lệnh hoàn tiền bất đồng bộ]`
3. **`Reference` (Đặc tả đầu vào / đầu ra / mã lỗi):**
   - Đầu vào: `CancelOrderInput` · Đầu ra: `Result<CancelOrderReceipt, OrderError>`
4. **`Explanation` (Lý do thiết kế & đánh đổi):**
   - `[Giải thích ngắn gọn tại sao tách bước hoàn tiền sang hàng đợi thay vì gọi đồng bộ]`

---

## 3. Thực Nghiệm Giao Diện Bằng Code Nháp (`/prototype` Live UI Switcher · Nếu có UI)

- **Cờ chuyển đổi phương án (`Live Switcher Flag`):** `./bin/control-app flag --set proto_variant=<A|B> --json`
- **So sánh thực nghiệm:**
  - `Variant A`: `[Mô tả + đường dẫn ảnh chụp .tmp/artifacts/proto-a.png + độ trễ đo được]`
  - `Variant B`: `[Mô tả + đường dẫn ảnh chụp .tmp/artifacts/proto-b.png + độ trễ đo được]`
- **Phương án được chọn:** `[Variant A / Variant B / SKIPPED (Backend-only)]`

---

## 4. Đấu Trường Kiến Trúc 5 Pha (`5-Phase /architect Arena · Pha 2 & Pha 3`)

### 4.1. Khung Chữ Ký Kiểu & Nơi Gọi (`Type Signatures & Caller Usage Sketch` · Chưa viết thân hàm)
```typescript
// CHỈ viết kiểu dữ liệu và chữ ký hàm từ góc nhìn nơi gọi (tuyệt đối chưa viết thân hàm)
export type OrderCancelStatus = "CANCELLED_IMMEDIATELY" | "REFUND_QUEUED";

export interface CancelOrderInput {
  readonly orderId: string;
  readonly actorId: string;
  readonly idempotencyKey: string;
  readonly reason: "CHANGED_MIND" | "DUPLICATE_ORDER" | "OUT_OF_STOCK";
}

export interface CancelOrderReceipt {
  readonly orderId: string;
  readonly status: OrderCancelStatus;
  readonly refundJobId?: string;
  readonly cancelledAtIso: string;
}

export declare function cancelOrder(input: CancelOrderInput): Promise<CancelOrderReceipt>;
```

### 4.2. Bảng Chấm Điểm Đấu Trường Đa Nhánh (`Cross-Judge Rubric` · Thang 100)
| Phương án Phác thảo | Độ sâu Module Ousterhout (`30đ`) | Trải nghiệm Nơi Gọi (`25đ`) | Khóa Trạng thái Sai bằng Kiểu (`25đ`) | Khả năng Kiểm chứng `./bin/control-app` (`20đ`) | Tổng điểm & Phán quyết của Trọng tài |
|---|---|---|---|---|---|
| **Sketch Nhánh A** | `[28/30]` | `[24/25]` | `[24/25]` | `[20/20]` | **`96/100` (CHỌN)** |
| **Sketch Nhánh B** | `[22/30]` | `[19/25]` | `[20/25]` | `[16/20]` | `77/100` (Loại vì lộ chi tiết cài đặt) |

### 4.3. Luật Đập Đi Làm Lại Khi Vào Code Thật (`Pha 5 · Scrap When Wrong Triggers`)
> Nếu trong Bước 6 (`BUILD`), Thợ gặp bất kỳ dấu hiệu nào dưới đây thì **BẮT BUỘC DỪNG CODE NGAY** và báo `SCRAP_TRIGGERED` để quay lại mục 4.1:
> 1. Phải truyền thêm tham số vá víu xuyên qua `>= 3` tầng hàm không liên quan;
> 2. Phải lặp lại cùng một đoạn code chữa cháy (`workaround`) ở `>= 2` nơi;
> 3. Phải dùng kiểu `any`, `@ts-ignore` hoặc ép kiểu cưỡng bức (`as unknown as T`).

---

## 5. Sơ Đồ Kiến Trúc & Luồng Dữ Liệu (`Architecture & Data Flow`)

```text
[Client / Caller]
       │ (1. Request + IdempotencyKey)
       ▼
[API Controller / Entrypoint] ──(2. Validate Schema)──► [Core Domain Service (cancelOrder)]
                                                               │
                                         ┌─────────────────────┴─────────────────────┐
                                         ▼ (Success)                                 ▼ (Error)
                                [Repository / DB TX]                        [Structured Error Rescue]
```

---

## 6. Bảng Ánh Xạ Lỗi & Cứu Hộ (`Error & Rescue Map`)

| Phương thức / Bước xử lý | Điều gì có thể sai (`Failure Mode`) | Phân loại Lỗi | Đã có Cứu hộ? | Hành động Cứu hộ & Lệnh `./bin/control-app` Tiếp theo | Thông báo Người dùng Nhận được |
|---|---|---|---|---|---|
| `[Bước 1: Xác thực đầu vào]` | `[Thiếu trường bắt buộc hoặc sai định dạng]` | `ValidationError` | `Y` | `[Trả mã 400 kèm danh sách trường lỗi và next_command]` | `"Dữ liệu đầu vào chưa hợp lệ."` |
| `[Bước 2: Ghi cơ sở dữ liệu]` | `[Xung đột khóa hoặc mất kết nối tạm thời]` | `DatabaseError` | `Y` | `[Rollback giao dịch, ghi log kèm mã truy vết, thử lại tối đa 2 lần]` | `"Hệ thống đang bận, vui lòng thử lại sau giây lát."` |

---

## 7. Danh Sách Đơn Vị Kiểm Chứng Độc Lập (`Sequence-Verifiable-Units`) & Phân Luồng `Worktree / Swarm`

- **Chế độ điều phối:** `[Local Git Worktrees (<= 10 nhánh) / Coordinator Bot + Cloud Agents + /swarm (> 10 nhánh)]`

| Mã Gói việc (`TIP`) | Thứ tự (`Sequence Unit`) | Vai trò Thợ | Danh sách Tệp Độc quyền (`owned_files` · Không giao nhau) | Lệnh Kiểm chứng Sống (`Live Verification via ./bin/control-app`) |
|---|---|---|---|---|
| `TIP-01` | `Unit 1 (PR #1)` | `backend-builder` | `src/services/order.ts`, `tests/services/order.test.ts` | `./bin/control-app seed --dry-run --json && ./bin/control-app dom --route /api/orders --json` |
| `TIP-02` | `Unit 2 (PR #2)` | `frontend-builder` | `src/components/OrderCard.tsx`, `tests/components/OrderCard.test.tsx` | `./bin/control-app screenshot --route /orders/ORD-01 --json` |

---

## 8. Bảng Tổng Hợp Duyệt 4 Góc Nhìn (`4-Lens Gate Summary`)

| Cổng Duyệt (`Lens`) | Trạng thái | Ghi chú & Quyết định Đã Chốt |
|---|---|---|
| **1. CEO / Phạm vi (`Scope Lens`)** | `CLEAR` | Đã chốt `D1..DN`, không còn quyết định treo. |
| **2. Thiết kế / Giao diện (`Design Lens`)** | `CLEAR` | Đã kiểm chứng `/prototype` và đủ 5 trạng thái (`Default`, `Loading`, `Empty`, `Error`, `Overflow`). |
| **3. Kỹ thuật / Bảo mật (`Eng & Security Lens`)** | `CLEAR` | Đã qua `5-Phase /architect Arena`, 100% luồng lỗi có cứu hộ, tuân thủ `Zero-Secret Policy`. |
| **4. Trải nghiệm Lập trình viên (`DX & Lever Lens`)** | `CLEAR` | Đã ánh xạ vào `./bin/control-app` và `Feature Map` (`references/features/README.md`). |

**PHÁN QUYẾT CUỐI CÙNG:** `APPROVED · NO UNRESOLVED DECISIONS`
