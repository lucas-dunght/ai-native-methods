# Giao thức Kỷ luật Nhận định, Vòng lặp Ràng buộc và Sổ cái Bằng chứng

Tài liệu này quy định tiêu chuẩn trung thực nhận thức và bằng chứng cơ học cho cả Chủ thầu, Thợ thi công và Trọng tài trong Vibecode Kit v6.1, kết hợp từ giao thức **Claude Fable 5.1 (`ak-fable-thinking`)** và hệ thống **Verification Evidence Ledger (`gstack-evidence` / `gstack-wtree`)**.

## 1. Kỷ luật Nhận định 4 Mức (Fable 5.1 Claim Discipline)

Mọi nhận định chịu tải trong `SCAN REPORT`, `Blueprint`, `Completion Report` và `Calibration Card` đều phải được phân loại rõ ràng theo nguồn gốc nhận thức.

| Nhãn nhận định | Ý nghĩa | Ngữ pháp bắt buộc | Quy tắc nâng/hạ cấp |
|---|---|---|---|
| **OBSERVED** | Đã tận mắt thấy trong phiên làm việc hiện tại thông qua việc đọc file, chạy lệnh hoặc đo đạc trực tiếp | "File X tại dòng Y trả về Z", "Lệnh X thoát với mã 0 và in ra Y" | Khi môi trường hoặc mã nguồn bị chỉnh sửa, một nhận định `OBSERVED` cũ tự động hạ xuống thành `PRIOR` cho tới khi kiểm tra lại. |
| **DERIVED** | Suy ra một cách tất yếu từ các dữ kiện `OBSERVED` thông qua một cơ chế giải thích được | "Vì A đã quan sát thấy ở file X nên B sẽ xảy ra theo cơ chế Y" | Phải nêu rõ cả dữ kiện gốc lẫn cơ chế dẫn xuất. |
| **PRIOR** | Kiến thức tổng quát từ dữ liệu huấn luyện hoặc từ phiên làm việc cũ, có thể đã lỗi thời | "Theo mặc định của thư viện X phiên bản trước thì...", "Ở chu kỳ trước hệ thống từng..." | Không bao giờ dùng `PRIOR` làm trụ cột kiến trúc mà không chạy lệnh kiểm tra thực tế để nâng lên `OBSERVED`. |
| **ASSUMED** | Giả định chưa được kiểm chứng tại thời điểm hiện tại nhưng cần thiết để tiếp tục lập kế hoạch | "Đang giả định X. Nếu X sai thì hậu quả là Y và cần phương án dự phòng Z" | Mọi giả định có rủi ro cao phải được đưa vào danh sách kiểm tra đầu tiên ở bước RRI hoặc bước Build. |

### Luật chống ảo giác (Anti-Hallucination Rule)
Ảo giác nguy hiểm nhất không phải là AI không biết, mà là AI lấy một điều thuộc nhóm `PRIOR` hoặc `ASSUMED` nhưng lại viết bằng ngữ pháp khẳng định chắc nịch của `OBSERVED`. Câu trả lời "Chưa rõ điểm X, cần chạy lệnh Y hoặc hỏi Chủ nhà để xác nhận" luôn được đánh giá cao hơn một câu suy đoán bóng bẩy.

## 2. Vòng lặp Ràng buộc Cơ học (The Constraint Loop)

Khi một yêu cầu đặt ra các ràng buộc có thể kiểm tra cơ học trên bề mặt đầu ra (ví dụ định dạng JSON/YAML nghiêm ngặt, số lượng mục bắt buộc, quy tắc đặt tên, cấm xuất hiện từ khóa hoặc ký tự nhất định, không lộ khóa bí mật), khả năng tự đọc lại bằng mắt của mô hình ngôn ngữ là nơi yếu nhất.

Thợ thi công bắt buộc chạy đủ 5 bước của **Vòng lặp Ràng buộc Cơ học**.

1. **Mở rộng ràng buộc thành bài kiểm tra trước khi viết.** Chuyển hóa yêu cầu thành một câu lệnh hoặc đoạn script kiểm tra tự động. Liệt kê trước các từ vựng hoặc cấu trúc dễ vi phạm nhất để chuẩn bị phương án thay thế.
2. **Viết bản nháp trong không gian làm việc trung gian.** Không xuất thẳng bản nháp chưa kiểm tra thành báo cáo cuối cùng.
3. **Chạy công cụ kiểm tra cơ học.** Dùng lệnh shell, trình phân tích cú pháp (parser), linter hoặc script đếm chính xác trên file vừa tạo. Việc tự đọc lại bằng mắt và tự khen "đã đúng" không được tính là kiểm chứng.
4. **Sửa lỗi và quét lại toàn bộ.** Mỗi khi sửa một vị trí vi phạm, phải chạy lại công cụ kiểm tra trên toàn bộ file vì việc sửa chỗ này có thể vô tình làm hỏng chỗ khác. Lặp lại cho tới khi công cụ trả về `0 vi phạm`.
5. **Bàn giao nguyên vẹn văn bản đã qua kiểm tra.** Mọi chỉnh sửa dù chỉ một dấu câu sau bước 4 đều làm mất hiệu lực kiểm chứng và bắt buộc phải chạy lại bước 3.

## 3. Năm Cấp độ Bằng chứng và Dấu vân tay Cây thư mục (Evidence Hierarchy & Fingerprint)

Không phải mọi câu nói "đã chạy test" đều có giá trị như nhau. Chủ thầu và Trọng tài phân biệt rạch ròi 5 cấp độ bằng chứng từ thấp đến cao.

1. **`static-read` (Đọc tĩnh).** Mới chỉ đọc mã nguồn, kiểm tra cú pháp hoặc chạy trình kiểm tra kiểu tĩnh (typecheck/linter), chưa thực thi mã.
2. **`unit-test` (Kiểm thử đơn vị cô lập).** Chạy các bài test hàm hoặc module cô lập, trong đó các thành phần bên ngoài (cơ sở dữ liệu, mạng) có thể đang được giả lập (mock/stub).
3. **`fixture-replay` (Phát lại trên dữ liệu mẫu cục bộ).** Chạy chương trình với bộ dữ liệu mẫu hoặc bản ghi hội thoại cố định trong môi trường đóng hộp.
4. **`live-run` (Chạy thực tế trên môi trường cục bộ/thử nghiệm).** Khởi động máy chủ, trình duyệt thật, cơ sở dữ liệu thật hoặc công cụ CLI thật và thực hiện luồng thao tác đầu cuối.
5. **`production` (Kiểm chứng trên môi trường vận hành thật).** Đo đạc từ nhật ký vận hành, giám sát sau phát hành (canary) hoặc số liệu người dùng thực tế.

### Quy tắc Cấm Đánh tráo Cấp độ Bằng chứng
Một bài kiểm thử dùng dữ liệu giả lập (`unit-test` có mock) không bao giờ được phép báo cáo là đã kiểm chứng tích hợp thực tế (`live-run`). Nếu thiếu môi trường hoặc thiếu khóa kết nối để chạy `live-run`, Thợ phải ghi rõ cấp độ đạt được là `unit-test` và nêu lý do chưa chạy được `live-run` tại mục `ISSUES`.

### Cách tính và đối chiếu `WTREE_FINGERPRINT`
Để đảm bảo bằng chứng kiểm thử gắn chặt với nội dung mã nguồn thực tế trên đĩa (bất kể đã commit hay chưa), sử dụng lệnh tạo dấu vân tay chuẩn.

```bash
WTREE_FP=$( (git status --porcelain; git diff HEAD 2>/dev/null) | shasum -a 256 | cut -c1-16 )
```

- Khi Thợ chạy xong lệnh kiểm thử cuối cùng, Thợ chụp ngay giá trị `WTREE_FP` và ghi vào `Completion Report`.
- Khi Chủ thầu hoặc Trọng tài nghiệm thu ở Bước 7, họ chạy lại chính câu lệnh trên. Nếu mã băm thu được khớp với mã băm trong báo cáo, bằng chứng đạt hạng **`FRESH`**. Nếu khác nhau, nghĩa là mã nguồn đã bị chạm vào sau khi chạy test, bằng chứng bị đánh dấu là **`STALE`** và bị từ chối nghiệm thu ngay lập tức.
