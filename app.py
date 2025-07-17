# encoding=utf-8
import json
import logging
import uuid
from threading import Lock
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS

from models.chatbot_model import ChatbotModel
from utils.app_init import before_init
from utils.helpers import load_all_scene_configs
from app_config import config

app = Flask(__name__)

# 使用配置文件中的CORS设置
CORS(app, origins="*", supports_credentials=True)

# 实例化ChatbotModel
chatbot_model = ChatbotModel(load_all_scene_configs())

# 会话存储 - 生产环境应使用Redis或数据库
sessions = {}
sessions_lock = Lock()

def get_or_create_session(session_id=None):
    """获取或创建会话"""
    with sessions_lock:
        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        if session_id not in sessions:
            sessions[session_id] = {
                'messages': [],
                'context': {},
                'created_at': None
            }
        
        return session_id, sessions[session_id]

@app.route('/multi_question', methods=['POST'])
def api_multi_question():
    """多轮问答接口（原有接口保持兼容）"""
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chatbot_model.process_multi_question(question)
    return jsonify({"answer": response})

@app.route(f'{config.API_PREFIX}/llm_chat', methods=['POST'])
def api_llm_chat():
    """流式AI聊天接口"""
    data = request.json
    messages = data.get('messages', [])
    user_input = data.get('user_input', '')
    session_id = data.get('session_id')
    
    if not user_input:
        return jsonify({"error": "No user_input provided"}), 400
    
    # 获取或创建会话
    session_id, session_data = get_or_create_session(session_id)
    
    # 检查是否是流式请求
    accept_header = request.headers.get('Accept', '')
    is_stream = 'text/event-stream' in accept_header
    
    try:
        if is_stream:
            # 流式响应
            def generate():
                try:
                    import time
                    
                    # 处理消息
                    response = chatbot_model.process_multi_question(user_input)
                    
                    # 流式输出：逐字符发送
                    buffer = ""
                    for i, char in enumerate(response):
                        buffer += char
                        
                        # 每隔几个字符或遇到标点符号时发送一次
                        if len(buffer) >= 3 or char in '。！？，、；：':
                            # 发送SSE格式数据
                            yield f"data: {buffer}\n\n"
                            buffer = ""
                            # 添加小延迟模拟真实流式体验
                            time.sleep(0.05)
                    
                    # 发送剩余内容
                    if buffer.strip():
                        yield f"data: {buffer}\n\n"
                    
                    # 发送完成标记
                    yield "data: [DONE]\n\n"
                
                except Exception as e:
                    logging.error(f"流式处理错误: {str(e)}")
                    yield f"data: [ERROR] {str(e)}\n\n"
            
            response = Response(
                generate(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'X-Session-ID': session_id
                }
            )
            return response
        else:
            # 非流式响应
            response = chatbot_model.process_multi_question(user_input)
            return jsonify({
                "response": response,
                "session_id": session_id
            })
    
    except Exception as e:
        logging.error(f"LLM聊天错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route(f'{config.API_PREFIX}/mock_slots', methods=['GET'])
def api_mock_slots():
    """获取模拟槽位数据"""
    mock_data = {
        "slots": {
            "phone_number": "13812345678",
            "user_name": "张三",
            "service_type": "流量套餐",
            "package_type": "月套餐"
        },
        "available_services": [
            {"id": 1, "name": "流量套餐", "description": "包月流量服务"},
            {"id": 2, "name": "通话套餐", "description": "包月通话服务"},
            {"id": 3, "name": "短信套餐", "description": "包月短信服务"}
        ]
    }
    return jsonify(mock_data)

@app.route(f'{config.API_PREFIX}/reset_session', methods=['POST'])
def api_reset_session():
    """重置会话"""
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({"error": "No session_id provided"}), 400
    
    with sessions_lock:
        if session_id in sessions:
            del sessions[session_id]
    
    return jsonify({"message": "Session reset successfully", "session_id": session_id})

@app.route(f'{config.API_PREFIX}/health', methods=['GET'])
def api_health():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "backend_url": config.backend_url,
        "environment": config.FLASK_ENV
    })

@app.route('/', methods=['GET'])
def index():
    """主页"""
    return send_file('./demo/user_input.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "API endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    before_init()
    
    # 配置日志
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print(f"🚀 后端服务启动中...")
    print(f"📍 地址: {config.backend_url}")
    print(f"🌍 环境: {config.FLASK_ENV}")
    print(f"🔗 允许跨域: {', '.join(config.CORS_ORIGINS)}")
    
    app.run(
        host=config.BACKEND_HOST,
        port=config.BACKEND_PORT,
        debug=config.FLASK_DEBUG
    )
