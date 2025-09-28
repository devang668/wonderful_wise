@echo off
chcp 65001 >nul
echo 🎤 迅飞语音听写项目 - 本地服务器
echo ================================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.6+
    echo 💡 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查必要文件
if not exist "index.html" (
    echo ❌ 缺少 index.html 文件
    pause
    exit /b 1
)

if not exist "js\xf-voice-dictation.js" (
    echo ❌ 缺少 js\xf-voice-dictation.js 文件
    pause
    exit /b 1
)

if not exist "js\crypto-js.min.js" (
    echo ❌ 缺少 js\crypto-js.min.js 文件
    pause
    exit /b 1
)

echo ✅ 文件检查完成，启动服务器...
echo.

REM 启动Python服务器
python start-server.py

pause
