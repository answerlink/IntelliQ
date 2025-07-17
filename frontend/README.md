# 电信业务AI问答系统前端

## 项目简介
本前端实现为运营商AI智能体产品的Web端问答交互界面，支持多轮对话、多业务办理流程模拟，与后端API无缝集成。

## 目录结构
- public/         # 静态资源与index.html
- src/
  - App.jsx      # 主应用入口，tab多对话
  - index.js     # React入口
  - App.css      # 全局样式
  - components/  # 主要UI组件
    - ChatBox.jsx           # 聊天主窗口
    - MessageBubble.jsx     # 聊天气泡
    - SlotFiller.jsx        # 卡槽补全区
    - KnowledgeCitation.jsx # 知识库引用区
- api/
  - aiApi.js     # 封装后端API请求

## 功能特性
- 多tab聊天对话，支持历史记录不丢失
- 新对话一键添加
- 聊天输入框支持快捷发送
- 聊天气泡AI进度、知识库引用区
- 自动卡槽补全与业务流程联动（mock_slots自动适配）
- 响应式适配桌面与移动端

## 启动方式
```bash
cd frontend
npm install
npm start
```
默认端口3000，需后端API服务（如Flask）已启动。

## API联调说明
- 主要通过`/api/faq`、`/api/mock_slots`等接口与后端联动。
- 可在`api/aiApi.js`中自定义API路径。
- 所有接口需结构化返回，详见后端文档。

## 依赖
- React 18
- Ant Design 5
- Axios
- react-router-dom

## 其他
如需扩展业务办理流程、知识库引用、卡槽补全等功能，请参考`components/`和`api/`目录代码。