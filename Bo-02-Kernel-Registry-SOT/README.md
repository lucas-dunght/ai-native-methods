# Bộ 02 · Kernel Registry và Nguồn Sự Thật Đa Xuất Xứ

**Phiên bản 2026.10 (v2.0)**

Khung tổ chức tri thức của một tổ chức hoặc dự án theo bốn xuất xứ độc lập gồm Sự thật lưu sẵn (`L1`), Sự thật dẫn xuất (`L2`), Nghĩa vụ rút từ văn bản pháp quy (`L3`) và Phán xét phong cách tự do (`L4`). Mỗi xuất xứ có chế độ kiểm chứng riêng và lưu trong kho riêng, ngăn chặn triệt để tình trạng một sổ cái duy nhất chồng lấn mọi loại tri thức và gây sai lệch khi AI Agent truy vấn.

Phiên bản **v2.0 (2026.10)** tích hợp cơ chế kiểm toán độ tươi bằng mã băm (`FRESH / STALE / EXPIRED`), bộ tính công thức `L2` tất định bằng mã thực thi (`Deterministic L2 Evaluator`), phân tầng chỉ mục từ `dependency-index.csv` lên đồ thị tri thức (`ak-graphify`) và bộ nhớ đồng bộ (`gstack /sync-gbrain` kèm kiểm toán rò rỉ dữ liệu `--audit`), cổng duyệt di trú qua thẻ quyết định `Decision Brief D<N>`, khóa phạm vi chỉ sao chép (`Copy-Only Scope Freeze`) và cầu nối liên thông tự động giữa Bộ 01, Bộ 02 và Bộ 03.

## Khi nào dùng

Sinh viên, kỹ sư hoặc tổ chức cần thiết lập một hệ thống tri thức nội bộ chuẩn hóa cho AI Agent và con người cùng truy cập trong các tình huống điển hình.

Thiết lập hệ thống quản trị tri thức cho một phòng ban, doanh nghiệp hoặc dự án khởi nghiệp. Xây dựng trợ lý AI nội bộ truy cập đúng nguồn sự thật mà không bịa số liệu. Tổ chức lại các bảng giá, định mức nguyên vật liệu (`BOM`), ma trận năng lực, văn bản pháp quy và sổ tay thương hiệu đang nằm phân tán. Đồ án tốt nghiệp hoặc luận văn về kiến trúc dữ liệu và hệ thống AI doanh nghiệp (`Enterprise AI Architecture`).

## Khi nào không dùng

Khi dữ liệu thuần túy là bảng nhật ký sự kiện thô (`raw event logs`) phục vụ phân tích thống kê mà chưa cần lớp ngữ nghĩa nghiệp vụ. Khi nhóm làm việc quá nhỏ và không có tri thức lặp lại cần tái sử dụng. Khi tổ chức đã có sẵn một hệ thống quản trị nguồn sự thật tách lớp đang vận hành ổn định với bằng chứng kiểm toán rõ ràng.

## Đặc điểm cốt lõi của bản v2.0 (2026.10)

Khác biệt hoàn toàn với cách tiếp cận "nhồi mọi tài liệu vào một Vector DB hoặc một Wiki duy nhất" ở sáu điểm cốt lõi.

Một, **Phân tách bốn xuất xứ (`L1`, `L2`, `L3`, `L4`) vào ba kho độc lập**. Không bao giờ trộn dữ liệu định lượng cứng (`L1`, `L2`) với nghĩa vụ pháp quy (`L3`) và phong cách diễn đạt (`L4`).

Hai, **Kiểm toán độ tươi bằng mã băm (`Staleness & Content-Hash Audit`) và Bộ tính `L2` tất định**. Mỗi mục `L1` và `L3` lưu mã băm `source_hash` của tài liệu gốc và trạng thái `verification_status: FRESH | STALE | EXPIRED`. Khi tài liệu gốc thay đổi hoặc hết hạn, mọi công thức `L2` và `Skill` phụ thuộc tự động chuyển sang `STALE`. Giá trị `L2` luôn được tính bằng script cơ học kèm dấu vết `audit_trace`, tuyệt đối không để AI tính nhẩm.

Ba, **Chỉ cấu trúc hóa phần có giá trị cao và Mở rộng chỉ mục phân tầng (`Tiered Hybrid Indexing`)**. Không nguyên tử hóa máy móc mọi văn bản. Với kho dưới 500 thành phần, chỉ dùng một bảng `dependency-index.csv` gọn nhẹ. Khi quy mô vượt 500 thành phần hoặc cần truy vấn liên kết sâu giữa mã nguồn và tài liệu, nâng cấp mượt mà lên đồ thị `ak-graphify` (gắn nhãn cạnh `EXTRACTED`, `INFERRED`, `AMBIGUOUS`) và đồng bộ qua `gstack /sync-gbrain` có kiểm soát quyền riêng tư (`brain_trust_policy`).

Bốn, **Phân loại quyết định 3 tầng và Cổng duyệt `Decision Brief D<N>`**. Mọi xung đột số liệu ở Phase 3 hoặc đề xuất cây thư mục di trú ở Phase 4 đều được trình cho con người qua thẻ `D<N>` (gồm giải thích `ELI10`, rủi ro `Stakes`, điểm `Completeness X/10` và phương án khuyến nghị).

Năm, **Khóa phạm vi chỉ sao chép (`Copy-Only Scope Freeze`)**. Ở Phase 5, Agent chỉ được phép dựng cấu trúc mới bằng cách sao chép, đồng thời chụp mã băm cây thư mục gốc trước và sau khi chạy để chứng minh cơ học rằng `0` file gốc bị xóa hay ghi đè.

Sáu, **Đường ống liên thông 3 Bộ (`Bộ 01 -> Bộ 02 -> Bộ 03`) và Cầu nối `Feature Map` (`pstack`)**. Nhận trực tiếp các `Fact Cards` hạng `verified` từ Bộ 01 làm đầu vào `L1`, cung cấp các mã định danh con trỏ (`[L1-...]`, `[L2-...]`, `[L3-...]`, `[L4-...]`) cho các `TIP` và `Blueprint` của Bộ 03 (`Vibecode Kit v6.2 × pstack`), đồng thời đối chiếu mã băm SHA-256 với bản đồ tính năng `references/features/README.md` (`Feature Map`) thông qua quy trình bảo trì định kỳ `/maintain-verification-skill` để ngăn chặn hiện tượng trôi lệch (`drift`) giữa tài liệu và mã nguồn thực tế.

## Cấu trúc thư mục

```
Bo-02-Kernel-Registry-SOT/
├── README.md                                  (file này)
├── Methodology.md                             Triết lý 4 xuất xứ, 5 phase v2.0 và kiểm toán độ tươi
├── Architecture.md                            Kiến trúc 3 kho, bộ tính L2, phân tầng Graphify/GBrain và cầu nối 3 Bộ
├── SKILL.md                                   Đặc tả skill v2.0.0 cài đặt cho AI Agent
├── Quick-Start.md                             Thiết lập Kernel Registry v2.0 đầu tiên trong 15 phút
├── templates/
│   ├── L1-stored-fact.yaml                    Mẫu sự thật lưu sẵn kèm source_hash và verification_status
│   ├── L2-derived-fact.yaml                   Mẫu sự thật dẫn xuất kèm deterministic_eval_cmd và audit_trace
│   ├── L3-obligation.yaml                     Mẫu nghĩa vụ pháp quy kèm source_hash và compliance_check
│   ├── L4-style.yaml                          Mẫu hồ sơ phong cách đứng ngoài đường kiểm cơ học
│   ├── dependency-index.csv                   Bảng chỉ mục phụ thuộc kèm provenance_tag (EXTRACTED/INFERRED)
│   ├── manifest.csv                           Bảng kiểm kê toàn bộ thành phần kèm trạng thái độ tươi
│   ├── classification-table.csv               Bảng phân loại Phase 2 kèm tầng quyết định 3 mức
│   └── queues-and-migration-map.md            Mẫu hàng đợi xung đột D<N>, hàng đợi chưa phân loại và bản đồ di trú
├── references/
│   ├── freshness-and-deterministic-l2.md      Giao thức kiểm toán độ tươi SHA-256 và bộ tính L2 tất định
│   ├── hybrid-indexing-and-gbrain.md          Giao thức phân tầng CSV, Graphify và đồng bộ GBrain an toàn
│   └── bo01-bo02-bo03-bridge.md               Giao thức liên thông tự động Bộ 01 -> Bộ 02 -> Bộ 03
└── examples/
    └── worked-example.md                      Ví dụ thực chiến end-to-end tái cấu trúc tri thức doanh nghiệp
```

## Bắt đầu nhanh

Đọc `Quick-Start.md` để dựng ngay một `Kernel Registry` v2.0 trong 15 phút trên tập tài liệu mẫu. Tiếp theo đọc `Methodology.md` để nắm rõ lý do tách 4 xuất xứ và quy trình 5 phase. Cuối cùng đọc `Architecture.md` và thư mục `references/` khi cần triển khai kiểm toán tự động hoặc tích hợp với Bộ 01 và Bộ 03.

## Đóng góp

Phương pháp được đúc kết từ thực tiễn thiết kế kiến trúc tri thức cho AI Agent trong môi trường nhiều nguồn sự thật đan xen. Mọi đề xuất cải tiến từ quá trình áp dụng thực tế đều được ghi nhận để hoàn thiện các phiên bản tiếp theo.
