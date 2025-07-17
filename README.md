
# IntelliQ
## 介绍
IntelliQ 是一个开源项目，旨在提供一个基于大型语言模型（LLM）的多轮问答系统。该系统结合了先进的意图识别和词槽填充（Slot Filling）技术，致力于提升对话系统的理解深度和响应精确度。本项目为开发者社区提供了一个灵活、高效的解决方案，用于构建和优化各类对话型应用。

<img src="https://github.com/answerlink/IntelliQ/blob/main/images/demo.gif"  height="388" width="690">

<img src="https://github.com/answerlink/IntelliQ/blob/main/images/slot_multi-turn-flow.png"  height="388" width="690">

## 特性
1. **多轮对话管理**：能够处理复杂的对话场景，支持连续多轮交互。
2. **意图识别**：准确判定用户输入的意图，支持自定义意图扩展。
3. **词槽填充**：动态识别并填充关键信息（如时间、地点、对象等）。
4. **接口槽技术**：直接与外部APIs对接，实现数据的实时获取和处理。
5. **前后端分离**：React前端 + Flask后端，支持现代化Web开发模式。
6. **流式AI聊天**：支持Server-Sent Events (SSE)，实现实时聊天体验。
7. **跨域支持**：内置CORS配置，支持本地开发和生产部署。
8. **环境配置**：灵活的环境变量配置，支持开发/生产环境切换。
9. **一键启动**：提供跨平台启动脚本，团队成员无需手动配置。
10. **易于集成**：提供了详细的API文档，支持多种编程语言和平台集成。

## 安装和使用

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 7+

### 🚀 快速启动（推荐）

**一键启动前后端服务：**

macOS/Linux:
```bash
./start_dev.sh
```

Windows:
```cmd
start_dev.cmd
```

### 📋 手动安装步骤

确保您已安装 git、python3、node.js。然后执行以下步骤：

**1. 克隆代码**
```bash
git clone https://github.com/answerlink/IntelliQ.git
cd IntelliQ
```

**2. 后端配置**
```bash
# 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装Python依赖
pip install -r requirements.txt
```

**3. 前端配置**
```bash
cd frontend
npm install
cd ..
```

**4. 环境配置**
- 复制 `.env.example` 为 `.env` 并根据需要修改配置
- 复制 `frontend/.env.example` 为 `frontend/.env` 并根据需要修改配置

**5. 启动服务**
```bash
# 方式1：分别启动
./start_backend.sh    # 启动后端 (端口5050)
./start_frontend.sh   # 启动前端 (端口3000)

# 方式2：手动启动
python app.py         # 后端
cd frontend && npm start  # 前端
```

**访问地址：**
- 前端界面：http://localhost:3000
- 后端API：http://localhost:5050
- API健康检查：http://localhost:5050/api/health

### 🧪 测试联调

启动后端服务后，运行测试脚本验证联调状态：

```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 运行测试
python test_connection.py
```

该脚本会测试：
- 后端健康检查
- LLM聊天接口
- 模拟槽位接口
- CORS跨域配置

## 📚 文档

- **[前后端联调说明](./前后端联调说明.md)** - 详细的前后端联调指南
- **[配置说明](./config.py)** - 环境变量和配置文件说明
- **[API接口文档](#api接口)** - RESTful API接口说明

### 🔗 API接口

#### 健康检查
```
GET /api/health
```

#### 流式AI聊天
```
POST /api/llm_chat
Content-Type: application/json
Accept: text/event-stream

{
  "messages": [],
  "user_input": "用户输入",
  "session_id": "可选的会话ID"
}
```

#### 获取模拟槽位
```
GET /api/mock_slots
```

#### 重置会话
```
POST /api/reset_session
{
  "session_id": "会话ID"
}
```

更多详细信息请查看 [前后端联调说明](./前后端联调说明.md)。

## 贡献

非常欢迎和鼓励社区贡献。如果您想贡献代码，请遵循以下步骤：

    Fork 仓库
    创建新的特性分支 (git checkout -b feature/AmazingFeature)
    提交更改 (git commit -m 'Add some AmazingFeature')
    推送到分支 (git push origin feature/AmazingFeature)
    开启Pull Request

查看 [CONTRIBUTING.md](https://github.com/answerlink/IntelliQ/blob/main/CONTRIBUTING.md)  了解更多信息。

### All Thanks To Our Contributors:
<a href="https://github.com/answerlink/IntelliQ/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=answerlink/IntelliQ" />
</a>

## License

**Apache License, Version 2.0**

## 版本更新

v1.3 2024-1-15 集成通义千问线上模型

v1.2 2023-12-24 支持Qwen私有化模型

v1.1 2023-12-21 改造通用场景处理器；完成高度抽象封装；提示词调优

v1.0 2023-12-17 首次可用更新；框架完成

v0.1 2023-11-23 首次更新；流程设计
