@echo off
chcp 65001 >nul
title 智能教学助手 一键启动

echo.
echo =================================================
echo     智能教学助手（基于DeepSeek） 一键启动中...
echo =================================================
echo.

echo [1/4] 正在检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 【错误】未检测到 Python 环境！
    echo 请先安装 Python 3.9 或更高版本（推荐从 https://www.python.org 下载）
    echo 安装时请务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [2/4] 正在检查并升级 pip...
python -m pip install --upgrade pip >nul 2>&1
if %errorlevel% neq 0 (
    echo 【警告】pip 升级失败，但将继续尝试安装依赖
) else (
    echo pip 已升级到最新版本
)

echo [3/4] 正在检查并自动安装所需库（streamlit 和 openai）...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo   - 正在安装 streamlit...
    python -m pip install streamlit
)

python -c "import openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo   - 正在安装 openai...
    python -m pip install openai
)

echo.
echo [4/4] 所有依赖已准备就绪，正在启动教学助手...

echo.
echo =================================================
echo 系统启动成功！浏览器即将打开教学助手界面
echo 如未自动打开，请手动访问： http://localhost:8501
echo =================================================
echo.

streamlit run app.py --server.port 8501

echo.
echo 如需关闭，请直接关闭此窗口
pause