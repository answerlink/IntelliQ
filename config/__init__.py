print("Config package initialized.")

DEBUG = True

# MODEL ------------------------------------------------------------------------

# 模型支持OpenAI规范接口
GPT_URL = 'https://api.openai.com/v1/chat/completions'
MODEL = 'gpt-3.5-turbo'
API_KEY = 'sk-xxxxxx'
SYSTEM_PROMPT = 'You are a helpful assistant.'

# MODEL ------------------------------------------------------------------------

# CONFIGURATION ------------------------------------------------------------------------

# 意图相关性判断阈值0-1
RELATED_INTENT_THRESHOLD = 0.5

# CONFIGURATION ------------------------------------------------------------------------
