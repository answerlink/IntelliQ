#!/bin/bash

# CRM助手 - 后端服务启动脚本

echo "🖥️ 启动CRM助手后端服务..."

# 检查是否存在.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，从.env.example复制..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ 已创建.env文件"
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

# 安装依赖
echo "📋 安装Python依赖..."
pip install -r requirements.txt

# 启动服务
echo "🚀 启动后端服务 (端口5050)..."
python app.py 