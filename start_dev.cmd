@echo off
chcp 65001 >nul
title CRM助手 - 开发环境启动

echo 🚀 CRM助手开发环境启动中...

:: 检查是否存在.env文件
if not exist ".env" (
    echo ⚠️  未找到.env文件，从.env.example复制...
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✅ 已创建.env文件
    ) else (
        echo ❌ 未找到.env.example文件，请手动创建.env文件
        pause
        exit /b 1
    )
)

:: 检查前端.env文件
if not exist "frontend\.env" (
    echo ⚠️  未找到前端.env文件，从前端.env.example复制...
    if exist "frontend\.env.example" (
        copy "frontend\.env.example" "frontend\.env" >nul
        echo ✅ 已创建前端.env文件
    ) else (
        echo ❌ 未找到前端.env.example文件，请手动创建前端.env文件
        pause
        exit /b 1
    )
)

:: 检查Python虚拟环境
if not exist "venv" (
    echo 📦 创建Python虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败，请检查Python安装
        pause
        exit /b 1
    )
)

:: 激活虚拟环境
echo 🔧 激活Python虚拟环境...
call venv\Scripts\activate.bat

:: 安装Python依赖
echo 📋 安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 安装Python依赖失败
    pause
    exit /b 1
)

:: 检查Node.js依赖
if not exist "frontend\node_modules" (
    echo 📦 安装前端依赖...
    cd frontend
    npm install
    if errorlevel 1 (
        echo ❌ 安装前端依赖失败
        pause
        exit /b 1
    )
    cd ..
)

echo.
echo 🎯 准备启动服务...
echo    后端地址: http://localhost:5050
echo    前端地址: http://localhost:3000
echo    API文档: http://localhost:5050/api/health
echo.
echo 💡 提示: 关闭窗口以停止服务
echo.

:: 启动后端服务（新窗口）
start "后端服务 - CRM助手" cmd /k "cd /d %cd% && call venv\Scripts\activate.bat && python app.py"

:: 等待后端启动
timeout /t 3 /nobreak >nul

:: 启动前端服务（新窗口）
start "前端服务 - CRM助手" cmd /k "cd /d %cd%\frontend && npm start"

echo ✅ 启动完成！
echo 💻 后端和前端服务已在新窗口中启动
echo 🌐 请在浏览器中访问: http://localhost:3000
echo.

pause 