# AI-Native Methods · Ba phương pháp làm việc với AI

![License](https://img.shields.io/badge/license-MIT-black.svg)
![Version](https://img.shields.io/badge/version-2026.10-blue.svg)
![Language](https://img.shields.io/badge/lang-Vietnamese-red.svg)

Bộ tài liệu chuyển giao ba phương pháp làm việc với AI cho sinh viên, giảng viên đại học và các nhóm phát triển sản phẩm. Mọi thương hiệu cụ thể đã được loại bỏ. Mỗi phương pháp đứng độc lập, có thể áp dụng riêng hoặc kết hợp thành một chuỗi liên hoàn.

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

### Bộ 03 · Vibecode Kit v6.1

Khung làm việc để xây sản phẩm phần mềm bằng cách điều phối đội ngũ AI agent. Ba vai trò chính (Chủ thầu, Thợ thi công, Chủ nhà) kết hợp cùng lớp Cố vấn và Trọng tài độc lập (Kongming / Arbiter). Quy trình 8 bước tự co giãn theo phân tầng rủi ro R0 đến R3.

Bản nâng cấp **v6.1 (2026.10)** tích hợp tinh hoa từ hai bộ công cụ `gstack` và `AgentKit (akkit)` gồm kỷ luật nhận định Fable 5.1 (`OBSERVED` / `DERIVED` / `PRIOR` / `ASSUMED`), sổ cái bằng chứng gắn dấu vân tay cây thư mục (`WTREE_FINGERPRINT`), phỏng vấn quyết định `D<N>` chấm điểm độ hoàn thiện (`Completeness X/10`) kèm sổ nợ làm tắt (`Shortcut Debt`), cổng duyệt kế hoạch 4 lăng kính (`CEO -> Design -> DX -> Eng`) và phản biện Red-Team, điều phối đa Thợ cô lập trên `git worktree` với quyền sở hữu file rời nhau (`Disjoint Ownership`), bàn giao chuyển phiên 9 mục có che mật khẩu (`Redacted Handoff`), phát hành hai chặng (`Beta -> Stable`) và thẻ hiệu chỉnh 100 điểm (`Calibration Card`).

Dùng cho đồ án xây ứng dụng, luận văn có deliverable phần mềm, dự án incubator, MVP và đội ngũ kỹ thuật AI-Native.

📂 [`Bo-03-Vibecode-Kit-v6/`](./Bo-03-Vibecode-Kit-v6/)

---

## Cấu trúc mỗi bộ

Mỗi bộ là một thư mục độc lập với cấu trúc nhất quán.

```
Bo-XX-Ten-Phuong-Phap/
├── README.md            Tổng quan ngắn
├── Methodology.md       Triết lý và phương pháp chi tiết
├── Architecture.md      Kiến trúc kỹ thuật và thành phần
├── SKILL.md             Đặc tả skill để cài vào Claude, Antigravity hoặc agent khác
├── Quick-Start.md       Hướng dẫn bắt đầu trong 10 đến 20 phút
├── templates/           Bản mẫu sẵn dùng
├── references/          Tài liệu giao thức chuyên sâu (nạp theo ngữ cảnh)
└── examples/            Ví dụ thực chiến từ đầu đến cuối
```

Ngoài các file markdown, mỗi bộ còn có hai dạng deliverable ở thư mục gốc.

- **File `.docx`** ở root repo. Bản tài liệu cho người đọc, có mục lục tự sinh, mở được trên Word, Pages, Google Docs.
- **File `.skill`** ở root repo. Bản đóng gói zip của `SKILL.md` cùng các thư mục `templates/`, `references/` và `examples/`. Cài vào Claude hoặc hệ thống AI agent bằng cách nạp file vào mục Skills.

---

## Bắt đầu nhanh

### Cho sinh viên và kỹ sư muốn dùng một bộ cụ thể

1. Mở thư mục Bộ tương ứng.
2. Đọc `README.md` trước.
3. Đọc `Quick-Start.md` và chạy thử trong 10 đến 20 phút.
4. Đọc `Methodology.md` để hiểu cơ sở lý luận.
5. Đọc `Architecture.md` và `references/` khi cần tùy biến hoặc mở rộng quy mô.

### Cho giảng viên muốn dùng làm tài liệu môn học

1. Đọc `Methodology.md` của bộ liên quan để đánh giá mức độ phù hợp với học phần.
2. Có thể dùng `Methodology.md` làm sườn bài giảng tuần đầu.
3. Các bản mẫu trong `templates/` và tình huống trong `examples/` dùng làm bài tập thực hành.
4. File `.docx` ở root tiện in ấn hoặc phát trực tiếp cho sinh viên.

### Cho người muốn cài skill vào Claude hoặc Antigravity

1. Tải file `.skill` của bộ liên quan (ví dụ `vibecode-kit-v6.skill`).
2. Trong Claude, mở Settings → Capabilities → Skills và tải file `.skill` lên. Trong Antigravity hoặc Claude Code, giải nén vào thư mục skills cấu hình của hệ thống.
3. Agent sẽ tự đọc phần khai báo frontmatter của `SKILL.md` và kích hoạt đúng quy trình.

---

## Triết lý chung

Ba bộ chia sẻ bốn nguyên tắc nền tảng.

**Một, AI không thay thế phán xét cuối cùng của con người.** Mọi quyết định có hậu quả nghiêm trọng hoặc đi qua cánh cửa một chiều phải có một con người ký nhận trách nhiệm. AI hỗ trợ khảo sát, tổng hợp, đề xuất, phản biện và thi công. Con người chọn hướng và chịu trách nhiệm.

**Hai, mọi khẳng định và báo cáo hoàn thành đều phải có bằng chứng truy ngược được.** Không chấp nhận nguồn thông tin mồ côi (Bộ 01), không trộn lẫn sự thật cứng với phong cách cá nhân (Bộ 02) và không nghiệm thu phần mềm khi thiếu bằng chứng chạy kiểm thử tươi mới gắn với dấu vân tay mã nguồn (Bộ 03 v6.1).

**Ba, không tự xây cái thị trường hoặc kho mã nguồn đã có sẵn.** Trước khi tự dựng quy trình hay viết hàm mới, luôn rà soát bậc thang tái sử dụng từ công cụ sẵn có trong dự án, thư viện chuẩn cho tới các mô hình ngôn ngữ lớn.

**Bốn, dự đoán trước khi làm, hiệu chỉnh sau khi chạy thật.** Mọi can thiệp đáng kể đều có tiêu chí dự đoán trước khi triển khai. Sau mỗi chu kỳ, đo kết quả thực tế và phân bổ sai số để hệ thống liên tục tiến hóa.

---

## Phối hợp ba bộ

Khi thực hiện một dự án nghiên cứu và phát triển sản phẩm hoàn chỉnh, có thể kết hợp cả ba bộ theo trình tự.

```
Bộ 01 (Tinh lọc thông tin từ internet)
   │
   │  Fact cards có nguồn và phân hạng tin cậy
   ▼
Bộ 02 (Kernel Registry SOT)
   │
   │  Tri thức phân lập theo L1, L2, L3, L4
   ▼
Bộ 03 (Vibecode Kit v6.1)
   │
   │  Đội ngũ AI thiết kế, thi công cô lập, chấm chéo và phát hành
   ▼
Deliverable cuối đã kiểm chứng
```

Không bắt buộc dùng cả ba cùng lúc. Mỗi bộ đều có thể vận hành độc lập.

---

## Đối tượng sử dụng

- Sinh viên thạc sĩ và cử nhân năm cuối các ngành Phân tích dữ liệu, Trí tuệ nhân tạo, Khoa học máy tính, Hệ thống thông tin, Kinh tế lượng.
- Giảng viên hướng dẫn đồ án tốt nghiệp và luận văn.
- Nhóm khởi nghiệp và kỹ sư phát triển sản phẩm theo mô hình AI-Native.
- Nghiên cứu sinh áp dụng vào đề tài thực nghiệm cá nhân.

---

## Phiên bản

Phiên bản hiện hành của kho tài liệu là **2026.10** (trong đó Bộ 01 và Bộ 02 ở bản `2026.06`, Bộ 03 được nâng cấp lên **Vibecode Kit v6.1 · 2026.10**). Khi áp dụng vào dự án, vui lòng ghi rõ phiên bản đã sử dụng trong báo cáo để thuận tiện đối chiếu.

---

## Đóng góp

Phương pháp được thiết kế để tiến hóa qua trải nghiệm thực tế. Sinh viên, giảng viên hoặc kỹ sư áp dụng phát hiện vấn đề hoặc đề xuất cải tiến vui lòng mở Issue hoặc Pull Request.

Khi đóng góp, vui lòng tuân thủ ba quy tắc văn phong.
- Không dùng dấu gạch ngang dài (em-dash) trong markdown (thay bằng dấu chấm, dấu phẩy hoặc dấu chấm giữa `·`)
- Không đặt dấu phẩy trước chữ "và"
- Không lạm dụng dấu hai chấm trong câu văn xuôi

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

Khi sử dụng trong báo cáo học thuật hoặc dự án, vui lòng trích dẫn theo mẫu.

```
Nguyễn, C. L. (2026). AI-Native Methods · Ba phương pháp làm việc với AI
(Version 2026.10, Vibecode Kit v6.1) [Computer software]. GitHub.
https://github.com/lucas-dunght/ai-native-methods
```
