# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from zhipuai import ZhipuAI

app = Flask(__name__)
# 允许跨域访问，这样你的网页才能请求这个后端
CORS(app) 

# 【⚠️关键步骤】：请在这里粘贴你的完整 API Key
# 注意：保留双引号，把 sk-... 或 id.secret 格式的完整字符串填在引号中间
API_KEY = "3587374a1cad4009b547b5153f2bd61a.zE8NyebFPxWXTxCh"

# 初始化智谱 AI 客户端
client = ZhipuAI(api_key=API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 1. 获取网页发来的消息
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"error": "没有收到消息内容"}), 400

        # 2. 调用智谱 AI (使用 GLM-4-Flash 模型)
        response = client.chat.completions.create(
            model="glm-4-flash",  # 这里指定模型
            messages=[
                {"role": "system", "content": "你是一个有用的智能助手。"},
                {"role": "user", "content": user_message}
            ],
        )

        # 3. 获取 AI 的回复内容
        ai_reply = response.choices[0].message.content
        
        # 4. 把回复发给网页
        return jsonify({"reply": ai_reply})

    except Exception as e:
        # 如果出错（比如 Key 填错了），返回错误信息
        return jsonify({"error": str(e)}), 500
