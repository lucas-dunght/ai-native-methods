#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# AI-Native Methods (2026.10 · Full-Stack 4-Layer) - All-in-One Bootstrap Installer
# Cài đặt trọn bộ 3 Bộ Phương Pháp cốt lõi (kèm Deep Module CLI scripts/*.py)
# vào cả ~/.gemini/config/skills/ và ~/.claude/skills/ + 58 Companion Skills
# + GStack CLI Binaries + Governance Hooks + Unified Search MCP v2.0.
# Cam kết bảo mật: KHÔNG ghi đè file key ~/.mcp_env nếu đã tồn tại.
# ==============================================================================

TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${TOOLS_DIR}/.." && pwd)"

GEMINI_SKILLS_DIR="${HOME}/.gemini/config/skills"
CLAUDE_SKILLS_DIR="${HOME}/.claude/skills"
CLAUDE_HOOKS_LIB="${HOME}/.claude/hooks/lib"
GSTACK_HOOKS_DIR="${HOME}/.gstack/hooks"

echo "=============================================================================="
echo "🚀 [AI-Native Methods 2026.10] Bắt đầu kiểm thử & cài đặt trọn bộ Công cụ & Kỹ năng"
echo "=============================================================================="

mkdir -p "${GEMINI_SKILLS_DIR}" "${GEMINI_SKILLS_DIR}/bin" "${CLAUDE_SKILLS_DIR}" "${CLAUDE_HOOKS_LIB}" "${GSTACK_HOOKS_DIR}"

# 0. Cổng Kiểm thử Sống (Live Self-Test & Constraint Loop Gate)
echo "🧪 [0/5] Chạy cổng kiểm thử tự thân (--self-test) cho cả 3 Bộ Kỹ năng..."
chmod +x "${REPO_ROOT}/Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py"
chmod +x "${REPO_ROOT}/Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py"
chmod +x "${REPO_ROOT}/Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py"
chmod +x "${REPO_ROOT}/Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py"

python3 "${REPO_ROOT}/Bo-01-Tinh-Loc-Thong-Tin-Internet/scripts/bo01_refine_tool.py" --self-test --json >/dev/null
python3 "${REPO_ROOT}/Bo-02-Kernel-Registry-SOT/scripts/bo02_registry_tool.py" --self-test --json >/dev/null
python3 "${REPO_ROOT}/Bo-02-Kernel-Registry-SOT/scripts/eval_l2.py" --self-test --json >/dev/null
python3 "${REPO_ROOT}/Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py" --self-test --json >/dev/null
python3 "${REPO_ROOT}/Bo-03-Vibecode-Kit-v6/scripts/bo03_vibecode_tool.py" constraint-check \
  --paths "${REPO_ROOT}/Bo-01-Tinh-Loc-Thong-Tin-Internet" "${REPO_ROOT}/Bo-02-Kernel-Registry-SOT" "${REPO_ROOT}/Bo-03-Vibecode-Kit-v6" --json >/dev/null
echo "   ✓ Cả 3 CLI Tools (bo01, bo02/eval_l2, bo03) & Constraint Loop đều đạt PASS 100%."

# 1. Cài đặt 3 Bộ Phương Pháp Cốt Lõi (Core Suites) vào cả Gemini và Claude Code
echo "📦 [1/5] Đồng bộ 3 Bộ Phương Pháp Cốt Lõi (Full-Stack 4 Lớp) vào Gemini & Claude Code..."
for host_dir in "${GEMINI_SKILLS_DIR}" "${CLAUDE_SKILLS_DIR}"; do
  rm -rf "${host_dir}/internet-info-refinement" "${host_dir}/kernel-registry-sot" "${host_dir}/vibecode-kit-v6"
  cp -R "${REPO_ROOT}/Bo-01-Tinh-Loc-Thong-Tin-Internet" "${host_dir}/internet-info-refinement"
  cp -R "${REPO_ROOT}/Bo-02-Kernel-Registry-SOT" "${host_dir}/kernel-registry-sot"
  cp -R "${REPO_ROOT}/Bo-03-Vibecode-Kit-v6" "${host_dir}/vibecode-kit-v6"
  chmod +x "${host_dir}/internet-info-refinement/scripts/"*.py
  chmod +x "${host_dir}/kernel-registry-sot/scripts/"*.py
  chmod +x "${host_dir}/vibecode-kit-v6/scripts/"*.py
done

# 2. Cài đặt 58 Companion Skills (Tavily + AgentKit + GStack)
echo "🧰 [2/5] Cài đặt 58 Companion Skills (Tavily, AgentKit, GStack) vào ${GEMINI_SKILLS_DIR}..."
for group in tavily akkit gstack; do
  group_path="${TOOLS_DIR}/skills/${group}"
  if [ -d "${group_path}" ]; then
    for skill_path in "${group_path}"/*; do
      [ -d "${skill_path}" ] || continue
      skill_name="$(basename "${skill_path}")"
      target="${GEMINI_SKILLS_DIR}/${skill_name}"
      if [ ! -e "${target}" ]; then
        cp -R "${skill_path}" "${target}"
      fi
    done
  fi
done

# 3. Cài đặt GStack CLI Binaries, Libs & Post-Upgrade Hook
echo "⚙️  [3/5] Cài đặt GStack CLI Binaries (gstack-wtree, gstack-evidence, ...), Libs và Hooks..."
if [ -d "${TOOLS_DIR}/lib" ]; then
  mkdir -p "${GEMINI_SKILLS_DIR}/lib"
  cp -R "${TOOLS_DIR}/lib/"* "${GEMINI_SKILLS_DIR}/lib/"
fi
for bin_file in "${TOOLS_DIR}/gstack-bin"/*; do
  [ -f "${bin_file}" ] || continue
  bname="$(basename "${bin_file}")"
  if [ "${bname}" = "post-upgrade-antigravity.sh" ]; then
    cp "${bin_file}" "${GSTACK_HOOKS_DIR}/post-upgrade-antigravity.sh"
    chmod +x "${GSTACK_HOOKS_DIR}/post-upgrade-antigravity.sh"
  else
    cp "${bin_file}" "${GEMINI_SKILLS_DIR}/bin/${bname}"
    chmod +x "${GEMINI_SKILLS_DIR}/bin/${bname}"
  fi
done

# 4. Cài đặt Governance & PR Contract Hooks
echo "🛡️  [4/5] Cài đặt Governance Hooks (pr-body-contract.cjs, writing-language.cjs, ...)..."
for hook_file in "${TOOLS_DIR}/hooks"/*.cjs; do
  [ -f "${hook_file}" ] || continue
  hname="$(basename "${hook_file}")"
  cp "${hook_file}" "${CLAUDE_HOOKS_LIB}/${hname}"
  chmod +x "${CLAUDE_HOOKS_LIB}/${hname}"
done

# 5. Cài đặt Unified Search Pool MCP v2.0
echo "🔍 [5/5] Khởi tạo môi trường Unified Search Pool MCP v2.0..."
chmod +x "${TOOLS_DIR}/unified-search-mcp/scripts/setup_env.sh"
chmod +x "${TOOLS_DIR}/unified-search-mcp/scripts/search_pool.py"
"${TOOLS_DIR}/unified-search-mcp/scripts/setup_env.sh"

echo ""
echo "=============================================================================="
echo "✅ HOÀN TẤT! Toàn bộ 3 Bộ Phương Pháp (4 Lớp) + 58 Skills + MCP + Hooks đã sẵn sàng."
echo "👉 Bước tiếp theo: Mở file ~/.mcp_env để điền API Key của bạn (nếu chưa điền)."
echo "=============================================================================="
