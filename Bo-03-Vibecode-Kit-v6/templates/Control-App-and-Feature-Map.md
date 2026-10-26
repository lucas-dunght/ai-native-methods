# Biểu Mẫu Đòn Bẩy Tự Kiểm Chứng (`./bin/control-app`) & Bản Đồ Tính Năng (`Feature Map`)

> **Trụ cột "Build the Lever" & "Materialized Memory" của Vibecode Kit v6.2 (`× pstack @poteto`)**
> Sao chép biểu mẫu này vào dự án của bạn để khởi tạo công cụ CLI `./bin/control-app` (theo 6 tiêu chuẩn *Deep Modules* của John Ousterhout) và bản đồ tra cứu nhanh `references/features/README.md` (`Feature Map`).

---

## Phần 1 · Sáu Tiêu Chuẩn Thiết Kế `./bin/control-app` Cho AI Agent (`Ousterhout Deep Module Checklist`)

Trước khi nghiệm thu công cụ `./bin/control-app` của dự án, hãy đánh dấu xác nhận đủ 6 tiêu chuẩn sau:

- [ ] **1. Dễ ghép nối & Hé lộ chức năng tăng dần (`Composable Subcommands`):** Phân tách thành các lệnh con độc lập (`seed`, `auth`, `flag`, `dom`, `screenshot`, `perf`, `repro`, `doctor`).
- [ ] **2. Bắt buộc có cờ `--dry-run` cho mọi lệnh gây tác dụng phụ:** Mọi thao tác ghi DB, đổi cờ hoặc xóa cache đều kiểm tra `--dry-run` và trả về kế hoạch dự kiến mà không sửa dữ liệu thật.
- [ ] **3. Thông báo lỗi chỉ dẫn hành động (`Actionable Error Messages`):** Khi gặp lỗi, đầu ra JSON luôn có trường `error.root_cause` và trường `error.next_command` chỉ rõ câu lệnh tiếp theo Agent cần chạy.
- [ ] **4. Có `--help` chi tiết và trả kết quả máy đọc được (`--json`):** Mọi subcommand đều hỗ trợ `--help` và xuất JSON chuẩn hóa.
- [ ] **5. Bao phủ trọn vẹn Trải nghiệm Phát triển (`Full DX Coverage`):** Hỗ trợ nạp dữ liệu mẫu (`seed`), giả lập đăng nhập (`auth`), bật/tắt cờ tính năng và nút chuyển `/prototype` (`flag`), chụp cây giao diện (`dom`), chụp ảnh màn hình (`screenshot`) và đo hiệu năng (`perf`).
- [ ] **6. Khép kín vòng lặp tự trị (`Close the Loop`):** Cho phép Agent tự chạy ứng dụng, tự thao tác, tự đọc log/trace và tự chụp bằng chứng mà không cần con người ngồi canh (`babysitting`).

---

## Phần 2 · Khung Script `./bin/control-app` Mẫu (Sẵn Dùng Ngay)

Lưu đoạn mã dưới đây vào `./bin/control-app` và cấp quyền thực thi (`chmod +x ./bin/control-app`):

```bash
#!/usr/bin/env bash
set -euo pipefail

SUBCOMMAND="${1:-help}"
shift || true

DRY_RUN="false"
JSON_OUT="false"
TARGET_ROUTE="/"
USER_ROLE="member"
FLAG_KV=""

# Support nested noun-verb aliases (e.g. 'db seed', 'auth impersonate', 'ui snapshot')
if [[ "$SUBCOMMAND" == "db" && "${1:-}" == "seed" ]]; then SUBCOMMAND="seed"; shift; fi
if [[ "$SUBCOMMAND" == "auth" && "${1:-}" == "impersonate" ]]; then SUBCOMMAND="auth"; shift; fi
if [[ "$SUBCOMMAND" == "ui" && "${1:-}" == "snapshot" ]]; then SUBCOMMAND="dom"; shift; fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN="true"; shift ;;
    --json) JSON_OUT="true"; shift ;;
    --route) TARGET_ROUTE="${2:-/}"; shift $(( $# >= 2 ? 2 : 1 )) ;;
    --role) USER_ROLE="${2:-}"; shift $(( $# >= 2 ? 2 : 1 )) ;;
    --set) FLAG_KV="${2:-}"; shift $(( $# >= 2 ? 2 : 1 )) ;;
    --help|-h) SUBCOMMAND="help"; shift ;;
    *) shift ;;
  esac
done

emit_error() {
  local code="$1"
  local cause="$2"
  local next_cmd="$3"
  printf '{"ok":false,"subcommand":"%s","dry_run":%s,"error":{"code":"%s","root_cause":"%s","next_command":"%s"}}\n' \
    "$SUBCOMMAND" "$DRY_RUN" "$code" "$cause" "$next_cmd"
  exit 1
}

case "$SUBCOMMAND" in
  help|--help|-h)
    cat << 'EOF'
Usage: ./bin/control-app <subcommand> [options]

Subcommands (Progressive Disclosure):
  seed        Seed deterministic test database state (requires --dry-run check)
  auth        Mint mock auth session for a test user role (--role admin|member|guest)
  flag        Toggle in-session feature flag or /prototype switcher (--set key=value)
  dom         Capture compact DOM / Accessibility tree snapshot (--route /path)
  screenshot  Capture headless browser screenshot proof (--route /path)
  perf        Measure route latency and query count (--route /path)
  doctor      Verify all routes in references/features/README.md (Feature Map)

Global Options:
  --dry-run   Preview side effects without mutating state
  --json      Emit machine-readable JSON output
  --help      Show detailed usage guide
EOF
    ;;
  seed)
    if [[ "$DRY_RUN" == "true" ]]; then
      printf '{"ok":true,"subcommand":"seed","dry_run":true,"planned_action":"Reset test DB schema and load fixtures/standard.sql"}\n'
      exit 0
    fi
    printf '{"ok":true,"subcommand":"seed","dry_run":false,"seeded_records":42,"artifact":".tmp/seed-receipt.json"}\n'
    ;;
  auth)
    if [[ -z "$USER_ROLE" ]]; then
      emit_error "MISSING_ROLE" "Role argument is empty" "./bin/control-app auth --role member --json"
    fi
    printf '{"ok":true,"subcommand":"auth","dry_run":%s,"role":"%s","session_file":".tmp/session-%s.json"}\n' \
      "$DRY_RUN" "$USER_ROLE" "$USER_ROLE"
    ;;
  flag)
    if [[ -z "$FLAG_KV" ]]; then
      emit_error "MISSING_FLAG_KV" "No key=value pair passed to --set" "./bin/control-app flag --set proto_variant=B --dry-run --json"
    fi
    printf '{"ok":true,"subcommand":"flag","dry_run":%s,"flag":"%s"}\n' "$DRY_RUN" "$FLAG_KV"
    ;;
  dom|screenshot|perf)
    printf '{"ok":true,"subcommand":"%s","route":"%s","dry_run":%s,"artifact":".tmp/artifacts/%s.json"}\n' \
      "$SUBCOMMAND" "$TARGET_ROUTE" "$DRY_RUN" "$SUBCOMMAND"
    ;;
  doctor)
    if [[ ! -f "references/features/README.md" ]]; then
      emit_error "FEATURE_MAP_MISSING" "File references/features/README.md does not exist yet" "mkdir -p references/features && cp templates/Control-App-and-Feature-Map.md references/features/README.md"
    fi
    printf '{"ok":true,"subcommand":"doctor","feature_map":"references/features/README.md","drift_detected":false}\n'
    ;;
  *)
    emit_error "UNKNOWN_SUBCOMMAND" "Subcommand '$SUBCOMMAND' is not supported" "./bin/control-app --help"
    ;;
esac
```

---

## Phần 3 · Biểu Mẫu Bản Đồ Tính Năng (`Feature Map` · Đặt tại `references/features/README.md`)

> **Nguyên lý "Materialized Memory":** Codebase là nguồn chân lý tối thượng, còn `Feature Map` là bản nén tiết kiệm token của codebase từ góc nhìn người dùng. Agent luôn đọc bảng này đầu tiên ở Bước 1 (`SCAN`).

| Mã Tính năng (`Feature ID`) | Tên Tính năng & Mục đích từ Góc nhìn Người dùng | Đường dẫn (`Route / Entrypoint`) | Tệp Nguồn Chính (`Primary Source Files`) | Lệnh Chạm & Kiểm Chứng Sống (`./bin/control-app Command`) | Mã băm SHA-256 (`Source Hash`) |
|---|---|---|---|---|---|
| `FEAT-01` | **Đăng nhập & Phiên làm việc:** Xác thực người dùng và cấp phát token phiên. | `POST /api/auth/login`<br/>`GET /login` | `src/auth/login.ts`<br/>`src/pages/Login.tsx` | `./bin/control-app auth --role member --json`<br/>`./bin/control-app dom --route /login --json` | `e3b0c44298fc...` |
| `FEAT-02` | **Quản lý & Hủy Đơn hàng:** Xem chi tiết đơn hàng và cho phép khách tự hủy khi ở trạng thái `PENDING` hoặc `PAID`. | `POST /api/orders/:id/cancel`<br/>`GET /orders/:id` | `src/orders/cancel-order.ts`<br/>`src/pages/OrderDetail.tsx` | `./bin/control-app seed --dry-run --json`<br/>`./bin/control-app screenshot --route /orders/ORD-01 --json` | `9f86d081884c...` |
| `FEAT-03` | **[Điền mã tính năng mới]** | `[Điền URL / Route / CLI]` | `[Điền đường dẫn file:line]` | `./bin/control-app dom --route [path] --json` | `[Điền 12 ký tự đầu SHA-256]` |

---

## Phần 4 · Quy Trình Bảo Trì Hàng Ngày (`/maintain-verification-skill`)

Để `Feature Map` (`references/features/README.md`) không bị trôi (`drift`) so với code thật, chạy quy trình bảo trì sau đây mỗi ngày hoặc ngay ở Bước 8 (`SHIP`) sau khi merge PR:

1. **Quét các tệp định tuyến và tính năng vừa thay đổi:**
   ```bash
   git diff --name-only HEAD~1 HEAD
   ```
2. **Cập nhật mã băm SHA-256 của từng tệp nguồn chính trong `references/features/README.md`:**
   ```bash
   shasum -a 256 src/orders/cancel-order.ts | cut -c1-12
   ```
3. **Chạy kiểm tra sức khỏe toàn diện qua `./bin/control-app doctor`:**
   ```bash
   ./bin/control-app doctor --json
   ```
4. **Xác nhận `drift_detected: false`** và lưu vết vào Sổ cái Nguồn Sự Thật (Bộ 02 · `Kernel Registry SOT`).
