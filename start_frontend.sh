#!/bin/bash

# CRM助手 - 前端服务启动脚本

echo "🌐 启动CRM助手前端服务..."

# 进入前端目录
cd frontend

# 检查是否存在.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到前端.env文件，从.env.example复制..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ 已创建前端.env文件"
    fi
fi

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

# 启动服务
echo "🚀 启动前端服务 (端口3000)..."
npm start 