# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os
from dotenv import load_dotenv  # 匯入 dotenv 套件

# 載入 .env 檔案中的環境變數
load_dotenv()

app = Flask(__name__)

# 從環境變數讀取設定
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key") # 如果沒讀到，就用後面那個預設值

# 模擬一組帳號密碼
USERS = {
    "admin": "1234",
    "student": "iot2025"
}

# 設定 Ollama 的 API 位置 (因為都在樹莓派本機跑，所以是 localhost)
OLLAMA_API_URL = "http://localhost:11434/api/chat"

DEFAULT_SYSTEM_PROMPT = "你是 Dcard 科技業版的嘴砲鄉民：反諷、吐槽、機智、短句。只針對內容的邏輯、職場常識、話術與情境吐槽；不得做人身攻擊與歧視，不猜測或散播個資。回覆 1–4 句，像真人留言；不要教育口吻、不要安慰、不要太多背景解釋。只輸出留言。"

# --- 路由設定 ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('chat_room'))
        else:
            return render_template('login.html', msg="帳號或密碼錯誤")
            
    return render_template('login.html')

@app.route('/chat')
def chat_room():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', name=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/ask_ai', methods=['POST'])
def api_ask_ai():
    if 'user' not in session:
        return jsonify({'reply': '你沒有權限，請先登入'}), 401

    # 從前端取得所有參數
    data = request.get_json()
    model_name = data.get('model', 'unsloth_model') # 預設模型
    system_prompt_text = data.get('system_prompt', DEFAULT_SYSTEM_PROMPT)
    title = data.get('title', '')
    content = data.get('content', '')

    # 依照訓練的格式，合併標題與內文
    user_message = f"【標題】{title}\n【內文】{content}"

    # 準備傳給 Ollama 的資料 (Payload)
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_prompt_text
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "stream": False,  # 不使用串流，一次回傳
        "options": {
            "temperature": 0.7
        }
    }

    try:
        # 呼叫 Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            # 取得 AI 回覆
            ai_reply = result['message']['content']
            return jsonify({'reply': ai_reply})
        else:
            return jsonify({'reply': f"Ollama 發生錯誤: {response.text}"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reply': "連線失敗，請確認樹莓派上的 Ollama 是否有啟動 (systemctl status ollama)"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)