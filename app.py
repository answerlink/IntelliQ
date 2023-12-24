# encoding=utf-8
from models.chatbot_model import ChatbotModel
from utils.app_init import before_init
from utils.helpers import load_all_scene_configs
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 实例化ChatbotModel
chatbot_model = ChatbotModel(load_all_scene_configs())


@app.route('/multi_question', methods=['POST'])
def api_multi_question():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chatbot_model.process_multi_question(question)
    return jsonify({"answer": response})


if __name__ == '__main__':
    before_init()
    app.run(port=5000, debug=True)
