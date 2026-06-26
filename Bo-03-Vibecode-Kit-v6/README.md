# Bộ 03 · Vibecode Kit v6

**Phiên bản 2026.06**

Khung làm việc để xây sản phẩm phần mềm hoặc giải pháp số bằng cách điều phối AI agent thay vì viết code thủ công. Ba vai trò rõ ràng, quy trình tự co giãn theo độ phức tạp tác vụ, chu trình thẻ dự đoán và hiệu chỉnh. Phù hợp với sinh viên có thể chưa thuần thục một ngôn ngữ lập trình cụ thể nhưng có khả năng phân tích vấn đề và phán xử.

## Khi nào dùng

Sinh viên hoặc tổ chức muốn xây phần mềm hoặc giải pháp số trong các tình huống.

Đồ án tốt nghiệp xây ứng dụng web, mobile, hoặc CLI. Luận văn thạc sĩ có deliverable là một hệ thống chạy được. Dự án incubator hoặc lab có sản phẩm demo. Cá nhân muốn build tool cá nhân không cần background lập trình sâu. Nhóm khởi nghiệp muốn ship MVP nhanh.

## Khi nào không dùng

Khi yêu cầu là code production-grade cho hệ thống nghiêm trọng (banking, healthcare, aviation) cần engineer review chuyên sâu. Khi sinh viên có mục tiêu học một ngôn ngữ lập trình cụ thể đến mức chuyên sâu. Khi domain quá narrow và AI training data không có (ví dụ embedded systems custom firmware).

## Đặc điểm cốt lõi

Khác với approach "chỉ dùng ChatGPT để viết code" ở năm điểm.

Một, có ba vai trò rõ ràng (Chủ thầu, Thợ thi công, Chủ nhà). Không lẫn vai.

Hai, quy trình tự co giãn theo tier R0 đến R3 của tác vụ. Không áp dụng full pipeline cho task 5 phút.

Ba, có thẻ dự đoán trước khi giao việc cho AI và thẻ hiệu chỉnh sau khi nhận kết quả. Calibration là bắt buộc.

Bốn, blueprint trước build. AI không generate code thẳng từ yêu cầu mơ hồ.

Năm, audit trail loop. Track mọi quyết định để học từ sai số qua các vòng.

## Cấu trúc thư mục

```
Bo-03-Vibecode-Kit-v6/
├── README.md            (file này)
├── Methodology.md       Triết lý 3 vai trò và 8 bước
├── Architecture.md      Kiến trúc kỹ thuật và workflow
├── SKILL.md             Đặc tả skill cài đặt
├── Quick-Start.md       Bắt đầu trong 20 phút
├── templates/
│   ├── TIP-template.md
│   ├── Blueprint-template.md
│   ├── RRI-template.md
│   ├── Completion-Report.md
│   ├── Calibration-Card.md
│   ├── Risk-Tier-Classification.md
│   └── Audit-Trail-Loop.md
└── examples/
    └── worked-example.md  (ẩn danh, web app tổng quát)
```

## Bắt đầu nhanh

Đọc Quick-Start.md để chạy phương pháp lần đầu trên một task vibecode nhỏ trong 20 phút. Sau đó đọc Methodology.md để hiểu ba vai và lý do từng bước. Cuối cùng đọc Architecture.md khi cần customize hoặc scale lên dự án lớn.

## Đóng góp

Phương pháp được thiết kế để tiến hoá. Phiên bản v6 là kết quả của nhiều vòng iterate từ v1 đến v5. Sinh viên hoặc giảng viên áp dụng phát hiện vấn đề vui lòng phản hồi để cải thiện phiên bản v7.
