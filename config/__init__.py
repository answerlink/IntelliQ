print("Config package initialized.")

DEBUG = True

# MODEL ------------------------------------------------------------------------

USE_MODEL = 'chatGPT'  # 「chatGPT， Qwen， tongyiQwen」

# OpenAI https://api.openai.com/v1/chat/completions
GPT_URL = 'https://api.openai.com/v1/chat/completions'
API_KEY = 'sk-xxxxxx'

# Qwen
Qwen_URL = 'https://www.your-local-Qwenurl/'

# tongyiQwen
DASHSCOPE_API_KEY = "sk-xxxxxx"

# MODEL ------------------------------------------------------------------------

# CONFIGURATION ------------------------------------------------------------------------

# 意图相关性判断阈值0-1
RELATED_INTENT_THRESHOLD = 0.5

# CONFIGURATION ------------------------------------------------------------------------
