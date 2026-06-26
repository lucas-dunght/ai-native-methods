# Conflict Queue Template

Hàng đợi xung đột giữa các fact cards. Người dùng phán xử, không phải agent.

## Quy tắc

Mỗi entry là một cặp hoặc nhóm cards mâu thuẫn nhau về cùng một sự thật.

Agent KHÔNG được tự chọn cards nào đúng. Agent đẩy thông tin lên cho user quyết định.

User phán xử dựa trên uy tín nguồn, ngày publish, methodology của nghiên cứu gốc, hoặc dựa trên kinh nghiệm domain.

## Format mẫu

### Conflict C-001

**Vấn đề**. Hai cards nói về cùng một sự thật với giá trị khác nhau.

**Card A · F-2026-004**
- Content. Thị trường edtech ĐNA đạt 6.7 tỷ USD trong năm 2023.
- Sources. S001 (báo cáo của hãng tư vấn quốc tế, tier-1)
- Methodology. Khảo sát top 50 doanh nghiệp.
- Date. Báo cáo công bố tháng 3 năm 2024.

**Card B · F-2026-018**
- Content. Thị trường edtech ĐNA đạt 8.2 tỷ USD trong năm 2023.
- Sources. S015 (báo chí kinh tế khu vực, tier-2)
- Methodology. Không rõ.
- Date. Bài viết tháng 6 năm 2024.

**Đề xuất phán xử của agent**.

Card A có nguồn tier-1 cao hơn và có methodology rõ ràng. Card B có nguồn tier-2 và methodology không rõ. Nghiêng về giữ Card A là canonical, đánh dấu Card B là conflict đã giải quyết với nhãn deprecated.

**Quyết định của user**.

[Ghi quyết định cuối ở đây]

- [ ] Giữ Card A, deprecate Card B
- [ ] Giữ Card B, deprecate Card A
- [ ] Giữ cả hai (giá trị khác do methodology khác, ghi rõ trong notes)
- [ ] Reject cả hai (cần thu thêm nguồn primary)
- [ ] Khác. [mô tả]

**Người phán xử**. [Tên]

**Ngày phán xử**. [YYYY-MM-DD]

---

### Conflict C-002

**Vấn đề**. Hai cards mâu thuẫn logic dù không nói cùng một sự thật.

**Card A · F-2026-022**
- Content. Việt Nam có 23 startup edtech được đầu tư từ 2022 đến 2024.

**Card B · F-2026-028**
- Content. Việt Nam có 31 lượt đầu tư edtech từ 2022 đến 2024.

**Mâu thuẫn logic**. Số startup được đầu tư khác với số lượt đầu tư (một startup có thể nhận nhiều vòng). Cần phân biệt rõ.

**Đề xuất phán xử**. Không phải mâu thuẫn thật, là hai metric khác nhau. Edit Card A thành "23 startup unique" và Card B thành "31 lượt deal" để phân biệt rõ. Đánh dấu liên quan trong cross_references.

**Quyết định của user**. [Ghi quyết định cuối ở đây]

---

## Lưu ý

Conflict queue phải được clear hết trước khi xuất báo cáo cuối ở giai đoạn 7.

Cards có liên quan đến conflict chưa giải quyết không được dùng trong báo cáo.

Khi clear, cập nhật field notes của cards liên quan với link đến conflict ID đã được phán xử.

Lưu lại lịch sử conflict trong git để có thể trace ngược khi cần audit research process.
