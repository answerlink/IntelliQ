print("Config package initialized.")

DEBUG = True

# MODEL ------------------------------------------------------------------------

USE_MODEL = 'tongyiQwen'  # 「chatGPT， Qwen， tongyiQwen」

# OpenAI https://api.openai.com/v1/chat/completions
GPT_URL = 'api.openai.com/v1/chat/completions'
API_KEY = 'sk-xxxxxx'

# Qwen
Qwen_URL = 'https://www.your-local-Qwenurl/'

# tongyiQwen
DASHSCOPE_API_KEY = "sk-713c76b6b23d44b6a30480819dcb0ca2"

# MODEL ------------------------------------------------------------------------

# CONFIGURATION ------------------------------------------------------------------------

# 意图相关性判断阈值0-1
RELATED_INTENT_THRESHOLD = 0.5

# CONFIGURATION ------------------------------------------------------------------------
