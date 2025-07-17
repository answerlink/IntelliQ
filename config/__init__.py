print("Config package initialized.")

DEBUG = True

# MODEL ------------------------------------------------------------------------

# 模型支持OpenAI规范接口
GPT_URL = 'https://api.siliconflow.cn/v1/chat/completions'
MODEL = 'Qwen/Qwen3-32B'
API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SYSTEM_PROMPT = 'You are a helpful assistant.'

# MODEL ------------------------------------------------------------------------

# API CONFIGURATION ------------------------------------------------------------------------

# API基础地址
API_BASE_URL = 'http://xxxxxxx:xxxx'

# 场景配置API地址(已弃用)
SCENE_CONFIG_API_URL = f'{API_BASE_URL}/api/mock_slots'

# 场景处理API地址模板
SCENE_API_URL_TEMPLATE = f'{API_BASE_URL}/api/{{scene_name}}'

# API请求超时时间（秒）
API_TIMEOUT = 10

# API CONFIGURATION ------------------------------------------------------------------------

# CONFIGURATION ------------------------------------------------------------------------

# 意图相关性判断阈值0-1（已废弃，保留用于兼容性）
RELATED_INTENT_THRESHOLD = 0.5

# 聊天记录数量（发送给LLM的历史消息条数）
CHAT_HISTORY_COUNT = 3

# 无场景识别的默认响应
NO_SCENE_RESPONSE = "您好，请问您需要办理什么业务？"

# API结果处理提示词
API_RESULT_PROMPT = "以下是查询的结果，请向用户解释，禁止使用markdown：\n\n{api_result}："

# CONFIGURATION ------------------------------------------------------------------------
