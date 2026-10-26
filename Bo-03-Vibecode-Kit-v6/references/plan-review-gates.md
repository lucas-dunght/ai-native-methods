# Giao Thức Lập Kế Hoạch Bằng Code, Đấu Trường `/architect` 5 Pha & Cổng Duyệt 4 Góc Nhìn (`VISION & BLUEPRINT Protocol`)

> **Bước 3 & Bước 4 của Vibecode Kit v6.2 (`× pstack`) · "Đo một trăm lần, cắt một lần" · Chống Ảo giác Tiến độ của Plan Mode truyền thống**

---

## 1. Tại Sao "Plan Mode" Truyền Thống Thất Bại? (`Critique of Abstract Plan Mode`)

Các bản kế hoạch văn bản trừu tượng (`Plan Mode` truyền thống) thường mắc hai căn bệnh kinh niên:
1. **Ảo giác Tiến độ (`Illusion of Progress`):** Chi tiết hóa quá mức tiểu tiết cài đặt bên trong (`over-specify implementation`) nhưng lại bỏ trống trải nghiệm của người gọi API hoặc người dùng cuối (`under-specify caller experience`).
2. **Hai Bẫy Duyệt Kế Hoạch (`Two Planning Traps`):**
   - **Bẫy 1:** Chấp nhận ngay phương án thiết kế đầu tiên do Agent sinh ra mà không có phương án đối chứng.
   - **Bẫy 2:** Review đối kháng quá đà trên một bản kế hoạch chữ trừu tượng, khiến Agent tự bịa ra hàng loạt rủi ro lý thuyết không bao giờ xảy ra trong thực tế để phòng thủ và làm phình to thiết kế.

Để khắc phục tận gốc, Vibecode Kit v6.2 bắt buộc thay thế việc lập kế hoạch trên giấy bằng **3 trụ cột thực nghiệm**: (1) `Working Backwards (4 ô Diátaxis + /unslop)`, (2) `/prototype (Live UI Switcher)` và (3) `5-Phase /architect Arena`.

---

## 2. Trụ Cột 1: Thiết Kế Ngược Từ README (`Working Backwards · Khung Diátaxis + /unslop`)

Khi thiết kế một module, gói thư viện hoặc dịch vụ dùng chung ở Bước 3 (`VISION`), Chủ thầu phải đi ngược từ việc viết tài liệu sử dụng (`Readme-Driven Development`) để đóng vai người gọi API trước khi thiết kế ruột hàm:

### Bốn Ô Tài Liệu Theo Khung `Diátaxis`:
1. **`Tutorial` (Bài học khởi đầu định hướng trải nghiệm):** Đoạn code ngắn nhất giúp người mới gọi chạy thành công tính năng trong 60 giây.
2. **`How-to` (Cẩm nang giải quyết bài toán thực tế):** Các đoạn code mẫu (`Caller Usage`) giải quyết 2 đến 3 kịch bản nghiệp vụ phổ biến nhất.
3. **`Reference` (Đặc tả kỹ thuật chuẩn xác):** Định nghĩa chính xác đầu vào, đầu ra, mã lỗi và bất biến trạng thái.
4. **`Explanation` (Giải thích lý do & đánh đổi):** Tại sao chọn thiết kế này và những giới hạn nào người gọi cần lưu ý.

### Quy Tắc Khử Văn Phong AI Rườm Rà (`/unslop`):
- Cắt bỏ 100% các câu mở đầu sáo rỗng, tính từ tán dương vô thưởng vô phạt hoặc các đoạn văn giải thích vòng vo.
- Mọi khẳng định trong bản thiết kế đều phải quy về kiểu dữ liệu, chữ ký hàm, câu lệnh CLI hoặc số liệu định lượng.

---

## 3. Trụ Cột 2: Lập Kế Hoạch Giao Diện Bằng Code Nháp (`/prototype` Live UI Switcher)

Đối với các tính năng có giao diện người dùng hoặc luồng tương tác phức tạp:
1. Thay vì tranh cãi trên bản mô tả bằng lời, hãy dựng nhanh **2 đến 3 phương án thiết kế/UI bằng code nháp** ẩn sau một nút chuyển trực tiếp trên màn hình (`Live UI Switcher` hoặc cờ `proto_variant=A|B|C`).
2. Sử dụng công cụ đòn bẩy `./bin/control-app` để:
   - Chuyển đổi qua lại giữa các phương án (`./bin/control-app flag --set proto_variant=B --json`);
   - Chụp ảnh màn hình và trích xuất cây giao diện (`DOM / accessibility tree`) ở cả trạng thái đầy đủ dữ liệu, trạng thái rỗng (`Empty`) và trạng thái lỗi (`Error`);
   - Đo đạc hiệu năng dựng hình thực tế.
3. Trình bày bằng chứng thực nghiệm của các phương án để Chủ nhà chọn phương án chiến thắng trước khi viết code hoàn thiện.

---

## 4. Trụ Cột 3: Đấu Trường Kiến Trúc 5 Pha Kỷ Luật (`5-Phase /architect Arena`)

Với mọi bài toán cấp `R2` và `R3`, Bước 4 (`BLUEPRINT`) bắt buộc vận hành qua 5 pha tuần tự của kỹ năng `/architect`:

```text
  [Pha 1: GROUND] ──► Chạy /how (Runtime) & /why (Git/PR/Ticket) để khóa quyền sở hữu (ownership) & ràng buộc.
         │
         ▼
  [Pha 2: SKETCH (Architecture Arena)] ──► Cho 2-3 nhánh (đa model) độc lập viết:
         │                                 "Type Signatures & Caller Usage Sketch"
         │                                 (CHỈ viết khung kiểu dữ liệu + chữ ký hàm + nơi gọi, CHƯA viết thân hàm).
         ▼
  [Pha 3: CROSS-JUDGE & SYNTHESIZE] ──► Dùng 1 model độc lập làm trọng tài chấm điểm theo Rubric
         │                              và tổng hợp thành bản thiết kế chữ ký hàm tốt nhất.
         ▼
  [Pha 4: IMPLEMENT AGAINST THE SKETCH] ──► Giao cho Thợ điền thân hàm thật theo TDD.
         │
         ▼
  [Pha 5: SCRAP WHEN WRONG] ──► Nếu khi vào code thật phát hiện phải truyền tham số vá víu,
                                lặp lại workaround ở nhiều nơi hoặc phải dùng any / ép kiểu cưỡng bức
                                ==> ĐẬP ĐI LÀM LẠI NGAY TỪ PHA 2!
```

### Bảng Tiêu Chí Chấm Điểm Đấu Trường Kiến Trúc (`Architecture Arena Rubric` · Thang 100):
| Tiêu chí chấm điểm | Trọng số | Câu hỏi kiểm định dành cho Trọng tài (`Cross-judge Model`) |
|---|---|---|
| **1. Độ sâu Module (`Ousterhout Deep Module`)** | `30đ` | Giao diện chữ ký hàm có đơn giản hơn nhiều so với độ phức tạp mà nó che giấu bên trong không, hay đang bị rò rỉ chi tiết cài đặt (`shallow module`)? |
| **2. Trải nghiệm Nơi Gọi (`Caller Ergonomics`)** | `25đ` | Nhìn vào đoạn code nơi gọi (`Caller Usage Sketch`), người dùng API có thể gọi đúng ngay mà không cần truyền hàng tá tham số cấu hình thừa không? |
| **3. Khóa Chặt Trạng thái Sai bằng Kiểu (`Make Illegal States Unrepresentable`)** | `25đ` | Kiểu dữ liệu (`Type Signatures`) có ngăn chặn được các trạng thái bất hợp lệ ngay từ lúc biên dịch không? |
| **4. Khả năng Kiểm chứng Độc lập (`Verifiability`)** | `20đ` | Có thể kiểm thử và gọi qua `./bin/control-app` dễ dàng mà không phải dựng hàng chục mock giả tạo không? |

### Luật Thép Pha 5: Khi Nào Phải Đập Đi Làm Lại (`Scrap When Wrong Triggers`)?
Trong quá trình thực thi Pha 4 (`Implement against the sketch`), nếu phát hiện bất kỳ dấu hiệu thực nghiệm nào dưới đây, Thợ và Chủ thầu **bắt buộc dừng lại và hủy bỏ bản phác thảo hiện tại (`Scrap when wrong`)** để quay về Pha 2:
1. **Truyền tham số vá víu (`Pass-through Parameter Hacks`):** Phải truyền thêm một tham số mới xuyên qua 3 tầng hàm trung gian chỉ để phục vụ một hàm con ở tận dưới đáy.
2. **Lặp lại đoạn code chữa cháy (`Repeated Workarounds`):** Phải viết lặp lại cùng một khối kiểm tra điều kiện hoặc biến đổi dữ liệu vá víu ở từ 2 nơi trở lên.
3. **Phá vỡ hệ thống kiểu (`Type Escape Hatches`):** Phải sử dụng `any`, `@ts-ignore`, `cast` cưỡng bức (`as unknown as T`) hoặc bỏ qua kiểm tra `null/undefined` để ép code chạy được.

---

## 5. Cổng Duyệt Kế Hoạch 4 Góc Nhìn (`4-Lens Plan Review Gate`)

Sau khi hoàn tất `5-Phase /architect Arena`, bản vẽ [`Blueprint-template.md`](../templates/Blueprint-template.md) phải đi qua 4 lăng kính kiểm định trước khi đóng dấu `APPROVED`:

1. **Lăng kính 1 · CEO / Phạm vi (`Scope & Value Lens`):**
   - Thách thức giả định gốc (`Premise Challenge`): Chúng ta có đang giải quyết đúng bài toán cốt lõi không?
   - Chọn chế độ duyệt phù hợp (`SCOPE EXPANSION`, `SELECTIVE EXPANSION`, `HOLD SCOPE` hoặc `SCOPE REDUCTION`).
2. **Lăng kính 2 · Thiết kế & Trải nghiệm (`Design & Interaction Lens`):**
   - Kiểm tra đầy đủ 5 trạng thái giao diện: `Default`, `Loading`, `Empty`, `Error` và `Overflow`.
   - Đối chiếu kết quả thực nghiệm từ `/prototype` (nếu có UI).
3. **Lăng kính 3 · Kỹ thuật & Cứu hộ Lỗi (`Engineering & Error Rescue Lens`):**
   - Lập **Bảng Ánh xạ Lỗi & Cứu hộ (`Error & Rescue Map`)**: Mọi lệnh gọi mạng, truy vấn DB hoặc phân tích dữ liệu có nguy cơ thất bại đều phải có hành động cứu hộ cụ thể và thông báo rõ ràng.
   - Đảm bảo 0 lỗ hổng bảo mật (`Zero-Secret Policy`, phân quyền chặt chẽ).
4. **Lăng kính 4 · Trải nghiệm Lập trình viên & Agent (`DX & Verification Lever Lens`):**
   - Kiểm tra xem tính năng mới đã được ánh xạ vào `./bin/control-app` và `Feature Map` (`references/features/README.md`) chưa.
   - Đảm bảo mọi thông báo lỗi mới đều có hướng dẫn lệnh tiếp theo (`next_command`) cho Agent.

---

## 6. Tham Vấn Quân Sư Độc Lập (`Kongming Advisory Protocol`)

Khi gặp một trong hai tình huống: (a) Bài toán thuộc tầng rủi ro `R3` (Xác thực, Thanh toán, Di chuyển dữ liệu lớn) hoặc (b) Hai phương án trong `Architecture Arena` có điểm số ngang ngửa nhau với đánh đổi phức tạp, Chủ thầu kích hoạt phiên tham vấn **Quân sư độc lập (`@kongming`)**:
- Cung cấp cho Quân sư bản tóm tắt hiện trạng (`/how` + `/why`), 2 bản `Type Signatures Sketch` và các ràng buộc bất biến.
- Quân sư chỉ trả về phán quyết phân tích ưu/nhược điểm và khuyến nghị chọn phương án, không trực tiếp sửa code để giữ sự độc lập tuyệt đối.
