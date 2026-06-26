# Bộ 02 · Kernel Registry và nguồn sự thật

**Phiên bản 2026.06**

Khung tổ chức tri thức của một tổ chức theo bốn xuất xứ. Sự thật lưu sẵn, sự thật dẫn xuất, sự thật rút từ văn bản pháp quy, phán xét tự do. Mỗi xuất xứ có chế độ tin riêng và lưu trong kho riêng. Ngăn tình trạng một sổ cái duy nhất chồng lấn mọi loại tri thức và gây sai khi truy vấn.

## Khi nào dùng

Sinh viên hoặc tổ chức cần thiết lập một hệ thống tri thức nội bộ cho AI agent và con người cùng truy cập, trong các tình huống.

Dự án quản lý tri thức cho một phòng ban hoặc cả tổ chức. Xây assistant AI nội bộ truy cập đúng nguồn sự thật. Tổ chức lại các bảng giá, BOM list, ma trận năng lực, văn bản pháp quy đang phân tán. Project luận văn về knowledge management hoặc enterprise AI architecture.

## Khi nào không dùng

Khi dữ liệu chỉ là raw data analytics chưa cần ngữ nghĩa. Khi tổ chức quá nhỏ dưới 10 người và không có tri thức tái sử dụng đáng kể. Khi đã có một SOT đang hoạt động tốt qua nhiều năm với evidence rõ ràng.

## Đặc điểm cốt lõi

Khác với approach "một SOT duy nhất" thường gặp ở ba điểm.

Một, phân tách bốn xuất xứ rõ ràng. Không trộn dữ liệu cứng với văn bản pháp quy với phán xét voice.

Hai, không atomize mọi thứ. Chỉ structure phần vừa lặp nhiều, vừa deterministic, vừa đắt khi sai.

Ba, ranh giới vai trò giữa agent và human nghiêm ngặt. Agent thi công kiểm kê và phân loại. Human phán xử khi có xung đột canonical fact.

## Cấu trúc thư mục

```
Bo-02-Kernel-Registry-SOT/
├── README.md            (file này)
├── Methodology.md       Triết lý 4 xuất xứ và 5 phase
├── Architecture.md      Kiến trúc 3 kho + dependency index
├── SKILL.md             Đặc tả skill cài đặt
├── Quick-Start.md       Bắt đầu trong 15 phút
├── templates/
│   ├── L1-stored-fact.yaml
│   ├── L2-derived-fact.yaml
│   ├── L3-obligation.yaml
│   ├── L4-style.yaml
│   ├── dependency-index.csv
│   ├── manifest.csv
│   └── classification-table.csv
└── examples/
    └── worked-example.md  (ẩn danh, lĩnh vực tổ chức tổng quát)
```

## Bắt đầu nhanh

Đọc Quick-Start.md để thiết lập kernel registry đầu tiên trong 15 phút trên một tập tài liệu nhỏ. Sau đó đọc Methodology.md để hiểu vì sao bốn xuất xứ được tách như vậy. Cuối cùng đọc Architecture.md để thiết kế registry production-ready.

## Đóng góp

Phương pháp dựa trên kinh nghiệm thực tế tổ chức tri thức trong môi trường có nhiều loại sự thật khác nhau. Sinh viên hoặc giảng viên áp dụng phát hiện vấn đề vui lòng phản hồi để cải thiện phiên bản sau.
