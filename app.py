# encoding=utf-8
from models.chatbot_model import ChatbotModel
from utils.app_init import before_init
from utils.helpers import load_scene_templates
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 加载场景模板
scene_templates = load_scene_templates('scene_config/scene_templates.json')

# 实例化ChatbotModel
chatbot_model = ChatbotModel(scene_templates)


@app.route('/multi_question', methods=['POST'])
def api_multi_question():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chatbot_model.process_multi_question(question)
    return jsonify({"answer": response})


@app.route('/', methods=['GET'])
def index():
    return send_file('./demo/user_input.html')

if __name__ == '__main__':
    before_init()
    app.run(port=5000, debug=True)
