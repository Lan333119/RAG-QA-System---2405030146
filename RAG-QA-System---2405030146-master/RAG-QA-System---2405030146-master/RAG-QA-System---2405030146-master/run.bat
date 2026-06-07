@echo off
echo ========================================
echo   RAG 智能问答系统 - 自动运行脚本
echo ========================================
echo.

REM 检查 Ollama 是否运行
echo [1/4] 检查 Ollama 服务...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✓ Ollama 服务已运行
) else (
    echo ✗ 未检测到 Ollama 服务！
    echo 请先启动 Ollama 后再运行此脚本
    pause
    exit /b 1
)

echo.
echo [2/4] 检查模型...
echo 检查 nomic-embed-text...
ollama list | findstr "nomic-embed-text" >nul
if errorlevel 1 (
    echo 未找到 nomic-embed-text，正在下载...
    ollama pull nomic-embed-text
) else (
    echo ✓ nomic-embed-text 已安装
)

echo 检查 qwen2:1.5b...
ollama list | findstr "qwen2:1.5b" >nul
if errorlevel 1 (
    echo 未找到 qwen2:1.5b，正在下载...
    ollama pull qwen2:1.5b
) else (
    echo ✓ qwen2:1.5b 已安装
)

echo.
echo [3/4] 启动 Streamlit 应用...
echo.

REM 启动应用
echo ========================================
echo   应用启动中，请稍候...
echo ========================================
echo.

py -m streamlit run app.py

echo.
echo 应用已关闭
pause
