# Trung Tâm Tài Liệu Kỹ Thuật · `AI-Native Methods` & Hệ Sinh Thái `tools/` (`2026.10`)

Thư mục `docs/` cung cấp bộ tài liệu hướng dẫn toàn diện cho hệ sinh thái công cụ, kỹ năng phụ trợ (`Companion Skills`) và cấu hình API Key Pool được đóng gói trong [`tools/`](../tools/README.md), tổ chức theo chuẩn **Diataxis 4 góc nhìn**.

---

## 1. Bản Đồ Tài Liệu Theo Chuẩn Diataxis

| Góc nhìn Diataxis | Tài liệu | Dành cho ai & Khi nào cần đọc |
|---|---|---|
| **1. Bài học thực hành (`Tutorial`)** | [tutorial-first-15-minutes-with-tools.md](./tutorial-first-15-minutes-with-tools.md) | **Người mới bắt đầu.** Hướng dẫn từng bước từ lúc `git clone` đến khi chạy `./tools/install-all.sh`, nạp khóa API đầu tiên và thấy kết quả định tuyến đa tín hiệu hoạt động trong 3 bước. |
| **2. Sổ tay thao tác (`How-To`)** | [how-to-configure-and-extend-api-tools.md](./how-to-configure-and-extend-api-tools.md) | **Kỹ sư & Người vận hành.** Hướng dẫn cách đăng ký và thêm nhiều khóa (`TAVILY_KEY_POOL`, `EXA_KEY_POOL`, `LINKUP_KEY_POOL`) vào `~/.mcp_env`, cách cấu hình `tavily-cli` / `gbrain`, cách kết nối MCP vào 7 AI Client và **cách viết code tích hợp thêm nhà cung cấp API mới vào `search_pool.py`**. |
| **3. Tham chiếu kỹ thuật (`Reference`)** | [reference-tools-and-api-config.md](./reference-tools-and-api-config.md) | **Lập trình viên tra cứu thông số.** Bảng mô tả chính xác 100% biến môi trường, hằng số `COOLDOWN_*`, chữ ký 3 hàm MCP (`web_search`, `web_extract`, `pool_status`), 21 tiện ích `gstack-bin`, 13 `hooks` và 58 kỹ năng phụ trợ. |
| **4. Giải thích kiến trúc (`Explanation`)** | [explanation-multi-signal-router-and-key-pool.md](./explanation-multi-signal-router-and-key-pool.md) | **Kiến trúc sư hệ thống & Giảng viên.** Giải thích lý do thiết kế chấm điểm đa tín hiệu chống bắt nhầm (`Anti-Hijacking`), xoay vòng khóa 2 tầng, cơ chế nhảy nhanh `HTTP 204` và băm một chiều `sha256(key)[:16]` để bảo vệ khóa trên ổ cứng. |

---

## 2. Liên Kết Nhanh Tới 3 Bộ Phương Pháp Cốt Lõi

- **Bộ 01 · Tinh Lọc Thông Tin Internet (v2.0):** [`../Bo-01-Tinh-Loc-Thong-Tin-Internet/README.md`](../Bo-01-Tinh-Loc-Thong-Tin-Internet/README.md)
- **Bộ 02 · Kernel Registry & Nguồn Sự Thật (v2.0):** [`../Bo-02-Kernel-Registry-SOT/README.md`](../Bo-02-Kernel-Registry-SOT/README.md)
- **Bộ 03 · Vibecode Kit (v6.1):** [`../Bo-03-Vibecode-Kit-v6/README.md`](../Bo-03-Vibecode-Kit-v6/README.md)
- **Tổng quan Thư mục Công cụ (`tools/`):** [`../tools/README.md`](../tools/README.md)
