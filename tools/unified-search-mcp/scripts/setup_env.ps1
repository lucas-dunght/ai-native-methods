# ==============================================================================
# Unified Search Pool - Cross-Platform Installer & Config Generator (Windows)
# ==============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

Write-Host "🚀 [Unified Search Pool] Đang thiết lập môi trường tại: $RootDir" -ForegroundColor Cyan

# 1. Khởi tạo virtualenv
$VenvDir = Join-Path $RootDir ".venv"
$PythonExe = Join-Path $VenvDir "Scripts\python.exe"

if (-not (Test-Path $VenvDir)) {
    Write-Host "📦 Đang tạo virtualenv tại $VenvDir..." -ForegroundColor Yellow
    python -m venv $VenvDir
    & $PythonExe -m pip install --upgrade pip
    & $PythonExe -m pip install "fastmcp>=0.1.0" "httpx>=0.27.0"
} else {
    Write-Host "✅ Virtualenv đã tồn tại." -ForegroundColor Green
}

# 2. Tạo file mẫu .mcp_env nếu chưa có
$EnvFile = Join-Path $env:USERPROFILE ".mcp_env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "📝 Đang tạo file cấu hình mẫu tại $EnvFile..." -ForegroundColor Yellow
    @"
# --- UNIFIED SEARCH KEY POOL ---
export TAVILY_KEY_POOL=""
export EXA_KEY_POOL=""
export LINKUP_KEY_POOL=""
"@ | Out-File -FilePath $EnvFile -Encoding utf8
}

$SearchScript = Join-Path $ScriptDir "search_pool.py"

# Escape dấu gạch chéo ngược cho JSON
$JsonPythonExe = $PythonExe.Replace("\", "\\")
$JsonSearchScript = $SearchScript.Replace("\", "\\")

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host "🎉 CÀI ĐẶT THÀNH CÔNG! DƯỚI ĐÂY LÀ ĐOẠN CẤU HÌNH DÀNH RIÊNG CHO MÁY CỦA BẠN:" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. Cấu hình JSON (Antigravity Global, Antigravity IDE, Claude Desktop, Cursor):" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------------------------"
Write-Host @"
{
  "mcpServers": {
    "unified-search": {
      "command": "$JsonPythonExe",
      "args": [
        "$JsonSearchScript"
      ]
    }
  }
}
"@

Write-Host ""
Write-Host "2. Lệnh thêm nhanh cho Claude Code CLI (PowerShell):" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------------------------"
Write-Host "claude mcp add unified-search `"$PythonExe`" `"$SearchScript`""

Write-Host ""
Write-Host "3. Cấu hình Hermes Agent (%USERPROFILE%\.hermes\config.yaml):" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------------------------"
Write-Host @"
mcp_servers:
  unified-search:
    command: "$($PythonExe.Replace('\', '/'))"
    args:
      - "$($SearchScript.Replace('\', '/'))"
    env: {}
    timeout: 120
    connect_timeout: 30
"@

Write-Host ""
Write-Host "4. Cấu hình DeepSeek Harness (%USERPROFILE%\.dsh\profiles\<profile>\cordis.patch.yml):" -ForegroundColor Cyan
Write-Host "------------------------------------------------------------------------------"
Write-Host @"
- id: mcp-unified-search
  name: "@deepseek-ai/dsh-mcp-client"
  config:
    serverName: unified-search
    transport: stdio
    command: $PythonExe
    args:
      - $SearchScript
    env: {}
"@
Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Green
