#!/bin/bash

# CRM助手 - 开发环境一键启动脚本
# 支持macOS和Linux系统

echo "🚀 CRM助手开发环境启动中..."

# 检查是否存在.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，从.env.example复制..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ 已创建.env文件"
    else
        echo "❌ 未找到.env.example文件，请手动创建.env文件"
        exit 1
    fi
fi

# 检查前端.env文件
if [ ! -f "frontend/.env" ]; then
    echo "⚠️  未找到前端.env文件，从前端.env.example复制..."
    if [ -f "frontend/.env.example" ]; then
        cp frontend/.env.example frontend/.env
        echo "✅ 已创建前端.env文件"
    else
        echo "❌ 未找到前端.env.example文件，请手动创建前端.env文件"
        exit 1
    fi
fi

# 检查Python虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活Python虚拟环境..."
source venv/bin/activate

# 安装Python依赖
echo "📋 安装Python依赖..."
pip install -r requirements.txt

# 检查Node.js依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd frontend
    npm install
    cd ..
fi

# 创建启动函数
start_backend() {
    echo "🖥️  启动后端服务 (端口5050)..."
    source venv/bin/activate
    python app.py
}

start_frontend() {
    echo "🌐 启动前端服务 (端口3000)..."
    cd frontend
    npm start
}

# 检查端口是否被占用
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  端口 $1 已被占用，请先关闭占用该端口的程序"
        return 1
    fi
    return 0
}

# 检查必要端口
if ! check_port 5050; then
    echo "❌ 后端端口5050被占用"
    exit 1
fi

if ! check_port 3000; then
    echo "❌ 前端端口3000被占用"
    exit 1
fi

echo ""
echo "🎯 准备启动服务..."
echo "   后端地址: http://localhost:5050"
echo "   前端地址: http://localhost:3000"
echo "   API文档: http://localhost:5050/api/health"
echo ""
echo "💡 提示: 使用 Ctrl+C 停止服务"
echo ""

# 并行启动前后端
if command -v gnome-terminal >/dev/null; then
    # Linux with gnome-terminal
    gnome-terminal --tab --title="后端服务" -- bash -c "$(declare -f start_backend); start_backend; exec bash"
    gnome-terminal --tab --title="前端服务" -- bash -c "$(declare -f start_frontend); start_frontend; exec bash"
elif command -v osascript >/dev/null; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && python app.py"'
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)/frontend"' && npm start"'
else
    # 无图形界面，顺序启动
    echo "🔄 后台启动后端服务..."
    start_backend &
    BACKEND_PID=$!
    
    sleep 3
    echo "🔄 启动前端服务..."
    start_frontend
    
    # 清理函数
    cleanup() {
        echo ""
        echo "🛑 停止服务..."
        kill $BACKEND_PID 2>/dev/null
        exit 0
    }
    
    trap cleanup SIGINT SIGTERM
    wait
fi

echo "✅ 启动完成！" 