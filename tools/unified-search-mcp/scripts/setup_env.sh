#!/usr/bin/env bash
set -e

# ==============================================================================
# Unified Search Pool - Cross-Platform Installer & Config Generator (Unix/macOS)
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "🚀 [Unified Search Pool] Đang thiết lập môi trường tại: ${ROOT_DIR}"

# 1. Khởi tạo virtualenv
if [ ! -d "${ROOT_DIR}/.venv" ]; then
    echo "📦 Đang tạo virtualenv tại ${ROOT_DIR}/.venv..."
    if command -v uv &> /dev/null; then
        uv venv "${ROOT_DIR}/.venv"
        uv pip install --python "${ROOT_DIR}/.venv/bin/python" "fastmcp>=0.1.0" "httpx>=0.27.0"
    else
        python3 -m venv "${ROOT_DIR}/.venv"
        "${ROOT_DIR}/.venv/bin/pip" install --upgrade pip
        "${ROOT_DIR}/.venv/bin/pip" install "fastmcp>=0.1.0" "httpx>=0.27.0"
    fi
else
    echo "✅ Virtualenv đã tồn tại."
fi

# 2. Cấp quyền thực thi script
chmod +x "${SCRIPT_DIR}/search_pool.py"

# 3. Tạo file mẫu ~/.mcp_env nếu chưa có
ENV_FILE="${HOME}/.mcp_env"
if [ ! -f "${ENV_FILE}" ]; then
    echo "📝 Đang tạo file cấu hình mẫu tại ${ENV_FILE}..."
    cat << 'EOF' > "${ENV_FILE}"
# --- UNIFIED SEARCH KEY POOL ---
export TAVILY_KEY_POOL=""
export EXA_KEY_POOL=""
export LINKUP_KEY_POOL=""
EOF
    chmod 600 "${ENV_FILE}"
fi

PYTHON_EXE="${ROOT_DIR}/.venv/bin/python"
SEARCH_SCRIPT="${SCRIPT_DIR}/search_pool.py"

echo ""
echo "=============================================================================="
echo "🎉 CÀI ĐẶT THÀNH CÔNG! DƯỚI ĐÂY LÀ ĐOẠN CẤU HÌNH DÀNH RIÊNG CHO MÁY CỦA BẠN:"
echo "=============================================================================="
echo ""
echo "1. Cấu hình JSON (Antigravity Global, Antigravity IDE, Claude Desktop, Cursor):"
echo "------------------------------------------------------------------------------"
cat << EOF
{
  "mcpServers": {
    "unified-search": {
      "command": "${PYTHON_EXE}",
      "args": [
        "${SEARCH_SCRIPT}"
      ]
    }
  }
}
EOF

echo ""
echo "2. Lệnh thêm nhanh cho Claude Code CLI:"
echo "------------------------------------------------------------------------------"
echo "claude mcp add unified-search \"${PYTHON_EXE}\" \"${SEARCH_SCRIPT}\""

echo ""
echo "3. Cấu hình Hermes Agent (~/.hermes/config.yaml):"
echo "------------------------------------------------------------------------------"
cat << EOF
mcp_servers:
  unified-search:
    command: "${PYTHON_EXE}"
    args:
      - "${SEARCH_SCRIPT}"
    env: {}
    timeout: 120
    connect_timeout: 30
EOF

echo ""
echo "4. Cấu hình DeepSeek Harness (~/.dsh/profiles/<profile>/cordis.patch.yml):"
echo "------------------------------------------------------------------------------"
cat << EOF
- id: mcp-unified-search
  name: "@deepseek-ai/dsh-mcp-client"
  config:
    serverName: unified-search
    transport: stdio
    command: "${PYTHON_EXE}"
    args:
      - "${SEARCH_SCRIPT}"
    env: {}
EOF
echo ""
echo "=============================================================================="
