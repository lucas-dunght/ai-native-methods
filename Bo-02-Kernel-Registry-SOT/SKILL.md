---
name: kernel-registry-sot
description: Tổ chức tri thức theo bốn xuất xứ L1 L2 L3 L4 với ba kho registry, obligations, style. Use when reorganizing scattered organizational knowledge, setting up internal knowledge base for AI agent, building enterprise SOT, or refactoring single-SOT into properly classified stores. Triggers on requests like "tổ chức lại tri thức", "xây kernel registry", "thiết lập SOT", "refactor knowledge base", "phân loại tài liệu nội bộ", "tổ chức bảng giá BOM văn bản pháp quy". Do NOT trigger for raw data analytics without semantic structure or for organizations under 10 people without meaningful knowledge reuse.
license: MIT
---

# Kernel Registry SOT Skill

## Mục đích

Skill này hướng dẫn agent đi qua năm phase của phương pháp Kernel Registry để tổ chức lại tri thức của một tổ chức theo bốn xuất xứ L1 L2 L3 L4. Agent thi công kiểm kê và phân loại. Human phán xử khi có xung đột.

## Khi nào kích hoạt

Trigger trên các yêu cầu user.

- "Giúp tôi tổ chức lại folder tri thức nội bộ X"
- "Thiết lập SOT cho doanh nghiệp Y"
- "Xây kernel registry cho dự án Z"
- "Refactor knowledge base hiện tại"
- "Phân loại bảng giá, BOM, văn bản pháp quy, voice"

Không trigger khi.

- Tri thức chỉ là raw data analytics chưa cần ngữ nghĩa
- Tổ chức quá nhỏ và không có tri thức tái sử dụng
- Đã có SOT hoạt động tốt qua nhiều năm

## Bốn xuất xứ

### L1 · Sự thật lưu sẵn

Giá, BOM, định mức, part number, ma trận năng lực, điều khoản hợp đồng cứng. Đo được, deterministic. Lưu key-value có kiểu, có ID, có nguồn.

### L2 · Sự thật dẫn xuất

Tổng dự toán, doanh thu kế hoạch. Tính từ L1 bằng công thức. Lưu công thức và inputs, không lưu giá trị.

### L3 · Sinh có ràng buộc

Nghĩa vụ rút từ văn bản pháp quy. Mỗi nghĩa vụ có ID, mô tả, link tới điều khoản gốc.

### L4 · Phán xét tự do

Voice CEO, phong cách, taste. Đứng NGOÀI đường kiểm. Lưu trong kho riêng, không trộn với registry.

## Quy trình thực hiện

Agent đi qua năm phase theo thứ tự.

### Phase 1 · Kiểm kê

Hỏi user các thư mục cần khảo sát. Duyệt mọi file, lập manifest đầy đủ.

```csv
component_id,component_type,path,domain,date_added,date_updated,status
```

Chưa di chuyển gì hết. Chỉ đọc và ghi.

CRITICAL. Nếu phạm vi thư mục không rõ, hỏi user trước. Không tự đoán.

### Phase 2 · Phân loại

Gán mỗi file (và nơi cần thì mỗi phần trong file) về L1, L2, L3, hay L4. Xuất bảng phân loại. File không chắc thì đánh dấu, không đoán.

```csv
file_path,classified_as,confidence,reason,notes
```

`confidence` thuộc {high, medium, low}. File `low` confidence đẩy vào unclassified queue.

### Phase 3 · Phát hiện xung đột và lỗ hổng

Phase có giá trị nhất. Tìm và nêu ra, không tự sửa.

- Bản trùng và mâu thuẫn của cùng sự thật.
- Tham chiếu hết hiệu lực.
- Sự thật được nhắc nhưng không tồn tại.
- Skills có nghĩa vụ chồng lấn.

Tất cả đẩy vào conflict queue và gap checklist.

CRITICAL. Agent KHÔNG tự chọn cái nào canonical. Đẩy lên user.

### Phase 4 · Đề xuất cấu trúc đích và migration map

Đề xuất cây thư mục mới theo ba kho cộng skills cộng dependency index. Kèm map từ đâu sang đâu cho mỗi file.

DỪNG LẠI Ở ĐÂY. Chờ user duyệt trước khi đụng vào cấu trúc.

### Phase 5 · Thực thi sau khi user duyệt

Chỉ sau khi user đồng ý. Dựng cấu trúc mới bằng cách SAO CHÉP. Không xoá, không di chuyển phá bản gốc. Gán ID. Sinh dependency index. Xuất completion report.

## Ranh giới vai trò

Agent làm.

- Kiểm kê toàn bộ thư mục
- Phân loại sơ bộ theo L1 L2 L3 L4
- Phát hiện trùng lặp và xung đột
- Đề xuất cấu trúc đích
- Dựng cấu trúc bằng sao chép sau khi user duyệt
- Sinh dependency index

Agent KHÔNG làm.

- Tự quyết canonical fact khi xung đột
- Tự đoán phân loại khi không chắc
- Xoá hoặc ghi đè file
- Di chuyển phá bản gốc
- Atomize mọi tài liệu một cách máy móc
- Trộn L4 vào registry
- Build graph database

## Forcing functions

Năm cơ chế cứng.

1. Không xoá file. Không ghi đè. Chỉ sao chép.
2. Không tự chọn canonical khi xung đột.
3. Không atomize mọi thứ. Chỉ phần lặp nhiều, deterministic, đắt khi sai.
4. Không build graph DB. Một dependency index CSV là đủ.
5. Không gộp style L4 vào registry L1 L2.

## Selectivity nước đi đầu

Kiểm kê làm trên toàn bộ. Restructure ở phase 4 ưu tiên cụm giá trị cao nhất trước.

Cụm giá trị cao nhất thường là registry cho nhóm con số (L1 và L2). Chứng minh cụm này gọn gàng trước. Các cụm khác làm thành các lô sau.

## Templates

Templates đi kèm trong `templates/`.
- `L1-stored-fact.yaml`
- `L2-derived-fact.yaml`
- `L3-obligation.yaml`
- `L4-style.yaml`
- `dependency-index.csv`
- `manifest.csv`
- `classification-table.csv`
- `conflict-queue.md`

## Anti-pattern cần tránh

- Một SOT duy nhất chồng lấn mọi loại tri thức.
- Atomize mọi tài liệu thành câu nhỏ nhất.
- Agent tự quyết canonical khi conflict.
- Trộn voice L4 vào registry.
- Build graph database trước.
- Skip phase 3 (phát hiện xung đột).

## Đo lường thành công

- Tỷ lệ truy vấn AI agent về registry trả đúng giá trị >= 95%
- Khi L1 thay đổi, trace ngược các thành phần phụ thuộc dễ qua dependency index
- Conflict queue được clear định kỳ, không tích đọng
- Skill chỉ chứa pointer ID, không lặp nội dung từ registry
