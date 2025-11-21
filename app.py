# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os
from dotenv import load_dotenv  # 匯入 dotenv 套件

# 1. 載入 .env 檔案中的環境變數
load_dotenv()

app = Flask(__name__)

# 2. 從環境變數讀取設定
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key") # 如果沒讀到，就用後面那個預設值
API_KEY = os.getenv("GEMINI_API_KEY")

# 檢查是否有讀取到 API Key (教學用，方便學生除錯)
if not API_KEY:
    raise ValueError("錯誤：讀取不到 API Key。請確認你有建立 .env 檔案，且裡面有 GEMINI_API_KEY 設定。")

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# 模擬一組帳號密碼
USERS = {
    "admin": "1234",
    "student": "iot2025"
}

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
    ''' 
    這是與 Gemini API 互動的函式
    會發送使用者訊息到 Gemini API，並取得回覆

    請同學完成這個函式的內容
    請同學完成這個函式的內容
    請同學完成這個函式的內容
    '''

    if 'user' not in session:
        return jsonify({'reply': '你沒有權限，請先登入'}), 401

    # 從前端取得使用者訊息
    data = request.get_json()
    user_message = data.get('message', '')

    # 這串是把 system prompt 跟使用者訊息組合成完整的 prompt
    system_prompt = "你是一個物聯網課程的助教，請用繁體中文簡短回答學生的問題。"
    # full_prompt 是要送給 Gemini API 的內容
    full_prompt = f"{system_prompt}\n\n學生問：{user_message}"

    # 請自己串接上次的 ask_gemini 函式
    # 請自己串接上次的 ask_gemini 函式
    # 請自己串接上次的 ask_gemini 函式
    ai_reply = "請放上串接 Gemini API 的回覆"
    return jsonify({'reply': ai_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)