# AI-Native Methods · Ba phương pháp làm việc với AI

![License](https://img.shields.io/badge/license-MIT-black.svg)
![Version](https://img.shields.io/badge/version-2026.06-blue.svg)
![Language](https://img.shields.io/badge/lang-Vietnamese-red.svg)

Bộ tài liệu chuyển giao ba phương pháp làm việc với AI cho sinh viên và giảng viên đại học. Mọi thương hiệu cụ thể đã được loại bỏ. Mỗi phương pháp đứng độc lập, có thể áp riêng hoặc kết hợp.

---

## Tổng quan ba bộ

### Bộ 01 · Phương pháp tinh lọc và làm giàu thông tin từ internet

Khung làm việc đa giai đoạn biến thông tin thô thu thập từ internet thành tri thức có chất lượng kiểm chứng được. Đầu vào là kết quả tìm kiếm hỗn loạn. Đầu ra là tập sự thật có nguồn, có phân hạng tin cậy, không trùng lặp, có đối chiếu chéo.

Dùng cho nghiên cứu thị trường, phân tích đối thủ cạnh tranh, tổng quan tài liệu, due diligence.

📂 [`Bo-01-Tinh-Loc-Thong-Tin-Internet/`](./Bo-01-Tinh-Loc-Thong-Tin-Internet/)

### Bộ 02 · Kernel Registry và nguồn sự thật

Khung tổ chức tri thức theo bốn xuất xứ L1 L2 L3 L4. Sự thật lưu sẵn, sự thật dẫn xuất, sự thật rút từ văn bản pháp quy, phán xét tự do. Mỗi xuất xứ có chế độ tin riêng và lưu trong kho riêng.

Dùng cho quản lý tri thức nội bộ, xây assistant AI nội bộ, refactor knowledge base.

📂 [`Bo-02-Kernel-Registry-SOT/`](./Bo-02-Kernel-Registry-SOT/)

### Bộ 03 · Vibecode Kit v6.0

Khung làm việc để xây sản phẩm phần mềm bằng cách điều phối AI agent. Ba vai trò Chủ thầu, Thợ thi công, Chủ nhà. Workflow 8 bước tự co giãn theo task.

Dùng cho đồ án xây ứng dụng, luận văn có deliverable phần mềm, dự án incubator, MVP.

📂 [`Bo-03-Vibecode-Kit-v6/`](./Bo-03-Vibecode-Kit-v6/)

---

## Cấu trúc mỗi bộ

Mỗi bộ là một thư mục độc lập với cấu trúc nhất quán.

```
Bo-XX-Ten-Phuong-Phap/
├── README.md            Tổng quan ngắn
├── Methodology.md       Triết lý và phương pháp chi tiết
├── Architecture.md      Kiến trúc kỹ thuật và thành phần
├── SKILL.md             Đặc tả skill để cài vào Claude hoặc agent khác
├── Quick-Start.md       Hướng dẫn bắt đầu trong 10 đến 20 phút
└── templates/           Bản mẫu sẵn dùng
```

Ngoài các file markdown, mỗi bộ còn có hai dạng deliverable.

- **File `.docx`** ở root repo. Bản tài liệu cho người đọc, có table of contents tự sinh, mở được trên Word, Pages, Google Docs.
- **File `.skill`** ở root repo. Bản zip của SKILL.md cộng templates folder. Cài vào Claude bằng cách drop file vào Skills section trong Settings.

---

## Bắt đầu nhanh

### Cho sinh viên muốn dùng một bộ cụ thể

1. Mở thư mục Bộ tương ứng.
2. Đọc README.md trước.
3. Đọc Quick-Start.md và chạy thử trong 10-20 phút.
4. Đọc Methodology.md để hiểu cơ sở lý luận.
5. Đọc Architecture.md khi cần customize.

### Cho giảng viên muốn dùng làm tài liệu môn học

1. Đọc Methodology.md của bộ liên quan để đánh giá phù hợp với học phần.
2. Có thể dùng Methodology.md làm slide bài giảng tuần đầu.
3. Templates trong thư mục con dùng làm bài tập thực hành.
4. File `.docx` ở root tiện in phát cho sinh viên.

### Cho người muốn cài skill vào Claude

1. Tải file `.skill` của bộ liên quan.
2. Mở Claude → Settings → Capabilities → Skills.
3. Upload file `.skill`.
4. Claude tự đọc SKILL.md frontmatter và load skill.

---

## Triết lý chung

Ba bộ chia sẻ ba nguyên tắc nền tảng.

**Một, AI không thay thế phán xét cuối cùng.** Mọi quyết định có hậu quả nghiêm trọng phải có một con người ký nhận trách nhiệm. AI hỗ trợ tổng hợp, đề xuất, phân loại. Người commit và chịu trách nhiệm.

**Hai, không tự xây cái thị trường đã commoditize.** Trước khi tự xây pipeline hoặc framework, đánh giá nghiêm túc xem các công cụ sẵn có và mô hình ngôn ngữ lớn có giải được không.

**Ba, dự đoán trước khi ship, hiệu chỉnh sau khi ship.** Mọi can thiệp đáng kể đều phải có thẻ dự đoán trước khi triển khai. Sau cycle, đo kết quả thật và phân bổ sai số cho các loại lỗi.

---

## Phối hợp ba bộ

Khi sinh viên làm một dự án nghiên cứu hoàn chỉnh, có thể dùng cả ba theo trình tự.

```
Bộ 01 (Tinh lọc thông tin)
   │
   │  fact cards có nguồn
   ▼
Bộ 02 (Kernel Registry)
   │
   │  L1 stored facts trong registry
   ▼
Bộ 03 (Vibecode Kit v6)
   │
   │  AI build sản phẩm với context chính xác
   ▼
Deliverable cuối
```

Không bắt buộc dùng cả ba. Mỗi bộ đứng riêng được.

---

## Đối tượng

- Sinh viên thạc sĩ và cử nhân năm cuối ngành Phân tích dữ liệu, AI, Khoa học máy tính, Kinh tế lượng.
- Giảng viên hướng dẫn đồ án và luận văn.
- Cán bộ tổ chức quan tâm đến triển khai AI trong môi trường học thuật.
- Nghiên cứu sinh áp dụng vào đề tài cá nhân.

---

## Phiên bản

Phiên bản hiện hành 2026.06. Mỗi bộ có thể được cập nhật độc lập. Phiên bản ghi trong README mỗi bộ.

Khi áp dụng vào dự án, ghi lại phiên bản đã dùng trong báo cáo dự án để khi có thay đổi sau này còn truy ngược được.

---

## Đóng góp

Phương pháp được thiết kế để tiến hoá theo trải nghiệm thực tế. Sinh viên hoặc giảng viên áp dụng phát hiện vấn đề hoặc đề xuất cải tiến vui lòng mở Issue hoặc Pull Request.

Khi đóng góp, vui lòng tuân thủ ba quy tắc văn phong.
- Không em-dash trong markdown (dùng dấu chấm, dấu phẩy, hoặc khoảng trắng)
- Không dấu phẩy trước "và"
- Không lạm dụng dấu hai chấm

---

## License

[MIT License](./LICENSE)

Copyright © 2026 Nguyễn Cảnh Lâm

---

## Tác giả

**Nguyễn Cảnh Lâm**
Chief AI Officer, Real-time Robotics

📧 nclamvn@gmail.com
🐙 [github.com/nclamvn](https://github.com/nclamvn)

---

## Trích dẫn

Khi sử dụng trong báo cáo học thuật hoặc dự án, vui lòng trích dẫn theo format.

```
Nguyễn, C. L. (2026). AI-Native Methods · Ba phương pháp làm việc với AI
(Version 2026.06) [Computer software]. GitHub.
https://github.com/nclamvn/ai-native-methods
```
