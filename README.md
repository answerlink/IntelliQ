
# IntelliQ
## 介绍
IntelliQ 是一个开源项目，旨在提供一个基于大型语言模型（LLM）的多轮问答系统。该系统结合了先进的意图识别和词槽填充（Slot Filling）技术，致力于提升对话系统的理解深度和响应精确度。本项目为开发者社区提供了一个灵活、高效的解决方案，用于构建和优化各类对话型应用。

<img src="https://github.com/answerlink/IntelliQ/blob/main/images/demo.gif"  height="388" width="690">

<img src="https://github.com/answerlink/IntelliQ/blob/main/images/slot_multi-turn-flow.png"  height="388" width="690">

## 特性
1. 多轮对话管理：能够处理复杂的对话场景，支持连续多轮交互。
2. 意图识别：准确判定用户输入的意图，支持自定义意图扩展。
3. 词槽填充：动态识别并填充关键信息（如时间、地点、对象等）。
4. 接口槽技术：直接与外部APIs对接，实现数据的实时获取和处理。
5. 自适应学习：不断学习用户交互，优化回答准确性和响应速度。
6. 易于集成：提供了详细的API文档，支持多种编程语言和平台集成。

## 安装和使用

确保您已安装 git、python3。然后执行以下步骤：
```
# 安装步骤
git clone https://github.com/answerlink/IntelliQ.git
cd IntelliQ
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 修改配置
配置项在 config/__init__.py
GPT_URL: 可修改为OpenAI的代理地址
API_KEY: 修改为ChatGPT的ApiKey

# 启动
python app.py

# 可视化调试可以浏览器打开 demo/user_input.html 或 127.0.0.1:5000
```

## 文档

查阅详细的API文档和使用说明，请访问 [文档链接]。

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
